from collections import defaultdict, deque
import heapq
from typing import Dict, List, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []
    
    def __lt__(self, other: 'Istasyon') -> bool:
        return self.idx < other.idx
    
    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

    def __str__(self):  
        return f"{self.ad} ({self.hat})"  

    def __repr__(self):  
        return self.__str__()  


class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)
    
    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)
    
    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """ BFS algoritması ile en az aktarma yapan rotayı bulur. """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = set()
        
        while kuyruk:
            mevcut, yol = kuyruk.popleft()
            
            if mevcut == hedef:
                return yol
            
            ziyaret_edildi.add(mevcut)
            
            for komsu, _ in mevcut.komsular:
                if komsu not in ziyaret_edildi:
                    kuyruk.append((komsu, yol + [komsu]))
        
        return None

    def heuristik(self, istasyon: Istasyon, hedef: Istasyon) -> int:
        """ Basit heuristik: Hat değişimi sayısını minimize etme. """
        return 1 if istasyon.hat != hedef.hat else 0

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """ A* algoritması ile en hızlı rotayı bulur. """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        pq = [(0 + self.heuristik(baslangic, hedef), 0, baslangic, [baslangic])]
        ziyaret_edildi = {}

        while pq:
            _, sure, mevcut, yol = heapq.heappop(pq)

            if mevcut == hedef:
                return yol, sure
            
            if mevcut in ziyaret_edildi and ziyaret_edildi[mevcut] <= sure:
                continue
            
            ziyaret_edildi[mevcut] = sure

            for komsu, ek_sure in mevcut.komsular:
                yeni_sure = sure + ek_sure
                heapq.heappush(pq, (yeni_sure + self.heuristik(komsu, hedef), yeni_sure, komsu, yol + [komsu]))
        
        return None



if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonları ekleme
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantıları ekleme 
    metro.baglanti_ekle("K1", "K2", 4)
    metro.baglanti_ekle("K2", "K3", 6)
    metro.baglanti_ekle("K3", "K4", 8)
    metro.baglanti_ekle("M1", "M2", 5)
    metro.baglanti_ekle("M2", "M3", 3)
    metro.baglanti_ekle("M3", "M4", 4)
    metro.baglanti_ekle("T1", "T2", 7)
    metro.baglanti_ekle("T2", "T3", 9)
    metro.baglanti_ekle("T3", "T4", 5)
    metro.baglanti_ekle("K1", "M2", 2)
    metro.baglanti_ekle("K3", "T2", 3)
    metro.baglanti_ekle("M4", "T3", 2)

    test_senaryolari = [
        ("K1", "K1", "Aynı istasyondan kendisine gitme testi"),
        ("K1", "K2", "Doğrudan bağlantı olan iki istasyon"),
        ("M1", "T4", "Aktarma gerektiren bir rota"),
        ("K1", "X1", "Ulaşılamaz istasyon kontrolü")
    ]

    for baslangic, hedef, aciklama in test_senaryolari:
        print(f"\nTest: {aciklama}")
        en_hizli_rota = metro.en_hizli_rota_bul(baslangic, hedef)
        if en_hizli_rota:
            rota, sure = en_hizli_rota
            print(f"En hızlı rota ({sure} dk):", " -> ".join(str(ist) for ist in rota))
        else:
            print("En hızlı rota: Ulaşılamaz")