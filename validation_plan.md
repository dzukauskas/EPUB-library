# VALIDATION_PLAN

## Paskirtis
Šis dokumentas apibrėžia, kaip bus tikrinama, ar sistema realiai veikia pakankamai patikimai. Jis skirtas acceptance / validation korpusui, edge case'ams ir minimaliam pasitikėjimo slenksčiui v1 etapui.

## Validation korpuso kūrimo principai

### 1. Testuoti ne tik „švarius“ EPUB
Validation korpusas turi apimti ne tik tvarkingas knygas, bet ir problemas, kurios realiai laužo workflow:
- kreivas TOC;
- keli skyriai viename XHTML faile;
- multi-anchor skyriai;
- appendix / glossary / references sumaišyti su body;
- sudėtingos lentelės;
- figūros su įvairiu caption modeliu;
- netolygus numeravimas;
- mišrus frontmatter / bodymatter.

Šiame validation sluoksnyje turi būti fiksuojami ne tik faktiniai ingest rezultatai, bet ir `EPUBCheck` signalai, nes jie duoda papildomą input kokybės vaizdą dar prieš chaptering.

### 2. Testuoti ne tik ingest, bet pilną kelią
Korpusas turi būti tikrinamas ne vien EPUB ingest etape.

Reikia bent trijų sluoksnių:
- ingest ir `chapter_map`;
- vieno skyriaus pilnas vertimo kelias;
- figūrų / blocker / QA / sync sąveika.

### 3. Validation turi būti dviejų tipų
#### A. Sintetiniai fixture EPUB
- maži, tiksliniai, kontroliuojami;
- skirti vienam edge case testuoti;
- kiekvienam fixture turi būti matoma, ar `EPUBCheck` rezultatas dera su realiu ingest elgesiu.

#### B. Realūs EPUB iš tikrų knygų
- skirti tikram sistemos patikimumui įvertinti;
- naudojami acceptance lygyje;
- turi palikti ne tik galutinį workflow rezultatą, bet ir `EPUBCheck` summary signalą kaip papildomą input kokybės artefaktą.

## Siūlomas validation planas v1

### Validation rinkinys A — sintetiniai fixture EPUB
Minimaliai reikėtų turėti bent šiuos fixture tipus:

1. **Clean linear EPUB**
   - aiškus TOC
   - aiškus spine
   - paprastos figūros

2. **Fragment-heavy EPUB**
   - keli `nav` entry į tą patį failą su skirtingais fragmentais

3. **Spine-first fallback EPUB**
   - netvarkingas ar nepakankamas TOC
   - aiškus body pagal heading'us

4. **Mixed body/appendix EPUB**
   - body chapter'iai sumaišyti su glossary / appendix / references

5. **Table-heavy EPUB**
   - paprastos ir sudėtingos lentelės

6. **Figure-heavy EPUB**
   - kelios svarbios figūros, skirtingi caption ir asset modeliai

### Validation rinkinys B — realūs EPUB
V1 minimaliam „pakankamo pasitikėjimo“ slenksčiui šiame dokumente laikomas toks realių EPUB rinkinys:
- bent **3 realios knygos** skirtingo sudėtingumo;
- bent viena santykinai tvarkinga;
- bent viena su problematišku `TOC/spine`;
- bent viena su daugiau figūrų / lentelių / mišresniu struktūriniu turiniu.

## Minimalus „pakankamo pasitikėjimo“ slenkstis v1
Sistema v1 gali būti laikoma pakankamai patikima tik jei:
- visi sintetiniai fixture acceptance scenarijai praeina;
- bent 3 realios EPUB knygos praeina per:
  - paruošimą,
  - `chapter_map` review,
  - bent po 1 pilną skyrių,
  - terminų / blocker / QA ciklą,
  - ir, jei reikia, figūrų pipeline.

Papildoma taisyklė:

- `EPUBCheck` nėra vienintelis acceptance kriterijus, bet validation metu jo signalai turi būti registruojami ir lyginami su realiu ingest / `chapter_map` rezultatu;
- `EPUBCheck` `blocking` radiniai turi sutapti su tais atvejais, kur sistema iš tikro negali saugiai tęsti `prepare-book`;
- `review_flag` lygio radiniai turi būti matomi acceptance medžiagoje net tada, kai sistema sugeba tęsti workflow.

## Ko šiame dokumente neturi būti
- neapspręstų produkto politikos klausimų;
- bendrų architektūrinių taisyklių, jau užrakintų kituose dokumentuose;
- promptų architektūros taisyklių;
- artefaktų schemų aprašymų, jei jos jau kanoniškai aprašytos kitur.

## Kaip naudoti šį dokumentą
- nauji acceptance / validation reikalavimai turi būti keliami čia;
- kai validation korpusas detalės, šis dokumentas turi augti ir konkretėti;
- šis dokumentas turi būti gyvas, bet ne maišomas su `OPEN_QUESTIONS.md`, nes validation planas nėra tas pats, kas atviri architektūriniai klausimai.
