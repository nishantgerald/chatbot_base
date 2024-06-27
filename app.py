#!/usr/bin/env python

import os
import dotenv
import argparse
import requests
from flask import jsonify
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_community.chat_message_histories import ChatMessageHistory
import gradio as gr


def load_environment():
    """Load environment variables from a .env file."""
    del os.environ['OPENAI_API_KEY']
    dotenv.load_dotenv()


def parse_arguments():
    """Parse and return the command line arguments."""
    parser = argparse.ArgumentParser(description="Chat with an AI-powered assistant")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--web", action="store_true", help="Run the app as a Gradio web server"
    )
    group.add_argument("--cli", action="store_true", help="Run the app in CLI mode")
    parser.add_argument("--prompt", type=str, help="Input text prompt for CLI mode")
    args = parser.parse_args()
    if args.cli and not args.prompt:
        parser.error("--cli requires --prompt to be specified")
    return args


@tool
def current_weather(latitude: str = "33.79", longitude: str = "-84.36") -> dict:
    """Return the current weather for a given latitude and longitude."""
    api_key = os.getenv("WEATHER_API_KEY")
    url = (
        f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}"
        f"&exclude=minutely,hourly,daily,alerts&appid={api_key}&units=imperial"
    )
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather data"}), 500
    return response.json().get("current", {})


@tool
def google_search(query: str) -> list:
    """Perform a Google search and return the top 5 results."""
    search = GoogleSearchAPIWrapper()
    return search.results(query, 5)


@tool
def url_reader(url: str) -> str:
    """Read the content of a URL and return a summary."""
    llm = initialize_llm()
    loader = WebBaseLoader(url)
    docs = loader.load()
    chain = load_summarize_chain(llm, chain_type="stuff")
    return chain.invoke(docs)


def initialize_llm() -> ChatOpenAI:
    """Initialize and return the language model."""
    return ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo-0125")


def create_agent(llm: ChatOpenAI, tools: list, tool_names: list) -> AgentExecutor:
    """Create and return the agent executor."""
    agent_scratchpad = MessagesPlaceholder(variable_name="agent_scratchpad")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    f"You are a very helpful assistant that can take on various personas if asked to."
                    f"Consider if any of the tools in {tool_names} are useful for the current context. "
                    "If not, don't use the tools. You provide responses in markdown format."
                ),
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


def setup_agent_with_history(
    agent_executor: AgentExecutor, memory: ChatMessageHistory
) -> RunnableWithMessageHistory:
    """Set up and return the agent with message history."""
    return RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    ).with_retry(stop_after_attempt=3)


def chat_response(
    agent_with_chat_history: RunnableWithMessageHistory, message: str
) -> str:
    """Get the chat response from the agent."""
    response = agent_with_chat_history.invoke(
        {"input": message}, config={"configurable": {"session_id": "test-session"}}
    )
    return response["output"]


def main():
    load_environment()
    args = parse_arguments()
    tools = [current_weather, google_search, url_reader]
    tool_names = ["CurrentWeather", "GoogleSearch", "URLReader"]
    llm = initialize_llm()
    agent_executor = create_agent(llm, tools, tool_names)
    memory = ChatMessageHistory(session_id="test-session")
    agent_with_chat_history = setup_agent_with_history(agent_executor, memory)

    if args.web:

        def gradio_chat_response(message, history):
            return chat_response(agent_with_chat_history, message)

        chatbot = gr.ChatInterface(gradio_chat_response, css="footer {visibility: hidden} label.svelte-1b6s6s {visibility: hidden}")
        chatbot.launch(share=True)

    if args.cli:
        response = chat_response(agent_with_chat_history, args.prompt)
        print(response)


if __name__ == "__main__":
    main()
