# PROJECT_CONSTITUTION

## Paskirtis
Šis dokumentas yra trumpas, beveik nekintantis projekto branduolys. Jis fiksuoja aukščiausio lygio taisykles, kurių negalima apeiti nei agentams, nei vėlesniems techniniams sprendimams.

## Misija
Projektas kuriamas asmeninei saviugdai ir mokymuisi.

Tikslas:
- iš angliškų medicininių knygų kurti patikimą, nuoseklią, LT / ES kontekstui peržiūrėtą lietuvišką mokymosi bazę;
- spręsti lietuviškų medicininių knygų trūkumo problemą;
- užtikrinti, kad vertimai būtų tinkami realiam mokymuisi, o ne tik paviršiniam skaitymui.

Projektas nėra bendro pobūdžio EPUB redaktorius ar vien tekstų ištraukimo įrankis.

## Du produkto sluoksniai
Kiekvienam skyriui egzistuoja 2 atskiri sluoksniai:

1. **Kanoninis LT skyrius**
2. **Mokymosi blokas**

### Kanoninis LT skyrius
- turi būti kuo ištikimesnis originalo prasmei, struktūrai ir funkcijai;
- negali būti laisvas perpasakojimas;
- aukštos rizikos turiniui taikoma LT / ES logika;
- turi likti kuo švaresnis skaitymui;
- detalus įrodymų pėdsakas negyvena pačiame tekste.

### Mokymosi blokas
- yra atskiras artefaktas, ne kanoninio skyriaus dalis;
- yra mokymuisi optimizuota antroji versija;
- gali būti išsamus ir turėti pavyzdžių;
- pagrindinis aiškinimas gali būti paprastesnis, bet terminija ir svarbios medicininės formuluotės turi likti profesionalios.

## Kanoninė tiesa
- **Repo yra vienintelis kanoninis šaltinis.**
- GitHub yra versionavimo ir atsekamumo sluoksnis, ne workflow state šaltinis.
- Obsidian yra vienakryptė sinchronizuota skaitymo ir mokymosi aplinka.
- Whimsical yra figūrų kūrimo / render sluoksnis, ne vienintelė kanoninė tiesa.
- Agentai privalo remtis artefaktais, o ne chat istorija ar spėjimu.

## Knygos ir leidimai
- kiekviena knyga visada turi savo atskirą kanoninį šaltinį;
- temos ar leidimo giminingumas nereiškia, kad šaltiniai gali būti suplakti į vieną;
- sistema negali traktuoti kelių leidimų ar panašių knygų kaip vieno bendro source sluoksnio be atskiro architektūrinio sprendimo.

## Lokalizacijos taisyklė
- universalus turinys verčiamas kuo ištikimiau;
- aukštos rizikos / norminis turinys pagrindiniame LT tekste turi būti lokalizuotas LT / ES logika;
- originalo rinkos specifika negali likti pagrindiniame LT tekste kaip tariama vietinė norma;
- jei originalo detalė verta išsaugoti, bet netinka kaip LT / ES norma, ji keliama į `Originalo kontekstas`.

## Aukštos rizikos turinys
Aukštos rizikos turinys:
- algoritmai ir veiksmų seka;
- vaistai, dozės, vartojimo keliai;
- indikacijos ir kontraindikacijos;
- kompetencijų ribos;
- guideline-dependent sprendimai;
- rinkai ar jurisdikcijai specifiniai dalykai;
- teisiniai / organizaciniai medicinos sistemos reikalavimai.

## Šaltinių politika
- jei terminas, teiginys ar lokalizacijos sprendimas neaiškus, sistema **privalo tikrinti internete**;
- negalima remtis vien modelio atmintimi, pasenusiomis žiniomis ar spėjimu;
- šaltinių prioritetas:
  1. oficialūs LT šaltiniai
  2. stiprūs LT medicinos / akademiniai / universitetiniai šaltiniai
  3. stiprūs LT klinikinės vartosenos šaltiniai
  4. oficialūs ES šaltiniai
  5. originalo rinkos šaltiniai tik kaip kontekstas

## Terminų politika
- bazinis vienetas yra **sąvoka** (`concept_id`), ne paprastas EN→LT žodžių poros modelis;
- globalų terminą leidžiama užrakinti tik su pakankama LT atrama;
- ES šaltinis vienas pats negali automatiškai sukurti globaliai užrakinto LT termino;
- aukštos rizikos terminai negali būti paliekami neužrakinti kaip tariamai baigti.

## Blocker'ių ir review politika
- pirmas blocker'io sprendėjas yra pati sistema;
- pati gali uždaryti blocker'į tik aukšto pasitikėjimo ir stiprios LT atramos atvejais;
- aukštos rizikos ar strateginiai sprendimai turi būti eskaluojami vartotojui;
- neleidžiama apeiti žmogaus patvirtinimo taškų.

## Žmogaus sprendimų interpretavimas
- vartotojas gali teikti sprendimus laisvu tekstu;
- sistema privalo juos paversti kanoniniu struktūriniu artefaktu prieš tęsdama workflow;
- prieš taikymą turi parodyti žmogui suprantamą interpretaciją;
- aukštos rizikos atvejais būtinas aiškus vartotojo patvirtinimas.

## Vykdymo riba
- V1 sistema yra **local desktop-first**;
- oficialiai orientuota į vartotojo macOS workstation;
- architektūra turi būti pernešama tarp Mac darbo vietų;
- V1 nepasižada lygiaverčio Windows ar Linux palaikymo.

## Darbo metodas
- sistema projektuojama taip, lyg visas kodas, skriptai, dokumentacija ir workflow būtų kuriami ir vykdomi per **OpenCode** arba **Codex CLI** su ChatGPT modeliu;
- agentai negali remtis chat atmintimi kaip kanoniniu state šaltiniu;
- sprendimai turi būti atsekami per failus, skriptus ir aiškius artefaktus repo viduje;
- visi svarbūs veiksmai turi turėti CLI-first entrypointus;
- komandos turi būti aiškios, pakartojamos ir tinkamos agentiniam vykdymui;
- skriptai turi būti kuo labiau deterministiniai, idempotentiški ir turėti aiškias exit būsenas;
- promptai, workflow taisyklės ir resume logika turi gyventi versionuojamuose failuose repo viduje.

Papildomos vykdymo taisyklės:

- `manual UI-only` žingsniai turi būti vengiami, išskyrus tuos sluoksnius, kurių kitaip padaryti neįmanoma ar nenaudinga;
- išoriniai įrankiai, pvz. `Whimsical Desktop MCP`, turi būti integruojami kaip programiniai backendai, ne kaip rankinio darbo priedai;
- sistema turi būti kuriama kaip CLI-first agentinė vertimo sistema, ne kaip rankinis darbo procesas su keliais pagalbiniais skriptais.

## Nekeičiami draudimai
- negalima spėlioti terminų ar LT / ES sprendimų;
- negalima remtis vien modelio atmintimi ten, kur reikia internetinės patikros;
- negalima suplakti kanoninio LT ir mokymosi sluoksnių;
- negalima apeiti blocker'ių ar žmogaus patvirtinimo taškų;
- negalima savavališkai keisti artefaktų už role prompto rašymo paviršiaus ribų.
