import streamlit as st
import requests
import json
import streamlit.components.v1 as components
import uuid

st.set_page_config(page_title="Home Device Controller")

api_endpoint =  "http://localhost:8001/"
device_endpoint = "http://localhost:3000"

if 'conversation_id' not in st.session_state:
   st.session_state.conversation_id = str(uuid.uuid4())

with st.sidebar:
    try:
        status_code = requests.get(device_endpoint).status_code
        components.iframe(device_endpoint, height=800)
    except requests.exceptions.ConnectionError:
        st.write("The Home Automation server is not running")
        st.write("Please setup server from https://github.com/manojmanivannan/home-automation-server")


st.title("💬 Home Device Controller")
st.caption("🚀 A Streamlit chatbot to control your devices")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {"question": prompt, "conversation_id": st.session_state.conversation_id}
        response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            ai_response = response.json().get("answer", "No response key in API output")
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            st.chat_message("assistant").write(ai_response)
        else:
            error_message = f"Error: Received status code {response.status_code}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.chat_message("assistant").write(error_message)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        st.chat_message("assistant").write(error_message)
