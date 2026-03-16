import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/query"


st.set_page_config(page_title="Clinical MedBot", page_icon="🤖")
st.markdown("""
<style>
    /* Push USER messages to the right */
    div.stChatMessage.st-emotion-cache-1c7y2kd.eeusbqq4
{ 
    align-self: flex-end;
  padding: .5em;
  background-color: aliceblue;
 
}

    div.stChatMessage.st-emotion-cache-4oy321.eeusbqq4
{
  align-self: flex-start;
  padding: .5em;
  background-color: hsla(208, 29%, 78%, 0.66);
  border-radius: 25px;
    
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🤖 Clinical MedBot</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = requests.post(API_URL, json={"query_text": prompt})

        if response.status_code == 200:
            result = response.json()
            print(result)  # Debug
            assistant_reply = result.get("answer", "No response received.")
        else:
            assistant_reply = f"Backend error: {response.status_code}"

    except Exception as e:
        assistant_reply = f"Error connecting to backend: {e}"

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)