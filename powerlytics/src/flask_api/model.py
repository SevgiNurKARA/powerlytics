from xgboost import XGBClassifier
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.feature_selection import SelectFromModel
import pickle
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Veri setini yükleme
df = pd.read_csv(r"powerlytics\powerlytics\src\flask_api\enerji_veri_seti.csv")

# Verim hesabı
birim_elektrik_maliyeti = {  # Örnek saatlik maliyetler
    '00-06': 0.5, '06-12': 0.8, '12-18': 1.2, '18-24': 0.9
}

def saat_araligi(saat):
    if 0 <= saat < 6:
        return '00-06'
    elif 6 <= saat < 12:
        return '06-12'
    elif 12 <= saat < 18:
        return '12-18'
    else:
        return '18-24'

# Temel özellikler
df["Saat"] = df["Saat Dilimi"].apply(lambda x: int(x.split(":")[0]))
df["Saat Aralığı"] = df["Saat"].apply(saat_araligi)
df["Günlük Maliyet"] = df.apply(lambda row: row["Kullanılan Enerji (kWh)"] * birim_elektrik_maliyeti[row["Saat Aralığı"]], axis=1)

# Alternatif maliyet önerisi
def en_uygun_saat(row):
    en_dusuk_maliyetli_saat = min(birim_elektrik_maliyeti, key=birim_elektrik_maliyeti.get)
    ideal_maliyet = row["Kullanılan Enerji (kWh)"] * birim_elektrik_maliyeti[en_dusuk_maliyetli_saat]
    return en_dusuk_maliyetli_saat, ideal_maliyet

df[["Önerilen Saat", "Önerilen Maliyet"]] = df.apply(en_uygun_saat, axis=1, result_type="expand")

# Karbon ayak izi hesabı
karbon_faktor = 0.4  # 1 kWh için kg cinsinden karbon emisyonu
df["Karbon Ayak İzi (kg)"] = df["Kullanılan Enerji (kWh)"] * karbon_faktor

# YENİ ÖZELLİKLER EKLENDİ
# Enerji verimliliği yüzdesi
df["Enerji Verimliliği (%)"] = (df["Kullanılan Enerji (kWh)"] / df["Çekilen Enerji (kWh)"]) * 100

# Maliyet farkı (Güncel maliyet - önerilen maliyet)
df["Maliyet Farkı"] = df["Günlük Maliyet"] - df["Önerilen Maliyet"]

# Maliyet tasarruf potansiyeli yüzdesi
df["Tasarruf Potansiyeli (%)"] = (df["Maliyet Farkı"] / df["Günlük Maliyet"]) * 100

# Gün kategorisi ekleme (Hafta içi/Hafta sonu)
if "Tarih" in df.columns:
    df["Tarih"] = pd.to_datetime(df["Tarih"])
    df["Haftanın Günü"] = df["Tarih"].dt.dayofweek
    df["Hafta Sonu mu"] = df["Haftanın Günü"].apply(lambda x: 1 if x >= 5 else 0)

# Mevsim bilgisi ekleme
if "Tarih" in df.columns:
    df["Ay"] = df["Tarih"].dt.month
    df["Mevsim"] = df["Ay"].apply(lambda x: 0 if 3 <= x <= 5 else (1 if 6 <= x <= 8 else (2 if 9 <= x <= 11 else 3)))

# One-hot encoding ile saat aralığı özelliği
saat_araligi_dummies = pd.get_dummies(df["Saat Aralığı"], prefix="Saat_Araligi")
df = pd.concat([df, saat_araligi_dummies], axis=1)

# ISO 50001 verileri için regresyon analizi
plt.figure(figsize=(10, 6))
sns.regplot(x=df["Çekilen Enerji (kWh)"], y=df["Kullanılan Enerji (kWh)"], scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.xlabel("Çekilen Enerji (kWh)")
plt.ylabel("Kullanılan Enerji (kWh)")
plt.title("ISO 50001 Enerji Kullanımı Regresyon Analizi")
plt.savefig("iso_50001_regresyon.png")
plt.close()

# Enerji verimliliği dağılımı
plt.figure(figsize=(10, 6))
sns.histplot(df["Enerji Verimliliği (%)"], kde=True)
plt.axvline(df["Enerji Verimliliği (%)"].mean(), color='red', linestyle='--', label=f'Ortalama: {df["Enerji Verimliliği (%)"].mean():.2f}%')
plt.title("Enerji Verimliliği Dağılımı")
plt.xlabel("Enerji Verimliliği (%)")
plt.ylabel("Frekans")
plt.legend()
plt.savefig("enerji_verimliligi_dagilimi.png")
plt.close()

# Korelasyon analizi
plt.figure(figsize=(12, 10))
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Sayısal Değişkenler Arası Korelasyon")
plt.tight_layout()
plt.savefig("korelasyon_matrisi.png")
plt.close()

# Model eğitimi için veriyi hazırlama
le_firma = LabelEncoder()
le_makine = LabelEncoder()
le_durum = LabelEncoder()
le_oneri = LabelEncoder()

df["Firma Adı"] = le_firma.fit_transform(df["Firma Adı"])
df["Makine Türü"] = le_makine.fit_transform(df["Makine Türü"])
df["Çalışma Durumu"] = le_durum.fit_transform(df["Çalışma Durumu"])
df["Öneri_Encoded"] = le_oneri.fit_transform(df["Öneri"])

# Özellik listesini genişletme
features = ["Firma Adı", "Makine Türü", "Çekilen Enerji (kWh)", "Kullanılan Enerji (kWh)",
            "Çalışma Durumu", "Saat", "Günlük Maliyet", "Karbon Ayak İzi (kg)",
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

# Cross-validation ile mevcut modelin performansını değerlendirme
base_model = XGBClassifier(n_estimators=200, learning_rate=0.1, max_depth=6, random_state=42)
cv_scores = cross_val_score(base_model, X_train, y_train, cv=5, scoring='accuracy')
print(f"Cross-validation accuracy (base model): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# Hiperparametre optimizasyonu için RandomizedSearchCV
param_grid = {
    'n_estimators': [100, 200, 300, 400, 500],
    'max_depth': [3, 4, 5, 6, 7, 8],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0],
    'gamma': [0, 0.1, 0.2, 0.3, 0.4],
    'min_child_weight': [1, 3, 5, 7]
}

random_search = RandomizedSearchCV(
    estimator=XGBClassifier(random_state=42, eval_metric='logloss'),  # Remove use_label_encoder=False
    param_distributions=param_grid,
    n_iter=25,
    scoring='accuracy',
    cv=5,
    verbose=1,
    random_state=42,
    n_jobs=-1
)

random_search.fit(X_train, y_train)
print(f"En iyi parametreler: {random_search.best_params_}")
print(f"En iyi cross-validation accuracy: {random_search.best_score_:.4f}")

# En iyi modeli kullanarak tahmin
best_model = random_search.best_estimator_
best_model.fit(X_train, y_train)

y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Optimized Model Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(report)

# Confusion Matrix görselleştirme
plt.figure(figsize=(10, 8))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=le_oneri.classes_, yticklabels=le_oneri.classes_)
plt.xlabel('Tahmin Edilen')
plt.ylabel('Gerçek')
plt.title('Confusion Matrix')
plt.savefig("confusion_matrix.png")
plt.close()

# Özellik önemini görselleştirme
plt.figure(figsize=(12, 8))
feature_importance = best_model.feature_importances_
sorted_idx = np.argsort(feature_importance)
plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx])
plt.yticks(range(len(sorted_idx)), [features[i] for i in sorted_idx])
plt.xlabel('Özellik Önemi')
plt.title('XGBoost Özellik Önemi')
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.close()

# Özellik seçimi
selector = SelectFromModel(best_model, threshold='mean')
selector.fit(X_train, y_train)
selected_feat_idx = selector.get_support()
selected_features = [features[i] for i in range(len(features)) if selected_feat_idx[i]]
print(f"\nSeçilen Özellikler: {selected_features}")

# Seçilmiş özelliklerle model eğitimi
X_train_selected = selector.transform(X_train)
X_test_selected = selector.transform(X_test)

final_model = XGBClassifier(**random_search.best_params_, random_state=42)
final_model.fit(X_train_selected, y_train)

y_pred_final = final_model.predict(X_test_selected)
final_accuracy = accuracy_score(y_test, y_pred_final)
final_report = classification_report(y_test, y_pred_final)

print(f"\nOptimize Edilmiş Model (Özellik Seçimi Sonrası) Accuracy: {final_accuracy:.4f}")
print("\nFinal Classification Report:")
print(final_report)

# En iyi modeli ve Label Encoder'ları kaydetme
os.makedirs('models', exist_ok=True)

# Tüm modelleri kaydet
with open('models/xgboost_energy_model_base.pkl', 'wb') as f:
    pickle.dump(base_model, f)

with open('models/xgboost_energy_model_optimized.pkl', 'wb') as f:
    pickle.dump(best_model, f)

with open('models/xgboost_energy_model_final.pkl', 'wb') as f:
    pickle.dump(final_model, f)

# Ek bileşenleri kaydetme
encoders = {
    'firma': le_firma,
    'makine': le_makine,
    'durum': le_durum,
    'oneri': le_oneri
}
with open('models/label_encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)

with open('models/feature_selector.pkl', 'wb') as f:
    pickle.dump(selector, f)

with open('models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Model bilgilerini loglama
model_info = {
    'Base Model Accuracy': cv_scores.mean(),
    'Optimized Model Accuracy': accuracy,
    'Final Model Accuracy': final_accuracy,
    'Best Parameters': random_search.best_params_,
    'Selected Features': selected_features,
    'Training Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

with open('models/model_info.txt', 'w') as f:
    for key, value in model_info.items():
        f.write(f"{key}: {value}\n")

print("\nTüm modeller ve ilgili bileşenler başarıyla kaydedildi.")