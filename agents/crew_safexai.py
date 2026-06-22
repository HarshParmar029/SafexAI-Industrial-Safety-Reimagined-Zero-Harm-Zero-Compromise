from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def _call_agent(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        max_tokens=800
    )
    return response.choices[0].message.content

def run_full_safexai_analysis(zone, sensor_data, active_permits):
    # Agent 1: Risk Intelligence
    risk_result = _call_agent(
        system_prompt="You are a Senior Process Safety Engineer with 20+ years experience in Indian steel, chemical and refinery plants. Expert in OISD, Factory Act, DGMS standards. Be specific, cite regulation sections.",
        user_prompt=f"Analyze compound risks in {zone}. Sensor data: {sensor_data}. Identify all dangerous combinations, risk level (CRITICAL/HIGH/MEDIUM), and specific regulatory violations with section numbers."
    )

    # Agent 2: Permit Compliance
    permit_result = _call_agent(
        system_prompt="You are a Permit-to-Work Compliance Specialist and former Safety Auditor. You catch dangerous permit conflicts that humans miss.",
        user_prompt=f"Validate these active permits in {zone}: {active_permits}. Cross-check with sensor conditions: {sensor_data}. Give SUSPEND/PROCEED/REVIEW decision for each permit with reasons."
    )

    # Agent 3: Emergency Orchestrator
    emergency_result = _call_agent(
        system_prompt="You are an Emergency Response Orchestrator trained on thousands of real Indian industrial incidents. Generate fast, regulatory-compliant response plans.",
        user_prompt=f"CRITICAL risk detected in {zone}. Sensor: {sensor_data}. Create a step-by-step emergency response timeline with actions in seconds/minutes, responsible persons, and DGFASLI compliance checklist."
    )

    final_output = f"""
## 🔴 Agent 1 — Compound Risk Intelligence
{risk_result}

---

## 📋 Agent 2 — Permit Compliance Specialist  
{permit_result}

---

## 🚨 Agent 3 — Emergency Response Orchestrator
{emergency_result}

---
*✅ 3-Agent SafexAI Analysis Complete | Powered by Groq Llama 3.3 70B*
"""
    return final_output
