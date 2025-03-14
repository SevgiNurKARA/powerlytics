from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score
import joblib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS yapılandırmasını daha açık bir şekilde belirtelim
CORS(app, origins=["http://localhost:3000"], supports_credentials=True, allow_headers=["Content-Type", "Authorization"])

# Modeller için klasör oluşturma
os.makedirs('models', exist_ok=True)

# Global değişkenler
model = None
le_firma = None

le_makine = None
le_durum = None
le_oneri = None
scaler = None
selector = None

# Verim hesabı için saatlik birim maliyet
birim_elektrik_maliyeti = {  
    '00-06': 0.5, '06-12': 0.8, '12-18': 1.2, '18-24': 0.9
}

# Saatlik maliyet bilgisi (detaylı)
saatlik_maliyet = {
    0: 0.5, 1: 0.5, 2: 0.4, 3: 0.4, 4: 0.3, 5: 0.3,
    6: 0.6, 7: 0.7, 8: 0.8, 9: 1.0, 10: 1.2, 11: 1.3,
    12: 1.4, 13: 1.3, 14: 1.2, 15: 1.0, 16: 0.9, 17: 0.8,
    18: 0.7, 19: 0.6, 20: 0.5, 21: 0.5, 22: 0.4, 23: 0.4
}

CARBON_EMISSION_FACTOR = 0.4  # 1 kWh başına karbon emisyonu (kg)

def saat_araligi(saat):
    if 0 <= saat < 6:
        return '00-06'
    elif 6 <= saat < 12:
        return '06-12'
    elif 12 <= saat < 18:
        return '12-18'
    else:
        return '18-24'

def train_model():
    global model, le_firma, le_makine, le_durum, le_oneri, scaler, selector
    
    # Veri setini oku
    df = pd.read_csv(r'powerlytics\powerlytics\src\flask_api\enerji_veri_seti.csv')
    
    # Temel özellikler
    df["Saat"] = df["Saat Dilimi"].apply(lambda x: int(x.split(":")[0]))
    df["Dakika"] = df["Saat Dilimi"].apply(lambda x: int(x.split(":")[1]))
    df["Saat Aralığı"] = df["Saat"].apply(saat_araligi)
    df["Günlük Maliyet"] = df.apply(lambda row: row["Kullanılan Enerji (kWh)"] * birim_elektrik_maliyeti[row["Saat Aralığı"]], axis=1)
    
    # Alternatif maliyet önerisi
    def en_uygun_saat(row):
        en_dusuk_maliyetli_saat = min(birim_elektrik_maliyeti, key=birim_elektrik_maliyeti.get)
        ideal_maliyet = row["Kullanılan Enerji (kWh)"] * birim_elektrik_maliyeti[en_dusuk_maliyetli_saat]
        return en_dusuk_maliyetli_saat, ideal_maliyet
    
    df[["Önerilen Saat", "Önerilen Maliyet"]] = df.apply(en_uygun_saat, axis=1, result_type="expand")
    
    # Karbon ayak izi hesabı
    df["Karbon Ayak İzi (kg)"] = df["Kullanılan Enerji (kWh)"] * CARBON_EMISSION_FACTOR
    
    # YENİ ÖZELLİKLER
    # Enerji verimliliği yüzdesi
    df["Enerji Verimliliği (%)"] = (df["Kullanılan Enerji (kWh)"] / df["Çekilen Enerji (kWh)"]) * 100
    
    # Maliyet farkı (Güncel maliyet - önerilen maliyet)
    df["Maliyet Farkı"] = df["Günlük Maliyet"] - df["Önerilen Maliyet"]
    
    # Maliyet tasarruf potansiyeli yüzdesi
    df["Tasarruf Potansiyeli (%)"] = (df["Maliyet Farkı"] / df["Günlük Maliyet"]) * 100
    
    # Tarih bilgisi varsa gün kategorisi ve mevsim bilgisi ekle
    if "Tarih" in df.columns:
        df["Tarih"] = pd.to_datetime(df["Tarih"])
        df["Haftanın Günü"] = df["Tarih"].dt.dayofweek
        df["Hafta Sonu mu"] = df["Haftanın Günü"].apply(lambda x: 1 if x >= 5 else 0)
        df["Ay"] = df["Tarih"].dt.month
        df["Mevsim"] = df["Ay"].apply(lambda x: 0 if 3 <= x <= 5 else (1 if 6 <= x <= 8 else (2 if 9 <= x <= 11 else 3)))
    
    # One-hot encoding ile saat aralığı özelliği
    saat_araligi_dummies = pd.get_dummies(df["Saat Aralığı"], prefix="Saat_Araligi")
    df = pd.concat([df, saat_araligi_dummies], axis=1)
    
    # ISO 50001 verileri için regresyon analizleri
    # 1. Enerji kullanımı ve maliyet
    plt.figure(figsize=(10, 6))
    sns.regplot(x=df["Kullanılan Enerji (kWh)"], y=df["Günlük Maliyet"], scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    plt.xlabel("Kullanılan Enerji (kWh)")
    plt.ylabel("Günlük Maliyet")
    plt.title("Günlük Enerji Kullanımı ve Maliyet İlişkisi")
    plt.savefig("models/regresyon_gunluk.png")
    plt.close()
    
    # 2. Çekilen ve kullanılan enerji arasındaki ilişki
    plt.figure(figsize=(10, 6))
    sns.regplot(x=df["Çekilen Enerji (kWh)"], y=df["Kullanılan Enerji (kWh)"], scatter_kws={'alpha':0.5}, line_kws={'color':'green'})
    plt.xlabel("Çekilen Enerji (kWh)")
    plt.ylabel("Kullanılan Enerji (kWh)")
    plt.title("ISO 50001 Enerji Kullanımı Regresyon Analizi")
    plt.savefig("models/iso_50001_regresyon.png")
    plt.close()
    
    # Kategorik değişkenleri encode et
    le_firma = LabelEncoder()
    le_makine = LabelEncoder()
    le_durum = LabelEncoder()
    le_oneri = LabelEncoder()
    
    df["Firma Adı"] = le_firma.fit_transform(df["Firma Adı"])
    df["Makine Türü"] = le_makine.fit_transform(df["Makine Türü"])
    df["Çalışma Durumu"] = le_durum.fit_transform(df["Çalışma Durumu"])
    df["Öneri_Encoded"] = le_oneri.fit_transform(df["Öneri"])
    
    # Özellik listesini oluştur
    features = ["Firma Adı", "Makine Türü", "Çekilen Enerji (kWh)", "Kullanılan Enerji (kWh)",
                "Çalışma Durumu", "Saat", "Dakika", "Günlük Maliyet", "Karbon Ayak İzi (kg)",
                "Enerji Verimliliği (%)", "Maliyet Farkı", "Tasarruf Potansiyeli (%)"]
    
    # Hafta Sonu ve Mevsim özelliklerini ekle
    if "Hafta Sonu mu" in df.columns:
        features.append("Hafta Sonu mu")
    if "Mevsim" in df.columns:
        features.append("Mevsim")
    
    # Saat aralığı one-hot kodlanmış özellikleri ekle
    for col in saat_araligi_dummies.columns:
        features.append(col)
    
    X = df[features]
    y = df["Öneri_Encoded"]
    
    # Veri ölçeklendirme
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Eğitim ve test setlerini ayırma
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
    
    # XGBoost modeli eğit (geliştirilmiş parametrelerle)
    # Not: Burada daha önce belirlenen en iyi parametreleri kullanıyoruz
    model = XGBClassifier(
        n_estimators=300,
        learning_rate=0.1,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        gamma=0.1,
        min_child_weight=3,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Özellik seçimi
    selector = SelectFromModel(model, threshold='mean')
    selector.fit(X_train, y_train)
    selected_feat_idx = selector.get_support()
    selected_features = [features[i] for i in range(len(features)) if selected_feat_idx[i]]
    
    # Seçilmiş özelliklerle model eğitimi
    X_train_selected = selector.transform(X_train)
    X_test_selected = selector.transform(X_test)
    
    # Final modeli oluştur
    final_model = XGBClassifier(
        n_estimators=300,
        learning_rate=0.1,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        gamma=0.1,
        min_child_weight=3,
        random_state=42
    )
    
    final_model.fit(X_train_selected, y_train)
    
    # Test seti üzerinde performans değerlendirmesi
    y_pred = final_model.predict(X_test_selected)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Final modeli kullan
    model = final_model
    
    # Modeli, encoderları ve diğer bileşenleri kaydet
    joblib.dump(model, 'models/xgboost_model.joblib')
    joblib.dump(le_firma, 'models/le_firma.joblib')
    joblib.dump(le_makine, 'models/le_makine.joblib')
    joblib.dump(le_durum, 'models/le_durum.joblib')
    joblib.dump(le_oneri, 'models/le_oneri.joblib')
    joblib.dump(scaler, 'models/scaler.joblib')
    joblib.dump(selector, 'models/selector.joblib')
    joblib.dump(features, 'models/features.joblib')
    joblib.dump(selected_features, 'models/selected_features.joblib')
    
    # Model bilgilerini loglama
    model_info = {
        'Model Türü': 'XGBoost Classifier',
        'Doğruluk (Accuracy)': accuracy,
        'Toplam Özellik Sayısı': len(features),
        'Seçilen Özellik Sayısı': len(selected_features),
        'Seçilen Özellikler': selected_features,
        'Eğitim Tarihi': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('models/model_info.txt', 'w') as f:
        for key, value in model_info.items():
            f.write(f"{key}: {value}\n")
    
    print(f"Model başarıyla eğitildi. Doğruluk: {accuracy:.4f}")
    return model_info

# Uygulama başlatıldığında modeli eğit veya kayıtlı modeli yükle
@app.route('/train', methods=['GET'])
def run_training():
    try:
        model_info = train_model()
        return jsonify({
            'success': True,
            'model_info': model_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def load_models():
    global model, le_firma, le_makine, le_durum, le_oneri, scaler, selector
    
    try:
        model = joblib.load('models/xgboost_model.joblib')
        le_firma = joblib.load('models/le_firma.joblib')
        le_makine = joblib.load('models/le_makine.joblib')
        le_durum = joblib.load('models/le_durum.joblib')
        le_oneri = joblib.load('models/le_oneri.joblib')
        scaler = joblib.load('models/scaler.joblib')
        selector = joblib.load('models/selector.joblib')
        features = joblib.load('models/features.joblib')
        selected_features = joblib.load('models/selected_features.joblib')
        return True
    except:
        print("Kaydedilmiş model bulunamadı, yeni model eğitiliyor...")
        train_model()
        return True

# Uygulama başlatıldığında modeli yükle
load_models()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Modellerin yüklü olduğundan emin ol
        if model is None or scaler is None or selector is None:
            load_models()

        # Request'ten verileri al
        data = request.get_json()
        
        # Gerekli özellikleri hazırla
        # Firma kodunu al
        if data.get('firma_adi') in le_firma.classes_:
            firma = le_firma.transform([data['firma_adi']])[0]
        else:
            firma = -1  # Bilinmeyen firma için -1
        
        # Makine türü kodunu al
        if data.get('makine_turu') in le_makine.classes_:
            makine = le_makine.transform([data['makine_turu']])[0]
        else:
            makine = -1  # Bilinmeyen makine türü için -1
        
        # Çalışma durumu kodunu al
        if data.get('calisma_durumu', 0) in le_durum.classes_:
            durum = le_durum.transform([data['calisma_durumu']])[0]
        else:
            durum = 0  # Varsayılan olarak 0
        
        # Saat bilgilerini al
        saat_dilimi = data.get('saat_dilimi', '00:00')
        saat = int(saat_dilimi.split(':')[0])
        dakika = int(saat_dilimi.split(':')[1]) if len(saat_dilimi.split(':')) > 1 else 0
        
        # Enerji değerlerini al
        cekilen_enerji = float(data.get('cekilen_enerji', 0))
        kullanilan_enerji = float(data.get('kullanilan_enerji', 0))
        
        # Temel hesaplamalar
        saat_aralik = saat_araligi(saat)
        gunluk_maliyet = kullanilan_enerji * birim_elektrik_maliyeti[saat_aralik]
        karbon_ayak_izi = kullanilan_enerji * CARBON_EMISSION_FACTOR
        
        # İleri hesaplamalar
        enerji_verimliligi = (kullanilan_enerji / cekilen_enerji * 100) if cekilen_enerji > 0 else 0
        
        # En uygun saat ve maliyet hesabı
        en_dusuk_maliyetli_saat = min(birim_elektrik_maliyeti, key=birim_elektrik_maliyeti.get)
        onerilen_maliyet = kullanilan_enerji * birim_elektrik_maliyeti[en_dusuk_maliyetli_saat]
        
        maliyet_farki = gunluk_maliyet - onerilen_maliyet
        tasarruf_potansiyeli = (maliyet_farki / gunluk_maliyet * 100) if gunluk_maliyet > 0 else 0
        
        # Saat aralığı one-hot kodlama
        saat_araligi_features = {}
        for aralik in ['00-06', '06-12', '12-18', '18-24']:
            prefix = f"Saat_Araligi_{aralik}"
            saat_araligi_features[prefix] = 1 if saat_aralik == aralik else 0
        
        # Tüm özellikleri bir araya getir
        feature_dict = {
            "Firma Adı": firma,
            "Makine Türü": makine,
            "Çekilen Enerji (kWh)": cekilen_enerji,
            "Kullanılan Enerji (kWh)": kullanilan_enerji,
            "Çalışma Durumu": durum,
            "Saat": saat,
            "Dakika": dakika,
            "Günlük Maliyet": gunluk_maliyet,
            "Karbon Ayak İzi (kg)": karbon_ayak_izi,
            "Enerji Verimliliği (%)": enerji_verimliligi,
            "Maliyet Farkı": maliyet_farki,
            "Tasarruf Potansiyeli (%)": tasarruf_potansiyeli
        }
        
        # Saat aralıklarını ekle
        feature_dict.update(saat_araligi_features)
        
        # Tarih ile ilgili özellikler, eğer bunlar modelde kullanıldıysa burada değerlendirilir
        if 'tarih' in data:
            tarih = pd.to_datetime(data['tarih'])
            feature_dict["Haftanın Günü"] = tarih.dayofweek
            feature_dict["Hafta Sonu mu"] = 1 if tarih.dayofweek >= 5 else 0
            feature_dict["Ay"] = tarih.month
            feature_dict["Mevsim"] = 0 if 3 <= tarih.month <= 5 else (1 if 6 <= tarih.month <= 8 else (2 if 9 <= tarih.month <= 11 else 3))
        
        # features nesnesini joblib'den yükle
        features = joblib.load('models/features.joblib')
        
        # Model için gerekli özelliklerin tam listesini oluştur
        feature_list = []
        for feature in features:
            feature_list.append(feature_dict.get(feature, 0))  # Eksik özellikler için 0 koy
        
        # Özellikleri ölçeklendir
        scaled_features = scaler.transform([feature_list])
        
        # Özellik seçimini uygula
        selected_features = selector.transform(scaled_features)
        
        # Tahmin yap
        prediction_encoded = model.predict(selected_features)[0]
        prediction = le_oneri.inverse_transform([prediction_encoded])[0]
        
        # Sonuçları hazırla
        result = {
            'oneri': prediction,
            'gunluk_maliyet': gunluk_maliyet,
            'onerilen_maliyet': onerilen_maliyet,
            'tasarruf_potansiyeli': tasarruf_potansiyeli,
            'karbon_ayak_izi': karbon_ayak_izi,
            'enerji_verimliligi': enerji_verimliligi,
            'onerilen_saat_araligi': en_dusuk_maliyetli_saat
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'stack_trace': str(e.__traceback__.tb_lineno)
        }), 400

@app.route('/model-info', methods=['GET'])
def model_info():
    try:
        # Model bilgilerini oku
        with open('models/model_info.txt', 'r') as f:
            info_lines = f.readlines()
        
        info_dict = {}
        for line in info_lines:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                info_dict[key.strip()] = value.strip()
        
        # Ek bilgileri ekle
        info_dict['unique_firms'] = list(le_firma.classes_) if le_firma is not None else []
        info_dict['unique_machines'] = list(le_makine.classes_) if le_makine is not None else []
        
        return jsonify(info_dict)
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

# Enerji analizini görselleştiren endpoint
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        
        # Gerekli veriler
        cekilen_enerji = float(data.get('cekilen_enerji', 0))
        kullanilan_enerji = float(data.get('kullanilan_enerji', 0))
        saat_dilimi = data.get('saat_dilimi', '00:00')
        saat = int(saat_dilimi.split(':')[0])
        
        # Elektrik maliyet bilgileri (farklı saat dilimleri için)
        birim_elektrik_maliyeti = {
            '00:00-06:00': 0.65,
            '06:00-17:00': 1.10,
            '17:00-22:00': 1.65,
            '22:00-24:00': 0.85
        }
        
        # Saat dilimi tespit etme fonksiyonu
        def saat_araligi(saat):
            if 0 <= saat < 6:
                return '00:00-06:00'
            elif 6 <= saat < 17:
                return '06:00-17:00'
            elif 17 <= saat < 22:
                return '17:00-22:00'
            else:
                return '22:00-24:00'
        
        # Karbon emisyon faktörü (kg CO2/kWh)
        CARBON_EMISSION_FACTOR = 0.47
        
        saat_aralik = saat_araligi(saat)
        gunluk_maliyet = kullanilan_enerji * birim_elektrik_maliyeti[saat_aralik]
        
        # Alternatif saat dilimlerinde maliyet hesabı
        alternatif_maliyetler = {}
        for aralik, maliyet in birim_elektrik_maliyeti.items():
            alternatif_maliyetler[aralik] = kullanilan_enerji * maliyet
        
        # En uygun saat dilimi
        optimal_saat = min(birim_elektrik_maliyeti, key=birim_elektrik_maliyeti.get)
        optimal_maliyet = alternatif_maliyetler[optimal_saat]
        tasarruf = gunluk_maliyet - optimal_maliyet if gunluk_maliyet > 0 else 0
        tasarruf_yuzdesi = (tasarruf / gunluk_maliyet * 100) if gunluk_maliyet > 0 else 0
        
        # Verimlilik
        verimlilik = (kullanilan_enerji / cekilen_enerji * 100) if cekilen_enerji > 0 else 0
        
        # Karbon ayak izi
        karbon_ayak_izi = kullanilan_enerji * CARBON_EMISSION_FACTOR
        
        # ISO 50001 değerlendirmesi (basit)
        iso_degerlendirme = "Verimli" if verimlilik > 85 else ("Orta" if verimlilik > 70 else "Verimsiz")
        
        # Saatlik maliyet verisi (görselleştirme için)
        hourly_costs = [
            {"hour": "00:00", "cost": birim_elektrik_maliyeti['00:00-06:00']},
            {"hour": "06:00", "cost": birim_elektrik_maliyeti['06:00-17:00']},
            {"hour": "17:00", "cost": birim_elektrik_maliyeti['17:00-22:00']},
            {"hour": "22:00", "cost": birim_elektrik_maliyeti['22:00-24:00']}
        ]
        
        # Regresyon verisi (görselleştirme için)
        regression_data = generate_regression_data(verimlilik)
        
        return jsonify({
            'current_time_range': saat_aralik,
            'current_cost': gunluk_maliyet,
            'alternative_costs': alternatif_maliyetler,
            'optimal_time_range': optimal_saat,
            'optimal_cost': optimal_maliyet,
            'potential_savings': tasarruf,
            'savings_percentage': tasarruf_yuzdesi,
            'efficiency': verimlilik,
            'carbon_footprint': karbon_ayak_izi,
            'iso_assessment': iso_degerlendirme,
            'hourlyCosts': hourly_costs,
            'regressionData': regression_data
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400

# Regresyon verisi üretme yardımcı fonksiyonu
def generate_regression_data(efficiency):
    import random
    
    base_points = []
    efficiency_points = []
    
    # Son 10 veri noktası için üret
    for i in range(10):
        x = 70 + random.random() * 30  # Random activity level
        y_base = x * 0.8 + random.random() * 10  # Baz tüketim
        y_efficient = x * (efficiency / 100) + random.random() * 5  # Verimli tüketim
        
        base_points.append({"x": x, "y": y_base})
        efficiency_points.append({"x": x, "y": y_efficient})
    
    return {
        "basePoints": base_points,
        "efficiencyPoints": efficiency_points,
        "regressionLine": {
            "start": {"x": 70, "y": 70 * 0.8},
            "end": {"x": 100, "y": 100 * (efficiency / 100)}
        }
    }
# Küme analizi için endpoint
@app.route('/cluster-analysis', methods=['GET'])
def cluster_analysis():
    try:
        # Veri setini oku
        df = pd.read_csv(r'powerlytics\powerlytics\src\flask_api\enerji_veri_seti.csv')
        
        # Temel analizler
        firma_bazli = df.groupby('Firma Adı').agg({
            'Kullanılan Enerji (kWh)': 'sum',
            'Çekilen Enerji (kWh)': 'sum'
        }).reset_index()
        
        firma_bazli['Verimlilik (%)'] = (firma_bazli['Kullanılan Enerji (kWh)'] / firma_bazli['Çekilen Enerji (kWh)'] * 100).round(2)
        
        # Makine türü bazlı
        makine_bazli = df.groupby('Makine Türü').agg({
            'Kullanılan Enerji (kWh)': 'mean',
            'Çekilen Enerji (kWh)': 'mean',
        }).reset_index()
        
        makine_bazli['Verimlilik (%)'] = (makine_bazli['Kullanılan Enerji (kWh)'] / makine_bazli['Çekilen Enerji (kWh)'] * 100).round(2)
        
        # Saat aralığı bazlı ortalama enerji kullanımı
        df['Saat'] = df['Saat Dilimi'].apply(lambda x: int(x.split(':')[0]))
        df['Saat Aralığı'] = df['Saat'].apply(saat_araligi)
        
        saat_bazli = df.groupby('Saat Aralığı').agg({
            'Kullanılan Enerji (kWh)': 'mean'
        }).reset_index()
        
        return jsonify({
            'firm_based': firma_bazli.to_dict(orient='records'),
            'machine_based': makine_bazli.to_dict(orient='records'),
            'time_based': saat_bazli.to_dict(orient='records')
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)