import streamlit as st
from core.classifier import QueryClassifier
from core.guardrails import GuardrailManager
from core.llm_client import LLMClient
from core.metrics import MetricsCollector
from core.router_engine import RouterEngine


classifier = QueryClassifier()
guardrails = GuardrailManager()
router_engine = RouterEngine()
llm_client = LLMClient()
metrics = MetricsCollector()

st.title("🚀 ModelDirector")
st.caption("Adaptive Multi-Provider LLM Gateway")
query = st.text_area("Enter your prompt", height=150, placeholder="Ask anything...")

if st.button("Generate"):
    if not query.strip():
        st.warning("Please enter a prompt")
        st.stop()

    try:
        guardrails.validate_input(query)
        classification = classifier.classify(query)
        selected_tier = router_engine.determine_tier(classification)
        messages = [{"role": "user", "content": query}]
        response, metadata = llm_client.generate(tier=selected_tier, messages=messages)
        answer = response.choices[0].message.content
        guardrails.validate_output(answer)
        metrics.store_request(
            {
                "query": query,
                "task": classification["task"],
                "complexity": classification["complexity"],
                "selected_tier": selected_tier,
                "actual_model": metadata["model"],
                "latency_ms": metadata["latency_ms"],
                "cost_usd": metadata["cost_usd"],
            }
        )
        st.success("""✅ Prompt Injection Check Passed""")
        st.success("""✅ Toxicity Check Passed""")
        st.success("""✅ Output Validation Passed""")
        st.title("Response:")
        st.markdown(answer)
        st.divider()
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Task", classification["task"])
            st.metric("Complexity", classification["complexity"])

        with col2:
            st.metric("Selected Tier", selected_tier)
            st.metric("Actual Model", metadata["model"])
        with col3:
            st.metric("Latency", f"{metadata['latency_ms']} ms")
            st.metric("Cost", f"${metadata['cost_usd']}")

    except Exception as e:
        metrics.store_guardrail_violation(query=query, violation=str(e))
        st.error(str(e))
