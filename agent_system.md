# AGENT_SYSTEM

## Paskirtis
Šis dokumentas apibrėžia promptų ir agentinių instrukcijų architektūrą: globalų promptą, role promptus, resume promptus, decision artifact modelį ir `structured_state` I/O kontraktą.

## Promptų architektūros modelis v1
V1 promptų architektūra remiasi trimis sluoksniais:

1. **vienas bazinis globalus promptas** visam projektui;
2. **atskiri rolių overlay promptai** pagal agento funkciją;
3. **atskiri resume promptai** būsenos atkūrimui ir tęsimui.

Ši struktūra pasirinkta todėl, kad:
- nekintančios projekto taisyklės neturi būti dubliuojamos kiekviename role prompt'e;
- rolės turi turėti savo siaurą vykdymo kontraktą;
- resume logika turi būti atskirta nuo darbo logikos.

Promptai laikomi repo viduje:

```text
shared/prompts/
  base/
    global_system_prompt.md
  roles/
    book_preparation.md
    chapter_pack.md
    research_localization.md
    translation.md
    blocker_resolution.md
    learning_block.md
    figure_pipeline.md
    qa_release.md
    obsidian_sync.md
  resume/
    resume_book_preparation.md
    resume_translation.md
    resume_blocker_resolution.md
    resume_figures.md
    resume_qa.md
    resume_obsidian_sync.md
```

## Bazinis globalus promptas
### Paskirtis
Bazinis globalus promptas yra visos sistemos „konstitucinis“ sluoksnis.

### Kanoninė struktūra
1. `Rolė ir misija`
2. `Kanoninė tiesa ir būsenos atkūrimas`
3. `Produkto sluoksnių modelis`
4. `Lokalizacijos politika`
5. `Terminų politika`
6. `Blocker'ių ir review politika`
7. `Žmogaus sprendimų interpretavimo taisyklė`
8. `Darbo ribos ir vykdymo aplinka`
9. `Artefaktų ir priklausomybių taisyklė`
10. `Stiliaus ir elgesio draudimai`
11. `Privalomas darbo modelis prieš vykdymą`

### Ką jis turi apimti
- projekto misiją;
- kanoninę tiesą ir state modelį;
- LT / ES-first lokalizacijos taisykles;
- terminų ir `concept_id` politiką;
- blocker'ių / review logiką;
- taisyklę, kad neaiškumai privalomai tikrinami internete;
- taisyklę, kad vartotojo laisvas tekstas turi virsti decision artifact'u prieš tęsiant workflow.

### Ko jis neturi turėti
- konkrečios vienos rolės veiksmų sekos;
- vieno konkretaus artefakto schemos detalės;
- vienos komandos sintaksės.

### Bazinio global prompto formatas
Bazinis globalus promptas turi būti laikomas viename versionuojamame failo artefakte:

- `shared/prompts/base/global_system_prompt.md`

Jo turinys turi būti:

- žmogui skaitomas;
- kuo mažiau dubliuojantis kitus failus;
- orientuotas į nekintamas taisykles.

V1 taisyklė:

- vienas globalus promptas = vienas versionuojamas repo failas;
- jis neturi būti generuojamas dinamiškai iš kelių šaltinių.

### Ką role promptai iš jo paveldi
Kiekvienas role overlay promptas turi laikyti šį bazinį promptą jau galiojančiu.

Tai reiškia:

- role promptas neturi iš naujo kartoti projekto misijos ar LT / ES politikos;
- role promptas gali remtis tuo, kad globalus promptas jau įkrovė bendrąsias taisykles.

### Kodėl bazinio global prompto skeletas būtinas
Be tikslaus bazinio global prompto skeleto agentai pradėtų:

- vieni per daug dubliuoti taisykles role promptuose;
- kiti išmesti svarbias nekintamas ribas;
- o resume ir role promptai palaipsniui pradėtų skirtis savo projekto supratimu.

## Role promptų taisyklės
### Bendri principai
- role promptai turi būti **kuo trumpesni**;
- jie neturi dubliuoti bazinio globaliojo prompto ar artefaktų semantikos;
- jie turi aiškiai apibrėžti konkrečios rolės vykdymo kontraktą.

### Role prompto kanoninė struktūra
1. `Rolės tikslas`
2. `Privalomi įėjimo artefaktai`
3. `Leidžiamas rašymo paviršius`
4. `Vykdymo seka`
5. `Eskalacijos ribos`
6. `Privaloma žmogui skaitoma išvestis`
7. `Privalomas structured_state YAML`
8. `Baigimo kriterijus`

### Role prompto sekcijų detalizacija
#### `1. Rolės tikslas`
Turi aiškiai atsakyti:

- ką ši rolė turi pasiekti;
- kokio sluoksnio ji liesti neturi;
- kur jos darbo riba baigiasi.

#### `2. Privalomi įėjimo artefaktai`
Turi būti dvi klasės:

- `required_inputs[]`
- `conditional_inputs[]`

Role promptas negali vartoti miglotos frazės „perskaityk, kas susiję“. Jis turi įvardyti konkrečius artefaktus ar artefaktų klases.

#### `3. Leidžiamas rašymo paviršius`
Turi būti bent:

- `writable_artifacts[]`
- `conditionally_writable_artifacts[]`
- `forbidden_artifacts[]`

Tai negali būti palikta interpretacijai.

#### `4. Vykdymo seka`
Ši sekcija turi būti ne ilga teorija, o trumpas vykdymo algoritmas:

1. perskaityk privalomus artefaktus;
2. patikrink būseną ir freshness;
3. jei reikia, atidaryk blocker'į ar sustok;
4. jei sąlygos tenkinamos, įrašyk leistinus artefaktus;
5. grąžink išvestį pagal role output šabloną.

#### `5. Eskalacijos ribos`
Turi tiksliai nurodyti:

- kokios sąlygos automatiškai veda į blocker'į;
- kada reikia vartotojo sprendimo;
- kada reikia kitos rolės įsikišimo.

#### `6. Privaloma žmogui skaitoma išvestis`
Minimalus karkasas turi apimti:

- ką rolė perskaitė;
- ką padarė;
- ką pakeitė arba siūlo pakeisti;
- ar atidarė blocker'ių;
- ar reikia vartotojo patvirtinimo;
- koks kitas žingsnis.

#### `7. Privalomas structured_state YAML`
Kiekvienas role promptas turi nurodyti:

- bendrą privalomą branduolį;
- kokius papildomus role-specific laukus leidžiama ar privaloma grąžinti.

#### `8. Baigimo kriterijus`
Role completion nėra tas pats, kas viso skyriaus approval.

Baigimo kriterijus turi aiškiai apibrėžti, kad:

- artefaktas įrašytas arba formaliai pasiūlytas;
- blocker'is atidarytas arba uždarytas, jei to reikėjo;
- `structured_state` grąžintas;
- kitas žingsnis aiškiai nustatytas.

### Ko role promptas neturi turėti
- pilnos projekto misijos perrašymo;
- pilnos LT / ES politikos dubliavimo;
- visų artefaktų schemų dubliavimo;
- visų kitų rolių atsakomybės aprašymo;
- neapibrėžtų frazių, pvz. „jei atrodo logiška, padaryk savaip“.

### Role promptų failų vardynas
Naudojami stabilūs snake_case vardai:
- `book_preparation.md`
- `chapter_pack.md`
- `research_localization.md`
- `translation.md`
- `blocker_resolution.md`
- `learning_block.md`
- `figure_pipeline.md`
- `qa_release.md`
- `obsidian_sync.md`

Vengti:

- skirtingų sinonimų tam pačiam vaidmeniui;
- failų vardų, kurie skiriasi nuo rolių pavadinimo dokumentacijoje.

### Kodėl role promptų skeletas būtinas
Be tikslaus role promptų skeleto agentai pradėtų:

- skirtingoms rolėms naudoti nevienodą išvesties logiką;
- pamiršti svarbias eskalacijos ribas;
- neaiškiai suprasti, kokius artefaktus jie gali liesti;
- grąžinti skirtingo formato atsakymus, kuriuos sunku pernaudoti kitoms rolėms.

### Role promptų minimalūs I/O kontraktai
Visi role promptai turi remtis bendra I/O logika.

#### Input kontraktas
Role promptas turi aiškiai įvardyti:
- privalomus input artefaktus;
- sąlyginius input artefaktus;
- privalomą būsenos patikrą prieš darbą.

#### Output kontraktas
Role promptas turi privalomai grąžinti:
- `human_summary`
- `structured_state`

Ir, jei taikoma:
- siūlomą decision artifact draft;
- siūlomą blocker'į;
- siūlomą refresh / stale pažymėjimą.

### Role-specific papildomi laukai
Nors bazinė struktūra visoms rolėms vienoda, kai kurioms rolėms reikia papildomų `structured_state` laukų.

#### `book_preparation`
Papildomai gali reikalauti:
- `chapter_map_confidence`
- `chapter_map_review_required`
- `book_profile_written`

#### `chapter_pack`
Papildomai gali reikalauti:
- `pack_written`
- `required_sections`
- `optional_sections_enabled`
- `optional_sections_disabled`
- `not_allowed_sections`
- `risk_flags`
- `new_term_candidates_count`

Šios keturios sekcijų grupės turi naudoti tik kanoninius `learning_section_id` iš `ARCHITECTURE.md`, ne LT heading'us ir ne role-local sinonimus.

#### `research_localization`
Papildomai gali reikalauti:
- `lt_sources_checked_count`
- `es_sources_checked_count`
- `claims_created`
- `required_claim_refs_materialized[]`
- `required_claim_refs_blocked[]`
- `localization_conflicts_found`

Šioje rolėje `claims_created` reiškia, kiek `chapter_pack.required_claims[]` claim coverage / obligation descriptor vienetų buvo materializuota į claims sluoksnį, o ne kiek jau egzistuojančių `claim_id` buvo perskaityta iš įėjimo artefakto. Vien `claims_created` skaičiaus nepakanka coverage closure įrodyti: tam turi likti persisted lineage per `claims[].required_claim_ref` ir, jei descriptor dar neuždengtas, per `blockers[].required_claim_refs[]`.

#### `translation`
Papildomai gali reikalauti:
- `canonical_chapter_written`
- `new_blockers_opened`
- `term_candidates_appended`

#### `blocker_resolution`
Papildomai gali reikalauti:
- `blockers_processed`
- `blockers_resolved`
- `blockers_escalated`
- `decision_artifact_drafts`

#### `learning_block`
Papildomai gali reikalauti:
- `learning_block_written`
- `required_sections_rendered`
- `optional_sections_enabled_rendered`
- `optional_sections_disabled`
- `not_allowed_sections`

Šių laukų semantika:
- `required_sections_rendered` ir `optional_sections_enabled_rendered` raportuoja realiai sugeneruotų sekcijų kanoninius `learning_section_id`;
- `optional_sections_disabled` ir `not_allowed_sections` raportuoja kanoninius `learning_section_id`, kurie šiame skyriuje nebuvo generuoti dėl planning-state sprendimo;
- `structured_state` neturi inventinti alternatyvaus sekcijų vardyno ar grąžinti LT heading'ų vietoj kanoninių ID.

#### `figure_pipeline`
Papildomai gali reikalauti:
- `figure_specs_written`
- `figures_rendered`
- `figures_exported`
- `figures_blocked`

#### `qa_release`
Papildomai gali reikalauti:
- `qa_checks_run`
- `release_state`
- `user_review_required`

#### `obsidian_sync`
Papildomai gali reikalauti:
- `sync_offered`
- `sync_applied`
- `synced_artifacts`
- `obsidian_sync_status`

## Resume promptų taisyklės
### Bendri principai
- resume promptas nėra darbo prompto kopija;
- jo tikslas — atkurti patikimą vykdymo būseną iš artefaktų;
- jis negali leisti tęsti darbo ant spėjimo ar pasenusio konteksto.

### Resume prompto kanoninė struktūra
1. `Resume tikslas`
2. `Privalomi state šaltiniai`
3. `Skaitymo tvarka`
4. `Būsenos atkūrimo algoritmas`
5. `Būsenos sutikrinimas ir konfliktų paieška`
6. `Kada negalima tęsti`
7. `Resume rezultatas žmogui`
8. `Privalomas structured_state YAML`
9. `Resume baigimo kriterijus`

### Resume promptų specializacija
Skirtingi resume promptai turi skirtingus privalomus state šaltinius:
- `resume_book_preparation`
- `resume_translation`
- `resume_blocker_resolution`
- `resume_figures`
- `resume_qa`
- `resume_obsidian_sync`

### Resume promptų failų modelis
Resume promptai turi būti laikomi atskiruose failuose:

- `shared/prompts/resume/`

Failų vardai turi būti stabilūs ir `snake_case` stiliaus.

### Resume prompto sekcijų detalizacija
#### `1. Resume tikslas`
Turi aiškiai atsakyti:

- ką agentas turi atkurti;
- kokio etapo būseną jis tikrina;
- kokio darbo jis dar neturi pradėti, kol būsena nepatvirtinta.

#### `2. Privalomi state šaltiniai`
Turi būti dvi klasės:

- `required_state_sources[]`
- `conditional_state_sources[]`

Resume promptas negali vartoti miglotos frazės „pažiūrėk, kas svarbu“. Jis turi įvardyti konkrečius artefaktus ar artefaktų klases.

#### `3. Skaitymo tvarka`
Tipinė tvarka turi būti:

1. globalus promptas ir role promptas jau laikomi galiojančiais;
2. pirma skaitomas kanoninis execution state šaltinis:
   - knygos lygiui `book.yaml.status`
   - skyriaus lygiui `qa/chapter_status.tsv` eilutė su `chapter_state`, `risk_class`, gate laukais, `release_state`, `user_review_required`, `user_review_status`, `obsidian_sync_status`, jei to skyriaus registry eilutė jau materializuota; jei eilutės dar nėra, tai reiškia pre-start būseną `not_started`
3. tada skaitomi tiesioginiai vykdymo artefaktai;
4. tada skaitomas freshness sluoksnis: `qa/dependency_index.yaml` ir susiję sidecar `.meta.yaml`, jei jie egzistuoja;
5. tik po to sprendžiama, ar būseną pavyko atkurti.

#### `4. Būsenos atkūrimo algoritmas`
Ši sekcija turi būti vykdomo pobūdžio, pvz.:

1. perskaityk pagrindinį statusų šaltinį;
2. nustatyk paskutinę formalią būseną iš kanoninių state laukų, o ne vien iš artefaktų egzistavimo;
3. patikrink `qa/dependency_index.yaml` ir sidecar `.meta.yaml`, ar reikalingi upstream artefaktai yra `fresh`;
4. patikrink, ar nėra atvirų blocker'ių;
5. nustatyk, ar galima tęsti tą pačią rolę, ar reikia kitos rolės, review ar migracijos.

#### `5. Būsenos sutikrinimas ir konfliktų paieška`
Resume promptas privalo ieškoti bent šių konfliktų:

- execution registry sako viena, bet `qa/dependency_index.yaml` ar sidecar freshness rodo kita;
- yra `stale_review` ar `blocked` sluoksnių;
- susijęs `decision_artifact.status != applied` (bent `draft` arba `awaiting_confirmation`), bet downstream artefaktai jau pakeisti pagal tą sprendimą; tai yra formalus inconsistency / repair atvejis;
- `approved` skyrius po upstream pakeitimo nebėra šviežias;
- Obsidian kopija pasenusi, nors repo jau pasikeitęs.

Jei execution registry ir freshness sluoksnis konfliktuoja, resume rezultatas turi būti `state_consistency = inconsistent`. Jei trūksta kanoninių state laukų, rezultatas turi būti `state_consistency = incomplete`. Resume promptas negali tokio konflikto „sutaisyti“ spėjimu.

#### `6. Kada negalima tęsti`
Resume promptas turi privalomai uždrausti tęsti, jei:

- kanoninės būsenos nepavyksta patikimai atkurti;
- yra schema versijos konfliktas;
- reikalingi artefaktai trūksta ar neatitinka schemos;
- execution registry trūksta kanoninių state laukų;
- yra atvirų blocker'ių, kurie pagal politiką neleidžia tęsti;
- reikalingas vartotojo sprendimas dar negautas;
- upstream pakeitimai pažymėjo sluoksnius `stale_review`, bet jie neperžiūrėti.

#### `7. Resume rezultatas žmogui`
Minimalus žmogui skaitomas rezultatas turi apimti:

- kokią būseną agentas rado;
- kokius artefaktus perskaitė;
- ar būsena atrodo nuosekli;
- ar yra blocker'ių ar stale sluoksnių;
- ar galima tęsti darbą;
- koks tikslus kitas žingsnis.

#### `8. Privalomas structured_state YAML`
Minimalus resume `structured_state` turi bent gebėti perduoti:

- `resume_role`
- `resume_target`
- `state_sources_read[]`
- `reconstructed_state`
- `state_consistency`
- `blocking_conditions[]`
- `can_resume`
- `required_user_action`
- `next_step`

#### `9. Resume baigimo kriterijus`
Resume laikomas užbaigtu tik jei:

- būklė atkurta iš kanoninių artefaktų;
- konfliktai patikrinti;
- aiškiai nustatyta, ar galima tęsti;
- žmogui grąžinta aiški santrauka;
- sugeneruotas `structured_state` YAML.

### Resume promptų specializacija pagal rolę
#### `resume_book_preparation`
Privalo bent skaityti:

- `book.yaml`
- `chapter_map.yaml`, jei approved map jau materializuotas
- `source/index/toc_review.yaml`, jei `chapter_map` review dar neuždarytas
- `source/index/*`
- `qa/chapter_status.tsv`, jei jau egzistuoja

Turi nustatyti:

- koks yra kanoninis `book_state` iš `book.yaml.status`;
- ar egzistuoja unresolved `chapter_map` proposal artefaktas `source/index/toc_review.yaml`;
- ar approved `chapter_map.yaml` jau materializuotas;
- ar galima pereiti į skyriaus starto leidimo būseną.

#### `resume_translation`
Privalo bent skaityti:

- `book.yaml`
- `chapter_map.yaml`
- `chapter_packs/<slug>.yaml`
- `research/<slug>.md`
- `claims/<slug>.yaml`, jei taikoma
- `blockers/<slug>.yaml`, jei egzistuoja
- `lt/chapters/<slug>.md`, jei jau egzistuoja
- `lt/chapters/<slug>.meta.yaml`, jei egzistuoja
- `qa/chapter_status.tsv`
- `qa/dependency_index.yaml`, jei egzistuoja

Turi nustatyti:

- kokia yra kanoninė execution būsena ir persisted `risk_class` iš `qa/chapter_status.tsv`;
- jei to skyriaus registry eilutė neegzistuoja, laikyti tai ne `translation` resume būsena, o ankstesnio lifecycle etapo problema ir nebandyti improvizuoti execution state iš vien artefaktų egzistavimo;
- ar freshness sluoksnis leidžia tęsti darbą;
- ar kiekvienas `chapter_pack.required_claims[]` descriptor yra arba materializuotas per `claims[].required_claim_ref`, arba dar formaliai atsekamas per `blockers[].required_claim_refs[]`;
- ar reikia tęsti vertimą, blocker resolution ar revision ciklą.

#### `resume_blocker_resolution`
Privalo bent skaityti:

- `blockers/<slug>.yaml`
- `research/<slug>.md`
- `claims/<slug>.yaml`, jei taikoma
- `books/<slug>/decisions/*.yaml`, susijusius su tuo skyriumi
- `qa/chapter_status.tsv`
- `qa/dependency_index.yaml`, jei egzistuoja

Turi nustatyti:

- kurie blocker'iai atviri;
- kurie jau išspręsti;
- kurie laukia vartotojo sprendimo;
- kurie `required_claim_refs[]` dar laiko atvirą claim coverage kelią;
- ar execution registry ir freshness sluoksnis leidžia tęsti auto-resolution.

#### `resume_figures`
Privalo bent skaityti:

- `source/index/figures.tsv`
- `lt/figures/specs/*`, susijusius su skyriumi
- `lt/figures/manifest.tsv`
- figūrų meta sluoksnį
- `qa/chapter_status.tsv`
- `qa/dependency_index.yaml`, jei egzistuoja

Turi nustatyti:

- kurios figūros tik atrastos;
- kurios turi spec;
- kurios renderintos;
- kurios užblokuotos;
- ar svarbi figūra neleidžia užbaigti skyriaus pagal execution registry ir freshness sluoksnį.

#### `resume_qa`
Privalo bent skaityti:

- `qa/chapter_status.tsv`
- `qa/dependency_index.yaml`, jei egzistuoja
- visus to skyriaus galutinius sluoksnius:
  - `lt/chapters`
  - `lt/learning`
  - `claims`
  - `blockers`
  - figūrų manifestą

Turi nustatyti:

- ar execution registry rodo `release_state = not_ready`, `release_candidate`, `approved`, `sync_ready` ar `synced`;
- ar reikia vartotojo review pagal `user_review_required` ir `user_review_status`;
- ar freshness sluoksnis konfliktuoja su execution registry;
- ar reikia dar vieno refresh ar rerun.

### Resume promptų draudimai
Resume promptai negali:

- pradėti naujo darbo dar nepatvirtinę būsenos;
- remtis vien chat istorija;
- taisyti artefaktų semantikos pakeliui, jei jų rolė nėra repair ar migrate režimas;
- ignoruoti schema mismatch ar stale būsenų;
- tyliai perkelti workflow į kitą etapą, jei yra atviras žmogaus patvirtinimo taškas.

### Kodėl resume promptų skeletas būtinas
Be tikslaus resume promptų skeleto agentai rizikuotų:

- pradėti tęsti darbą nuo klaidingos vietos;
- neaptikti, kad upstream sluoksniai jau pasenę;
- supainioti `approved`, `stale_review` ir `blocked` būsenas;
- pradėti naują veiksmą prieš gaunant vartotojo sprendimą.

## Versionavimas ir laikymas repo viduje
Promptai turi būti versionuojami repo viduje, ne laikomi tik chat istorijoje.

Siūloma vieta:
- `shared/prompts/`

Šis modelis:
- sumažina taisyklių dubliavimą;
- leidžia keisti projekto „konstituciją“ vienoje vietoje;
- leidžia rolėms būti tikslioms ir siaurų pareigų;
- leidžia resume logiką laikyti atskirai nuo darbo logikos;
- gerai dera su OpenCode / Codex CLI workflow.

## Griežtas išvesties šablonas
Kiekvienas role promptas privalo grąžinti:
- ką perskaitė;
- ką nusprendė;
- kokius artefaktus pakeitė arba siūlo pakeisti;
- ar yra blocker'ių;
- ar reikia vartotojo patvirtinimo;
- koks kitas žingsnis.

Išvestis turi būti **dviguba**:
- žmogui skaitoma dalis;
- aiškiai atskirtas `structured_state` YAML blokas.

## `structured_state` schema v1
### Top-level required laukai
- `output_type`
- `output_version`
- `role`
- `status`
- `execution_scope`
- `artifacts_read[]`
- `artifacts_written[]`
- `blockers[]`
- `requires_user_confirmation`
- `next_step`

### Top-level optional laukai
- `human_summary_ref`
- `warnings[]`
- `stale_artifacts[]`
- `decision_artifact_drafts[]`
- `metrics`
- `role_payload`
- `notes`

Svarbus principas:
- papildomi duomenys negali būti laisvai mėtyti į top-level be schemos;
- role-specific plėtra turi gyventi `role_payload` bloke.

### Leidžiamos `role` reikšmės
- `book_preparation`
- `chapter_pack`
- `research_localization`
- `translation`
- `blocker_resolution`
- `learning_block`
- `figure_pipeline`
- `qa_release`
- `obsidian_sync`
- `resume_book_preparation`
- `resume_translation`
- `resume_blocker_resolution`
- `resume_figures`
- `resume_qa`
- `resume_obsidian_sync`

### Leidžiamos `status` reikšmės
- `success`
- `blocked`
- `needs_user_review`
- `needs_user_decision`
- `failed`

### `execution_scope`
Privalomas objektas:
- `scope_type`
- `scope_ref`

Leistini `scope_type`:
- `book`
- `chapter`
- `blocker`
- `claim`
- `concept`
- `figure`
- `sync`

### `next_step`
Privalomas objektas:
- `step_type`
- `step_ref`

Leistini `step_type`:
- `continue_same_role`
- `handoff_to_role`
- `wait_user_review`
- `wait_user_decision`
- `rerun_role`
- `stop_blocked`
- `offer_sync`
- `no_further_action`

`step_ref` turi nurodyti konkretų kitą veiksmą ar rolę, pvz.:

- `translation`
- `blocker_resolution`
- `approve_chapter`
- `sync_obsidian`
- `user_review`

### `blockers[]` schema
Kiekvienas blocker vienetas turi turėti bent:
- `blocker_id`
- `type`
- `severity`
- `status`
- `summary`
- `requires_user_decision`

Optional:
- `affected_artifacts[]`
- `recommended_action`

Leistinos `severity`:
- `low`
- `medium`
- `high`
- `critical`

Leistinos `status`:
- `open`
- `resolved`
- `escalated`
- `not_applicable`

### Resume role papildomas kontraktas
Jei `role` yra resume klasės, papildomai privaloma:
- `reconstructed_state`
- `state_consistency`
- `can_resume`
- `required_user_action`

Leistinos `state_consistency`:
- `consistent`
- `inconsistent`
- `incomplete`

`required_user_action`:
- `none`
- `review`
- `decision`
- `repair`
- `migration`

### Laukų semantika
#### `artifacts_read[]`
Sąrašas konkrečių artefaktų kelių ar loginio identifikatoriaus objektų, kuriuos agentas faktiškai perskaitė.

Minimalus vieneto modelis:
- `path`
- `artifact_type`

#### `artifacts_written[]`
Sąrašas artefaktų, kuriuos agentas:
- sukūrė,
- pakeitė,
- arba siūlo pakeisti.

Minimalus vieneto modelis:
- `path`
- `artifact_type`
- `write_mode`

Leistinos `write_mode` reikšmės:
- `created`
- `updated`
- `proposed`
- `unchanged`

#### `requires_user_confirmation`
Boolean reikšmė:
- `true`
- `false`

Jei `true`, `status` negali būti traktuojamas kaip pilnai vykdytinas be papildomo žmogaus sprendimo.

### Papildomų laukų schemos
#### `stale_artifacts[]`
Jei laukas naudojamas, kiekvienas vienetas turi turėti bent:
- `path`
- `artifact_type`
- `freshness_status`
- `reason`

Leistinos `freshness_status` reikšmės:
- `stale_auto`
- `stale_review`
- `blocked`

`outdated_synced_copy` neturi būti naudojamas bendrame freshness enum'e. Sync pasenimo signalai turi būti rodomi per `obsidian_sync_status` arba susijusius sync role laukus.

#### `decision_artifact_drafts[]`
Jei role generuoja sprendimo draft'us, kiekvienas vienetas turi turėti bent:
- `decision_type`
- `scope_type`
- `scope_ref`
- `risk_level`
- `requires_confirmation`
- `target_path`

Semantika:
- `decision_artifact_drafts[]` yra tik reporting / proposal mechanizmas;
- jis niekada nėra kanoninis lifecycle state ar resume truth source;
- vien `decision_artifact_drafts[]` negali unlock'inti workflow tęsinio ar apply;
- jei workflow remiasi kanoniniu decision draft'u, jis turi egzistuoti repo kaip `books/<book_slug>/decisions/<decision_id>.yaml`;
- jei `target_path` yra tik siūlomas, o failas dar neįrašytas, tai yra proposal-only būsena, ne kanoninis decision state.

#### `metrics`
Jei naudojamas `metrics`, leidžiami tik skaitiniai ar aiškiai enum tipo laukai.

Pavyzdžiai:
- `lt_sources_checked_count`
- `es_sources_checked_count`
- `claims_created_count`
- `blockers_processed_count`
- `figures_rendered_count`

`metrics` negali būti laisvas tekstinis sąvartynas.

#### `role_payload`
`role_payload` yra vienintelė vieta role-specific plėtrai.

Taisyklės:
- role-specific laukai negali būti keliami į top-level be atskiro architektūrinio sprendimo;
- `role_payload` turi būti aiškiai susietas su `role` reikšme;
- vienai rolei leidžiami tik jai priskirti papildomi laukai.
- `role_payload` reporting laukai yra tik execution I-O santrauka ir nepakeičia kanoninės artefaktų schemos iš `ARCHITECTURE.md`.

### Minimalus YAML pavyzdys
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

### Ką agentai turi draudžiamai laikyti `structured_state`
`structured_state` negali būti:
- laisvas prose tekstas YAML viduje;
- vieta kanoninei repo tiesai laikyti vietoj tikrų artefaktų;
- neapribota role-specific inventorizacija be schemos;
- vienintelis šaltinis, iš kurio vyksta resume ar approval, jei repo artefaktai su juo konfliktuoja.

`structured_state` yra vykdymo išvestis, ne kanoninis pakeitimo pakaitalas.

### Kodėl ši schema būtina
Be pilnos `structured_state` schemos agentai vis dar turėtų per daug laisvės:

- kiekviena rolė galėtų grąžinti kitokį YAML;
- orchestration sluoksnis negalėtų stabiliai interpretuoti rezultatų;
- resume promptai nevienodai suprastų būseną;
- žmogui parodyta santrauka ir mašininis blokas galėtų pradėti gyventi atskiras tiesas.

Todėl ši schema yra paskutinis formalus promptų architektūros sluoksnis, reikalingas pilnam uždarymui.

## Decision artifact modelis v1
### Kur gyvena sprendimai
- `books/<book_slug>/decisions/`
- vienas sprendimas = vienas atskiras YAML failas
- kanoninis lifecycle artefaktas yra `books/<book_slug>/decisions/<decision_id>.yaml`

### `decision_id` modelis
- `YYYYMMDD-HHMMSS-<scope>-<short-slug>`

### Kada privalomas decision artifact
- `chapter_map` review
- eskaluoto blocker'io sprendimas
- aukštos rizikos termino promotion / atmetimas
- knygos lygio lokalizacijos išimtis
- aukštos rizikos skyriaus galutinis patvirtinimas
- bet koks vartotojo review, keičiantis politiką

### Techninis source-of-truth
- pilna `decision_artifact` techninė schema, enum'ai, leistini `status` perėjimai, conditional required taisyklės ir apply boundary gyvena `ARCHITECTURE.md`;
- `AGENT_SYSTEM.md` nedubliuoja pilno required laukų sąrašo ir nekonkuruoja su technine schema;
- agentai turi remtis tuo, kad vienintelis kanoninis lifecycle failas yra `books/<book_slug>/decisions/<decision_id>.yaml`, o ne atskiras `decision_draft` artefaktų tipas.

### Agentinė sprendimų taikymo taisyklė
1. vartotojas pateikia laisvą tekstą;
2. sistema sugeneruoja `decision artifact draft` tame pačiame kanoniniame decision failo modelyje;
3. sistema parodo žmogui suprantamą interpretaciją;
4. jei pagal `ARCHITECTURE.md` reikalingas patvirtinimas, agentas sustoja ir laukia aiškaus vartotojo confirmation;
5. jei patvirtinimo nereikia, agentas gali tęsti tik po parodytos interpretacijos ir tik pagal `ARCHITECTURE.md` apply boundary;
6. `structured_state.decision_artifact_drafts[]` naudojamas tik raportuoti arba siūlyti draft'ą, bet ne pakeisti kanoninį lifecycle state;
7. agentas negali inventinti jokio papildomo persistinamo state tarp `awaiting_confirmation` ir `applied`;
8. jei iki `applied` atsiranda daliniai downstream pakeitimai, tai laikoma formalų repair reikalaujančiu inconsistency atveju.

Komandų nuosavybės taisyklė:
- `review-chapter-map approve|revise` valdo `chapter_map` review sprendimo persistinimą;
- `resolve-blockers apply --blocker <id>` valdo eskaluoto blocker'io sprendimo persistinimą;
- `approve-chapter` valdo review-gated chapter approval sprendimo persistinimą;
- read-only komandos pagal nutylėjimą pačios nekuria `decision_artifact`, jei `architecture.md` aiškiai nenustato kitaip.

## Siauras rašymo paviršius
Kiekviena rolė pagal nutylėjimą turi **griežtai apribotą rašymo paviršių**.

Pagrindinė taisyklė:
- **default = siauras rašymo paviršius**;
- **išimtys = tik aiškiai išvardytos role prompt'e arba artefaktų priklausomybių taisyklėse**.

### Praktiniai pavyzdžiai
- `translation` gali rašyti kanoninį LT skyrių ir papildyti terminų kandidatus, bet negali savavališkai keisti globalaus terminų sluoksnio;
- `research_localization` gali rašyti `research` ir `claims`, bet negali pats perrašyti užbaigto kanoninio LT skyriaus be aiškios priklausomos taisyklės;
- `blocker_resolution` gali atnaujinti blocker'ius, `research`, kai kuriuos terminų sluoksnius ir paveiktą LT tekstą, bet negali apeiti aukštos rizikos review politikos;
- `learning_block` gali rašyti tik mokymosi bloką ir jo meta sluoksnius;
- `obsidian_sync` negali keisti kanoninių repo artefaktų.

## Kodėl šis dokumentas svarbus
Be šio sluoksnio agentai pradėtų:
- nevienodai interpretuoti tą pačią architektūrą;
- skirtingoms rolėms naudoti skirtingus išvesties modelius;
- neaiškiai suprasti, kada jie gali tęsti, o kada turi eskaluoti;
- remtis ne artefaktais, o prompto improvizacija.
