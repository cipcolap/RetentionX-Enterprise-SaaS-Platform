# 📊 RetentionX — SaaS Churn Analytics & Unit Economics Engine

**RetentionX** — это сквозная аналитическая платформа для подписочных сервисов (SaaS/Subscription Business). Продукт объединяет когортный анализ удержания (Retention), расчёт показателей юнит-экономики и машинное обучение для прогнозирования оттока клиентов (Churn Prediction) на ранней стадии.

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn%20%2F%20CatBoost-orange.svg)

---

## 🚀 Ключевые возможности

* **Product Analytics & Cohorts:** Автоматическое построение когортных матриц Retention Rate по месяцам.
* **Unit Economics Calculator:** Моделирование LTV, CAC, ARPU и расчет коэффициента здоровья экономики ($LTV/CAC \ge 3.0$).
* **ML Churn Prediction Engine:** Классификатор факторов риска оттока на основе машинного обучения.
* **Risk Profiling (XAI):** Выделение ключевых паттернов ухода клиентов (неактивность, тикеты поддержки, падение активности) для таргетированного маркетинга.
* **Interactive Dashboard:** Динамический интерфейс с живой фильтрацией клиентов группы риска и выгрузкой отчетов.

---

## 🏗️ Архитектура системы

Проект построен по сервисной архитектуре и разделен на фронтенд и бэкенд:

```text
               ┌────────────────────────┐
               │    Frontend (Client)   │
               │ HTML5 / Tailwind / JS  │
               └───────────┬────────────┘
                           │  HTTP / REST API (fetch)
                           ▼
               ┌────────────────────────┐
               │   FastAPI Backend API  │
               └─────┬────────────┬─────┘
                     │            │
  ┌──────────────────┴──┐      ┌──┴──────────────────┐
  │  ML Model (Churn)   │      │ Database / SQL      │
  │ Scikit-Learn/CatBoost │      │ PostgreSQL (Schema) │
  └─────────────────────┘      └─────────────────────┘
