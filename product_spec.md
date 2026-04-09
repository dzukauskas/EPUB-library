# PRODUCT_SPEC

## Paskirtis
Šis dokumentas fiksuoja produkto taisykles: ką sistema turi gaminti, kokiais principais tai turi daryti ir kokio pobūdžio išvestys yra kanoniškai leidžiamos.

## Vieno skyriaus išvestys
Kiekvienas skyrius turi 2 galutines išvestis:

1. **Kanoninis LT skyrius** — `lt/chapters/<slug>.md`
2. **Mokymosi blokas** — `lt/learning/<slug>.md`

## Failų modelis
Kiekvienam skyriui turi būti bent:

- `lt/chapters/<slug>.md` — kanoninis LT skyrius
- `lt/learning/<slug>.md` — mokymosi blokas

Repo yra vienintelis kanoninis šaltinis. Obsidian yra vienakryptė sinchronizuota skaitymo ir mokymosi kopija, kurioje gali būti saugomi abu artefaktai: ir kanoninis LT skyrius, ir mokymosi blokas.

## Knygos darbo eiga
### Naujos knygos pradžia
Prieš 1 skyriaus vertimą sistema turi atlikti visos knygos įvadinį paruošimą:

- ingest'inti EPUB;
- išanalizuoti knygos tematiką;
- sudaryti preliminarų rizikos žemėlapį;
- ištraukti pasikartojančių terminų branduolį;
- pažymėti tikėtinus LT / ES konfliktų tipus;
- sukurti knygos lygio profilį / paruošimo failą;
- sugeneruoti ir pateikti `chapter_map`;
- pranešti, kad knyga paruošta vertimui;
- laukti vartotojo leidimo pradėti 1 skyrių.

### Vertimo seka
- knyga verčiama nuosekliai nuo pirmo skyriaus;
- dirbama po vieną skyrių;
- prie kito skyriaus pereinama tik po vartotojo leidimo.

### Vieno skyriaus ciklas
Vienam vartotojo prašymui sistema gali tame pačiame skyriuje pereiti per pilną ciklą iki QA arba sustoti ties pirmu privalomu žmogaus sprendimo tašku:

- kanoninis LT skyrius;
- terminijos sprendimai;
- LT / ES validacija;
- blocker resolution;
- mokymosi blokas;
- QA.

Tai aprašo vartotojo sąveikos modelį, o ne techninių vykdymo žingsnių skaičių.

Po to vartotojas gali paprašyti pataisų.

## Taisymo politika po review
### Numatytoji taisymo politika
Numatytoji taisymo seka:

1. lokalus taisymas
2. paveiktos sekcijos pergeneravimas
3. viso skyriaus perrašymas tik išimtimi

### Po taisymo turi būti atnaujinta
Po taisymo turi būti atnaujinami paveikti sluoksniai:

- kanoninis LT skyrius;
- mokymosi blokas;
- terminų sluoksnis;
- blockeriai;
- QA vartai.

## Lokalizacijos logika
### Bendra taisyklė
- universalus turinys verčiamas kuo ištikimiau;
- aukštos rizikos / norminis turinys pagrindiniame LT tekste turi būti LT / ES logikos;
- originalo rinkos specifika negali likti pagrindiniame LT tekste kaip tariama vietinė norma.

### `Originalo kontekstas`
Jei originalo detalė verta išsaugoti, bet netinka kaip LT / ES norma, ji turi būti perkelta į aiškiai pažymėtą `Originalo kontekstas` bloką.

### Pasenęs ar konfliktiškas originalo turinys
Jei originali knyga pateikia pasenusį, abejotiną ar su LT / ES praktika konfliktuojantį aukštos rizikos turinį:

- jo negalima palikti pagrindiniame kanoniniame LT tekste kaip dabartinės tiesos;
- prireikus jis perkeliamas į `Originalo kontekstas`;
- sprendimo logika turi būti fiksuojama `research` sluoksnyje.

## Aukštos rizikos turinys
Aukštos rizikos turinys:

- algoritmai ir veiksmų seka;
- vaistai, dozės, vartojimo keliai;
- indikacijos ir kontraindikacijos;
- kompetencijų ribos;
- guideline-dependent sprendimai;
- rinkai ar jurisdikcijai specifiniai dalykai;
- teisiniai / organizaciniai medicinos sistemos reikalavimai.

Žemos rizikos turinys:

- anatomija;
- fiziologija;
- patofiziologija;
- bendri aiškinamieji aprašymai.

## Šaltinių politika
### Neaiškumų tikrinimas
Jei terminas, teiginys ar lokalizacijos sprendimas neaiškus, sistema privalo tikrinti internete. Negalima remtis vien modelio atmintimi, pasenusiomis žiniomis ar spėjimu.

### Šaltinių prioritetas
1. oficialūs LT šaltiniai
2. stiprūs LT medicinos / akademiniai / universitetiniai šaltiniai
3. stiprūs LT klinikinės vartosenos šaltiniai
4. oficialūs ES šaltiniai
5. originalo rinkos šaltiniai tik kaip kontekstas

### Globalaus termino užrakinimo slenkstis
Naują globalų terminą galima užrakinti tik tada, kai yra:

- vienas tikrai stiprus oficialus LT šaltinis;
- arba du nepriklausomi stiprūs LT šaltiniai, jei oficialaus nėra.

### ES šaltinių vaidmuo
ES šaltinis gali leisti tęsti darbą, bet pats vienas negali automatiškai sukurti globaliai užrakinto LT termino.

### Konfliktuojantys stiprūs šaltiniai
Jei stiprūs LT ar ES šaltiniai tarpusavyje konfliktuoja:

- sistema negali improvizuoti „vidurinio“ varianto;
- jei nėra aiškaus stipresnio šaltinio pagal hierarchiją, tai tampa blockeriu ir turi būti eskaluojama vartotojui.

## Terminų architektūra
### Pagrindinis vienetas
Globaliame terminų žodyne bazinis vienetas yra **sąvoka** (`concept_id`), ne raw angliškas terminas.

### Modelis
Kiekviena sąvoka turi:

- vieną pageidaujamą globalų LT terminą;
- galimus kontekstinius variantus;
- draudžiamus / atmestus variantus;
- LT šaltinių pagrindą;
- statusą.

### Būsenos
Globalus terminų sluoksnis turi bent 3 būsenas:

- globaliai užrakintas
- leidžiamas tik konkrečiame kontekste
- kandidatas, dar neužrakintas

### Promotion taisyklė
- sistema gali auto-promote’inti tik tada, kai yra pakankama LT atrama pagal globalų užrakinimo slenkstį ir nėra rimto konkurencinio varianto, kuris sukeltų dviprasmybę;
- jei keli LT variantai atrodo panašiai stiprūs, jei šaltiniai konfliktuoja, arba jei sprendimas paveiktų aukštos rizikos turinį ar globalų terminų sluoksnį, sistema negali promuoti automatiškai ir turi palikti review / escalation kelią;
- tai reiškia: automatinis promotion leidžiamas tik aukšto pasitikėjimo, vienareikšmiams atvejams, o visi abejotini ar konfliktiniai atvejai turi būti sprendžiami per formalų review.

### Konfliktas su jau užrakintu terminu
- pagal nutylėjimą galioja globaliai užrakintas terminas;
- knygos lygiu galima leisti išimtį tik su aiškia priežastimi ir review;
- jei tokia išimtis kartojasi per kelias knygas, sistema turi siūlyti ją kelti į globalią kontekstinę išimtį.

### Vartotojo pataisų promotion
- vienkartinė lokali pataisa lieka tame skyriuje;
- kartotinio pobūdžio pataisoms sistema turi siūlyti promotion į knygos lygio ar globalų sluoksnį;
- galutinis promotion sprendimas yra review-gated.

### Termino pasikeitimas vėliau
Jei globalus terminas pasikeičia:

- sistema automatiškai suranda visus paveiktus skyrius;
- mažos rizikos vietoms gali siūlyti ar taikyti automatinį atnaujinimą;
- aukštos rizikos ir jau užbaigtiems skyriams reikia review.

## Santrumpos ir akronimai
- jei yra aiškiai įsitvirtinusi LT santrumpa, naudoti ją;
- jei tarptautinė / angliška santrumpa yra svarbi skaitymui ir literatūrai, pirmą kartą rodyti: `lietuviškas pilnas terminas (angliška santrumpa)`;
- jei santrumpa aukštos vertės mokymuisi, ją papildomai laikyti mokymosi bloko terminų sekcijoje.

## Blocker'ių politika
### Kas sprendžia blockerį
Pirmas sprendėjas turi būti pati sistema, ne vartotojas.

### Sprendimo tvarka
- sistema aptinka blockerį;
- atlieka tikslinę LT ir, jei reikia, ES paiešką;
- klasifikuoja problemą;
- jei turi aukštą pasitikėjimą ir stiprią LT atramą, gali pati uždaryti blockerį;
- visais kitais atvejais turi pateikti vartotojui trumpą sprendimo paketą.

### Eskalavimo taisyklė
Sistema pati gali uždaryti blockerį tik tada, kai turi aukštą pasitikėjimą ir stiprią LT atramą. Kitais atvejais ji eskaluoja vartotojui.

## Skyriaus užbaigimas
### Galutinis užbaigimas
- mažos rizikos skyriams sistema gali užbaigti pati;
- aukštos rizikos skyriams reikia galutinio vartotojo patvirtinimo.

### Jei skyriuje lieka problema
Aukštos rizikos blockeriai negali būti ignoruojami. Laikinas juodraštis leidžiamas kaip tarpinė būsena, bet neužbaigtas skyrius negali būti laikomas pilnai patikimu.

## Mokymosi blokas
### Bendra logika
Mokymosi blokas yra vienas standartizuotas artefaktas per skyrių, ne kelios atskiros išvestys.

### Struktūra
- yra pastovus branduolys visiems skyriams;
- papildomos sekcijos prisitaiko pagal skyriaus tipą.

### Pavyzdžių politika
- aiškinamieji pavyzdžiai leidžiami plačiai;
- klinikiniai mini-scenarijai leidžiami tik kaip aiškiai pažymėti mokomieji pavyzdžiai;
- originalo / LT-ES šaltinių pavyzdžiai ir sistemos sugeneruoti didaktiniai pavyzdžiai turi būti atskirti.

### Angliški terminai mokymosi bloke
- LT terminas yra pagrindinis;
- EN terminas rodomas saikingai ir tik atrinktiems aukštos vertės terminams;
- jei terminas aukštos vertės mokymuisi, jis turi būti rodomas dviem vietomis:
  1. pirmą kartą mokymosi bloko tekste formatu `lietuviškas terminas (english term)`;
  2. atskiroje terminų sekcijoje kaip svarbus LT/EN atitikmuo;
- jei terminas nėra aukštos vertės mokymuisi, EN forma neturi būti kaišiojama į tekstą vien dėl pilnumo.

### Papildomi LT / ES aiškinimai
Mokymosi blokas gali turėti papildomų LT / ES aiškinimų, kurie originalioje knygoje tiesiogiai nebuvo pateikti, jei jie padeda geriau suprasti temą. Jie turi būti aiškiai atskirti nuo to, kas tiesiogiai kilo iš originalo.

### Perregeneravimas pasikeitus kanoniniam skyriui
Mišrus modelis:

- jei pakeitimas mažas, mokymosi blokas pažymimas kaip reikalaujantis atnaujinimo;
- jei pakeitimas esminis, sistema jį automatiškai perregeneruoja.

### Anki / Q&A
Kol kas tai nėra privaloma pagrindinio workflow dalis. Šis sluoksnis paliekamas vėlesniam etapui.

### Mokymosi bloko branduolio schema v1
Mokymosi blokas negali būti laisvos formos konspektas. Jis turi turėti:

- pastovų branduolį, kad būtų nuoseklus per visas knygas;
- temines sekcijas, kurios aktyvuojamos tik tada, kai jos tikrai tinka konkrečiam skyriui.

### Privalomos sekcijos visiems mokymosi blokams
Kanoninė privalomų sekcijų eilė:

1. `Skyriaus esmė`
2. `Svarbiausi terminai`
3. `Pagrindinė logika / mechanizmas`
4. `Paaiškinamieji pavyzdžiai`
5. `Ką būtina atsiminti`
6. `Savikontrolės klausimai`

Šie LT pavadinimai yra vienintelės kanoninės žmogui matomos v1 sekcijų antraštės šiam branduoliui. Techninis `learning_section_id` vardynas turi būti aprašytas `architecture.md` ir išlaikyti 1:1 ryšį su šiomis sekcijomis, bet negali jų pakeisti ar sukurti atskiros produkto taksonomijos.

Papildomos taisyklės šioms sekcijoms:

- `Skyriaus esmė` turi būti trumpas įėjimo taškas, ne ilgas naratyvas; pageidaujamas formatas yra `3-8` glausti punktai arba trumpas struktūruotas blokas su pagrindiniais akcentais;
- `Svarbiausi terminai` privalo išlaikyti LT centrą ir rodyti EN tik tada, kai tai naudinga mokymuisi; joje turi būti LT terminas, EN atitikmuo, jei taikoma, ir trumpas paaiškinimas ar funkcija, net jei terminų nedaug;
- `Pagrindinė logika / mechanizmas` turi paaiškinti ne tik faktus, bet ir reiškinio ar veiksmų sekos logiką; anatomijai / fiziologijai tai dažniausiai yra mechanizmo logika, patologijai - pokyčių seka, klinikiniams skyriams - atpažinimo ar veikimo logika;
- `Paaiškinamieji pavyzdžiai` privalo aiškiai atskirti originalo / LT-ES kilmės turinį nuo sistemos sugeneruotų didaktinių pavyzdžių; jei realių pavyzdžių mažai, sekcija vis tiek paliekama, bet gali būti trumpa;
- `Ką būtina atsiminti` turi būti orientuota į greitą kartojimą ir veikti kaip greito grįžimo sekcija; formatas turi likti glaustas, be ilgo aiškinamojo teksto;
- `Savikontrolės klausimai` turi būti orientuoti į supratimą, ne vien į aklą atmintį, ir negali virsti pilnu Anki kortelių formatu; pageidaujamas formatas yra trumpi klausimai.

### Sąlyginės sekcijos pagal skyriaus tipą
Leidžiamos / privalomos sekcijos:

- `Algoritminė eiga`
- `Vaistai ir dozės`
- `Raudonos vėliavos / dažnos klaidos`
- `Klinikiniai mini-scenarijai`
- `Papildomas LT / ES paaiškinimas`
- `Paveikslų / schemų paaiškinimas`

Šie LT pavadinimai taip pat lieka kanoniniai žmogui matomi heading'ai. Jei workflow ar schema naudoja techninius `learning_section_id`, jie turi deterministiškai rodyti tik į šiame skyriuje ir aukščiau jau užrakintas produkto sekcijas.

Taisyklės:

- `Algoritminė eiga` privaloma, jei skyrius iš esmės yra algoritminio pobūdžio;
- `Vaistai ir dozės` privaloma, jei skyriaus branduolys stipriai remiasi farmakologiniu turiniu;
- `Raudonos vėliavos / dažnos klaidos` labai rekomenduojama aukštos rizikos skyriams;
- `Klinikiniai mini-scenarijai` leidžiami tik kaip aiškiai pažymėti mokomieji scenarijai;
- `Papildomas LT / ES paaiškinimas` leidžiamas tik aiškiai atskiriant jį nuo originalo;
- `Paveikslų / schemų paaiškinimas` naudojamas tik tada, kai figūra mokymosi požiūriu tikrai svarbi.

### Sekcijų būsenos
Kiekviena mokymosi bloko sekcija turi turėti vieną iš loginių būsenų:

- `required`
- `optional_enabled`
- `optional_disabled`
- `not_allowed`

### Ryšys su `chapter_pack`
Mokymosi bloko struktūra negali būti nustatoma vien iš jau sugeneruoto LT teksto.

Ji turi būti iš anksto valdoma per `chapter_pack`, kuriame turi būti bent:

- `learning_block_profile`
- `required_sections[]`
- `optional_sections_enabled[]`
- `optional_sections_disabled[]`
- `not_allowed_sections[]`

### Kada sekcija turi būti automatiškai pažymėta kaip `required`
Sistema turi automatiškai žymėti papildomas sekcijas kaip `required`, jei tenkinamos tam tikros sąlygos.

Pavyzdžiai:

- jei skyriuje yra aiški algoritminė veiksmų seka -> `Algoritminė eiga = required`;
- jei skyriuje yra vaistai ir dozės -> `Vaistai ir dozės = required`;
- jei skyrius aukštos rizikos ir jame tikėtinos pavojingos interpretavimo klaidos -> `Raudonos vėliavos / dažnos klaidos = required`;
- jei skyriuje svarbios figūros -> `Paveikslų / schemų paaiškinimas = optional_enabled` arba `required`, priklausomai nuo svarbos.

### Ko mokymosi blokas neturi daryti
Jis neturi:

- tapti antru kanoniniu vertimu;
- laisvai perrašyti visą originalo logiką neprisirišus prie kanoninio LT sluoksnio;
- maišyti šaltinio kilmės ir sugeneruotų didaktinių pavyzdžių vienoje nepažymėtoje masėje;
- grūsti EN terminų ten, kur jie nepadeda mokymuisi;
- būti nestruktūruotas ir kaskart vis kitoks.

### Kodėl šitas branduolys logiškas būtent šitam projektui
Šis modelis atitinka projekto tikslą:

- mokymosi blokas išlieka nuoseklus per visas knygas;
- jis nėra per sausas;
- jis turi pavyzdžių;
- jis leidžia turėti aiškią mokymosi architektūrą, ne tik gražesnį konspektą;
- jis išlieka pakankamai formalus OpenCode / Codex CLI agentams.

## Atsekamumas
### Block-level atsekamumas
Pilno block-level atsekamumo nereikia.

### Paliekama tik
- chapter-level source ryšys;
- claim-level įrodymų pėdsakas aukštos rizikos turiniui;
- figure/source ryšys figūrų sluoksnyje.

## Lentelės, figūros, schemos
### Lentelės
Įprastos lentelės turi būti pateikiamos tinkamiausiu markdown formatu, nes galutinis vartojimas yra Obsidian.

### Figūros ir schemos
- svarbios schemos ir diagramos turi būti perpiešiamos lietuviškai per **Whimsical Desktop MCP**;
- raster paveikslėliai ir nuotraukos gali išlaikyti originalų vaizdinį pagrindą, bet visas juose matomas tekstas galutinėje LT išvestyje turi būti lokalizuotas lietuviškai;
- galutinis paveikslėlis negali palikti EN ar kitos kalbos teksto kaip matomo sluoksnio; mixed-language paveikslėlis nelaikomas priimtinu rezultatu;
- `Whimsical` yra pirminis schemų ir diagramų backendas naujame projekte, o paveikslėliams su tekstu leidžiamas atskiras lokalizacijos backendas.

### Kanoninis figūrų modelis
Kiekviena svarbi figūra pirmiausia turi turėti tekstinį kanoninį spec failą repo viduje. Tik po to schema ar diagrama renderinama per Whimsical MCP, o paveikslėlis su tekstu lokalizuojamas per jam skirtą backendą.

### Figure/source ryšys
Figūrų sluoksnyje turi būti aiškus source ryšys.

## Obsidian produktinė politika
### Sync pasiūlymas
Kai skyrius pilnai užbaigtas, sistema turi pati pasiūlyti sinchronizaciją į Obsidian `vault`, kurio kelias įrašytas sistemos failuose.

### Ką sync'inti
Pagal nutylėjimą į Obsidian keliauja:

- kanoninis LT skyrius;
- mokymosi blokas;
- lietuviškai perdirbtos figūros / schemos.

Techninis `research` ir claim-level sluoksnis pagal nutylėjimą nekeliauja.

### Repo vs Obsidian
- repo yra vienintelis kanoninis šaltinis;
- Obsidian yra vienakryptė sinchronizuota skaitymo ir mokymosi aplinka, kurioje saugomi abu sluoksniai;
- pataisymai Obsidian'e savaime netampa kanonine tiesa.

## Knygos lygio profilis
Kiekviena knyga turi turėti atskirą, gyvą knygos lygio profilį / paruošimo failą.

Jame turi gyventi bent:

- knygos tema ir paskirtis;
- preliminarus rizikos žemėlapis;
- pasikartojančių terminų branduolys;
- tikėtini LT / ES konfliktų tipai;
- knygai būdingos lokalizacijos taisyklės;
- atviri knygos lygio klausimai.

Jis turi būti automatiškai atnaujinamas tik tada, kai realiai pasikeičia knygos lygio žinios.

## Knygos ir leidimai
Kiekviena knyga visada turi savo atskirą kanoninį šaltinį. Temos ar leidimo giminingumas nereiškia, kad šaltiniai gali būti suplakti į vieną.

## V1 produkto riba
- projektas kuriamas nuo nulio;
- pirmas etapas yra **EPUB-first**;
- PDF lieka vėlesniam etapui;
- V1 sistema yra **local desktop-first** ir orientuota į vartotojo macOS workstation.
