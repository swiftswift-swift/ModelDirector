import streamlit as st

st.set_page_config(page_title="ModelDirector", page_icon="🚀", layout="wide")
st.title("🚀 ModelDirector")
st.subheader("Adaptive Multi-Provider LLM Gateway")
st.markdown("""ModelDirector is an intelligent LLM orchestration platform built using LiteLLM.""")
st.success("""
It dynamically routes user requests across multiple AI providers based on:
- Task Type
- Query Complexity
- Cost Efficiency
- Latency
- Provider Availability
""")
st.warning("""
The system also includes:   
- Multi-Provider Fallbacks
- AI Guardrails
- Cost Tracking
- Latency Monitoring
- Redis-Based Observability
""")
st.caption("Use the sidebar to explore Chat, Analytics, and Guardrails.")
