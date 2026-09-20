from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Initialize FastAPI App
app = FastAPI(
    title="RetentionX Analytics Engine API",
    description="API бэкенда для аналитической платформы и прогнозирования оттока",
    version="1.0.0"
)

# CORS setup (позволяет фронтенду свободно отправлять запросы к бэкенду)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# 1. ML Predictor Logic (Модель прогнозирования оттока)
# ------------------------------------------------------------------
class ChurnPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._train_dummy_model()

    def _train_dummy_model(self):
        # Синтетические данные для примера [неактивность, тикеты, падение активности %]
        X = np.random.rand(1000, 3) * [30, 10, 100]
        y = (X[:, 0] > 14) | (X[:, 1] > 3) | (X[:, 2] > 50)
        self.model.fit(X, y.astype(int))

    def predict_risk(self, inactivity_days: int, support_tickets: int, usage_drop: float):
        features = np.array([[inactivity_days, support_tickets, usage_drop]])
        prob = self.model.predict_proba(features)[0][1]
        
        factors = []
        if inactivity_days > 10:
            factors.append(f"Высокая неактивность ({inactivity_days} дн.)")
        if support_tickets >= 3:
            factors.append(f"Частые обращения в поддержку ({support_tickets} шт.)")
        if usage_drop > 40:
            factors.append(f"Падение активности на {usage_drop}%")

        return {
            "churn_risk_percent": round(prob * 100, 1),
            "risk_level": "CRITICAL" if prob > 0.7 else "MEDIUM" if prob > 0.4 else "LOW",
            "top_risk_factors": factors or ["Стабильная активность"]
        }

predictor = ChurnPredictor()

# ------------------------------------------------------------------
# 2. Pydantic Модели (Схемы данных для входных запросов)
# ------------------------------------------------------------------
class UserMetricsInput(BaseModel):
    user_id: str
    inactivity_days: int
    support_tickets: int
    usage_drop_percent: float

class UnitEconomicsInput(BaseModel):
    cac: float               # Стоимость привлечения ($)
    arpu: float              # Средняя выручка с пользователя ($)
    lifespan_months: int     # Время жизни клиента (в месяцах)

# ------------------------------------------------------------------
# 3. API Endpoints
# ------------------------------------------------------------------

@app.get("/", tags=["General"])
def root():
    """Проверка работоспособности API"""
    return {"status": "ok", "message": "RetentionX Analytics Backend Running"}


@app.get("/api/v1/metrics/summary", tags=["Analytics"])
def get_metrics_summary():
    """Сводная аналитика для верхней панели дашборда"""
    return {
        "mrr": 425000,
        "net_revenue_retention": 112.4,
        "avg_churn_rate": 2.1,
        "ltv_cac_ratio": 4.8
    }


@app.get("/api/v1/customers/at-risk", tags=["Analytics"])
def get_at_risk_customers():
    """Список пользователей с повышенным риском оттока для таблицы"""
    return [
        {
            "id": "USR-8921",
            "name": "TechCorp Logistics",
            "mrr": 4200,
            "inactivity": 18,
            "tickets": 4,
            "risk_score": 87,
            "risk_level": "CRITICAL",
            "top_factor": "Высокая неактивность (18 дн.)"
        },
        {
            "id": "USR-4102",
            "name": "FinTech Global",
            "mrr": 8900,
            "inactivity": 12,
            "tickets": 5,
            "risk_score": 74,
            "risk_level": "CRITICAL",
            "top_factor": "Частые обращения в поддержку"
        },
        {
            "id": "USR-1054",
            "name": "Retail Systems",
            "mrr": 1800,
            "inactivity": 8,
            "tickets": 2,
            "risk_score": 42,
            "risk_level": "MEDIUM",
            "top_factor": "Падение активности на 45%"
        }
    ]


@app.post("/api/v1/predict/churn", tags=["ML Prediction"])
def predict_churn(data: UserMetricsInput):
    """Индивидуальный ML-прогноз оттока по параметрам пользователя"""
    result = predictor.predict_risk(
        inactivity_days=data.inactivity_days,
        support_tickets=data.support_tickets,
        usage_drop=data.usage_drop_percent
    )
    return {
        "user_id": data.user_id,
        "prediction": result
    }


@app.post("/api/v1/analytics/unit-economics", tags=["Analytics"])
def calculate_unit_economics(data: UnitEconomicsInput):
    """Расчет LTV, LTV/CAC и оценки юнит-экономики"""
    ltv = data.arpu * data.lifespan_months
    ltv_cac_ratio = round(ltv / data.cac, 2) if data.cac > 0 else 0
    is_healthy = ltv_cac_ratio >= 3.0

    return {
        "ltv": ltv,
        "cac": data.cac,
        "ltv_cac_ratio": ltv_cac_ratio,
        "is_healthy": is_healthy,
        "status": "Здоровая экономика" if is_healthy else "Высокий CAC или высокий отток"
    }
