# Powerlytics Enerji İzleme Sistemi
![FireShot Capture 002 - OptiPower Enerji İzleme Sistemi -  localhost](https://github.com/user-attachments/assets/0818091e-0cdd-4dfc-9827-ffbb6fe8df90)


# Powerlytics

Powerlytics, firmaların enerji kullanımını takip edebileceği ve analiz edebileceği bir web uygulamasıdır. Proje, şirketlerin enerji tüketimini optimize etmelerine, verimliliklerini artırmalarına ve karbon ayak izlerini azaltmalarına yardımcı olmayı amaçlamaktadır.

---

## 🚀 Proje Hakkında
Powerlytics, enerji tüketim verilerini analiz eden ve işletmelere enerji yönetimi konusunda içgörüler sunan bir sistemdir. Bu projede:

- **Vue.js** ile modern, kullanıcı dostu ve dinamik bir arayüz oluşturuldu.
- **Flask API** kullanılarak enerji verilerinin işlendiği ve saklandığı bir backend geliştirildi.
- **XGBoost** ve **Scikit-learn** kullanılarak enerji verimliliği tahmin eden bir makine öğrenmesi modeli oluşturuldu.
- **Label Encoding** yöntemi kullanılarak veriler analiz edilip işleme alındı.

## 🚀 Özellikler
- **Enerji Yönetimi Gösterge Paneli:** Günlük enerji tüketimi, maliyet, karbon ayak izi ve verimlilik gibi temel metriklerin anlık görüntülenmesi.
- **Makine Bazlı Takip:** Çekilen enerji, kullanılan enerji, puant durumu ve ISO 50001 verimlilik analizi.
- **Akıllı Enerji Öneri Sistemi:** Makine öğrenmesi ile enerji tüketimini analiz eden ve tasarruf sağlayan öneriler sunma.
- **Tarihsel ve Saatlik Analiz:** Geçmiş ve güncel verilerin karşılaştırılması.
- **Saat Dilimi Maliyet Analizi:** Belirli saat aralıklarında oluşan enerji maliyetlerini detaylı şekilde gösterme.
- **Verimlilik Takibi ve Uyarılar:** Verimlilik seviyesinin düşmesi veya anormal enerji tüketimi durumlarında otomatik uyarılar.
- **Dinamik Grafikler ve Görselleştirme:** Anlık verileri ve geçmiş tüketimi kıyaslamak için gelişmiş grafik bileşenleri.

---

## 🚀 Teknolojiler

### **Frontend:**
- **Vue.js** (Reactif ve hızlı kullanıcı arayüzü)
- **Vue Router** (Sayfa yönlendirmeleri)
- **CSS (Tailwind benzeri modern stiller)** (Görsel düzenleme)

### Backend:
- **Flask** (Python tabanlı API)
- **Pandas** (Veri işleme ve analitik)
- **XGBoost** (Makine öğrenmesi tabanlı enerji analizi)
- **Scikit-learn** (Veri ön işleme ve modelleme)
- **Pickle** (Model saklama ve yükleme)

---

## 📂 Proje Yapısı
```
Powerlytics/
│── src/
│   ├── flask_api/
│   │   ├── app.py                # Flask API servisi
│   │   ├── train_model.py        # Model eğitimi ve kaydetme
│   │   ├── api.py                # API için gerekli endpointler
│   │   ├── model.py              # Makine öğrenmesi modeli
│   │   ├── requirements.txt      # Gerekli bağımlılıklar
│   │── templates/
│   │── static/
│
│── src/components/
│   ├── Dashboard.vue             # Ana gösterge paneli
│   ├── Analysis.vue              # Detaylı analiz ekranı
│   ├── Reports.vue               # Raporlar
│   ├── Settings.vue              # Kullanıcı ayarları
│   ├── EnergyChart.vue           # Enerji tüketim grafiği bileşeni
│   ├── CircularProgress.vue      # Yüzdelik grafik bileşeni
│   ├── BarChart.vue              # Bar grafikleri
│
│── models/
│   ├── enerji_veri_seti.csv      # Örnek enerji verisi
│   ├── xgboost_model.pkl         # Eğitilmiş XGBoost modeli
│   ├── label_encoders.pkl        # Kategorik verileri işlemek için label encoder
│
│── README.md                     # Proje açıklama dosyası
```

---

## 🔧 Kurulum ve Çalıştırma

### 1️⃣ Bağımlılıkları Yükleme
Projeyi çalıştırabilmek için bağımlılıkları yükleyin.

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
Eğer eğitimli bir model yoksa, aşağıdaki komutu çalıştırarak yeni bir model oluşturabilirsiniz:
```bash
python train_model.py
```
Bu işlem tamamlandığında `models/` klasörüne yeni model ve ilgili etiket kodlayıcılar kaydedilecektir.

### 3️⃣ API'yi Başlatma
```bash
python api.py
```
Flask API, varsayılan olarak `http://127.0.0.1:3000` adresinde çalışır.

### 4️⃣ Frontend Uygulamasını Başlatma
```bash
npm run dev
```
Bu komut ile Vue.js tabanlı ön yüz çalıştırılır.

---

## 📊 Model Eğitimi Detayları
Eğitimde kullanılan **enerji_veri_seti.csv**, aşağıdaki bilgileri içermektedir:

| Özellik | Açıklama |
|---------|---------|
| **Firma Adı** | Enerji tüketimini takip eden firma |
| **Makine Türü** | Kullanılan makine tipi |
| **Çekilen Enerji (kWh)** | Toplam çekilen enerji miktarı |
| **Kullanılan Enerji (kWh)** | Gerçek tüketilen enerji miktarı |
| **Saat Aralığı** | Gün içinde belirlenen saat dilimi |
| **Öneri** | Makine için enerji verimliliğini artırma önerisi |

XGBoost kullanılarak eğitilen model, optimum enerji tüketimi için tahminlerde bulunur ve öneriler sunar. Model, `n_estimators=200`, `learning_rate=0.1`, `max_depth=6` gibi parametreler ile optimize edilmiştir.

---

## 📌 API Endpointleri
Flask API, dış uygulamalar ile entegrasyonu sağlamak için aşağıdaki endpointleri sunar:

| Endpoint | Açıklama |
|----------|---------|
| `POST /predict` | Verilen enerji verileriyle tahmin yapar |
| `GET /status` | API'nin çalışır durumda olup olmadığını kontrol eder |

Örnek kullanım:
```bash
curl -X POST "http://127.0.0.1:3000/predict" -H "Content-Type: application/json" -d '{"Firma Adı": "Firma A", "Makine Türü": "Tür A", "Çekilen Enerji": 50, "Kullanılan Enerji": 45, "Çalışma Durumu": "Normal"}'
```

Yanıt:
```json
{"Öneri": "Makineyi kapat, enerji tasarrufu sağla"}
```

---

## 📌 Gelecek Geliştirmeler
- **Gerçek zamanlı enerji izleme:** Canlı veri akışı ve anlık analiz özellikleri eklenecek.
- **Daha gelişmiş tahmin modelleri:** Makine öğrenmesi modelleri daha büyük veri setleriyle eğitilecek.
- **Özelleştirilebilir raporlama:** Kullanıcıların kendi ihtiyaçlarına göre özel raporlar oluşturmasına olanak sağlanacak.
- **Mobil uyum:** Mobil cihazlardan erişimi kolaylaştıracak bir arayüz geliştirilecek.

Geri bildirimlerinizi paylaşabilirsiniz! 🚀


---
Arayüzün tam fonksiyonlu çalışır hali için qr kodu tarayın!!!!
![image](https://github.com/user-attachments/assets/132a325b-c706-4c08-87b8-f6eb0d37f8ff)



