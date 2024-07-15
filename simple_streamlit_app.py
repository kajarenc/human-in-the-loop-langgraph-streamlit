import uuid

import streamlit as st
from simple_graph import graph

st.write(id(graph))

if "current_user_thread_id" not in st.session_state:
    st.session_state.current_user_thread_id = str(uuid.uuid4())

x = st.slider('Select a value')
st.write(st.session_state)

st.image(graph.get_graph().draw_mermaid_png())

# Input
initial_input = {"input": "hello world"}

# Thread
thread = {"configurable": {"thread_id": st.session_state.current_user_thread_id}}

# Run the graph until the first interruption
for event in graph.stream(initial_input, thread, stream_mode="values"):
    st.write("=-----------------=!!")
    st.write(event)

# Get user input
user_input = st.text_input("Tell me how you want to update the state: ")

if user_input == "":
    st.stop()

# We now update the state as if we are the human_feedback node
graph.update_state(thread, {"user_feedback": user_input}, as_node="human_feedback")

# We can check the state
st.write("--State after update--")
st.write(graph.get_state(thread))

# We can check the next node, showing that it is node 3 (which follows human_feedback)
st.write(graph.get_state(thread).next)

# Continue the graph execution
for event in graph.stream(None, thread, stream_mode="values"):
    st.write("=-----------------=")
    st.write(event)

st.write(graph.get_state(thread).values)
