import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class ChurnPredictor:
    def __init__(self):
        # Инициализируем тестовую модель
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._train_dummy_model()

    def _train_dummy_model(self):
        # Имитация обучения на синтетических данных
        # Признаки: [дни без активности, кол-во тикетов поддержки, падение использования %]
        X = np.random.rand(1000, 3) * [30, 10, 100]
        y = (X[:, 0] > 14) | (X[:, 1] > 3) | (X[:, 2] > 50)
        self.model.fit(X, y.astype(int))

    def predict_risk(self, inactivity_days: int, support_tickets: int, usage_drop: float):
        features = np.array([[inactivity_days, support_tickets, usage_drop]])
        prob = self.model.predict_proba(features)[0][1]
        
        # Оцениваем главные факторы риск-профиля
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
            "top_risk_factors": factors or ["Нормальная активность"]
        }

predictor = ChurnPredictor()
