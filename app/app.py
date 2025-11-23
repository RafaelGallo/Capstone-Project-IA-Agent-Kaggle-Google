import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Load .env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(ENV_PATH)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise Exception("ERROR: GEMINI_API_KEY not found in .env")

# Import agent
from agent_capstone import evaluate_agent_advanced

# Streamlit settings
st.set_page_config(page_title="Clinical Trials Navigator", layout="wide")
st.title("🧭 Clinical Trials Navigator – Dashboard")
st.write("Explore COVID-19 clinical trials using an AI multi-agent pipeline.")

# Patient form
st.header("👤 Patient Information")
with st.form("patient_form"):
    age = st.number_input("Age", min_value=1, max_value=120, value=60)
    sex = st.selectbox("Sex", ["male", "female"])
    symptoms = st.text_input("Symptoms", "breathing problems")
    condition = st.text_input("Condition", "COVID")
    comorb = st.text_input("Comorbidities", "diabetes")
    location = st.text_input("Location", "Brazil")
    submitted = st.form_submit_button("Run Agent")

# Run agent
if submitted:
    user_prompt = (
        f"Patient: {age}-year-old {sex}. "
        f"Condition: {condition}. "
        f"Symptoms: {symptoms}. "
        f"Comorbidities: {comorb}. "
        f"Location: {location}."
    )

    with st.spinner("Running AI Multi-Agent Pipeline..."):
        result = evaluate_agent_advanced(user_prompt)

    st.success("Done!")

    # Final report
    st.header("📄 Final Report")
    st.text(result["state"]["final_report"])

    # Trials summary
    st.header("🔍 Trials Summary")
    tool = result["state"]["tool_result"]

    df_summary = pd.DataFrame([{
        "Condition": tool.get("condition", ""),
        "Total Trials": tool.get("total_trials", 0)
    }])
    st.table(df_summary)

    # Trials examples
    st.header("📋 Trials — Table View")
    if "examples" in tool and len(tool["examples"]) > 0:
        df_examples = pd.DataFrame(tool["examples"])
        st.dataframe(df_examples, use_container_width=True)
    else:
        st.warning("No trial examples returned.")

    # Plot
    st.header("📊 Trial Status Plot")
    plot_path = result["state"].get("status_plot_path")
    if plot_path and os.path.exists(plot_path):
        st.image(plot_path)
    else:
        st.warning("Plot unavailable.")

    # Explanation
    st.header("📝 Explanation")
    st.markdown(result["state"]["explanation"])

    # Validation metrics
    st.header("🧪 Evaluation Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.json(result["validation"])
    with col2:
        st.metric("Score", f"{result['score'] * 100:.2f}%")
        st.metric("Runtime (sec)", result["runtime_sec"])
