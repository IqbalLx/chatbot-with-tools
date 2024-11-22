import os
from typing import Tuple, Optional

import openai
from openai.types.chat import ChatCompletionMessageToolCall

SYSTEM_PROMPT = """You are government assistant to assist civiliant to automatically generate government-issue certificate. 
You are equipped with tools to generate Police clearance certificate (SKCK) and resident certificate, make sure every time user ask to generate certificate you ask what their 
government ID or NIK is, NIK is 16 digit long, as it is required for the tools to work. Always response and ask user using Bahasa Indonesia. 
Don't respond your tool usage need in the content. Stick to your tools, don't hallucinate"""

TOOLS = [
    {
      "type": "function",
      "function": {
        "name": "create_skck",
        "description": "Generate Police clearance certificate (SKCK)",
        "parameters": {
          "type": "object",
          "properties": {
            "nik": {
              "type": "string",
              "description": "Provided user government ID or NIK"
            },
          },
          "required": ["nik"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "create_resident_certificate",
        "description": "Generate resident certificate as proof people actually resident in this area",
        "parameters": {
          "type": "object",
          "properties": {
            "nik": {
              "type": "string",
              "description": "Provided user government ID or NIK"
            },
          },
          "required": ["nik"]
        }
      }
    },
  ]

def llama_chat_completion(messages) -> Tuple[str, Optional[ChatCompletionMessageToolCall]]:
    client = openai.OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.environ.get("GROQ_API_KEY")
    )

    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=messages,
        tools=TOOLS,
        tool_choice='auto',
        stream=False
    )

    message = completion.choices[0].message
    chat_resp = message.content
    tool_calls = message.tool_calls

    return str(chat_resp), tool_calls

