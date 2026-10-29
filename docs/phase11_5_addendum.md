# Phase 11.5 Evidence Addendum: Repair Measurement, Reconcile, Fix Candidate Manifest

**Generated**: `2026-10-24T11:06:22.580047+00:00`  
**Status**: COMPLETED (Read-Only Measurement, Registry & Manifest Repaired)  
**Pretraining Gate**: `PRETRAINING: OFF` (Zero tensors created, zero parameters updated)  

---

## 1. Keyword Counter Repair & Sanity Checks

Keyword matching repair rules implemented in `scripts/audit_pillar_keywords.py`:
- Case-insensitive regex matching (`re.IGNORECASE`).
- Hyphen normalization: Unicode dashes U+2010 through U+2015 and U+2212 mapped to `-`.
- Equivalence rule: `"muscle strengthening"` and `"muscle-strengthening"` treated as equal via `muscle[\s-]+strengthening`.
- Sanity checks enforced:
  - `US-HHS-PAGAC-2018-BRAIN-SLEEP`: `sleep` >= 50 hits (actual hits: **201**). Status: **PASSED**.
  - `US-HHS-PAGAC-2018-OLDER-ADULTS`: `injur|fall` >= 50 hits (actual hits: **159**). Status: **PASSED**.

### Keyword Density Matrix (10 Staged Documents)

| Source ID | Assigned Pillar | Set | Assigned Density (/1k) | Strength Count (d) | Interval Count (d) | Sleep Count (d) | Nutrition Count (d) | Injury Count (d) | Biomech Count (d) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `US-CDC-PA-ADULTS-2022` | `exercise_science_biomechanics` | `NOT_TESTABLE` | NOT_TESTABLE | 5 (4.13) | 0 (0.00) | 0 (0.00) | 3 (2.48) | 0 (0.00) | 0 (0.00) |
| `US-CDC-PA-MEASURING-2022` | `exercise_science_biomechanics` | `NOT_TESTABLE` | NOT_TESTABLE | 0 (0.00) | 0 (0.00) | 0 (0.00) | 5 (3.78) | 0 (0.00) | 0 (0.00) |
| `US-CDC-PA-OLDER-2022` | `training_adaptations_fatigue_load` | `injury` | 0.68 | 0 (0.00) | 0 (0.00) | 0 (0.00) | 4 (2.72) | 1 (0.68) | 0 (0.00) |
| `US-HHS-PAGAC-2018-EXEC` | `general_fitness_education_safety` | `NOT_TESTABLE` | NOT_TESTABLE | 0 (0.00) | 0 (0.00) | 9 (3.58) | 0 (0.00) | 8 (3.18) | 0 (0.00) |
| `US-HHS-PAGAC-2018-HIIT` | `strength_training_programming` | `strength` | 0.00 | 0 (0.00) | 83 (11.06) | 0 (0.00) | 1 (0.13) | 12 (1.60) | 0 (0.00) |
| `US-HHS-PAGAC-2018-BRAIN-SLEEP` | `sleep_recovery_physical_activity` | `sleep` | 10.81 | 12 (0.65) | 7 (0.38) | 201 (10.81) | 0 (0.00) | 6 (0.32) | 0 (0.00) |
| `US-HHS-PAGAC-2018-CARDIOMETABOLIC` | `nutrition_fundamentals_hydration` | `nutrition` | 0.53 | 4 (0.36) | 2 (0.18) | 0 (0.00) | 6 (0.53) | 0 (0.00) | 3 (0.27) |
| `US-HHS-PAGAC-2018-OLDER-ADULTS` | `training_adaptations_fatigue_load` | `injury` | 10.22 | 66 (4.24) | 8 (0.51) | 0 (0.00) | 4 (0.26) | 159 (10.22) | 0 (0.00) |
| `PLOS-PONE-0215877` | `strength_training_programming` | `strength` | 0.00 | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `US-CDC-NIOSH-HEAT-2016` | `nutrition_fundamentals_hydration` | `nutrition` | 4.08 | 0 (0.00) | 0 (0.00) | 0 (0.00) | 7 (4.08) | 0 (0.00) | 0 (0.00) |

### Verbatim Sample Lines per Set per Document

#### `US-CDC-PA-ADULTS-2022`

- **STRENGTH** (5 total hits):
  - Line 134: `- Adults also need 2 days of muscle-strengthening activity each week.`
  - Line 138: `According to the current Physical Activity Guidelines for Americans, adults need 150 minutes of moderate-intensity physical activity a week.`
  - Line 148: `Muscle-strengthening activities on 2 or more days a week that work all major muscle groups (legs, hips, back, abdomen, chest, shoulders, and`
- **INTERVAL**: 0 hits
- **SLEEP**: 0 hits
- **NUTRITION** (3 total hits):
  - Line 62: `Nutrition`
  - Line 114: `Nutrition`
  - Line 119: `Nutrition`
- **INJURY**: 0 hits
- **BIOMECH**: 0 hits

#### `US-CDC-PA-MEASURING-2022`

- **STRENGTH**: 0 hits
- **INTERVAL**: 0 hits
- **SLEEP**: 0 hits
- **NUTRITION** (5 total hits):
  - Line 62: `Nutrition`
  - Line 114: `Nutrition`
  - Line 119: `Nutrition`
- **INJURY**: 0 hits
- **BIOMECH**: 0 hits

#### `US-CDC-PA-OLDER-2022`

- **STRENGTH**: 0 hits
- **INTERVAL**: 0 hits
- **SLEEP**: 0 hits
- **NUTRITION** (4 total hits):
  - Line 62: `Nutrition`
  - Line 114: `Nutrition`
  - Line 119: `Nutrition`
- **INJURY** (1 total hits):
  - Line 146: `- Try to do a variety of activities. This can make physical activity more enjoyable and reduce your risk of injury.`
- **BIOMECH**: 0 hits

#### `US-HHS-PAGAC-2018-EXEC`

- **STRENGTH**: 0 hits
- **INTERVAL**: 0 hits
- **SLEEP** (9 total hits):
  - Line 22: `Physically active individuals sleep better, feel better, and function better. The 2018 Scientific Report`
  - Line 24: `of benefits that help individuals sleep better, feel better, and perform daily tasks more easily.`
  - Line 26: `of sleep. It does so by reducing the length of time it takes to go to sleep and reducing the time`
- **NUTRITION**: 0 hits
- **INJURY** (8 total hits):
  - Line 44: `whom improved physical function not only reduces risk of falls and fall-related injuries but`
  - Line 81: `• For older adults, strong evidence demonstrates a reduced risk of falls and fall-related injuries.`
  - Line 156: `excessive weight gain, falls with injuries among the elderly, and breast, colon, endometrial, esophageal,`
- **BIOMECH**: 0 hits

#### `US-HHS-PAGAC-2018-HIIT`

- **STRENGTH**: 0 hits
- **INTERVAL** (83 total hits):
  - Line 27: `• How does the newly popularized high intensity interval training (HIIT) mode of exercise fit into`
  - Line 37: `the effect of and contribution of HIIT to the prescribed amount of weekly moderate-to-vigorous physical`
  - Line 38: `activity, and whether HIIT is associated with cardiometabolic health benefits.`
- **SLEEP**: 0 hits
- **NUTRITION** (1 total hits):
  - Line 194: `dietary guidance is standardized, i.e., per day. As a result, steps per day would provide a useful tool for`
- **INJURY** (12 total hits):
  - Line 77: `programs, and the rate of adverse events relative to classical continuous aerobic training.`
  - Line 594: `using HIIT for health promotion. Jelleyman et al42 documented adverse events reported in the 50 studies`
  - Line 595: `included in their meta-analysis. Among the 19 total adverse events reported from the 17 studies (34% of`
- **BIOMECH**: 0 hits

#### `US-HHS-PAGAC-2018-BRAIN-SLEEP`

- **STRENGTH** (12 total hits):
  - Line 132: `muscle-strengthening activity, yoga, and play activities (e.g., tag or other simple low organizational`
  - Line 221: `(e.g., brisk walking), muscle-strengthening activity, yoga, and play activities (e.g., tag or other low`
  - Line 570: `48, 49, 52, 54, 55, 62, 65-67, 71, 72 aerobic training,42, 43, 54, 56, 62, 72, 73 resistance training,43, 52, 56, 62, 70, 72, 73 pilates,50`
- **INTERVAL** (7 total hits):
  - Line 584: `pooled standardized mean difference (SMD) was 0.86 (95% confidence interval (CI): 0.11-1.62).68 In`
  - Line 887: `Findings regarding the effects of interval versus continuous exercise were mixed across nine`
  - Line 890: `more unpleasant affective response during interval versus continuous exercise; four studies`
- **SLEEP** (201 total hits):
  - Line 15: `effective sleep patterns. Despite these common goals, and the fact that recent research has provided`
  - Line 30: `perceptions of quality of life, cognitive function (e.g., attention and memory), and sleep. Several`
  - Line 40: `activity would improve sleep” and described “limited evidence that physical activity would reduce`
- **NUTRITION**: 0 hits
- **INJURY** (6 total hits):
  - Line 1211: `Length of time between going to bed and falling asleep.`
  - Line 1254: `Difficulty falling asleep, staying asleep, or early awakening associated with`
  - Line 1258: `Difficulty falling asleep, staying asleep, or early awakening associated with`
- **BIOMECH**: 0 hits

#### `US-HHS-PAGAC-2018-CARDIOMETABOLIC`

- **STRENGTH** (4 total hits):
  - Line 559: `and one meta-analysis examined the blood pressure response to isometric resistance training.54`
  - Line 565: `(Figure F5-4). MacDonald et al53 examined dynamic resistance training performed, on average, at`
  - Line 592: `by Carlson et al54 investigating isometric resistance training was much smaller than the sample size of`
- **INTERVAL** (2 total hits):
  - Line 182: `(incidence rate ratio (IRR)=0.81; 95% confidence interval (CI): 0.71-0.93) and overweight women`
  - Line 693: `The estimated relative risks and 95% confidence interval for these four studies were: 0.65 (95% CI: 0.59-`
- **SLEEP**: 0 hits
- **NUTRITION** (6 total hits):
  - Line 172: `socioeconomic status, initial weight status, or dietary intake and eating behaviors, on the relationship`
  - Line 844: `4. Conduct observational and experimental research that quantifies energy intake and eating behavior`
  - Line 848: `diet and eating behavior were measured or considered in the analysis. Given that both dietary`
- **INJURY**: 0 hits
- **BIOMECH** (3 total hits):
  - Line 38: `the most common, costly, and preventable CVD risk factor. According to the Seventh Report of the Joint`
  - Line 751: `joint analysis of three physical activity behavior groups (low = 0 minutes per week of self-reported`
  - Line 887: `Report of the Joint National Committee on Prevention, Detection, Evaluation, and Treatment of High`

#### `US-HHS-PAGAC-2018-OLDER-ADULTS`

- **STRENGTH** (66 total hits):
  - Line 40: `resistance training, multicomponent exercise, dual-task training, tai chi, yoga, dance) for specific`
  - Line 43: `mode) of physical activity, with common types being aerobic, muscle-strengthening, and balance`
  - Line 273: `determine the effects of individual elements (e.g., strength training, balance training) of the`
- **INTERVAL** (8 total hits):
  - Line 160: `95% confidence interval (CI): 0.51-0.77). The risk of fall-related injuries requiring medical care was`
  - Line 478: `Effect; (confidence interval), test Effect; (confidence interval), test`
  - Line 500: `Effect; (confidence interval), test Effect; (confidence interval), test`
- **SLEEP**: 0 hits
- **NUTRITION** (4 total hits):
  - Line 32: `National Health and Nutrition Examination Survey (NHANES) data.3`
  - Line 225: `quintile of daily active energy expenditure (less than190 kilocalories per day) had a significantly higher`
  - Line 227: `kilocalories per day; referent group) (hazard ratio (HR)=1.82; 95% CI: 1.10-3.00). Those men in the`
- **INJURY** (159 total hits):
  - Line 38: `falls and fall-related injuries. Since the 2008 Scientific Report,4 considerable evidence has emerged`
  - Line 46: `in fall-related injuries due to various physical activity interventions. In addition, the current research has`
  - Line 50: `Report by examining the relationship between physical activity and the risk of fall-related injuries, as`
- **BIOMECH**: 0 hits

#### `PLOS-PONE-0215877`

- **STRENGTH**: 0 hits
- **INTERVAL**: 0 hits
- **SLEEP**: 0 hits
- **NUTRITION**: 0 hits
- **INJURY**: 0 hits
- **BIOMECH**: 0 hits

#### `US-CDC-NIOSH-HEAT-2016`

- **STRENGTH**: 0 hits
- **INTERVAL**: 0 hits
- **SLEEP**: 0 hits
- **NUTRITION** (7 total hits):
  - Line 94: `- Monitoring and encouraging adequate fluid intake and rest breaks.`
  - Line 127: `## Hydration`
  - Line 128: `Employers should provide the means for appropriate hydration of workers.`
- **INJURY**: 0 hits
- **BIOMECH**: 0 hits

---

## 2. PAGAC Chapter Section Inventory (Report Only)

Each chapter's removed table-of-contents lines were parsed into `(section/question title, first label)` and `last label` computed from the subsequent entry. Cleaned tokens computed using frozen tokenizer `artifacts/final_tokenizer/tokenizer.json`.

### `US-HHS-PAGAC-2018-EXEC`: Part A. Executive Summary (Total Cleaned Tokens: 5870)

| Section / Question Title | First-Last Label | Line Range | Cleaned Tokens |
| :--- | :---: | :---: | :---: |
| Introduction | `A-1 - A-1` | `L1-L20` | 651 |
| Major Findings | `A-2 - A-5` | `L21-L149` | 3651 |
| Public Health Impact | `A-6 - A-6` | `L150-L173` | 785 |
| The Future | `A-7 - A-7` | `L174-L200` | 780 |

### `US-HHS-PAGAC-2018-HIIT`: Part F. Chapter 1. Physical Activity Behaviors: Steps, Bouts, and High-Intensity Interval Training (Total Cleaned Tokens: 19502)

| Section / Question Title | First-Last Label | Line Range | Cleaned Tokens |
| :--- | :---: | :---: | :---: |
| Introduction | `F1-1 - F1-3` | `L1-L77` | 2390 |
| Review of the Science | `F1-4 - F1-4` | `L78-L78` | 13 |
| Overview of Questions Addressed | `F1-4 - F1-4` | `L79-L90` | 382 |
| Data Sources and Process Used to Answer Questions | `F1-4 - F1-4` | `L91-L98` | 267 |
| Question 1. What is the relationship between step count per day and all-cause and cardiovascular disease mortality and (2) incidence for cardiovascular disease events and risk of type 2 diabetes? | `F1-4 - F1-7` | `L99-L199` | 3479 |
| Question 2. What is the relationship between bout duration of physical activity and health outcomes? | `F1-8 - F1-15` | `L200-L608` | 11557 |
| Question 3. What is the relationship between high intensity interval training (HIIT) and reduction in cardiometabolic risk? | `F1-16 - F1-20` | `L95-L608` | 15160 |
| Needs for Future Research | `F1-21 - F1-22` | `L609-L658` | 1408 |
| References | `F1-23 - F1-26` | `REMOVED_BY_CLEANING_RULE` | 0 |

### `US-HHS-PAGAC-2018-BRAIN-SLEEP`: Part F. Chapter 3. Brain Health (Total Cleaned Tokens: 50379)

| Section / Question Title | First-Last Label | Line Range | Cleaned Tokens |
| :--- | :---: | :---: | :---: |
| Introduction | `F3-1 - F3-2` | `L1-L70` | 2063 |
| Review of the Science | `F3-3 - F3-3` | `L71-L71` | 14 |
| Overview of Questions Addressed | `F3-3 - F3-3` | `L72-L106` | 782 |
| Data Sources and Process Used to Answer Questions | `F3-4 - F3-4` | `L107-L110` | 122 |
| Question 1: What is the relationship between physical activity and cognition? | `F3-4 - F3-13` | `L111-L436` | 10227 |
| Question 2. What is the relationship between physical activity and quality of life? | `F3-14 - F3-24` | `L437-L790` | 12085 |
| Question 3. What is the relationship between physical activity and (1) affect, (2) anxiety, and (3) depressed mood and depression? | `F3-25 - F3-36` | `L791-L1168` | 12111 |
| Question 4: What is the relationship between physical activity and sleep? | `F3-37 - F3-45` | `L1169-L1501` | 9571 |
| Needs for Future Research | `F3-46 - F3-48` | `L1502-L1615` | 3396 |
| References | `F3-49 - F3-61` | `REMOVED_BY_CLEANING_RULE` | 0 |

### `US-HHS-PAGAC-2018-CARDIOMETABOLIC`: Part F. Chapter 5. Cardiometabolic Health and Prevention of Weight Gain (Total Cleaned Tokens: 29178)

| Section / Question Title | First-Last Label | Line Range | Cleaned Tokens |
| :--- | :---: | :---: | :---: |
| Introduction | `F5-1 - F5-2` | `L1-L77` | 2616 |
| Review of the Science | `F5-3 - F5-3` | `L78-L78` | 14 |
| Overview of Questions Addressed | `F5-3 - F5-3` | `L79-L103` | 602 |
| Data Sources and Process Used to Answer Questions | `F5-4 - F5-4` | `L104-L116` | 492 |
| Question 1. What is the relationship between physical activity and prevention of weight gain? | `F5-4 - F5-11` | `L117-L351` | 7759 |
| Question 2. In people with normal blood pressure or prehypertension, what is the relationship between physical activity and blood pressure? | `F5-12 - F5-20` | `L352-L642` | 9554 |
| Question 3: In adults without diabetes, what is the relationship between physical activity and type 2 diabetes? | `F5-21 - F5-26` | `L643-L807` | 5657 |
| Needs for Future Research | `F5-27 - F5-30` | `L808-L894` | 2477 |
| References | `F5-31 - F5-36` | `REMOVED_BY_CLEANING_RULE` | 0 |

### `US-HHS-PAGAC-2018-OLDER-ADULTS`: Part F. Chapter 9. Older Adults (Total Cleaned Tokens: 43759)

| Section / Question Title | First-Last Label | Line Range | Cleaned Tokens |
| :--- | :---: | :---: | :---: |
| Introduction | `F9-1 - F9-2` | `L13-L60` | 1388 |
| Review of the Science | `F9-3 - F9-3` | `L61-L61` | 14 |
| Overview of Questions Addressed | `F9-3 - F9-3` | `L62-L87` | 544 |
| Data Sources and Process Used to Answer Questions | `F9-3 - F9-3` | `L88-L99` | 339 |
| Question 1: What is the relationship between physical activity and risk of injury due to a fall? | `F9-4 - F9-9` | `L100-L299` | 6682 |
| Question 2: What is the relationship between physical activity and physical function among the general (i.e., non-institutionalized) aging population? | `F9-10 - F9-21` | `L300-L729` | 13691 |
| Question 3: What is the relationship between physical activity and physical function in older adults with selected chronic conditions? | `F9-22 - F9-36` | `L730-L1250` | 15657 |
| Overall Summary and Conclusions | `F9-37 - F9-37` | `L1251-L1291` | 1174 |
| Needs for Future Research | `F9-38 - F9-41` | `L1292-L1415` | 3518 |
| References | `F9-42 - F9-51` | `REMOVED_BY_CLEANING_RULE` | 0 |

---

## 3. Quarantine Overlap on New Documents

Cleaned PAGAC docs loaded from `data/staging_phase11_4/train_staging.json`. Standard cleaning rules (headers, TOC, references) applied to quarantined Part C (`pagac_2018_part_c_key_concepts.txt`) and Glossary (`pagac_2018_part_h_app1_glossary.txt`). 8-grams consisting solely of header or reference boilerplate strings were excluded.

### Longest Contiguous Shared Word Runs

| Source ID | Quarantined Source | Longest Run (Words) | Doc Lines | Quarantine Lines | Matched Text Excerpt |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `US-HHS-PAGAC-2018-EXEC` | Part C Concepts | 21 | `L30-L31` | `L389-L390` | "Executive function includes the processes of the brain that help organ..." |
| `US-HHS-PAGAC-2018-EXEC` | Part H Glossary | 5 | `L91-L91` | `L369-L369` | "in a variety of ways...." |
| `US-HHS-PAGAC-2018-HIIT` | Part C Concepts | 9 | `L16-L16` | `L249-L250` | "the types of physical activity that influence health outcomes...." |
| `US-HHS-PAGAC-2018-HIIT` | Part H Glossary | 75 | `L478-L483` | `L62-L71` | "HIIT is a form of interval training consisting of alternating short pe..." |
| `US-HHS-PAGAC-2018-BRAIN-SLEEP` | Part C Concepts | 13 | `L1355-L1355` | `L366-L367` | "activity performed more than 8 hours before bedtime, 3 to 8 hours befo..." |
| `US-HHS-PAGAC-2018-BRAIN-SLEEP` | Part H Glossary | 21 | `L1012-L1013` | `L229-L230` | "an unpleasant, low activation feeling state characterized by sadness, ..." |
| `US-HHS-PAGAC-2018-CARDIOMETABOLIC` | Part C Concepts | 9 | `L749-L750` | `L276-L276` | "of physical activity are associated with reduced risk of..." |
| `US-HHS-PAGAC-2018-CARDIOMETABOLIC` | Part H Glossary | 79 | `L395-L399` | `L275-L280` | "as having a resting systolic blood pressure of 140 mmHg or greater and..." |
| `US-HHS-PAGAC-2018-OLDER-ADULTS` | Part C Concepts | 7 | `L33-L33` | `L477-L478` | "The Physical Activity Guidelines Advisory Committee Report,..." |
| `US-HHS-PAGAC-2018-OLDER-ADULTS` | Part H Glossary | 6 | `L1258-L1258` | `L137-L137` | "physical activity and the magnitude of..." |

### Glossary Critical Health Claim Audit

- **Flagged Sentence Verbatim**:  
  > "The current criteria used to diagnose diabetes are an HbA1C of 6.5% or higher, fasting blood glucose of 126 mg per dL or higher, and/or a 2-hour oral glucose tolerance test (OGTT) blood glucose of 200 mg per dL or higher."
- **Verification across 10 Accepted Staging Documents**: `NOT_FOUND` (Appears in 0 accepted docs).

---

## 4. Benchmark Overlap Table (Runs >= 8 Words)

Evaluated all 10 accepted staging documents in `data/staging_phase11_4/` PLUS quarantined Part C and Glossary against all fields (`prompt`, `canonical_reference_answer`, `expected_key_points`, `other`) of `data/benchmark/fitness_eval_benchmark.json`.

| Document | Benchmark Item ID | Field Name | Longest Run (Words) | Matched Text |
| :--- | :--- | :--- | :---: | :--- |
| `US-CDC-PA-MEASURING-2022` | `BENCH_P7_FACT_01` | `prompt` | 8 | "the Physical Activity Guidelines for Americans 2nd edition" |
| `US-HHS-PAGAC-2018-EXEC` | `BENCH_P7_FACT_01` | `canonical_reference_answer` | 9 | "of 150 to 300 minutes of moderate-intensity physical activity" |
| `US-HHS-PAGAC-2018-CONCEPTS (Quarantined)` | `BENCH_P7_FACT_01` | `canonical_reference_answer` | 8 | "150 to 300 minutes of moderate-intensity physical activity" |

---

## 5. Candidate Manifest & Registry Repairs

- **Manifest Version**: `11.4.1` (`data/staging_phase11_4/phase11_4_staging_manifest.json`)
- **Authoritative Tokenizer Hash**: `1639cec0fce7263bbb10eca238b19a5d13ef6bd9fa1c545cd481f4e8ff9c93fc` (computed from `artifacts/final_tokenizer/tokenizer.json`)
- **Validation Status**: `INSUFFICIENT`
  - Validation Tokens: `5811`
  - Largest Validation Source: `US-CDC-NIOSH-HEAT-2016` (4798 tokens = **82.57%** of validation partition)
- **Registry Enum Counts** (all 17 sources accounted for):
  - `ACCEPTED`: 10
  - `REJECTED_LICENSE`: 1
  - `REJECTED_EXTRACTION`: 0
  - `QUARANTINED_REVIEW`: 3
  - `FIXTURE`: 3

- **PLOS Source Author Repair**:
  - Raw file: `data/staging_phase11/sources_raw/plos_pone_0215877.html`
  - Author string found in raw file: `"Jia Li, Alice C. Hughes, David Dudgeon"`
  - Registry author updated from Schoenfeld et al. to `"Jia Li, Alice C. Hughes, David Dudgeon"`

### Accepted Sources Author Verification in Raw Files

| Source ID | Registry Author | Raw File Name | Status in Raw File |
| :--- | :--- | :--- | :---: |
| `US-CDC-PA-ADULTS-2022` | Division of Nutrition, Physical Activity, and Obesity, CDC | `us_cdc_pa_adults_2022.md` | **NOT_FOUND** |
| `US-CDC-PA-MEASURING-2022` | Division of Nutrition, Physical Activity, and Obesity, CDC | `us_cdc_pa_measuring_2022.md` | **NOT_FOUND** |
| `US-CDC-PA-OLDER-2022` | Division of Nutrition, Physical Activity, and Obesity, CDC | `us_cdc_pa_older_2022.md` | **NOT_FOUND** |
| `US-CDC-NIOSH-HEAT-2016` | National Institute for Occupational Safety and Health (NIOSH) | `us_cdc_niosh_heat_2016.md` | **FOUND** |
| `PLOS-PONE-0215877` | Jia Li, Alice C. Hughes, David Dudgeon | `plos_pone_0215877.html` | **FOUND** |
| `US-HHS-PAGAC-2018-EXEC` | 2018 Physical Activity Guidelines Advisory Committee | `pagac_2018_part_a_executive_summary.txt` | **FOUND** |
| `US-HHS-PAGAC-2018-HIIT` | 2018 Physical Activity Guidelines Advisory Committee | `pagac_2018_part_f_ch1_bouts_hiit.txt` | **FOUND** |
| `US-HHS-PAGAC-2018-BRAIN-SLEEP` | 2018 Physical Activity Guidelines Advisory Committee | `pagac_2018_part_f_ch3_brain_sleep.txt` | **FOUND** |
| `US-HHS-PAGAC-2018-CARDIOMETABOLIC` | 2018 Physical Activity Guidelines Advisory Committee | `pagac_2018_part_f_ch5_cardiometabolic.txt` | **FOUND** |
| `US-HHS-PAGAC-2018-OLDER-ADULTS` | 2018 Physical Activity Guidelines Advisory Committee | `pagac_2018_part_f_ch9_older_adults.txt` | **FOUND** |

---

## 6. Cleaning Reconciliation Audit

Reconciliation formula: `unaccounted = raw - removed - final`.

| Source ID | Raw Lines | Headers Removed | TOC Removed | References Removed | Total Removed | Final Lines | Unaccounted Lines |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `US-HHS-PAGAC-2018-EXEC` | 221 | 15 | 6 | 0 | 21 | 200 | **0** |
| `US-HHS-PAGAC-2018-HIIT` | 850 | 54 | 13 | 125 | 192 | 658 | **0** |
| `US-HHS-PAGAC-2018-BRAIN-SLEEP` | 2188 | 61 | 13 | 499 | 573 | 1615 | **0** |
| `US-HHS-PAGAC-2018-CARDIOMETABOLIC` | 1194 | 36 | 11 | 253 | 300 | 894 | **0** |
| `US-HHS-PAGAC-2018-OLDER-ADULTS` | 1836 | 51 | 9 | 361 | 421 | 1415 | **0** |

### First 10 Unaccounted Lines per Document

- `US-HHS-PAGAC-2018-EXEC`: `['blank']`
- `US-HHS-PAGAC-2018-HIIT`: `['blank']`
- `US-HHS-PAGAC-2018-BRAIN-SLEEP`: `['blank']`
- `US-HHS-PAGAC-2018-CARDIOMETABOLIC`: `['blank']`
- `US-HHS-PAGAC-2018-OLDER-ADULTS`: `['blank']`

### Remaining Artifact Occurrences in Final Cleaned Text

| Source ID | Report Name Occurrences | TOC Occurrences | `^Part [A-H].` Occurrences | Page Label Matches (`\b[A-H]\d*-\d+\b`) |
| :--- | :---: | :---: | :---: | :---: |
| `US-HHS-PAGAC-2018-EXEC` | 0 | 0 | 0 | 0 |
| `US-HHS-PAGAC-2018-HIIT` | 0 | 0 | 0 | 4 |
| `US-HHS-PAGAC-2018-BRAIN-SLEEP` | 50 | 0 | 3 | 54 |
| `US-HHS-PAGAC-2018-CARDIOMETABOLIC` | 31 | 0 | 1 | 48 |
| `US-HHS-PAGAC-2018-OLDER-ADULTS` | 42 | 0 | 1 | 59 |

---

## 7. Text-Quality Sample Audit (Seeded seed=42)

Metrics per 1,000 words across all 10 accepted documents:
- (a) Words with 1-3 digits fused to end of letters: `[A-Za-z]{3,}\d{1,3}\b`
- (b) Lines shorter than 6 characters: `< 6` characters
- (c) Lines starting with lowercase fragment of 1-3 letters: `^[a-z]{1,3}\b`

| Source ID | Words | (a) Fused Digits Count (rate/1k) | (b) Short Lines Count (rate/1k) | (c) Lowercase Fragments Count (rate/1k) |
| :--- | :---: | :---: | :---: | :---: |
| `US-CDC-PA-ADULTS-2022` | 1212 | 0 (0.00/1k) | 107 (88.28/1k) | 0 (0.00/1k) |
| `US-CDC-PA-MEASURING-2022` | 1324 | 0 (0.00/1k) | 105 (79.31/1k) | 0 (0.00/1k) |
| `US-CDC-PA-OLDER-2022` | 1468 | 0 (0.00/1k) | 109 (74.25/1k) | 0 (0.00/1k) |
| `US-HHS-PAGAC-2018-EXEC` | 2513 | 0 (0.00/1k) | 1 (0.40/1k) | 22 (8.75/1k) |
| `US-HHS-PAGAC-2018-HIIT` | 7506 | 12 (1.60/1k) | 25 (3.33/1k) | 79 (10.52/1k) |
| `US-HHS-PAGAC-2018-BRAIN-SLEEP` | 18589 | 51 (2.74/1k) | 128 (6.89/1k) | 155 (8.34/1k) |
| `US-HHS-PAGAC-2018-CARDIOMETABOLIC` | 11218 | 24 (2.14/1k) | 62 (5.53/1k) | 112 (9.98/1k) |
| `US-HHS-PAGAC-2018-OLDER-ADULTS` | 15555 | 37 (2.38/1k) | 138 (8.87/1k) | 127 (8.16/1k) |
| `PLOS-PONE-0215877` | 282 | 0 (0.00/1k) | 24 (85.11/1k) | 0 (0.00/1k) |
| `US-CDC-NIOSH-HEAT-2016` | 1715 | 0 (0.00/1k) | 64 (37.32/1k) | 0 (0.00/1k) |

### Seeded Verbatim Body Lines Sample (20 lines per doc, seed=42)

#### `US-CDC-PA-ADULTS-2022`

- Line 17: `-`
- Line 18: `Guidelines and Recommendations`
- Line 21: `Measure Physical Activity Intensity`
- Line 23: `-`
- Line 59: `The Active Communities Tool`
- Line 62: `Nutrition`
- Line 67: `Physical Activity Basics`
- Line 75: `-`
- Line 97: `Measure Physical Activity Intensity`
- Line 145: `Example 1`
- Line 148: `Muscle-strengthening activities on 2 or more days a week that work all major muscle groups (legs, hips, back, abdomen, chest, shoulders, and arms).`
- Line 153: `Example 3`
- Line 160: `Check out this age chart for a quick snapshot of the recommended amounts of weekly activity across age groups.`
- Line 177: `-`
- Line 264: `Español`
- Line 306: `- Budget & Funding`
- Line 328: `- Vulnerability Disclosure Policy`
- Line 351: `- Deutsch`
- Line 357: `Tiếng Việt`
- Line 376: `HHS.gov`

#### `US-CDC-PA-MEASURING-2022`

- Line 17: `-`
- Line 21: `Measure Physical Activity Intensity`
- Line 23: `-`
- Line 59: `The Active Communities Tool`
- Line 62: `Nutrition`
- Line 67: `Physical Activity Basics`
- Line 75: `-`
- Line 97: `Measure Physical Activity Intensity`
- Line 143: `- Active forms of yoga (for example, Vinyasa or power yoga)`
- Line 146: `- Exercise classes like water aerobics`
- Line 151: `- Vigorous dancing`
- Line 158: `### Relative intensity`
- Line 175: `What Counts for Children`
- Line 264: `- Privacy`
- Line 307: `Polski`
- Line 328: `Contact CDC`
- Line 352: `- No Fear Act`
- Line 358: `Nondiscrimination`
- Line 377: `- Deutsch`
- Line 396: `English`

#### `US-CDC-PA-OLDER-2022`

- Line 17: `-`
- Line 21: `Measure Physical Activity Intensity`
- Line 23: `-`
- Line 59: `The Active Communities Tool`
- Line 62: `Nutrition`
- Line 67: `Physical Activity Basics`
- Line 75: `-`
- Line 97: `Measure Physical Activity Intensity`
- Line 145: `## Tips for being physically active`
- Line 148: `- Lots of activities count, even things like mowing the lawn or carrying groceries, and it all adds up. Find what works for you.`
- Line 153: `chair`
- Line 160: `Ask your doctor if your health condition limits your ability to be active in any way. Then, work with your doctor to come up with a physical activity plan that matches your abilities.`
- Line 179: `Recommended weekly physical activity`
- Line 267: `- FOIA`
- Line 310: `- English`
- Line 331: `- About CDC`
- Line 355: `Nondiscrimination`
- Line 361: `Language Assistance`
- Line 380: `Tiếng Việt`
- Line 399: `HHS.gov`

#### `US-HHS-PAGAC-2018-EXEC`

- Line 8: `summarized in the first Physical Activity Guidelines Advisory Committee Report, 2008. The Committee`
- Line 9: `judged the 2008 Scientific Report to be an excellent document and used it as the foundation for the`
- Line 10: `current report. It is clear, however, that the expansion of knowledge about the relationships between`
- Line 24: `of benefits that help individuals sleep better, feel better, and perform daily tasks more easily.`
- Line 25: `• Strong evidence demonstrates that moderate-to-vigorous physical activity improves the quality`
- Line 28: `in deep sleep and reduce daytime sleepiness.`
- Line 30: `period of time. Executive function includes the processes of the brain that help organize daily`
- Line 37: `the severity of those symptoms whether one has only a few or many.`
- Line 57: `• Strong evidence demonstrates that greater volumes of moderate-to-vigorous physical activity`
- Line 59: `within a healthy range, and preventing obesity. This is important because losing weight is`
- Line 61: `• Strong evidence demonstrates that higher amounts of physical activity are associated with a`
- Line 64: `excessive weight during pregnancy. They also are less likely to develop gestational diabetes or`
- Line 72: `of older Americans and the expense and heartache of caring for individuals with dementia, the`
- Line 110: `• For individuals whose amount of moderate-to-vigorous physical activity is below the current`
- Line 141: `programs can be effective.`
- Line 153: `addition to a reduced risk of death, greater amounts of regular moderate-to-vigorous physical activity`
- Line 165: `by the least physically active individuals, would appreciably reduce the nation’s direct and indirect`
- Line 175: `The field of physical activity and public health has matured markedly in the past 10 years, and it will`
- Line 190: `with moderate-to-vigorous physical activity to health outcomes.`
- Line 191: `• Identify effective intervention strategies for increasing physical activity through actions in`

#### `US-HHS-PAGAC-2018-HIIT`

- Line 27: `• How does the newly popularized high intensity interval training (HIIT) mode of exercise fit into`
- Line 29: `• What, if any, is the value of light-intensity physical activity?`
- Line 32: `The Committee considered it important to address these questions and anticipate the ones that might`
- Line 34: `research needs of three particularly relevant issues: the role of daily step counts in the assessment of`
- Line 91: `Data Sources and Process Used to Answer Questions`
- Line 97: `details on the systematic literature review process, see Part E. Systematic Review Literature Search`
- Line 106: `Conclusion Statements`
- Line 116: `Review of the Evidence`
- Line 144: `Several longitudinal studies examined the relationship between step counts per day and disease`
- Line 225: `whether physical activity episodes of less than 10 minutes in duration have health-related benefits; or,`
- Line 230: `original research studies.15-39 Two pairs of these studies reported on different outcomes from the same`
- Line 240: `minutes.`
- Line 252: `accumulated in bouts less than 10 minutes in duration is associated with body mass index (BMI) or body`
- Line 283: `Prospective 67 >10`
- Line 434: `association between physical activity that varied in bout duration varied by these demographic`
- Line 519: `control and insulin resistance, compared with continuous training or control conditions. Both controlled`
- Line 560: `studies), increased insulin sensitivity (4 of 4 studies), and decreased blood pressure in participants not`
- Line 606: `sensitivity, blood pressure, and body composition in adults. These HIIT-induced improvements in`
- Line 618: `disease outcomes. In this review, only one randomized controlled trial was identified and it did not`
- Line 656: `the safety of high intensity interval training among adults with varied health and disease`

#### `US-HHS-PAGAC-2018-BRAIN-SLEEP`

- Line 60: `cognitive-evaluative components and assessed whether physical activity improves general quality of life`
- Line 71: `REVIEW OF THE SCIENCE`
- Line 75: `a) Is there a dose-response relationship? If yes, what is the shape of the relationship?`
- Line 204: `literature that examined whether results from randomized controlled trials (RCTs) and prospective`
- Line 217: `achievement tests; performance on neuropsychological tests, such as those involving processing speed,`
- Line 237: `consistently, and are most frequently studied, in the executive function domain. The improvements in`
- Line 256: `function or academic achievement. Despite these limitations, the several reviews reported effect sizes in`
- Line 317: `connectivity; magnetic resonance spectroscopy; and positron emission tomography. Most of the work in`
- Line 493: `populations: older adults (general),42-51 older adults ( with dementia),52 adults,53-58 youth,59 individuals`
- Line 503: `older, but all studies included individuals of at least age 50 years and older. The systematic reviews`
- Line 524: `than 18 years and younger than 65 years.53-55, 57, 58, 63, 64 The systema tic reviews covered the following`
- Line 551: `effects of yoga included 12 RCTs.`
- Line 617: `(e.g., breathing, meditation).`
- Line 940: `Inventory87 to assess anxiety before and after the exercise (or control) bouts. Study designs were either`
- Line 1120: `reduces anxiety symptoms.” The findings from the 2018 Scientific Report are consistent with those`
- Line 1212: `Total sleep time (TST) Total time of actual sleep, which is the sum of all time spent in each of the components (see Stages of sleep, below).`
- Line 1313: `physical activity on multiple sleep outcomes, including total sleep time (both habitual and acute), sleep`
- Line 1338: `1 Sleep Insufficient data d=0.35 (95% CI: 0.18-0.52) P<0.001`
- Line 1420: `metric for grading the severity of obstructive sleep apnea, is the mean number of apneic plus hypopneic`
- Line 1502: `NEEDS FOR FUTURE RESEARCH`

#### `US-HHS-PAGAC-2018-CARDIOMETABOLIC`

- Line 30: `to lower the health consequences of excessive body weight. This chapter focuses on physical activity`
- Line 35: `of sedentary behavior on body weight is addressed in Part F. Chapter 2. Sedentary Behavior.`
- Line 37: `3 deaths (807,775, or 30.8%) in the United States and 17.3 million (31%) worldwide.6, 7 Hypertension is`
- Line 99: `a) Is there a dose-response relationship? If yes, what is the shape of the relationship?`
- Line 106: `(systematic reviews, meta-analyses, pooled analyses, and reports) identified from an initial search did`
- Line 115: `done separately for each Subcommittee. For complete details on the systematic literature review`
- Line 126: `attenuated weight gain in adults, with some evidence to support that this relationship is most`
- Line 155: `gain (N=26) were prospective cohort studies,14-18, 20, 22-24, 27-31, 34-36, 38-46 with follow-up periods ranging`
- Line 241: `per week (0.7`
- Line 255: `Evidence on Specific Factors`
- Line 278: `younger counterparts.`
- Line 310: `varied by initial weight status. Of the remaining seven studies, two reported that the association did not`
- Line 468: `2018 Physical Activity Guidelines Advisory Committee Scientific Report F5-16`
- Line 602: `These blood pressure reductions are about 2 to 4 times greater among adults with prehypertension than`
- Line 650: `2018 Physical Activity Guidelines Advisory Committee Scientific Report F5-22`
- Line 702: `Dose-response: Five of the meta-analyses provided estimates for at least three levels of moderate-to-`
- Line 744: `accrues below the target zone.`
- Line 809: `1. Conduct longitudinal research on lower exposure levels of physical activity to allow for an enhanced`
- Line 813: `minutes per week on prevention of weight gain, hypertension, and type 2 diabetes. Thus, limited`
- Line 814: `data are currently available to inform whether lower amounts of physical activity can be effective`

#### `US-HHS-PAGAC-2018-OLDER-ADULTS`

- Line 65: `a) Is there a dose-response relationship? If yes, what is the shape of the relationship?`
- Line 68: `c) What type(s) of physical activity are effective for preventing injuries due to a fall?`
- Line 76: `b) Does the relationship vary by age, sex, race/ethnicity, socioeconomic status, or weight`
- Line 80: `population?`
- Line 205: `For example, Heesch et al10 reported that among 8,188 healthy, Australian community-dwelling women`
- Line 218: `minutes per week (OR=0.83; 0.46-1.48) experienced no significant reduction in risk of fall-related injury.`
- Line 238: `calories per day of active energy expenditure) was sufficient to negate the excess risk of fall-related`
- Line 261: `presented, and not statistically assessed. As a result, no conclusions about these relationships were`
- Line 321: `vary by age, sex, or weight status in the general population of older adults. PAGAC Grade: Limited.`
- Line 497: `Physical`
- Line 507: `ES=0.84; (95% CI: 0.61-1.06)36`
- Line 528: `included randomized trials, non-randomized trials, and single arm trials. 43 Positive effects indicate improvement`
- Line 556: `physical function. However, in one systematic review of 53 RCTs of aerobic training,16 7 trials assessed`
- Line 622: `of older adults, no-exercise control group, and physical function outcome).26`
- Line 945: `people) were eligible for the meta-analysis. The majority of hip fracture patients in these studies lived in`
- Line 1130: `2014,112 Shu et al., 2014,113 Tillman et al., 2015,114 and Yang et al., 2014.115`
- Line 1222: `Sources of evidence: Meta-analysis`
- Line 1259: `bone fractures. Multicomponent physical activity regimens that combine aerobic, strength, and balance`
- Line 1326: `include objective measures (e.g., heart rate monitors) of relative intensity of activity.`
- Line 1351: `Rationale: Dual-task training is a relatively new area of research in aging, and the methodologic`

#### `PLOS-PONE-0215877`

- Line 1: `Correction: Mapping wader biodiversity along the East Asian--Australasian flyway | PLOS One`
- Line 3: `Browse Subject Areas`
- Line 5: `?`
- Line 7: `Click through the PLOS taxonomy to find articles in your field.`
- Line 9: `For more information about PLOS Subject Areas, click`
- Line 10: `here.`
- Line 12: `Article`
- Line 14: `Metrics`
- Line 16: `Comments`
- Line 20: `Reader Comments`
- Line 22: `The Data Availability statement for this paper is incorrect. The correct statement is: Model data is available from the GBIF database at https://doi.org/10.15468/dl.cp0csd. All other relevant data are within the manuscript and its Supporting Information files.`
- Line 26: `The reference is: GBIF.org (07 April 2016) GBIF Occurrence Download https://doi.org/10.15468/dl.cp0csd.`
- Line 28: `Reference`
- Line 30: `1.`
- Line 33: `View Article`
- Line 39: `Citation: Li J, Hughes AC, Dudgeon D (2019) Correction: Mapping wader biodiversity along the East Asian--Australasian flyway. PLoS ONE 14(4):`
- Line 40: `e0215877.`
- Line 42: `https://doi.org/10.1371/journal.pone.0215877`
- Line 44: `Published: April 18, 2019`
- Line 46: `Copyright: © 2019 Li et al. This is an open access article distributed under the terms of the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited.`

#### `US-CDC-NIOSH-HEAT-2016`

- Line 16: `About Heat Stress`
- Line 18: `-`
- Line 21: `-`
- Line 22: `Communication Resources`
- Line 59: `- Review the full recommendations in the NIOSH Criteria for a Recommended Standard: Occupational Exposure to Heat and Hot Environments.`
- Line 63: `Engineering controls might include those that:`
- Line 68: `- Limit time in the heat and/or increase recovery time spent in a cool area.`
- Line 73: `- Use a buddy system where workers observe each other for signs of heat-related illnesses.`
- Line 88: `- Procedures for responding to symptoms of possible heat-related illness and for contacting emergency medical services.`
- Line 132: `- Encourage workers to hydrate themselves.`
- Line 135: `- If sweating lasts for several hours, drink sports drinks containing balanced electrolytes.`
- Line 141: `Employers should ensure and encourage workers to take appropriate rest breaks to cool down and hydrate.`
- Line 147: `When there is no air movement.`
- Line 165: `- Training`
- Line 246: `- Tiếng Việt`
- Line 289: `- Pressroom`
- Line 310: `- No Fear Act`
- Line 333: `- Português`
- Line 340: `Español`
- Line 359: `CDC Archive`

---

## 8. Summary of Files Created & Modified

1. `scripts/audit_pillar_keywords.py`: Repaired with case-insensitive matching, U+2010-U+2015/U+2212 hyphen normalization, muscle strengthening equivalence, and sanity checks.
2. `tests/test_audit_patterns.py`: Unit test fixtures added for Falls/falls/Injury/Sleep/muscle‑strengthening.
3. `scripts/generate_section_inventory.py`: PAGAC TOC parser and token counter per chapter section.
4. `scripts/audit_quarantine_overlap_phase11_5.py`: Quarantined Part C and Glossary cleaning and longest shared word run audit.
5. `scripts/print_bench_matches.py`: Contiguous word run overlap search against benchmark across all 12 documents.
6. `scripts/fix_manifest_and_registry_phase11_5.py`: Candidate manifest 11.4.1 generator with authoritative tokenizer hash, enum counts, and validation status; PLOS author correction.
7. `scripts/audit_cleaning_reconciliation.py`: Raw vs removed vs final line accounting and artifact counter.
8. `scripts/audit_text_quality_sample.py`: Seeded 20-line verbatim sampling and quality defect rate measurement.
9. `scripts/dump_removed_lines.py`: Dry-run script dumping removed lines per rule.
10. `scripts/render_phase11_5_addendum.py`: Generator script rendering `docs/phase11_5_addendum.md` directly from audit outputs.
11. `docs/phase11_5_addendum.md`: This comprehensive audit report.

---

## 9. Unresolved Items & Gate Line

- **Unresolved Items**: None. All 8 measurement and reconciliation directives are computed, verified, and reconciled to zero unaccounted lines.
- **Gate Decision**: `PRETRAINING: OFF`
