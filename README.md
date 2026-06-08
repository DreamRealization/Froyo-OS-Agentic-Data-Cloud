# FroyoOS — Agentic Data Cloud on Google Cloud Platform

[![GCP](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![AlloyDB](https://img.shields.io/badge/AlloyDB-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/alloydb)
[![BigQuery](https://img.shields.io/badge/BigQuery-669DF6?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/bigquery)
[![Gemini](https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Cloud Run](https://img.shields.io/badge/Cloud_Run-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/run)

> **A complete end-to-end Agentic Data Application built on Google Cloud Platform** — transforming unstructured dark data into a production-grade AI agent system with real-time HTAP capabilities, LLM evaluation, and conversational analytics.

---

## 🏆 Project Overview

FroyoOS is a multi-codelab certification project demonstrating advanced Google Cloud skills across 5 interconnected codelabs. The system processes raw PDF documents through an AI pipeline, federates data across AlloyDB and BigQuery, deploys a multi-agent application, evaluates AI agents using LLM-as-a-Judge, and exposes conversational analytics through Antigravity IDE.

### Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    FroyoOS Architecture                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PDFs ──► Dataplex DataScan ──► BigQuery (froyo_data)            │
│                                      │                           │
│                                      ▼                           │
│                              AlloyDB (bigquery_fdw)              │
│                                      │                           │
│                                      ▼                           │
│                           MCP Toolbox (Cloud Run)                │
│                                      │                           │
│                                      ▼                           │
│                         FroyoOS Agent App (Gemini)               │
│                           ├── check_allergens tool               │
│                           └── place_order tool                   │
│                                      │                           │
│                                      ▼                           │
│                    LLM-as-a-Judge Evaluation Framework           │
│                                      │                           │
│                                      ▼                           │
│              Antigravity IDE + BigQuery Conversational Agent     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📚 Codelab Series

| # | Codelab | Key Technologies | Status |
|---|---------|-----------------|--------|
| 1 | [Dark Data to Structured Gold](#codelab-1) | Dataplex, BigQuery, GCS, Gemini | ✅ Complete |
| 2 | [AlloyDB-BigQuery Zero ETL Federation](#codelab-2) | AlloyDB, bigquery_fdw, VPC | ✅ Complete |
| 3 | [Agentic App with AlloyDB HTAP](#codelab-3) | MCP Toolbox, Cloud Run, Gemini ADK | ✅ Complete |
| 4 | [Agent Evaluation with Gemini](#codelab-4) | LLM-as-a-Judge, Vertex AI, ADK Eval | ✅ Complete |
| 5 | [Data Agents in Antigravity IDE & BigQuery](#codelab-5) | Antigravity IDE, BQ Conversational Agent | ✅ Complete |

---

## 🗂️ Repository Structure

```
froyo-agentic-cloud/
├── README.md                          # This file
├── CodeLab_1/
│   ├── README.md                      # Codelab 1 documentation
│   └── setup.sh                       # Setup script
├── CodeLab_2/
│   ├── README.md                      # Codelab 2 documentation
│   ├── setup_alloydb.sh               # AlloyDB provisioning script
│   └── federation.sql                 # BigQuery federation SQL
├── CodeLab_3/
│   ├── README.md                      # Codelab 3 documentation
│   ├── tools.yaml                     # MCP Toolbox configuration
│   ├── deploy.sh                      # Cloud Run deployment script
│   └── app-nobill.py                  # Agent application
├── CodeLab_4/
│   ├── README.md                      # Codelab 4 documentation
│   ├── agent_eval.py                  # Evaluation script
│   └── eval_results.md                # Sample evaluation results
├── CodeLab_5/
│   ├── README.md                      # Codelab 5 documentation
│   ├── GEMINI.md                      # Antigravity IDE context file
│   ├── load_tables.sh                 # BigQuery table loading script
│   └── bq_agent_config.json           # BigQuery agent configuration
├── Screenshots/
└── .github/
    └── workflows/
        └── validate.yml               # CI validation workflow
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Database** | AlloyDB (PostgreSQL 15), BigQuery |
| **AI/ML** | Gemini 2.0 Flash, Vertex AI, Google ADK |
| **Infrastructure** | Cloud Run, VPC, Private Service Connect |
| **Data Pipeline** | Dataplex DataScan, GCS, BigQuery Federation |
| **Agent Framework** | MCP Toolbox for Databases, LangChain |
| **IDE** | Antigravity IDE, Google Cloud Data Agent Kit |
| **Security** | Secret Manager, IAM, VPC Egress Controls |
| **Language** | Python 3.12, SQL, YAML |

---

## ⚡ Quick Start

### Prerequisites
- Google Cloud Project with billing enabled
- `gcloud` CLI installed and configured
- Python 3.12+
- AlloyDB cluster running

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/froyo-agentic-cloud.git
cd froyo-agentic-cloud

# Set your project
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Run Codelab 3 setup (requires AlloyDB + BigQuery from Codelabs 1 & 2)
cd codelab-3-agent-app
chmod +x deploy.sh
./deploy.sh
```

---

## 🎯 Key Achievements

- **Zero-ETL Federation**: Connected AlloyDB to BigQuery using `bigquery_fdw` extension eliminating data duplication
- **HTAP Architecture**: Hybrid Transactional/Analytical Processing — live orders in AlloyDB, analytics in BigQuery
- **Production-grade Security**: MCP Toolbox with parameterized SQL prevents SQL injection
- **LLM Evaluation**: Implemented LLM-as-a-Judge pattern scoring tool accuracy and groundedness
- **Conversational Analytics**: Natural language interface to complex multi-table BigQuery queries

---

## 📊 Results

| Metric | Score |
|--------|-------|
| Tool Routing Accuracy | 1.0 / 1.0 ✅ |
| Response Groundedness | 0.5 / 1.0 ✅ |
| SQL Injection Prevention | PASS ✅ |
| Jailbreak Resistance | PASS ✅ |

---

## 👤 Author

**Dhyan Jain**
- LinkedIn: [linkedin.com/in/dhyanjain](https://linkedin.com/in/dhyanjain)
- GitHub: [github.com/dhyanjain](https://github.com/dhyanjain)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
