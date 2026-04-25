import matplotlib.pyplot as plt

class Napaka_tipa(Exception):
    def __init__(self, niz):
        super().__init__(self,niz)


class Nuk_t:
    def __init__(self, serija, leta, st_testov, skupna_energija):
        self.serija = serija #ime serije
        
        if not isinstance(leta, tuple) or len(leta) != 2 or any(not isinstance(x, int) for x in leta):
            raise Napaka_tipa('leta morajo biti par 2 števil oblike (od, do)')
        self.leta = leta # leta/leta med katerimi je potekala posamezna serija testov
        
        if not isinstance(st_testov, int):
            raise Napaka_tipa('St testov mora biti celo število')
        self.st_testov = st_testov 
        
        if not isinstance(skupna_energija, int) and not isinstance(skupna_energija, float):
            raise Napaka_tipa('St testov mora biti število')
        
        self.povprecna = round(skupna_energija / st_testov, 2) if st_testov != 0 else 0 #povpr. sproscena energija v kt -> tipa float ali int
        
        self.skupna_energija = skupna_energija #koliko energije v kilotonah se je sprostilo pri eksplozijah


    #get metode
    def get_serija(self):
        return self.serija
    
    def get_leta(self):
        return self.leta
    
    def get_st_testov(self):
        return self.st_testov
    
    def get_povprecna(self):
        return self.povprecna
    
    def get_skupna_energija(self):
        return self.skupna_energija

    #magicne metode
    def __repr__(self):
        return f'Serija: {self.serija}, leta: {self.leta}, st. testov: {self.st_testov}, povprecje: {self.povprecna}, skupno: {self.skupna_energija}'
   
#dedovano 
class Neimenovan(Nuk_t):
    def __init__(self, leta, st_testov, skupna_energija):
        super().__init__('Neimenovan', leta, st_testov, skupna_energija)

class Drzava:
    def __init__(self, ime, n_testi = [], zaloga=0):
        self.ime = ime #ime drzave
        
        if not isinstance(n_testi, list):
            raise Napaka_tipa('Nuklearni testi morajo biti podani v seznamu')
        elif any([not isinstance(test, Nuk_t) for test in n_testi]):
            raise Napaka_tipa('Seznam nuklearnih testov mora vsebovati izključno nuklearne teste')
        self.n_testi = n_testi #vsi nuklearni testi, ki jih je izvedla drzava
        
        self.st_testov = len(n_testi)#stevilo serij n_testov
        self.skupno_st_n_testov = sum(n_test.st_testov for n_test in n_testi) #skupno stevilo testov, čez vse serije, ki jih je izvedla država
        
        if not isinstance(zaloga, int):
            raise Napaka_tipa('Zaloga mora biti tipa int')
        elif zaloga < 0:
            raise Napaka_tipa('Zaloga ne more biti negativna')
        self.zaloga = zaloga #zaloga je iz leta 2020
        
        self.skupna_energija = sum([n_test.get_skupna_energija() for n_test in n_testi])

    #get metode
    def get_ime(self):
        return self.ime
    
    def get_n_testi(self):
        return self.n_testi
    
    def get_st_testov(self):
        return self.st_testov
    
    def get_skupno_st_n_testov(self):
        return self.skupno_st_n_testov
    
    def get_skupna_energija(self):
        return self.skupna_energija
    
    def get_zaloga(self):
        return self.zaloga
    
    def get_najstevilcnejsa(self):
        return max(self.n_testi, key = lambda x: x.st_testov) if self.n_testi else None
    
    def get_najbolj_unicujoca(self):
        return max(self.n_testi, key = lambda x: x.skupna_energija) if self.n_testi else None
    
    
    def get_izbrana_serija(self,izbrana):
        """Vrne seznam vseh serij z izbranim imenom, ki jih
        je ta država izvedla (pričakujemo enega, ampak mozno tudi vec)"""
        izbrani_testi = list()
        for test in self.n_testi:
            if test.get_serija() == izbrana:
                izbrani_testi.append(test)
        return izbrani_testi
    
    #Izris
    def narisi_serije_po_skupni_energiji(self):
        """Narise graf skupnih energij, pri čemer posebej označi top 5"""
        Y = [x.get_skupna_energija() for x in self.get_n_testi()]
        labeli_za_X = [f'{x.get_serija()}\n({x.get_leta()[0]}-{x.get_leta()[1]})' for x in self.get_n_testi()]
        
        top_5 = sorted(list(enumerate(Y)), key = lambda x: x[1])[-5:]
        top_5_i = [x[0] for x in top_5]
        top_5_y = [x[1] for x in top_5]
        izbrani_X = [labeli_za_X[i] for i in top_5_i]
        
        fig = plt.figure(figsize = (10, 6))
        plt.plot(list(range(len(Y))),Y, color = "#1fb487", linewidth = 1.5)
        plt.scatter(top_5_i, top_5_y, color= 'red', zorder = 100, s=20) #pikice na ta vecjih 5-ih
        
        plt.yscale('log')
        plt.xticks(top_5_i, izbrani_X, fontsize = 8, rotation = 45, ha = 'right')
        plt.title(f'Serije po skupni energiji ({self.get_ime()})')
        plt.grid(True, which="both", linestyle="--", alpha=0.3)

        plt.tight_layout()
        plt.show()
        plt.close()
        return


    
    def narisi_serije_po_povprecni_energiji(self):
        """Narise graf povprecni energij, pri čemer posebej označi top 5"""
        Y = [x.get_povprecna() for x in self.get_n_testi()]
        labeli_za_X = [f'{x.get_serija()}\n({x.get_leta()[0]}-{x.get_leta()[1]})' for x in self.get_n_testi()]
        
        top_5 = sorted(list(enumerate(Y)), key = lambda x: x[1])[-5:]
        top_5_i = [x[0] for x in top_5]
        top_5_y = [x[1] for x in top_5]
        izbrani_X = [labeli_za_X[i] for i in top_5_i]
        
        fig = plt.figure(figsize = (10, 6))
        plt.plot(list(range(len(Y))), Y, color = "#1fb487", linewidth = 1.5)
        plt.scatter(top_5_i, top_5_y, color= 'red', zorder = 100, s=20) #pikice na ta vecjih 5-ih
        
        plt.yscale('log')
        plt.xticks(top_5_i, izbrani_X, fontsize = 8, rotation = 45, ha = 'right')
        plt.title(f'Serije po povprecni energiji ({self.get_ime()})')
        plt.grid(True, which="both", linestyle="--", alpha=0.3)

        plt.tight_layout()
        plt.show()
        plt.close()
        return


    #metode na objektih
    def spremeni_zalogo(self, kolicina):
        """Nastavi zalogo jedrskih orozij na izbrano kolicino in vrne novo nastavljeno vrednost zaloge"""
        if not isinstance(kolicina, int):
            raise Napaka_tipa('Zaloga jedrskih orožij mora biti tipa int')
        self.zaloga = kolicina
        return self.zaloga
    
    def dodaj_nuk_test(self, nuk_t):
        """Doda nuk_t državi"""
        if not isinstance(nuk_t, Nuk_t):
            raise Napaka_tipa('nuklearni test, mora biti tipa nuklearni test')
        self.n_testi.append(nuk_t)
        self.st_testov += 1
        self.skupno_st_n_testov = nuk_t.get_st_testov()
        self.skupna_energija += nuk_t.get_skupna_energija()
    
    def dodaj_vec_nuk_testov(self, nuk_testi):
        """Doda vec nuk_t državi"""
        if not isinstance(nuk_testi, list) or any(not isinstance(nuk_t, Nuk_t) for nuk_t in nuk_testi):
            raise Napaka_tipa('nuklearni test, mora biti tipa nuklearni test')
        self.n_testi.extend(nuk_testi)
        self.st_testov += len(nuk_testi)
        self.skupno_st_n_testov += sum([n_test.st_testov for n_test in nuk_testi]) 
        self.skupna_energija += sum([n_test.get_skupna_energija() for n_test in nuk_testi])

    def nastavi_nuk_teste(self, nuk_testi):
        """Zamenja trenutne nuklearne teste z novimi"""
        if not isinstance(nuk_testi, list) or any(not isinstance(nuk_t, Nuk_t) for nuk_t in nuk_testi):
            raise Napaka_tipa('nuklearni test, mora biti tipa nuklearni test')
        self.n_testi = nuk_testi
        self.st_testov = len(nuk_testi)
        self.skupno_st_n_testov = sum(n_test.st_testov for n_test in nuk_testi) #skupno stevilo testov, čez vse serije, ki jih je izvedla država
        self.skupna_energija = sum([n_test.get_skupna_energija() for n_test in nuk_testi])

    #Magične metode
    def __str__(self):
        return f'{self.get_ime()} je imela v letu 2020 na zalogi {self.get_zaloga()} kosov nuklearnega orozja.Do danes je država zabeležila že {self.get_skupno_st_n_testov()} posameznih nuklearnih testov,\
ki jih je izvedla v sklopu {self.get_st_testov()} serij. Vsi testi skupaj so sprostili {self.get_skupna_energija()}kt energije. Najbolj uničujoč test je potekalo pod imenom {(self.get_najbolj_unicujoca()).get_serija()}, potekal je od leta {(self.get_najbolj_unicujoca()).get_leta()[0]} do \
leta {(self.get_najbolj_unicujoca()).get_leta()[1]}, pri čemer se je sprostilo {(self.get_najbolj_unicujoca()).get_skupna_energija()}kt energije, s povprečno vrednostjo {self.get_najbolj_unicujoca().get_povprecna()}kt na posamezni test v seriji.' if self.get_najbolj_unicujoca() else f'{self.get_ime()} je imela v letu 2020 na zalogi {self.get_zaloga()} kosov nuklearnega orozja. V naši bazi ni uradnih podatkov o njihovih testiranjih, kar pa ne pomeni, da se le ti niso zgodili.'

    def __repr__(self):
        return f'Ime:\n{self.ime},\n,Najstevilcnejsi test:\n{self.get_najstevilcnejsa()},\nskupno st testov:\n{self.skupno_st_n_testov},\nZaloga: {self.zaloga},\n Skupna energija: {self.skupna_energija}kT'
    
    @staticmethod
    def poisci_drzavo(drzave, ime):
        """Iz seznama drzav izbere tisto, ki ustreza našemu imenu 
        (če nobena vrne none + predpostavlja, da se vsaka država pojavi zgolj 1x)"""
        drzava_l = [x for x in drzave if x.get_ime() == ime]
        if drzava_l:
            return drzava_l[0]
        return None
    

