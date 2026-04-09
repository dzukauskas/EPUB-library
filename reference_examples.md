# REFERENCE_EXAMPLES

## Paskirtis
Šis dokumentas laiko tik iliustracinius, nekanoninius pavyzdžius, kurie padeda:

- greičiau suprasti, kaip atrodo tipiniai artefaktai;
- turėti paruoštus sample path'us ir ID implementacijai ar testams;
- sumažinti agentų interpretacijos laisvę ten, kur naudinga pamatyti konkretų pavyzdį.

Jei šio dokumento pavyzdžiai kada nors konfliktuotų su kanoniniais dokumentais, visada laimi atitinkamas kanoninis dokumentas. Dokumentų vaidmenų, vardų ir skaitymo tvarkos klausimais laimi `document_system.md`; kitu atveju:

- `project_constitution.md`
- `product_spec.md`
- `architecture.md`
- `agent_system.md`
- `implementation_plan.md`
- `validation_plan.md`
- `open_questions.md`

## Statusas
Šis dokumentas yra:

- `illustrative`
- `non-normative`
- `implementation/reference only`

Tai reiškia:

- `003-airway`, `books/demo`, `figure-3-1-001-...` ir panašūs vardai yra tik sample duomenys;
- jie nėra užrakinti projekto identifikatoriai;
- agentai turi perimti semantiką, o ne aklai kopijuoti sample vardus į realų projektą.

## Pavyzdys: `structured_state` po `translation`
```yaml
output_type: structured_state
output_version: "1.0"
role: translation
status: needs_user_decision
execution_scope:
  scope_type: chapter
  scope_ref: 003-airway
artifacts_read:
  - path: books/demo/chapter_packs/003-airway.yaml
    artifact_type: chapter_pack
  - path: books/demo/research/003-airway.md
    artifact_type: research
artifacts_written:
  - path: books/demo/lt/chapters/003-airway.md
    artifact_type: canonical_lt_chapter
    write_mode: updated
blockers:
  - blocker_id: blocker-003-dose-conflict
    type: dose_or_algorithm_risk
    severity: high
    status: escalated
    summary: Konfliktas tarp LT ir ES atramos dėl dozavimo interpretacijos.
    requires_user_decision: true
requires_user_confirmation: true
next_step:
  step_type: wait_user_decision
  step_ref: blocker-003-dose-conflict
role_payload:
  canonical_chapter_written: true
  new_blockers_opened: 1
```

Šio pavyzdžio paskirtis:

- parodyti minimalią `structured_state` formą su realistišku blocker'iu;
- duoti vieną stabilų sample chapter identifikatorių testams ar fixtures;
- padėti greitai atpažinti, kaip atrodo `artifacts_read[]` ir `artifacts_written[]`.

## Pavyzdys: Whimsical figūros darbo erdvė
Siūlomas sample išdėstymas:

```text
Private/
  Medical Translation/
    <book_slug>/
      _shared/
      001-<chapter-slug>/
      002-<chapter-slug>/
      ...
```

Kanoninio failo vardas:

```text
figure-3-1-001-airway-fig-01 | Viršutinių kvėpavimo takų schema
```

Draft failo vardas:

```text
DRAFT | figure-3-1-001-airway-fig-01 | Viršutinių kvėpavimo takų schema
```

Šio pavyzdžio paskirtis:

- parodyti skirtumą tarp kanoninio ir draft figūros failo;
- duoti vieną konkretų `figure_id` sample;
- padėti vizualiai suprasti deterministic mapping tarp repo ir Whimsical.

## Pavyzdys: Obsidian vault struktūra vienai knygai
```text
<Vault>/Medical Books/<book_slug>/
  00 Book Home.md
  01 Chapter Index.md
  10 Canonical LT/
    001-<slug>.md
    002-<slug>.md
  20 Learning/
    001-<slug>.md
    002-<slug>.md
  30 Figures/
    figure-<id>.png
    figure-<id>.svg
```

Repo -> Obsidian sample mapping:

- `books/<slug>/lt/chapters/<chapter>.md` -> `<Vault>/Medical Books/<slug>/10 Canonical LT/<chapter>.md`
- `books/<slug>/lt/learning/<chapter>.md` -> `<Vault>/Medical Books/<slug>/20 Learning/<chapter>.md`
- `books/<slug>/lt/figures/rendered/<figure>.png` -> `<Vault>/Medical Books/<slug>/30 Figures/<figure>.png`
- `books/<slug>/lt/figures/exported/<figure>.svg` -> `<Vault>/Medical Books/<slug>/30 Figures/<figure>.svg`

Papildomi sample failai:

- `<Vault>/Medical Books/<slug>/00 Book Home.md`
- `<Vault>/Medical Books/<slug>/01 Chapter Index.md`
- `10 Canonical LT/003-airway.md`
- `20 Learning/003-airway.md`

Šio pavyzdžio paskirtis:

- padėti greitai suprasti vault navigacijos logiką;
- duoti vieną aiškų chapter pairing sample;
- suteikti testams ar prototipams vieną nuoseklų path mapping pavyzdį.

## Pavyzdys: promptų failų vardynas
Sample promptų failų rinkinys:

- `shared/prompts/base/global_system_prompt.md`
- `shared/prompts/roles/book_preparation.md`
- `shared/prompts/roles/chapter_pack.md`
- `shared/prompts/roles/research_localization.md`
- `shared/prompts/roles/translation.md`
- `shared/prompts/roles/blocker_resolution.md`
- `shared/prompts/roles/learning_block.md`
- `shared/prompts/roles/figure_pipeline.md`
- `shared/prompts/roles/qa_release.md`
- `shared/prompts/roles/obsidian_sync.md`
- `shared/prompts/resume/resume_book_preparation.md`
- `shared/prompts/resume/resume_translation.md`
- `shared/prompts/resume/resume_blocker_resolution.md`
- `shared/prompts/resume/resume_figures.md`
- `shared/prompts/resume/resume_qa.md`
- `shared/prompts/resume/resume_obsidian_sync.md`

Šio pavyzdžio paskirtis:

- duoti vieną aiškų vardyno reference implementacijai;
- padėti išvengti sinonimų ar neprognozuojamų failų vardų;
- sutrumpinti agentų laiką, kai reikia scaffold'inti promptų katalogą.

## Pavyzdys: žmogui skaitoma role išvestis
Minimalus žmogui skaitomas karkasas gali naudoti šiuos aiškius label'ius:

- `ką perskaitė`
- `ką nusprendė`
- `kokius artefaktus pakeitė arba siūlo pakeisti`
- `ar yra blocker'ių`
- `ar reikia vartotojo patvirtinimo`
- `koks kitas žingsnis`

Šio pavyzdžio paskirtis:

- duoti vieną stabilų žmogui skaitomos role išvesties reference;
- sumažinti riziką, kad agentai tą patį semantinį bloką pavadins vis kitu vardu;
- palengvinti review ir CLI orchestration sluoksnio interpretaciją.

## Pavyzdys: blocker escalation paketas žmogui
Jei reikia parodyti blocker'į žmogui sprendimui, sample laukai gali būti:

- `blocker_id`
- `problemos tipas`
- `trumpa esmė`
- `kur tai rasta`
- `koks dabar siūlomas LT variantas / sprendimas`
- `kokie 2–3 alternatyvūs variantai`
- `kokie LT šaltiniai rasti`
- `kokie ES šaltiniai rasti`
- `sistemos rekomendacija`
- `kas pasikeis, jei pasirinksi A/B/C`

Šio pavyzdžio paskirtis:

- parodyti vieną aiškų escalation packet label'ų rinkinį;
- padėti suvienodinti blocker review UI ar CLI pranešimus;
- išlaikyti žmogui sprendžiamų situacijų struktūrą.

## Pavyzdys: loginiai sprendimo flag'ai
Sample būsenos / sprendimo išraiškos:

- `can_global_lock = true`
- `can_global_lock = false`
- `release_state = not_ready`
- `release_state = release_candidate`
- `obsidian_sync_status = outdated_synced_copy`
- `freshness_status = stale_review`

Šio pavyzdžio paskirtis:

- turėti vieną reference formą fixtures ir debug išvestims;
- padėti aiškiai atskirti release, sync ir freshness signalus;
- duoti sample loginio sprendimo žymėjimą, nepaverčiant jo papildoma kanonine schema.

## Pavyzdys: sidecar `.meta.yaml`
Sample poros:

- `lt/chapters/003-airway.md`
- `lt/chapters/003-airway.meta.yaml`
- `shared/terminology/global_concepts.tsv`
- `shared/terminology/global_concepts.meta.yaml`

Sample turinys:

```yaml
schema_type: canonical_lt_chapter_meta
schema_version: 1.0
artifact_path: books/demo/lt/chapters/003-airway.md
artifact_fingerprint: sha256:demo-fingerprint
```

Šio pavyzdžio paskirtis:

- duoti vieną konkretų sidecar pavyzdį agentams ir fixture'ams;
- parodyti, kaip atrodytų `schema_version: 1.0` lygio metadata sample;
- išlaikyti sample kelią tarp markdown artefakto ir jo sidecar failo.

## Vendor reference pastabos
Ši sekcija nėra normatyvinė. Ji skirta laikyti tikslesnius vendor-specific reference punktus, kurie anksčiau gyveno monolite.

### EPUBLib reference
- Dokumentacijos pavyzdžiuose matomas `EPUB.reset_toc(..., spine_only=True)` kelias TOC perstatymui pagal spine tvarką.
- `BookManifest.get(..., ignore_fragment=True)` dokumentuoja fragmentų ignoravimo lookup elgseną.
- Šių detalių architektūrinė išvada šiame projekte: chaptering negali remtis vien lookup default'ais, nes reikia išlaikyti ir pilną `filename#fragment`, ir normalizuotą kelią.

Nuorodos:
- [EPUBLib API](https://epub-lib.readthedocs.io/en/latest/epublib.html)
- [EPUBLib Manifest API](https://epub-lib.readthedocs.io/en/latest/epublib.package.manifest.html)

### Whimsical reference
- `Whimsical` neturi bendro tiesioginio board importo; oficialūs keliai yra image upload, text -> `mind map` / `stack`, ir Mermaid importas.
- Mermaid importui oficialiai palaikomi `graph`, `flowchart`, `sequenceDiagram`.
- Board eksportui pagrindinis kelias yra `PNG`, `PDF` gaunamas per `Print`, o `SVG` kelias yra eksperimentinis.
- Dabartiniai oficialūs export docs aprašo `selection`, `whole board` arba `separate frames` eksportą ir `1x` arba `2x` dydžio pasirinkimą; aiškiai nurodytas `Free` plano ribojimas šiame reference taške yra `Made with Whimsical` watermark'as ant eksportuotų paveikslų.
- Desktop / workspace sluoksnis nėra `offline-first`, todėl preflight turi tikrinti prisijungimą ir pasiekiamumą.

Nuorodos:
- [Whimsical Importing](https://help.whimsical.com/imports-exports/importing)
- [Whimsical Exporting](https://help.whimsical.com/imports-exports/exporting-from-whimsical)
- [Whimsical Desktop App FAQ](https://help.whimsical.com/faqs/desktop-app)

## Legacy string bankas
Ši sekcija skirta tik migracijos traceability, fixture'ams ir string-level testams. Ji nėra taisyklių šaltinis.

Sample tokenai ir vardai:

- `chapter map`
- `figure_spec`
- `global_concepts`
- `claim-level`
- `decision artifacts`
- `draft`
- `ignore_fragment`
- `reset_toc(..., spine_only=True)`
- `can_global_lock =`
- `Medical Books/`
- `Medical Translation/`
- `<book_slug>`
- `<book_slug>/`
- `003-airway.md`
- `figure-3-1-001-airway-fig-01 | Viršutinių kvėpavimo takų schema`
- `figure-3-1-001-first-chapter-fig-01.png`
- `resume_book_preparation.md`
- `resume_translation.md`
- `resume_blocker_resolution.md`
- `resume_figures.md`
- `resume_qa.md`
- `resume_obsidian_sync.md`

Section label reference'ai:

- `1. Rolė ir misija`
- `2. Kanoninė tiesa ir būsenos atkūrimas`
- `3. Produkto sluoksnių modelis`
- `4. Lokalizacijos politika`
- `5. Terminų politika`
- `6. Blocker'ių ir review politika`
- `7. Žmogaus sprendimų interpretavimo taisyklė`
- `8. Darbo ribos ir vykdymo aplinka`
- `9. Artefaktų ir priklausomybių taisyklė`
- `10. Stiliaus ir elgesio draudimai`
- `11. Privalomas darbo modelis prieš vykdymą`
- `1. Skyriaus esmė`
- `2. Svarbiausi terminai`
- `3. Pagrindinė logika / mechanizmas`
- `4. Paaiškinamieji pavyzdžiai`
- `5. Ką būtina atsiminti`
- `6. Savikontrolės klausimai`

## Kaip naudoti šį dokumentą
- naudok jį kaip sample banką implementacijai, prototipams ir fixtures;
- jei reikia kurti testinius duomenis, pradėk nuo čia, o ne nuo improvizacijos;
- jei reikia spręsti kanoninę taisyklę, grįžk į atitinkamą pagrindinį dokumentą;
- jei pavyzdys pasensta, jį galima atnaujinti nekeičiant jokios kanoninės politikos.

## Ko šis dokumentas neturi daryti
- kurti naujų produkto ar architektūros taisyklių;
- tapti antru `architecture.md` ar `agent_system.md`;
- perrašyti kanoninius dokumentus savo pavyzdžiais;
- vėl kaupti visą projektą į vieną „lengviau skaityti“ super dokumentą.
