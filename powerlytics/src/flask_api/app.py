from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

app = Flask(__name__)
CORS(app)  # CORS'u etkinleştir

# Modeller için klasör oluşturma
os.makedirs('models', exist_ok=True)

# Global değişkenler
model = None
le_firma = None
le_makine = None

def train_model():
    global model, le_firma, le_makine
    
    # Veri setini oku
    df = pd.read_csv(r'faket_retgen\src\flask_api\enerji_veri_seti.csv')
    
    # Kategorik değişkenleri encode et
    le_firma = LabelEncoder()
    le_makine = LabelEncoder()
    
    df['Firma Adı'] = le_firma.fit_transform(df['Firma Adı'])
    df['Makine Türü'] = le_makine.fit_transform(df['Makine Türü'])
    
    # Saat dilimini sayısal değere çevir
    df['Saat'] = df['Saat Dilimi'].apply(lambda x: int(x.split(':')[0]))
    df['Dakika'] = df['Saat Dilimi'].apply(lambda x: int(x.split(':')[1]))
    
    # Feature'ları seç
    features = ['Firma Adı', 'Makine Türü', 'Çekilen Enerji (kWh)', 
                'Kullanılan Enerji (kWh)', 'Çalışma Durumu', 'Verimlilik (%)',
                'Saat', 'Dakika']
    
    X = df[features]
    y = df['Öneri']
    
    # Modeli eğit
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Encoder'ları ve modeli kaydet
    joblib.dump(model, 'models/model.joblib')
    joblib.dump(le_firma, 'models/le_firma.joblib')
    joblib.dump(le_makine, 'models/le_makine.joblib')

# Uygulama başlatıldığında modeli eğit
train_model()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Request'ten verileri al
        data = request.get_json()
        
        # Gelen veriyi hazırla
        firma = le_firma.transform([data['firma_adi']])[0]
        makine = le_makine.transform([data['makine_turu']])[0]
        saat = int(data['saat_dilimi'].split(':')[0])
        dakika = int(data['saat_dilimi'].split(':')[1])
        
        # Tahmin için feature'ları hazırla
        features = np.array([[
            firma,
            makine,
            float(data['cekilen_enerji']),
            float(data['kullanilan_enerji']),
            int(data['calisma_durumu']),
            float(data['verimlilik']),
            saat,
            dakika
        ]])
        
        # Tahmin yap
        prediction = model.predict(features)[0]
        
        return jsonify({
            'oneri': prediction
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400

@app.route('/model-info', methods=['GET'])
def model_info():
    """Model bilgilerini döndüren endpoint"""
    return jsonify({
        'model_type': 'Random Forest Classifier',
        'features': [
            'Firma Adı', 'Makine Türü', 'Çekilen Enerji (kWh)', 
            'Kullanılan Enerji (kWh)', 'Çalışma Durumu', 'Verimlilik (%)',
            'Saat', 'Dakika'
        ],
        'unique_firms': list(le_firma.classes_),
        'unique_machines': list(le_makine.classes_)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)