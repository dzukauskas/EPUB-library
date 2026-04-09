# ARCHITECTURE

## Paskirtis
Šis dokumentas fiksuoja techninę projekto architektūrą: repo struktūrą, artefaktus, būsenų mašiną, ingest, terminų engine, figūrų pipeline, schemas, versijavimą ir priklausomybių logiką.

## Repo struktūra v1
Žemiau pateiktas medis aprašo target v1 scaffold, o ne teigia, kad visas jis jau materializuotas dabartiniame working tree. Dabartiniai root norminiai dokumentai šiame repo jau egzistuoja nurodytais tikrais failų vardais, o likusi medžio dalis yra v1 statomas karkasas.

```text
repo/
  README.md
  AGENTS.md
  PLANS.md
  project_constitution.md
  product_spec.md
  architecture.md
  document_system.md
  agent_system.md
  implementation_plan.md
  open_questions.md
  validation_plan.md
  reference_examples.md
  pyproject.toml
  uv.lock
  .python-version
  repo_config.example.toml
  repo_config.local.toml         # gitignored

  shared/
    terminology/
      global_concepts.tsv
      global_variants.tsv
      acronym_policy.tsv
    localization/
      source_priority.yaml
      lt_source_map.yaml
      risk_policy.yaml
    learning/
      learning_block_schema.yaml
      examples_policy.yaml
    prompts/
      base/
      roles/
      resume/
    schemas/
      book_profile.schema.yaml
      epubcheck_summary.schema.yaml
      chapter_pack.schema.yaml
      blocker.schema.yaml
      figure_spec.schema.yaml
      decision_artifact.schema.yaml
      structured_state.schema.yaml

  books/
    <book_slug>/
      book.yaml
      chapter_map.yaml
      decisions/
      migrations/

      source/
        epub/
          source.epub
        index/
          chapters.json
          chapters.md
          toc_review.yaml
          epubcheck_report.raw.json
          epubcheck_summary.yaml
          figures.tsv
          figures.meta.yaml
        chapters-en/
          <slug>.md
          <slug>.meta.yaml
        figures-raw/

      research/
        <slug>.md
      claims/
        <slug>.yaml
      blockers/
        <slug>.yaml
      chapter_packs/
        <slug>.yaml

      lt/
        chapters/
          <slug>.md
          <slug>.meta.yaml
        learning/
          <slug>.md
          <slug>.meta.yaml
        figures/
          manifest.tsv
          manifest.meta.yaml
          specs/
            figure-<id>.yaml
          rendered/
            figure-<id>.png
            figure-<id>.meta.yaml
          exported/
            figure-<id>.svg
            figure-<id>.meta.yaml

      terms/
        candidates.tsv
        local_concepts.tsv
        local_variants.tsv

      qa/
        chapter_status.tsv
        dependency_index.yaml
        reports/

      obsidian/
        sync_manifest.yaml

  src/
    medtranslate/
      config/
      epub_ingest/
      chaptering/
      terminology/
      localization/
      translation/
      learning/
      figures/
      qa/
      obsidian/
      prompts/
      cli/

  scripts/
  tests/
    fixtures/
```

### Kanoninė chapter-scoped failų vardyno taisyklė v1
- `chapter_slug` yra loginis skyriaus identifikatorius be numerio prefikso, pvz. `airway`.
- `chapter_number` yra atskiras struktūrinis laukas kanoniniuose artefaktuose ir nėra chapter-scoped failo stem dalis.
- Kanoninis repo ir Obsidian chapter-scoped on-disk file stem v1 yra `<chapter_slug>`.
- Todėl šiame dokumente tokie keliai kaip `source/chapters-en/<slug>.md`, `research/<slug>.md`, `claims/<slug>.yaml`, `blockers/<slug>.yaml`, `chapter_packs/<slug>.yaml`, `lt/chapters/<slug>.md` ir `lt/learning/<slug>.md` reiškia realų on-disk failo vardą su tuo pačiu `chapter_slug`.
- Išoriniai vendor ar workspace organizavimo sluoksniai gali naudoti kitą aplankų vardyną, jei tai tame sluoksnyje aprašyta atskirai; ši taisyklė užrakina tik repo ir Obsidian chapter-scoped failų vardus.

### Ką reiškia ši struktūra
#### Root lygis
- `AGENTS.md` — repo-local agent entrypoint ir darbo ribų priminimas.
- `PLANS.md` — repo-local ExecPlan standartas.
- `project_constitution.md` — aukščiausio lygio projekto branduolys ir nekintamos taisyklės.
- `product_spec.md` — detalizuotos produkto taisyklės.
- `architecture.md` — techninė architektūra.
- `document_system.md` — dokumentų sistemos žemėlapis, prioritetai ir vardų atitiktis.
- `agent_system.md` — promptų, role promptų, resume promptų ir agentinio I/O architektūra.
- `implementation_plan.md` — statybos seka ir įgyvendinimo bangos.
- `open_questions.md` — tik dar neuždaryti klausimai.
- `validation_plan.md` — acceptance / validation korpusas ir patikimumo slenkstis.
- `reference_examples.md` — iliustraciniai, nekanoniniai pavyzdžiai.
- `pyproject.toml` + `uv.lock` — naujo projekto Python bazė. Numatoma Python 3.13+ kryptis, nes EPUB sluoksnis planuojamas ant `EPUBLib`.
- `repo_config.local.toml` — workstation-specific konfigūracija, pvz. Obsidian `vault` keliai. Ji neturi būti kanoninė projekto būsena.

#### `shared/`
Čia gyvena viskas, kas turi būti reusable tarp knygų:

- globalus sąvokomis grįstas terminų sluoksnis;
- LT / ES šaltinių prioritetai;
- rizikos politika;
- mokymosi bloko schema;
- agentų promptai ir schemos.

#### `docs/`
Jei root `docs/` subtree vėliau naudojamas, jis laikomas tik pagalbiniu repo-engineering / support sluoksniu.

Taisyklės:

- jis negali dubliuoti ar perrašyti top-level norminių dokumentų iš šio repo;
- `docs/decisions/`, jei naudojamas, gali laikyti tik repo-engineering ADR ar pagalbines pastabas, bet ne kanoninį produkto / workflow / book state sprendimų sluoksnį;
- kanoniniai workflow sprendimai visada gyvena `books/<book_slug>/decisions/<decision_id>.yaml`;
- `docs/policies/`, jei naudojamas, negali tapti alternatyviu produkto, lokalizacijos ar rizikos politikų source-of-truth šalia jau užrakintų norminių failų ir `shared/` artefaktų.

#### `books/<book_slug>/`
Čia gyvena visa konkrečios knygos kanoninė būsena.

##### `book.yaml`
Knygos lygio profilis / paruošimo failas. Čia turi gyventi:

- knygos tema ir paskirtis;
- preliminarus rizikos žemėlapis;
- pasikartojančių terminų branduolys;
- tikėtini LT / ES konfliktų tipai;
- knygai būdingos lokalizacijos taisyklės;
- atviri knygos lygio klausimai.

##### `chapter_map.yaml`
Kanoninis patvirtintas skyriaus žemėlapis po review. V1 siūlomas `chapter_map` negyvena šiame faile: jis turi būti laikomas `source/index/toc_review.yaml`, kol segmentacija dar nepatvirtinta.

##### `source/`
Originalo ir ingest artefaktų sluoksnis:

- originalus EPUB;
- aptikto skyrių žemėlapio indeksai;
- `chapters-en/` kaip darbo navigacijos sluoksnis;
- raw figūrų inventory.

##### `research/`
Skyriaus lygio tyrimo ir lokalizacijos sprendimų sluoksnis.

##### `claims/`
Tik aukštos rizikos turinio claim-level atramai.

##### `blockers/`
Atskiras blocker'ių sluoksnis kiekvienam skyriui. Čia gyvena:

- blockerio tipas;
- rizikos lygis;
- rasti LT / ES šaltiniai;
- siūlomas sprendimas;
- būsena;
- ar reikalinga eskalacija vartotojui.

##### `chapter_packs/`
Prieš vertimą sugeneruotas vykdomas skyriaus preflight artefaktas.

##### `lt/chapters/`
Kanoninis LT sluoksnis.

##### `lt/learning/`
Atskiras mokymosi blokas. Jis negali būti tame pačiame faile kaip kanoninis LT skyrius.

##### `lt/figures/`
Figūrų kanoninis lietuviškas sluoksnis:

- `manifest.tsv`;
- tekstiniai figūrų spec failai;
- renderintos išvestys;
- pasirenkamos papildomos eksportuotos versijos.

##### `terms/`
Knygos lygio terminų sluoksnis:

- kandidatai;
- lokalios sąvokos;
- lokalūs variantai.

##### `qa/`
Kanoninio chapter execution registry, dependency freshness indekso ir QA ataskaitų sluoksnis.

##### `obsidian/`
Tik sync pagalbinis sluoksnis, ne kanoninis šaltinis.

### Pagrindiniai architektūriniai principai, įtvirtinti struktūroje
1. **Globalu vs lokalus**

- `shared/` — globalios reusable taisyklės;
- `books/<slug>/` — konkrečios knygos vykdymo būsena.

2. **Kanoninis vs mokymosi sluoksnis**

- `lt/chapters/` — kanoninis LT tekstas;
- `lt/learning/` — mokymosi sluoksnis;
- jie negali būti suplakti.

3. **Research / claims / blockers yra atskiri sluoksniai**

- ne viskas turi gyventi viename `research` faile;
- aukštos rizikos atrama, blockeriai ir skyrių tyrimas turi būti aiškiai atskirti.

4. **Figūros turi savo atskirą pipeline**

- figūros nėra tik skyriaus priedas;
- jos turi turėti kanoninį spec sluoksnį ir atskirą render kelią.

5. **Repo yra vienintelis kanoninis šaltinis**

- `Obsidian` yra vienakryptė sinchronizuota skaitymo ir mokymosi aplinka, kurioje saugomi abu sluoksniai: kanoninis LT skyrius ir mokymosi blokas;
- `Whimsical MCP` yra schemų ir diagramų render / edit backendas, o raster paveikslėliams su tekstu naudojamas atskiras lokalizacijos backendas; nė vienas iš jų nepakeičia repo kaip kanoninės tiesos.

### Kodėl ši struktūra logiška būtent šitam projektui
Ši struktūra leidžia:

- dirbti po vieną skyrių;
- turėti aiškų knygos lygio profilį;
- kaupti globalią terminiją tarp knygų;
- atskirti kanoninį LT vertimą nuo mokymosi bloko;
- turėti pilną blocker'ių sprendimo ciklą be chat atminties;
- leisti OpenCode / Codex CLI agentams dirbti deterministiškai per failus ir CLI entrypointus.

## Kanoniniai artefaktai
Šiame dokumente atskiriamos dvi skirtingos klasifikavimo ašys:

- `kanoninis` = repo source-of-truth tame scope;
- `materializuojamas` = artefaktas generuojamas, perrašomas ar perrefreshinamas iš upstream įėjimų ir todėl turi freshness / dependency logiką.

Svarbi taisyklė:

- artefaktas gali būti kanoninis ir kartu materializuojamas; `materializuojamas` šiame dokumente nereiškia `nekanoninis`.

### Pirminiai kanoniniai artefaktai
- `book.yaml`
- `chapter_map.yaml`
- `research/<slug>.md`
- `claims/<slug>.yaml`
- `shared/terminology/global_concepts.tsv`
- `shared/terminology/global_variants.tsv`
- `books/<slug>/terms/local_concepts.tsv`
- `books/<slug>/terms/local_variants.tsv`
- `books/<slug>/decisions/*.yaml`
- `lt/figures/specs/<id>.yaml`

### Kanoniniai, bet materializuojami artefaktai
- `source/index/toc_review.yaml`
- `source/index/figures.tsv`
- `chapter_packs/*.yaml`
- `blockers/*.yaml`
- `lt/chapters/*.md`
- `lt/learning/*.md`
- `lt/figures/manifest.tsv`
- `qa/chapter_status.tsv`

Šie artefaktai lieka kanoniniai savo workflow ar produkto scope, nors jie materializuojami iš upstream įėjimų ir gali būti pažymėti kaip `stale_*` pagal priklausomybių taisykles.

### Pagalbiniai materializuojami artefaktai
- `source/index/chapters.json`
- `source/index/chapters.md`
- `source/index/epubcheck_report.raw.json`
- `source/index/epubcheck_summary.yaml`
- `source/chapters-en/*.md`
- `lt/figures/rendered/*`
- `lt/figures/exported/*`
- `obsidian/sync_manifest.yaml`

## Kanoninių artefaktų detalus semantinis kontraktas
Ši dalis apibrėžia ne galutinę sintaksę, o kokią informaciją privalo turėti kiekvienas artefaktas. Tikslas yra pirmiausia užfiksuoti semantinį kontraktą, o tik po to galutinai apsispręsti dėl `yaml`, `json` ar `tsv` formų.

### `book.yaml`
Knygos lygio profilis.

Privalomi laukai:

- `book_id`
- `book_slug`
- `title_en`
- `source_type` (`epub`)
- `source_path`
- `status` (`source_added`, `preparation_running`, `prepared_waiting_chapter_map_review`, `prepared_waiting_translation_permission`, `active_translation`, `book_blocked`, `completed`) — kanoninis `book_state` laukas
- `domain_tags[]`
- `risk_profile`
- `approved_chapter_map_version`

Papildomi / sąlyginiai laukai:

- `title_lt_working`
- `edition_label`, jei aktualu
- `expected_lt_eu_conflicts[]`
- `core_repeating_concepts[]`
- `book_specific_localization_rules[]`
- `open_book_level_questions[]`
- `last_preparation_review_at`
- `notes`, jei reikia

Paskirtis:

- būti vieninteliu knygos lygio paruošimo ir konteksto artefaktu;
- būti automatiškai atnaujinamam tik tada, kai realiai pasikeičia knygos lygio žinios.

Minimalus v1 techninis kontraktas:

- `risk_profile` yra privalomas objektas, ne laisva prose pastaba;
- minimalus v1 `risk_profile` shape:
  - `overall_level` (`low`, `mixed`, `high`)
  - `risk_drivers[]`
- `risk_drivers[]` saugo tik normalizuotus book-level rizikos signalus:
  - `algorithms`
  - `medications_and_doses`
  - `indications_and_contraindications`
  - `competency_boundaries`
  - `guideline_dependent_content`
  - `jurisdiction_specific_content`
  - `legal_organizational_requirements`
- `risk_drivers[]` gali būti `[]`, jei knygos lygio preliminarus rizikos žemėlapis dar nerodo specifinių driver'ių;
- `approved_chapter_map_version` yra privalomas sveikasis skaičius `>= 0`;
- kol dar neegzistuoja joks approved `chapter_map.yaml`, `approved_chapter_map_version = 0`;
- jei `prepare-book` materializuoja approved `chapter_map.yaml` tiesiogiai be atskiro review etapo, to paties apply metu jis turi nustatyti `approved_chapter_map_version = 1`;
- kiekvienas vėlesnis sėkmingai pritaikytas `review-chapter-map approve|revise` sprendimas, kuris materializuoja ar atnaujina approved `chapter_map.yaml`, turi padidinti `approved_chapter_map_version` lygiai per `+1`.

### `chapter_map.yaml`
Kanoninis skyrių žemėlapis po review.

Privalomi vienetai kiekvienam skyriui:

- `chapter_number`
- `chapter_slug`
- `title_en`
- `source_segments[]`
- `source_strategy`
- `segmentation_confidence`
- `needs_manual_review`

Papildomi / sąlyginiai laukai:

- `title_lt_working`, jei jau nustatytas
- `start_anchor` arba atitinkamas source start point, jei to reikalauja pasirinkta segmentavimo strategija
- `end_anchor`, jei reikia pagal naudojamą `source_strategy`
- `notes`
- `review_flags[]`, jei review metu reikia papildomų žymų

Paskirtis:

- būti vieninteliu kanoniniu skyriaus segmentacijos šaltiniu prieš vertimą;
- neleisti pradėti 1 skyriaus ar kito skyriaus darbo ant nepatvirtinto segmentavimo.

Papildomas kontraktas:

- `chapter_map.yaml` yra tik approved artefaktas ir negali būti naudojamas proposal būsenai;
- top-level `status` laukas šiame artefakte nenaudojamas; approved segmentacijos būsena apibrėžiama tuo, kad egzistuoja pats `chapter_map.yaml`, o workflow/proposal būsenos lieka `book.yaml.status` ir `source/index/toc_review.yaml.proposal_status`;
- jei segmentacija dar laukia review, siūlomas artefaktas turi gyventi `source/index/toc_review.yaml`, o ne kaip "siūlomas `chapter_map.yaml`".

### `source/index/toc_review.yaml`
`chapter_map` review proposal artefaktas prieš approval.

Privalomi top-level laukai:

- `book_slug`
- `proposal_status` (`pending_review`, `resolved`)
- `proposed_chapters[]`

Privalomi vienetai kiekvienam `proposed_chapters[]`:

- `chapter_number`
- `chapter_slug`
- `title_en`
- `source_segments[]`
- `source_strategy`
- `segmentation_confidence`
- `needs_manual_review`
- `review_flags[]`

Papildomi / sąlyginiai laukai:

- `title_lt_working`, jei jau nustatytas
- `start_anchor` arba atitinkamas source start point, jei to reikalauja pasirinkta segmentavimo strategija
- `end_anchor`, jei reikia pagal naudojamą `source_strategy`
- `notes`

Paskirtis:

- būti vieninteliu persisted `chapter_map` pasiūlymo artefaktu v1;
- saugoti review reikšmingus confidence ir `review_flags[]` signalus tol, kol segmentacija dar nepatvirtinta.

Papildomas kontraktas:

- `prepare-book` rašo šį failą tik tada, kai `chapter_map` dar reikia vartotojo review;
- `review-chapter-map approve|revise` iš šio artefakto materializuoja approved `chapter_map.yaml` ir pažymi proposal kaip `resolved`;
- kol `proposal_status = pending_review`, downstream workflow negali traktuoti `proposed_chapters[]` kaip patvirtinto `chapter_map`;
- v1 neegzistuoja atskira "siūlomo `chapter_map.yaml`" būsena ar failo režimas.

### Bendras `source_segments[]` item modelis v1
Šis kontraktas vienodai taikomas:

- `chapter_map.yaml.chapters[]`
- `source/index/toc_review.yaml.proposed_chapters[]`
- `chapter_packs/<slug>.yaml`

`source_segments[]` v1 visada saugo objektus, ne raw string'us.

Kiekvienas `source_segments[]` vienetas turi bent:

- `href`
- `normalized_path`

Papildomi / sąlyginiai laukai:

- `start_anchor`
- `end_anchor`

Semantika:

- `href` saugo tikslų originalo target reference ta pačia logine forma, kuria jis buvo identifikuotas ingest metu; jei originalas remiasi fragmentu, čia išlaikomas pilnas `filename#fragment`, o ne tik failo vardas;
- `normalized_path` saugo to paties resurso fragmentų neturintį normalizuotą kelią, naudojamą matching, grouping ir konfliktų tikrinimui;
- `start_anchor` ir `end_anchor` šiame item modelyje naudojami tik tada, kai konkretus segmentas prasideda ar baigiasi resurso viduje pagal anchor / heading ribą; jei segmentas apima visą resursą be vidinės ribos, šie laukai gali būti absent;
- masyvo eiliškumas yra kanoninė skaitymo tvarka ir negali būti permaišomas vien dėl kosmetikos;
- top-level `start_anchor` ir `end_anchor` laukai `chapter_map.yaml` ir `source/index/toc_review.yaml` lieka tik pasirenkami chapter-level boundary mirror laukai; jei jie pateikti, jie turi sutapti su pirmo ir paskutinio `source_segments[]` item atitinkamais anchor signalais ir negali jiems prieštarauti;
- `chapter_packs/<slug>.yaml.source_segments[]` pernaudoja tą pačią struktūrą be papildomo transformavimo ar alternatyvaus formato.

### `source/index/epubcheck_summary.yaml`
Pagalbinis source/ingest validation artefaktas, apibendrinantis `EPUBCheck` rezultatą.

Privalomi top-level laukai:

- `book_slug`
- `source_path`
- `source_fingerprint`
- `tool_name`
- `tool_version`
- `ran_at`
- `status` (`passed`, `passed_with_review_flags`, `blocked`)
- `counts`
- `workflow_impact`
- `findings[]`

Privalomi laukai `counts` bloke:

- `blocking`
- `review_flag`
- `warning`

Privalomi laukai `workflow_impact` bloke:

- `prepare_book_allowed`
- `requires_manual_review`
- `should_open_technical_blocker`

Privalomi laukai kiekvienam `findings[]` vienetui:

- `finding_code`
- `original_severity`
- `normalized_class` (`blocking`, `review_flag`, `warning`)
- `summary`
- `workflow_impact`

Privalomi laukai `findings[].workflow_impact` bloke:

- `prepare_book_allowed`
- `requires_manual_review`
- `should_open_technical_blocker`

Papildomi / sąlyginiai laukai:

- `location`, jei `EPUBCheck` grąžina pakankamai aiškų target reference

Paskirtis:

- būti vieninteliu normalizuotu `EPUBCheck` summary artefaktu v1;
- leisti `prepare-book` ir validation sluoksniui remtis stabilia struktūra, o ne raw tool teksto parsingu;
- saugoti knygos lygio source validation signalus neperimant `book.yaml`, `chapter_map.yaml` ar `qa/chapter_status.tsv` atsakomybės.

Papildomas kontraktas:

- šis artefaktas yra source-level pagalbinis validation sluoksnis, o ne nauja centrinė workflow state ašis;
- jis turi būti materializuojamas `prepare-book` metu po sėkmingo `EPUBCheck` paleidimo;
- `review_flag` radiniai negali likti tik šiame faile, jei jie daro įtaką segmentacijos patikimumui; jie turi būti perkelti į ingest / `chapter_map` review signalus;
- `blocking` radiniai gali būti pakankamas pagrindas atidaryti techninį blocker'į;
- top-level `workflow_impact` yra agreguotas loginis visų `findings[].workflow_impact` blokų OR rezultatas po normalizacijos;
- `findings[].workflow_impact` naudoja tą patį trijų loginių laukų shape kaip top-level blokas, bet jo semantika yra lokali konkrečiam radiniui:
  - `prepare_book_allowed` rodo, ar vien šis radinys leidžia tęsti `prepare-book`;
  - `requires_manual_review` rodo, ar vien šis radinys turi būti perneštas į žmogaus review signalą;
  - `should_open_technical_blocker` rodo, ar vien šis radinys yra pakankamas techninio blocker'io kandidatui.
- raw `EPUBCheck` JSON išvestis turi būti saugoma atskirai kaip `source/index/epubcheck_report.raw.json`.

### `source/index/figures.tsv`
Kanoninis, bet materializuojamas source-layer figūrų discovery inventorius.

Privalomi stulpeliai fiksuota tvarka:

- `source_figure_id`
- `chapter_slug`
- `source_reference`
- `asset_filename`
- `media_type`
- `alt_text`
- `caption_text`
- `candidate_type`
- `importance_candidate`
- `backend_candidate`

Papildoma required vs blank-cell taisyklė:

- v1 neturi papildomų optional columns;
- `asset_filename`, `media_type`, `alt_text` ir `caption_text` gali turėti tuščias reikšmes, jei source jų neduoda arba candidate nekyla iš tiesioginio `<img>` asset'o, bet šie stulpeliai vis tiek privalo egzistuoti header'yje.

Tapatybės taisyklė:

- `source_figure_id` yra vienintelis row identity ir turi būti stabilus bei unikalus knygos scope;
- `chapter_slug` yra required scope laukas, bet ne identity;
- `source_reference` ir `asset_filename` negali būti laikomi identity, nes gali kartotis arba būti tušti;
- `lt/figures/specs/<id>.yaml.source_figure_id` turi deterministiškai rodyti atgal į šio inventoriaus eilutę.

Discovery hint'ų semantika:

- `candidate_type` (`decorative`, `table_like`, `simple_image`, `diagram`, `algorithmic_flow`, `sequence_like`, `mixed`) yra discovery lygio struktūrinė hipotezė, ne final `figure_type`;
- `importance_candidate` (`required_for_understanding`, `strong_learning_value`, `optional`, `decorative`) yra discovery lygio svarbos signalas, ne final chapter completion verdict;
- `backend_candidate` (`whimsical_mcp`, `raster_text_localization`, `table_to_markdown`, `textual_fallback`, `no_pipeline`) yra routing candidate, ne final `render_backend` ar `render_strategy`.

Workflow vaidmuo:

- `prepare-book` materializuoja pradinį `source/index/figures.tsv` ir `source/index/figures.meta.yaml`;
- `inventory-figures` gali tą patį inventorių perrefreshinti iš source, bet negali jo paversti galutinių būsenų registru;
- `build-figure-specs` ir `resume_figures` naudoja jį atrastų kandidatų visatai atstatyti;
- final figūros semantinė tiesa prasideda tik `lt/figures/specs/<id>.yaml`, o final render / export / embed registras prasideda tik `lt/figures/manifest.tsv`;
- blocker ir chapter completion logika lieka downstream `lt/figures/specs/<id>.yaml`, `lt/figures/manifest.tsv` ir `qa/chapter_status.tsv` sluoksniuose.

Šiame TSV negyvena:

- `figure_id`
- `figure_type`
- `render_backend`
- `render_strategy`
- `review_required`
- `spec_reconcile_required`
- `status`
- `rendered_png_path`
- `exported_vector_path`
- `embedded_in_chapter`
- `embedded_in_learning_block`
- blocker ar dependency laukai

Formalizavimas:

- sidecar failas yra `books/<slug>/source/index/figures.meta.yaml`;
- sidecar turi nurodyti `schema_type: figure_candidate_inventory`, `schema_version: "1.0"`, `artifact_path`, `artifact_fingerprint`, `required_columns[]` ir `optional_columns[]`;
- `required_columns[]` turi kartoti visus 10 aukščiau išvardytų stulpelių ta pačia tvarka;
- `optional_columns[] = []`.

### `chapter_packs/<slug>.yaml`
Vykdomas skyriaus preflight artefaktas.

Privalomi blokai:

- `chapter_slug`
- `chapter_number`
- `source_segments[]`
- `chapter_type`
- `risk_flags[]`
- `draft_mode`
- `required_research_tracks[]`
- `required_claims[]`
- `term_candidates_snapshot[]`
- `global_term_locks[]`
- `local_term_locks[]`
- `expected_figures[]`
- `learning_block_profile`
- `required_sections[]`
- `optional_sections_enabled[]`
- `optional_sections_disabled[]`
- `not_allowed_sections[]`
- `blocking_conditions[]`

Paskirtis:

- būti vieninteliu vykdomu skyriaus įėjimo kontraktu prieš kanoninio LT teksto generavimą;
- sujungti terminiją, riziką, figūras ir mokymosi sluoksnio tipą į vieną preflight objektą.

Papildomas kontraktas:

- `source_segments[]` šiame artefakte pernaudoja bendrą v1 `source_segments[]` item modelį iš chaptering sluoksnio ir negali naudoti atskiro, pack-local formato;
- `required_claims[]` yra privalomas preflight claim coverage / obligation descriptor masyvas, ne jau egzistuojančių `claim_id` registras;
- `build-chapter-pack` gali sukurti validų `chapter_pack` dar prieš atsirandant `claims/<slug>.yaml`, nes `required_claims[]` aprašo, kokia claim-level atrama turi būti sukurta ar peržiūrėta vėlesniame etape;
- kiekvienas `required_claims[]` vienetas turi būti seklus objektas su bent `claim_key`, `claim_type`, `source_scope`, `why_required`;
- `claim_key` yra stabilus chapter-local descriptor identifikatorius ir vienintelis kanoninis join raktas tarp `chapter_pack`, `claims` ir claim-related blocker'ių tame skyriuje;
- `research-chapter` turi kiekvieną `required_claims[]` descriptor vienetą arba materializuoti į `claims/<slug>.yaml` per `claims[].required_claim_ref`, arba palikti formaliai neišspręstą per blocker / review kelią su `blockers[].required_claim_refs[]`;
- claim coverage closure tame skyriuje vertinama pagal `chapter_pack.required_claims[].claim_key` padengimą per `claims[].required_claim_ref` ir, jei dar neišspręsta, per `blockers[].required_claim_refs[]`; nė vienas `required_claims[]` vienetas negali likti be jokio formalaus downstream ryšio;
- `required_claims[]` kartu yra ir kanoninis preflight signalas chapter-level `risk_class` derivacijai: jei masyvas nėra tuščias, downstream `build-chapter-pack` privalo materializuoti `qa/chapter_status.tsv.risk_class = high`; jei masyvas yra `[]`, downstream `build-chapter-pack` privalo materializuoti `risk_class = low`;
- `chapter_type` yra privalomas string enum, apibūdinantis dominuojantį source chapter turinio tipą; leistinos v1 reikšmės:
  - `expository` — vyrauja aiškinamasis ar aprašomasis turinys be dominuojančios veiksmų sekos ar vaistų/dozių centro;
  - `algorithmic` — vyrauja žingsninė sprendimų ar veiksmų seka;
  - `pharmacology` — vyrauja vaistų, dozių ar režimų logika;
  - `mixed` — nėra vienos aiškiai dominuojančios ankstesnės klasės;
- `draft_mode` yra privalomas string enum; v1 leidžiama tik reikšmė `preflight_scaffold`;
- `draft_mode = preflight_scaffold` reiškia, kad `chapter_pack` yra vykdomas planavimo / preflight artefaktas, o ne atskiras vartotojui rodomo vertimo juodraščio tipas ir ne papildoma workflow state ašis;
- `risk_flags[]` lieka granularių rizikos priežasčių rinkiniu pačiame `chapter_pack`; jis gali paaiškinti, kodėl skyrius laikomas jautriu, bet negali tapti atskiru persisted `risk_class` enum'u ar override mechanizmu;
- `risk_flags[]` yra privalomas masyvas, kuriam leidžiama `[]`; jei item'ų yra, jie gali būti tik šie normalizuoti machine-facing flag'ai:
  - `algorithmic_sequence`
  - `medication_or_dose`
  - `indication_or_contraindication`
  - `competency_boundary`
  - `guideline_dependent`
  - `jurisdiction_specific`
  - `legal_or_organizational`
- `required_research_tracks[]` yra privalomas masyvas, kuriam leidžiama `[]`; jei item'ų yra, jie gali būti tik šie v1 track ID:
  - `lt_official`
  - `lt_academic`
  - `lt_clinical`
  - `es_official`
  - `source_market_context`
- `term_candidates_snapshot[]` yra privalomas masyvas, kuriam leidžiama `[]`; kiekvienas vienetas turi būti seklus objektas su bent `source_term_en`, `candidate_lt`, `context`, `needs_review`, o `concept_id` lieka optional, jei kandidatas dar nesurištas su kanonine sąvoka;
- `global_term_locks[]`, `local_term_locks[]` ir `expected_figures[]` yra privalomi masyvai, kuriems leidžiama `[]`, kai tame pjūvyje nėra elementų;
- `global_term_locks[]` vienetas turi būti seklus objektas su bent `concept_id`, `preferred_lt`, `lock_basis`; jei jis materializuoja globalią kontekstinę taisyklę, tada papildomai privalo turėti `global_variant_key` ir `usage_scope`;
- jei `global_variant_key` nepateiktas, `global_term_locks[]` row turi būti grįžtamas į `shared/terminology/global_concepts.tsv`; jei `global_variant_key` pateiktas, row turi būti grįžtamas į `shared/terminology/global_variants.tsv`, o `preferred_lt` turi sutapti su to source row `allowed_lt_variant`;
- `local_term_locks[]` vienetas turi būti seklus objektas su bent `local_term_key`, `concept_id`, `source_term_en`, `preferred_lt`, `usage_scope`;
- jei `local_term_key` prasideda `lc-`, row turi būti grįžtamas į `books/<slug>/terms/local_concepts.tsv`, o `usage_scope` tame snapshot'e turi būti `book_default`; jei `local_term_key` prasideda `lv-`, row turi būti grįžtamas į `books/<slug>/terms/local_variants.tsv`, `preferred_lt` turi sutapti su source row `allowed_lt_variant`, o `source_term_en` turi būti paveldimas per tą patį `concept_id` iš atitinkamo concept row;
- `expected_figures[]` vienetas turi būti seklus objektas su bent `figure_key`, `source_ref`, `importance`, `learning_relevance`;
- nė vienas iš šių masyvų negali būti modeliuojamas vien raw free-text elementais kaip vieninteliu elemento tipu;
- `learning_block_profile` lieka privalomas viršutinis mokymosi bloko profilis;
- `learning_block_profile` v1 yra privalomas string enum, ne free-text prose laukas; leistinos reikšmės:
  - `expository`
  - `algorithmic`
  - `pharmacology`
  - `mixed`
- `blocking_conditions[]` yra privalomas masyvas, kuriam leidžiama `[]`; kiekvienas vienetas turi būti seklus objektas su bent `condition_type`, `summary`, `blocks_before`, o `requires_user_decision` lieka optional loginis signalas;
- `blocking_conditions[].condition_type` v1 nėra uždaras globalus enum, bet turi būti stabilus machine-facing snake_case identifikatorius;
- `blocking_conditions[].blocks_before` gali būti tik:
  - `research_localization`
  - `translation`
- `required_sections[]`, `optional_sections_enabled[]`, `optional_sections_disabled[]`, `not_allowed_sections[]` kartu sudaro pilną planning-state modelį tam pačiam kanoninių learning sekcijų rinkiniui, o ne tik papildomoms sekcijoms;
- `required_sections[]` turi apimti ir pastovų privalomą branduolį iš `product_spec.md`, ir sąlyginai privalomas sekcijas pagal skyriaus tipą, riziką ar figūrų svarbą;
- jei naudojamas minimalus v1 `learning_section_id` modelis, jis reiškia tik techninius kanoninius ID jau užrakintoms produkto sekcijoms, o ne naują konkuruojančią taksonomiją.

Kanoninis v1 `learning_section_id` rinkinys:

- `chapter_essence` -> `Skyriaus esmė`
- `key_terms` -> `Svarbiausi terminai`
- `core_logic` -> `Pagrindinė logika / mechanizmas`
- `explanatory_examples` -> `Paaiškinamieji pavyzdžiai`
- `must_remember` -> `Ką būtina atsiminti`
- `self_check_questions` -> `Savikontrolės klausimai`
- `algorithmic_flow` -> `Algoritminė eiga`
- `medications_and_doses` -> `Vaistai ir dozės`
- `red_flags_common_errors` -> `Raudonos vėliavos / dažnos klaidos`
- `clinical_mini_scenarios` -> `Klinikiniai mini-scenarijai`
- `lt_es_context` -> `Papildomas LT / ES paaiškinimas`
- `figure_explanations` -> `Paveikslų / schemų paaiškinimas`

Papildomos taisyklės šiam rinkiniui:

- `learning_section_id` yra stabilus machine-facing identifikatorius; žmogui rodomas heading'as lieka `product_spec.md` užrakintas LT pavadinimas;
- `required_sections[]`, `optional_sections_enabled[]`, `optional_sections_disabled[]` ir `not_allowed_sections[]` gali saugoti tik šiuos `learning_section_id`, ne laisvą tekstą ir ne LT heading'us;
- visi šio rinkinio ID kartu turi sudaryti pilną v1 planning-state partition tame skyriuje: tas pats ID negali kartotis daugiau nei viename masyve;
- šeši branduolio ID (`chapter_essence`, `key_terms`, `core_logic`, `explanatory_examples`, `must_remember`, `self_check_questions`) visada turi būti `required_sections[]` masyve ta pačia kanonine tvarka kaip `product_spec.md`;
- likę šeši sąlyginiai ID kiekviename `chapter_pack` turi būti deterministiškai paskirstyti tarp `required_sections[]`, `optional_sections_enabled[]`, `optional_sections_disabled[]` ir `not_allowed_sections[]` pagal produkto taisykles ir skyriaus kontekstą.

### `research/<slug>.md`
Skyriaus lygio tyrimo ir lokalizacijos sprendimų žurnalas.

Privalomos sekcijos:

- `Skyriaus tikslas`
- `LT šaltinių apžvalga`
- `ES šaltinių apžvalga`
- `Lokalizacijos sprendimai`
- `Originalo kontekstas`
- `Atviri klausimai`
- `Galutinis agento auditas`

Paskirtis:

- saugoti žmogui skaitomą sprendimų istoriją;
- neperkrauti kanoninio LT teksto techniniais įrodymais.

### `claims/<slug>.yaml`
Tik aukštos rizikos teiginių sluoksnis.

Šis registras top-level lygyje turi turėti `chapter_slug`.

Kiekvienas claim vienetas turi turėti:

- `claim_id`
- `required_claim_ref`
- `claim_text_lt_summary`
- `claim_type` (`dose`, `algorithm`, `contraindication`, `guideline`, ir pan.)
- `risk_level`
- `supporting_lt_sources[]`
- `supporting_es_sources[]`
- `localization_decision`
- `status` (`validated`, `blocked`, `needs_review`)

Paskirtis:

- laikyti claim-level atramą tik ten, kur ji būtina;
- neleisti aukštos rizikos turiniui likti be aiškios atramos.
- `required_claim_ref` turi deterministiškai rodyti į `chapter_pack.required_claims[].claim_key`, kuris pareikalavo šio claim coverage; vienas descriptor gali materializuotis į vieną ar daugiau claim įrašų, bet kiekvienas materializuotas claim turi turėti vieną aiškų lineage ryšį.

### `blockers/<slug>.yaml`
Atskiras blocker'ių registras tam skyriui.

Šio registro top-level lygyje turi būti `chapter_slug`.

Kiekvienas blockeris turi turėti:

- `blocker_id`
- `required_claim_refs[]`
- `term_refs[]`
- `type`
- `severity`
- `location`
- `problem_summary`
- `status` (`open`, `resolved`, `escalated`)
- `requires_user_decision`

Papildomi / sąlyginiai laukai:

- `source_fragment`
- `current_lt_fragment`, jei jau egzistuoja
- `lt_sources_checked[]`
- `es_sources_checked[]`
- `proposed_resolution`
- `auto_resolvable`
- `notes`

Paskirtis:

- neleisti blocker'iams pasimesti `research` tekste;
- duoti sistemai formalų auto-resolution ir escalation sluoksnį.
- `required_claim_refs[]` turi būti `[]`, jei blocker'is nesusijęs su claim coverage; claim-related blocker'ių atveju jis turi nurodyti, kurių `chapter_pack.required_claims[].claim_key` vienetų tas blocker'is dar neleidžia laikyti uždengtais.
- `term_refs[]` turi būti `[]`, jei blocker'is nesusijęs su terminija; terminų blocker'ių atveju leidžiamos reikšmės yra tik `concept:<concept_id>`, `global_variant:<global_variant_key>` ir `local:<local_term_key>`.

### `terms/candidates.tsv`
Knygos lygio kandidatinių terminų inbox.

Privalomi stulpeliai:

- `concept_id`, jei jau priskirtas
- `source_term_en`
- `candidate_lt`
- `chapter_slug`
- `context`
- `risk_level`
- `lt_evidence_count`
- `es_evidence_count`
- `proposed_status`
- `final_status`
- `notes`

Paskirtis:

- būti tarpiniu sluoksniu tarp naujai aptikto termino ir kanoninio užrakinimo.
- v1 neturi atskiro `shared/terminology/global_candidates.tsv`; visi nauji kandidatai pirmiausia gyvena `books/<slug>/terms/candidates.tsv`, o iš ten tik po review / promotion gali materializuotis į `shared/terminology/global_concepts.tsv` arba `shared/terminology/global_variants.tsv`.
- kandidatų stadijos signalai, tokie kaip `lt_evidence_count`, `es_evidence_count`, `proposed_status` ir `final_status`, gyvena tik šiame inbox arba blocker / decision sluoksnyje ir nėra kanoninių locked TSV row header dalis.

### `shared/terminology/global_concepts.tsv`
Globaliai užrakintų cross-book default sąvokų sluoksnis.

Privalomi stulpeliai:

- `concept_id`
- `source_term_en`
- `preferred_lt`
- `domain`
- `risk_class`
- `lock_basis`
- `lt_sources`

Optional stulpeliai:

- `es_sources`
- `notes`

Papildomos taisyklės:

- vienas row per `concept_id`;
- `concept_id` yra vienintelis identity, o `preferred_lt` gali keistis tik kaip controlled update tam pačiam `concept_id`;
- čia gyvena tik globalūs default lock'ai, ne kandidatai ir ne kontekstinės išimtys;
- failo kelias jau nusako scope, todėl atskiras papildomas scope row laukas čia neleidžiamas;
- `chapter_pack.global_term_locks[]` default row be `global_variant_key` turi ateiti iš čia;
- `lt_sources` ir `es_sources` yra stabilūs list-valued TSV langeliai ir serializuojami pagal bendrą TSV taisyklę žemiau.

### `shared/terminology/global_variants.tsv`
Globalių kontekstinių išimčių sluoksnis.

Privalomi stulpeliai:

- `global_variant_key`
- `concept_id`
- `allowed_lt_variant`
- `usage_scope`
- `restriction_note`
- `approval_basis`

Optional stulpeliai:

- `notes`

Papildomos taisyklės:

- vienas row per `global_variant_key`;
- `global_variant_key` yra stabilus rule ID, o `concept_id` turi jau egzistuoti `shared/terminology/global_concepts.tsv`;
- šis failas nepakeičia globalaus default'o visur; jis tik jį perrašo siaurame `usage_scope`;
- `chapter_pack.global_term_locks[]` row su `global_variant_key` turi ateiti iš čia, o `preferred_lt` tame snapshot'e turi sutapti su `allowed_lt_variant`.

### `books/<slug>/terms/local_concepts.tsv`
Knygos lygio default arba local-only užrakintų sąvokų sluoksnis.

Privalomi stulpeliai:

- `local_term_key`
- `concept_id`
- `source_term_en`
- `preferred_lt`
- `domain`
- `risk_class`
- `lock_basis`
- `lt_sources`

Optional stulpeliai:

- `es_sources`
- `notes`

Papildomos taisyklės:

- vienas row per `local_term_key`, unikalų tame `book_slug`;
- `local_term_key` su prefiksu `lc-` identifikuoja `local_concepts.tsv` row;
- jei tas pats `concept_id` jau egzistuoja `shared/terminology/global_concepts.tsv`, toks row yra sąmoningas book-level override; jei ne, tai local-only locked concept iki promotion;
- row negali egzistuoti, jei jis pilnai dubliuoja galiojantį globalų default'ą ir nesukuria jokio book-specific skirtumo;
- `chapter_pack.local_term_locks[]` row su `local_term_key` prefiksu `lc-` turi ateiti iš čia.

### `books/<slug>/terms/local_variants.tsv`
Knygos lygio kontekstinių išimčių sluoksnis.

Privalomi stulpeliai:

- `local_term_key`
- `concept_id`
- `allowed_lt_variant`
- `usage_scope`
- `restriction_note`
- `approval_basis`

Optional stulpeliai:

- `notes`

Papildomos taisyklės:

- vienas row per `local_term_key`, unikalų tame `book_slug`;
- `local_term_key` su prefiksu `lv-` identifikuoja `local_variants.tsv` row;
- `concept_id` turi resolve'intis arba į `shared/terminology/global_concepts.tsv`, arba į `books/<slug>/terms/local_concepts.tsv` tame pačiame book scope;
- variant row negali pats įvesti naujos sąvokos;
- `chapter_pack.local_term_locks[]` row su `local_term_key` prefiksu `lv-` turi ateiti iš čia ir turi būti siauresnis už atitinkamą book default ar globalų default.

### `lt/figures/specs/<id>.yaml`
Kanoninis tekstinis figūros spec.

Privalomi laukai:

- `figure_id`
- `chapter_slug`
- `source_figure_id`
- `figure_type`
- `importance`
- `source_payload_reference`
- `structure_model`
- `text_layers[]`
- `labels[]`
- `must_preserve[]`
- `may_simplify[]`
- `localization_rules[]`
- `render_backend` (`whimsical_mcp` schemoms / diagramoms; `raster_text_localization` paveikslėliams su tekstu)
- `render_strategy`
- `export_strategy`
- `fallback_export_formats[]`
- `embed_targets[]`
- `review_required`
- `spec_reconcile_required`
- `depends_on_claim_ids[]`
- `depends_on_chapter_sections[]`
- `status`

Sąlyginai privalomi laukai:

- `lt_caption`, jei figūra turi bent vieną LT-facing `embed_targets[]` tikslą.

Optional:

- `source_caption`
- `notes`

Paskirtis:

- būti kanonine figūros semantine tiesa repo viduje;
- leisti perrenderinti figūrą neprarandant jos loginės struktūros.

### `lt/figures/manifest.tsv`
Renderintų figūrų registras.

Privalomi stulpeliai:

- `figure_id`
- `chapter_slug`
- `spec_path`
- `rendered_png_path`
- `exported_vector_path`, jei yra
- `source_figure_id`
- `status`
- `embedded_in_chapter`
- `embedded_in_learning_block`

### `qa/chapter_status.tsv`
Kanoninis chapter execution registry.

Privalomi laukai kiekvienai materializuotai skyriaus eilutei:

- `chapter_slug`
- `risk_class`
- `chapter_state`
- `segmentation_status`
- `research_status`
- `claims_status`
- `terminology_status`
- `localization_status`
- `blockers_status`
- `canonical_lt_status`
- `learning_block_status`
- `figures_status`
- `qa_status`
- `release_state`
- `user_review_required`
- `user_review_status`
- `obsidian_sync_status`
- `last_updated`

Paskirtis:

- būti kanoniniu chapter execution registry per OpenCode / Codex CLI;
- būti pagrindiniu chapter execution source-of-truth CLI guard'ams ir resume logikai;
- neleisti workflow būsenos laikyti tik pokalbyje, tarpiniuose loguose ar spėti iš artefaktų egzistavimo.

Papildomas kontraktas:

- `prepare-book` gali materializuoti tik šio failo header-only shell su fiksuotu stulpelių rinkiniu, bet be chapter-level eilučių;
- kol konkrečiam skyriui dar nėra registry eilutės, tai semantiškai reiškia `chapter_state = not_started`, o gate / release / review / sync ašys tam skyriui dar nelaikomos materializuotomis;
- `start-chapter` yra vienintelis v1 komandų owner'is, kuris pirmą kartą sukuria konkretaus skyriaus registry eilutę ir nustato bent `chapter_state = pack_pending` bei `risk_class = pending_pack`;
- `risk_class` yra required policy klasifikatorius su vienintelėmis leistinomis reikšmėmis `pending_pack`, `high` ir `low`;
- `build-chapter-pack` yra vienintelis v1 komandų owner'is, kuris išsprendžia `risk_class` iš `chapter_pack.required_claims[]`: ne tuščias masyvas -> `high`, `[]` -> `low`, ir po sėkmingo pack materializavimo perveda `chapter_state` į `pack_ready`;
- `qa-chapter` gali atnaujinti tik QA etapo snapshot laukus ir savo `chapter_state` perėjimus, bet negali bootstrapinti naujos registry eilutės ar pirmą kartą spręsti `risk_class`;
- `review-chapter`, `approve-chapter` ir resume logika `risk_class` tik skaito iš šio registro ir negali jo taisyti ar perderivuoti.

## Pirmi formatų sprendimo principai
Nors galutinio formato viskam dar nefiksuojame, pirmi loginiai principai yra tokie:

- `yaml` — ten, kur reikia hierarchinių, žmogui skaitomų ir agentui taisomų struktūrų;
- `tsv` — ten, kur svarbios stabilios lentelinės bazės ir diffo aiškumas;
- `md` — ten, kur reikia žmogui skaitomo naratyvinio ar audito sluoksnio.

Iš to seka bazinis pasirinkimas:

- `book`, `chapter_map`, `chapter_pack`, `claims`, `blockers`, `figure spec` — greičiausiai `yaml`;
- `global terminology`, `manifest`, `execution registries` ir kitos stabilios lentelinės bazės — greičiausiai `tsv`;
- `research`, `kanoninis LT skyrius`, `mokymosi blokas` — `md`.

## Formalus artefaktų formatas ir versijavimas
### Bendras modelis
Visi struktūriniai YAML artefaktai turi turėti:
- `schema_type`
- `schema_version`

`md` ir `tsv` artefaktams naudojami sidecar `.meta.yaml` failai.

### Kodėl šitas žingsnis svarbus dabar
Be kanoninių artefaktų kontrakto dar neįmanoma tvarkingai projektuoti:

- CLI komandų;
- agentų rolių;
- workflow būsenų mašinos;
- automatinio blocker resolution;
- Obsidian sync logikos.

Todėl artefaktų semantika yra antras architektūros žingsnis po repo struktūros.

### Versijų semantika
Naudojama `major.minor` schema:
- `major` — breaking change
- `minor` — atgal suderinamas išplėtimas

### `required` vs `optional`
- `required` — be lauko agentas nebegali patikimai nuspręsti, ką daryti
- `optional` — nebuvimas nesugriauna workflow semantikos
- `conditionally required` — priklauso nuo konteksto / rizikos / role-specific logikos

### Migracijos politika
- atskiras CLI entrypointas: `migrate-artifacts`
- migracijos pėdsakas: `books/<slug>/migrations/<timestamp>-<from>-to-<to>.yaml`
- auto-migracija leidžiama tik saugiems `minor` pakeitimams
- `major` pakeitimams būtinas review arba aiški migracijos logika

### Markdown ir TSV versijavimas
Kadangi `md` ir `tsv` failuose nenorima teršti žmogui skaitomo turinio techniniais laukais, jiems naudojamas sidecar modelis.

Kiekvienam kanoniniam `md` ar `tsv` artefaktui leidžiama arba privaloma turėti sidecar:

- `<name>.meta.yaml`

Sidecar turi bent:

- `schema_type`
- `schema_version`
- `artifact_path`
- `artifact_fingerprint`, jei taikoma

### Required vs optional taisyklės
#### Required laukai
Laukas laikomas `required`, jei be jo:

- agentas negali nustatyti artefakto tapatybės;
- agentas negali nustatyti scope / rizikos / priklausomybės;
- agentas negali patikimai nuspręsti, ką daryti toliau;
- jo trūkumas pakeistų produkto politikos prasmę.

#### Optional laukai
Laukas laikomas `optional`, jei:

- jo nebuvimas nesugriauna workflow semantikos;
- jis tik pagerina aiškumą, auditą ar ateities plėtrą;
- sistema gali turėti saugų default elgesį be to lauko.

#### Conditional required laukai
Kai kurie laukai yra `conditionally required`.

Pavyzdžiai:

- `claims_status` negali būti `not_required`, kai `risk_class = high`, bet gali būti `not_required`, kai `risk_class = low`;
- `lt_caption` figūros spec faile privalomas tik jei figūra turi būti įterpiama į LT sluoksnį;
- `requires_confirmation = true` reikalauja, kad `confirmation_status` negalėtų būti `not_required`.

Šie conditional rules turi būti laikomi schemose kaip loginės validacijos taisyklės, ne tik prose pastabos.

### TSV artefaktų formalios taisyklės
Kadangi `tsv` nėra savideskriptyvus kaip `yaml`, kiekvienam kanoniniam TSV failui taikomos šios taisyklės:

1. header eilutė yra privaloma ir fiksuota;
2. header tvarka yra schemos dalis, ne kosmetika;
3. sidecar `.meta.yaml` faile privaloma nurodyti:
   - `schema_type`
   - `schema_version`
   - `required_columns[]`
   - `optional_columns[]`
4. agentas negali tyliai perrašyti TSV su kita kolonų tvarka ar kitu header rinkiniu.
5. terminų list-valued stulpeliai, tokie kaip `lt_sources` ir `es_sources`, visose kanoninėse terminology TSV schemose serializuojami tuo pačiu `;` separatoriumi; mišrūs separatoriai negalimi.

Tai taikoma bent:

- `shared/terminology/global_concepts.tsv`
- `shared/terminology/global_variants.tsv`
- `books/<slug>/terms/local_concepts.tsv`
- `books/<slug>/terms/local_variants.tsv`
- `books/<slug>/terms/candidates.tsv`
- `source/index/figures.tsv`
- `lt/figures/manifest.tsv`
- `qa/chapter_status.tsv`

`source/index/figures.tsv` sidecar yra `books/<slug>/source/index/figures.meta.yaml` su `schema_type: figure_candidate_inventory`, `schema_version: "1.0"`, visais 10 `required_columns[]` pagal šio artefakto semantinį kontraktą aukščiau ir `optional_columns[] = []`.

### Markdown artefaktų formalios taisyklės
`md` failams galioja ši tvarka:

- pats markdown skirtas žmogui skaitomam turiniui;
- schema, priklausomybės ir šviežumas laikomi sidecar `.meta.yaml` faile;
- agentai negali dėti privalomų mašininių laukų į pačio turinio vidų, išskyrus aiškiai leistinus nematomus techninius marker'ius, jei tokių kada nors reikės.

Tai taikoma bent:

- `research/<slug>.md`
- `lt/chapters/<slug>.md`
- `lt/learning/<slug>.md`
- `source/chapters-en/<slug>.md`

### Schema versioning politika v1
#### `major` pakeitimas
`major` versija didinama tik jei:

- keičiasi required laukai;
- keičiasi laukų tipai taip, kad senas agentas gali neteisingai suprasti reikšmę;
- keičiasi enum reikšmių semantika;
- keičiasi failo struktūra taip, kad senas parseris nebegali jos saugiai skaityti.

Šiame `chapter_pack + claims` mazge `required_claims`, `global_term_locks`, `local_term_locks`, `expected_figures`, `required_sections`, `optional_sections_enabled`, `optional_sections_disabled`, `not_allowed_sections`, `supporting_lt_sources` ir `supporting_es_sources` perkėlimas ar įtraukimas į required kontraktą yra `major` schema change, ne tylus `minor` patikslinimas.

Terminų persistencijos mazge `shared/terminology/global_concepts.tsv`, `shared/terminology/global_variants.tsv`, `books/<slug>/terms/local_concepts.tsv`, `books/<slug>/terms/local_variants.tsv`, `chapter_pack.*term_locks[]` ir `blockers[].term_refs[]` required header / field pakeitimai taip pat yra `major` schema change. `migrate-artifacts` negali saugiai iš akies atspėti trūkstamų `global_variant_key`, `local_term_key`, `usage_scope` ar `term_refs[]`; tokie ankstyvi scaffold artefaktai turi būti aiškiai migruojami arba regeneruojami ranka.

#### `minor` pakeitimas
`minor` versija didinama jei:

- pridedami nauji optional laukai;
- pridedamos naujos enum reikšmės, kurios nekeičia senų reikšmių prasmės;
- plečiami audit / notes / sidecar metaduomenys be breaking change.

#### Ką agentai privalo tikrinti
Kiekvienas agentas prieš skaitydamas struktūrinį artefaktą turi tikrinti:

- `schema_type`
- `schema_version`
- ar ši versija palaikoma šiame vykdymo cikle

Jei ne:

- workflow negali tęstis tyliai;
- reikia arba migracijos, arba aiškaus `unsupported_schema_version` blocker'io.

### Migracijos taisyklė v1
Jei schema keičiasi taip, kad seni artefaktai tampa nesuderinami, sistema negali jų „pataisyti iš akies“. Turi būti formalus migracijos kelias.

Kiekviena migracija turi palikti pėdsaką:

- `books/<slug>/migrations/<timestamp>-<from>-to-<to>.yaml`

Jame turi būti bent:

- `migration_id`
- `from_schema_version`
- `to_schema_version`
- `affected_artifacts[]`
- `performed_by`
- `performed_at`
- `notes`

### YAML artefaktų minimalios formalios schemos
Toliau pateikiamas ne visas `JSON Schema` lygio formatas, o galutinė v1 laukų klasifikacija, kuri turi būti atspindėta schemose.

#### `book.yaml` (`schema_type: book_profile`)
Required:

- `schema_type`
- `schema_version`
- `book_id`
- `book_slug`
- `title_en`
- `source_type`
- `source_path`
- `status`
- `domain_tags`
- `risk_profile`
- `approved_chapter_map_version`

Optional:

- `title_lt_working`
- `edition_label`
- `expected_lt_eu_conflicts`
- `core_repeating_concepts`
- `book_specific_localization_rules`
- `open_book_level_questions`
- `last_preparation_review_at`
- `notes`

`status` šiame artefakte saugo kanoninį `book_state` enum:

- `source_added`
- `preparation_running`
- `prepared_waiting_chapter_map_review`
- `prepared_waiting_translation_permission`
- `active_translation`
- `book_blocked`
- `completed`

`risk_profile` šiame artefakte yra required objektas su bent:

- `overall_level`
- `risk_drivers`

Leistinos `risk_profile.overall_level` reikšmės:

- `low`
- `mixed`
- `high`

Leistinos `risk_profile.risk_drivers[]` reikšmės:

- `algorithms`
- `medications_and_doses`
- `indications_and_contraindications`
- `competency_boundaries`
- `guideline_dependent_content`
- `jurisdiction_specific_content`
- `legal_organizational_requirements`

`approved_chapter_map_version` šiame artefakte yra required integer `>= 0`:

- `0` reiškia, kad dar neegzistuoja joks approved `chapter_map.yaml`;
- `1` yra pirmas approved `chapter_map.yaml`;
- kiekvienas vėlesnis pritaikytas approved map atnaujinimas didina reikšmę lygiai per `+1`.

#### Bendras `source_segments[]` item modelis v1
Šį item modelį pernaudoja:

- `chapter_map.yaml.chapters[]`
- `source/index/toc_review.yaml.proposed_chapters[]`
- `chapter_packs/<slug>.yaml`

`source_segments` v1 yra objektų masyvas.

Kiekvienam `source_segments[]` vienetui required:

- `href`
- `normalized_path`

Optional:

- `start_anchor`
- `end_anchor`

Papildomos taisyklės:

- `href` saugo pilną ingest metu užfiksuotą resurso reference; jei originalas remiasi fragmentu, čia turi likti pilnas `filename#fragment`;
- `normalized_path` saugo to paties resurso fragmentų neturintį normalizuotą kelią;
- `start_anchor` ir `end_anchor` naudojami tik tada, kai konkretus segmentas prasideda ar baigiasi resurso viduje;
- top-level `start_anchor` ir `end_anchor` `chapter_map.yaml` ar `source/index/toc_review.yaml` vienete, jei jie pateikti, turi būti chapter-level mirror signalai pirmam ir paskutiniam `source_segments[]` item ir negali prieštarauti jų boundary reikšmėms.

#### `chapter_map.yaml` (`schema_type: chapter_map`)
Top-level required:

- `schema_type`
- `schema_version`
- `book_slug`
- `chapters`

Kiekvienam `chapters[]` vienetui required:

- `chapter_number`
- `chapter_slug`
- `title_en`
- `source_segments`
- `source_strategy`
- `segmentation_confidence`
- `needs_manual_review`

Optional:

- `title_lt_working`
- `start_anchor`
- `end_anchor`
- `notes`
- `review_flags`

Papildomos taisyklės:

- `chapter_map.yaml` yra tik approved segmentation artefaktas;
- top-level `status` laukas šiame artefakte draudžiamas; proposal būsena gyvena tik `source/index/toc_review.yaml.proposal_status`, o knygos orchestration būsena tik `book.yaml.status`;
- jei skyrių žemėlapis dar laukia review, proposal turi gyventi `source/index/toc_review.yaml`, ne šiame faile.

#### `source/index/toc_review.yaml` (`schema_type: chapter_map_review`)
Top-level required:

- `schema_type`
- `schema_version`
- `book_slug`
- `proposal_status`
- `proposed_chapters`

Kiekvienam `proposed_chapters[]` vienetui required:

- `chapter_number`
- `chapter_slug`
- `title_en`
- `source_segments`
- `source_strategy`
- `segmentation_confidence`
- `needs_manual_review`
- `review_flags`

Optional:

- `title_lt_working`
- `start_anchor`
- `end_anchor`
- `notes`

Papildomos taisyklės:

- leistinos `proposal_status` reikšmės: `pending_review`, `resolved`;
- `review_flags` yra required masyvas; jei signalų nėra, naudojamas `[]`;
- `proposed_chapters[]` sąmoningai naudoja tą pačią segmentacijos struktūrą kaip approved `chapter_map`, kad `review-chapter-map` galėtų materializuoti `chapter_map.yaml` be laisvo permap'inimo;
- `chapter_map.yaml` ir `source/index/toc_review.yaml` negali abu būti traktuojami kaip approved segmentacijos šaltinis; konfliktų atveju approved `chapter_map.yaml` visada laimi;
- v1 nėra "proposed `chapter_map.yaml`" režimo.

#### `source/index/epubcheck_summary.yaml` (`schema_type: epubcheck_summary`)
Top-level required:

- `schema_type`
- `schema_version`
- `book_slug`
- `source_path`
- `source_fingerprint`
- `tool_name`
- `tool_version`
- `ran_at`
- `status`
- `counts`
- `workflow_impact`
- `findings`

Required `counts` laukai:

- `blocking`
- `review_flag`
- `warning`

Required `workflow_impact` laukai:

- `prepare_book_allowed`
- `requires_manual_review`
- `should_open_technical_blocker`

Required kiekvienam `findings[]` vienetui:

- `finding_code`
- `original_severity`
- `normalized_class`
- `summary`
- `workflow_impact`

Required `findings[].workflow_impact` laukai:

- `prepare_book_allowed`
- `requires_manual_review`
- `should_open_technical_blocker`

Optional:

- `location`

Papildomos taisyklės:

- leistinos `status` reikšmės: `passed`, `passed_with_review_flags`, `blocked`;
- leistinos `normalized_class` reikšmės: `blocking`, `review_flag`, `warning`;
- `status = blocked` naudojamas, kai bent vienas `blocking` radinys daro EPUB nepatikimą ingest etapui;
- `status = passed_with_review_flags` naudojamas, kai EPUB gali būti ingest'inamas, bet reikia žmogaus review signalų;
- top-level `workflow_impact` yra agreguotas OR rezultatas iš visų `findings[].workflow_impact` reikšmių;
- `findings[].workflow_impact` naudoja tą patį shape kaip top-level `workflow_impact`, bet aprašo tik vieno radinio lokalią įtaką workflow;
- šis artefaktas turi likti source/ingest pagalbiniu validation failu ir negali tapti `book.yaml`, `chapter_map.yaml` ar `qa/chapter_status.tsv` pakaitalu.

#### `chapter_packs/<slug>.yaml` (`schema_type: chapter_pack`)
Required:

- `schema_type`
- `schema_version`
- `book_slug`
- `chapter_slug`
- `chapter_number`
- `source_segments`
- `chapter_type`
- `risk_flags`
- `draft_mode`
- `required_research_tracks`
- `required_claims`
- `term_candidates_snapshot`
- `global_term_locks`
- `local_term_locks`
- `expected_figures`
- `learning_block_profile`
- `required_sections`
- `optional_sections_enabled`
- `optional_sections_disabled`
- `not_allowed_sections`
- `blocking_conditions`

Optional:

- `notes`

Papildomos taisyklės:

- `source_segments[]` pernaudoja bendrą v1 `source_segments[]` item modelį be pack-local variacijos;
- `required_research_tracks[]` yra required masyvas; jei item'ų yra, jie gali būti tik `lt_official`, `lt_academic`, `lt_clinical`, `es_official`, `source_market_context`;
- `required_claims`, `global_term_locks`, `local_term_locks`, `expected_figures`, `required_sections`, `optional_sections_enabled`, `optional_sections_disabled`, `not_allowed_sections` yra required masyvai; jei konkrečiam skyriui tame pjūvyje nėra elementų, naudojamas `[]`, o ne optional lauko praleidimas;
- `required_claims[]` išlaiko preflight obligation descriptor semantiką ir nereiškia, kad `claims/<slug>.yaml` jau egzistuoja ar kad masyve saugomi tik finalūs `claim_id`;
- kiekvienas `required_claims[].claim_key` yra stabilus chapter-local join raktas, kurį privalo naudoti tiek `claims[].required_claim_ref`, tiek claim-related `blockers[].required_claim_refs[]`;
- `required_claims[]` kartu yra kanoninis upstream derivation signalas `qa/chapter_status.tsv.risk_class`: ne tuščias masyvas reiškia, kad downstream `build-chapter-pack` turi materializuoti `risk_class = high`, o `[]` reiškia, kad jis turi materializuoti `risk_class = low`;
- `chapter_type` naudoja tik šias string enum reikšmes: `expository`, `algorithmic`, `pharmacology`, `mixed`;
- `draft_mode` naudoja tik vieną leistiną v1 string enum reikšmę: `preflight_scaffold`;
- `draft_mode = preflight_scaffold` žymi vykdomą preflight pack tipą ir nepakeičia `chapter_state`, `risk_class`, gate ar review ašių;
- pats `chapter_pack` nelaiko atskiro `risk_class` lauko; persisted policy klasifikatorius gyvena tik `qa/chapter_status.tsv`, o `risk_flags[]` lieka granularių priežasčių rinkiniu, kuris negali jo perrašyti ar pakeisti;
- `risk_flags[]` yra required masyvas; jei item'ų yra, jie gali būti tik `algorithmic_sequence`, `medication_or_dose`, `indication_or_contraindication`, `competency_boundary`, `guideline_dependent`, `jurisdiction_specific`, `legal_or_organizational`;
- `term_candidates_snapshot[]` yra required masyvas; kiekvienam row required: `source_term_en`, `candidate_lt`, `context`, `needs_review`; `concept_id` lieka optional;
- `global_term_locks[]` default row identity yra `concept_id`; jei row materializuoja globalią kontekstinę taisyklę, `global_variant_key` ir `usage_scope` tampa privalomi, `preferred_lt` turi sutapti su source row `allowed_lt_variant`, o source row turi egzistuoti `shared/terminology/global_variants.tsv`;
- jei `global_variant_key` nepateiktas, `global_term_locks[]` row turi resolve'intis į `shared/terminology/global_concepts.tsv`; tam pačiam `concept_id` tame pačiame `chapter_pack` leidžiama turėti ir default row, ir siauresnį variant row, jei jų `usage_scope` skiriasi ir abu realiai reikalingi tame skyriuje;
- `local_term_locks[]` kiekvienam row required: `local_term_key`, `concept_id`, `source_term_en`, `preferred_lt`, `usage_scope`;
- jei `local_term_key` prefiksas `lc-`, source row turi būti `books/<slug>/terms/local_concepts.tsv`, o `usage_scope` turi būti `book_default`; jei `local_term_key` prefiksas `lv-`, source row turi būti `books/<slug>/terms/local_variants.tsv`, `preferred_lt` turi sutapti su source row `allowed_lt_variant`, o `source_term_en` turi būti resolve'inamas per tą patį `concept_id`;
- kiekvienas `local_term_locks[]` row turi būti grįžtamas į vieną konkretų local TSV row, o local lock'ai tame pačiame `concept_id` visada turi aukštesnį precedence už globalias taisykles;
- `learning_block_profile` lieka required viršutinis profilis ir naudoja tik šias string enum reikšmes: `expository`, `algorithmic`, `pharmacology`, `mixed`;
- `blocking_conditions[]` yra required masyvas; kiekvienam row required: `condition_type`, `summary`, `blocks_before`; `requires_user_decision` lieka optional;
- `blocking_conditions[].condition_type` yra stabilus machine-facing snake_case identifikatorius, bet v1 dar nėra uždaras globalus enum;
- `blocking_conditions[].blocks_before` gali būti tik `research_localization` arba `translation`;
- keturi learning sekcijų masyvai kartu su `learning_block_profile` aprašo pilną planning-state modelį tam pačiam kanoninių sekcijų rinkiniui;
- jei naudojamas minimalus v1 `learning_section_id` modelis, tai yra techniniai kanoniniai ID jau užrakintoms produkto sekcijoms, ne nauja produkto taksonomija.
- keturi learning sekcijų masyvai gali turėti tik semantiniame kontrakte aukščiau užrakintus `learning_section_id`;
- visi kanoninio v1 rinkinio `learning_section_id` turi būti suklasifikuoti tiksliai viename iš keturių masyvų tame pačiame `chapter_pack`;
- šeši branduolio ID visada turi likti `required_sections` masyve kanonine tvarka;
- tas pats `learning_section_id` negali pasikartoti keliuose masyvuose ar būti keičiamas į žmogui matomą LT heading'ą kaip saugojimo formatą.

#### `claims/<slug>.yaml` (`schema_type: claims_register`)
Top-level required:

- `schema_type`
- `schema_version`
- `book_slug`
- `chapter_slug`
- `claims`

Kiekvienam `claims[]` vienetui required:

- `claim_id`
- `required_claim_ref`
- `claim_text_lt_summary`
- `claim_type`
- `risk_level`
- `supporting_lt_sources`
- `supporting_es_sources`
- `localization_decision`
- `status`

Optional:

- `notes`
- `depends_on_concepts`
- `depends_on_sections`

Papildomos taisyklės:

- `required_claim_ref` privalo sutapti su vienu `chapter_pack.required_claims[].claim_key` tame pačiame skyriuje;
- `supporting_lt_sources` ir `supporting_es_sources` yra required masyvai; jei atrama dar neužfiksuota, naudojamas `[]`, o ne optional lauko praleidimas;
- jei abu support masyvai tušti, `status = validated` negali būti laikomas validžiu;
- jei abu support masyvai tušti arba atrama nepakankama / konfliktuojanti, `needs_review` ir `blocked` lieka leidžiami statusai.

#### `blockers/<slug>.yaml` (`schema_type: blocker_register`)
Top-level required:

- `schema_type`
- `schema_version`
- `book_slug`
- `chapter_slug`
- `blockers`

Kiekvienam `blockers[]` vienetui required:

- `blocker_id`
- `required_claim_refs`
- `term_refs`
- `type`
- `severity`
- `location`
- `problem_summary`
- `status`
- `requires_user_decision`

Optional:

- `source_fragment`
- `current_lt_fragment`
- `lt_sources_checked`
- `es_sources_checked`
- `proposed_resolution`
- `auto_resolvable`
- `notes`

Papildomos taisyklės:

- `required_claim_refs` yra required masyvas; blocker'iui, kuris nesusijęs su claim coverage, naudojamas `[]`;
- jei blocker'is yra vienintelis formaliai likęs kelias konkrečiam `required_claims[].claim_key`, tas `claim_key` turi būti įtrauktas į `required_claim_refs`.
- `term_refs` yra required masyvas; blocker'iui, kuris nesusijęs su terminija, naudojamas `[]`;
- `term_refs[]` leidžiamos reikšmės yra tik `concept:<concept_id>`, `global_variant:<global_variant_key>` ir `local:<local_term_key>`;
- `term_unresolved` blocker'is turi turėti bent vieną `concept:<concept_id>` ref'ą;
- `term_conflict` ir `lt_eu_conflict` blocker'iai turi turėti `concept:<concept_id>` ir visus konkrečius `global_variant:` / `local:` ref'us, jei konfliktas jau susijęs su egzistuojančiomis taisyklėmis;
- blocker'is negali būti laikomas išspręstu vien prose lygmeniu: prieš `status = resolved` jo `term_refs[]` turi rodyti į realiai egzistuojančius kanoninius row, arba susijęs `decision_artifact` turi iškart materializuoti tokį row prieš uždarymą.

#### `books/<book_slug>/decisions/<decision_id>.yaml` (`schema_type: decision_artifact`)
Required:

- `schema_type`
- `schema_version`
- `decision_id`
- `book_slug`
- `decision_type`
- `scope_type`
- `scope_ref`
- `source_user_input`
- `interpreted_resolution`
- `risk_level`
- `affected_artifacts`
- `requires_confirmation`
- `confirmation_status`
- `proposed_by`
- `created_at`
- `status`

Optional:

- `applied_by`
- `applied_at`
- `supersedes`
- `notes`

Leistinos `decision_type` reikšmės:

- `chapter_map_review`
- `blocker_resolution`
- `term_resolution`
- `book_localization_exception`
- `chapter_approval`

`decision_type` semantika ir komandų ownership:

- `chapter_map_review` — vienintelis kanoninis `chapter_map` review sprendimo tipas; jį tame scope valdo tik `review-chapter-map approve|revise`.
- `blocker_resolution` — naudojamas tik tada, kai `resolve-blockers apply --blocker <id>` uždaro eskaluotą ne-termininį blocker'į ir neprideda naujos terminų taisyklės ar knygos lygio lokalizacijos išimties.
- `term_resolution` — naudojamas tik tada, kai `resolve-blockers apply --blocker <id>` sukuria, pakeičia, atmeta arba promuoja terminų taisyklę `terms/*` ar `shared/terminology/*` lineage.
- `book_localization_exception` — naudojamas tik tada, kai `resolve-blockers apply --blocker <id>` normalizuoja žmogaus patvirtintą knygos lygio lokalizacijos išimtį į `book.yaml.book_specific_localization_rules[]`; `refresh-book-profile` gali tik perrašyti jau pritaikytą žinią ir pats šio `decision_type` nekūrė.
- `chapter_approval` — vienintelis review-gated skyriaus galutinio patvirtinimo sprendimo tipas; jį tame scope valdo tik `approve-chapter`.

Leistinos `scope_type` reikšmės:

- `book`
- `chapter`
- `blocker`
- `concept`

Leistinos `risk_level` reikšmės:

- `low`
- `medium`
- `high`
- `critical`

`affected_artifacts[]` yra required ne-tuščias masyvas.
Kiekvienam `affected_artifacts[]` vienetui required:

- `path`
- `artifact_type`

`chapter_map_review` scope binding v1:

- `scope_type = book`
- `scope_ref = <book_slug>`
- toks sprendimas turi deklaruoti bent proposal artefaktą `source/index/toc_review.yaml` ir approved segmentacijos artefaktą `chapter_map.yaml` savo `affected_artifacts[]` sąraše; jei apply metu atnaujinamas ir `book.yaml`, jis taip pat turi būti įtrauktas.

V1 lifecycle modelis:

- v1 naudoja vieną kanoninį decision lifecycle failą: `books/<book_slug>/decisions/<decision_id>.yaml`;
- tas pats `decision_artifact` failas naudojamas ir draft, ir laukiančiai patvirtinimo, ir pritaikytai būsenai;
- atskira `decision_draft` artefaktų šeima v1 neįvedama;
- atskira `adjudication_packs/` persistinama artefaktų šeima v1 neįvedama; kai reikia kelių variantų palyginimo, tam naudojamas `decision_artifact` kartu su susijusiais `blockers`, `research`, `claims` ir kitais kanoniniais artefaktais, o ne paralelinis pack registras.

Leistinos `status` reikšmės:

- `draft`
- `awaiting_confirmation`
- `applied`

Leistinos `confirmation_status` reikšmės:

- `not_required`
- `pending`
- `confirmed`

Leistini `status` perėjimai:

1. naujai sukurtas kanoninis `decision_artifact` visada startuoja kaip `draft`;
2. `draft -> awaiting_confirmation` leidžiamas tik jei `requires_confirmation = true` ir interpretacija jau parodyta žmogui;
3. `draft -> applied` leidžiamas tik jei `requires_confirmation = false` ir interpretacija jau parodyta žmogui;
4. `awaiting_confirmation -> applied` leidžiamas tik po aiškaus vartotojo confirmation;
5. jokių kitų persistinamų `status` perėjimų v1 nėra.

Conditional required taisyklės:

- `requires_confirmation = false` -> `confirmation_status = not_required`;
- `requires_confirmation = true` ir `status != applied` -> `confirmation_status = pending`;
- `requires_confirmation = true` ir `status = applied` -> `confirmation_status = confirmed`;
- `applied_by` ir `applied_at` turi būti absent, kai `status` yra `draft` arba `awaiting_confirmation`;
- `applied_by` ir `applied_at` yra required, kai `status = applied`;
- `supersedes` yra required tik kai naujai pritaikytas sprendimas sąmoningai pakeičia ankstesnį jau `applied` sprendimą tam pačiam `decision_type + scope_type + scope_ref` lineage;
- `notes` lieka optional visose būsenose.

Apply boundary:

- kol `status != applied`, `affected_artifacts[]` yra tik deklaruojamas poveikio sąrašas, o ne leidimas keisti downstream artefaktus;
- jei workflow remiasi kanoniniu decision draft'u, jis turi egzistuoti repo kaip `books/<book_slug>/decisions/<decision_id>.yaml`;
- v1 nėra atskiro persistinamo state tarp `awaiting_confirmation` ir `applied`;
- todėl `awaiting_confirmation -> applied` laikomas vienu loginiu apply žingsniu;
- jei confirmation gautas, bet apply neužbaigtas, `status` negali būti tyliai perkeltas į kitą neaprašytą būseną;
- jei iki sėkmingo `applied` atsiranda daliniai ar pilni downstream pakeitimai pagal tą sprendimą, tai yra formalus inconsistency / repair atvejis;
- `status = applied` reiškia, kad sprendimas formaliai pritaikytas ir paveikti repo artefaktai jau suderinti su tuo sprendimu.

#### `lt/figures/specs/<id>.yaml` (`schema_type: figure_spec`)
Required:

- `schema_type`
- `schema_version`
- `figure_id`
- `chapter_slug`
- `source_figure_id`
- `figure_type`
- `importance`
- `source_payload_reference`
- `structure_model`
- `text_layers`
- `labels`
- `must_preserve`
- `may_simplify`
- `localization_rules`
- `render_backend`
- `render_strategy`
- `export_strategy`
- `fallback_export_formats`
- `embed_targets`
- `review_required`
- `spec_reconcile_required`
- `depends_on_claim_ids`
- `depends_on_chapter_sections`
- `status`

Optional:

- `source_caption`
- `lt_caption`
- `notes`

Papildomos taisyklės:

- `text_layers`, `labels`, `must_preserve`, `may_simplify`, `localization_rules`, `fallback_export_formats`, `embed_targets`, `depends_on_claim_ids`, `depends_on_chapter_sections` yra required masyvai; jei konkrečiam spec sluoksniui tame pjūvyje nėra elementų, naudojamas `[]`, o ne optional lauko praleidimas;
- `render_backend` turi būti vienas iš: `whimsical_mcp`, `raster_text_localization`;
- `render_backend = whimsical_mcp` taikomas schemoms, diagramoms ir kitoms nuo nulio perpiešiamoms figūroms; `render_backend = raster_text_localization` taikomas raster paveikslėliams ar nuotraukoms, kuriuose turi būti pašalintas matomas svetimos kalbos tekstas ir įrašytas LT tekstas;
- `review_required` ir `spec_reconcile_required` yra required loginiai signalai, ne laisvos prose pastabos;
- `spec_reconcile_required` yra atskiras reconcile signalas ir nėra `Figure būsenų mašina` enum pakaitalas;
- `lt_caption` lieka conditionally required tik tada, kai `embed_targets` turi bent vieną LT-facing tikslą.

#### `qa/dependency_index.yaml` (`schema_type: dependency_index`)
Required:

- `schema_type`
- `schema_version`
- `artifacts`

Kiekvienam `artifacts[]` vienetui required:

- `artifact_id`
- `artifact_type`
- `path`
- `depends_on`
- `freshness_status`

Optional:

- `input_fingerprints`
- `stale_reason`
- `last_materialized_at`

### Agentų elgesys nepavykus schema validacijai
Jei artefaktas neatitinka schemos:

- agentas negali jo naudoti kaip kanoninės tiesos;
- agentas turi atidaryti aiškų techninį blocker'į;
- jei įmanoma, turi pasiūlyti migracijos ar repair kelią;
- workflow negali tyliai tęstis su „gal vis tiek pakaks“ logika.

### Kodėl šitas sluoksnis būtinas
Be tikslių schemų ir versijavimo sistema ilgainiui subyrėtų:

- agentai skirtingai suprastų tuos pačius failus;
- ateities pakeitimai tyliai sugadintų senus artefaktus;
- nebegalėtume saugiai tęsti darbo tarp sesijų ir agentų;
- OpenCode / Codex CLI pradėtų spėlioti failų struktūras.

## Agentų rolės
- Machine-facing role identifikatoriai turi būti snake_case ir sutapti su `agent_system.md` `structured_state.role` enum bei role promptų failų vardais.
- `user_review` šiame dokumente žymi žmogaus review vartus / veiksmą workflow lygyje, bet nėra agent `role` enum reikšmė ir neturi atskiro role prompt failo.

- `book_preparation`
- `chapter_pack`
- `research_localization`
- `translation`
- `blocker_resolution`
- `learning_block`
- `figure_pipeline`
- `qa_release`
- `obsidian_sync`

### Rolių kontraktai
Kadangi sistema bus naudojama per OpenCode / Codex CLI su ChatGPT modeliu, agentų rolės turi būti aiškiai atskirtos ne pagal UI, o pagal atsakomybę ir artefaktus.

Svarbus principas:

- tai nebūtinai reiškia atskirus fizinius procesus ar atskiras mašinas;
- tai gali būti atskiri režimai, promptai ar entrypointai;
- tačiau kiekviena rolė turi turėti aiškų kontraktą: ką skaito, ką rašo, ko negali daryti be eskalacijos.

#### `book_preparation`
Paskirtis:

- ingest'inti EPUB;
- sugeneruoti pradinį `chapter_map`;
- sukurti `book.yaml` profilį;
- nustatyti preliminarų rizikos žemėlapį;
- aptikti pasikartojančius terminų branduolius;
- sugeneruoti paruošimo santrauką vartotojui.

Skaito:

- `source.epub`
- `shared/localization/*`
- `shared/terminology/*`

Rašo:

- `books/<slug>/book.yaml`
- `books/<slug>/chapter_map.yaml`, jei approved map gali būti materializuotas be papildomo review
- `books/<slug>/source/index/toc_review.yaml`, jei segmentacija dar laukia review
- `source/index/*`

Negali:

- pradėti 1 skyriaus vertimo be vartotojo leidimo.

#### `chapter_pack`
Paskirtis:

- iš patvirtinto `chapter_map` ir knygos profilio sukurti vykdomą skyriaus `chapter_pack`;
- nuspręsti, kokių tyrimo, claim, terminų ir figūrų sluoksnių reikės tam skyriui.

Skaito:

- `book.yaml`
- `chapter_map.yaml`
- `shared/terminology/*`
- `books/<slug>/terms/*`

Rašo:

- `chapter_packs/<slug>.yaml`
- pradinius `blockers`, jei aptinkamos akivaizdžios kliūtys

#### `translation`
Paskirtis:

- generuoti kanoninį LT skyrių pagal `chapter_pack`, `research`, terminų sluoksnį ir lokalizacijos taisykles.

Skaito:

- `chapter_pack`
- `research`
- `claims`
- `shared/terminology/*`
- `books/<slug>/terms/*`
- source skyrių segmentus

Rašo:

- `lt/chapters/<slug>.md`
- prireikus papildymus į `research`
- kandidatinius terminus į `terms/candidates.tsv`

Negali:

- aukštos rizikos neaiškumų palikti nepažymėtų;
- savavališkai užbaigti konfliktinį skyrių be blocker resolution ciklo.

#### `research_localization`
Paskirtis:

- tikslinė LT / ES šaltinių paieška;
- lokalizacijos sprendimų fiksavimas;
- claim-level atramos sukūrimas aukštos rizikos turiniui.

Skaito:

- source skyrių
- `chapter_pack`
- atvirus blocker'ius

Rašo:

- `research/<slug>.md`
- `claims/<slug>.yaml`
- terminų įrodymų pagrindą kandidatams

#### `blocker_resolution`
Paskirtis:

- spręsti blocker'ius po vieną;
- automatiškai uždaryti tik tuos blocker'ius, kuriems yra aukštas pasitikėjimas ir stipri LT atrama;
- kitais atvejais paruošti vartotojui sprendimo paketą.

Skaito:

- `blockers/<slug>.yaml`
- `research`
- `claims`
- terminų sluoksnį

Rašo:

- atnaujintus blocker'ių statusus
- siūlomus sprendimus
- prireikus terminų promotion siūlymus

#### `learning_block`
Paskirtis:

- iš kanoninio LT skyriaus sugeneruoti atskirą mokymosi bloką;
- įtraukti papildomus LT / ES aiškinimus pagal taisykles;
- valdyti mokymosi bloko struktūrinį branduolį ir temines sekcijas.

Skaito:

- `lt/chapters/<slug>.md`
- `chapter_pack`
- `research`
- `claims`

Rašo:

- `lt/learning/<slug>.md`

#### `figure_pipeline`
Paskirtis:

- inventorizuoti figūras;
- sukurti tekstinius figūrų spec failus;
- valdyti renderinimą per `Whimsical Desktop MCP` schemoms ir diagramoms bei per raster paveikslėlių tekstų lokalizacijos backendą paveikslėliams su tekstu;
- eksportuoti ir registruoti galutines figūrų išvestis.

Skaito:

- `source/index/figures.tsv`
- source figūras
- `chapter_pack`
- figūrų spec sluoksnį

Rašo:

- `lt/figures/specs/*`
- `lt/figures/manifest.tsv`
- `lt/figures/rendered/*`
- `lt/figures/exported/*`

Negali:

- laikyti svarbios figūros užbaigta be render / export / embed patikros.

#### `qa_release`
Paskirtis:

- paleisti QA vartus;
- nustatyti, ar skyrius pasiekė release-ready būseną;
- nustatyti, ar skyriui reikia vartotojo review ar galima judėti iki sync pasiūlymo.

Skaito:

- visus skyriaus artefaktus
- `qa/chapter_status.tsv`

Rašo:

- atnaujintą chapter execution registry
- QA ataskaitas

#### `obsidian_sync`
Paskirtis:

- po užbaigto skyriaus pasiūlyti sync į Obsidian;
- sinchronizuoti tik leistinus sluoksnius;
- niekada nelaikyti Obsidian kanoniniu šaltiniu.

Skaito:

- `lt/chapters/*`
- `lt/learning/*`
- `lt/figures/*`
- `obsidian/sync_manifest.yaml`

Rašo:

- sync metaduomenis
- atnaujintą `obsidian/sync_manifest.yaml`

#### `user_review` (žmogaus vartai, ne agent role)
Vartotojas nėra pasyvus patvirtintojas. Jis turi teisę:

- patvirtinti ar atmesti `chapter_map`;
- spręsti eskaluotus blocker'ius;
- pateikti skyriaus pataisas po review;
- patvirtinti finalinį `risk_class = high` skyriaus užbaigimą;
- leisti pradėti kitą skyrių;
- leisti sinchronizuoti į Obsidian.

## Workflow būsenų mašina
### Workflow state modelis v1
Workflow state modelis v1 naudoja atskiras kanonines ašis:

1. `book_state` — knygos lygio orchestration būsena, saugoma `book.yaml.status`.
2. `chapter_state` — skyriaus vykdymo kursorius, saugomas `qa/chapter_status.tsv.chapter_state`, kai to skyriaus registry eilutė jau egzistuoja; eilutės nebuvimas reiškia `not_started`.
3. `risk_class` — chapter-level policy klasifikatorius, materializuotas `qa/chapter_status.tsv.risk_class`, kai to skyriaus registry eilutė jau egzistuoja.
4. gate status fields — skyriaus readiness laukai `qa/chapter_status.tsv`.
5. `release_state` — repo lygio chapter release readiness.
6. `user_review_status` kartu su `user_review_required` — formalus review reikalavimas ir jo būsena.
7. `obsidian_sync_status` — Obsidian sync operacinė būsena.

`freshness_status` nėra nei `book_state`, nei `chapter_state`, nei gate statusas. Jis gyvena tik `qa/dependency_index.yaml` ir sidecar `.meta.yaml` metaduomenyse.

### `book_state`
- `source_added`
- `preparation_running`
- `prepared_waiting_chapter_map_review`
- `prepared_waiting_translation_permission`
- `active_translation`
- `book_blocked`
- `completed`

### `chapter_state`
- `not_started`
- `pack_pending`
- `pack_ready`
- `research_running`
- `translation_running`
- `blockers_open`
- `blocker_resolution_running`
- `canonical_ready`
- `learning_ready`
- `figures_pending`
- `qa_running`
- `qa_complete`
- `revision_requested`

`chapter_state` yra orchestration cursor. Jis negali dubliuoti gate, `user_review_status`, `release_state` ar `obsidian_sync_status` semantikos. Tokios reikšmės kaip `canonical_ready`, `learning_ready`, `figures_pending` ir `qa_complete` reiškia tik tai, kurioje vykdymo vietoje sustojo pipeline, o ne kad chapter jau praėjo vartus, gavo review ar tapo release-ready.

Bootstrap ir ownership taisyklės:

- kol registry eilutė neegzistuoja, skyrius laikomas `not_started`;
- `start-chapter` pirmą kartą sukuria registry eilutę ir nustato `chapter_state = pack_pending`;
- `build-chapter-pack` perveda `chapter_state` į `pack_ready`;
- kiekviena downstream komanda atnaujina tik savo vykdymo etapo `chapter_state` perėjimą;
- `qa-chapter` valdo tik `qa_running` ir `qa_complete` perėjimus, bet negali retroaktyviai bootstrapinti ankstesnių būsenų.

### `risk_class`
`risk_class` yra policy klasifikatorius, materializuotas `qa/chapter_status.tsv`, o ne atskiras workflow state cursor ar gate statusas.

Leistinos reikšmės:

- `pending_pack`
- `high`
- `low`

Semantika:

- `pending_pack` — skyrius jau pradėtas ir turi registry eilutę, bet `chapter_pack` dar nesumaterializuotas, todėl policy klasifikacija dar negali būti galutinai išspręsta;
- `high` — `chapter_pack.required_claims[]` turi bent vieną descriptor vienetą; skyriui reikia claim-level atramos, `claims_status` negali būti `not_required`, o finalus approval kelias visada lieka review-gated prieš `approved`;
- `low` — `chapter_pack.required_claims[] = []`; claim gate gali būti `not_required`, o skyrius gali eiti automatiniu approval keliu, jei nėra kito review-gated pagrindo.

Derivacijos taisyklės:

- `start-chapter` pirmą kartą sukurtai registry eilutei nustato `risk_class = pending_pack`;
- `build-chapter-pack` materializuoja `risk_class` deterministiškai iš `chapter_pack.required_claims[]`: ne tuščias masyvas -> `high`, tuščias masyvas -> `low`;
- `qa-chapter`, `review-chapter`, `approve-chapter` ir resume logika šį lauką tik skaito arba validuoja iš `qa/chapter_status.tsv` ir negali jo perrašyti ar iš naujo išvedinėti iš vien `risk_flags[]`, claim failo egzistavimo ar kitų ad hoc signalų.

### Gate status fields
Šie `qa/chapter_status.tsv` laukai visada naudoja vieną bendrą modelį:

- `segmentation_status`
- `research_status`
- `claims_status`
- `terminology_status`
- `localization_status`
- `blockers_status`
- `canonical_lt_status`
- `learning_block_status`
- `figures_status`
- `qa_status`

Leistinos reikšmės:

- `not_started`
- `in_progress`
- `passed`
- `blocked`
- `not_required`

Jei freshness ar pataisos invaliduoja ankstesnį rezultatą, paveiktas gate laukas grįžta į `in_progress` arba `blocked`. `stale_*` signalai lieka dependency ir sidecar metaduomenyse, ne gate enum'e.

### `release_state`
Leistinos reikšmės:

- `not_ready`
- `release_candidate`
- `approved`
- `sync_ready`
- `synced`

Semantika:

- `not_ready` — bent vienas required gate laukas nėra `passed` arba `not_required`;
- `release_candidate` — visi required gate laukai yra `passed` arba `not_required`, bet chapter dar nėra formaliai `approved`;
- `approved` — chapter repo viduje formaliai užbaigtas pagal review politiką;
- `sync_ready` — chapter yra `approved` ir gali būti siūlomas pirmajam arba pakartotiniam sync;
- `synced` — chapter yra `approved`, o Obsidian kopija aktuali.

Jei repo turinys po sync pasikeičia, bet visi required gate laukai išlieka žali, `release_state` grįžta į `sync_ready`, o `obsidian_sync_status` tampa `outdated_synced_copy`. Jei bent vienas required gate laukas degraduoja į `in_progress` arba `blocked`, `release_state` visada krinta į `not_ready`.

### `user_review_required` ir `user_review_status`
`user_review_required` ir `user_review_status` sudaro atskirą review ašį.

Leistinos `user_review_status` reikšmės:

- `not_required`
- `pending`
- `completed`

Loginės taisyklės:

- `user_review_required = false` -> `user_review_status = not_required`;
- `user_review_required = true` ir review dar neužbaigtas -> `user_review_status = pending`;
- `user_review_required = true` ir reikiamas review užbaigtas -> `user_review_status = completed`;
- po naujo `revision_requested` ciklo `user_review_status` grįžta į `pending`, jei review vis dar privalomas.

### `obsidian_sync_status`
Leistinos reikšmės:

- `not_synced`
- `sync_offered`
- `synced`
- `outdated_synced_copy`

Tai yra sync operacinė būsena, ne bendras workflow ar freshness pakaitalas.

### Knygos lygio būsenų perėjimo logika
- EPUB pridėjimas -> `source_added`
- ingest + profilio kūrimas -> `preparation_running`
- paruoštas pirminis `chapter_map` -> `prepared_waiting_chapter_map_review`
- `review-chapter-map approve|revise`, kai sprendimas pritaikytas ir approved `chapter_map.yaml` jau suderintas su repo, -> `prepared_waiting_translation_permission`
- `start-chapter`, kai pirmą kartą sėkmingai materializuota to skyriaus execution registry eilutė, -> `active_translation`
- kritinis neišspręstas knygos lygio konfliktas -> `book_blocked`
- visi planuoti skyriai užbaigti -> `completed`

### Skyriaus būsenų taisyklės
#### `not_started`
Skyrius dar nepradėtas. Sistema negali jo liesti be vartotojo komandos pradėti konkretų skyrių. Iki `start-chapter` šis statusas gali būti atvaizduojamas vien registry eilutės nebuvimu.

#### `pack_pending`
Skyrius turi patvirtintą segmentaciją, registry eilutė jau sukurta, bet dar neturi `chapter_pack`.

#### `pack_ready`
Skyrius jau turi vykdomą preflight artefaktą ir gali pereiti į tyrimo / vertimo ciklą.

#### `research_running`
Vyksta LT / ES šaltinių paieška, terminijos ir lokalizacijos pagrindo rinkimas.

#### `translation_running`
Generuojamas kanoninis LT tekstas.

#### `blockers_open`
Aptikta bent viena problema, kurios negalima ignoruoti.

#### `blocker_resolution_running`
Sistema aktyviai sprendžia blocker'ius.

#### `canonical_ready`
Kanoninis LT skyrius yra sugeneruotas. Tai nėra gate ar release pakaitalas.

#### `learning_ready`
Mokymosi blokas sugeneruotas. Tai nėra review ar approval pakaitalas.

#### `figures_pending`
Svarbios figūros dar nebaigtos. Tai nereiškia, kad `figures_status` jau yra `blocked`; tą sprendžia gate laukas.

#### `qa_running`
Vyksta QA vartai arba jų rerun.

#### `qa_complete`
Paskutinis reikalingas QA paleidimas baigtas ir dabartinis gate snapshot jau materializuotas `qa/chapter_status.tsv`. Tai dar nereiškia nei review completion, nei `release_state = approved`.

#### `revision_requested`
Vartotojas pateikė pataisų. Pagal nutylėjimą sistema taiko 3 lygių taisymo politiką: lokalus pataisymas -> sekcijos perrašymas -> pilnas perrašymas tik išimtimi.

### Kur sistema turi sustoti ir laukti vartotojo
Sistema privalo sustoti bent šiais taškais:

- po knygos paruošimo ir prieš skyriaus vertimo startą;
- kai `chapter_map` reikia vartotojo patvirtinimo;
- kai blocker'is eskaluotas vartotojui;
- kai `user_review_required = true` ir `user_review_status = pending`;
- prieš sync į Obsidian;
- prieš kitą skyrių.

### Kur sistema gali tęsti pati
Sistema gali tęsti pati tame pačiame skyriuje, jei:

- turi patvirtintą `chapter_map`;
- turi leidimą dirbti tuo skyriumi;
- blocker'iai nėra eskaluoti vartotojui;
- nėra sustojimo taško, kuriam reikia žmogaus sprendimo.

## CLI semantinis modelis
Pagrindinės komandos:
- `prepare-book`
- `review-chapter-map`
- `start-chapter`
- `build-chapter-pack`
- `research-chapter`
- `translate-chapter`
- `resolve-blockers`
- `build-learning-block`
- `inventory-figures`
- `build-figure-specs`
- `render-figures`
- `validate-figures`
- `qa-chapter`
- `review-chapter`
- `revise-chapter`
- `approve-chapter`
- `sync-obsidian`
- `refresh-book-profile`
- `migrate-artifacts`

Komandų taisyklės:
- šiame semantiniame CLI sluoksnyje viena komanda = viena atsakomybė;
- komandos yra resumable;
- komandų guard'ai remiasi kanoniniu `book_state` / `chapter_state` + gate / review / release / sync laukais ir `qa/dependency_index.yaml`, o ne ad hoc artefaktų egzistavimo spėjimu;
- žmogaus patvirtinimo taškai negali būti apeinami;
- kiekviena komanda turi aiškią loginę išėjimo būseną.

### Detalus semantinis CLI kontraktas
Šioje sistemoje aprašomas semantinis CLI kontraktas, o ne galutinis binarinio pavadinimo sprendimas.
Šiame skyriuje komanda reiškia atominį, resumable, guard-based CLI entrypointą.
`product_spec.md` minimas vienas vartotojo prašymas yra aukštesnio lygio operatoriaus workflow vienetas, kuris gali sekoje paleisti kelias čia aprašytas komandas.
Toks orchestration sluoksnis negali apeiti komandų guard'ų, žmogaus patvirtinimo taškų ar pakeisti vienos-komandos-vienos-atsakomybės principo.

#### `prepare-book`
Paskirtis:

- priimti EPUB;
- paleisti `EPUBCheck` kaip privalomą preflight validatoriaus sluoksnį;
- ingest'inti jį per `EPUBLib`;
- sugeneruoti pradinį `chapter_map` pasiūlymą;
- sukurti `book.yaml`;
- sugeneruoti source indeksus;
- užbaigti knygos paruošimą ir perkelti `book.yaml.status` į `prepared_waiting_chapter_map_review` arba `prepared_waiting_translation_permission`.

Minimalūs argumentai:

- `--book-id` arba automatinis slug generavimas
- `--epub <path>`

Pasirenkami argumentai:

- `--title-override`
- `--edition-label`
- `--force`, jei leidžiama perkurti dar nepradėtą paruošimą

Komanda turi:

- sukurti `books/<slug>/` struktūrą;
- paleisti external CLI validatorių `EPUBCheck`;
- jei validatorius sėkmingai paleistas, išsaugoti `source/index/epubcheck_report.raw.json` ir `source/index/epubcheck_summary.yaml`;
- jei `EPUBCheck` nepasiekiamas arba nepasileidžia, sustoti su aiškiu techniniu blocker'iu;
- užpildyti `book.yaml`;
- jei `chapter_map` review dar reikalingas, sugeneruoti `source/index/toc_review.yaml` kaip proposal artefaktą;
- jei `chapter_map` review nereikalingas, materializuoti approved `chapter_map.yaml` tiesiogiai;
- sugeneruoti `source/index/*`;
- `review_flag` lygio `EPUBCheck` signalus perkelti į ingest / `chapter_map` review signalus, kai jie mažina segmentacijos patikimumą;
- sustoti būsenose `prepared_waiting_chapter_map_review` arba `prepared_waiting_translation_permission`.

#### `review-chapter-map`
Paskirtis:

- parodyti aptiktą skyrių žemėlapį;
- leisti patvirtinti arba koreguoti segmentaciją;
- užfiksuoti patvirtintą `chapter_map`.

Galimi režimai:

- `show`
- `approve`
- `revise`

Komanda negali pradėti 1 skyriaus vertimo.

Papildomas kontraktas:

- `show` yra read-only režimas ir, kai review dar neuždarytas, turi rodyti `source/index/toc_review.yaml` proposal artefaktą;
- `approve` ir `revise` yra vieninteliai v1 komandų režimai, kurie valdo `chapter_map_review` `decision_artifact` tame scope;
- `approve` ir `revise` yra vieninteliai v1 komandų režimai, kurie gali materializuoti arba atnaujinti approved `chapter_map.yaml` iš `source/index/toc_review.yaml`;
- komanda, gavusi žmogaus instrukciją apie `chapter_map`, turi persistinti `source_user_input` ir `interpreted_resolution` kanoniniame `decision_artifact` prieš keisdama `chapter_map.yaml`;
- po sėkmingo `approve` arba `revise` pritaikymo `source/index/toc_review.yaml` turi būti pažymėtas `proposal_status = resolved`;
- kai `approve` arba `revise` pasiekia `decision_artifact.status = applied`, ta pati komanda turi atnaujinti `book.yaml.status` į `prepared_waiting_translation_permission`;
- tas pats apply žingsnis turi ir materializuoti naują `approved_chapter_map_version`: jei anksčiau buvo `0`, nustatyti `1`; kitu atveju padidinti ankstesnę approved versiją lygiai per `+1`;
- jei aiškus žmogaus confirmation jau gautas tame pačiame dialogo žingsnyje, komanda gali pereiti tiesiai į `applied`; kitu atveju ji turi sustoti ties `awaiting_confirmation`.

#### `start-chapter`
Paskirtis:

- leisti pradėti tik konkretų skyrių;
- užtikrinti, kad negalima praleisti ankstesnio skyriaus be aiškaus policy išplėtimo;
- pirmą kartą materializuoti konkretaus skyriaus registry eilutę ir pereiti jį iš implicit `not_started` į `pack_pending`.

Minimalūs argumentai:

- `--book <slug>`
- `<chapter>`

Komanda turi patikrinti:

- ar patvirtintas `chapter_map`;
- ar vartotojas tikrai leidžia pradėti būtent šį skyrių;
- ar ankstesnis skyrius neužstrigęs neteisingoje būsenoje.

Po sėkmingo `start-chapter` tame skyriuje turi atsirasti pirmoji `qa/chapter_status.tsv` eilutė bent su šiomis pradinėmis reikšmėmis:

- `chapter_state = pack_pending`
- `risk_class = pending_pack`
- `segmentation_status = passed`
- visi kiti gate laukai = `not_started`
- `release_state = not_ready`
- `user_review_required = false`
- `user_review_status = not_required`
- `obsidian_sync_status = not_synced`

Papildomas kontraktas:

- kai `start-chapter` sėkmingai sukuria pirmą to skyriaus execution registry eilutę, ta pati komanda turi nustatyti `book.yaml.status = active_translation`;
- jei `book.yaml.status` jau yra `active_translation`, vėlesnių skyrių startas šios būsenos nekeičia į jokį kitą tarpinių variantų statusą.

#### `build-chapter-pack`
Paskirtis:

- sukurti vykdomą skyriaus `chapter_pack`;
- atnaujinti terminų kandidatų snapshotą;
- nustatyti reikalingus tyrimo, claims, blocker ir figūrų sluoksnius.

Komanda turi:

- užpildyti `chapter_packs/<slug>.yaml`;
- atnaujinti jau egzistuojančią to skyriaus `qa/chapter_status.tsv` eilutę;
- užpildyti `required_claims[]` kaip preflight claim coverage / obligation descriptor masyvą, o ne kaip jau egzistuojančių `claim_id` sąrašą;
- iš `required_claims[]` deterministiškai išspręsti `risk_class = high|low` ir pervesti `chapter_state` į `pack_ready`;
- jei reikia, inicijuoti `blockers/<slug>.yaml`;
- nepraeiti tyliai, jei skyriaus segmentacija ar bazinis knygos profilis dar neparuošti.

#### `research-chapter`
Paskirtis:

- atlikti LT / ES paiešką;
- užpildyti `research/<slug>.md`;
- sukurti ar atnaujinti `claims/<slug>.yaml` aukštos rizikos turiniui;
- atnaujinti terminų kandidatų įrodymų pagrindą.

Komanda turi:

- privalomai naudoti internetinę paiešką ten, kur yra neaiškumas;
- kiekvieną `chapter_pack.required_claims[]` descriptor vienetą arba materializuoti į `claims/<slug>.yaml` su `required_claim_ref`, arba palikti formaliai neišspręstą per blocker / review kelią su `required_claim_refs[]`;
- neužrakinti globalių terminų be pakankamos LT atramos;
- atidaryti blocker'ius, jei konfliktai neišsprendžiami.

#### `translate-chapter`
Paskirtis:

- sugeneruoti kanoninį LT skyrių pagal `chapter_pack`, `research`, `claims` ir terminų sluoksnį.

Komanda turi:

- rašyti į `lt/chapters/<slug>.md`;
- neužbaigti skyriaus, jei lieka atvirų aukštos rizikos blocker'ių;
- atnaujinti susijusius terminų kandidatus.

#### `resolve-blockers`
Paskirtis:

- perbėgti visus atvirus blocker'ius tame skyriuje;
- automatiškai uždaryti tik aukšto pasitikėjimo ir stiprios LT atramos atvejus;
- kitus blocker'ius eskaluoti vartotojui per aiškų sprendimo paketą.

Galimi režimai:

- `auto`
- `report`
- `apply --blocker <id>`

Komanda turi:

- atnaujinti `blockers/<slug>.yaml`;
- prireikus atnaujinti `research`, `claims`, `terms/*`, `lt/chapters/*`.

Papildomas kontraktas:

- `report` yra read-only režimas ir pats nerašo `decision_artifact`;
- `auto` negali apeiti `requires_user_decision = true` blocker'ių ir negali savavališkai pritaikyti žmogaus sprendimą reikalaujančių pakeitimų;
- `apply --blocker <id>` yra vienintelis v1 komandų režimas, kuris valdo eskaluoto blocker'io sprendimo normalizavimą į `decision_artifact` tame scope;
- ta komanda turi persistinti tik vieną iš `decision_type` reikšmių `blocker_resolution`, `term_resolution` arba `book_localization_exception`, pagal tai, ar sprendimas uždaro blocker'į be termino pokyčio, keičia terminų taisyklę, ar įveda `book.yaml.book_specific_localization_rules[]` išimtį;
- jei blocker'iui reikia žmogaus sprendimo, `apply --blocker <id>` turi persistinti `source_user_input` ir `interpreted_resolution` prieš bet kokius downstream pakeitimus ir negali jų taikyti, kol sprendimas nėra `applied`.

#### `build-learning-block`
Paskirtis:

- iš kanoninio LT skyriaus ir susijusių artefaktų sugeneruoti `lt/learning/<slug>.md`.

Komanda turi:

- laikytis pastovaus branduolio + teminių sekcijų modelio;
- rodyti EN terminus tik pagal patvirtintą politiką;
- aiškiai atskirti iš originalo kilusius ir papildomus LT / ES didaktinius sluoksnius.

#### Figūrų pipeline komandos
Siūlomi entrypointai:

- `inventory-figures`
- `build-figure-specs`
- `render-figures`
- `validate-figures`

Paskirtis:

- aptikti, kokių figūrų reikia;
- sukurti tekstinius spec failus;
- renderinti per `Whimsical Desktop MCP` schemoms ir diagramoms bei lokalizuoti paveikslėlių tekstą per atskirą raster backendą;
- eksportuoti ir validuoti galutines išvestis.

Šių komandų dizaino principas:

- figūros turi būti valdomos kaip atskiras pipeline;
- svarbios figūros negali būti tyliai praleistos;
- MCP / export problemos turi virsti formalia būsenos ir blocker'ių logika.

#### `qa-chapter`
Paskirtis:

- paleisti reikiamus vartus konkrečiam skyriui;
- atnaujinti `qa/chapter_status.tsv` kaip kanoninį chapter execution registry;
- materializuoti QA etapo `chapter_state` perėjimus, gate laukus, `release_state`, `user_review_required`, `user_review_status` ir `obsidian_sync_status` pagal kanoninį state modelį.

Komanda turi tikrinti ne tik kanoninį LT tekstą, bet ir terminų, blocker'ių, figūrų ir mokymosi bloko suderinamumą. Ji negali bootstrapinti naujos registry eilutės ar pirmą kartą išspręsti `risk_class`: jei eilutė dar neegzistuoja arba `risk_class = pending_pack`, pirmiausia turi būti paleistas `start-chapter` / `build-chapter-pack`, o ne `qa-chapter`. Kai `risk_class = high`, `claims_status` negali būti `not_required`; kai `risk_class = low`, `claims_status` gali būti `not_required`, jei claim-level atrama tame skyriuje nereikalinga.

#### `review-chapter` ir `revise-chapter`
`review-chapter` paskirtis:

- parodyti santrauką, kokioje būsenoje skyrius yra;
- parodyti persisted `risk_class` (`pending_pack`, `high` arba `low`);
- parodyti, ar galima tvirtinti.

`review-chapter` yra read-only komanda ir pagal nutylėjimą pati nerašo `decision_artifact`.
Ji rodo `risk_class` iš `qa/chapter_status.tsv` ir gali paaiškinti jo pagrindą per `chapter_pack.required_claims[]` bei `risk_flags[]`, bet negali šio lauko keisti. Jei execution registry eilutė dar neegzistuoja arba `risk_class = pending_pack`, komanda turi reikalauti `start-chapter` / `build-chapter-pack` kelio, o ne pati iš naujo klasifikuoti riziką. Jei registry eilutė jau egzistuoja, bet QA snapshot pasenęs, komanda turi reikalauti naujo `qa-chapter`.

`revise-chapter` paskirtis:

- priimti vartotojo pastabas;
- paleisti 3 lygių taisymo politiką:
  - lokalus pataisymas,
  - sekcijos perrašymas,
  - pilnas perrašymas tik išimtimi.

Jei `revise-chapter` metu vartotojo pastaba peržengia lokalaus taisymo ribą ir faktiškai išsprendžia vieną iš privalomų decision klasės atvejų, komanda negali tyliai taikyti pokyčio kaip paprastos redakcijos: ji turi sukurti ar atnaujinti atitinkamą `decision_artifact` pagal jo scope.

#### `approve-chapter`
Paskirtis:

- formaliai patvirtinti skyrių tada, kai pagal taisykles to reikia iš vartotojo;
- neleisti netyčia pereiti prie kito skyriaus be aiškios approval būsenos.

Papildomas kontraktas:

- jei `risk_class = high`, `approve-chapter` visada valdo review-gated approval kelią ir negali nustatyti `approved` be žmogaus patvirtinimo;
- jei `user_review_required = true`, `approve-chapter` yra vienintelė v1 komanda, valdanti `risk_class = high` ar kitaip review-gated skyriaus galutinio `chapter_approval` `decision_artifact`;
- komanda turi persistinti `source_user_input` ir `interpreted_resolution` prieš keisdama chapter approval būseną;
- `approved` būsena negali būti nustatyta apeinant `decision_artifact` apply boundary, jei tam skyriui pagal politiką reikalingas žmogaus patvirtinimas;
- komanda remiasi persisted `risk_class` iš `qa/chapter_status.tsv` ir jo iš naujo nederivuoja.

#### `sync-obsidian`
Paskirtis:

- pasiūlyti ir, gavus leidimą, sinchronizuoti:
  - kanoninį LT skyrių,
  - mokymosi bloką,
  - lietuviškai perdirbtas figūras.

Komanda negali:

- sync'inti `research`, `claims`, `blockers` ar kitų techninių artefaktų pagal nutylėjimą;
- tyliai perrašyti kanoninės tiesos repo ribų.

V1 taisyklė:

- aiškus vartotojo leidimas sync'inti yra operacinis patvirtinimas, bet ne atskira `decision_artifact` klasė, kol architektūra aiškiai nenusprendžia kitaip.

#### `refresh-book-profile`
Paskirtis:

- automatiškai atnaujinti `book.yaml`, jei po užbaigto skyriaus pasikeitė knygos lygio terminai, rizikos, lokalizacijos taisyklės ar atviri klausimai.

Komanda turi:

- atnaujinti profilį tik kai realiai pasikeičia knygos lygio žinios;
- vengti bereikalingo churn.

### Komandų valdymo principai v1
#### Viena komanda = viena atsakomybė
Komandos turi būti pakankamai siauros, kad agentas ir žmogus aiškiai suprastų:

- ką komanda padarė,
- ko nepadarė,
- kokius artefaktus pakeitė.

#### Komandos turi būti resumable
Jei sesija nutrūko, agentas turi galėti perskaityti artefaktus ir tęsti nuo paskutinės formalios būsenos, o ne iš pokalbio atminties.

#### Žmogaus patvirtinimo taškai negali būti apeinami
Komandos negali:

- pradėti 1 skyriaus be leidimo;
- judėti prie kito skyriaus be leidimo;
- sync'inti į Obsidian be leidimo;
- užbaigti `risk_class = high` skyriaus be review, jei to reikalauja politika.

#### Komandos turi turėti aiškias exit būsenas
Bent jau loginiame lygmenyje kiekviena komanda turi grįžti vieną iš aiškių rezultatų:

- `success`
- `blocked`
- `needs_user_review`
- `needs_user_decision`
- `failed`

#### Komandos neturi tyliai slėpti svarbių side-effectų
Jei komanda pakeitė:

- terminų sluoksnį,
- blocker'ių būseną,
- knygos profilį,
- mokymosi bloką,
- figūrų manifestą,

ji turi tai aiškiai atspindėti artefaktuose ir chapter execution registry.

### Kodėl šitas sluoksnis svarbus
Be aiškių CLI entrypointų visa architektūra liktų graži tik dokumentuose. Tikslas yra ne tik aprašyti viziją, bet turėti sistemą, kurią vėliau realiai galės vykdyti OpenCode / Codex CLI agentai.

Todėl komandų modelis yra tiltas tarp:

- produkto taisyklių;
- artefaktų;
- agentų rolių;
- realaus vykdymo.

## QA / Release architektūra
Minimalūs vartai kiekvienam skyriui:
- segmentacija
- terminija
- lokalizacija
- blockeriai
- kanoninis LT tekstas
- mokymosi blokas
- figūros
- research / claims

Release būsenos:
- `not_ready`
- `release_candidate`
- `approved`
- `sync_ready`
- `synced`

Šiame sluoksnyje `chapter_state` tebėra tik orchestration cursor. Gate, review, release ir sync ašys vertinamos atskirai ir negali būti išvedinėjamos vien iš `chapter_state`.

### Kodėl šis sluoksnis svarbus
Be aiškios release policy agentai rizikuotų:

- per anksti laikyti skyrių užbaigtu;
- supainioti `approved` su `synced`;
- nematyti skirtumo tarp `risk_class = low` ir `risk_class = high` skyriaus approval kelio;
- ignoruoti figūras ar claims kaip antraeilius sluoksnius.

Todėl QA ir release policy yra paskutinis esminis sluoksnis prieš realų implementacijos planą.

### Minimalūs QA vartai kiekvienam skyriui
Nepriklausomai nuo temos, kiekvienas skyrius turi praeiti bent šiuos vartus:

Visi gate laukai naudoja bendrą enum:

- `not_started`
- `in_progress`
- `passed`
- `blocked`
- `not_required`

#### Segmentacijos vartai
Tikslas:

- patikrinti, ar skyrius remiasi patvirtintu `chapter_map`;
- ar source segmentai priskirti teisingai;
- ar nėra akivaizdžios TOC/spine klaidos.

Privaloma būsena:

- `segmentation_status = passed`

#### Terminijos vartai
Tikslas:

- patikrinti, ar aukštos rizikos terminai neužstrigę kaip neužrakinti kandidatai;
- ar naudojami globaliai užrakinti terminai ten, kur jie turi galioti;
- ar knygos lygio išimtys nėra neleistinai išsiplėtusios.

Privaloma būsena:

- `terminology_status = passed`

#### Lokalizacijos vartai
Tikslas:

- patikrinti, ar aukštos rizikos norminis turinys nėra paliktas kaip neadaptuota originalo tiesa;
- ar `Originalo kontekstas` naudotas tik ten, kur leidžia politika;
- ar lokalizacijos sprendimai užfiksuoti `research` sluoksnyje.

Privaloma būsena:

- `localization_status = passed`

#### Blockerių vartai
Tikslas:

- patikrinti, ar nėra atvirų aukštos svarbos blocker'ių;
- ar visi `escalated` blocker'iai turi vartotojo sprendimą;
- ar auto-resolve neatidarė naujų konfliktų.

Privaloma būsena:

- `blockers_status = passed`

#### Kanoninio LT teksto vartai
Tikslas:

- patikrinti, ar kanoninis LT skyrius egzistuoja;
- ar jis nėra tik laikinas juodraštis;
- ar nėra aiškių completeness, struktūros ar stiliaus trūkumų.

Privaloma būsena:

- `canonical_lt_status = passed`

#### Mokymosi bloko vartai
Tikslas:

- patikrinti, ar mokymosi blokas egzistuoja;
- ar jis suderintas su kanoniniu LT sluoksniu;
- ar papildomi LT / ES aiškinimai aiškiai atskirti nuo originalo kilmės turinio;
- ar laikomasi pastovaus branduolio + teminių sekcijų taisyklės.

Privaloma būsena:

- `learning_block_status = passed`

#### Figūrų vartai
Tikslas:

- patikrinti, ar visos svarbios figūros turi spec failus;
- ar schemos ir diagramos sėkmingai renderintos per `Whimsical Desktop MCP`, o paveikslėlių tekstas sėkmingai lokalizuotas per raster backendą;
- ar eksportas ir įterpimas užbaigti;
- ar galutinėse LT figūrų išvestyse neliko matomo EN ar kitos kalbos teksto;
- ar antraeilės figūros aiškiai pažymėtos, jei jų nebuvo būtina baigti.

Privaloma būsena:

- `figures_status = passed` arba `not_required`, jei skyriui figūros nereikalingos.

#### Tyrimo ir claims vartai
Tikslas:

- patikrinti, ar `risk_class = low` skyriui pakanka skyriaus lygio `research`;
- ar `risk_class = high` skyriui egzistuoja claim-level atrama;
- ar kiekvienas `chapter_pack.required_claims[].claim_key` yra arba materializuotas per `claims[].required_claim_ref`, arba dar formaliai atsekamas per `blockers[].required_claim_refs[]` kol neišspręstas;
- ar nėra norminių teiginių be atramos.

Privaloma būsena:

- `research_status = passed`
- jei `risk_class = high`, `claims_status = passed`
- jei `risk_class = low`, `claims_status = passed` arba `not_required`

### Rizikos lygio skirtumai QA politikoje
#### `risk_class = low`
`risk_class = low` skyriui pakanka:

- visų bazinių vartų žalios būsenos;
- joks atviras blocker'is negali likti aktyvus;
- sistema gali pati pereiti į `release_candidate`;
- `claims_status = not_required` leidžiama tik šiame kelyje;
- jei `user_review_required = false`, sistema gali pati pereiti į `approved`, jei politika tai leidžia.

#### `risk_class = high`
`risk_class = high` skyriui papildomai reikia:

- claim-level atramos;
- aiškiai uždarytų lokalizacijos konfliktų;
- `claims_status` negali būti `not_required`;
- galutinio vartotojo review prieš `approved` būseną.

Tai reiškia:

- `risk_class = high` skyrius negali būti laikomas galutinai užbaigtu vien automatiniais vartais.

### Release būsenų detalizacija
#### `not_ready`
Skyrius:

- dar neturi visų required gate laukų `passed` arba `not_required`;
- negali būti laikomas release candidate, net jei dalis artefaktų jau sugeneruota;
- į šią būseną grįžta po pataisų ar freshness-driven degradacijos, jei bent vienas required gate laukas tampa `in_progress` arba `blocked`.

#### `release_candidate`
Skyrius:

- visi required gate laukai yra `passed` arba `not_required`;
- nebeturi atvirų kritinių blocker'ių;
- laukia paskutinio review arba formalaus approval žingsnio.

#### `approved`
Skyrius:

- visi required gate laukai yra `passed` arba `not_required`;
- gavo reikiamą vartotojo review, jei pagal politiką tai būtina;
- laikomas pilnai užbaigtu repo viduje.

#### `sync_ready`
Skyrius:

- yra `approved`;
- turi visus leistinus sync artefaktus;
- gali būti siūlomas sinchronizacijai į Obsidian;
- apima ir atvejį, kai `obsidian_sync_status = outdated_synced_copy`, bet repo gate laukai tebėra žali.

#### `synced`
Skyrius:

- yra `approved`;
- leistini sluoksniai sėkmingai sinchronizuoti į Obsidian;
- repo vis tiek išlieka vienintelis kanoninis šaltinis.

### Kas negali būti laikoma užbaigtu skyriumi
Skyrius negali būti laikomas užbaigtu, jei bent vienas iš šių punktų teisingas:

- `chapter_map` nepatvirtintas;
- yra atvirų aukštos rizikos blocker'ių;
- aukštos rizikos claim'ai neturi atramos;
- kanoninis LT skyrius yra tik laikinas juodraštis;
- mokymosi blokas neatnaujintas po esminio kanoninio pakeitimo;
- svarbi figūra neužbaigta;
- `risk_class = high` skyriui trūksta vartotojo review;
- skyrius tik sinchronizuotas į Obsidian, bet nepatvirtintas repo viduje.

### `qa/chapter_status.tsv` minimalūs laukai v1
Privalomi stulpeliai:

- `chapter_slug`
- `risk_class`
- `chapter_state`
- `segmentation_status`
- `research_status`
- `claims_status`
- `terminology_status`
- `localization_status`
- `blockers_status`
- `canonical_lt_status`
- `learning_block_status`
- `figures_status`
- `qa_status`
- `release_state`
- `user_review_required`
- `user_review_status`
- `obsidian_sync_status`
- `last_updated`

`chapter_state` šiame registre yra kanoninis orchestration cursor. Gate, review, release ir sync ašys turi būti skaitomos tiesiogiai iš savo laukų, o ne išvedinėjamos vien iš `chapter_state`.
`prepare-book` gali palikti tik šio failo header-only shell. Kiekvieno konkretaus skyriaus registry eilutė atsiranda tik po `start-chapter`; jos nebuvimas reiškia `not_started`.
`risk_class` šiame registre yra privalomas policy klasifikatorius su vienintelėmis leistinomis reikšmėmis `pending_pack`, `high` ir `low`. `start-chapter` pirmą kartą nustato `pending_pack`, o `build-chapter-pack` jį materializuoja į `high` arba `low` iš `chapter_pack.required_claims[]`. `qa-chapter`, `review-chapter`, `approve-chapter` ir resume logika šį lauką tik skaito arba validuoja.
Kai `risk_class = high`, `claims_status` šiame registre negali būti `not_required`; kai `risk_class = low`, `claims_status` gali būti `not_required`.

### QA komandų elgesio taisyklės
#### `qa-chapter` negali būti tik linteris
Ji turi tikrinti ne vien tekstinius pažeidimus, bet ir:

- blocker'ių būseną;
- terminų readiness;
- claims atramą;
- figūrų completeness;
- mokymosi bloko suderinamumą.

#### QA turi būti pakartojamas
Visi vartai turi būti pakartotinai paleidžiami po pataisų, blocker resolution ar esminio termino pasikeitimo.

#### QA turi būti selektyvus po pataisų
Po lokalaus taisymo sistema neturi aklai perregeneruoti visko. Ji turi perleisti bent:

- paveiktus vartus;
- priklausomus sluoksnius;
- bendrą release tikrinimą, jei tai paliečia užbaigimo būseną.

## EPUB ingest + chaptering architektūra
### Principas
- `EPUBLib` yra EPUB struktūros backendas;
- skyriaus segmentacija yra produkto logika, ne vien bibliotekos default’as.

### Kodėl šitas sluoksnis kritinis
Kadangi projektas yra `EPUB-first`, būtent ingest + chaptering sluoksnis tampa visos sistemos pamatu. Jei šitas sluoksnis bus miglotas ar per daug heuristinis be kontrolės, vėliau grius:

- terminų nuoseklumas;
- blocker resolution;
- figūrų pipeline;
- mokymosi blokas;
- skyriaus lygio workflow tvarka.

Todėl būtina pirmiausia padaryti ne greitą extraction, o valdomą, review-friendly EPUB ingest architektūrą.

### Ingest etapai
1. EPUB atidarymas ir bazinė validacija
2. Resource modelio atkūrimas
3. Vidinis chaptering modelis
4. Sluoksniuota segmentacijos strategija:
   - `nav/toc + spine`
   - `spine-first`
   - `mixed`
5. Confidence modelis
6. Siūlomas vs patvirtintas `chapter_map`
7. Source skyrių ištraukimas
8. Lentelių inventorizacija
9. Figūrų inventorizacija

### Išėjimo artefaktai po `prepare-book`
- `book.yaml`
- `chapter_map.yaml` (tik jei approved map jau materializuotas)
- `source/index/chapters.json`
- `source/index/chapters.md`
- `source/index/toc_review.yaml` (kai chaptering dar laukia review)
- `source/index/epubcheck_report.raw.json` (kai `EPUBCheck` CLI sėkmingai paleistas)
- `source/index/epubcheck_summary.yaml`
- `source/index/figures.tsv`
- `source/chapters-en/*` (po patvirtinto `chapter_map`)
- `qa/chapter_status.tsv` (leidžiamas tik header-only shell be chapter-level eilučių)

### EPUB conformance validation preflight
`EPUBCheck` v1 architektūroje yra privalomas EPUB conformance validation sluoksnis, kuris papildo `EPUBLib`, bet jo nepakeičia.

Paskirtis:

- anksti patikrinti, ar source EPUB nėra taip sugadintas, kad ingest tampa nepatikimas;
- palikti ir raw tool pėdsaką, ir normalizuotą repo summary artefaktą;
- duoti aiškų signalą, kurie radiniai yra `blocking`, kurie tik `review_flag`, o kurie tik `warning`.

Boundary taisyklė v1:

- `EPUBCheck` yra external CLI validatorius, ne ingest branduolio biblioteka;
- kanoninis v1 įrankis šiame validation sluoksnyje yra būtent `EPUBCheck`;
- jo raw `JSON` ataskaita negali būti laikoma stabiliu vidiniu API;
- vidinis workflow turi remtis `source/index/epubcheck_summary.yaml`, ne tiesioginiu raw tool output parsingu.

V1 išvesties modelis:

- raw tool ataskaita: `source/index/epubcheck_report.raw.json`;
- normalizuota repo santrauka: `source/index/epubcheck_summary.yaml`.

Top-level loginis modelis:

- `status = passed`, jei nėra nei `blocking`, nei workflow reikšmingų `review_flag`;
- `status = passed_with_review_flags`, jei EPUB vis dar ingest'inamas, bet summary turi bent vieną svarbų `review_flag`;
- `status = blocked`, jei bent vienas `blocking` radinys daro EPUB nepatikimą ingest etapui.

Findings klasės:

- `blocking`
- `review_flag`
- `warning`

Workflow taisyklės:

- `blocking` radiniai gali automatiškai atidaryti techninį blocker'į;
- `review_flag` radiniai nepaverčiami blocker'iu automatiškai, bet negali likti tik `epubcheck_summary.yaml`, jei jie turi įtakos segmentacijos review;
- `warning` radiniai yra informaciniai, jei jie nekeičia ingest patikimumo.

### EPUB atidarymas ir bazinė validacija
Pirmas etapas:

- paleisti `EPUBCheck` preflight ir įvertinti jo summary statusą;
- atidaryti EPUB per `EPUBLib`;
- nuskaityti `metadata`, `manifest`, `spine`, `nav`;
- patikrinti, ar EPUB apskritai turi pakankamą struktūrinį vientisumą darbui.

Tikrinami minimalūs dalykai:

- ar failas tikrai atsidaro kaip EPUB;
- ar yra skaitoma package / OPF informacija;
- ar yra bent vienas content dokumentas;
- ar yra spine;
- ar yra nav dokumentas arba bent pakankamai content dokumentų spine analizei.

Jei šitas sluoksnis nepraeina:

- knyga negali pereiti į `prepared_waiting_chapter_map_review` ar `prepared_waiting_translation_permission` būsenas;
- turi būti formuojamas aiškus techninis blocker'is, ne bendra klaida.

### Resource modelio atkūrimas
Sistema turi susikurti savo vidinį modelį iš `EPUBLib` objekto.

Boundary taisyklė v1:

- tiesioginis `EPUBLib` objektų naudojimas leidžiamas tik ingest sluoksnyje;
- visi downstream etapai (`chapter_map` review, `chapter_pack`, tyrimas, vertimas, figūrų pipeline, QA) turi remtis tik projekto vidiniu ingest/chaptering modeliu ir iš jo materializuotais kanoniniais artefaktais;
- raw `EPUBLib` objektai negali būti laikomi stabiliu tarpiniu API tarp ingest ir kitų sistemos mazgų;
- v1 šita boundary taisyklė neįpareigoja kurti bendros cross-source abstrakcijos būsimiems PDF ar kitiems source tipams.

Minimalūs vidiniai vienetai:

- `PublicationMetadata`
- `ManifestResource`
- `SpineEntry`
- `NavEntry`
- `ContentDocument`
- `ImageResource`
- `TableCandidate`
- `FigureCandidate`

Svarbus principas:

- `manifest` ir `spine` negali būti suplakti į vieną dalyką;
- `spine` nurodo reading order;
- `manifest` nurodo visus resource'us;
- `nav/toc` yra signalas apie semantinę skyriaus struktūrą, bet ne absoliuti tiesa.

### Vidinis chaptering modelis
Kiekvienas kandidatinis skyrius turi bent:

- `candidate_id`
- `title_en_raw`
- `normalized_title`
- `candidate_number`, jei aptikta
- `start_reference`
- `end_reference`
- `source_segments[]`
- `source_strategy`
- `confidence`
- `review_flags[]`

Kur:

- `start_reference` ir `end_reference` negali būti vien tik supaprastinti iki filename be fragmento, jei originalas realiai remiasi anchor'ais;
- sistema turi atskirai laikyti pilną `href` / `filename#fragment` ir normalizuotą failo kelią.

### Segmentacijos strategija v1
Sistema turi naudoti ne vieną, o sluoksniuotą segmentacijos strategiją.

#### Pirminė strategija: nav/toc + spine suderinimas
Numatytoji eiga:

1. paimti `nav/toc` įrašus;
2. iš jų ištraukti pilnus target reference (`filename` + galimi fragmentai);
3. sulyginti su `spine` reading order;
4. pabandyti suformuoti chapter kandidatų seką.

Tikslas:

- išnaudoti semantinę leidėjo pateiktą struktūrą;
- bet neleisti `toc` sugadinti reading order, jei jis chaotiškas.

#### Antrinė strategija: spine-first fallback
Jei `nav/toc` sluoksnis nepatikimas:

- sistema turi pereiti į `spine-first` analizę;
- naudoti dokumentų seką, heading signalus, numeravimo patterns ir kitus tekstinius indikatorius.

Tai ypač svarbu EPUB, kuriuose:

- TOC nepilnas;
- keli skyriai gyvena viename XHTML faile;
- yra mišrūs `frontmatter`, `bodymatter`, `appendix` perėjimai.

#### Mišri strategija: nav signalas, spine riba, heading patikra
Jei vien nav ar vien spine duoda dviprasmį rezultatą, sistema turi gebėti naudoti mišrų sprendimą:

- `nav` duoda kandidatinį startą,
- `spine` nustato reading order ribas,
- heading analizė padeda patvirtinti ar atmesti kandidatą.

### Segmentacijos nepatikimumo signalai
Mažiausiai šie signalai turi kelti review flag'ą:

- keli `nav` įrašai rodo į tą patį failą su skirtingais fragmentais;
- `nav` įrašai neatitinka spine tvarkos;
- iš `nav` matosi neaiškus chapter numbering;
- trūksta numeruotų skyrių, bet yra daug aukšto lygio heading'ų spine dokumentuose;
- viename spine dokumente aptinkami keli panašaus lygio skyriaus startai;
- aiškūs `appendix`, `glossary`, `index`, `references` perėjimai sumaišyti su body chapter'iais;
- segmentacijos confidence per maža.

### Confidence modelis
`chapter_map` negali būti tik „sugeneruotas / nesugeneruotas“. Reikia confidence lygio.

Loginiai lygiai:

- `high`
- `medium`
- `low`

`high`:

- TOC ir spine tarpusavyje dera;
- chapter starts atrodo vienareikšmiai;
- nėra rimtų review flag'ų.

`medium`:

- pagrindinė struktūra aiški, bet yra keli įtartini taškai;
- galima automatiškai sugeneruoti siūlomą `chapter_map`, bet reikia vartotojo akies.

`low`:

- TOC/spine stipriai konfliktuoja;
- reikia būtinai review prieš bet kokį vertimo workflow startą.

### `chapter_map` generavimo taisyklė v1
Galutinis `chapter_map` turi būti dviejų žingsnių artefaktas:

1. siūlomas `chapter_map` gyvena `source/index/toc_review.yaml`
2. patvirtintas `chapter_map` gyvena `chapter_map.yaml`

Siūlomas map turi turėti:

- aptiktus skyrius;
- confidence;
- review flag'us;
- segmentacijos strategijos kilmę (`nav+spine`, `spine-first`, `mixed`).

Papildomos taisyklės:

- siūlomas map saugomas per `proposal_status + proposed_chapters[]` modelį, ne per "siūlomo `chapter_map.yaml`" režimą;
- patvirtintas map tampa kanoniniu tik po vartotojo review;
- kol proposal nepatvirtintas, `chapter_pack` ir `source/chapters-en/*` negali remtis `source/index/toc_review.yaml` kaip approved segmentation source.

### Source skyrių ištraukimas
Kai `chapter_map` patvirtintas, sistema turi generuoti `source/chapters-en/*.md`.

Svarbus principas:

- šie failai nėra kanoninis šaltinis;
- jie yra darbo navigacijos ir agentinio skaitymo sluoksnis;
- jie turi būti deterministiškai perregeneruojami iš source + `chapter_map`.

Kiekvienas source chapter failas turi bent:

- skyriaus pavadinimą;
- source segmentų sąrašą;
- source dokumentų ribas;
- ištrauktą tekstinį turinį;
- žymas apie svarbias lenteles ar figūras, jei jos aptiktos.

### XHTML -> vidinis teksto modelis
Siūlomas principas:

1. `EPUBLib` duoda content dokumentus;
2. sistema juos verčia į vidinį blokinį modelį;
3. tik po to generuoja `source/chapters-en/*.md`.

Blokiniai vienetai turi bent apimti:

- heading
- paragraph
- list
- table
- figure_reference
- note/callout
- code/preformatted, jei pasitaiko
- unknown_block

Kodėl tai geriau:

- vėliau lengviau daryti kokybiškesnį table / figure / learning pipeline;
- neapsiribojama vien „flat markdown“ ankstyvame etape;
- galima atskirti, kas yra tekstas, o kas struktūrinis objektas.

### Lentelių inventorizacija
Ingest etape reikia bent:

- aptikti visas lenteles source skyriuje;
- susieti jas su skyriumi;
- pažymėti, ar lentelė paprasta ar sudėtinga;
- užfiksuoti, ar reikės papildomo review prieš vertimą.

Siūlomi laukeliai vidiniam table candidate modeliui:

- `table_id`
- `chapter_slug`
- `source_reference`
- `complexity`
- `header_shape`
- `rowspan_or_colspan_detected`
- `needs_manual_review`

### Figūrų inventorizacija
Ingest metu turi būti surinkti ne tik image failai, bet ir semantinis figūrų kontekstas.

Kiekvienam figure candidate reikia bent vienos `source/index/figures.tsv` eilutės pagal aukščiau aprašytą fiksuotą 10 stulpelių kontraktą.

Ingest / `prepare-book` šiame inventoriuje turi materializuoti `candidate_type`, `importance_candidate` ir `backend_candidate` kaip persisted discovery signalus, o ne kaip final `figure_spec` ar render registry laukus.

Svarbus principas:

- jei figūra aptikta kaip reikšminga supratimui, ingest turi ją pažymėti kaip kandidatę į pilną figure pipeline;
- jei ji dekoratyvinė ar antraeilė, sistema gali tai pažymėti vėlesniam review.

### Kada `prepare-book` turi sustoti
Komanda turi sustoti ir laukti vartotojo, jei bent viena sąlyga teisinga:

- `EPUBCheck` nepasiekiamas arba nepasileidžia kaip external CLI validatorius;
- `source/index/epubcheck_summary.yaml.status = blocked`;
- `chapter_map` confidence nėra pakankamas tyliai laikyti jį patikimu;
- aptikta neaiški spine/nav struktūra;
- yra daug vieno failo su daug fragmentų skyrių;
- yra stiprūs signalai, kad body / appendix / glossary ribos sumaišytos;
- source figūrų sluoksnis atrodo neišbaigtas ar netipiškas.

### Ką `EPUBLib` sprendžia ir ko nesprendžia
`EPUBLib` stipriai padeda šiose vietose:

- aiškus `manifest` modelis;
- aiškus `spine` modelis;
- `nav/toc` priėjimas;
- filename / id lookup;
- geresnis EPUB3 struktūros modelis nei senesniame kelyje.

Konkrečios `EPUBLib` API detalės, kurios svarbios šiai architektūrai:

- biblioteka dokumentuoja `EPUB.reset_toc(..., spine_only=True)` kelią, kuris naudingas TOC rekonstrukcijai pagal reading order;
- manifest lookup dokumentuojamas su `ignore_fragment=True`, todėl lookup gali sąmoningai ignoruoti `#fragment` dalį;
- dėl to mūsų vidinis modelis privalo saugoti ir pilną `filename#fragment`, ir normalizuotą failo kelią, o chaptering negali būti paliekamas vien bibliotekos lookup elgsenai.

Bet mūsų sistema vis tiek pati turi spręsti:

- kas yra tikras skyriaus startas;
- kaip elgtis su multi-anchor tais pačiais failais;
- kada reikia review;
- kaip iš ingest pereiti į patikimą `chapter_map`;
- kaip klasifikuoti lenteles ir figūras pagal vertimo workflow poreikius.

## Terminų ir blocker'ių engine
### Bazinis vienetas
- `concept_id`

### Terminų sluoksniai
- `shared/terminology/global_concepts.tsv`
- `shared/terminology/global_variants.tsv`
- `books/<slug>/terms/candidates.tsv`
- `books/<slug>/terms/local_concepts.tsv`
- `books/<slug>/terms/local_variants.tsv`

### Terminų pipeline
1. candidate normalization
2. evidence collection
3. evidence grading
4. resolution decision:
   - `promote_global_lock`
   - `allow_context_variant`
   - `keep_local_only`
   - `keep_candidate`
   - `reject`
   - `escalate_user_review`

### Blockerių tipai
- `term_unresolved`
- `term_conflict`
- `lt_eu_conflict`
- `claim_missing_support`
- `dose_or_algorithm_risk`
- `market_specific_content`
- `figure_missing_or_unfinished`
- `segmentation_uncertain`
- `translation_structure_drift`

### Escalation paketas
Turi apimti bent:
- `blocker_id`
- problemos tipą
- trumpą esmę
- vietą
- siūlomą LT variantą / sprendimą
- alternatyvas
- LT šaltinius
- ES šaltinius
- sistemos rekomendaciją
- sprendimo pasekmes

### Terminų sluoksnio loginis modelis
Terminų persistencija v1 nenaudoja vieno bendro persisted „sąvokos objekto“. Kanoninis sluoksnis yra padalintas į atskiras row rūšis pagal jų vaidmenį, o kandidatų signalai, blocker'iai ir review sprendimai gyvena atskiruose artefaktuose.

Kanoniniai invariantai:

- `concept_id` yra vienintelis bazinis sąvokos identifikatorius visur;
- `usage_scope` yra vienintelis kanoninis scope field name terminų taisyklėse;
- globalus ar local scope nusakomas failo keliu, ne papildomu scope row lauku;
- workflow signalai, tokie kaip evidencijos skaitikliai, kandidato būsena ar review poreikis, nepriklauso kanoninių locked TSV row header'iui;
- `chapter_pack` materializuoja tik konkrečiam skyriui taikytinų taisyklių snapshot'ą ir nėra terminų source-of-truth.

Be `concept_id` sistema pradėtų:

- painioti sinonimus ir near-synonyms;
- kurti dubliuotus terminų įrašus iš skirtingų knygų;
- nesugebėti atskirti „tas pats terminas, bet kita sritis“ nuo „iš tikro kita sąvoka“.

### Terminų artefaktų vaidmenys
#### `shared/terminology/global_concepts.tsv`
Čia gyvena tik globaliai užrakintos sąvokos.

Naudojimas:

- translation agentas jį laiko pirmo lygio tiesos šaltiniu;
- terminology QA tikrina, ar aukštos rizikos vietose nėra neteisėtų nukrypimų.
- vienas row per `concept_id` saugo cross-book default `preferred_lt`, `risk_class`, `lock_basis` ir LT / ES atramos sąrašus.

#### `shared/terminology/global_variants.tsv`
Čia gyvena tik globalios kontekstinės išimtys.

Naudojimas:

- jei tas pats `concept_id` tam tikroje srityje gali turėti kitą leistiną LT variantą, tai turi būti formalizuota čia, ne palikta kaip laisvas improvizavimas.
- vienas row per `global_variant_key` saugo siaurą globalią taisyklę tam pačiam `concept_id`, o ne antrą globalų default'ą.

#### `books/<slug>/terms/candidates.tsv`
Knygos lygio inbox.

Naudojimas:

- visi naujai aptikti terminai pirmiausia patenka čia;
- tai nėra aktyvi kanoninė bazė;
- tai tarpinis sluoksnis tarp aptikimo ir sprendimo.
- kandidato stadijos skaitikliai, siūlomas statusas ir galutinis resolution signalas lieka čia arba blocker / decision sluoksnyje, ne locked TSV row'uose.

#### `books/<slug>/terms/local_concepts.tsv`
Knygos lygio default arba local-only užrakintos sąvokos.

Naudojimas:

- kai šios knygos default `preferred_lt` turi skirtis nuo globalaus default'o;
- kai sąvoka dar nėra promuota į `shared/`, bet šioje knygoje jau turi kanoninį locked row;
- `local_term_key` su prefiksu `lc-` identifikuoja šio failo row.

#### `books/<slug>/terms/local_variants.tsv`
Knygos lygio kontekstiniai leidžiami variantai.

Naudojimas:

- siauresnėms knygos lygio taisyklėms, kurios perrašo book default'ą tik konkrečiame `usage_scope`;
- `local_term_key` su prefiksu `lv-` identifikuoja šio failo row;
- toks row negali įvesti naujos sąvokos ir turi resolve'intis į jau egzistuojantį `concept_id`.

### Kanoninių terminų precedence v1
Kai tame pačiame skyriuje egzistuoja keli to paties `concept_id` terminų rule sluoksniai, taikomas tik toks precedence orderis:

1. `books/<slug>/terms/local_variants.tsv`, jei `usage_scope` match'ina;
2. `books/<slug>/terms/local_concepts.tsv` book default;
3. `shared/terminology/global_variants.tsv`, jei `usage_scope` match'ina;
4. `shared/terminology/global_concepts.tsv` globalus default;
5. `books/<slug>/terms/candidates.tsv` niekada nėra aktyvus lock'as ir negali būti naudojamas kaip „baigtas“ terminų rule.

`chapter_pack` gali materializuoti ir default row, ir siauresnį variant row tam pačiam `concept_id`, jei abu reikalingi skirtingiems `usage_scope` tame pačiame skyriuje.

### Terminų kandidatų rinkimas v1
Privalomi signalai:

- source heading'ai ir subheading'ai;
- aiškiai mediciniškai svarbios pasikartojančios noun phrase konstrukcijos;
- aukštos rizikos claim tekstai;
- vaistai, santrumpos, algoritmų pavadinimai;
- figūrų caption'ai, jei jie mokymuisi reikšmingi.

Svarbus principas:

- kandidatas neturi būti renkamas vien todėl, kad tai retas angliškas žodis;
- jis turi būti renkamas tada, kai yra tikėtina, kad terminas vėliau kartosis arba paveiks vertimo nuoseklumą.

### Terminų sprendimo pipeline
#### Candidate normalization
Kai randamas kandidatas, sistema turi:

- normalizuoti EN terminą;
- patikrinti, ar toks `concept_id` jau egzistuoja globaliai;
- patikrinti, ar yra lokalus knygos lygio atitikmuo;
- tik tada kurti naują kandidatinį vienetą `books/<slug>/terms/candidates.tsv`.

#### Evidence collection
Kiekvienam kandidatui sistema turi rinkti:

- oficialius LT šaltinius;
- stiprius LT akademinius / medicininius šaltinius;
- stiprius LT klinikinės vartosenos šaltinius;
- tik po to ES šaltinius.

Tai turi būti daroma per realią interneto paiešką, ne per modelio atmintį.

#### Evidence grading
Kiekvienas rastas šaltinis turi būti įvertintas bent pagal:

- `jurisdiction_level` (`LT`, `ES`, `other`)
- `authority_level` (`official`, `academic`, `clinical_usage`, `context_only`)
- `supports_preferred_lt`
- `supports_variant_lt`
- `notes`

#### Resolution decision
Po įrodymų rinkimo sistema turi pasirinkti vieną iš loginių baigčių:

- `promote_global_lock`
- `allow_context_variant`
- `keep_local_only`
- `keep_candidate`
- `reject`
- `escalate_user_review`

### Globalaus užrakinimo taisyklė v1
Resolution engine turi turėti aiškų loginį testą:

- `official_lt_source_present == true`
- arba `strong_lt_sources >= 2` ir jie nepriklausomi

ES šaltiniai gali:

- padėti suprasti sąvoką;
- leisti tęsti mažesnės rizikos darbą;
- paremti kontekstinį variantą;

bet negali vieni patys automatiškai sukurti `global_locked` būsenos.

### Kontekstinių išimčių modelis v1
Kontekstinė išimtis nėra bendras sąvokos statusas; tai atskira kanoninė row rūšis.

Globali kontekstinė taisyklė turi bent:

- `global_variant_key`
- `concept_id`
- `allowed_lt_variant`
- `usage_scope`
- `restriction_note`
- `approval_basis`

Book-scoped lokali kontekstinė taisyklė turi bent:

- `local_term_key`
- `concept_id`
- `allowed_lt_variant`
- `usage_scope`
- `restriction_note`
- `approval_basis`

Svarbus principas:

- kontekstinė išimtis nėra antras pageidaujamas terminas visur;
- ji turi galioti tik aiškiai apibrėžtame kontekste.
- variant row'ai nedubliuoja `risk_class`; jie jį paveldi per `concept_id` iš atitinkamo concept row;
- kanoninėse taisyklėse lieka tik `usage_scope`; alternatyvūs senesni scope vardai čia nebenaudojami.

### Terminų promotion ir review politika v1
Naujas ar pasikeitęs terminų sprendimas pirmiausia turi atsirasti local sluoksnyje:

- `books/<slug>/terms/local_concepts.tsv`, jei tai book default arba local-only locked concept;
- `books/<slug>/terms/local_variants.tsv`, jei tai context-specific taisyklė.

Promotion taisyklės:

- promotion niekada nekuria naujo `concept_id`; naudojamas tas pats bazinis sąvokos identifikatorius;
- jei promuojamas local default, materializuojamas arba atnaujinamas `shared/terminology/global_concepts.tsv` row;
- jei promuojama local kontekstinė taisyklė, materializuojamas `shared/terminology/global_variants.tsv` row su nauju `global_variant_key`;
- po promotion local row turi būti pervertintas: jei jis tapo identiškas naujam global rule ir nebekuria jokio book-specific skirtumo, jis pašalinamas; jei skirtumas lieka, row išlieka kaip sąmoningas local override.

Sistema gali auto-promote'inti tik tada, kai tenkinamos abi sąlygos:

- yra pakankama LT atrama pagal globalų slenkstį;
- nėra konkurencinio rimto varianto, kuris sukeltų dviprasmybę.

Sistema negali auto-promote'inti, jei:

- keli LT variantai atrodo vienodai stiprūs;
- LT ir ES sluoksniai veda į skirtingą praktinį sprendimą;
- terminas aukštos rizikos srityje turi realų kontekstinį konfliktą;
- tas pats terminas jau turi kitą globalų užrakinimą, su kuriuo naujas kandidatas konfliktuoja.

Tokiais atvejais sprendimas turi būti `escalate_user_review`.

Review / escalation privaloma bent tada, kai:

- `risk_class = high`;
- keičiamas jau esamas globalus `preferred_lt`;
- keičiamas jau esamas `shared/terminology/global_variants.tsv` rule;
- keli LT variantai atrodo panašiai stiprūs;
- LT ir ES sluoksniai veda į skirtingą praktinę interpretaciją;
- neaiški pati concept boundary;
- local override siūloma promuoti globaliai vien pagal vienos knygos vartoseną be pakankamos LT atramos.

Jei terminas dar neišspręstas, ypač aukštos rizikos atveju, `chapter_pack` negali materializuoti laikino pseudo-lock'o. Toks terminas turi likti `books/<slug>/terms/candidates.tsv` ir `blockers/<slug>.yaml` / `decision_artifact` kelyje, kol atsiranda realus kanoninis row.

### Terminų atnaujinimo poveikio modelis
Kai globaliai užrakinamas naujas terminas arba pasikeičia senas:

- sistema turi perskaičiuoti paveiktų skyrių rinkinį;
- pažymėti, kurie skyriai turi potencialų neatitikimą;
- mažos rizikos vietose gali siūlyti auto-fix;
- aukštos rizikos vietose turi atidaryti review užduotį.

Tam reikia bent dviejų mechanizmų:

1. terminų naudojimo indekso per skyrius
2. chapter execution registry `qa/chapter_status.tsv`

### Blocker'ių tipologija ir sprendimo algoritmas
Kiekvienas blocker'ių tipas turi skirtingą sprendimo strategiją.

Bendras algoritmas:

1. paimti visus `open` blocker'ius tame skyriuje;
2. sugrupuoti juos pagal tipą ir rimtumą;
3. spręsti aukščiausios svarbos blocker'ius pirmiausia;
4. po kiekvieno sprendimo pervertinti priklausomus blocker'ius;
5. jei reikia, eskaluoti vartotojui.

Auto-resolve leidžiamas tik jei:

- yra aukštas pasitikėjimas sprendimu;
- yra stipri LT atrama, jei problema LT-centrinė;
- nėra kelių lygiaverčių strateginių variantų;
- pakeitimas nekeičia produkto politikos taisyklių.

Escalation privaloma jei:

- problema strateginė, o ne tik techninė;
- keli variantai atrodo lygiaverčiai;
- šaltiniai konfliktuoja;
- sprendimas paveiktų globalų terminų sluoksnį, bet tam nepakanka vienareikšmio pagrindo;
- sprendimas keistų aukštos rizikos turinį taip, kad reikalingas vartotojo prioritetų pasirinkimas.

### Terminų ir blocker'ių ryšys su kitais sluoksniais
Šis engine turi turėti formalias sąsajas su:

- `chapter_pack` — kad žinotų, kokie terminai ir rizikos laukiami;
- `research` — kad gautų žmogui skaitomą sprendimo istoriją;
- `claims` — kad matytų aukštos rizikos atramą;
- `lt/chapters` — kad galėtų taikyti pataisas;
- `lt/learning` — kad po esminių termino pakeitimų pažymėtų poreikį perregeneruoti mokymosi bloką;
- `qa/chapter_status.tsv` — kad atnaujintų chapter execution registry gate ir readiness laukus.

### Kodėl šis sluoksnis yra projekto branduolys
Ši sistema kuriama ne vien tam, kad išverstų tekstą. Ji kuriama tam, kad:

- terminija būtų nuosekli per visas knygas;
- LT / ES validacija būtų formali, ne atsitiktinė;
- neaiškumai būtų sprendžiami ne intuicija, o procesu;
- vartotojas būtų įtraukiamas tik ten, kur tikrai reikia jo sprendimo.

Todėl terminų ir blocker'ių engine yra vienas pagrindinių projekto architektūrinių centrų.

## Figūrų architektūra
### Bendri principai
- repo spec yra kanoninė figūros semantinė tiesa;
- `Whimsical Desktop MCP` yra pirminis schemų ir diagramų render backendas;
- raster paveikslėliams ir nuotraukoms su matomu svetimos kalbos tekstu naudojamas atskiras tekstų lokalizacijos backendas;
- figūrų pipeline yra atskiras workflow sluoksnis.

### Figūrų etapai
1. discovery
2. triage
3. importance classification
4. spec creation
5. render
6. export
7. validation
8. embed

### Mermaid taisyklė
- `Mermaid-first`:
  - flowchart
  - sequence diagram
  - aiškiai loginės algoritminės schemos
- `Direct Whimsical-first`:
  - mind map
  - anatominės / vizualinės schemos
  - mišrios edukacinės diagramos
  - laisvo išdėstymo figūros

### Whimsical organizavimas
- vieta: `Private/Medical Translation/<book_slug>/`
- knyga = vienas `classic folder`
- skyrių subfolderiai + `_shared/`
- viena figūra = vienas Whimsical failas
- failo vardas:
  - `<figure_id> | <trumpas LT pavadinimas>`
- `frame_id` neprivalomas v1
- rankinis redagavimas leidžiamas, bet turi grįžti į repo spec
- draft failai tik atskiri: `DRAFT | ...`
- V1 eksportas = whole-file export

### Figure būsenų mašina
- `discovered`
- `triaged`
- `spec_ready`
- `render_pending`
- `render_running`
- `rendered`
- `exported`
- `validated`
- `embedded`
- `blocked`

`spec_reconcile_required` nėra atskira primary state machine būsena. Tai atskiras reconcile signalas figure spec sluoksnyje, kuris rodo, kad rankiniai Whimsical pakeitimai dar nesuderinti atgal į repo kanoninę tiesą.

### Kada figūra tampa blockeriu
Jei ji yra `required_for_understanding` ir dar nepasiekė bent `validated + embedded`.

### Figure discovery
Ingest metu sistema turi surinkti visus `figure_candidate` vienetus iš:

- `<img>` resursų;
- caption tekstų;
- EPUB turinio blokų, kuriuose aiškiai matosi schema / diagrama;
- lentelių, kurios iš tikro yra diagraminio pobūdžio;
- tekstinių nuorodų į paveikslus ar algoritmus.

Discovery inventorius remiasi tuo pačiu `source/index/figures.tsv` 10 stulpelių kontraktu, aprašytu aukščiau.

`candidate_type`, `importance_candidate` ir `backend_candidate` šiame TSV yra persisted discovery hint'ai: triage jais remiasi kaip įėjimu ir gali juos perinterpretuoti, bet galutinis semantinis užrakinimas atsiranda tik materializuojant `lt/figures/specs/<id>.yaml`.

### Figure triage
Po discovery sistema turi klasifikuoti kiekvieną kandidatą į vieną iš loginių klasių:

- `decorative`
- `table_like`
- `simple_image`
- `diagram`
- `algorithmic_flow`
- `sequence_like`
- `mixed`

Triage tikslas:

- nuspręsti, ar figūra turi keliauti į pilną `Whimsical` pipeline;
- ar jai reikia raster paveikslėlių tekstų lokalizacijos pipeline;
- ar pakanka markdown lentelės;
- ar pakanka tekstinio paaiškinimo;
- ar figūra tampa blockeriu.

### Importance classification
Kiekviena figūra turi gauti bent vieną svarbos klasę:

- `required_for_understanding`
- `strong_learning_value`
- `optional`
- `decorative`

Svarbos klasė pirmiausia valdo blocker ir completion politiką. Pagrindinį backendą pirmiausia lemia `candidate_type` ir tai, ar figūroje yra matomas svetimos kalbos tekstinis sluoksnis.

### Backend pasirinkimo principas
- `diagram`, `algorithmic_flow`, `sequence_like` ir schema-dominant `mixed` kandidatai pagal nutylėjimą keliauja į `Whimsical` pipeline;
- `simple_image` ir tekstą turintys `mixed` kandidatai pagal nutylėjimą keliauja į raster paveikslėlių tekstų lokalizacijos pipeline;
- `table_like` pagal nutylėjimą keliauja į markdown, nebent triage aiškiai nustato, kad tai faktiškai schema;
- `decorative` kandidatai gali būti paliekami už pilno pipeline ribų tik tada, kai tai nepalieka mixed-language galutinio paveikslėlio.

Discovery inventoriuje `backend_candidate = no_pipeline` leidžiama tik kandidatams, kurie sąmoningai nepatenka į pilną render pipeline; tai nėra final `figure_spec.render_backend` reikšmė.

### Kanoninis figūros spec sluoksnis
Spec failas yra vienintelė kanoninė figūros semantinė tiesa, kuri turi leisti:

- perrenderinti figūrą;
- taisyti terminiją;
- atnaujinti LT caption;
- keisti eksporto strategiją;
- nesiremti vien tuo, kas ranka nupiešta board'e.

Kanoniniame spec faile privalomai gyvena ir šios laukų grupės, kurios turi sutapti su formalia `figure_spec` schema aukščiau:

- `source_payload_reference`
- `structure_model`
- `text_layers[]`
- `labels[]`
- `render_backend`
- `render_strategy`
- `export_strategy`
- `embed_targets[]`
- `review_required`
- `spec_reconcile_required`
- `depends_on_claim_ids[]`
- `depends_on_chapter_sections[]`

Kur:

- `structure_model` aprašo loginę figūros sandarą;
- `text_layers[]` laiko lietuvintinus tekstus ir jų tipą;
- `render_backend` nusprendžia, ar figūra eina per `Whimsical`, ar per raster paveikslėlių tekstų lokalizacijos backendą;
- `render_strategy` nusprendžia, ar figūra kuriama tiesiogiai, ar per tarpinį formatą;
- `embed_targets[]` nurodo, kur figūra turi būti įterpta;
- `spec_reconcile_required` rodo, ar rankiniai Whimsical pakeitimai dar turi būti suderinti atgal į repo spec;
- `depends_on_claim_ids[]` ir `depends_on_chapter_sections[]` laiko minimalią claim/section priklausomybę stale ir rerender logikai.

### Figure-spec-first principas
Pagrindinė architektūrinė taisyklė:

- pirmiausia kuriamas tekstinis figūros spec;
- tik po to schema ar diagrama renderinama į `Whimsical`, o paveikslėlis su tekstu lokalizuojamas per raster backendą.

Tai būtina dėl keturių priežasčių:

1. perrenderinimas tampa deterministiškas;
2. terminijos pakeitimai nebereikalauja gaudyti teksto pačiame board'e;
3. render backendą vėliau galima keisti neprarandant figūros logikos;
4. galima atskirti semantinę tiesą nuo vizualios išvesties.

### Mermaid kaip tarpinis sluoksnis
Naudoti Mermaid, jei figūra yra:

- `algorithmic_flow`
- `sequence_like`
- paprasta loginė schema be sudėtingo laisvo layout'o

Nenaudoti Mermaid, jei figūra yra:

- anatominis ar pusiau iliustracinis vaizdas;
- mišri schema su daug rankinio erdvinio išdėstymo;
- wireframe / UI / laisvos formos edukacinis paaiškinimas;
- sudėtinga vizualinė kompozicija, kurios Mermaid neaprašo natūraliai.

Kai Mermaid tinka, pipeline gali būti:

- `figure spec` -> `Mermaid` -> `Whimsical board` -> `export`

### Whimsical Desktop MCP preflight
Prieš bet kokį renderinimą sistema turi atlikti formalų preflight.

Preflight turi tikrinti bent:

- ar Whimsical desktop app paleista;
- ar vartotojas prisijungęs;
- ar workspace pasiekiamas;
- ar render backendas pažymėtas kaip prieinamas šioje sesijoje;
- ar galima sukurti ar pasiekti target failą / board'ą;
- ar eksportavimo kelias veikia.

Preflight rezultatas turi būti vienas iš:

- `ready`
- `ready_with_warnings`
- `blocked`

### Whimsical vendor ribos, iš kurių kyla schemų ir diagramų v1 architektūra
Šios architektūros sprendimai apie importą, eksportą ir preflight kyla iš realių `Whimsical` produkto ribų:

- `Whimsical` neturi universalaus tiesioginio board importo; vietoj to leidžia importuoti vaizdus, tekstą į `mind map` / `stack` formas ir Mermaid kodą;
- Mermaid importui oficialiai palaikomi tik `graph`, `flowchart` ir `sequenceDiagram`, todėl ne visi Mermaid tipai gali būti laikomi pirminiu render keliu;
- image export pagrindinis kelias yra `PNG`, `PDF` gaunamas per `Print`, o `SVG` kelias laikomas eksperimentiniu;
- Oficialūs export docs šiuo metu aprašo `selection`, `whole board` arba `separate frames` eksportą ir `1x` arba `2x` dydžio pasirinkimą; todėl architektūra negali užrakinti vien tik `whole board` eksporto ar vien `1x` rezoliucijos kaip nekintamo kontrakto;
- Plan-tier ar workspace lygio export ribojimai turi būti tikrinami per `preflight` / runtime capability check, o ne laikomi iš anksto užrakinta schema taisykle; šiuo metu aiškiai dokumentuotas `Free` plano ribojimas, svarbus šiam projektui, yra watermark'as ant eksportuotų paveikslų;
- jei export stringa, realūs fallback keliai yra `SVG`, `PDF` arba mažesnių board dalių eksportas;
- `Whimsical` desktop/workspace sluoksnis nėra `offline-first`, todėl interneto ryšio ir pasiekiamumo patikra preflight etape yra normali architektūros dalis, ne pasirenkamas patogumas.

### Raster paveikslėlių tekstų lokalizacijos backendas
Kai figūra nėra perpiešiama nuo nulio per `Whimsical`, bet galutinėje LT išvestyje negali palikti matomo svetimos kalbos teksto, v1 naudoja atskirą raster paveikslėlių tekstų lokalizacijos backendą.

Automatinis branduolys:

- `PaddleOCR` aptinka tekstinius regionus ir jų turinį;
- `LaMa` / `lama-cleaner` pašalina seną tekstą ir atstato foną;
- `Pillow` užrašo LT pakeitimo tekstą.

Rankinis hard-case fallback:

- `Photopea`.

Privalomos taisyklės:

- `OpenCV inpaint` nelaikomas pirminiu v1 inpainting backendu; jis gali būti tik lokali pagalbinė technika, bet ne kanoninis architektūros pasirinkimas;
- jei galutinėje figūros išvestyje lieka matomas EN ar kitos kalbos tekstas, figūra negali būti laikoma `validated`;
- dvikalbis overlay ar „paliekam originalų tekstą ir užrašom LT šalia“ modelis nėra leidžiamas galutiniame paveikslėlyje;
- jei `Photopea` naudojamas rankiniam fallback, galutinis lokalizacijos rezultatas vis tiek turi būti suderintas atgal į repo spec `text_layers[]`, `labels[]` ir kitą lokalizacijos metadata.

### Render strategijos
Kiekviena figūra turi turėti aiškų `render_strategy`:

- `direct_whimsical`
- `mermaid_to_whimsical`
- `raster_text_localization`
- `manual_layout_with_spec`
- `table_to_markdown`
- `textual_fallback`

`raster_text_localization` taikomas paveikslėliams ar nuotraukoms, kurių originalus vizualinis branduolys gali būti paliktas, bet matomas tekstas turi būti pilnai pakeistas LT sluoksniu.

`textual_fallback` negali būti naudojamas figūroms, kurios pažymėtos `required_for_understanding`, jei projekto politika reikalauja pilno lietuviško perdirbimo. Jei paveikslėlis paliekamas galutinėje LT išvestyje, jis negali būti laikomas užbaigtu tol, kol iš jo nepašalintas matomas svetimos kalbos tekstas.

### Board organizavimo modelis
Whimsical organizavimo taisyklės v1:

#### Vieta Whimsical viduje
Visas projektinis figūrų sluoksnis gyvena vartotojo `Private` srityje.

Siūloma aukščiausio lygio struktūra:

```text
Private/
  Medical Translation/
    <book_slug>/
      _shared/
      001-<chapter-slug>/
      002-<chapter-slug>/
      ...
```

#### Vienetas knygos aplanko viduje
V1 taisyklė:

- viena figūra = vienas atskiras Whimsical failas

Nenaudojamas modelis:

- viena knyga = vienas board su daug figūrų;
- vienas skyrius = vienas board su daug figūrų kaip pirminis kelias.

#### Failų pavadinimų politika
Kiekvieno kanoninio figūros failo pavadinimas turi būti:

```text
<figure_id> | <trumpas LT pavadinimas>
```

Taisyklės:

- kanoninis identitetas yra `figure_id`, ne žmogui gražus pavadinimas;
- trumpas LT pavadinimas skirtas žmogaus navigacijai;
- agentai programiškai remiasi `figure_id` ir `whimsical_file_id`, ne vien failo vardu.

#### Ar reikia `frame_id`
Kadangi V1 modelis yra „viena figūra = vienas failas“, `frame_id` nėra privalomas kanoninis laukas.

V1 minimaliam ryšiui pakanka:

- `figure_id`
- `whimsical_file_id`
- `whimsical_url`

#### Rankinis redagavimas Whimsical'e
Rankinis redagavimas leidžiamas.

Bet galioja griežta taisyklė:

- repo spec lieka kanoninė figūros tiesa;
- jei figūra ranka pataisyta Whimsical'e, sistema turi pažymėti, kad reikia suderinti board būseną atgal į repo spec;
- kol tas suderinimas neatliktas, figūra negali būti laikoma pilnai `fresh`.

Tam naudojamas privalomas reconcile signalas figure spec sluoksnyje:

- `spec_reconcile_required`

#### Draft failų politika
Jei reikia eksperimentuoti ar daryti tarpinį juodraštį:

- turi būti kuriamas atskiras failas;
- tokio failo vardas turi prasidėti `DRAFT | <figure_id> | <trumpas LT pavadinimas>`.

Taisyklės:

- kanoniniu laikomas tik failas, kurio vardas prasideda `figure_id | ...`;
- export pipeline ignoruoja `DRAFT | ...` failus;
- jei draft tampa galutiniu, jis turi būti arba pervadintas į kanoninį, arba jo turinys perkeltas į kanoninį failą.

#### Ar reikalingas atskiras Whimsical index / home failas
V1 modelyje ne.

Priežastis:

- `Book Home` ir `Chapter Index` jau egzistuoja repo / Obsidian sluoksnyje;
- Whimsical turi likti figūrų darbo erdve, o ne antru dokumentacijos centru.

### Export architektūra
Pagrindinė pageidaujama išvestis:

- `primary_output = png`

Papildomos išvestys:

- `secondary_output = svg`, jei įmanoma
- `secondary_output = pdf`, jei SVG netinka ar nepasiekiamas

Eksporto vienetas ir fallback tvarka:

1. whole-file PNG export
2. SVG export
3. PDF export
4. perkurti / supaprastinti figūrą, jei eksportas stringa dėl pačios failo struktūros

Jei po visų fallback'ų figūra vis tiek negaunama:

- figūra tampa `blocked`;
- jei ji svarbi supratimui, skyrius negali būti laikomas pilnai užbaigtu.

### Validation po render
Po render ir export sistema turi atlikti bent šiuos patikrinimus:

- ar failas egzistuoja;
- ar failo formatas atitinka tikslą;
- ar eksportuota būtent kanoninė viso figūros failo išvestis;
- ar figūros manifestas atnaujintas;
- ar LT caption ir numeracija sutampa su spec;
- ar figūra įterpta į reikiamą artefaktą:
  - kanoninį LT skyrių,
  - mokymosi bloką,
  - arba abu, jei taip nustatyta.

Tik po šitų patikrų figūra gali pereiti į `validated` būseną.

### Figure būsenų mašina ir ryšiai
`embedded` reiškia ne tik „turime PNG“, bet ir kad figūra realiai įterpta ten, kur reikia.

`blocked` naudojama, jei:

- render backend neprieinamas;
- eksportas nepraėjo;
- spec nepakankamas;
- figūros turinys per daug neaiškus automatiniam perdirbimui;
- reikia vartotojo sprendimo dėl svarbos ar supaprastinimo politikos.

Figūra tampa skyriaus blockeriu, jei tenkinamos abi sąlygos:

1. ji klasifikuota kaip `required_for_understanding` arba kitaip pažymėta kaip privaloma;
2. ji nepasiekė bent `validated` + `embedded` būsenos.

Jei figūra tik `optional` ar `decorative`, jos neužbaigtumas neturi blokuoti viso skyriaus, bet turi būti aiškiai matomas manifestuose ir chapter execution registry.

Sistema turi aiškiai žinoti:

- ar figūra įterpiama į `lt/chapters/<slug>.md`;
- ar figūra papildomai įterpiama į `lt/learning/<slug>.md`;
- ar mokymosi bloke naudojama ta pati figūra, ar supaprastintas jos variantas;
- ar mokymosi blokui reikia papildomo didaktinio paaiškinimo prie figūros.

## Priklausomybių / perregeneravimo grafas
### Priklausomybių metaduomenys
Kiekvienas materializuojamas artefaktas, kuriam taikomas freshness / perregeneravimo sekimas, turi turėti:
- `artifact_id`
- `artifact_type`
- `path`
- `depends_on[]`
- `input_fingerprints`
- `freshness_status`
- `stale_reason[]`
- `last_materialized_at`

### `freshness_status`
- `fresh`
- `stale_auto`
- `stale_review`
- `blocked`

### Pakeitimų klasės
#### Terminų pakeitimai
- `surface_form_only`
- `preferred_lt_changed_same_concept`
- `context_rule_changed`
- `concept_boundary_changed`

#### Claim pakeitimai
- `citation_only`
- `wording_aligned`
- `support_status_changed`
- `clinical_meaning_changed`

#### Kanoninio LT skyriaus pakeitimai
- `non_semantic_copyedit`
- `term_update`
- `semantic_local_change`
- `high_risk_semantic_change`
- `structure_change`
- `figure_reference_change`

### Release būsenos degradavimo logika
- jei po auto-refresh bent vienas required gate laukas grįžta į `in_progress` -> `release_state = not_ready`
- jei po aukštos rizikos ar strateginio pokyčio bent vienas required gate laukas tampa `blocked` -> `release_state = not_ready`
- jei po sync repo pasikeitė, bet visi required gate laukai lieka žali -> `obsidian_sync_status = outdated_synced_copy`, `release_state = sync_ready`

### Kur gyvena priklausomybių metaduomenys
Siūlomas modelis:

- markdown artefaktams naudoti sidecar failus:
  - `lt/chapters/<slug>.meta.yaml`
  - `lt/learning/<slug>.meta.yaml`
  - `source/chapters-en/<slug>.meta.yaml`
- figūrų išvestims naudoti:
  - `lt/figures/rendered/<id>.meta.yaml`
  - `lt/figures/exported/<id>.meta.yaml`
- papildomai laikyti centralizuotą indeksą:
  - `qa/dependency_index.yaml`

### Ką turi turėti sidecar / indeksas
Minimalūs laukai:

- `artifact_id`
- `artifact_type`
- `path`
- `depends_on[]`
- `input_fingerprints`
- `freshness_status`
- `stale_reason[]`
- `last_materialized_at`

`depends_on[]` turi rodyti ne tik failus, bet ir loginę priklausomybę, pvz.:

- `concept:airway-adjunct`
- `claim:003-claim-07`
- `figure_spec:figure-3-1-airway`
- `chapter_pack:003-airway`

### Jei pasikeičia terminas
#### Visada daroma
Kai pasikeičia globalus arba knygos lygio terminas, sistema privalo:

- rasti visus paveiktus skyrius per `dependency_index.yaml`;
- pažymėti jų `chapter_pack` kaip `stale_auto`;
- pažymėti `qa/chapter_status.tsv`, kad `terminology_status` grįžta į `in_progress`, o jei atsiranda neišspręstas konfliktas ar reikia žmogaus sprendimo -> į `blocked`.

#### Jei pakeitimas yra `surface_form_only`
- `claims` nereikia laikyti semantiškai pasenusiais;
- kanoninis LT skyrius gali būti auto-atnaujintas, jei pakeitimas nekeičia reikšmės;
- mokymosi blokas pažymimas `stale_auto` ir gali būti perregeneruotas automatiškai po kanoninio skyriaus atnaujinimo;
- figūrų spec failai lieka `fresh`, nebent terminas naudojamas caption / label sluoksnyje;
- jei figūrų label'uose jis naudojamas, renderintos figūros pažymimos `stale_auto`.

#### Jei pakeitimas yra `preferred_lt_changed_same_concept`
- `chapter_pack` visada `stale_auto`;
- kanoninis LT skyrius `stale_auto` žemos rizikos vietoms;
- jei terminas vartojamas aukštos rizikos claim'e, atitinkamo skyriaus `claims_status` grįžta bent į `in_progress`, o jei atsiranda neišspręstas konfliktas -> į `blocked`;
- mokymosi blokas visada `stale_auto`, kai tik kanoninis skyrius bus atnaujintas;
- figūrų spec failai, kurių `labels[]` ar `lt_caption` priklauso nuo to `concept_id`, pažymimi `stale_auto`.

#### Jei pakeitimas yra `context_rule_changed`
- visi skyriai, kuriuose naudojamas tas `concept_id`, pažymimi bent `stale_review`;
- knygos lygio lokalios išimtys turi būti pervertintos;
- aukštos rizikos vietose atidaromas `term_conflict` arba `localization_policy_exception` blocker'is;
- mokymosi blokas negali būti perregeneruotas automatiškai, kol neatsinaujina kanoninis LT skyrius.

#### Jei pakeitimas yra `concept_boundary_changed`
- tai traktuojama kaip strateginis pakeitimas;
- visi susiję `claims`, `chapter_pack`, kanoniniai LT skyriai ir mokymosi blokai pažymimi `stale_review`;
- reikia review dėl to, ar ankstesni vertimai iš viso kalbėjo apie tą pačią sąvoką;
- jei figūros priklausė nuo seno `concept_id`, jų spec failai taip pat tampa `stale_review`.

### Jei pasikeičia claim
#### `citation_only`
- kanoninis LT skyrius nelaikomas semantiškai pasenusiu;
- `claims/<slug>.yaml` atsinaujina;
- `qa/chapter_status.tsv` pažymima, kad claims sluoksnis buvo atnaujintas;
- mokymosi blokas paprastai neliečiamas, nebent jis aiškiai rodė šaltinio pobūdį.

#### `wording_aligned`
- jei claim santrauka pakeista be semantinio pokyčio, kanoninis LT skyrius gali būti `stale_auto` tik tose vietose, kurios atspindi claim wording;
- mokymosi blokas tampa `stale_auto`, jei jame yra su tuo claim'u susijęs paaiškinimas;
- figūros neliečiamos, nebent claim keičia label'ą ar caption'ą.

#### `support_status_changed`
- atitinkamas kanoninis LT skyrius tampa `stale_review`;
- atidaromas blocker'is `claim_missing_support` arba `lt_eu_conflict`, jei claim nebeturi pakankamos atramos;
- mokymosi blokas negali būti laikomas šviežiu;
- jei claim maitina algoritminę figūrą ar svarbų vizualą, figūros spec taip pat tampa `stale_review`.

#### `clinical_meaning_changed`
- tai automatiškai aukštos rizikos įvykis;
- `chapter_pack`, kanoninis LT skyrius, mokymosi blokas, susijusios figūros ir QA būsena tampa `stale_review`;
- release būsena negali likti `approved`, `sync_ready` ar `synced`; jei bent vienas required gate laukas degraduoja, ji turi grįžti į `not_ready`.

### Jei pataisomas kanoninis LT skyrius
#### `non_semantic_copyedit`
- mokymosi blokas neperregeneruojamas;
- figūros neliečiamos;
- pakanka minimalaus stilistinio / formatavimo QA;
- `release_state` gali likti esamas, jei pakeitimas tikrai ne semantinis.

#### `term_update`
- mokymosi blokas pažymimas `stale_auto`;
- jei terminas naudotas figūrų label'uose ar caption'uose, atitinkamos figūros pažymimos `stale_auto`;
- terminijos QA turi būti paleistas iš naujo;
- jei skyrius buvo `synced` ir required gate laukai po pakeitimo vis dar žali, `obsidian_sync_status` turi būti pažymėtas `outdated_synced_copy`, o `release_state` grąžintas į `sync_ready`.

#### `semantic_local_change`
- mokymosi blokas perregeneruojamas automatiškai;
- figūros tikrinamos tik jei jos priklauso nuo paveikto skyriaus poskyrio ar pavyzdžių;
- `qa_status` grįžta bent į `in_progress`.

#### `high_risk_semantic_change`
- susiję `claims_status` grįžta bent į `in_progress`, o jei reikia žmogaus sprendimo ar atsiranda konfliktas -> į `blocked`;
- atidaromi blocker'iai, jei pakeitimas paliečia norminį teiginį, dozės interpretaciją ar LT/ES konfliktą;
- mokymosi blokas tampa `stale_review` arba `stale_auto` priklausomai nuo to, ar reikia papildomo žmogaus sprendimo;
- susijusios figūros, kurių `depends_on_claim_ids[]` ar `depends_on_chapter_sections[]` apima pakeistą vietą, tampa `stale_review`;
- jei bent vienas required gate laukas degraduoja, release būsena turi būti sumažinta iki `not_ready`.

#### `structure_change`
- mokymosi blokas visada perregeneruojamas;
- figūrų `embed_targets[]` ir įterpimo vietos turi būti peržiūrėtos;
- jei keičiasi skyriuje figūrų nuorodų logika, atidaromas `figure_reference_change` blocker'is arba tiesioginis refresh.

#### `figure_reference_change`
- ne visada reikia keisti kanoninio LT turinį plačiau, bet figūrų pipeline turi būti paleistas iš naujo bent tam susijusiam `figure_id`;
- mokymosi blokas pažymimas `stale_auto`, jei jame figūra taip pat naudojama.

### Kada mokymosi blokas perregeneruojamas automatiškai
Mokymosi blokas turi būti automatiškai perregeneruojamas, jei:

- pasikeitė kanoninio LT skyriaus semantinis turinys;
- pasikeitė terminas, kuris naudojamas mokymosi bloke;
- pasikeitė claim, nuo kurio tiesiogiai priklauso mokymosi bloko paaiškinimas;
- pasikeitė figūra, kuri įterpta į mokymosi bloką.

Mokymosi blokas neturi būti automatiškai perregeneruojamas, jei:

- pakeitimas tik stiliaus ar formatavimo lygio;
- pakeitimas nekeičia jokios mokymosi bloko semantinės vietos.

### Kada figūros perrenderuojamos automatiškai
Figūros turi būti automatiškai perrenderuojamos tik jei:

- pasikeitė jų spec failas;
- pasikeitė `lt_caption` ar `labels[]` dėl termino atnaujinimo;
- pasikeitė Mermaid tarpinis modelis;
- pasikeitė figure embed vieta ir reikia naujo export / crop / frame parinkimo.

Figūros negali būti automatiškai perrenderuojamos, jei:

- pasikeitimas aukštos rizikos ir keičia klinikinę algoritminę logiką;
- reikia žmogaus sprendimo dėl supaprastinimo ar lokalizacijos politikos;
- MCP preflight ar export pipeline yra `blocked` būsenoje.

### `qa/chapter_status.tsv` poveikio taisyklės
Minimalios peržymėjimo taisyklės:

- term change -> `terminology_status = in_progress`, o jei reikia žmogaus sprendimo ar yra blocker'is -> `blocked`;
- claim change -> `claims_status = in_progress`, o jei support konfliktas neleidžia tęsti -> `blocked`;
- canonical LT semantic change -> `canonical_lt_status = in_progress`, `qa_status = in_progress`;
- learning block stale -> `learning_block_status = in_progress`;
- figure stale -> `figures_status = in_progress`, jei figūra reikalinga;
- bent vienas required gate laukas nėra `passed` arba `not_required` -> `release_state = not_ready`;
- synced chapter repo pakeitimas, kai required gate laukai lieka žali -> `obsidian_sync_status = outdated_synced_copy`, `release_state = sync_ready`.

### Kodėl šitas grafas būtinas
Be formalaus priklausomybių / perregeneravimo grafo agentai darys vieną iš dviejų blogų dalykų:

- arba perregeneruos per daug ir kels bereikalingą churn;
- arba paliks pasenusius sluoksnius, kurie atrodys žali, nors iš tikro jau konfliktuoja su nauja kanonine būsena.

## Obsidian architektūra
### Vaidmuo
Iki šio taško buvo užfiksuota tik aukšto lygio taisyklė, kad Obsidian yra vienakryptė sinchronizuota skaitymo ir mokymosi aplinka.

Pagrindiniai principai:

1. Obsidian nėra kanoninis šaltinis. Jis yra skaitymo ir mokymosi kopija.
2. Vault struktūra turi būti patogi žmogui skaityti, bet ir pakankamai stabili agentinei sinchronizacijai.
3. Kanoninis LT skyrius ir mokymosi blokas turi būti laikomi greta, bet ne viename faile.
4. Figūros turi būti laikomos taip, kad markdown nuorodos būtų stabilios ir nereikėtų ranka taisyti kelių po kiekvieno sync.
5. Failų pavadinimai turi būti stabilūs, nuspėjami ir vienodi tarp repo bei Obsidian, kad agentai lengvai rastų porinius artefaktus.

### Vault struktūra v1
```text
  <Vault>/Medical Books/<book_slug>/
  00 Book Home.md
  01 Chapter Index.md
  10 Canonical LT/
    <slug>.md
  20 Learning/
    <slug>.md
  30 Figures/
    figure-<id>.png
    figure-<id>.svg
```

### Sync mapping
- `books/<slug>/lt/chapters/<chapter>.md` -> `<Vault>/Medical Books/<slug>/10 Canonical LT/<chapter>.md`
- `books/<slug>/lt/learning/<chapter>.md` -> `<Vault>/Medical Books/<slug>/20 Learning/<chapter>.md`
- `books/<slug>/lt/figures/rendered/<figure>.png` -> `<Vault>/Medical Books/<slug>/30 Figures/<figure>.png`
- `books/<slug>/lt/figures/exported/<figure>.svg` -> `<Vault>/Medical Books/<slug>/30 Figures/<figure>.svg`
- papildomai sistema gali generuoti `00 Book Home.md` ir `01 Chapter Index.md`

### Kodėl būtent toks išdėstymas
#### `00 Book Home.md`
Tai knygos landing page Obsidian'e.

Jame gali būti:

- knygos pavadinimas;
- trumpa knygos paskirtis;
- būsena;
- nuorodos į Chapter Index;
- nuorodos į pirmą / paskutinį užbaigtą skyrių;
- trumpa pastaba, kad repo yra vienintelis kanoninis šaltinis.

#### `01 Chapter Index.md`
Tai žmogui patogus navigacinis indeksas Obsidian'e.

Jame turi būti:

- skyrių sąrašas;
- nuorodos į kanoninį LT sluoksnį;
- nuorodos į mokymosi bloką;
- aiški pora tarp abiejų sluoksnių.

#### `10 Canonical LT/`
Čia laikomi tik kanoniniai LT skyriai.

Tai leidžia:

- skaityti knygą kuo arčiau „tikros knygos“ logikos;
- neplakti didaktinio sluoksnio su kanoniniu tekstu;
- turėti švarią vietą, jei vartotojas nori skaityti tik kanoninį vertimą.

#### `20 Learning/`
Čia laikomi tik mokymosi blokai.

Tai leidžia:

- atskirai mokytis iš didaktinio sluoksnio;
- greitai pereiti per mokymosi versijas neprarandant ryšio su kanoniniu skyriumi;
- per Obsidian naudoti atskirus mokymosi darbo srautus.

#### `30 Figures/`
Čia laikomos visos šios knygos galutinės figūrų išvestys.

Tai leidžia:

- turėti stabilias relative nuorodas tiek iš `10 Canonical LT`, tiek iš `20 Learning`;
- nenaudoti atskirų figūrų kopijų kiekviename skyriuje;
- išvengti perteklinio asset dubliavimo vault viduje.

### Ar kanoninis LT ir mokymosi blokas turi eiti greta
Taip.

Bet „greta“ reiškia ne tame pačiame faile, o:

- tas pats `chapter_slug`;
- du atskiri failai;
- du atskiri aplankai.

### Figūrų laikymo taisyklė Obsidian'e
- viena galutinė figūra = vienas bendras asset;
- figūros neturi būti dubliuojamos po skyrių aplankus;
- visi skyrių ir mokymosi blokų markdown failai turi remtis tais pačiais assetais iš `30 Figures/`;
- failo vardas turi sutapti su repo `figure_id`;
- pageidaujama pirminė išvestis yra PNG, o vektorinė versija gali būti papildoma, jei naudinga.

### Failų pavadinimų politika Obsidian'e
#### Knygos aplankas
Naudojamas stabilus `book_slug`, ne vien žmogui gražus, bet nestabilus pavadinimas.

#### Skyrių failai
Naudojamas stabilus `<chapter_slug>.md` modelis, nes chapter numeris repo ir Obsidian failų varduose nėra kanoninio file stem dalis.

#### Home ir index failai
Naudojami stabilūs pavadinimai:

- `00 Book Home.md`
- `01 Chapter Index.md`

#### Figūrų failai
Naudojamas `figure_id`, ne laisvas caption ar žmogaus sugalvotas vardas.

### Obsidian sync kelio kontraktas
Repo pusė turi tiksliai žinoti, į kokį vault kelią ir kokiu pavadinimu keliauja kiekvienas leistinas artefaktas. Sync negali remtis vien rankiniu browse kiekvieną kartą.

Šie failai laikomi sync išvesties dalimi, ne rankinio darbo objektais.

### Ko Obsidian vault struktūra neturi daryti
- neturi tapti antru kanoninės tiesos centru;
- neturi dubliuoti `research`, `claims`, `blockers`, `decisions`, techninių schemų ar dependency indeksų;
- neturi priimti `research`, `claims`, `blockers`, `decisions` ar kitų techninių artefaktų pagal nutylėjimą;
- neturi laužyti ryšio tarp repo identifikatorių ir vault failų vardų.

### Kodėl ši struktūra logiška būtent šitam projektui
Ji atitinka visus jau priimtus principus:

- repo lieka vienintelis kanoninis šaltinis;
- Obsidian saugo abu vartotojui svarbius sluoksnius;
- kanoninis LT ir mokymosi blokas yra aiškiai atskirti;
- figūros turi vieną bendrą stabilų asset sluoksnį;
- sync pipeline gali būti deterministinis ir agentams lengvai valdomas.

## V1 vykdymo riba
Oficiali v1 vykdymo riba:

- `local desktop-first`;
- oficiali pirminė aplinka yra vartotojo `macOS` workstation;
- pagrindinis vykdymas turi vykti lokaliai vartotojo kompiuteryje, ne serveryje ir ne headless cloud aplinkoje.

Tai reiškia:

- `Whimsical Desktop MCP` laikomas lokalaus desktop backendu;
- `Obsidian` sync laikomas lokalia desktop integracija;
- CI ir nuotolinė vykdymo aplinka negali būti laikomi pilnais pakaitalais lokaliam vykdymui.

### GitHub vaidmuo
`GitHub` vaidmuo šiame projekte:

- commit istorija;
- diff peržiūra;
- rollback galimybė;
- švarių pakeitimų sekimas;
- saugi nuotolinė atsarginė repo kopija.

Svarbi taisyklė:

- `GitHub` nėra kanoninė vykdymo būsena;
- kanoninė vykdymo būsena vis tiek gyvena repo artefaktuose pačiame projekte;
- `GitHub` yra versionavimo ir atsekamumo sluoksnis, ne alternatyvus workflow state modelis.

### Architektūros neutralumas tarp Mac darbo vietų
Nors v1 orientuota į vartotojo dabartinę `macOS` darbo vietą, sistema turi būti projektuojama taip, kad ją būtų galima perkelti į kitą `Mac` kompiuterį be architektūrinio perrašymo.

Tai reiškia:

- negalima hardkodinti absoliučių workstation kelių į kanoninius failus;
- workstation-specific keliai turi gyventi `repo_config.local.toml` ar kitame lokaliame konfigūracijos sluoksnyje;
- skriptai turi remtis repo-relative keliais, kur tik įmanoma;
- architektūra neturi būti pririšta prie vieno konkretaus `Mac` modelio.

### Perėjimas į kitą Mac ateityje
Sistema turi būti kuriama taip, kad:

- repo būtų galima tiesiog perkelti ar iš naujo atsiklonuoti kitame `Mac`;
- lokali konfigūracija būtų lengvai perrašoma nekeičiant kanoninių artefaktų;
- CLI workflow išliktų tas pats;
- `Whimsical Desktop MCP` ir `Obsidian` integracijoms nereikėtų keisti produkto architektūros, tik workstation-specific nustatymus.

### Ką tai reiškia implementacijai
Iš šios ribos seka konkrečios taisyklės:

- visi svarbūs įrankiai turi turėti CLI-first entrypointus;
- joks kanoninis artefaktas negali priklausyti nuo vienos konkrečios mašinos absoliutaus kelio;
- testuose ir skriptuose reikia vengti prielaidų apie vieną konkretų workstation path;
- `repo_config.local.toml` yra teisinga vieta laikyti Obsidian vault kelią, lokalius eksportų katalogus ir workstation-specific integracijų nustatymus.

### Ko v1 nepasižada
V1 šiame etape nepasižada:

- lygiaverčio `Windows` palaikymo;
- lygiaverčio `Linux` palaikymo;
- pilnai headless serverinio vykdymo figūrų ir Obsidian sluoksniams.
