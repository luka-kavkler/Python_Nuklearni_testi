from app import prikazi_animacijo
from pridobivanje_podatkov import drzave
from razredi import Drzava, Nuk_t

def osnovne_informacije_o_drzavah():
    """vpraša katera država te zanima, jo izpiše in vrne"""
    prevod_vnosov = {'ZDA': 'ZDA','FR' : 'Francija', 'VB' : 'Velika Britanija', 'USSR' : 'USSR/RUSIJA', 'KIT' : 'Kitajska', 'IZ' : 'Izrael', 'IN' : 'Indija', 'NK' : 'Severna Koreja', 'P': 'Pakistan'}
    ime = input(f'Katera država te zanima? {list(prevod_vnosov.items())}:\n').upper()
    izbrana = Drzava.poisci_drzavo(drzave, prevod_vnosov[ime])
    print(izbrana)
    return izbrana

def primerjalni_podatki(drzava1):
    prevod_vnosov = {'ZDA': 'ZDA','FR' : 'Francija', 'VB' : 'Velika Britanija', 'USSR' : 'USSR/RUSIJA', 'KIT' : 'Kitajska', 'IZ' : 'Izrael', 'IN' : 'Indija', 'NK' : 'Severna Koreja', 'P': 'Pakistan'}
    ime = input(f'Zapiši katero državo želiš izbrati za primerjavo. {list(prevod_vnosov.items())}:\n').upper()
    
    if ime not in prevod_vnosov:
        print('Vnos ni bil pravilen; Poskusi ponovno')
        primerjalni_podatki(drzava1)
        return
    prevod_vnosov = {'ZDA': 'ZDA','FR' : 'Francija','VB' : 'Velika Britanija', 'USSR' : 'USSR/RUSIJA', 'KIT' : 'Kitajska', 'IZ' : 'Izrael', 'IN' : 'Indija', 'NK' : 'Severna Koreja', 'P': 'Pakistan'}
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

def risanje_grafov(drzava):
    """Vpraša uporabnika kateri graf želi in ga izriše"""
    if not isinstance(drzava, Drzava):
        raise ValueError
    if drzava.get_ime() not in {'ZDA', 'Velika Britanija', 'Francija', 'USSR/RUSIJA', 'Kitajska'}:
        print('Žal je ta funkcija omogočena zgolj za države: ZDA, Velika Britanija, Francija, USSR/RUSIJA, Kitajska')
        return  
    veljavni = {'povprečna', 'skupna'}
    vnos = input('Te zanima povprečna ali skupna sproščena energija po serijah? (povprečna/skupna):\n').lower()
    if vnos not in veljavni:
        print('Vnos ni veljaven.')
        if input('Želite poskusiti še enkrat?(Ja/Ne)') == 'Ja':
            risanje_grafov(drzava)
        return

    if vnos == 'povprečna':
        drzava.narisi_serije_po_povprecni_energiji()
    elif vnos == 'skupna':
        drzava.narisi_serije_po_skupni_energiji()
    return


while input('Te zanimajo nuklearna testiranja?(Ja/Ne):\n').lower() == 'ja':
    if input('Želiš pogledati zgodovinsko animacijo vseh atomskih testov?(Ja/Ne):\n').lower() == 'ja':
        time = int(input('Koliko časa naj traja animacija? (optimalno med 30-60)'))
        print('Število vseh testiranj:')
        prikazi_animacijo(time)
    interesna = osnovne_informacije_o_drzavah()
    if input('Te zanima grafični prikaz?(Ja/Ne):\n').lower() == 'ja':
        risanje_grafov(interesna)

    while input(f'Bi rad drzavo po imenu {interesna.get_ime()} primerjal z drugimi?(Ja/Ne):\n').lower() == 'ja':
        primerjalni_podatki(interesna)

        



