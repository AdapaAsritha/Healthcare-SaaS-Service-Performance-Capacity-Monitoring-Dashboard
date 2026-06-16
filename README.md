# Healthcare SaaS Service Performance & Capacity Monitoring Dashboard 🏥📊

> An end-to-end IT Service Management (ITSM) analytics portfolio project simulating a real-world Healthcare SaaS platform.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![SQL](https://img.shields.io/badge/SQL-SQLite-lightgrey.svg)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-yellow.svg)
![Prophet](https://img.shields.io/badge/Forecasting-Prophet-green.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)

---

## 📑 Table of Contents
- [Project Overview](#-project-overview)
- [Architecture & Tech Stack](#-architecture--tech-stack)
- [Project Structure](#-project-structure)
- [Key Features](#-key-features)
- [Dashboard Screenshots](#-dashboard-screenshots)
- [Key Findings](#-key-findings)
- [ITIL Alignment](#-itil-alignment)
- [Skills Demonstrated](#-skills-demonstrated)
- [How to Run](#-how-to-run)
- [SQL Schema](#-sql-schema)
- [Author](#-author)

---

## 📖 Project Overview

As Healthcare Software-as-a-Service (SaaS) platforms (like athenahealth, Epic, or Cerner) scale to serve millions of patient records and financial transactions, **Service Reliability and Capacity Planning** become mission-critical. A Service Performance Analyst bridges the gap between engineering, IT operations, and product teams to ensure platform availability meets strict Service Level Agreements (SLAs).

This project simulates a real-world Service Performance Analyst role. It models 8 core microservices of a healthcare SaaS platform (Patient Portal, Claims Processing, EHR, etc.), tracks 12 months of synthetic incident and availability data, and applies machine learning time-series forecasting to predict future capacity bottlenecks.

The end goal is a comprehensive **Power BI Dashboard** and an actionable **Stakeholder Memo** designed to alert engineering teams to critical risks before they impact patient care or hospital revenue cycles.

---

## 🏗 Architecture & Tech Stack

```text
[Raw Data Simulation] ──> [Data Storage & KPIs] ──> [Predictive Analytics] ──> [Visualization]
     Python (Faker)               SQLite                   Prophet (ML)             Power BI
```

| Tool | Purpose | Libraries / Version |
|---|---|---|
| **Python** | Data Generation, Analysis, Forecasting | `pandas`, `faker`, `prophet`, `scipy`, `seaborn` |
| **SQLite** | Relational Database & KPI Extraction | `sqlite3` (built-in) |
| **Jupyter** | Exploratory Data Analysis | `jupyter` |
| **Power BI** | Executive Dashboards & BI Reporting | Power BI Desktop |

---

## 📂 Project Structure

```text
healthcare-saas-dashboard/
│
├── data/
│   ├── raw/                  # Generated raw CSVs
│   └── processed/            # Query results and Power BI-ready CSVs
│
├── sql/
│   ├── schema.sql            # SQLite database schema
│   └── kpi_queries.sql       # 10 analytical SQL queries
│
├── notebooks/
│   ├── 02_incident_analysis.ipynb
│   └── 03_capacity_forecasting.ipynb
│
├── reports/
│   ├── charts/               # PNG outputs of EDA
│   ├── incident_analysis_report.txt
│   ├── capacity_risk_report.csv
│   └── capacity_planning_report.txt
│
├── docs/
│   ├── powerbi_instructions.md
│   └── stakeholder_recommendations.md
│
├── powerbi-screenshots/      # Exported dashboard views
│
├── data_generation.py        # Generates synthetic data
├── load_to_db.py             # Loads data into SQLite
├── run_queries.py            # Executes SQL KPIs
├── requirements.txt
└── README.md
```

---

## ✨ Key Features

1. **Synthetic Data Pipeline**: Custom Python scripts utilizing `Faker` to simulate 12 months of realistic incident, uptime, and capacity utilization data.
2. **Relational Database Design**: Robust SQLite schema linking incidents, SLAs, and capacity metrics to service ownership.
3. **Automated KPI Extraction**: 10 complex SQL queries calculating SLA breaches, MTTR, and rolling uptime trends.
4. **Downtime Impact Scoring**: Pandas workflow mapping incident severity to estimated business impact scores.
5. **Incident Trend Analysis**: Heatmap generation identifying peak vulnerability windows (e.g., weekday mid-day spikes).
6. **SLA Compliance Matrix**: Visual tracking of historical SLA performance across 8 microservices.
7. **Time-Series Forecasting**: Facebook Prophet implementation predicting CPU, Memory, and Storage utilization 90 days into the future.
8. **Automated Risk Scoring Engine**: Custom algorithm scoring capacity risks (0-100) based on projected time-to-breach.
9. **Executive BI Dashboard**: 3-page Power BI interactive dashboard with complex DAX measures.
10. **Actionable ITIL Reporting**: Formal stakeholder memos translating data into engineering action items.

---

## 🖼 Dashboard Screenshots

### Page 1: Executive Summary
![Executive Summary](powerbi-screenshots/page1.png)
*(Placeholder: Add your exported screenshot here)*

### Page 2: Incident Trends
![Incident Trends](powerbi-screenshots/page2.png)
*(Placeholder: Add your exported screenshot here)*

### Page 3: Capacity & Risk
![Capacity Risk](powerbi-screenshots/page3.png)
*(Placeholder: Add your exported screenshot here)*

---

## 🔍 Key Findings

Based on the simulated 12-month data analysis:
1. **Claims Processing Bottleneck**: The Claims Processing service recorded the highest total downtime (47 hours) in Q4, primarily caused by Application-category incidents on Tuesday mornings.
2. **Critical SLA Breaches**: Despite maintaining 99.1% overall platform uptime, the EHR and Billing Engine services breached their strict 99.9% SLA targets in 4 out of the last 12 months.
3. **Resource Exhaustion Warning**: Prophet time-series models indicate the Authentication Service's CPU utilization is trending at a 4.2% MoM growth rate and will cross the 85% critical threshold within 45 days.
4. **MTTR Discrepancy**: Mean Time to Resolve (MTTR) for P1 incidents averages 3.2 hours, indicating inconsistent escalation pathways compared to the 1.5 hour target.
5. **Day-of-Week Patterns**: 65% of all high-severity incidents occur between Tuesday and Thursday during peak hospital operating hours (10 AM - 2 PM EST).

---

## ⚙️ ITIL Alignment

| ITIL Process | Project Component | Deliverable |
|---|---|---|
| **Incident Management** | Trend analysis, MTTR tracking | Incident Trends Dashboard |
| **Problem Management** | Root cause categorization | Business Impact Scoring Model |
| **Availability Management** | Uptime % and SLA tracking | SLA Compliance Matrix |
| **Capacity Management** | ML forecasting, resource utilization | Capacity Risk Register & Prophet Models |
| **Continual Service Improvement**| Actionable recommendations | Stakeholder Memo |

---

## 🛠 Skills Demonstrated

| Skill | Where demonstrated in project |
|---|---|
| **Python Scripting** | `data_generation.py`, automated query execution |
| **Data Manipulation** | `pandas` merges, aggregations, and pivot tables in notebooks |
| **SQL Data Modeling** | `schema.sql` Primary/Foreign keys, optimized indexes |
| **Advanced SQL** | Window functions (`LAG`), conditional aggregations in `kpi_queries.sql` |
| **Machine Learning** | Time-series forecasting with Facebook `prophet` |
| **Data Visualization** | `seaborn`/`matplotlib` heatmaps and grid plots |
| **Power BI / DAX** | 15+ custom DAX measures, dynamic filtering, conditional formatting |
| **Business Communication** | ITIL-aligned `stakeholder_recommendations.md` memo |

---

## 🚀 How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/healthcare-saas-dashboard.git
   cd healthcare-saas-dashboard
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Generate Data & Setup Database**:
   ```bash
   python data_generation.py
   python load_to_db.py
   python run_queries.py
   ```
4. **Run Analysis Notebooks**:
   Open and run all cells in `notebooks/02_incident_analysis.ipynb` and `notebooks/03_capacity_forecasting.ipynb`.
5. **View Dashboard**:
   Open `healthcare_saas_dashboard.pbix` in Power BI Desktop (requires setting up the data source paths following the `docs/powerbi_instructions.md` guide).

---

## 💾 SQL Schema

```sql
CREATE TABLE IF NOT EXISTS services (
    service_id TEXT PRIMARY KEY,
    service_name TEXT NOT NULL,
    service_tier TEXT NOT NULL,
    team_owner TEXT,
    sla_uptime_target_pct REAL
);

-- (See sql/schema.sql for the complete definition of incidents, availability, capacity, and sla_tracking tables)
```

---

## 📸 ScreenShots

```Screenshots of the Dashboard Output

<img width="3300" height="2550" alt="healthcare_saas_dashboard_page-0001" src="https://github.com/user-attachments/assets/7943463c-ba6d-41a7-8a20-0a9671dd06ea" />
<img width="3300" height="2550" alt="healthcare_saas_dashboard_page-0002" src="https://github.com/user-attachments/assets/5fb49314-dd81-4fdc-8152-19a1a9d1cb99" />
<img width="3300" height="2550" alt="healthcare_saas_dashboard_page-0003" src="https://github.com/user-attachments/assets/e7274a00-6b0e-458e-bedf-d389d989d3f3" />

```



## 👤 Author

**Aasritha Adapa**
- Email: [aasrithaadapa@gmail.comL]

*Built for the Service Performance Analyst role application.*
