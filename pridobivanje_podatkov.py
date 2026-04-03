import re
import requests
from razredi import Nuk_t


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


def izlusci_posamezne_vrstice(tekst_tabela):
    """Tabelo vnosov za države razdeli na vrstice
    vrstica: [ime_serije, leta (par, z zacetnim in koncnim letom), stevilo_testov, rang energije, skupna sproščena energija(v kilotonah)]
    """
    serije = re.split('<tr>',tekst_tabela)[2:] #vrze vn tisto z naslovi pa eno spredaj, ki ne vem od kod pride
    serije = list(map(lambda tr: re.findall(r'<th>(.+?)</t[hd]>', tr) + re.findall(r'<td class="text-right">(.+?)</t[db]', tr), serije))
    return serije [:-1]

def ustvari_objekte(tabela_vrstic):
    """Dano seznam vrstic nuklearnih testov oblike:
    vrstica: [ime_serije, leto, stevilo_testov, rang energije, skupna sproščena energija(v kilotonah)]
    pretvori v seznam objektov tipa Nuk_t
    """
    nuk_testi = list()
    
    for tr in tabela_vrstic:
        print(tr)
        serija, leta, st_testov, rang_energije, skupna_energija = tr
        if '-' in leta:
            zac, kon = leta.split('-')
            leta = (int(zac), int(zac[:2] +kon))
        elif '–' in leta:
            zac, kon = leta.split('–')
            leta = (int(zac), int(zac[:2] + kon))
        else:
            leta = (int(leta), int(leta))
        st_testov = int(st_testov)
        skupna_energija = int(skupna_energija.replace(',',''))
        nuk_testi.append(Nuk_t(serija, leta, st_testov, skupna_energija))
    return nuk_testi






url = 'https://www.atomicarchive.com/almanac/test-sites/us-testing.html'
    
print(ustvari_objekte(izlusci_posamezne_vrstice(preberi(url))))