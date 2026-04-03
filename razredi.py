class Nuk_t:
    def __init__(self, serija, leto, st_testov, skupna_energija):
        self.serija = serija
        self.leto = leto
        self.st_testov = st_testov
        self.povprecna = skupna_energija / st_testov
        self.skupna_energija = skupna_energija

    def __repr__(self):
        return f'Serija: {self.serija},\nleto: {self.leto},\nst. testov: {self.st_testov}\npovprecje: {self.povprecna},\nskupno: {self.skupna_energija}\n'

