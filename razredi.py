class Nuk_t:
    def __init__(self, serija, leto, st_testov, skupna_energija):
        self.serija = serija #ime serije
        self.leto = leto # leto/leta med katerimi je potekala posamezna serija testov
        self.st_testov = st_testov 
        self.povprecna = skupna_energija / st_testov if st_testov != 0 else 0 #povpr. sproscena energija v kt -> tipa float ali int
        self.skupna_energija = skupna_energija #koliko energije v kilotonah se je sprostilo pri eksplozijah

    def get_serija(self):
        return self.serija
    
    def get_leto(self):
        return self.leto
    
    def get_st_testov(self):
        return self.st_testov
    
    def get_povprecna(self):
        return self.povprecna
    
    def get_skupna(self):
        return self.skupna_energija

    def __repr__(self):
        return f'Serija: {self.serija}, leto: {self.leto}, st. testov: {self.st_testov}, povprecje: {self.povprecna}, skupno: {self.skupna_energija}'

class Neimenovan(Nuk_t):
    def __init__(self, leto, st_testov, skupna_energija):
        super().__init__('Neimenovan', leto, st_testov, skupna_energija)

class Drzava:
    def __init__(self, ime, n_testi = [Neimenovan(0,0,0)]):
        self.ime = ime #ime drzave
        self.n_testi = n_testi #vsi nuklearni testi, ki jih je izvedla drzava
        self.skupno_st_n_testov = sum(n_test.st_testov for n_test in n_testi) #skupno stevilo testov, čez vse serije, ki jih je izvedla država

    def get_ime(self):
        return self.ime
    
    def get_n_testi(self):
        return self.n_testi
    
    def get_skupno_st_n_testov(self):
        return self.skupno_st_n_testov
    
    def get_najstevilcnejsa(self):
        return max(self.n_testi, key = lambda x: x.st_testov)
    
    def get_najbolj_unicujoca(self):
        return max(self.n_testi, key = lambda x: x.skupna_energija)

    def __repr__(self):
        return f'Ime:\n{self.ime},\nNajstevilcnejsi test:\n{self.get_najstevilcnejsa()}\nskupno st testov:\n{self.skupno_st_n_testov}\n' 
