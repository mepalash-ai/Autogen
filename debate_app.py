# packages

import os
from autogen import ConversableAgent
import streamlit as st

def main():
    # LLM config
    llm_config = {
        "config_list":[
            {
                "model": "gpt-4o-mini",
                "temperature": 0.9,
                "api_key": os.environ.get("OPENAI_API_KEY")
            }
        ]
    }

    # Title
    st.title("Conversial Debate")

    prompt = st.chat_input("Enter a topic to debate about")
    if prompt:
        st.header(f"Topic: {prompt}")

    # Conversation settings
    with st.expander("Conversation Settings"):
        number_of_turns = st.slider(
            "Number of turns",
            min_value=1,
            max_value=10,
            value=1
        )

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Style of Person A")
            style_a = st.radio(
                "Choose style for first speaker",
                ["Friendly", "Neutral", "Unfriendly"],
                key="style_a"
            )

        with col2:
            st.subheader("Style of Person B")
            style_b = st.radio(
                "Choose style for second speaker",
                ["Friendly", "Neutral", "Unfriendly"],
                key="style_b"
            )
    # set up agents
    if prompt:
        person_a = ConversableAgent(
            name="user",
            system_message=f"""
            You are a person who believes that {prompt}.
            You try to convince others of this.
            You answer in a {style_a} way.
            Answr very short and concise.
            """,
            llm_config=llm_config,
            human_input_mode="NEVER",
        )
        
        person_b = ConversableAgent(
            name="ai",
            system_message=f"""
            You are a person who believes the opposite of {prompt}.
            You answer in a {style_b} way.
            Answr very short and concise.
            """,
            llm_config=llm_config,
            human_input_mode="NEVER",
        )

        # Start the conversation
        result = person_a.initiate_chat(
            recipient=person_b,
            message=prompt,
            max_turns=number_of_turns
        )

        messages = result.chat_history

        for message in messages:
            name = message["name"]
            if name == "user":
                with st.container():
                    col1, col2 = st.columns([3, 7])
                    with col2:
                        with st.chat_message(name=name):
                            st.write(message["content"])
            else:
                with st.container():
                    col1, col2 = st.columns([7, 3])
                    with col1:
                        with st.chat_message(name=name):
                            st.write(message["content"])

if __name__ == "__main__":
    main()


