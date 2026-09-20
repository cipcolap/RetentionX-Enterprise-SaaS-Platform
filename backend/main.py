from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from catboost import CatBoostClassifier, Pool
import shap
import json

app = FastAPI(title="RetentionX API", version="1.0.0")

# Настройка CORS для работы с фронтендом Vercel/Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "RetentionX ML Engine is running"}

@app.post("/api/analyze-churn")
async def analyze_churn(file: UploadFile = File(...)):
    try:
        # 1. Чтение загруженного CSV-файла
        df = pd.read_csv(file.file)
        
        # Проверка необходимых колонок
        required_cols = ['user_id', 'monthly_spend', 'inactivity_days', 'support_tickets', 'churn']
        for col in required_cols:
            if col not in df.columns:
                raise HTTPException(status_code=400, detail=f"Отсутствует обязательная колонка: {col}")

        # 2. Подготовка фичей и обучение ML-модели (CatBoost)
        X = df[['monthly_spend', 'inactivity_days', 'support_tickets']]
        y = df['churn']

        model = CatBoostClassifier(iterations=100, depth=4, learning_rate=0.1, verbose=0)
        model.fit(X, y)

        # 3. Расчёт вероятностей оттока
        probabilities = model.predict_proba(X)[:, 1]
        df['churn_risk_pct'] = (probabilities * 100).round(1)

        # 4. Расчёт факторов SHAP (Интерпретируемость оттока)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

        # 5. Формирование списка клиентов высокого риска
        high_risk_users = []
        feature_names = ['Расходы в месяц', 'Дни неактивности', 'Обращения в поддержку']
        
        for idx, row in df.iterrows():
            if row['churn_risk_pct'] >= 40.0:
                # Определение главного фактора риска через SHAP
                user_shap = shap_values[idx]
                top_feature_idx = np.argmax(np.abs(user_shap))
                top_reason = f"Высокий фактор: {feature_names[top_feature_idx]}"

                high_risk_users.append({
                    "id": str(row['user_id']),
                    "name": f"Клиент #{row['user_id']}",
                    "email": f"user_{row['user_id']}@company.com",
                    "plan": "Enterprise" if row['monthly_spend'] > 300 else "Standard",
                    "mrr": float(row['monthly_spend']),
                    "risk": float(row['churn_risk_pct']),
                    "reason": top_reason,
                    "inactivity": int(row['inactivity_days']),
                    "tickets": int(row['support_tickets'])
                })

        # 6. Расчёт ключевых метрик юнит-экономики
        total_mrr = float(df['monthly_spend'].sum())
        avg_arpu = float(df['monthly_spend'].mean())
        overall_churn = float((df['churn'].mean() * 100).round(1))

        return {
            "status": "success",
            "summary": {
                "total_users": len(df),
                "total_mrr": total_mrr,
                "arpu": avg_arpu,
                "overall_churn_rate": overall_churn,
                "high_risk_count": len(high_risk_users)
            },
            "high_risk_users": sorted(high_risk_users, key=lambda x: x['risk'], reverse=True)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
