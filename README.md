# Powerlytics Enerji İzleme Sistemi
![Ekran görüntüsü 2025-03-06 092652](https://github.com/user-attachments/assets/c708e808-2b5c-44a0-859a-9867d42a7502)


Powerlytics, firmaların enerji kullanımını takip edebileceği ve analiz edebileceği bir web uygulamasıdır. Vue.js tabanlı bir arayüz ile enerji tüketimi, makine verimliliği ve öneriler sunan bir sistem geliştirilmiştir.

---

## 🚀 Proje Hakkında
Powerlytics, firmaların enerji tüketim verilerini kullanarak analiz yapmasını sağlayan bir sistemdir. Proje kapsamında:
- Vue.js ile modern bir kullanıcı arayüzü oluşturuldu.
- Flask API ile enerji verilerinin işlendiği bir backend geliştirildi.
- XGBoost modeli ile makine öğrenmesi kullanılarak enerji verimliliği analiz edildi ve öneriler oluşturuldu.
- Label Encoding yöntemiyle veriler sayısal hale getirildi.
- Öneriler sınıflandırılarak firmalara en uygun aksiyonlar sunuldu.

---

## 📌 Teknolojiler

### Frontend:
- Vue.js
- Vue Router
- Font Awesome
- CSS (Tailwind benzeri modern stiller)

### Backend:
- Flask (Python tabanlı API servisi)
- Pandas (Veri işleme)
- XGBoost (Makine öğrenmesi modeli)
- Scikit-learn (Veri ön işleme ve modelleme)
- Pickle (Model saklama)

---

## 📂 Proje Yapısı
```
Powerlytics/
│── src/
│   │── flask_api/
│   │   ├── enerji_veri_seti.csv   # Örnek enerji verisi
│   │   ├── train_model.py         # Model eğitimi ve kaydetme
│   │   ├── api.py                 # Flask API servisi
│   │── components/
│   │   ├── Dashboard.vue          # Gösterge paneli
│   │   ├── Analysis.vue           # Analiz sayfası
│   │── App.vue                    # Ana bileşen
│   │── main.js                     # Vue.js uygulama başlangıç dosyası
│── models/
│   │── xgboost_energy_model.pkl    # Eğitilmiş model
│   │── label_encoders.pkl          # Label Encoders
│── README.md
```

---

## 🔧 Kurulum ve Çalıştırma

### 1️⃣ Bağımlılıkları Yükleme
Öncelikle, proje dizinine giderek bağımlılıkları yükleyin.

#### Backend için:
```bash
cd src/flask_api
pip install -r requirements.txt
```

#### Frontend için:
```bash
cd src
npm install
```

### 2️⃣ Model Eğitimi
Önceden tanımlanmış bir model bulunuyorsa bu adımı atlayabilirsiniz. Modeli eğitmek için:
```bash
python train_model.py
```
Bu işlem sonucunda `models/` klasörüne eğitilmiş model ve label encoders kaydedilecektir.

### 3️⃣ Flask API Başlatma
Flask API'yi çalıştırmak için:
```bash
python api.py
```
API, varsayılan olarak `http://127.0.0.1:3000` adresinde çalışacaktır.

### 4️⃣ Vue.js Uygulamasını Başlatma
Frontend uygulamasını başlatmak için:
```bash
npm run dev
```

---

## 📊 Model Eğitimi Detayları

Eğitimde kullanılan veri seti `enerji_veri_seti.csv` olup, aşağıdaki özelliklere sahiptir:

| Özellik | Açıklama |
|---------|-------------|
| Firma Adı | Enerji tüketimi yapan firma |
| Makine Türü | Kullanılan makine tipi |
| Çekilen Enerji (kWh) | Toplam çekilen enerji |
| Kullanılan Enerji (kWh) | Gerçekten kullanılan enerji |
| Saat Dilimi | Günün hangi saatinde olduğu |
| Öneri | Enerji tasarrufu için öneri (Makineyi kapat, verimi artır, vb.) |

Model, XGBoost kullanılarak eğitilmiş olup `n_estimators=200`, `learning_rate=0.1`, `max_depth=6` gibi parametrelerle optimize edilmiştir.


---

## 📌 API Endpointleri
Flask API üzerinden aşağıdaki endpointler kullanılabilir:

| Endpoint | Açıklama |
|----------|-------------|
| `/predict` | Verilen giriş verilerine göre öneri döndürür |
| `/train` | Modeli tekrar eğitir |
| `/status` | API durumunu kontrol eder |

Örnek kullanım:
```bash
curl -X POST "http://127.0.0.1:3000/predict" -H "Content-Type: application/json" -d '{"Firma Adı": "Firma A", "Makine Türü": "Tür A", "Çekilen Enerji": 50, "Kullanılan Enerji": 45, "Çalışma Durumu": 1, "Saat Dilimi": 600}'
```

Yanıt:
```json
{"öneri": "Makineyi daha verimli kullan"}
```

---

## 🛠 Gelecek Geliştirmeler
- Daha fazla veri ile modelin iyileştirilmesi
- Daha gelişmiş görselleştirme özellikleri
- Gerçek zamanlı veri işleme ve canlı tahminler
- Kullanıcı bazlı firma yönetimi

---
Arayüzün tam fonksiyonlu çalışır hali için qr kodu tarayın!!!!
![image](https://github.com/user-attachments/assets/132a325b-c706-4c08-87b8-f6eb0d37f8ff)


## 📢 Katkıda Bulunma
Proje açık kaynak olup katkıda bulunabilirsiniz. Forklayın, geliştirin ve PR açın!

