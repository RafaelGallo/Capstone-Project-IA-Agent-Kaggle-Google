import json
import logging
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from google import generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise Exception("ERROR: GEMINI_API_KEY not found in .env")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Global memory store
memory = {}

# Load dataset
df_small = pd.read_csv(
    r"C:\Users\rafae.RAFAEL_NOTEBOOK\Downloads\Kaggle\Capstone-Project-IA-Agent-Kaggle-Google\input\COVID clinical trials.csv"
)

# Tool: retrieve trials by condition
def tool_find_trials(condition):
    cond = str(condition).strip().lower()
    subset = df_small[df_small["Conditions"].str.contains(cond, case=False, na=False)]
    subset = subset.replace({np.nan: None})
    examples = subset.head(3).to_dict(orient="records")
    return {
        "condition": condition,
        "total_trials": len(subset),
        "examples": examples
    }

# Tool: generate trial status chart
def plot_trial_status():
    counts = df_small["Status"].value_counts()
    plt.figure(figsize=(6,4))
    counts.plot(kind="bar", color="skyblue")
    plt.title("COVID-19 Trials by Status")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("trial_status.png")
    return "trial_status.png"

# Base class for all agents
class AgentBase:
    def __init__(self, name):
        self.name = name
    def run(self, state):
        raise NotImplementedError

# Intake agent: extract patient profile
class IntakeAgent(AgentBase):
    def __init__(self):
        super().__init__("IntakeAgent")
    def run(self, state):
        logging.info("Running IntakeAgent")
        user_text = state.get("input_text", "")
        prompt = f"""
Extract patient info into JSON:

Text:
{user_text}

Return ONLY JSON with:
age, sex, condition, symptoms, comorbidities, location.
"""
        response = model.generate_content(prompt).text
        try:
            data = json.loads(response)
        except:
            data = {
                "age": None,
                "sex": None,
                "condition": "",
                "symptoms": [],
                "comorbidities": [],
                "location": ""
            }
        memory["patient_profile"] = data
        state["patient_profile"] = data
        return state

# Retrieval agent: find trials and generate plot
class RetrievalAgent(AgentBase):
    def __init__(self):
        super().__init__("RetrievalAgent")
    def run(self, state):
        logging.info("Running RetrievalAgent")
        patient = memory.get("patient_profile", {})
        condition = patient.get("condition", "")
        tool_result = tool_find_trials(condition)
        memory["tool_result"] = tool_result
        state["tool_result"] = tool_result
        plot_path = plot_trial_status()
        memory["status_plot_path"] = plot_path
        state["status_plot_path"] = plot_path
        return state

# Explainer agent: generate explanation
class ExplainerAgent(AgentBase):
    def __init__(self):
        super().__init__("ExplainerAgent")
    def run(self, state):
        logging.info("Running ExplainerAgent")
        tr = memory.get("tool_result", {})
        prompt = f"""
Explain in plain language the meaning of these clinical trial results:

{json.dumps(tr, indent=2)}
"""
        explanation = model.generate_content(prompt).text
        memory["explanation"] = explanation
        state["explanation"] = explanation
        return state

# Report agent: build final report
class ReportAgent(AgentBase):
    def __init__(self):
        super().__init__("ReportAgent")
    def run(self, state):
        logging.info("Running ReportAgent")

        patient = memory.get("patient_profile", {})
        tool_res = memory.get("tool_result", {})
        explanation = memory.get("explanation", "")
        plot_path = memory.get("status_plot_path", "")

        # Clean LLM repetitions
        lines = []
        seen = set()
        for line in explanation.split("\n"):
            t = line.strip()
            if t and t not in seen:
                lines.append(t)
                seen.add(t)
        clean_text = "\n".join(lines)

        # Build final report
        report = f"""
Clinical Trials Navigator — Final Report
=======================================

Patient Profile
---------------
{json.dumps(patient, indent=2)}

Trial Results
-------------
Condition Searched: {tool_res.get("condition", "")}
Total Trials Found: {tool_res.get("total_trials", 0)}

Examples (first 3)
------------------
{json.dumps(tool_res.get("examples", []), indent=2)}

Explanation
-----------
{clean_text}

Plot Saved At
-------------
{plot_path}
"""

        memory["final_report"] = report
        state["final_report"] = report
        return state

# Validation rules
def validate_state(state):
    return {
        "patient_parsed": isinstance(state.get("patient_profile"), dict),
        "tool_used": "tool_result" in state,
        "has_examples": bool(state.get("tool_result", {}).get("examples")),
        "explanation_ok": len(state.get("explanation", "")) > 10
    }

# Score calculation
def compute_score(val):
    return sum(val.values()) / len(val)

# Full pipeline (parallel + sequential)
def evaluate_agent_advanced(user_text):

    print("\n=== Advanced Agent Evaluation Started ===\n")

    state = {"input_text": user_text}
    start_all = time.time()

    # Run Intake + Retrieval in parallel
    def run_parallel(state):
        intake = IntakeAgent()
        retr = RetrievalAgent()
        with ThreadPoolExecutor(max_workers=2) as ex:
            f1 = ex.submit(intake.run, state)
            f2 = ex.submit(retr.run, state)
            s1 = f1.result()
            s2 = f2.result()
        return {**state, **s1, **s2}

    t0 = time.time()
    state = run_parallel(state)
    print("Parallel took:", round(time.time() - t0, 3), "sec")

    # Run Explainer
    t0 = time.time()
    state = ExplainerAgent().run(state)
    print("Explainer took:", round(time.time() - t0, 3), "sec")

    # Run Report
    t0 = time.time()
    state = ReportAgent().run(state)
    print("Report took:", round(time.time() - t0, 3), "sec")

    runtime = round(time.time() - start_all, 3)

    # Validation
    validation = validate_state(state)
    score = compute_score(validation)

    result = {
        "state": state,
        "validation": validation,
        "score": score,
        "runtime_sec": runtime
    }

    print("\n=== Evaluation Complete ===")
    print("Score:", score * 100, "%")
    print("Runtime:", runtime, "sec")
    print("Validation:", validation)

    return result