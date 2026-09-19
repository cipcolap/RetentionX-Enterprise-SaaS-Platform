# RetentionX Engine 🚀
> Autonomous Revenue Loss Prevention & Churn Analytics Platform for B2B SaaS

RetentionX Engine is an enterprise-grade Micro-SaaS platform designed to predict customer churn, optimize unit economics ($LTV$, $CAC$, $Payback$), and trigger automated AI-driven rescue workflows before users cancel their subscriptions.

---

## Key Features

* **Interactive Unit Economics Simulator:** Real-time $LTV$, $CAC$, and $ARR$ forecasting with dynamic slider adjustments.
* **Cohort Retention Matrix:** Color-coded $M0 \dots M12$ retention heatmaps and retention curve analysis.
* **ML Churn Predictor & SHAP Factors:** Machine learning classification (CatBoost/XGBoost) with explicit risk attribution.
* **Autonomous AI Playbooks:** Automated agentic rescue workflows (discounts, VIP concierge, support escalations).
* **Gemini API Integration:** AI-generated strategic retention advisories tailored to live financial metrics.
* **$1M Investor Pitch Deck:** Built-in interactive pitch deck for fundraising and demonstration.

---

## Tech Stack

* **Frontend:** React, Tailwind CSS, Recharts, Lucide Icons, Vite
* **Backend:** Python 3.10+, FastAPI, Pandas, NumPy, CatBoost, SHAP
* **AI Engine:** Google Gemini API (`@google/genai`)

---

## Quick Start

### 1. Frontend Setup
```bash
# Clone the repository
git clone [https://github.com/your-username/retentionx-engine.git](https://github.com/your-username/retentionx-engine.git)
cd retentionx-engine

# Install dependencies & run locally
npm install
npm run dev
