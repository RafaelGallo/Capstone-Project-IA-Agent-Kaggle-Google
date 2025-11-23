# 📘 Clinical Trials Navigator — Capstone Project Google/Kaggle
*A Multi-Agent AI System for Exploring COVID-19 Clinical Trials*

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Project](https://img.shields.io/badge/Project-Multi--Agent%20AI-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat-square&logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?style=flat-square&logo=streamlit)
![Multi Agent](https://img.shields.io/badge/AI-Multi--Agent%20System-green?style=flat-square)
![Gemini 2.5 Flash](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-9cf?logo=google&style=flat-square)
![Generative AI](https://img.shields.io/badge/Google%20Generative%20AI-Enabled-orange?style=flat-square)
![Dataset](https://img.shields.io/badge/Dataset-ClinicalTrials.gov-purple?style=flat-square)
![COVID-19](https://img.shields.io/badge/COVID--19-Data-red?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Local%20%2F%20Kaggle-blueviolet?style=flat-square)
![Evaluation](https://img.shields.io/badge/Evaluation-Score%20Auto--Validation-yellowgreen?style=flat-square)
![Pipeline Tested](https://img.shields.io/badge/Pipeline-Tested-success?style=flat-square)

![](https://www.desiai.ai/wp-content/uploads/2025/11/Google-X-Kaggle-1068x601.jpg)


## 📌 Overview

ClinicalTrials.gov contains thousands of COVID-19 related clinical studies, but navigating this volume of information manually is extremely difficult.
This project implements a **multi-agent AI pipeline** capable of:

* Parsing patient information
* Identifying the most relevant clinical trials
* Summarizing the top matches
* Generating an AI-written explanation
* Producing visual analytics and plots
* Delivering everything through an interactive **Streamlit dashboard**

This project was built as part of the **Agents Intensive – Capstone Project**, applying multi-agent architectures, tool-use, validation, and reasoning.

## 🚀 Key Features

### ✔ Multi-Agent Reasoning Pipeline

* **IntakeAgent** → parses patient profile
* **SearchAgent** → queries trial dataset
* **AnalysisAgent** → extracts examples and generates explanations
* **EvaluatorAgent** → validates reasoning and computes a performance score

### ✔ Tool Integration

* ClinicalTrials.gov dataset
* Search & filtering tools
* Custom matplotlib visualizations

### ✔ Streamlit Dashboard

Fully interactive application allowing users to:

* Enter patient information
* Run the multi-agent pipeline
* View matched trials
* Read detailed explanations
* Visualize trial statistics

## 🧭 Application — Screenshots

### 🖥 Dashboard UI

![](https://github.com/RafaelGallo/Capstone-Project-IA-Agent-Kaggle-Google/blob/main/output/0.png?raw=true)

### 🧍 Patient Form

![](https://github.com/RafaelGallo/Capstone-Project-IA-Agent-Kaggle-Google/blob/main/output/1.png?raw=true)

### 📊 Trial Summary

![](https://github.com/RafaelGallo/Capstone-Project-IA-Agent-Kaggle-Google/blob/main/output/2.png?raw=true)

### 🧠 AI-Generated Explanation

![](https://github.com/RafaelGallo/Capstone-Project-IA-Agent-Kaggle-Google/blob/main/output/3.png?raw=true)

### 🔬 Trial Details

![](https://github.com/RafaelGallo/Capstone-Project-IA-Agent-Kaggle-Google/blob/main/output/trial_status.png?raw=true)

*(Replace paths with your image folder)*

## 🧪 Example Output (Summary)

For the input:

* **Age:** 60
* **Sex:** male
* **Condition:** COVID
* **Symptoms:** breathing problems
* **Comorbidities:** diabetes
* **Location:** Brazil

The agent found: **5,783 relevant trials**
The explanation clearly states that for the top 3 examples, **no published results** are available yet.

The evaluation subsystem reported:

```json
{
  "patient_parsed": true,
  "tool_used": true,
  "has_examples": true,
  "explanation_ok": true
}
```

**Final Score:** **100%**
**Runtime:** ~17 seconds

## 🧬 Technology Stack

### **AI / LLM**

* Gemini 2.5 Flash
* OpenAI Agents Framework (multi-agent)
* Structured output + tool calling

### **Python / Libraries**

* pandas
* matplotlib
* python-dotenv
* Streamlit
* json
* pathlib

## 📂 Project Structure

```
📁 Capstone-Clinical-Trials-Agent
│
├── app/
│   ├── app.py                 # Streamlit dashboard
│   ├── agent_capstone.py      # Multi-agent pipeline
│   ├── tools/                 # Tool functions
│   └── plots/                 # Generated visualizations
│
├── data/
│   └── clinical_trials.csv
│
├── images/                    # Screenshots for README
│
├── .env                       # GEMINI_API_KEY
├── requirements.txt
└── README.md
```

## 🔑 Environment Setup

Create a **.env** file:

```
GEMINI_API_KEY=your_key_here
```

Install dependencies:

```
pip install -r requirements.txt
```

Run Streamlit:

```
streamlit run app/app.py
```

## 📘 How It Works (Step-by-Step)

### 1. User enters patient profile

### 2. IntakeAgent parses structured fields

### 3. SearchAgent retrieves all matching trials

### 4. A bar plot is automatically generated

### 5. AnalysisAgent produces a rich explanation

### 6. EvaluatorAgent validates the answer

### 7. Dashboard displays results

## 🏁 Final Result

A fully functional **AI-Powered Clinical Trials Navigator**, integrating:

* Multi-agent reasoning
* Medical dataset search
* Automatic chart generation
* LLM explanation generation
* Streamlit interactive interface

This project demonstrates real-world agentic AI applied to biomedical research.

## ⭐ Author

**Rafael Gallo**
Data Scientist 
