# Akbank-Python-ile-Yapay-Zekaya-Giri-Bootcamp-Proje
# Metro Ağı Rota Planlayıcı 🚇

Bu proje, bir metro ağı için en hızlı ve en az aktarma yapan rotayı bulan bir algoritma içermektedir. Kullanıcılar, istasyonlar arasındaki en kısa sürede gidilebilecek yolu veya en az aktarma gerektiren rotayı bulabilirler.

##  Kullanılan Teknolojiler ve Kütüphaneler

- `collections`: `deque` veri yapısı, genişlik öncelikli arama (BFS) algoritması için kuyruk yapısında kullanıldı.
- `heapq`: Öncelikli kuyruk yönetimi için kullanıldı, A* algoritmasında en düşük maliyetli rotayı seçmek için kullanıldı.
- `typing`: Daha iyi kod okunabilirliği ve tip güvenliği için kullanıldı.

##  Algoritmaların Çalışma Mantığı

### **BFS (Breadth-First Search - Genişlik Öncelikli Arama)**
BFS algoritması, en az aktarma yapan rotayı bulmak için kullanılır. Algoritmanın mantığı:
1. Başlangıç istasyonu kuyruğa eklenir.
2. Ziyaret edilen istasyonlar takip edilir.
3. Komşu istasyonlar keşfedilerek en kısa yoldaki istasyonlar eklenir.
4. Hedef istasyona ulaşıldığında rota döndürülür.

 **Neden BFS?**  
BFS, ağı bir ağaç gibi gezerek **en kısa adım sayısını** bulmamızı sağlar. Metro ağında **en az aktarma yapılan rotayı** bulmak için uygundur.

---

### **A* (A-Star) Algoritması**
A* algoritması, en hızlı rotayı bulmak için kullanılır. Çalışma prensibi:
1. Öncelikli kuyruk (heapq) kullanarak en düşük maliyetli yolu belirler.
2. Her istasyonun toplam yol süresini takip eder.
3. **Heuristik fonksiyonu** (hat değişimini minimize eden bir tahmin) ile en iyi yol tahmini yapılır.
4. En düşük maliyetli istasyon seçilerek hedefe en hızlı şekilde ulaşılır.

 **Neden A*?**  
A* algoritması, **en hızlı rotayı** bulmada Dijkstra’dan daha verimli olabilir çünkü heuristik fonksiyon ile gereksiz yolları eler.

---

##  Örnek Kullanım ve Test Sonuçları

```python
metro = MetroAgi()
metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
metro.baglanti_ekle("K1", "M1", 5)

rota, sure = metro.en_hizli_rota_bul("K1", "M1")
print(f"En hızlı rota ({sure} dk):", " -> ".join(str(ist) for ist in rota))
```

 **Ornek Çıktı:**
```
En hızlı rota (5 dk): Kızılay (Kırmızı Hat) -> AŞTİ (Mavi Hat)
```

##  Projeyi Geliştirme Fikirleri

- Daha gelişmiş heuristik kullanımı (örneğin, istasyonların coğrafi koordinatlarını kullanarak gerçek mesafeyi tahmin etme).
- İstasyonlar arası yoğunluk bilgisi ekleme.
- Kullanıcıdan doğrudan istasyon ve hedef girişi alan bir **arayüz** ekleme.

---

