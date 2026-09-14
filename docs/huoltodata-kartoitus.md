# Huoltodatan kerääminen 50 moottorimallille — kartoitus

**Päivätty:** 2026-09-14
**Tausta:** FB-ryhmässä kysyttiin Volvo Penta MD6:n öljytilavuutta. Kysymys on ostosignaali,
mutta emme voi vastata siihen luotettavasti ilman varmennettua datapohjaa. Tämä dokumentti
kartoittaa mitä sen rakentaminen vaatii.

**Tila:** Vaihe 0 on tehty — tulokset: [`huoltodata-vaihe0-tulos.md`](huoltodata-vaihe0-tulos.md)
ja [`data/huoltodata-vaihe0.csv`](data/huoltodata-vaihe0.csv).

---

## 0. Lähtötilanne — mitä meillä jo on

Kaksi asiaa, jotka pienentävät työtä merkittävästi:

**a) Moottorimalli↔suodatin-mappaus on jo katalogissa.** Osculatin suodatintuotteiden
varianttien nimet sisältävät moottorisovellukset:

| Merkki | Katalogissa olevat sovellusrivit |
|--------|----------------------------------|
| Suzuki | DF8/9.9/15/20, DF40/50/60/70, DF90/100/115, DF140, DF150/200/225 |
| Mercury | EFI 40/60 (myös Honda), EFI 80/90/115, Verado 4-syl, Verado 6-syl, FourStroke 175–400 hv |
| Yamaha / Selva | 5GH-13440-20 (+ Honda 50 hv), N26-13440-00 |
| Yanmar | 2-3GM/3Y, 3JH-4J, 6L + OEM-öljynsuodatinnumerot |
| Volvo Penta | "kaikki mallit MD30 → TAMD103P-A", D4/D6, IPS-vetolaitteet, 10 huoltosarjaa |
| Tohatsu, Honda | yleiset rivit (ei mallierittelyä) |

**b) Öljyt ovat jo valikoimassa.** Bergoline GENERAL OIL -sarja (Osculatin kautta):
TC-W3 (65.081.00/01), Marine Speed 4T 10W-40 (65.082.00), Prestige Diesel 15W-40 (65.085.01),
Hypo Marine 80W-90 (65.087.00) ja Bio (65.086.00), Sintetix Diesel 10W-40 (65.084.01).
Neljä viidestä TOP-5-kategoriasta on siis katettu. Puuttuu 25W-40 ja 10W-30.

---

## 1. Datamalli — mitä yksi rivi sisältää

| Kenttä | Esimerkki | Huom. |
|--------|-----------|-------|
| `valmistaja` | Volvo Penta | |
| `malli` | MD6A | |
| `variantit` | MD6A, MD6B | eri tilavuudet → eri rivit |
| `vuodet` | 1966–1975 | |
| `tyyppi` | diesel-sisämoottori | 4T-perä / 2T-perä / bensa-sisäperä / diesel |
| `oljy_spec` | VDS-4.5 15W-40 (nykysuositus) | **ei** käsikirjan 1960-luvun suositus |
| `oljy_l_suodattimella` | 3,1 | |
| `oljy_l_ilman` | 2,8 | |
| `suodatin_oem` | 834337 | |
| `suodatin_sku` | 17.501.xx | linkitys omaan katalogiin |
| `vaihteisto_malli` | MS / MS2 | määräytyy vaihteistosta, ei koneesta |
| `vaihteisto_oljy` | sama kuin moottorissa | |
| `vaihteisto_l` | 1,1 | |
| `vaihtovali_h` | 100 | |
| `lahde` | Volvo Penta Workshop Manual MD6A, s. 36 | **pakollinen** |
| `varmennettu_pvm` | 2026-09-14 | |
| `varmentaja` | nimi | |

`lahde`-kenttä on se, joka tekee datasta puolustettavan. Ilman sitä kyseessä on arvaus.

---

## 2. Mistä data tulee — neljä tasoa

| Taso | Lähde | Kustannus | Käytetäänkö |
|------|-------|-----------|-------------|
| 1 | **Oma katalogi** — suodatin↔moottori-mappaus | 0 € | **Kyllä**, lähtöpiste |
| 2 | **OEM:n julkiset käyttöohjekirjat** — Volvo Penta (volvopenta.com/your-engine, moottorinumerolla), Yanmar, Yamaha, Mercury, Suzuki, Honda | 0 €, työtä | **Kyllä**, pääasiallinen lähde |
| 3 | **Aftermarket-katalogit** — Sierra Catalog (Dometic Marine), Orbitrade | lisenssimaksu, sopimus | Vain jos taso 2 ei riitä |
| 4 | **Kolmannen osapuolen manuaalikirjastot** (ManualsLib, downloadboatmanuals ym.) | 0 € | **Ei.** Usein luvattomia kopioita — sekä oikeudellinen että laaturiski |

Huviveneiden direktiivi (RCD 2013/53/EU) velvoittaa toimittamaan moottorin mukana
käyttöohjeen huolto-ohjeineen, joten taso 2 on lähtökohtaisesti olemassa ja saatavilla.

---

## 3. Oikeudellinen puoli

**Ei oikeudellista neuvoa — tämä on se, mikä pitää tarkistuttaa juristilla ennen julkaisua.**

- **Yksittäinen luku on fakta.** "MD6A: 2,8 l" ei ole tekijänoikeuden suojaama.
  Tekijänoikeus suojaa käsikirjan tekstin ja taulukon esitystavan, ei lukua.
- **Mutta tietokantaan voi kohdistua sui generis -oikeus.** EU:n tietokantadirektiivi
  96/9/EY suojaa tietokantaa, jonka sisällön hankkimiseen, varmentamiseen tai
  esittämiseen on tehty huomattava investointi — 15 vuotta. Merkittävän osan
  systemaattinen poiminta esim. Sierran katalogista on riski, vaikka yksittäiset
  luvut ovatkin faktoja.
- **Turvallinen linja:** luvut kerätään itse OEM:n julkisista käyttöohjekirjoista,
  lähde kirjataan riville, taulukoita ei kopioida sellaisenaan eikä toisen kokoamaa
  tietokantaa jäljennetä. Näin syntyy **oma** tietokanta, johon meillä on itsellämme
  sui generis -oikeus.

**Huomioitava asymmetria autopuoleen:** ajoneuvoissa EU:n tyyppihyväksyntäsääntely
pakottaa valmistajat luovuttamaan korjaus- ja huoltotiedot, ja siitä syntyi TecDocin
kaltainen markkina. **Venemoottoreille vastaavaa velvoitetta ei ole.** Valmista
"marine-TecDocia" ei siis ole ostettavissa — data on koottava itse. Se on työn syy,
mutta myös sen arvo: kilpailijoilla ei ole sitä myöskään.

---

## 4. Työmäärä

**Per rivi, varmennettuna:**

| Vaihe | Aika |
|-------|------|
| Mallin tunnistus + oikean käsikirjan löytäminen | 10–20 min |
| Lukujen poiminta (öljy, suodatin, vaihteisto, vaihtoväli) | 10 min |
| Ristiinvarmennus toisesta lähteestä | 10 min |
| Kirjaus + lähdeviite | 5 min |
| **Yhteensä** | **~45 min** |

**Kokonaisuus (alkuperäinen arvio):**

| Erä | Tunnit |
|-----|--------|
| Skeeman ja työkalun pystytys | 8–16 |
| 50 mallia × 45 min | 38 |
| Vaikeat tapaukset (vanhat mallit, monta varianttia), +20 % | 8 |
| Venemekaanikon katselmointi | 8 |
| **Yhteensä** | **~62–70 h ≈ 1,5–2 htv-viikkoa** |

Kustannus 60 €/h laskennallisella hinnalla **~4 000 €**; ulkoa ostettu mekaanikon
katselmus +500–800 €. Ylläpito ~4–8 h/vuosi.

> **Vaiheen 0 jälkeen päivitetty:** todellinen rivimäärä on 52, ja niistä 27 on
> tunnistettu vain OEM-numerolla, mikä kaksinkertaistaa rivin työn. Päivitetty
> kokonaisarvio **57–65 h**. Yksityiskohdat: `huoltodata-vaihe0-tulos.md`.

---

## 5. Mitkä 50 mallia — priorisointi kannan mukaan

| Ryhmä | Rivejä | Esimerkit |
|-------|--------|-----------|
| Nelitahtiperämoottorit | ~18 | Yamaha F4–F425, Honda BF2.3–BF250, Suzuki DF2.5–DF350, Mercury FourStroke/Verado, Tohatsu MFS |
| Kaksitahtiperämoottorit | ~6 | Johnson/Evinrude, Yamaha 2T, Mercury 2T, Suzuki DT — moottoriöljyä ei mitata (sekoitussuhde), mutta vaihteistoöljy kyllä |
| Purjeveneiden apumoottorit | ~6 | Volvo Penta MD2020, D1-13/D1-20/D1-30; Yanmar 1GM10/2GM20/3GM30/3YM30 |
| Isommat dieselit | ~5 | Volvo Penta D2-40/D2-55, D3, D4, D6 |
| Bensiinisisäperät | ~5 | Volvo Penta 4.3 V6, 5.0/5.7 V8, 8.1; MerCruiser 4.5/6.2 |

Järjestys kannan koon mukaan, ei aakkosissa. **MD6 on listan häntäpäässä** — 1960-luvun
kone, marginaalinen kanta. Se oli hyvä testikysymys, mutta väärä paikka aloittaa.

---

## 6. Riskit ja niiden hallinta

| Riski | Hallinta |
|-------|----------|
| **Väärä luku → konevaurio** | Kaksi riippumatonta lähdettä per rivi; mekaanikon katselmus ennen julkaisua |
| **Malli tunnistettu väärin** | Palvelu kieltäytyy vastaamasta, kun mallimerkintä on epätäydellinen, ja kysyy tarkennusta. Kieltäytyminen on oikea vastaus, ei puute |
| **Vastuu julkaistusta tiedosta** | Näkyvä varaus ("tarkista aina moottorin oma käsikirja") ei poista vastuuta — tarkistuta ehdot ja vakuutus |
| **Vanhentunut öljysuositus** | Kirjataan nykysuositus, ei käsikirjan alkuperäistä. Esim. vanhat Volvo Penta -dieselit → VDS-4.5 |
| **Lähdeaineiston laillisuus** | Vain OEM:n julkaisemat käyttöohjekirjat; ei skreippausta manuaalikirjastoista |

---

## 7. Vaiheistus

| Vaihe | Sisältö | Työ | Tila |
|-------|---------|-----|------|
| **0** | Poimi katalogin suodatinriveiltä olemassa oleva malli↔suodatin-mappaus taulukoksi | 2–3 h (toteutui ~15 min) | **Tehty** |
| **1** | Perämoottoririvit + Volvo D1-13/D1-20, 18 riviä. Julkaise huoltokortteina tuotesivuille | ~11 h | Seuraava |
| **2** | Tila B: 27 OEM-numerorivin käännös + öljytiedot | ~27 h | Odottaa mittaria |
| **3** | Hakutoiminto kauppaan: moottorimalli → öljy + määrä + suodatin → ostoskoriin | erikseen | |

**Mittari vaiheen 1 jälkeen:** konversio huoltokortilta öljyn ja suodattimen ostoon.
Jos se ei liiku, vaihetta 2 ei kannata tehdä. Vaihe 1 on tarkoituksella riittävän
pieni, että sen voi hylätä.

---

## 8. Mitä ei kannata tehdä

- **Ei skreipata** ManualsLibia, downloadboatmanuals.comia tai Sierran katalogia.
- **Ei anneta kielimallin generoida lukuja muistista.** Tämä on juuri se virhe, joka
  MD6-kokeilussa oli lähellä tapahtua: luku löytyi hakutuloksen katkelmasta, ei
  alkuperäisestä käsikirjasta, eikä sitä olisi saanut julkaista sellaisenaan.
- **Ei aloiteta harvinaisista malleista**, vaikka kysymys tulisi juuri niistä.
