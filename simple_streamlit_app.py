import uuid

import streamlit as st
from simple_graph import graph

if "current_user_thread_id" not in st.session_state:
    st.session_state.current_user_thread_id = uuid.uuid4()

x = st.slider('Select a value')
st.write(st.session_state)

st.image(graph.get_graph().draw_mermaid_png())

# Input
initial_input = {"input": "hello world"}

# Thread
thread = {"configurable": {"thread_id": st.session_state.current_user_thread_id}}

# Run the graph until the first interruption
for event in graph.stream(initial_input, thread, stream_mode="values"):
    st.write("=-----------------=")
    st.write(event)
