import streamlit as st

from app.deps import get_conversation

welcome_message = {"role": "assistant", "content": "Hello, I'm a travel assistant. Ask me about your dream destination."}


st.title("Travel assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [welcome_message]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # User message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Response
    response = get_conversation().ask(prompt)

    # Assistant message
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
