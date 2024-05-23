# AI-Powered Chatbot

Welcome to this base AI-powered chatbot that combines the power of large language models with practical utilities to assist, entertain, and inform. Built using Python and robust libraries, this chatbot offers both web and command-line interfaces for a dynamic and responsive interaction experience.
This is meant to serve as a chatbot template that you can fork and customize based on your needs (eg: adding more tools or additional agents)

## Capabilities

In addition to regular conversational abilities, this chatbot integrates multiple tools to provide:
- **Current Weather Information**: Fetches and displays current weather conditions based on location.
- **Google Search**: Performs a top-5 Google search and returns the most relevant results.
- **URL Content Reader**: Reads and summarizes content from a provided URL.

Using a sophisticated language model from OpenAI, the chatbot understands and generates human-like text, ensuring a natural conversational experience.

## How to Run

### Requirements
Before starting, ensure Python is installed on your system along with the following packages:
```
Flask==2.2.2
Flask-Bootstrap==3.3.7.1
Flask-Compress==1.12
Flask-Cors==4.0.0
Flask-SQLAlchemy==3.0.3
google-api-core==2.11.0
google-api-python-client==2.86.0
gradio==4.31.5
gradio_client==0.16.4
langchain==0.2.0
langchain-community==0.0.36
langchain-core==0.2.1
langchain-openai==0.1.7
langchain-text-splitters==0.2.0
langchainhub==0.1.15
python-dotenv==1.0.0
requests==2.31.0
```

You'll also need a `.env` file in your project root with necessary API keys (e.g., `WEATHER_API_KEY` for fetching weather data).

### Setting Up
Clone the repository and navigate into the project directory. Install the required Python packages using:
`pip install -r requirements.txt`

### Running the Application
You can choose between a web interface or a command-line interface to run the chatbot:

1. **Web Interface**:
`./app.py –web`

This command starts a Gradio web server allowing you to interact with the bot through a web browser.

2. **Command-Line Interface**:
`./app.py –cli –prompt “Your question here”`

Use this mode for a quick command-line interaction. Replace `"Your question here"` with your query.

## Example Usage

Here’s how to interact with the chatbot:

- Ask about the weather:
> "What's the current weather in Atlanta?"
- Perform a Google search:
> "Top 5 results for AI advancements in 2024"
- Summarize a webpage:
> "Summarize the content of www.example.com"

Explore the functionalities of this AI-powered chatbot, and feel free to fork and use this as a base template for any other smart-chatbots you'd like to create.