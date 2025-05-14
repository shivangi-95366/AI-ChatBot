import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')

@cl.on_chat_start
async def start_chat():
    # Set default settings
    
    settings = {
        "temperature": 0.7,  # Controls creativity (0.0-1.0)
        "max_tokens": 2000,  # Maximum response length
    }
    
    cl.user_session.set("settings", settings)
    
    # Welcome message
    welcome_message = """🌟 **Welcome to Shivangi's AI ChatBot!** 🌟  
🤖 *Powered by Google Gemini 2.0 Flash*

I can assist you with a wide range of tasks, including:

✅ Answering questions across any topic  
📊 Interpreting and analyzing data  
📝 Generating creative and professional content  
🛠️ Solving technical and coding problems  
💡 Brainstorming ideas and strategies

Just type your question or request below, and I’ll be happy to help!

*Let’s get started!* 🚀"""

    
    await cl.Message(content=welcome_message).send()

@cl.on_message
async def main(message: cl.Message):
    settings = cl.user_session.get("settings")
    user_input = message.content.lower().strip()

    # List of possible identity-related queries
    identity_queries = [
        "who built you", "who created you", "who made you", "who developed you",
        "who is your creator", "who is your developer", "who programmed you",
        "who coded you", "who designed you", "who is behind you",
        "who made this chatbot", "who is the maker", "who's your creator",
        "who built this bot", "who built this assistant", "who are you built by",
        "who developed this app", "tell me about your creator", "who owns you",
        "who is the author", "who is your author", "who made this app",
        "who created this assistant", "who is your engineer", "who designed this bot"
    ]

    # Check if any trigger phrase is present
    if any(query in user_input for query in identity_queries):
        custom_reply = """
🙋‍♀️ I was built by **Shivangi Gupta**,  
🚀 Powered by **Google Gemini 2.0 Flash**  
💻 Running on **Chainlit** — an open-source LLM UI framework.

Here to assist you with anything you need! 😊
"""
        await cl.Message(content=custom_reply).send()
        return

    # Default Gemini response handling
    msg = cl.Message(content="")
    await msg.send()

    try:
        response = model.generate_content(
            message.content,
            generation_config=genai.types.GenerationConfig(
                temperature=settings["temperature"],
                max_output_tokens=settings["max_tokens"]
            )
        )
        await cl.Message(content=response.text).send()

    except Exception as e:
        await cl.Message(content=f"⚠️ Error: {str(e)}").send()

    # Get settings from session
    settings = cl.user_session.get("settings")
    
    # Create a loading message
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        # Generate response from Gemini
        response = model.generate_content(
            message.content,
            generation_config=genai.types.GenerationConfig(
                temperature=settings["temperature"],
                max_output_tokens=settings["max_tokens"]
            )
        )
        
        # Send the response
        await cl.Message(content=response.text).send()
        
    except Exception as e:
        error_message = f"⚠️ An error occurred: {str(e)}"
        await cl.Message(content=error_message).send()

@cl.on_settings_update
async def update_settings(settings):
    # Update settings when user changes them in UI
    cl.user_session.set("settings", settings)