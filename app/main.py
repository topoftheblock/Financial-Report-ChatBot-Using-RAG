import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Ensure the root directory is in the path so we can import from src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent.generator import FinancialRAGAgent
from app.components import render_sidebar, render_agent_thoughts

# Load environment variables (API Keys)
load_dotenv()

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Financial AI Analyst",
    page_icon="💹",
    layout="centered"
)

# -------------------------------------------------------------------
# 1. Initialize Session State
# -------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your Financial Analyst AI. I can search SEC filings, extract exact metrics, and calculate margins or YoY growth. What would you like to know?"}
    ]

# Initialize the Agent only once to save time
if "agent" not in st.session_state:
    # You can surface these parameters in the sidebar later if you wish
    st.session_state.agent = FinancialRAGAgent(model_name="gpt-4o", temperature=0.0)

# -------------------------------------------------------------------
# 2. Render UI Components
# -------------------------------------------------------------------
render_sidebar()

st.title("💹 Financial AI Analyst")
st.write("Ask questions about company financials, risk factors, or growth metrics.")

# Display existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # If the assistant message has thoughts saved, render them
        if "thoughts" in msg:
            render_agent_thoughts(msg["thoughts"])

# -------------------------------------------------------------------
# 3. Handle User Input & Agent Execution
# -------------------------------------------------------------------
if prompt := st.chat_input("E.g., What was AAPL's revenue in 2023 vs 2022? Calculate the growth."):
    
    # Add user message to UI and state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process the agent response
    with st.chat_message("assistant"):
        # We use a status container to show the user that the bot is actively using tools
        with st.status("Analyzing financials and calculating...", expanded=True) as status_box:
            
            try:
                # Execute the agent
                response = st.session_state.agent.query(prompt)
                
                final_answer = response.get("output", "I could not generate an answer.")
                thoughts = response.get("intermediate_steps", [])
                
                status_box.update(label="Analysis Complete!", state="complete", expanded=False)
                
            except Exception as e:
                final_answer = "I encountered an error while processing your request."
                thoughts = []
                st.error(f"Error details: {str(e)}")
                status_box.update(label="Error occurred", state="error")

        # Display the thoughts (tool execution) inside an expander
        render_agent_thoughts(thoughts)
        
        # Display the final text answer
        st.markdown(final_answer)
        
    # Save the assistant's response and thoughts to session state
    st.session_state.messages.append({
        "role": "assistant", 
        "content": final_answer,
        "thoughts": thoughts
    })