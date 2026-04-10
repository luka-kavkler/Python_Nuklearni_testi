from app import prikazi_animacijo
from pridobivanje_podatkov import drzave
from razredi import Drzava, Nuk_t

def osnovne_informacije_o_drzavah():
    """vpraša katera država te zanima, jo izpiše in vrne"""
    prevod_vnosov = {'ZDA': 'ZDA','FR' : 'Francija', 'USSR' : 'USSR/RUSIJA', 'KIT' : 'Kitajska', 'IZ' : 'Izrael', 'IN' : 'Indija', 'NK' : 'Severna Koreja', 'P': 'Pakistan'}
    ime = input(f'Katera država te zanima? {prevod_vnosov.items()}:\n').upper()
    izbrana = Drzava.poisci_drzavo(drzave, prevod_vnosov[ime])
    print(izbrana)
    return izbrana

def primerjalni_podatki(drzava1):
    prevod_vnosov = {'ZDA': 'ZDA','FR' : 'Francija', 'USSR' : 'USSR/RUSIJA', 'KIT' : 'Kitajska', 'IZ' : 'Izrael', 'IN' : 'Indija', 'NK' : 'Severna Koreja', 'P': 'Pakistan'}
    ime = input(f'Zapiši katero državo želiš izbrati za primerjavo. {prevod_vnosov.items()}:\n').upper()
    
    if ime not in prevod_vnosov:
        print('Vnos ni bil pravilen; Poskusi ponovno')
        primerjalni_podatki(drzava1)
        return
    prevod_vnosov = {'ZDA': 'ZDA','FR' : 'Francija', 'USSR' : 'USSR/RUSIJA', 'KIT' : 'Kitajska', 'IZ' : 'Izrael', 'IN' : 'Indija', 'NK' : 'Severna Koreja', 'P': 'Pakistan'}
    lastnosti = {'število serij', 'skupno število testov', 'skupna sproščena energija', 'zaloga'}
    drzava2 = Drzava.poisci_drzavo(drzave, prevod_vnosov[ime])
    lastnost = input('Po kateri lastnosti želiš primerjati državi? (število serij, skupno število testov, skupna sproščena energija, zaloga):\n').lower()
    if lastnost not in lastnosti:
        print('!Izbrana lastnost ni v naboru lastnosti!')
        if input('Za ponovni poiskus vnesite 1:') == '1':
            primerjalni_podatki(drzava1)
            return
        else:
            osnovne_informacije_o_drzavah()
    if lastnost == 'število serij':
        lastnost1 = drzava1.get_st_testov()
        lastnost2 = drzava2.get_st_testov()
    elif lastnost == 'skupno število testov':
        lastnost1 = drzava1.get_skupno_st_n_testov()
        lastnost2 = drzava2.get_skupno_st_n_testov()
    elif lastnost == 'skupna sproščena energija':
        lastnost1 = drzava1.get_skupna_energija()
        lastnost2 = drzava2.get_skupna_energija()
    else:
        lastnost1 = drzava1.get_zaloga()
        lastnost2 = drzava2.get_zaloga()
    max_drzava, min_drzava, max_lastnost, min_lastnost = (drzava1, drzava2, lastnost1, lastnost2) if lastnost1 > lastnost2 else (drzava2, drzava1, lastnost2, lastnost1)
    print(f'{lastnost}: {max_drzava.get_ime()}({max_lastnost})>{min_drzava.get_ime()}({min_lastnost}),\npri čemer je razlika med njima:{max_lastnost - min_lastnost}.')
    


while input('Te zanimajo nuklearna testiranja?(Ja/Ne):\n').lower() == 'ja':
    if input('Želiš pogledati animacijo vseh testiranj?(Ja/Ne):\n').lower() == 'ja':
        print('Število vseh testiranj:')
        prikazi_animacijo()
    interesna = osnovne_informacije_o_drzavah()
    while input(f'Bi rad drzavo po imenu {interesna.get_ime()} primerjal z drugimi?(Ja/Ne):\n').lower() == 'ja':
        primerjalni_podatki(interesna)

        



