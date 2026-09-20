from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ml_model import predictor

app = FastAPI(title="RetentionX Analytics Engine API")

# Включаем CORS, чтобы фронтенд мог свободно делать запросы к бэкенду
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMetricsInput(BaseModel):
    user_id: str
    inactivity_days: int
    support_tickets: int
    usage_drop_percent: float

@app.get("/")
def root():
    return {"status": "ok", "message": "RetentionX Analytics Backend Running"}

@app.get("/api/v1/metrics/summary")
def get_metrics_summary():
    # Эндпоинт для общей сводки дашборда
    return {
        "mrr": 425000,
        "net_revenue_retention": 112.4,
        "avg_churn_rate": 2.1,
        "ltv_cac_ratio": 4.8
    }

@app.post("/api/v1/predict/churn")
def predict_churn(data: UserMetricsInput):
    # ML-прогноз для конкретного пользователя
    result = predictor.predict_risk(
        inactivity_days=data.inactivity_days,
        support_tickets=data.support_tickets,
        usage_drop=data.usage_drop_percent
    )
    return {
        "user_id": data.user_id,
        "prediction": result
    }
