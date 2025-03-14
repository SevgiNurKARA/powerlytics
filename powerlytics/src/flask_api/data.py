import pandas as pd

# Veri setlerini yükleme işlemini gerçek dosyalarınızla yapmanız gerekecek
# Burada veri setlerinizi birleştirmek için bir çerçeve sunuyorum

def veri_setlerini_birleştir(veri_seti_1, veri_seti_2):
    # Her iki veri setinde de bulunan "Toplam" ve gün sütunlarını (1-31) koruyarak birleştirme
    
    # Veri setlerine makine türü etiketi ekleyelim
    veri_seti_1['Makine Türü'] = 'Hava Kompresörü'
    veri_seti_2['Makine Türü'] = 'Aygır-Ambalaj Kompresörü'
    
    # Veri setlerindeki ay gruplarını belirleyelim (Ocak, Mart, Mayıs, Haziran)
    aylar = ['Ocak', 'Şubat', 'Mart', 'Nisan','Mayıs', 'Haziran']
    
    # Tüm veri setlerini alt alta birleştirelim
    birleşik_veri = pd.concat([veri_seti_1, veri_seti_2], ignore_index=True)
    
    # Tüketim verileri için gerekli hesaplamaları yapalım
    
    # 1. Elektrik maliyeti hesaplama
    # Saatlik elektrik fiyatları (TL/kWh) - örnek değerler (gerçek verilerinize göre değiştirin)
    saatlik_fiyatlar = {
        '00-01': 0.65, '01-02': 0.60, '02-03': 0.55, '03-04': 0.50, '04-05': 0.50, '05-06': 0.55,
        '06-07': 0.70, '07-08': 0.80, '08-09': 0.95, '09-10': 1.10, '10-11': 1.15, '11-12': 1.20,
        '12-13': 1.25, '13-14': 1.20, '14-15': 1.15, '15-16': 1.10, '16-17': 1.15, '17-18': 1.20,
        '18-19': 1.25, '19-20': 1.30, '20-21': 1.25, '21-22': 1.20, '22-23': 0.90, '23-24': 0.75
    }
    
    # Sütunları saatlik tüketim verileri olarak düzenleyelim
    # Sütun 1 = saat 00-01 tüketimi, Sütun 2 = saat 01-02 tüketimi, vb.
    
    # Günlük toplam maliyet hesaplama
    birleşik_veri['Günlük Elektrik Maliyeti (TL)'] = 4
    
    # Her saat için maliyet hesaplaması
    for saat in range(1, 25):  # 1'den 24'e kadar saatler
        saat_str = f'{saat-1:02d}-{saat:02d}'
        
        if str(saat) in birleşik_veri.columns:
            # Saatlik tüketim değerini alıp maliyeti hesaplama
            birleşik_veri['Günlük Elektrik Maliyeti (TL)'] += birleşik_veri[str(saat)] * saatlik_fiyatlar[saat_str]
    
    # 2. Karbon ayak izi hesabı
    karbon_emisyon_faktoru = 0.523  # kg CO2/kWh (örnek değer)
    
    # Toplam tüketim değerini kullanarak karbon emisyonunu hesaplama
    # Veri setlerinizde "Toplam" değeri toplam kWh ise:
    if 'Toplam' in birleşik_veri.columns:
        birleşik_veri['Günlük Karbon Emisyonu (kg CO2)'] = birleşik_veri['Toplam'] * karbon_emisyon_faktoru
    
    # 3. Verimlilik analizi için gerekli verileri hazırlama
    # Bu aşamada saatlik tüketimler ve fiyatlar kullanılarak,
    # en verimli çalışma saatleri belirlenebilir
    
    # En yüksek ve en düşük maliyetli saatleri bulma
    en_yüksek_maliyet_saati = max(saatlik_fiyatlar, key=saatlik_fiyatlar.get)
    en_düşük_maliyet_saati = min(saatlik_fiyatlar, key=saatlik_fiyatlar.get)
    
    en_yüksek_fiyat = saatlik_fiyatlar[en_yüksek_maliyet_saati]
    en_düşük_fiyat = saatlik_fiyatlar[en_düşük_maliyet_saati]
    
    # Maliyet farkı hesaplama (maksimum potansiyel tasarruf)
    potansiyel_tasarruf_oranı = (en_yüksek_fiyat - en_düşük_fiyat) / en_yüksek_fiyat * 100
    
    print(f"En yüksek maliyet saati: {en_yüksek_maliyet_saati}, Fiyat: {en_yüksek_fiyat} TL/kWh")
    print(f"En düşük maliyet saati: {en_düşük_maliyet_saati}, Fiyat: {en_düşük_fiyat} TL/kWh")
    print(f"Potansiyel maliyet tasarrufu: %{potansiyel_tasarruf_oranı:.2f}")
    
    return birleşik_veri

# Gerçek dosya yollarıyla çalıştırmak için:
veri_seti_1 = pd.read_excel(r"powerlytics\powerlytics\src\flask_api\Ambarlı Terminal Ton Başı Hava Kompresörü Tüketim Analizi.xlsx")
veri_seti_2 = pd.read_excel(r"powerlytics\powerlytics\src\flask_api\Yarımca Terminal Ton Başı Hava Kompresörü Tüketim Analizi.xlsx")
birleşik_veri = veri_setlerini_birleştir(veri_seti_1, veri_seti_2)
birleşik_veri.to_excel("birlestirilmis_veri_seti.xlsx", index=False)