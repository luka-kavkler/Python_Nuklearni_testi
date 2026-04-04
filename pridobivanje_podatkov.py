import re
import requests
from razredi import Nuk_t, Neimenovan, Drzava


def preberi(url, tag_tabele = '<table class="table table-striped table-sm">'):
    """Vrne tekst prve tabele tabele izbranega htmlja"""
    req = requests.get(url)
    req.encoding = 'UTF-8'
    tekst = req.text
    tekst = tekst.split(tag_tabele)[1]
    tekst = tekst.split('</table>')[0]
    tekst = tekst.replace('\t','')
    tekst = tekst.replace('\n', '')
    return tekst


def izlusci_am(tekst_tabela):
    """Tabelo vnosov za države razdeli na vrstice, prilagojeno na spletno stran amerike
    vrstica: [ime_serije, leta (par, z zacetnim in koncnim letom), stevilo_testov, rang energije, skupna sproščena energija(v kilotonah)]
    """
    serije = re.split('<tr>',tekst_tabela)[2:] #vrze vn tisto z naslovi pa eno spredaj, ki ne vem od kod pride
    serije = list(map(lambda tr: re.findall(r'<th>(.+?)</t[hd]>', tr) + re.findall(r'<td class="text-right">(.+?)</t[db]', tr), serije))
    return serije[:-1]



def izlusci_fr_kt_ru(tekst_tabela):
    """Prilagojen regex za spletno stran s francoskimi, ruskimi ali kitrajskimi testi"""
    serije = re.split('<tr>',tekst_tabela)[2:] #vrze vn tisto z naslovi pa eno spredaj, ki ne vem od kod pride
    serije = list(map(lambda tr: re.findall(r'<th>(.+?)</t[hd]>', tr) + re.findall(r'<td>(.+?)</t[db]', tr) + re.findall(r'<td class="text-right">(.+?)</t[db]', tr), serije))
    return serije[:-1]


def izlusci_brit(tekst_tabela):
    """Prilagojen regex za spletno stran z britanskimi testi"""
    serije = re.split('<tr>',tekst_tabela)[2:] #vrze vn tisto z naslovi pa eno spredaj, ki ne vem od kod pride
    serije = list(map(lambda tr: re.findall(r'<th>(.+?)</th>', tr) + re.findall(r'<td>(.+?)</td', tr) + re.findall(r'<td class="text-right">(.+?)</t[db]', tr), serije)) 
    for i, tr in enumerate(serije):
        if len(tr) == 6:
            serije[i] = tr[:2] + tr[3:] #režem notes pri vsaki vrstici, kjer se pojavi
    return serije[:-1]

def izlusci_zaloge(tekst_tabela):
    """Prilagojen regex za spletno stran z zalogami nuklearnih orožij,
    izluščil bom samo zalogo iz leta 2020
    vrne pare (drzava, zaloga)
    """
    zaloge = re.split('<tr>',tekst_tabela)[2:-1] #vrze vn tisto z naslovi pa eno spredaj, ki ne vem od kod pride + zadnjo z vsotami
    zaloge = list(map(lambda tr: [re.search(r'<th>(.+?)</th>', tr).group(1), re.findall(r'<td class="text-right">(.+?)</t[db]', tr)[-1]], zaloge))
    return zaloge

def pretvori_zaloge_v_slovar(zaloge, imena_drzav):
    """rezultat funkcije izlusci_zaloge pretvori v slovar
    imena drzav so slovar, ki bo imena drzav iz zaloge prevedel v slovenscino
    """
    slovar_zalog = dict()
    for drzava, zaloga in zaloge:
        slovar_zalog[imena_drzav[drzava]] = int(zaloga.replace(',',''))
    return slovar_zalog


def ustvari_objekte(tabela_vrstic):
    """Dano seznam vrstic nuklearnih testov oblike:
    vrstica: [ime_serije, leto, stevilo_testov, rang energije, skupna sproščena energija(v kilotonah)]
    pretvori v seznam objektov tipa Nuk_t
    """
    nuk_testi = list()
    for tr in tabela_vrstic:
        tr = list(map(lambda td: re.sub(r"<.*?>", "", td), tr)) #francozi majo italic tage
        tr = [td for td in tr if td != ' ' and td != '']
        if len(tr) != 5: #kitajci nimajo imen serije
            tr = [''] + tr  
        serija, leta, st_testov, rang_energije, skupna_energija = tr
        if '-' in leta:
            zac, kon = leta.split('-')
            leta = (int(zac), int(zac[:2] +kon))
        elif '–' in leta:
            zac, kon = leta.split('–')
            if len(kon) == 2:
                leta = (int(zac), int(zac[:2] + kon))
            else:
                leta = (int(zac), int(kon))
        else:
            leta = (int(leta), int(leta))
        st_testov = int(st_testov)
        skupna_energija = int(skupna_energija.replace(',','')) if '.' not in skupna_energija else int(float(skupna_energija.replace(',','')))
        if serija and serija != '---':
            nuk_testi.append(Nuk_t(serija, leta, st_testov, skupna_energija))
        else:
            nuk_testi.append(Neimenovan(leta, st_testov, skupna_energija))
    return nuk_testi




###Ustvarjanje objektov
url_am = 'https://www.atomicarchive.com/almanac/test-sites/us-testing.html'
url_ki = 'https://www.atomicarchive.com/almanac/test-sites/prc-testing.html'
url_fr = 'https://www.atomicarchive.com/almanac/test-sites/french-testing.html'
url_brit = 'https://www.atomicarchive.com/almanac/test-sites/uk-testing.html'
url_rus = 'https://www.atomicarchive.com/almanac/test-sites/soviet-testing.html'
url_zaloga = 'https://www.atomicarchive.com/almanac/stockpiles.html'


imena_drzav = {'United States' : 'ZDA', 'India' : 'Indija', 'USSR/Russia' : 'USSR/Rusija', 'United&nbsp;Kingdom' : 'Velika Britanija', 'France' : 'Francija', 'China' : 'Kitajska', 'Pakistan' : 'Pakistan', 'North Korea' : 'Severna Koreja', 'Israel' : 'Izrael'}
slovar_zalog = pretvori_zaloge_v_slovar(izlusci_zaloge(preberi(url_zaloga)), imena_drzav)
drzave = list()
for ime_drzave in imena_drzav.values():
    tren_drzava = Drzava(ime_drzave, zaloga = slovar_zalog[ime_drzave] if ime_drzave in slovar_zalog else 0)
    if ime_drzave == 'ZDA':
        tren_drzava.nastavi_nuk_teste(ustvari_objekte(izlusci_am(preberi(url_am))))
    elif ime_drzave == 'USSR/Rusija':
        tren_drzava.nastavi_nuk_teste(ustvari_objekte(izlusci_fr_kt_ru(preberi(url_rus))))
    elif ime_drzave == 'Francija':
        tren_drzava.nastavi_nuk_teste(ustvari_objekte(izlusci_fr_kt_ru(preberi(url_fr))))
    elif ime_drzave == 'Kitajska':
        tren_drzava.nastavi_nuk_teste(ustvari_objekte(izlusci_fr_kt_ru(preberi(url_ki))))
    elif ime_drzave == 'Velika Britanija':
        tren_drzava.nastavi_nuk_teste(ustvari_objekte(izlusci_brit(preberi(url_brit))))
    drzave.append(tren_drzava)
for drzava in drzave:
    print(drzava)

#opomba: Skupne količine energije pridejo malo drugače kot na spletni strani, ampak s kalkulatorjem mi je za Veliko Britanijo prišlo skozi, da imajo pač oni narobe in ne jaz;; so narobe sešteli zgleda

