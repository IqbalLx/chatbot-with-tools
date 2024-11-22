import json
import os
from dotenv import load_dotenv
import psycopg2 as pg
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from modules.llm import llama_chat_completion, SYSTEM_PROMPT
from modules.user_repository import get_user
from modules.pdf_tools import create_skck, create_resident_certificate

if os.path.exists(".env"):
    load_dotenv(".env")

db = pg.connect(os.environ["POSTGRES_CONNSTRING"])

st.title("💬 GovernBOT")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

for msg in st.session_state.messages:
    if msg["role"] == 'system':
        if "filepath" in msg["content"]:
            _, filepath = msg["content"].split("::")
            pdf_viewer(filepath)
        continue

    st.chat_message(msg["role"]).write(msg["content"])

if question := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    bot_response, tool_calls = llama_chat_completion(st.session_state.messages)
    if tool_calls is not None:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            nik = function_args.get("nik")
            if nik is None:
                st.session_state.messages.append({"role": "system", "content": "NIK is not provided, please ask user to provide their NIK"})
                continue

            user = get_user(db, nik)
            if user is None:
                st.session_state.messages.append({"role": "system", "content": "After checking database, unfortunately the user is not found in our system, please ask user to reinput and double-check their NIK"})
                continue

            if function_name == 'create_skck':
                filepath = create_skck(user)
            elif function_name == 'create_resident_certificate':
                filepath = create_resident_certificate(user)
            
            st.session_state.messages.append({"role": "system", "content": "certificate successfully created, inform user about this"})
            st.session_state.messages.append({"role": "system", "content": f"filepath::{filepath}"})
            pdf_viewer(filepath)

        bot_response, _ = llama_chat_completion(st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.chat_message("assistant").write(bot_response)

