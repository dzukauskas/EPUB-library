# IMPLEMENTATION_PLAN

## Paskirtis
Šis dokumentas fiksuoja pilnos sistemos statybos seką nuo nulio. Tai nėra MVP planas. Tai yra teisinga pilnos sistemos įgyvendinimo tvarka, kad Codex / OpenCode agentai neprisidarytų architektūrinių skolų.

Svarbus principas:

- projektas neturi būti statomas kaip greitai sulipdytas pirmas variantas, kurį vėliau refaktorizuosime;
- tačiau vis tiek reikia aiškios fazėmis valdomos įgyvendinimo tvarkos, nes kai kurie sluoksniai logiškai priklauso nuo kitų.

## Bazinė įgyvendinimo strategija
Sistema statoma tokia logika:

1. kanoniniai artefaktai ir vykdymo kontraktai
2. EPUB ingest ir chaptering branduolys
3. terminų ir blocker’ių engine
4. kanoninio LT skyriaus generavimo ciklas
5. mokymosi bloko generavimo ciklas
6. figūrų pipeline: schemos ir diagramos per Whimsical Desktop MCP, raster paveikslėliai su tekstu per atskirą lokalizacijos kelią
7. QA, release ir Obsidian sync
8. pilnas hardening su fixtures, acceptance ir realių knygų patikra

## Fazės v1

### Fazė 0 — projekto karkasas ir vykdymo kontraktas
Tikslas:
- sukurti naują repo nuo nulio;
- įtvirtinti bazinę katalogų struktūrą;
- įdiegti Python 3.13+ bazę;
- įtvirtinti `pyproject.toml`, lock failą, konfigūraciją;
- įrašyti produkto specifikaciją, architektūrą ir workflow dokumentus;
- aprašyti artefaktų schemas.

Privalomi rezultatai:
- teisinga repo struktūra;
- `shared/`, `books/`, `src/`, `tests/`;
- artefaktų schemų failai;
- baziniai CLI entrypointų stub'ai;
- bazinis statusų modelis.

Šioje fazėje dar nėra pilno workflow, bet jau yra teisingas architektūrinis karkasas.

### Fazė 1 — EPUB ingest branduolys
Tikslas:
- įdiegti `EPUBLib` backendą;
- įdiegti `EPUBCheck` validation sluoksnį kaip privalomą `prepare-book` preflight;
- sukurti publication/resource/spine/nav vidinį modelį;
- realizuoti `prepare-book`;
- sugeneruoti `chapter_map` proposal artefaktą review etapui;
- sukurti source indeksus ir knygos profilį.

Privalomi rezultatai:
- sistema priima EPUB;
- `prepare-book` visada paleidžia `EPUBCheck`;
- kai `EPUBCheck` CLI sėkmingai paleistas, sistema išsaugo `source/index/epubcheck_report.raw.json` ir `source/index/epubcheck_summary.yaml`;
- sugeneruoja `book.yaml`;
- kai reikia review, sugeneruoja `source/index/toc_review.yaml` kaip siūlomą `chapter_map` artefaktą;
- kai review nereikalingas arba jau užbaigtas, materializuoja approved `chapter_map.yaml`;
- sugeneruoja `source/index/*`;
- gali palikti `qa/chapter_status.tsv` kaip header-only shell be chapter-level eilučių;
- parodo vartotojui skyrių žemėlapį review.

Dar nelaikoma pilna sistema, nes dar nėra vertimo, terminijos ir QA branduolio.

### Fazė 2 — `chapter_pack` + tyrimo sluoksnis
Tikslas:
- realizuoti `start-chapter`;
- realizuoti `build-chapter-pack`;
- realizuoti `research-chapter`;
- įdiegti knygos lygio profilio atnaujinimą;
- sukurti `claims/<slug>.yaml` aukštos rizikos turiniui.

Privalomi rezultatai:
- `start-chapter` gali pirmą kartą materializuoti konkretaus skyriaus `qa/chapter_status.tsv` eilutę su `chapter_state = pack_pending`;
- sistema gali iš patvirtinto `chapter_map` sukurti vykdomą `chapter_pack`;
- `build-chapter-pack` išsprendžia `risk_class` į `high|low` ir perveda registry eilutę į `pack_ready`;
- sistema gali atlikti LT / ES šaltinių paiešką ir užpildyti `research`;
- sistema gali pradėti kurti claim-level atramą.

### Fazė 3 — terminų engine + blocker registration
Tikslas:
- realizuoti `concept_id` modelį;
- realizuoti terminų kandidatų rinkimą;
- realizuoti įrodymų rinkimą ir grading;
- realizuoti blocker’ių registravimą;
- realizuoti auto-promotion ir escalation logikos pagrindus.

Privalomi rezultatai:
- sistema gali aptikti naujus terminus;
- sulyginti juos su globaliu sluoksniu;
- nuspręsti, ar tai globalus lock, lokali išimtis ar kandidatas;
- atidaryti blocker'ius, jei terminas ar lokalizacijos sprendimas neaiškus.

Šioje vietoje sistema jau įgauna sprendimų branduolį.

### Fazė 4 — kanoninio LT skyriaus generavimo ciklas
Tikslas:
- realizuoti `translate-chapter`;
- integruoti `chapter_pack`, `research`, `claims`, terminų sluoksnį ir blocker’ių sluoksnį į vieną vertimo ciklą;
- užtikrinti, kad aukštos rizikos neaiškumai neužsibaigtų tyliai.

Privalomi rezultatai:
- sistema gali sugeneruoti `lt/chapters/<slug>.md`;
- gali sugrįžti į blocker resolution ciklą;
- gali išlaikyti clean kanoninio LT teksto modelį.

Šioje fazėje atsiranda pirmas tikras pilnas kanoninio vertimo kelias vienam skyriui.

### Fazė 5 — mokymosi bloko generavimo ciklas
Tikslas:
- realizuoti `build-learning-block`;
- įtvirtinti pastovaus branduolio + teminių sekcijų logiką;
- įdiegti pavyzdžių politiką;
- įdiegti EN terminų rodymo politiką.

Privalomi rezultatai:
- sistema po kanoninio LT skyriaus sugeneruoja `lt/learning/<slug>.md`;
- mokymosi blokas atitinka produkto taisykles;
- po esminių kanoninio teksto pakeitimų sistema moka pažymėti ar perregeneruoti mokymosi sluoksnį.

Šioje vietoje gaunamas pirmas pilnas dviejų sluoksnių skyriaus modelis.

### Fazė 6 — figūrų pipeline: Whimsical Desktop MCP + raster text localization
Tikslas:
- realizuoti figure discovery -> triage -> spec -> backend selection -> render / localize -> export -> validation -> embed ciklą;
- įdiegti Whimsical Desktop MCP preflight schemų ir diagramų keliui;
- įdiegti Mermaid tarpinį sluoksnį ten, kur jis tinka schemų ir diagramų keliui;
- įdiegti eksportavimo ir hard-case fallback taisykles, įskaitant rankinį Photopea fallback raster keliui.

Privalomi rezultatai:
- svarbios figūros turi kanoninį spec failą;
- schemos ir diagramos gali būti kuriamos / atnaujinamos per `Whimsical Desktop MCP`;
- raster paveikslėliai su tekstu gali būti lokalizuojami per atskirą kelią nepaliekant mixed-language galutinės išvesties;
- sistema gali eksportuoti rezultatą ir įterpti jį į reikiamus sluoksnius;
- figūros gali tapti formaliais blocker'iais.

Šioje fazėje sistema jau pasiekia pilną figūrų politikos modelį.

### Fazė 7 — QA, release ir approval politika
Tikslas:
- realizuoti `qa-chapter`;
- realizuoti release būsenas;
- įdiegti aukštos rizikos review logiką;
- realizuoti `approve-chapter`.

Privalomi rezultatai:
- skyrius nebegali būti laikomas užbaigtu vien „iš akies“;
- `qa-chapter` refreshina jau egzistuojantį chapter execution registry ir nebekonkuruoja su ankstyvu `start-chapter` / `build-chapter-pack` bootstrap keliu;
- agentai turi formalų būdą nuspręsti, ar skyrius tik `release_candidate`, ar jau `approved`.

### Fazė 8 — Obsidian sync sluoksnis
Tikslas:
- realizuoti `sync-obsidian`;
- užtikrinti, kad į vault keliauja tik leistini sluoksniai;
- palikti repo vieninteliu kanoniniu šaltiniu.

Privalomi rezultatai:
- po `approved` skyriaus sistema gali pasiūlyti sync;
- gavus leidimą, sinchronizuoti kanoninį LT skyrių, mokymosi bloką ir figūras;
- joks Obsidian redagavimas netampa kanonine tiesa automatiškai.

### Fazė 9 — hardening ir realių knygų validacija
Tikslas:
- išplėsti fixtures;
- įtraukti realių EPUB knygų acceptance scenarijus;
- ištestuoti edge case'us;
- stabilizuoti terminų ir figūrų pipeline ant realaus korpuso.

Privalomi rezultatai:
- ne tik graži architektūra, bet ir realus patikimumas;
- aiškus sąrašas, kokius EPUB tipus sistema suvaldo gerai, o kokiems vis dar reikia rankinio review.

## Kada sistema laikoma pilnai veikiančia v1
Sistema laikoma pilnai veikiančia v1, kai ji sugeba:
1. priimti EPUB;
2. sugeneruoti ir review'inti `chapter_map`;
3. leisti pradėti 1 skyrių tik po vartotojo leidimo;
4. sugeneruoti `chapter_pack`;
5. atlikti LT / ES tyrimą;
6. valdyti terminų kandidatų, globalių lock'ų ir blocker'ių sluoksnį;
7. sugeneruoti kanoninį LT skyrių;
8. sugeneruoti mokymosi bloką;
9. perdirbti svarbias figūras pagal užrakintą figūrų politiką: schemas ir diagramas per Whimsical Desktop MCP, o raster paveikslėlius su tekstu per atskirą lokalizacijos kelią, nepaliekant mixed-language galutinės išvesties;
10. paleisti QA vartus;
11. gauti vartotojo review ten, kur reikia;
12. pasiūlyti sync į Obsidian.

Pilna sistema formaliai atsiranda ne po Fazės 1 ar 3, o tik tada, kai pasiekiama bent Fazė 8.

## Kodėl vis tiek verta dirbti fazėmis
Fazės čia nereiškia produkto apkarpymo. Jos reiškia tik teisingą pilnos sistemos statybos seką.

To reikia todėl, kad:

- kitaip agentai bandys statyti viską iš karto ir architektūra subyrės;
- kai kurie sluoksniai fiziškai negali būti teisingai padaryti, kol nėra ankstesnių artefaktų;
- fazės leidžia anksti tikrinti, ar architektūra neprasilenkia su realiu vykdymu.

## Rekomenduojamos įgyvendinimo bangos
### Banga 1
Fazė 0 + Fazė 1 + Fazė 2:
- repo karkasas;
- artefaktų schemos;
- `EPUBLib` ingest;
- `EPUBCheck` preflight validation;
- `chapter_map` generavimas ir review paruošimas;
- `book.yaml`;
- `chapter_pack`;
- `research` ir `claims` pradinis sluoksnis.

Kodėl būtent taip:

- be šito dar nėra ant ko statyti terminų, vertimo ir figūrų sluoksnių;
- tai yra pats kritinis pamatas visam likusiam workflow.

### Banga 2
Fazė 3 + Fazė 4 + Fazė 5:
- terminų engine;
- blocker resolution bazė;
- kanoninis LT skyrius;
- mokymosi blokas.

Šioje vietoje sistema jau pradeda vykdyti pagrindinę projekto misiją vienam skyriui.

### Banga 3
Fazė 6 + Fazė 7 + Fazė 8 + Fazė 9:
- pilnas figūrų pipeline;
- QA ir release policy;
- Obsidian sync;
- hardening ant realių knygų.

## Ką svarbiausia perduoti Codex / OpenCode agentams
Šis perdavimo paketas aprašo statomą v1 scaffold logiką; agentai neturi manyti, kad visas target medis jau pilnai materializuotas dabartiniame working tree.

Agentams turi būti perduota bent:
- `project_constitution.md`
- `product_spec.md`
- `architecture.md`
- `agent_system.md`
- `implementation_plan.md`
- taisyklė, kad negalima improvizuoti prieš jau priimtus sprendimus.
