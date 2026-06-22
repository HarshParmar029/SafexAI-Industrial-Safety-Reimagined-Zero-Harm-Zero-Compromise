from crewai import Agent, Crew, Task
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)

# Agents
risk_agent = Agent(
    role='Compound Risk Intelligence Expert',
    goal='Identify dangerous combinations across sensors, permits, workers and context',
    backstory='Senior Process Safety Engineer with 20+ years experience in steel, chemical and refinery plants. Expert in OISD, Factory Act, DGMS standards.',
    llm=llm,
    verbose=True
)

permit_agent = Agent(
    role='Permit-to-Work Compliance Specialist',
    goal='Cross-check active permits against live conditions and historical risks',
    backstory='Former Safety Auditor who has prevented multiple major incidents.',
    llm=llm,
    verbose=True
)

emergency_agent = Agent(
    role='Autonomous Emergency Response Orchestrator',
    goal='Generate fastest, regulatory-compliant response plan',
    backstory='Trained on thousands of real industrial incidents and best response protocols.',
    llm=llm,
    verbose=True
)

def run_full_safexai_analysis(zone, sensor_data, active_permits):
    """Run complete multi-agent analysis"""
    task1 = Task(
        description=f"Analyze compound risks in {zone} using this sensor data: {sensor_data}",
        agent=risk_agent,
        expected_output="Risk level, key compound risks, regulatory violations"
    )
    task2 = Task(
        description=f"Validate these permits against current risks: {active_permits}",
        agent=permit_agent,
        expected_output="Permit status recommendations with actions"
    )
    task3 = Task(
        description="If critical risk, create detailed emergency response timeline",
        agent=emergency_agent,
        expected_output="Step-by-step response plan with timings"
    )

    crew = Crew(
        agents=[risk_agent, permit_agent, emergency_agent],
        tasks=[task1, task2, task3],
        verbose=2
    )
    
    result = crew.kickoff(inputs={"zone": zone})
    return result
