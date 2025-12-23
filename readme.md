1. Giriş
2. 
Bu projenin amacı, flat_prices.json veri setini kullanarak ev fiyatlarını tahmin eden bir Çoklu Doğrusal Regresyon (Multiple Linear Regression) modeli geliştirmektir. Proje; veri temizleme, Geriye Doğru Eleme (Backward Elimination) yöntemiyle istatistiksel özellik seçimi, model değerlendirmesi ve Flask tabanlı bir web arayüzü sunumunu kapsamaktadır.

3. Veri Ön İşleme (Data Preprocessing)
Ham veriyi modele uygun hale getirmek için şu adımlar uygulanmıştır:
	•	Öznitelik Seçimi: Başlangıçta konumu, brüt alanı (carpet area) ve oda sayılarını içeren en fazla 10 öznitelik seçilmiştir.
	•	Eksik Veri Analizi: Veri setindeki eksik değerler kontrol edilmiştir. Ödev gereksinimlerini karşılamak adına manuel olarak eksik veriler eklenmiş ve bu değerler SimpleImputer kullanılarak median (medyan) stratejisiyle doldurulmuştur.
	◦	Neden Medyan? Medyan, uç değerlerden (aykırı verilerden) etkilenmediği için ortalamaya göre daha güvenilir bir doldurma yöntemidir.
	•	Kategorik Veriler: location (konum) gibi sayısal olmayan veriler, One-Hot Encoding yöntemiyle sayısal formatta yeni sütunlara dönüştürülmüştür.
	◦	drop_first=True parametresi kullanılarak "Kukla Değişken Tuzağı" (Dummy Variable Trap) engellenmiştir.

4. Geriye Doğru Eleme (Backward Elimination)
Modelin doğruluğunu artırmak ve gereksiz öznitelikleri temizlemek için bu yöntem uygulanmıştır:
	•	Anlamlılık Düzeyi: p>0.05 olan öznitelikler modelden çıkarılmıştır.
	•	Öznitelik Koruma: carpet_area (metrekare) özniteliği, istatistiksel değeri (p-value) yüksek çıksa bile modelde manuel olarak tutulmuştur.
	◦	Neden? Alan (metrekare), bir evin fiyatını belirleyen en temel fiziksel faktördür. Bu öznitelik çıkarıldığında model ölçeğini kaybetmekte ve mantıksız (negatif) sonuçlar üretmektedir.

5. Model Eğitimi ve Değerlendirme
Veri seti %80 eğitim ve %20 test olacak şekilde bölünmüştür.
	•	Algoritma: Çoklu Doğrusal Regresyon.
	•	Metrikler:
	◦	R2 (R-Kare): Modelin veriyi ne kadar iyi açıkladığını gösterir.
	◦	MAE ve MSE: Tahmin edilen fiyat ile gerçek fiyat arasındaki hata payını ölçer.
	•	Görselleştirme: Gerçek fiyatlar ile tahmin edilen fiyatlar arasındaki ilişkiyi gösteren bir regresyon grafiği oluşturulmuştur. Verilerin kırmızı çizgi etrafında yoğunlaşması yüksek başarıyı kanıtlamaktadır.

6. Flask Arayüzü ve Kullanıcı Deneyimi (GUI)
Eğitilen model model.pkl olarak kaydedilmiş ve Flask kullanılarak bir web arayüzüne entegre edilmiştir.
	•	Negatif Sonuç Koruması: Doğrusal regresyon bir ekstrapolasyon (dış değer tahmin) aracı olduğu için, çok küçük girişler yapıldığında (örneğin tüm odaların 1 seçilmesi) matematiksel olarak negatif sonuçlar üretebilir.
	•	Kullanıcı Dostu Mantık: Kullanıcıya negatif veya hatalı bir fiyat göstermemek adına app.py dosyasına özel bir kontrol eklenmiştir. Fiyat sıfırın altına düştüğünde sistem: "Bu küçük değerler için fiyat tahmini yapılamıyor (Model Sınırı)" uyarısını vermektedir.

7. Sonuç ve Değerlendirme
Bu çalışma, makine öğrenmesi modellerinin sadece koddan ibaret olmadığını, aynı zamanda veri mantığının (alan bilgisinin) korunması gerektiğini göstermiştir.
	1	Metrekarenin Önemi: İstatistiksel olarak elense bile, fiziksel gerçeklik için bazı özniteliklerin korunması gerektiği görülmüştür.
	2	Sınırlamalar: Lineer modellerin eğitim verisi dışındaki çok küçük değerlerde hata payının arttığı gözlemlenmiştir.
