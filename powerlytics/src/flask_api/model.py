from xgboost import XGBClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

df = pd.read_csv(r"faket_retgen\src\flask_api\enerji_veri_seti.csv")

# Yeni özellik mühendisliği
df["Enerji Kullanım Oranı"] = df["Kullanılan Enerji (kWh)"] / (df["Çekilen Enerji (kWh)"] + 1e-6)

# Yoğun saatler: 06:00-18:00 arası yoğun saat kabul edelim (360-1080 dakika)
df["Saat Dilimi"] = df["Saat Dilimi"].apply(lambda x: int(x.split(":")[0]) * 60 + int(x.split(":")[1]))
df["Yoğun Saat Mi"] = df["Saat Dilimi"].apply(lambda x: 1 if 360 <= x <= 1080 else 0)

# Kategorik verileri kodlama
le_firma = LabelEncoder()
le_makine = LabelEncoder()
le_durum = LabelEncoder()
le_oneri = LabelEncoder()  # Öneri sütunu için LabelEncoder eklendi

df["Firma Adı"] = le_firma.fit_transform(df["Firma Adı"])
df["Makine Türü"] = le_makine.fit_transform(df["Makine Türü"])
df["Çalışma Durumu"] = le_durum.fit_transform(df["Çalışma Durumu"])
df["Öneri_Encoded"] = le_oneri.fit_transform(df["Öneri"])  # Öneri sütununu kodlama

# Güncellenmiş giriş değişkenleri
X = df[["Firma Adı", "Makine Türü", "Çekilen Enerji (kWh)", "Kullanılan Enerji (kWh)", 
        "Çalışma Durumu", "Saat Dilimi", "Enerji Kullanım Oranı", "Yoğun Saat Mi"]]

y = df["Öneri_Encoded"]  # Kodlanmış öneri sütununu kullanma

# Veriyi tekrar eğitim ve test setlerine ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost modeli oluşturma ve eğitme
xgb_model = XGBClassifier(n_estimators=200, learning_rate=0.1, max_depth=6, random_state=42)
xgb_model.fit(X_train, y_train)

# Modelin doğruluğunu değerlendirme
y_pred_xgb = xgb_model.predict(X_test)
accuracy_xgb = accuracy_score(y_test, y_pred_xgb)
report_xgb = classification_report(y_test, y_pred_xgb)

print(f"Accuracy: {accuracy_xgb}")
print("\nClassification Report:")
print(report_xgb)

# Sınıf etiketlerinin gerçek değerlerini görmek için
print("\nSınıf Etiketleri Eşleştirmesi:")
for i, label in enumerate(le_oneri.classes_):
    print(f"{i}: {label}")

# Model ve Label Encoder'ları kaydetme
# Modeller için klasör oluşturma
os.makedirs('models', exist_ok=True)

# XGBoost modelini kaydetme
with open('models/xgboost_energy_model.pkl', 'wb') as f:
    pickle.dump(xgb_model, f)

# Label Encoder'ları kaydetme
encoders = {
    'firma': le_firma,
    'makine': le_makine,
    'durum': le_durum,
    'oneri': le_oneri
}

with open('models/label_encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)

print("\nModel ve Label Encoder'lar başarıyla kaydedildi.")