# DMed - Smart Hospital Management System

## 🏥 Overview
DMed is a comprehensive digital platform for hospital registration, triage, and online appointment booking.

## 🚀 Features
- **Smart Triage**: AI-powered complaint classification (Urgent/Chronic/Fast)
- **Real-time Bed Allocation**: Automatic bed assignment based on category
- **Online Booking**: Patients can book appointments via mobile/web
- **Admin Dashboard**: Real-time analytics and reporting
- **EMR Integration**: Seamless integration with existing hospital systems
- **Multi-platform**: Web, Mobile (React Native), and Kiosk

## 🛠️ Tech Stack
- **Backend**: FastAPI, PostgreSQL, Redis, Celery
- **Frontend**: React, TailwindCSS, WebSocket
- **Mobile**: React Native
- **AI/ML**: Scikit-learn, TfidfVectorizer, RandomForest
- **DevOps**: Docker, Kubernetes (optional), GitHub Actions
- **Monitoring**: Prometheus, Grafana

## 📦 Quick Start

### Development
```bash
# Clone repository
git clone https://github.com/your-org/dmed.git
cd dmed

# Start services
docker-compose up -d

D:\dmed-full\dist\DMedRelease\DMed\
├── DMed.exe              ← asosiy dastur
├── ISHGA_TUSHIRISH.bat   ← buni bosing
├── backend\              ← API + PostgreSQL
├── frontend\build\       ← web interfeys
├── ai-model\             ← AI triage modeli
└── runtime\postgres\     ← PostgreSQL (port 55432)