# SafexAI — System Architecture

## High-Level Architecture
┌─────────────────────────────────────────────────────────────┐

│                    DATA INGESTION LAYER                      │

├──────────────┬──────────────┬──────────────┬───────────────┤

│  IoT Sensors │  CCTV Feeds  │  PTW Logs    │  Shift Records│

│  (Gas/Temp/  │  (YOLOv8 PPE │  (Permit     │  (Handover    │

│   Pressure)  │   Detection) │   Database)  │   Patterns)   │

└──────┬───────┴──────┬───────┴──────┬───────┴───────┬───────┘

└──────────────┴──────────────┴───────────────┘

│

┌─────────▼─────────┐

│  SAFEXAI CORE AI  │

│  ENGINE (Groq     │

│  Llama 3.3 70B)   │

└─────────┬─────────┘

│

┌─────────────────────┼─────────────────────┐

│                     │                     │

┌───────▼───────┐   ┌─────────▼───────┐   ┌────────▼────────┐

│    AGENT 1    │   │    AGENT 2      │   │    AGENT 3      │

│  Compound     │   │   Permit        │   │   Emergency     │

│  Risk         │   │   Intelligence  │   │   Response      │

│  Detector     │   │   Specialist    │   │   Orchestrator  │

└───────┬───────┘   └─────────┬───────┘   └────────┬────────┘

└─────────────────────┼─────────────────────┘

│

┌───────────────┼───────────────┐

│               │               │

┌─────────▼──┐   ┌────────▼──────┐  ┌────▼────────────┐

│ RAG Engine │   │  Geospatial   │  │  PDF Report     │

│ LlamaIndex │   │  Heatmap      │  │  Generator      │

│ +ChromaDB  │   │  (Folium)     │  │  (ReportLab)    │

└────────────┘   └───────────────┘  └─────────────────┘

│

┌─────────▼─────────┐

│    STREAMLIT      │

│    DASHBOARD      │

│      8 Tabs       │

└───────────────────┘

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| LLM | Groq Llama 3.3 70B | Ultra-fast inference |
| Multi-Agent | Custom 3-Agent System | Risk + Permit + Emergency |
| Computer Vision | YOLOv8 (HuggingFace) | PPE detection |
| RAG | LlamaIndex + ChromaDB | Regulatory search |
| Dashboard | Streamlit | Real-time UI |
| Maps | Folium | Geospatial heatmap |
| Reports | ReportLab | PDF generation |
| Regulations | OISD-105/144, Factory Act 1948, DGFASLI | Compliance |

## Data Flow

1. IoT sensors stream → Core Engine
2. Core Engine triggers 3 agents simultaneously
3. Agents correlate compound risks
4. RAG searches regulatory corpus
5. Dashboard updates real-time
6. Emergency protocol auto-triggers on CRITICAL
7. PDF report auto-generated for DGFASLI

## Key Innovation

**Traditional:** Single sensor → Single alert (misses combinations)

**SafexAI:** Multiple sources → AI correlation → Compound risk score

**Example:** CO 185ppm + Hot Work Permit + High Temp = CRITICAL
(No single sensor would flag this combination)
