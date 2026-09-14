# Vaihe 0: katalogin malli↔suodatin-mappaus — tulos

**Tehty:** 2026-09-14
**Lähde:** Shopify-katalogi, tuotetyyppi `Filters & Maintenance` (kaikki tuotteet ja variantit)
**Tuotos:** [`docs/data/huoltodata-vaihe0.csv`](data/huoltodata-vaihe0.csv) — 52 huoltoriviä

---

## Mitä saatiin

**52 huoltoriviä** johdettiin suoraan katalogista. Jokaisella on jo suodattimen SKU,
hinta ja ehdotettu öljy-SKU. Puuttuvat kentät (öljyn spesifikaatio, öljytilavuus,
vaihteistoöljy ja -tilavuus, vaihtoväli, lähdeviite) ovat tyhjinä sarakkeina valmiina.

| Tila | Mitä tiedetään | Rivejä | Työ / rivi |
|------|----------------|--------|------------|
| **A** | Moottorimalli tiedossa katalogista | **19** | ~30 min — vain öljytiedot |
| **B** | Vain OEM-suodatinnumero, moottorimalli ei | **27** | ~60 min — vaatii ensin OEM→malli-käännöksen |
| **C** | Ei sovellustietoa lainkaan | **6** | ~45 min — selvitettävä mitä suodatin sovittaa |

| Tyyppi | Rivejä |
|--------|--------|
| 4T-perämoottori | 17 |
| Diesel (sisä- ja purjevene) | 32 |
| Bensiinisisäperä | 3 |

---

## Kolme löydöstä, jotka muuttavat suunnitelmaa

### 1. Kuusi suodatinta myydään ilman sovellustietoa

Nämä variantit ovat kaupassa otsikolla `Default Title` tai pelkkänä SKU-numerona:

| SKU | Tuote | Hinta |
|-----|-------|-------|
| 17.504.03 | YAMAHA / SELVA öljynsuodatin 4T-perämoottoriin | 11,77 € |
| 17.504.10 | TOHATSU öljynsuodatin 4T-perämoottoriin | 15,95 € |
| 17.504.12 | HONDA öljynsuodatin 4T-perämoottoriin | 13,95 € |
| 17.504.01 | SUZUKI öljynsuodatin (otsikkona pelkkä SKU) | 4,74 € |
| 17.504.05 | MERCURY öljynsuodatin (otsikkona pelkkä SKU) | 14,06 € |
| 17.501.33 | YANMAR öljynsuodatin diesel | 28,90 € |

**Asiakas ei voi tietää sopiiko suodatin hänen moottoriinsa, joten hän ei osta sitä.**
Tämä on korjattavissa heti Osculatin tuotekatalogista, riippumatta koko
huoltodataprojektista — ja se on todennäköisesti nopein yksittäinen myyntivaikutus,
joka tästä työstä irtoaa.

### 2. Volvon ja Yanmarin suodattimet on tunnistettu vain OEM-numerolla

27 riviä 52:sta on muotoa "Oil filter VOLVO diesel 3582732". Numero on oikein, mutta
**se ei kerro mihin moottoriin suodatin menee** — ei meille eikä asiakkaalle.
Näillä riveillä työ on kaksinkertainen: ensin OEM-numero → moottorimalli, vasta sitten
öljytilavuus. Tämä oli kartoituksen suurin aliarvio: oletin rivien olevan
mallipohjaisia, ja ne ovatkin numeropohjaisia.

Poikkeus: **17.600.06** on nimetty "D1-13/D1-20" — ainoa Volvo-rivi, jolla malli on
suoraan luettavissa. Loput yhdeksän huoltosarjaa on pelkkiä numeroita.

### 3. Bensiinisisäperille ei ole öljyä lainkaan

Kolme riviä (17.501.02, .03, .06) on Volvo Pentan bensiinikoneiden öljynsuodattimia.
Niille sopivaa **25W-40:tä ei ole valikoimassa** — CSV:ssä lukee `PUUTTUU 25W-40`.
Tämä vahvistaa TOP-5-listan kohdan 5: se on ainoa aidosti puuttuva öljy.

**Lisäksi:** vaihteistoöljyn tilavuutta ei voi johtaa katalogista lainkaan, koska
perämoottorin kulmavaihteelle ei ole suodatinta eikä siten suodatinriviä. Meillä on
80W-90 hyllyssä (65.087.00) mutta ei yhtään moottorikohtaista tilavuutta.
Vaihteistotilavuudet on kerättävä kokonaan erikseen, myös 2T-moottoreille.

---

## Päivitetty työmääräarvio

Kartoituksen arvio oli 38 h 50 rivin keruulle. Todellinen rivijakauma muuttaa sitä:

| Erä | Rivejä | h |
|-----|--------|---|
| Tila A | 19 | 9,5 |
| Tila B (OEM-käännös + öljytiedot) | 27 | 27 |
| Tila C | 6 | 4,5 |
| **Keruu yhteensä** | **52** | **41** |
| Skeema ja työkalu | | 8–16 |
| Mekaanikon katselmointi | | 8 |
| **Yhteensä** | | **57–65 h** |

Osuu kartoituksen haarukkaan (62–70 h), mutta työ jakautuu eri tavalla: puolet menee
OEM-numeroiden kääntämiseen moottorimalleiksi, ei öljytilavuuksien etsimiseen.

Vaihe 0 itsessään oli arvioitu 2–3 tunniksi. Se meni noin 15 minuuttiin, koska
katalogi oli haettavissa ohjelmallisesti eikä käsin.

---

## Suositus vaiheeseen 1

Kartoituksessa ehdotin 12 riviä. Data sanoo, että luontevampi ensimmäinen erä on
**tila A:n ja C:n perämoottoririvit + Volvo D1-13/D1-20 = 18 riviä, noin 11 h.**

Perustelut:
- Kattaa **koko perämoottoripuolen**, joka on 90 % Suomen moottoroidusta venekannasta
- Korjaa samalla ne kuusi tuotesivua, jotka eivät nyt myy lainkaan
- Ei koske yhteenkään OEM-numerorivin käännökseen, eli ei törmää työn kalleimpaan osaan
- Volvo D1-13/D1-20 tulee mukaan ilmaiseksi, koska malli on jo tiedossa

**Tila B jätetään odottamaan.** 27 riviä × 60 min on 27 tuntia, ja moni niistä on
vanhoja, pienen kannan moottoreita. Se kannattaa tehdä vasta, jos vaiheen 1 mittari
(konversio huoltokortilta öljyn ja suodattimen ostoon) näyttää vihreää.

---

## CSV:n sarakkeet

`rivi_id`, `prio` (1–4, kannan koon mukaan), `valmistaja`, `malli_sovellus`, `tyyppi`,
`suodatin_sku`, `suodatin_oem`, `suodatin_hinta_eur`, `oljy_spec`,
`oljy_l_suodattimella`, `oljy_l_ilman`, `vaihteisto_oljy`, `vaihteisto_l`,
`vaihtovali_h`, `oljy_sku_ehdotus`, `lahde`, `varmennettu_pvm`, `varmentaja`, `tila`

`lahde` on pakollinen kenttä: rivi ei ole valmis ilman viitettä siihen
käyttöohjekirjaan ja sivuun, josta luku on otettu.
