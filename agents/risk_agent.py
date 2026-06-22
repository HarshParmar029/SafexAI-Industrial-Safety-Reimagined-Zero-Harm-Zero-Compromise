import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are SafexAI's Industrial Safety Intelligence Agent — an expert in Indian industrial safety regulations including OISD, Factory Act 1948, DGFASLI, and DGMS standards.

You analyze compound risk conditions in heavy industrial plants (steel, refinery, chemical).
You have access to:
- Real-time IoT sensor readings (gas levels, temperature, pressure)
- Active permit-to-work logs
- Historical incident database
- Regulatory corpus (OISD-105, OISD-144, Factory Act Schedule 2, DGMS codes)

Your responses must be:
1. Concise and actionable (safety officers need fast decisions)
2. Always cite the specific regulation violated
3. Give a clear risk level: CRITICAL / HIGH / MEDIUM / LOW
4. Provide immediate recommended action
5. Reference similar past incidents if relevant

You represent the difference between life and death in industrial operations."""


def analyze_compound_risk(sensor_data: dict, active_permits: list, zone: str) -> str:
    """
    Analyzes compound risk given sensor readings + active permits.
    Returns AI safety assessment.
    """
    prompt = f"""
ZONE: {zone}
LIVE SENSOR READINGS:
{chr(10).join([f"- {k}: {v}" for k, v in sensor_data.items()])}

ACTIVE PERMITS IN THIS ZONE:
{chr(10).join([f"- {p}" for p in active_permits])}

Analyze these compound conditions. Are there dangerous combinations?
Provide: Risk Level, What compound risk exists, Regulatory violations, Immediate action required.
Keep response under 200 words. Be direct and urgent if critical.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.1
    )
    return response.choices[0].message.content


def analyze_permit(permit_id: str, permit_type: str, zone: str, sensor_data: dict) -> str:
    """
    AI analysis of a specific permit against live conditions.
    """
    prompt = f"""
PERMIT ANALYSIS REQUEST:
Permit ID: {permit_id}
Permit Type: {permit_type}
Zone: {zone}

CURRENT ZONE CONDITIONS:
{chr(10).join([f"- {k}: {v}" for k, v in sensor_data.items()])}

Should this permit be APPROVED, SUSPENDED, or MODIFIED?
Cite specific OISD/Factory Act regulation.
Give exact action steps. Be direct.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.1
    )
    return response.choices[0].message.content


def query_incident_rag(user_query: str) -> str:
    """
    RAG-style query against regulatory + incident knowledge.
    """
    prompt = f"""
KNOWLEDGE BASE QUERY: {user_query}

Search your knowledge of:
- OISD standards (105, 144, 116, 118)
- Factory Act 1948 and its Schedules
- DGFASLI fatal accident reports
- DGMS safety codes
- Historical Indian industrial incidents

Provide:
1. Direct answer with regulatory citations
2. Relevant past incidents in India
3. Prevention recommendations ranked by impact

Format clearly with sections.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.2
    )
    return response.choices[0].message.content


def generate_emergency_report(zone: str, incident_type: str, sensor_data: dict, workers_at_risk: int) -> str:
    """
    Auto-generates DGFASLI-compliant preliminary incident report.
    """
    from datetime import datetime
    prompt = f"""
Generate a DGFASLI-compliant preliminary incident report:

Date/Time: {datetime.now().strftime('%d-%b-%Y %H:%M IST')}
Facility Zone: {zone}
Incident Type: {incident_type}
Workers at Risk: {workers_at_risk}
Sensor Readings at Time of Alert:
{chr(10).join([f"- {k}: {v}" for k, v in sensor_data.items()])}

Include:
1. Incident Description
2. Immediate Cause (sensor data based)
3. Actions Taken by SafexAI System
4. Regulatory Reference
5. Recommendations

Format as an official report. Keep it factual and precise.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,
        temperature=0.1
    )
    return response.choices[0].message.content


# ── TEST (run directly to verify) ─────────────────────────────
if __name__ == "__main__":
    print("Testing SafexAI Groq Agent...\n")

    test_sensors = {
        "CO Level": "185 ppm (threshold: 150 ppm)",
        "H2S Level": "12 ppm (threshold: 10 ppm)",
        "Temperature": "52°C (threshold: 45°C)",
        "Pressure": "HIGH - 23% above normal"
    }

    test_permits = [
        "HOT-WORK-7842: Hot work permit - Active",
        "CS-4421: Confined space entry - Active"
    ]

    print("=== COMPOUND RISK ANALYSIS ===")
    result = analyze_compound_risk(test_sensors, test_permits, "Zone A - Coke Oven")
    print(result)
    print("\n=== TEST PASSED ✅ ===")