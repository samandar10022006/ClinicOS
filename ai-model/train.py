import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import re
from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parent

# Mock dataset (haqiqiy tizimda kattaroq ma'lumotlar bazasi kerak)
data = {
    'complaint': [
        'yurak ogrigi va nafas qisilishi', 'qon ketish', 'hushini yoqotdi',
        'qandli diabet kasalligi', 'gipertoniya', 'surunkali astma',
        'isitma va bosh ogrigi', 'yogol qichishadi', 'shikastlangan oyog',
        'infarkt belgilari', 'insult', 'tutqanoq',
        'doimiy bosh ogrigi', 'yurak yetishmovchiligi', 'qon bosimi tushib ketdi'
    ],
    'category': [
        'urgent', 'urgent', 'urgent',
        'chronic', 'chronic', 'chronic',
        'fast', 'fast', 'fast',
        'urgent', 'urgent', 'urgent',
        'chronic', 'chronic', 'urgent'
    ]
}

df = pd.DataFrame(data)

# Preprocessing
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Zа-яА-Я0-9\s]', '', text)
    return text

df['cleaned'] = df['complaint'].apply(preprocess_text)

# Vectorization
vectorizer = TfidfVectorizer(max_features=100)
X = vectorizer.fit_transform(df['cleaned'])
y = df['category']

# Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, MODEL_DIR / 'model.pkl')
joblib.dump(vectorizer, MODEL_DIR / 'vectorizer.pkl')

print("Model trained and saved!")