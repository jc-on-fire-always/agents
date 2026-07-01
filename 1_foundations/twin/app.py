from openai import OpenAI
# pyrefly: ignore [missing-import]
from context import TWIN_SYSTEM_PROMPT
# pyrefly: ignore [missing-import]
from tools import tools, handle_tool_calls
# pyrefly: ignore [missing-import]
from styles import CSS, JS, EXAMPLES
from dotenv import load_dotenv
import gradio as gr

load_dotenv(override=True)

MODEL_NAME = "gemini-3.5-flash"

import os
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
openai = OpenAI(
    base_url=GEMINI_BASE_URL,
    api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
)

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]


def chat(message, history):
    messages = system + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        tool_calls = message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(message)
        messages.extend(results)
        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    return response.choices[0].message.content


if __name__ == "__main__":
    gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        title="Digital Twin",
        description="Talk to my AI twin about my career",
        chatbot=gr.Chatbot(show_label=False),
    ).launch(css=CSS, js=JS, theme=gr.themes.Base())
