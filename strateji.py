import tkinter as tk
from tkinter import messagebox


class Oyuncu:
    def __init__(self, isim, sembol):
        self.isim = isim
        self.sembol = sembol
        self.tas_sayisi = 0
        self.skor = 0


class OyunTahtasi:
    def __init__(self):
        self.hucreler = [""] * 9

    def sifirla(self):
        self.hucreler = [""] * 9

    def bos_mu(self, konum):
        return self.hucreler[konum] == ""

    def tas_koy(self, konum, sembol):
        if self.bos_mu(konum):
            self.hucreler[konum] = sembol
            return True

        return False

    def tas_tasi(self, eski, yeni, sembol):
        if self.hucreler[eski] != sembol:
            return False

        if not self.bos_mu(yeni):
            return False

        self.hucreler[eski] = ""
        self.hucreler[yeni] = sembol

        return True

    def kazanan_var_mi(self, sembol):
        kazanma_durumlari = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        for durum in kazanma_durumlari:
            if all(
                self.hucreler[i] == sembol
                for i in durum
            ):
                return True

        return False


class UcluStrateji:
    def __init__(self, pencere):
        self.pencere = pencere

        self.pencere.title("Üçlü Strateji")
        self.pencere.geometry("520x680")
        self.pencere.resizable(False, False)

        self.tahta = OyunTahtasi()

        self.oyuncu1 = None
        self.oyuncu2 = None

        self.aktif_oyuncu = None
        self.secili_tas = None

        self.butonlar = []

        self.giris_ekrani()


    # -------------------------
    # EKRANI TEMİZLE
    # -------------------------

    def ekrani_temizle(self):
        for widget in self.pencere.winfo_children():
            widget.destroy()


    # -------------------------
    # GİRİŞ EKRANI
    # -------------------------

    def giris_ekrani(self):
        self.ekrani_temizle()

        baslik = tk.Label(
            self.pencere,
            text="ÜÇLÜ STRATEJİ",
            font=("Arial", 24, "bold")
        )
        baslik.pack(pady=30)

        aciklama = tk.Label(
            self.pencere,
            text="İki oyuncunun adını girin.",
            font=("Arial", 12)
        )
        aciklama.pack(pady=10)

        tk.Label(
            self.pencere,
            text="1. Oyuncu",
            font=("Arial", 12, "bold")
        ).pack()

        self.isim1_giris = tk.Entry(
            self.pencere,
            font=("Arial", 13),
            width=25
        )
        self.isim1_giris.pack(pady=10)

        tk.Label(
            self.pencere,
            text="2. Oyuncu",
            font=("Arial", 12, "bold")
        ).pack()

        self.isim2_giris = tk.Entry(
            self.pencere,
            font=("Arial", 13),
            width=25
        )
        self.isim2_giris.pack(pady=10)

        basla_buton = tk.Button(
            self.pencere,
            text="Oyuna Başla",
            font=("Arial", 13, "bold"),
            width=20,
            height=2,
            command=self.oyunu_baslat
        )
        basla_buton.pack(pady=25)

        kurallar = tk.Label(
            self.pencere,
            text=(
                "Kurallar:\n"
                "• Her oyuncunun 3 taşı vardır.\n"
                "• Önce taşlar tahtaya yerleştirilir.\n"
                "• Sonrasında taşlar hareket ettirilir.\n"
                "• Üçlü oluşturan oyuncu kazanır."
            ),
            font=("Arial", 11),
            justify="left"
        )
        kurallar.pack(pady=10)


    # -------------------------
    # OYUNU BAŞLAT
    # -------------------------

    def oyunu_baslat(self):
        isim1 = self.isim1_giris.get().strip()
        isim2 = self.isim2_giris.get().strip()

        if isim1 == "":
            isim1 = "Oyuncu 1"

        if isim2 == "":
            isim2 = "Oyuncu 2"

        self.oyuncu1 = Oyuncu(isim1, "X")
        self.oyuncu2 = Oyuncu(isim2, "O")

        self.aktif_oyuncu = self.oyuncu1

        self.tahta.sifirla()

        self.oyun_ekrani()


    # -------------------------
    # OYUN EKRANI
    # -------------------------

    def oyun_ekrani(self):
        self.ekrani_temizle()

        baslik = tk.Label(
            self.pencere,
            text="Üçlü Strateji",
            font=("Arial", 22, "bold")
        )
        baslik.pack(pady=15)

        self.skor_label = tk.Label(
            self.pencere,
            font=("Arial", 12, "bold")
        )
        self.skor_label.pack(pady=5)

        self.sira_label = tk.Label(
            self.pencere,
            font=("Arial", 13)
        )
        self.sira_label.pack(pady=5)

        self.asama_label = tk.Label(
            self.pencere,
            font=("Arial", 11)
        )
        self.asama_label.pack(pady=5)

        tahta_frame = tk.Frame(self.pencere)
        tahta_frame.pack(pady=20)

        self.butonlar = []

        for i in range(9):
            buton = tk.Button(
                tahta_frame,
                text="",
                font=("Arial", 28, "bold"),
                width=4,
                height=2,
                command=lambda i=i: self.hucreye_tikla(i)
            )

            buton.grid(
                row=i // 3,
                column=i % 3,
                padx=5,
                pady=5
            )

            self.butonlar.append(buton)

        self.mesaj_label = tk.Label(
            self.pencere,
            text="",
            font=("Arial", 11)
        )
        self.mesaj_label.pack(pady=10)

        yeni_tur_buton = tk.Button(
            self.pencere,
            text="Yeni Tur",
            width=15,
            command=self.yeni_tur
        )
        yeni_tur_buton.pack(pady=5)

        yeni_oyuncular_buton = tk.Button(
            self.pencere,
            text="Yeni Oyuncular",
            width=15,
            command=self.giris_ekrani
        )
        yeni_oyuncular_buton.pack(pady=5)

        self.ekrani_guncelle()


    # -------------------------
    # HÜCREYE TIKLAMA
    # -------------------------

    def hucreye_tikla(self, konum):
        oyuncu = self.aktif_oyuncu

        # 1. aşama: taş yerleştirme
        if oyuncu.tas_sayisi < 3:

            if not self.tahta.bos_mu(konum):
                self.mesaj_label.config(
                    text="Bu kare dolu."
                )
                return

            self.tahta.tas_koy(
                konum,
                oyuncu.sembol
            )

            oyuncu.tas_sayisi += 1

            if self.tahta.kazanan_var_mi(
                oyuncu.sembol
            ):
                oyuncu.skor += 1

                self.ekrani_guncelle()

                messagebox.showinfo(
                    "Kazanan",
                    f"{oyuncu.isim} kazandı!"
                )

                return

            self.oyuncu_degistir()

        # 2. aşama: taş taşıma
        else:

            if self.secili_tas is None:

                if self.tahta.hucreler[konum] == oyuncu.sembol:

                    self.secili_tas = konum

                    self.mesaj_label.config(
                        text="Taş seçildi. Şimdi boş kare seç."
                    )

                    self.ekrani_guncelle()

                else:
                    self.mesaj_label.config(
                        text="Önce kendi taşını seçmelisin."
                    )

                return

            else:

                if konum == self.secili_tas:

                    self.secili_tas = None

                    self.mesaj_label.config(
                        text="Seçim iptal edildi."
                    )

                    self.ekrani_guncelle()

                    return

                if self.tahta.hucreler[konum] == oyuncu.sembol:

                    self.secili_tas = konum

                    self.mesaj_label.config(
                        text="Yeni taş seçildi."
                    )

                    self.ekrani_guncelle()

                    return

                if not self.tahta.bos_mu(konum):

                    self.mesaj_label.config(
                        text="Bu kare dolu."
                    )

                    return

                self.tahta.tas_tasi(
                    self.secili_tas,
                    konum,
                    oyuncu.sembol
                )

                self.secili_tas = None

                if self.tahta.kazanan_var_mi(
                    oyuncu.sembol
                ):
                    oyuncu.skor += 1

                    self.ekrani_guncelle()

                    messagebox.showinfo(
                        "Kazanan",
                        f"{oyuncu.isim} kazandı!"
                    )

                    return

                self.oyuncu_degistir()

        self.mesaj_label.config(text="")
        self.ekrani_guncelle()


    # -------------------------
    # OYUNCU DEĞİŞTİR
    # -------------------------

    def oyuncu_degistir(self):
        if self.aktif_oyuncu == self.oyuncu1:
            self.aktif_oyuncu = self.oyuncu2
        else:
            self.aktif_oyuncu = self.oyuncu1


    # -------------------------
    # EKRANI GÜNCELLE
    # -------------------------

    def ekrani_guncelle(self):
        self.skor_label.config(
            text=(
                f"{self.oyuncu1.isim}: "
                f"{self.oyuncu1.skor}   |   "
                f"{self.oyuncu2.isim}: "
                f"{self.oyuncu2.skor}"
            )
        )

        self.sira_label.config(
            text=(
                f"Sıra: {self.aktif_oyuncu.isim} "
                f"({self.aktif_oyuncu.sembol})"
            )
        )

        if self.aktif_oyuncu.tas_sayisi < 3:
            self.asama_label.config(
                text="Taş yerleştirme aşaması"
            )
        else:
            self.asama_label.config(
                text="Taş hareket ettirme aşaması"
            )

        for i in range(9):

            sembol = self.tahta.hucreler[i]

            self.butonlar[i].config(
                text=sembol
            )

            if i == self.secili_tas:
                self.butonlar[i].config(
                    relief="sunken"
                )
            else:
                self.butonlar[i].config(
                    relief="raised"
                )


    # -------------------------
    # YENİ TUR
    # -------------------------

    def yeni_tur(self):
        self.tahta.sifirla()

        self.oyuncu1.tas_sayisi = 0
        self.oyuncu2.tas_sayisi = 0

        self.aktif_oyuncu = self.oyuncu1

        self.secili_tas = None

        self.mesaj_label.config(text="")

        self.ekrani_guncelle()


pencere = tk.Tk()

oyun = UcluStrateji(pencere)

pencere.mainloop()
