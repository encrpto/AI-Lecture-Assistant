import streamlit as st
import requests

st.set_page_config(page_title="AI Lecture Assistant")

st.title("🎥 AI Lecture Assistant")


file = st.file_uploader("Upload Lecture Video", type=["mp4"])

if file:
    if st.button("Process Lecture"):
        with st.spinner("Processing..."):
            res = requests.post(
                "http://localhost:8000/process",
                files={"file": file}
            )
            st.success("Processed!")


st.header("Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(msg)

query = st.chat_input("Ask question")

if query:
    st.session_state.messages.append(("user", query))

    with st.chat_message("assistant"):
        res = requests.post(
            "http://localhost:8000/chat",
            json={"question": query}
        )

        answer = res.json()["answer"]
        st.markdown(answer)

    st.session_state.messages.append(("assistant", answer))