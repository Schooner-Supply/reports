# Venemoottoriöljyt Suomessa — valikoiman TOP-5

**Päivätty:** 2026-09-14
**Tekijä:** Schooner Supply / dataselvitys
**Kysymys:** Minkälaisia moottoreita suomalaisissa veneissä on, mitä öljyä niihin kuuluu, ja mitkä viisi öljyä kannattaa ottaa myyntiin volyymin perusteella.

---

## 1. Yhteenveto (TL;DR)

Suomen venemoottorikanta on **ylivoimaisesti perämoottorivoittoinen**: 875 700 moottoroidusta
veneestä 90 % on perämoottoriveneitä, ja niistä valtaosa on korkeintaan 20 hv:n koneita.
Sisä- ja sisäperämoottoriveneitä on vain 40 200 kpl, ja määrä on **laskenut 29 % kahdeksassa
vuodessa**. Öljyvalikoiman painopisteen pitää siis olla perämoottoripuolella, ei
sisäperämoottoreissa.

**Suositeltu TOP-5:**

| # | Tuote | Spesifikaatio | Kohdekanta | Arvioitu vuosivolyymi (Suomi) |
|---|-------|---------------|------------|-------------------------------|
| 1 | 4T-perämoottoriöljy **10W-30** | NMMA **FC-W**, API SL/SM | ~514 000 nelitahtiperämoottoria | ~450 000 l |
| 2 | Perämoottorin **vaihteistoöljy SAE 80W-90** | API **GL-5** hypoidi | ~787 000 perämoottorivenettä | ~83 000 l / ~165 000 pulloa |
| 3 | 2T-perämoottoriöljy **TC-W3** | NMMA **TC-W3**, tuhkaton | ~272 000 kaksitahtista | ~130 000 l |
| 4 | Merimoottoridiesel **15W-40** | Volvo Penta **VDS-4.5**, API CK-4/CJ-4, ACEA E7/E9 | ~40 000 dieselkonetta | ~126 000 l |
| 5 | Sisäperämoottoriöljy **25W-40** | NMMA **FC-W** | ~20 000 bensiinisisäperää | ~65 000 l |

Litroissa mitattuna järjestys on yllä oleva. **Kappaleissa (pulloissa) mitattuna vaihteistoöljy
nousee kakkoseksi tai jopa ykköseksi**, koska pakkauskoko on 0,5–1 l ja vaihtoväli on vuosittainen.

---

## 2. Lähdetilanne — lue tämä ennen lukujen käyttöä

Kolme rajoitusta, jotka vaikuttavat siihen, mitä tästä datasta voi päätellä:

**a) Traficomin raakadataa ei saatu ladattua.**
Selvityksen tekohetkellä session verkkopolitiikka esti `traficom.fi`- ja
`avoindata.suomi.fi`-domainit (proxy vastasi 403). Luvut alla ovat Traficomin
**julkaistuista tilastoista ja tutkimuksista**, eivät omasta ajostamme rekisteridumpin
päälle. Jos halutaan SKU-tason tarkkuus (esim. tehojakauma desiileittäin), datasetti
pitää ladata ympäristössä, jossa nämä domainit on sallittu.

**b) Traficomin venerekisterin avoin data ei sisällä moottoritietoja.**
Tämä on olennaisin rajoitus. Traficom on itse todennut, että veneen moottoria ei ole sidottu
veneeseen samalla tavalla kuin auton moottori ajoneuvoon, ja moottoritiedot julkaistaan omana
aineistonaan. Venedatasta löytyy **suurin moottoriteho**, venetyyppi, rungon pituus ja
valmistusvuosi — mutta **ei moottorimerkkiä, ei tahtilukua, ei polttoainetta**.
Merkkikohtaista moottorijakaumaa **ei siis voi johtaa Traficomin datasta lainkaan.**

**c) Rekisteri kattaa vain osan venekannasta.**
Rekisteröintivelvollisuus koskee veneitä, joiden rungon pituus on **vähintään 5,5 m** tai
moottoriteho **vähintään 15 kW (yli 20 hv)**. Rekisterissä on ~231 600 vesikulkuneuvoa (88 %
moottoriveneitä), mutta Suomen koko venekanta on ~1,7 miljoonaa venettä. Juuri se segmentti,
joka on öljyvolyymin kannalta suurin — **enintään 20 hv:n mökkiperämoottorit** — jää rekisterin
ulkopuolelle lähes kokonaan.

Siksi kannan rakenne on otettu Traficomin **Veneilytutkimus 2024** -julkaisusta
(*Veneilyn määrä sekä sen taloudelliset ja ympäristövaikutukset Suomessa*), joka kattaa myös
rekisteröimättömät veneet.

---

## 3. Moottorikanta Suomessa

### 3.1 Kannan rakenne (Traficom, Veneilytutkimus 2024)

| Venetyyppi | Määrä | Osuus moottoroiduista | Muutos 2016→2024 |
|------------|-------|----------------------|------------------|
| Perämoottorivene, **≤ 20 hv** | 576 600 | 66 % | **+91 %** |
| Perämoottorivene, **> 20 hv** | 210 400 | 24 % | +25 % |
| Sisämoottori- ja sisäperämoottorivene | 40 200 | 4,6 % | **−29 %** |
| *(Moottoroidut yhteensä)* | **875 700** | 100 % | +58 % |
| Soutuveneet (ei moottoria) | 528 300 | — | — |
| *Koko venekanta* | *~1,7 milj.* | — | +48 % |

Rekisteripuolella (~231 600 vesikulkuneuvoa): moottorivene 88 %, purjevene toiseksi yleisin,
vesiskootterit kolmanneksi yleisin ja kasvussa (yli 11 000 kpl ja nousee).
Ensirekisteröinnit ovat laskussa — moottoriveneitä 1 649 kpl (−16 %), vesijettejä 355 (−47 %) —
eli **uusmyynti ei ole ajuri, kannan huolto on**.

### 3.2 Mitä tämä tarkoittaa moottorityypeittäin

**Perämoottorit (~787 000 venettä, 90 % moottoroidusta kannasta).**
Uusia kaksitahtisia ei enää myydä, mutta käytettyjen kauppa käy vilkkaana — Nettivenen datan
mukaan yhtenä alkuvuotena myytiin 437 nelitahtista ja 364 kaksitahtista, eli **kaksitahtiset
ovat edelleen lähes puolet käytettyjen moottoreiden kaupasta**. Kaksitahtinen kanta ei siis
katoa vielä vuosiin, ja se on painottunut nimenomaan pieniin mökkimoottoreihin.
Merkkikentässä Yamaha, Honda, Suzuki, Mercury ja Tohatsu; Mercuryn pienet koneet ovat
Tohatsun valmistamia ja isommat Hondan pohjalta — sama öljyspeksi joka tapauksessa.

**Sisä- ja sisäperämoottorit (40 200 venettä, laskeva).**
Bensiinipuolella lähes yksinomaan Volvo Penta (GM-pohjaiset 4,3 V6 sekä 5,0/5,7 small-block ja
7,4 big-block V8) ja MerCruiser. Dieselpuolella Volvo Penta D-sarja ja vanhemmat MD/AQAD,
Yanmar, Nanni, Vetus.

**Purjeveneet.** Rekisterin toiseksi yleisin tyyppi. Käytännössä jokaisessa on pieni
apumoottoridiesel (Volvo Penta MD2020/D1-20/D1-30, Yanmar 2GM/3YM) — tämä on
dieselöljyn toinen jalka bensasisäperien lisäksi. Purjeveneistä 70 % on katsastettu, eli
omistajat huoltavat veneensä selvästi keskimääräistä ahkerammin.

---

## 4. Mitä öljyä mihinkin kuuluu

| Moottorityyppi | Oikea spesifikaatio | Huom. |
|----------------|--------------------|-------|
| **Nelitahtiperämoottori** (Yamaha F, Honda BF, Suzuki DF, Mercury FourStroke, Tohatsu MFS) | **NMMA FC-W**, SAE 10W-30 tai 10W-40 | FC-W lisää korroosiosuojan, vaahtoamisenkeston ja leikkauslujuuden vs. autoöljy. Suzuki DF suosittelee 10W-40, Yamaha/Honda 10W-30 tai 10W-40 → **10W-30 kattaa Suomen olosuhteissa kaikki**. Katalysaattorillisiin FC-W (CAT). |
| **Kaksitahtiperämoottori** (vanhat Johnson/Evinrude/Yamaha/Mercury/Suzuki 2T) | **NMMA TC-W3**, tuhkaton | Ei saa korvata autojen 2T-öljyllä: väärä öljy → renkaiden jumitus ja karstoittuminen. Sekoitussuhde tyypillisesti 1:50, öljyinjektiolla varustetuissa säiliöön. |
| **Perämoottorin ja perävetolaitteen kulmavaihde** | **SAE 80W-90, API GL-5** hypoidi | Sama öljy käy käytännössä kaikkiin perämoottorimerkkeihin (Mercury, MerCruiser Alpha, Johnson/Evinrude/OMC, Suzuki, Yamaha, Tohatsu). Volvo Pentan vetolaitteet: valmistaja määrittää 75W-90 synteettisen — oma SKU tarvittaessa. |
| **Bensiinisisäperä / -sisämoottori** (Volvo Penta GM-pohjaiset, MerCruiser) | **SAE 25W-40, NMMA FC-W** | Sekä Volvo Penta että Mercury määrittävät 25W-40 marine-öljyn. Vaihtoväli 100–150 h tai vähintään kerran vuodessa. |
| **Merimoottoridiesel** (Volvo Penta D1–D6, MD/AQAD, Yanmar, Nanni, Vetus) | **SAE 15W-40**, Volvo Penta **VDS-4.5**, API CK-4/CJ-4/CI-4, ACEA E7/E9 | VDS-4.5 on taaksepäin yhteensopiva kaikkiin vanhempiin VDS-1/2/3/4-koneisiin → **yksi SKU kattaa koko Volvo Penta -dieselkannan**. Sama öljy käy myös Yanmariin ja Nanniin API-luokituksen kautta. |
| **Trim & tilt -hydrauliikka** | ATF tai valmistajan trim-neste | Pieni volyymi, ei TOP-5:een. |

---

## 5. Volyymiarvio ja TOP-5-perustelu

Alla oleva on **malli, ei mitattua dataa**. Kannan koko on Traficomin, mutta huoltoaktiivisuus,
tahtilukujakauma ja öljymäärät ovat arvioita. Ne on kirjoitettu näkyviin, jotta luvut voi
korjata paremmilla oletuksilla.

| Segmentti | Kanta | Osuus, jolle SKU käy | Vaihtoja/vuosi | l / vaihto | **l / vuosi** |
|-----------|-------|---------------------|----------------|-----------|--------------|
| 4T-perä ≤20 hv | 576 600 | 60 % on 4T → 346 000 | 35 % | 0,8 | ~97 000 |
| 4T-perä >20 hv | 210 400 | 80 % on 4T → 168 000 | 60 % | 3,5 | ~353 000 |
| **→ 10W-30 FC-W yhteensä** | | | | | **~450 000** |
| 2T-perä (kaikki koot) | 272 000 | 100 % | jatkuva kulutus 1:50 | 0,6–3,0 | **~130 000** |
| Diesel (purje + sisä) | ~40 000 | 100 % | 70 % | 4,5 | **~126 000** |
| Vaihteistoöljy (kaikki perämoottorit) | 787 000 | 100 % | 30 % | 0,35 | **~83 000** (≈165 000 pulloa) |
| 25W-40 bensiinisisäperä | ~20 000 | 100 % | 65 % | 5,0 | **~65 000** |

**Miksi juuri nämä viisi:**

1. **10W-30 FC-W** — ei kilpailijaa listalla. Kohdekanta on 514 000 moottoria ja kasvaa
   (+91 % pienissä perämoottoreissa 8 vuodessa). Yksi viskositeetti kattaa kaikki viisi
   päämerkkiä Suomen vesissä.
2. **80W-90 GL-5 vaihteistoöljy** — pakollinen vuosihuoltotuote, joka koskee **jokaista**
   perämoottorivenettä riippumatta tahtiluvusta, tehosta tai merkistä. Alhainen litravolyymi
   mutta korkein kappalemäärä ja paras katteen kestävyys pienessä pakkauksessa.
3. **TC-W3** — kaksitahtikanta ei katoa, koska käytettyjen 2T-moottoreiden kauppa on edelleen
   lähes yhtä suurta kuin nelitahtisten. Kulutus on jatkuvaa (per tankattu litra), ei
   kertaluonteista → uusintaostoja koko kauden ajan.
4. **15W-40 VDS-4.5** — pieni kanta mutta suurin kate ja korkein huoltoaktiivisuus
   (purjeveneistä 70 % katsastettu). Yksi SKU kattaa taaksepäin yhteensopivuutensa ansiosta
   koko Volvo Penta -dieselkannan sekä Yanmarin ja Nannin.
5. **25W-40 FC-W** — segmentti on laskeva (−29 %), mutta se on ainoa oikea speksi Volvo Pentan
   ja MerCruiserin bensakoneisiin, litroja per vaihto on eniten, eikä tuotteelle ole
   korvaajaa muualla listalla.

**Kuudes, jos valikoimaa laajennetaan:** 4T-perämoottoriöljy **10W-40** (Suzuki DF:n oma
suositus ja lämpimän kauden käyttäjien valinta) tai **Volvo Penta -vetolaiteöljy 75W-90 synt.**

---

## 5b. Merkit: TOP-3 per öljylaji

**Menetelmä ja varaus:** venemoottoriöljyjen merkkikohtaista myyntitilastoa ei julkaista
Suomessa — ei Traficomilla, ei Finnboatilla, ei kaupan keskusliitoilla. Alla oleva järjestys
perustuu **jakelupeittoon**: montako Suomen merkittävää kanavaa (Motonet, Biltema, Bauhaus,
Kärkkäinen, Watski, Maritim, Marinekauppa, Marineparts, Harrasteosa, SVB, Veneakselisto,
Motobox, Fiksaa, WaveMotor) pitää merkkiä hyllyssä. Se on paras havaittava proxy volyymille,
mutta se **ei ole mitattu myynti**.

| Öljylaji | 1. | 2. | 3. |
|----------|----|----|----|
| **10W-30 FC-W (4T-perä)** | **Quicksilver** (Mercury) | **Yamalube** | **Star brite Pro Star** |
| **80W-90 GL-5 (vaihteisto)** | **Quicksilver** High Performance Gear Lube | **Star brite** 80W-90 | **Yamalube** 80W-90 |
| **TC-W3 (2T-perä)** | **Quicksilver** TCW3 Premium | **Neste Marine 2T** | **Liqui Moly** Marine 2T |
| **15W-40 (merimoottoridiesel)** | **Volvo Penta VDS-4.5** (OEM) | **Orbitrade** 15W-40 | **Liqui Moly** Marine 15W-40 |
| **25W-40 FC-W (bensiinisisäperä)** | **Quicksilver** 25W-40 | **Star brite Pro Star** 25W-40 | **Liqui Moly** Marine 4T 25W-40 |

### Huomiot

- **Quicksilver on ainoa merkki, joka kattaa kaikki viisi lajia.** Se on myös ainoa, jonka
  valmistaja itse listaa 25W-40:n sopivaksi sekä MerCruiseriin, OMC:hen **että Volvo Pentaan** —
  eli yksi SKU kattaa koko bensiinisisäperäkannan.
- **Star brite kattaa neljä viidestä** (ei dieseliä) ja on NMMA FC-W -sertifioitu.
  Kaksi merkkiä riittää siis koko valikoimaan, kun diesel hoidetaan Volvo Pentan omalla öljyllä.
- **Ketjujen omia merkkejä ei voi ostaa jälleenmyyntiin.** Motonetin *Motox Marine* (80W-90) ja
  Bilteman omat perämoottori- ja dieselöljyt ovat volyymissa kärkipäätä, mutta ne ovat
  kilpailijoiden private labeleita — ne kuuluvat hintavertailuun, eivät ostoslistalle.
- **OEM-öljyt ovat jälleenmyyjäkanavan tuotteita.** Yamalube, Suzuki ECSTAR Marine (10W-40,
  Suzukin oma suositus) ja Honda Marine (5W-30) myydään pääosin merkkihuoltojen ja
  sopimuskauppiaiden kautta — vaativat yleensä dealer-sopimuksen, eivät ole vapaasti tukusta.
- **Kotimainen kulma:** Neste Marine 2T on NMMA TC-W3 -luokiteltu ja Teboil valmistaa
  marine-voiteluaineensa Haminassa. Jos kotimaisuus halutaan myyntiargumentiksi, nämä ovat
  ainoat aidot vaihtoehdot.

**Suositus toimittajarakenteeksi:** *Quicksilver* (5/5 lajia) + *Star brite* (4/5, edullisempi
hintapiste) + *Volvo Penta VDS-4.5* (diesel, OEM-nimi jota asiakas hakee) = koko TOP-5 katettu
kolmella toimittajasuhteella.

---

## 6. Ristiintarkistus omaan dataan (Shopify)

- **Korjaus:** tämän raportin ensimmäinen versio väitti, ettei katalogissa ole yhtään
  moottoriöljyä. Se oli väärin — haku katkesi 30 tulokseen. Katalogissa on jo
  **Bergoline GENERAL OIL -sarja** Osculatin kautta, ja se kattaa neljä viidestä
  TOP-5-kategoriasta:

  | SKU | Tuote | Hinta | Kattaa |
  |-----|-------|-------|--------|
  | 65.081.00 / .01 | 2 stroke sea F1, NMMA TC-W3, 1 l / 5 l | 15,95 / 64,90 € | **#3** |
  | 65.082.00 | Marine Speed 4-stroke 10W-40 | 13,95 € | **#1** (10W-40) |
  | 65.085.01 | Prestige Diesel Marine 15W-40 | 55,95 € | **#4** |
  | 65.087.00 | Hypo Marine SAE 80W-90 | 12,45 € | **#2** |
  | 65.086.00 | Hypo Marine 80W-90 Bio Type | 19,95 € | #2 (bio) |
  | 65.084.01 | Sintetix Diesel Marine 10W-40 | 63,95 € | — |
  | 65.083.00 / .01 | Marine Hydraulic Oil / ATF Red Oil | 12,95 / 13,95 € | — |

  Kysymys ei siis ole "mitkä viisi otetaan sisään" vaan **"miksi olemassa olevat eivät
  löydy eivätkä myy"**. Aidosti puuttuu vain **25W-40** (bensiinisisäperä, TOP-5 #5)
  ja **10W-30** nykyisen 10W-40:n rinnalle. Luvun 5b merkkisuositukset koskevat sitä,
  mihin valikoimaa laajennetaan tai millä Bergoline korvataan — eivät nollatilannetta.
- **Öljynsuodattimet on jo valikoimassa** ja ne osoittavat samaan moottorikantaan:
  Suzuki, Yamaha/Selva, Mercury, Tohatsu ja Honda nelitahtiperämoottoreille sekä
  Volvo ja Yanmar sisämoottoreille. Öljy on näiden luonteva liitännäinen — suodatin ja
  öljy myydään samassa ostoskorissa. Yksityiskohtainen erittely: `huoltodata-vaihe0-tulos.md`.
- Valikoimassa on myös **öljynvaihtopumput ja imurit** (Marco, Osculati) sekä
  vaihteistoöljypumppu (65.116.20) — kokonainen öljynvaihtokori on rakennettavissa jo
  olemassa olevien tuotteiden päälle.
- **Oma myyntidata ei riitä öljyjen priorisointiin.** Viimeisen 12 kk myydyin tuote on
  39 kpl ja koko top-25:n yhteismäärä 358 kpl. Volyymijärjestys on siksi johdettava
  kantarakenteesta, ei omasta historiasta.

---

## 7. Suositus toimenpiteiksi

1. Otetaan **viisi SKU:ta** yllä olevan taulukon mukaisesti — käytännössä täydennetään
   olemassa olevaa Bergoline-sarjaa 25W-40:llä ja 10W-30:llä.
2. Pakkauskoot: 10W-30 ja TC-W3 sekä **1 l että 4/5 l**; vaihteistoöljy **0,5 l** (kertakäyttö,
   yksi vaihto per vene); 15W-40 ja 25W-40 **5 l**.
3. Vaaditaan toimittajalta **NMMA-sertifikaatit näkyviin** (FC-W ja TC-W3) — se on ainoa
   konkreettinen erottautumistekijä Motonetin ja Bilteman yleisöljyjä vastaan, ja se on myös
   takuuehtojen kannalta ratkaiseva.
4. Niputetaan öljyt olemassa olevien **öljynsuodattimien ja öljynvaihtopumppujen** kanssa
   merkkikohtaisiksi huoltopaketeiksi (esim. "Yamaha F60 -vuosihuolto").
5. Sesonki: perämoottoriöljyn kysyntä painottuu **huhti–kesäkuulle** (kevätvarustelu) ja
   **syys–lokakuulle** (talvisäilytys). Varasto sisään maaliskuussa.

**Ennen lopullista ostopäätöstä kannattaa vielä hakea:** Traficomin venerekisterin
tehojakauma (suurin moottoriteho -kenttä) desiileittäin, jotta 4T-öljyn pakkauskokojakauma
(1 l vs. 4 l) osuu oikein. Se vaatii raakadatan latauksen ympäristössä, jossa
`traficom.fi` ei ole estetty.

---

## Lähteet

- [Vesikulkuneuvojen määrä rekisterissä kasvaa – veneet vaihtavat yhä useammin omistajaa (Traficom)](https://www.traficom.fi/fi/ajankohtaista/vesikulkuneuvojen-maara-rekisterissa-kasvaa-veneet-vaihtavat-yha-useammin-omistajaa)
- [Veneilyn määrä sekä sen taloudelliset ja ympäristövaikutukset Suomessa 2024 (Traficom)](https://www.traficom.fi/sites/default/files/media/publication/Veneilyn%20m%C3%A4%C3%A4r%C3%A4%20sek%C3%A4%20sen%20taloudelliset%20ja%20ymp%C3%A4rist%C3%B6vaikutukset%20Suomessa%202024_FINAL.pdf)
- [Veneilijöiden määrä on kasvanut (Traficom)](https://traficom.fi/fi/uutiset/veneilijoiden-maara-kasvanut-nopeiden-veneiden-kuljettajille-toivotaan-alaikarajaa)
- [Venerekisteri (Traficom)](https://traficom.fi/fi/veneily/veneen-rekisterointi/venerekisteri)
- [Vesikulkuneuvojen avoin data (Avoindata.fi)](https://avoindata.suomi.fi/data/fi/dataset/veneiden-avoin-data)
- [Vesikulkuneuvojen ensirekisteröinnit 2025 (Totalvene)](https://www.totalvene.fi/lue/reportaasi/vesikulkuneuvojen-ensirekisteroeinnit-2025)
- [Käytetyt koneet käyvät kaupaksi, kaksitahtisia perämoottoreita myydään edelleen paljon (Kipparilehti)](https://kipparilehti.fi/kaytetyt-koneet-kayvat-kaupaksi-kaksitahtisia-peramoottoreita-myydaan-edelleen-paljon/)
- [TC-W3 Two-Stroke Oil Certification Program (NMMA)](https://www.nmma.org/certification/oil/tc-w3)
- [FC-W Catalyst Compatible Four-Stroke Oil Certification (NMMA)](https://www.nmma.org/certification/oil/fc-wcat)
- [Millaista öljyä Volvo Penta sisäperämoottoreihin käytetään? (WaveMotor)](https://wavemotor.fi/millaista-oljya-volvo-penta-sisaperamoottoreihin-kaytetaan/)
- [VDS-4.5 Engine oil 15W40 (Volvo Penta)](https://www.volvopenta.com/shop/0/part-group/PG1740)
- [Vaihteistoöljy Outboard 80W-90 GL5 (Watski)](https://www.watski.fi/ljy-Outboard-80W-90-GL5-119HE)
- [Star brite Pro Star 25W-40 (Starbrite.fi)](https://starbrite.fi/tuote/moniaste-4-tahti-peramoottorioljy-sae-25w-40/)
- [Neste Marine 2T](https://motocafe.fi/tuote/neste-marine-2t-kaksitahtimoottorioljy-peramoottoreihin-1-litra/)
- [Orbitrade 15W-40 (Veneakselisto)](https://veneakselisto.com/kauppa/tuote/orbitrade-15w-40-merimoottorioljy-5-l/)
- [Suzuki ECSTAR Marine 10W-40 (Motobox)](https://www.motobox.fi/tuote/suzuki-ecstar-marine-moottorioljy-10w-40-semi-synthetic-4l/)
- [Teboil Marine](https://www.teboil.fi/tuotteet/voiteluaineet/marine)
