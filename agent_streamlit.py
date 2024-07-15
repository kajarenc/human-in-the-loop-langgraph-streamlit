import uuid

import streamlit as st
from agent_graph import app

from langchain_core.messages import HumanMessage, ToolMessage

if "current_user_thread_id" not in st.session_state:
    st.session_state.current_user_thread_id = str(uuid.uuid4())

if "interrupted_to_ask_human" not in st.session_state:
    st.session_state.interrupted_to_ask_human = False

if "feedback_from_human" not in st.session_state:
    st.session_state.feedback_from_human = ""

x = st.slider('Select a value')
st.write(st.session_state)

st.image(app.get_graph().draw_mermaid_png())

config = {"configurable": {"thread_id": st.session_state.current_user_thread_id}}

if not st.session_state.interrupted_to_ask_human:

    input_message = HumanMessage(
        content="Use the search tool to ask the user where they are, then look up the weather there"
    )

    for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
        st.write(event["messages"][-1].pretty_repr(html=True))

    if app.get_state(config).values["messages"][-1].tool_calls[0]["name"] == "AskHuman":
        st.session_state.interrupted_to_ask_human = True

if not st.session_state.interrupted_to_ask_human and st.session_state.feedback_from_human != "":
    st.empty()

if st.session_state.interrupted_to_ask_human:
    text_input = st.text_input("Where are you located?")
    if text_input:
        st.session_state.feedback_from_human = text_input
        st.session_state.interrupted_to_ask_human = False

if st.session_state.feedback_from_human and not st.session_state.interrupted_to_ask_human:
    tool_call_id = app.get_state(config).values["messages"][-1].tool_calls[0]["id"]
    st.session_state.human_input = ""
    # We now create the tool call with the id and the response we want
    tool_message = [ToolMessage(tool_call_id=tool_call_id, content=st.session_state.feedback_from_human)]

    # We now update the state
    # Notice that we are also specifying `as_node="ask_human"`
    # This will apply this update as this node,
    # which will make it so that afterwards it continues as normal

    app.update_state(config, {"messages": tool_message}, as_node="ask_human")

    st.write(app.get_state(config).next)

    for event in app.stream(None, config, stream_mode="values"):
        st.write(event["messages"][-1].pretty_repr(html=True))

    st.session_state.feedback_from_human = ""
