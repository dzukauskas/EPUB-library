# DOCUMENT_SYSTEM

## Paskirtis
Šis dokumentas apibrėžia:
- kokie dokumentai sudaro projekto dokumentų sistemą;
- koks yra kiekvieno dokumento vaidmuo;
- kokia yra dokumentų tarpusavio prioritetų tvarka;
- kaip spręsti likusius dubliavimus ar senesnių vardų pėdsakus.

Jis turi būti laikomas kanoniniu „kaip skaityti dokumentaciją“ žemėlapiu.

---

## 1. Dokumentų sistema

Šiuo metu projektą sudaro šie pagrindiniai dokumentai:

### Frozen core
1. `PROJECT_CONSTITUTION.md`
2. `PRODUCT_SPEC.md`

### Working design
3. `ARCHITECTURE.md`
4. `AGENT_SYSTEM.md`
5. `IMPLEMENTATION_PLAN.md`
6. `OPEN_QUESTIONS.md`
7. `VALIDATION_PLAN.md`

### Reference layer
8. `REFERENCE_EXAMPLES.md`

Šis sąrašas apibrėžia vienintelę norminę projekto dokumentų sistemą. Root `docs/` subtree, jei vėliau naudojamas, nelaikomas lygiaverčiu norminių dokumentų sluoksniu ir negali dubliuoti šių failų ar kanoninio workflow state.

---

## 2. Dokumentų paskirtys

### `PROJECT_CONSTITUTION.md`
Trumpas beveik nekintantis branduolys.

Jame turi gyventi tik:
- projekto misija;
- kanoninės tiesos taisyklė;
- dviejų sluoksnių modelis;
- LT / ES-first logika;
- aukšto lygio draudimai;
- vykdymo ribos.

Jei taisyklė pakankamai aukšto lygio ir beveik nekintama, ji turi gyventi čia.

### `PRODUCT_SPEC.md`
Produkto taisyklės.

Jame turi gyventi:
- ką sistema gamina;
- kaip atrodo galutiniai produktiniai sluoksniai;
- terminų, lokalizacijos, mokymosi bloko ir Obsidian produktinės taisyklės.

Jei taisyklė atsako į klausimą „ką turi gauti vartotojas ir pagal kokias produkto taisykles“, ji turi gyventi čia.

### `ARCHITECTURE.md`
Techninė architektūra.

Jame turi gyventi:
- repo struktūra;
- artefaktai;
- būsenų mašina;
- ingest architektūra;
- terminų engine;
- figūrų pipeline;
- priklausomybių grafas;
- schema/versioning.

Jei klausimas yra „kaip sistema sukonstruota techniškai“, jis turi gyventi čia.

### `AGENT_SYSTEM.md`
Promptų ir agentinio vykdymo architektūra.

Jame turi gyventi:
- globalus promptas;
- role promptai;
- resume promptai;
- `structured_state`;
- decision artifact modelis;
- siauro rašymo paviršiaus taisyklės.

Jei klausimas yra „kaip turi mąstyti ir komunikuoti agentai“, jis turi gyventi čia.

### `IMPLEMENTATION_PLAN.md`
Statybos seka.

Jame turi gyventi:
- fazės;
- bangos;
- kas statoma pirma;
- kada sistema laikoma pilnai veikiančia v1.

Jei klausimas yra „kokia tvarka viską statyti“, jis turi gyventi čia.

### `OPEN_QUESTIONS.md`
Tik dar neuždaryti klausimai.

Jei klausimas jau išspręstas, jis čia nebeturi gyventi.

### `VALIDATION_PLAN.md`
Tik acceptance / validation korpusas ir patikimumo slenkstis.

Jei turinys nėra apie testinį korpusą, edge case'us ar validation kriterijus, jis neturi gyventi čia.

### `REFERENCE_EXAMPLES.md`
Iliustraciniai, nekanoniniai pavyzdžiai.

Jame gali gyventi:
- sample path'ai;
- sample artefaktų išvestys;
- sample failų vardynas;
- vieno scenarijaus reference pavyzdžiai.

Jame neturi gyventi:
- naujos normatyvinės taisyklės;
- kanoninių dokumentų pakaitalai;
- turinys, kuris prieštarauja pagrindiniams dokumentams.

---

## 3. Dokumentų prioritetų tvarka

Jei ateityje tarp dokumentų atsirastų persidengimų ar formuluočių skirtumų, taikoma ši prioritetų tvarka:

1. `PROJECT_CONSTITUTION.md`
2. `PRODUCT_SPEC.md`
3. `ARCHITECTURE.md`
4. `AGENT_SYSTEM.md`
5. `IMPLEMENTATION_PLAN.md`
6. `VALIDATION_PLAN.md`
7. `OPEN_QUESTIONS.md`

Tai reiškia:
- aukštesnis dokumentas laimi prieš žemesnį;
- `OPEN_QUESTIONS.md` niekada negali perrašyti jau užrakintos taisyklės iš aukštesnio dokumento;
- `VALIDATION_PLAN.md` negali keisti produkto ar architektūros taisyklių, jis tik tikrina jų patikimumą.

`REFERENCE_EXAMPLES.md` nėra šios prioritetų grandinės dalis. Jis negali perrašyti nė vieno aukščiau esančio dokumento ir turi būti laikomas tik pagalbiniu reference sluoksniu.

---

## 4. Kaip spręsti likusius dubliavimus

### 4.1. `PROJECT_CONSTITUTION.md` ir `PRODUCT_SPEC.md`
Jei kažkas aprašyta abiejuose dokumentuose:
- `PROJECT_CONSTITUTION.md` turi laikyti tik aukščiausio lygio trumpą principą;
- `PRODUCT_SPEC.md` gali laikyti detalesnę produkto taisyklę.

Taisyklė:
- **Constitution = principas**
- **Product Spec = detalizuota produkto taisyklė**

### 4.2. `ARCHITECTURE.md` ir `AGENT_SYSTEM.md`
Jei tema susijusi su agentais:
- techniniai vykdymo artefaktai ir state modelis gyvena `ARCHITECTURE.md`;
- promptų, I/O ir agentinio elgesio taisyklės gyvena `AGENT_SYSTEM.md`.

### 4.3. `IMPLEMENTATION_PLAN.md`
Jis neturi tapti nei produkto taisyklių, nei architektūros pakaitalu.
Jis tik aprašo statybos seką.

---

## 5. Senų vardų ir likusių pėdsakų taisyklė

Jei kur nors dokumentuose dar liktų senesni ar netikslūs vardai, galioja šios kanoninės atitikties taisyklės:

- `PROJECT_SPEC.md` reikia laikyti pakeistu į `PRODUCT_SPEC.md`
- `WORKFLOW.md` reikia laikyti išskaidytu į:
  - `AGENT_SYSTEM.md`
  - `IMPLEMENTATION_PLAN.md`
  - ir dalinai į `PROJECT_CONSTITUTION.md` / `PRODUCT_SPEC.md`, priklausomai nuo turinio

Tai reiškia:
- jei kur nors liktų senas vardas, agentai neturi jo interpretuoti kaip atskiro naujo dokumento;
- reikia remtis šiuo dokumentu kaip vardų ir vaidmenų kanonine lentele.

---

## 6. Kaip agentai turi skaityti dokumentaciją

### Minimalus skaitymo kelias prieš rimtą darbą
1. `PROJECT_CONSTITUTION.md`
2. `PRODUCT_SPEC.md`
3. pagal poreikį:
   - `ARCHITECTURE.md`
   - `AGENT_SYSTEM.md`
   - `IMPLEMENTATION_PLAN.md`
4. tik tada:
   - `OPEN_QUESTIONS.md`, jei tema dar neuždaryta;
   - `VALIDATION_PLAN.md`, jei kalbama apie acceptance / patikimumą.
5. pasirinktinai:
   - `REFERENCE_EXAMPLES.md`, jei reikia konkretaus sample path'o, sample YAML ar sample failų vardyno.

### Kodėl taip
Nes agentas pirmiausia turi suprasti:
- projekto misiją,
- produkto taisykles,
- o tik po to techninę ir agentinę realizaciją.

---

## 7. Ko šis dokumentas neturi daryti

Jis neturi:
- dubliuoti visos architektūros;
- perrašyti produkto taisyklių;
- tapti nauju „milžinišku super dokumentu“;
- laikyti atvirų klausimų ar validation scenarijų detalių;
- paversti `REFERENCE_EXAMPLES.md` nauju pusiau-kanoniniu taisyklių centru.
- leisti root `docs/` subtree tyliai virsti antru norminių taisyklių ar workflow state sluoksniu.

Jo vienintelė paskirtis:
- **užrakinti dokumentų sistemos logiką, roles ir prioritetus**.

---

## 8. Praktinė taisyklė tolimesniam darbui

Jei ateityje keičiamas ar papildomas bet kuris dokumentas, pirmiausia reikia klausti:

1. ar tai yra aukšto lygio principas?
2. ar tai yra produkto taisyklė?
3. ar tai yra techninė architektūra?
4. ar tai yra agentų vykdymo logika?
5. ar tai yra statybos planas?
6. ar tai tik atviras klausimas?
7. ar tai validation / acceptance klausimas?
8. ar tai tik iliustracinis pavyzdys / reference?

Tik tada sprendžiama, į kurį dokumentą pokytis turi keliauti.

Tai padės išvengti naujų dubliavimų ir dokumentacijos išsikraipymo.
