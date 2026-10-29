# Project NOVA Phase 11.3: Slice Audit & Evidence Hardening Report

> **Diagnostic-Only Audit Addendum**  
> Generated dynamically by `scripts/render_addendum.py` from machine-computed artifacts in `data/staging_phase11/audit_outputs/`.  
> **Invariants Strictly Preserved**: Zero changes to `train_staging.json`, `val_staging.json`, staging manifest, token counts (97,808 tokens), tokenizer, model weights, or training code. Pretraining remains OFF.

---

## 1. Executive Summary & Audit Overview

Phase 11.3 executes an independent, machine-checked audit of slice provenance, boundary quality, pillar keyword distributions, and legal rights verification across the 10 accepted staging documents and candidate registry entries.

### Registry Status Summary (Task 6 Enum)

| Status | Count | Description |
| :--- | :---: | :--- |
| `ACCEPTED` | 10 | Accepted staging documents admitted into pretraining split (97,808 tokens) |
| `REJECTED_LICENSE` | 1 | Disqualified by license gate (OpenStax Anatomy & Physiology 2e CC BY-NC-SA / AI prohibition) |
| `REJECTED_EXTRACTION` | 0 | Disqualified due to OCR/extraction corruption |
| `QUARANTINED_REVIEW` | 3 | Candidate sources held in quarantine pending deeper policy/safety/benchmark review (US-ARMY FM 7-22, PAGAC Concepts, PAGAC Glossary) |
| `FIXTURE` | 3 | Synthetic test fixtures validating rejection gates |
| **Total Tracked** | **17** | All registry entries |

---

## 2. Task 1: PAGAC Slice Audit (`scripts/audit_pagac_slices.py`)

The 5 accepted modular PAGAC document extracts were matched back page-by-page to the 779-page authentic PDF (`us_hhs_pagac_report_2018.pdf`) using normalized line overlap across all pages.

| Document Source ID | File Name | Matched PDF Pages | First Page Label | Last Page Label | Page Count | Running-Header Part/Chapter Character Shares |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `US-HHS-PAGAC-2018-EXEC` | `pagac_2018_part_a_executive_summary.txt` | pp. 23–35 | `A-5` | `C-2` | 13 | • **Part A. Executive Summary**: 23.39%<br>• **Part B. Introduction**: 58.54%<br>• **Part C. Background and Key Physical Activity Concepts**: 18.06% |
| `US-HHS-PAGAC-2018-HIIT` | `pagac_2018_part_f_ch1_bouts_hiit.txt` | pp. 107–120 | `E-13` | `F1-2` | 14 | • **Part E. Systematic Review Literature Search Methodology**: 77.22%<br>• **Part F . The Science Base**: 2.84%<br>• **New Issues in Defining Physical Activity**: 0.6%<br>• **Part F. Chapter 1. Physical Activity Behaviors: Steps, Bouts, and High Intensity Training**: 19.34% |
| `US-HHS-PAGAC-2018-BRAIN-SLEEP` | `pagac_2018_part_f_ch3_brain_sleep.txt` | pp. 207–222 | `F3-20` | `F3-35` | 16 | • **Part F. Chapter 3. Brain Health**: 100.0% |
| `US-HHS-PAGAC-2018-CARDIOMETABOLIC` | `pagac_2018_part_f_ch5_cardiometabolic.txt` | pp. 315–330 | `F4-67` | `F5-15` | 16 | • **Part F. Chapter 4. Cancer Prevention**: 1.78%<br>• **Part F. Chapter 5. Cardiometabolic Health and Prevention of Weight Gain**: 98.22% |
| `US-HHS-PAGAC-2018-OLDER-ADULTS` | `pagac_2018_part_f_ch9_older_adults.txt` | pp. 473–486 | `F9-35` | `F9-48` | 14 | • **Part F. Chapter 9. Older Adults**: 100.0% |

### Detailed PAGAC Slice Finding Notes

#### `US-HHS-PAGAC-2018-EXEC` (pagac_2018_part_a_executive_summary.txt)
- **Target Chapter Title**: 2018 PAGAC Scientific Report: Part A. Executive Summary
- **Matched PDF Range**: Page 23 (Label `A-5`) to Page 35 (Label `C-2`) [13 pages]
- **Character Volume**: 33,939 characters extracted
- **Running-Header Breakdown**:
  - `Part A. Executive Summary`: **23.39%** (7,939 chars, pages 23–25)
  - `Part B. Introduction`: **58.54%** (19,869 chars, pages 26–33)
  - `Part C. Background and Key Physical Activity Concepts`: **18.06%** (6,131 chars, pages 34–35)

#### `US-HHS-PAGAC-2018-HIIT` (pagac_2018_part_f_ch1_bouts_hiit.txt)
- **Target Chapter Title**: 2018 PAGAC Scientific Report: Part F. Chapter 1: Physical Activity and Habitual Physical Activity / High-Intensity Interval Training
- **Matched PDF Range**: Page 107 (Label `E-13`) to Page 120 (Label `F1-2`) [14 pages]
- **Character Volume**: 28,939 characters extracted
- **Running-Header Breakdown**:
  - `Part E. Systematic Review Literature Search Methodology`: **77.22%** (22,346 chars, pages 107–116)
  - `Part F . The Science Base`: **2.84%** (822 chars, page 117)
  - `New Issues in Defining Physical Activity`: **0.6%** (173 chars, page 118)
  - `Part F. Chapter 1. Physical Activity Behaviors: Steps, Bouts, and High Intensity Training`: **19.34%** (5,598 chars, pages 119–120)

#### `US-HHS-PAGAC-2018-BRAIN-SLEEP` (pagac_2018_part_f_ch3_brain_sleep.txt)
- **Target Chapter Title**: 2018 PAGAC Scientific Report: Part F. Chapter 3: Brain Health and Sleep
- **Matched PDF Range**: Page 207 (Label `F3-20`) to Page 222 (Label `F3-35`) [16 pages]
- **Character Volume**: 44,682 characters extracted
- **Running-Header Breakdown**:
  - `Part F. Chapter 3. Brain Health`: **100.0%** (44,682 chars, pages 207–222)

#### `US-HHS-PAGAC-2018-CARDIOMETABOLIC` (pagac_2018_part_f_ch5_cardiometabolic.txt)
- **Target Chapter Title**: 2018 PAGAC Scientific Report: Part F. Chapter 5: Cardiometabolic Health and Weight Management
- **Matched PDF Range**: Page 315 (Label `F4-67`) to Page 330 (Label `F5-15`) [16 pages]
- **Character Volume**: 42,152 characters extracted
- **Running-Header Breakdown**:
  - `Part F. Chapter 4. Cancer Prevention`: **1.78%** (750 chars, page 315)
  - `Part F. Chapter 5. Cardiometabolic Health and Prevention of Weight Gain`: **98.22%** (41,402 chars, pages 316–330)

#### `US-HHS-PAGAC-2018-OLDER-ADULTS` (pagac_2018_part_f_ch9_older_adults.txt)
- **Target Chapter Title**: 2018 PAGAC Scientific Report: Part F. Chapter 9: Physical Activity and Older Adults: Fall Prevention and Sarcopenia
- **Matched PDF Range**: Page 473 (Label `F9-35`) to Page 486 (Label `F9-48`) [14 pages]
- **Character Volume**: 40,928 characters extracted
- **Running-Header Breakdown**:
  - `Part F. Chapter 9. Older Adults`: **100.0%** (40,928 chars, pages 473–486)


---

## 3. Task 2: Boundary & Extraction-Quality Evidence (`scripts/audit_boundary_quality.py`)

Audits the first 5 lines, last 15 lines, and detects 5 structural artifact classes across all 10 accepted documents:
1. `reference_list_lines`: Numbered citations containing `doi` or `year;volume`
2. `table_of_contents_lines`: Lines with dot leaders (`...`)
3. `running_header_lines`: Running Part/Chapter lines and report header strings
4. `source_adapted_lines`: Explicit attribution/adapted lines (e.g. `Source: Adapted from...`)
5. `page_number_artifacts`: Standalone page numbers and report page footer markers

### Extraction Artifact Density Summary Table

| Document ID | Total Lines | Total Chars | References Chars (%) | TOC Dot Leaders Chars (%) | Running Headers Chars (%) | Source: Adapted Chars (%) | Page Artifacts Chars (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `US-CDC-PA-ADULTS-2022` | 381 | 23,455 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 90 (0.38%) |
| `US-CDC-PA-MEASURING-2022` | 407 | 25,852 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 81 (0.31%) |
| `US-CDC-PA-OLDER-2022` | 404 | 27,654 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 81 (0.29%) |
| `US-CDC-NIOSH-HEAT-2016` | 369 | 22,785 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 34 (0.15%) |
| `PLOS-PONE-0215877` | 1131 | 71,413 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 28 (0.04%) |
| `US-HHS-PAGAC-2018-EXEC` | 411 | 33,553 | 0 (0.0%) | 4300 (12.82%) | 1418 (4.23%) | 0 (0.0%) | 1005 (3.0%) |
| `US-HHS-PAGAC-2018-HIIT` | 569 | 28,397 | 0 (0.0%) | 1207 (4.25%) | 1736 (6.11%) | 0 (0.0%) | 1103 (3.88%) |
| `US-HHS-PAGAC-2018-BRAIN-SLEEP` | 547 | 44,166 | 0 (0.0%) | 0 (0.0%) | 1744 (3.95%) | 0 (0.0%) | 1273 (2.88%) |
| `US-HHS-PAGAC-2018-CARDIOMETABOLIC` | 524 | 41,659 | 0 (0.0%) | 1284 (3.08%) | 2403 (5.77%) | 122 (0.29%) | 1244 (2.99%) |
| `US-HHS-PAGAC-2018-OLDER-ADULTS` | 534 | 40,421 | 152 (0.38%) | 0 (0.0%) | 1540 (3.81%) | 0 (0.0%) | 1096 (2.71%) |

### Boundary Line Evidence: First 5 Lines & Last 15 Lines

#### `US-CDC-PA-ADULTS-2022` (us_cdc_pa_adults_2022.md)
**First 5 Lines:**
```text
L001: Title: Adult Activity: An Overview | Physical Activity Basics | CDC
L002: 
L003: Description: See physical activity recommendations for adults and examples of how to meet the weekly goals.
L004: 
L005: Source: https://www.cdc.gov/physical-activity-basics/guidelines/adults.html
```
**Last 15 Lines:**
```text
L367: [Polski](https://www.cdc.gov/other/language-assistance.html#Polish)
L368: [Português](https://www.cdc.gov/other/language-assistance.html#Portuguese)
L369: [Italiano](https://www.cdc.gov/other/language-assistance.html#Italian)
L370: [Deutsch](https://www.cdc.gov/other/language-assistance.html#German)
L371: [日本語](https://www.cdc.gov/other/language-assistance.html#Japanese)
L372: [فارسی](https://www.cdc.gov/other/language-assistance.html#Farsi)
L373: [English](https://www.cdc.gov/other/language-assistance.html#English)
L374: [Archive](https://www.cdc.gov/physical-activity-basics/guidelines/adults.html#mobile-footer-archive)
L375: - [CDC Archive](https://archive.cdc.gov/)
L376: - [Public Health Publications](https://stacks.cdc.gov/)
L377: [CDC Archive](https://archive.cdc.gov/)
L378: [Public Health Publications](https://stacks.cdc.gov/)
L379: [HHS.gov](https://hhs.gov)
L380: [USA.gov](https://usa.gov)
L381: 
```

#### `US-CDC-PA-MEASURING-2022` (us_cdc_pa_measuring_2022.md)
**First 5 Lines:**
```text
L001: Title: How to Measure Physical Activity Intensity | Physical Activity Basics | CDC
L002: 
L003: Description: Learn about ways to measure aerobic physical activity intensity.
L004: 
L005: Source: https://www.cdc.gov/physical-activity-basics/measuring/index.html
```
**Last 15 Lines:**
```text
L393: [Polski](https://www.cdc.gov/other/language-assistance.html#Polish)
L394: [Português](https://www.cdc.gov/other/language-assistance.html#Portuguese)
L395: [Italiano](https://www.cdc.gov/other/language-assistance.html#Italian)
L396: [Deutsch](https://www.cdc.gov/other/language-assistance.html#German)
L397: [日本語](https://www.cdc.gov/other/language-assistance.html#Japanese)
L398: [فارسی](https://www.cdc.gov/other/language-assistance.html#Farsi)
L399: [English](https://www.cdc.gov/other/language-assistance.html#English)
L400: [Archive](https://www.cdc.gov/physical-activity-basics/measuring/index.html#mobile-footer-archive)
L401: - [CDC Archive](https://archive.cdc.gov/)
L402: - [Public Health Publications](https://stacks.cdc.gov/)
L403: [CDC Archive](https://archive.cdc.gov/)
L404: [Public Health Publications](https://stacks.cdc.gov/)
L405: [HHS.gov](https://hhs.gov)
L406: [USA.gov](https://usa.gov)
L407: 
```

#### `US-CDC-PA-OLDER-2022` (us_cdc_pa_older_2022.md)
**First 5 Lines:**
```text
L001: Title: Older Adults: Adding Activity Recommendations | Physical Activity Basics | CDC
L002: 
L003: Description: Learn ways older adults can add physical activity to their lives.
L004: 
L005: Source: https://www.cdc.gov/physical-activity-basics/adding-older-adults/index.html
```
**Last 15 Lines:**
```text
L390: [Polski](https://www.cdc.gov/other/language-assistance.html#Polish)
L391: [Português](https://www.cdc.gov/other/language-assistance.html#Portuguese)
L392: [Italiano](https://www.cdc.gov/other/language-assistance.html#Italian)
L393: [Deutsch](https://www.cdc.gov/other/language-assistance.html#German)
L394: [日本語](https://www.cdc.gov/other/language-assistance.html#Japanese)
L395: [فارسی](https://www.cdc.gov/other/language-assistance.html#Farsi)
L396: [English](https://www.cdc.gov/other/language-assistance.html#English)
L397: [Archive](https://www.cdc.gov/physical-activity-basics/adding-older-adults/index.html#mobile-footer-archive)
L398: - [CDC Archive](https://archive.cdc.gov/)
L399: - [Public Health Publications](https://stacks.cdc.gov/)
L400: [CDC Archive](https://archive.cdc.gov/)
L401: [Public Health Publications](https://stacks.cdc.gov/)
L402: [HHS.gov](https://hhs.gov)
L403: [USA.gov](https://usa.gov)
L404: 
```

#### `US-CDC-NIOSH-HEAT-2016` (us_cdc_niosh_heat_2016.md)
**First 5 Lines:**
```text
L001: Title: Workplace Recommendations | Heat Stress | CDC
L002: 
L003: Description: Provides basic recommendations that apply to workers exposed to heat in different workplaces.
L004: 
L005: Source: https://www.cdc.gov/niosh/topics/heatstress/recommendations.html
```
**Last 15 Lines:**
```text
L355: [Polski](https://www.cdc.gov/other/language-assistance.html#Polish)
L356: [Português](https://www.cdc.gov/other/language-assistance.html#Portuguese)
L357: [Italiano](https://www.cdc.gov/other/language-assistance.html#Italian)
L358: [Deutsch](https://www.cdc.gov/other/language-assistance.html#German)
L359: [日本語](https://www.cdc.gov/other/language-assistance.html#Japanese)
L360: [فارسی](https://www.cdc.gov/other/language-assistance.html#Farsi)
L361: [English](https://www.cdc.gov/other/language-assistance.html#English)
L362: [Archive](https://www.cdc.gov/niosh/topics/heatstress/recommendations.html#mobile-footer-archive)
L363: - [CDC Archive](https://archive.cdc.gov/)
L364: - [Public Health Publications](https://stacks.cdc.gov/)
L365: [CDC Archive](https://archive.cdc.gov/)
L366: [Public Health Publications](https://stacks.cdc.gov/)
L367: [HHS.gov](https://hhs.gov)
L368: [USA.gov](https://usa.gov)
L369: 
```

#### `PLOS-PONE-0215877` (plos_pone_0215877.html)
**First 5 Lines:**
```text
L001: <!DOCTYPE html>
L002: <html xmlns="http://www.w3.org/1999/xhtml"
L003:       xmlns:dc="http://purl.org/dc/terms/"
L004:       xmlns:doi="http://dx.doi.org/"
L005:       lang="en" xml:lang="en"
```
**Last 15 Lines:**
```text
L1117:     preferredFont: "STIX",
L1118:     webFont: "STIX-Web",
L1119:     linebreaks: { automatic: false }
L1120:   },
L1121:   jax: ["input/MathML", "output/HTML-CSS"]
L1122: });
L1123: </script>
L1124: 
L1125: <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=MML_HTMLorMML"></script>
L1126: 
L1127: <div class="reveal-modal-bg"></div>
L1128: </body>
L1129: </html>
L1130: 
L1131: 
```

#### `US-HHS-PAGAC-2018-EXEC` (pagac_2018_part_a_executive_summary.txt)
**First 5 Lines:**
```text
L001: Part A. Executive Summary 
L002: 2018 Physical Activity Guidelines Advisory Committee Scientific Report A-5
L003: small increases in moderate-intensity physical activity provide health benefits. There is no 
L004: threshold that must be exceeded before benefits begin to occur. 
L005: • For individuals whose physical activity is below the current public health target range, greater
```
**Last 15 Lines:**
```text
L397: lifestyle behaviors on the risk of disease, an observation that is now well accepted. Also widely 
L398: recognized is the fact that individual behaviors, including physical activity behaviors, are determined not 
L399: solely by individual choice but by social and cultural factors as well as environmental impediments or 
L400: opportunities. 
L401: Thus, while exercise science and epidemiologic science remain central to the field of physical activity 
L402: and public health, the field now includes an array of other scientific disciplines. Behavioral science, 
L403: clinical science, recreation science, transportation science, city planning, political science, and other 
L404: disciplines are now recognized to be essential for the proper study and practice of physical activity and 
L405: public health. 
L406: The widening range of scientific fields currently contributing to this topic reflects the recognition that 
L407: physical activity is embedded and intricately connected to every aspect of daily life. No longer viewed 
L408: only as distinct and prolonged bouts of “vigorous physical exercise,”6 physical activity is recognized as 
L409: encompassing the accumulation of movement occurring throughout the day, regardless of location, 
L410: type, or purpose. This broader view of physical activity complicates the study, understanding, and 
L411: discussion of this key health behavior. The purpose of this chapter is to provide a brief discussion of 
```

#### `US-HHS-PAGAC-2018-HIIT` (pagac_2018_part_f_ch1_bouts_hiit.txt)
**First 5 Lines:**
```text
L001: Part E. Systematic Review Literature Search Methodology 
L002: 2018 Physical Activity Guidelines Advisory Committee Scientific Report E-13
L003: pooled analyses, or reports to abstracting original articles and when new research questions required 
L004: changes in the abstraction form.  
L005: Abstract Data 
```
**Last 15 Lines:**
```text
L555: health recommendations?
L556: • What, if any, is the value of light-intensity physical activity?
L557: • At any given volume of moderate-to-vigorous physical activity, does the composition of baseline
L558: physical activity influence health outcomes?
L559: The Committee considered it important to address these questions and anticipate the ones that might 
L560: arise following the publication of the 2018 Scientific Report by investigating the current data and further 
L561: research needs of three particularly relevant issues: the role of daily step counts in the assessment of 
L562: daily accumulated physical activity across all intensity levels, including light-intensity activity; the impact 
L563: on health benefits of moderate-to-vigorous physical activity in bouts lasting less than 10 minutes; and 
L564: the effect of and contribution of HIIT to the prescribed amount of weekly moderate-to-vigorous physical 
L565: activity, and whether HIIT is associated with cardiometabolic health benefits. 
L566: All the dose-response data used to develop the physical activity targets for the 2008 Guidelines2 were 
L567: developed using epidemiologic data from longitudinal cohort studies with the condition as the outcome 
L568: and moderate-to-vigorous physical activity as the exposure. One well-accepted limitation of reported 
L569: data is the inability to incorporate light-intensity physical activity. With the advent of devices to 
```

#### `US-HHS-PAGAC-2018-BRAIN-SLEEP` (pagac_2018_part_f_ch3_brain_sleep.txt)
**First 5 Lines:**
```text
L001: Part F. Chapter 3. Brain Health 
L002:  
L003: 2018 Physical Activity Guidelines Advisory Committee Scientific Report F3-20 
L004:  
L005: Physical activity as part of other activities that involve mental and physical components, such as qigong 
```
**Last 15 Lines:**
```text
L533: For additional details on this body of evidence, visit: https://health.gov/paguidelines/second-
L534: edition/report/supplementary-material.aspx for the Evidence Portfolio. 
L535: Comparing 2018 Findings with the 2008 Scientific Report 
L536: The 2008 Scientific Report1 concluded that “population-based, prospective cohort studies provide 
L537: substantial evidence that regular physical activity protects against the onset of depression symptoms 
L538: and major depressive disorder.” In addition, it concluded that RCTs showed that physical activity 
L539: “reduces depression symptoms in people diagnosed as depressed, healthy adults, and medical patients 
L540: without psychiatric disorders.” In the context of anxiety, the 2008 Scientific Report1 concluded that “a 
L541: small number of nationally representative and population-based cross-sectional and prospective cohort 
L542: studies supports that regular physical activity protects against the onset of anxiety disorders and anxiety 
L543: symptoms.” The 2008 Scientific Report1 also concluded that “participation in physical activity programs 
L544: reduces anxiety symptoms.” The findings from the 2018 Scientific Report are consistent with those 
L545: reported in 2008 but significantly extend them to include more information from prospective 
L546: observational studies in the context of depression and from RCTs that now definitely demonstrate that 
L547: physical activity is an effective treatment for reducing anxiety and depressive symptoms. In addition, the 
```

#### `US-HHS-PAGAC-2018-CARDIOMETABOLIC` (pagac_2018_part_f_ch5_cardiometabolic.txt)
**First 5 Lines:**
```text
L001: Part F. Chapter 4. Cancer Prevention 
L002:  
L003:  
L004: 2018 Physical Activity Guidelines Advisory Committee Scientific Report    F4-67 
L005: 90. Shen D, Mao W, Liu T, et al. Sedentary behavior and incident cancer: a meta-analysis of prospective 
```
**Last 15 Lines:**
```text
L510: physical activity (LMVPA) among adults with normal blood pressure. The protective effect increased by 
L511: about 6 percent for each further increase of 10 MET-hours per week. For adults with 20 MET hours per 
L512: week of leisure-time LMVPA, the risk of hypertension was reduced by 12 percent (RR=0.88; 95% CI: 0.83-
L513: 0.92); and for those for 60 MET-hours per week of leisure-time LMVPA, the risk of hypertension was 
L514: reduced by 33 percent (RR=0.67; 95% CI: 0.58-0.78). The relationship between leisure-time physical 
L515: activity and incident hypertension was linear, with no cutoff of benefit, and slightly weaker with 
L516: (RR=0.94; 95% CI: 0.92-0.9 6) than without (RR=0.91; 95% CI: 0.89-0.93) BMI adjustment. These same 
L517: dose-response trends were seen for total physical activity such that for each 50 MET-hours per week 
L518: increase in total physical activity, the risk of hypertension was reduced by 7 percent (RR=0.93; 95% CI: 
L519: 0.88-0.98); and for 64.5 MET-hours per week of total physical activity, the risk of hypertension was 
L520: reduced by 10 percent. The relationship between total physical activity and incident hypertension was 
L521: linear, with no cutoff of benefit, and slightly stronger with than without BMI adjustment. The authors 
L522: acknowledged their meta-analysis was limited by the considerable variety of physical activity self-report 
L523: questionnaires used in the primary level studies.  
L524:   
```

#### `US-HHS-PAGAC-2018-OLDER-ADULTS` (pagac_2018_part_f_ch9_older_adults.txt)
**First 5 Lines:**
```text
L001: Part F. Chapter 9. Older Adults  
L002:  
L003: 2018 Physical Activity Guidelines Advisory Committee Scientific Report F9-35 
L004:  
L005: and 6-Minute Walk Test (SMD=0.78; 95% CI: 0.35-1.21). Interventions with tai chi alone appear more 
```
**Last 15 Lines:**
```text
L520: of life in community-dwelling older adults with impaired mobility, physical disability and/or multi-
L521: morbidity: a meta-analysis. Ageing Res Rev. 2012;11(1):136-149. doi:10.1016/j.arr.2011.11.002. 
L522: 84. Giné-Garriga M, Roqué-Fíguls M, Coll-Planas L, Sitjà-Rabert M, Salvà A. Physical exercise 
L523: interventions for improving performance-based measures of physical function in community-dwelling, 
L524: frail older adults: a systematic review and meta-analysis. Arch Phys Med Rehabil. 2014;95(4):753-769.e3. 
L525: doi:10.1016/j.apmr.2013.11.007. 
L526: 85. Nash KC. The effects of exercise on strength and physical performance in frail older people: a 
L527: systematic review. Rev Clin Gerontol. 2012;22(4):274-285. doi:10.1017/S0959259812000111. 
L528: 86. Theou O, Stathokostas L, Roland KP, et al. The effectiveness of exercise interventions for the 
L529: management of frailty: a systematic review. J Aging Res. April 2011:569194. doi:10.4061/2011/569194. 
L530: 87. Valenzuela T. Efficacy of progressive resistance training interventions in older adults in nursing 
L531: homes: a systematic review. J Am Med Dir Assoc. 2012;13(5):418-428. doi:10.1016/j.jamda.2011.11.001. 
L532: 88. Vermeulen J, Neyens JC, van Rossum E, Spreeuwenberg MD, de Witte LP. Predicting ADL disability in 
L533: community-dwelling elderly people using physical frailty indicators: a systematic review. BMC Geriatr. 
L534: 2011;11:33. doi:10.1186/1471-2318-11-33. 
```


---

## 4. Task 3: Pillar Keyword Evidence — No Narrative (`scripts/audit_pillar_keywords.py`)

Quantitative keyword density per 1,000 words computed using exact regex definitions:
- `strength`: `resistance training|muscle-strengthening|strength training|repetition|hypertrophy`
- `interval`: `high-intensity interval|HIIT|interval`
- `sleep`: `sleep`
- `nutrition`: `diet|dietary|energy intake|calorie|nutrition|hydration|fluid`
- `injury`: `injur|fall|adverse event`
- `biomech`: `biomechanic|joint|torque|moment arm|kinematic`

### Quantitative Pillar Density Matrix (Occurrences per 1,000 Words)

| Document ID | Assigned Pillar | Density of Assigned Pillar's Keyword Set | Density of Every Other Set |
| :--- | :--- | :---: | :--- |
| `US-CDC-PA-ADULTS-2022` | `exercise_physiology` | **0.00** | strength=4.12; interval=0.00; sleep=0.00; nutrition=5.77; injury=0.00 |
| `US-CDC-PA-MEASURING-2022` | `exercise_physiology` | **0.00** | strength=0.00; interval=0.00; sleep=0.00; nutrition=7.55; injury=0.00 |
| `US-CDC-PA-OLDER-2022` | `injury_prevention` | **0.68** | strength=0.00; interval=0.00; sleep=0.00; nutrition=5.45; biomech=0.00 |
| `US-CDC-NIOSH-HEAT-2016` | `nutrition_hydration` | **5.24** | strength=0.00; interval=0.00; sleep=0.00; injury=0.00; biomech=0.00 |
| `PLOS-PONE-0215877` | `strength_training` | **0.00** | interval=0.31; sleep=0.00; nutrition=0.00; injury=0.00; biomech=0.00 |
| `US-HHS-PAGAC-2018-EXEC` | `fitness_education` | **N/A** | strength=0.00; interval=0.00; sleep=0.23; nutrition=1.16; injury=0.69; biomech=0.23 |
| `US-HHS-PAGAC-2018-HIIT` | `strength_training` | **0.00** | interval=2.56; sleep=0.00; nutrition=2.05; injury=0.26; biomech=0.00 |
| `US-HHS-PAGAC-2018-BRAIN-SLEEP` | `recovery_sleep` | **0.00** | strength=0.47; interval=0.95; nutrition=0.00; injury=0.00; biomech=0.00 |
| `US-HHS-PAGAC-2018-CARDIOMETABOLIC` | `nutrition_hydration` | **0.16** | strength=0.00; interval=0.16; sleep=0.00; injury=0.00; biomech=0.16 |
| `US-HHS-PAGAC-2018-OLDER-ADULTS` | `injury_prevention` | **8.51** | strength=2.72; interval=0.00; sleep=0.00; nutrition=0.00; biomech=0.00 |

### Verbatim Sample Lines (Up to 3 Per Regex Set with Line Numbers)

#### `US-CDC-PA-ADULTS-2022` (Total Words: 1,213)
- **Set `strength`** (Density: 4.12 / 1k words):
  - Line 137: `- Adults also need 2 days of muscle-strengthening activity each week.`
  - Line 141: `According to the current [Physical Activity Guidelines for Americans](https://odphp.health.gov/our-work/nutrition-physical-activity/physical`
  - Line 151: `Muscle-strengthening activities on 2 or more days a week that work all major muscle groups (legs, hips, back, abdomen, chest, shoulders, and`
- **Set `nutrition`** (Density: 5.77 / 1k words):
  - Line 64: `[Nutrition](https://www.cdc.gov/nutrition/php/about/index.html)`
  - Line 117: `[Nutrition](https://www.cdc.gov/nutrition/php/about/index.html)`
  - Line 122: `[Nutrition](https://www.cdc.gov/nutrition/php/about/index.html)`

#### `US-CDC-PA-MEASURING-2022` (Total Words: 1,325)
- **Set `nutrition`** (Density: 7.55 / 1k words):
  - Line 64: `[Nutrition](https://www.cdc.gov/nutrition/php/about/index.html)`
  - Line 117: `[Nutrition](https://www.cdc.gov/nutrition/php/about/index.html)`
  - Line 122: `[Nutrition](https://www.cdc.gov/nutrition/php/about/index.html)`

#### `US-CDC-PA-OLDER-2022` (Total Words: 1,469)
- **Set `nutrition`** (Density: 5.45 / 1k words):
  - Line 64: `[Nutrition](https://www.cdc.gov/nutrition/php/about/index.html)`
  - Line 117: `[Nutrition](https://www.cdc.gov/nutrition/php/about/index.html)`
  - Line 122: `[Nutrition](https://www.cdc.gov/nutrition/php/about/index.html)`
- **Set `injury`** (Density: 0.68 / 1k words):
  - Line 149: `- Try to do a variety of activities. This can make physical activity more enjoyable and reduce your risk of injury.`

#### `US-CDC-NIOSH-HEAT-2016` (Total Words: 1,716)
- **Set `nutrition`** (Density: 5.24 / 1k words):
  - Line 97: `- Monitoring and encouraging adequate fluid intake and rest breaks.`
  - Line 132: `## Hydration`
  - Line 133: `Employers should provide the means for appropriate hydration of workers.`

#### `PLOS-PONE-0215877` (Total Words: 3,181)
- **Set `interval`** (Density: 0.31 / 1k words):
  - Line 208: `window.NREUM||(NREUM={}),__nr_require=function(t,e,n){function r(n){if(!e[n]){var o=e[n]={exports:{}};t[n][0].call(o.exports,function(e){var`

#### `US-HHS-PAGAC-2018-EXEC` (Total Words: 4,320)
- **Set `sleep`** (Density: 0.23 / 1k words):
  - Line 65: `anxiety, enhanced quality of sleep, and improved physical function is difficult. In addition, monetizing`
- **Set `nutrition`** (Density: 1.16 / 1k words):
  - Line 126: `Committee,2 similar to the expert committees formed for the Dietary Guidelines for Americans3 process.`
  - Line 261: `of Health (NIH), and the President’s Council on Fitness, Sports & Nutrition (PCFSN). Each Subcommittee`
  - Line 342: `3. U.S. Department of Health and Human Services; U.S. Department of Agriculture. 2015–2020 Dietary`
- **Set `injury`** (Density: 0.69 / 1k words):
  - Line 50: `excessive weight gain, falls with injuries among the elderly, and breast, colon, endometrial, esophageal,`
  - Line 155: `activity and risk of musculoskeletal injury; physical activity and cognition; physical activity within specific`
- **Set `biomech`** (Density: 0.23 / 1k words):
  - Line 154: `prevention; bone, joint, and muscle health and performance; obesity and weight management; physical`

#### `US-HHS-PAGAC-2018-HIIT` (Total Words: 3,910)
- **Set `interval`** (Density: 2.56 / 1k words):
  - Line 125: `◦ High Intensity Interval Training (HIIT)?`
  - Line 211: `• High Intensity Interval Training (HIIT)?`
  - Line 521: `Question 3. What is the relationship between high intensity interval training (HIIT) and reduction in`
- **Set `nutrition`** (Density: 2.05 / 1k words):
  - Line 56: `Research Bias Assessment using Adapted Nutrition Evidence Library Bias Assessment Tool Instrument).`
  - Line 259: `Original Research Bias Assessment using Adapted Nutrition Evidence Library`
  - Line 445: `1. U.S Department of Agriculture (USDA). Nutrition evidence library—about. USDA website.`
- **Set `injury`** (Density: 0.26 / 1k words):
  - Line 186: `◦ Addresses Adverse Events?`

#### `US-HHS-PAGAC-2018-BRAIN-SLEEP` (Total Words: 6,323)
- **Set `strength`** (Density: 0.47 / 1k words):
  - Line 51: `strength training, and alternative or complementary types in one.55`
  - Line 90: `examined a diversity of physical activity modalities, including aerobic training, strength training,`
  - Line 91: `combined aerobic and resistance training, flexibility, balance, yoga, and tai chi.72`
- **Set `interval`** (Density: 0.95 / 1k words):
  - Line 297: `Findings regarding the effects of interval versus continuous exercise were mixed across nine`
  - Line 300: `more unpleasant affective response during interval versus continuous exercise; four studies`
  - Line 301: `documented no difference in affective responses during interval and continuous exercise. Only one`

#### `US-HHS-PAGAC-2018-CARDIOMETABOLIC` (Total Words: 6,142)
- **Set `interval`** (Density: 0.16 / 1k words):
  - Line 220: `(incidence rate ratio (IRR)=0.81; 95% confidence interval (CI): 0.71-0.93) and overweight women`
- **Set `nutrition`** (Density: 0.16 / 1k words):
  - Line 210: `socioeconomic status, initial weight status, or dietary intake and eating behaviors, on the relationship`
- **Set `biomech`** (Density: 0.16 / 1k words):
  - Line 68: `the most common, costly, and preventable CVD risk factor. According to the Seventh Report of the Joint`

#### `US-HHS-PAGAC-2018-OLDER-ADULTS` (Total Words: 5,524)
- **Set `strength`** (Density: 2.72 / 1k words):
  - Line 31: `A pooled analysis of five RCTs of strength training (N=240 participants) reported that strength training`
  - Line 68: `activity (e.g., progressive muscle-strengthening training, tai chi, tango dancing, multicomponent`
  - Line 101: `healthier counterparts. Aerobic, muscle-strengthening, and multicomponent physical activity appear to`
- **Set `injury`** (Density: 8.51 / 1k words):
  - Line 57: `greater need of fall prevention programs compared older adults without this impairment. The only`
  - Line 86: `Strong evidence demonstrates that participation in multicomponent group or home-based fall`
  - Line 87: `prevention physical activity and exercise programs can reduce the risk of injury from falls, including`


---

## 5. Task 4: Verifier Hardening & Verification Results (`scripts/verify_evidence_quotes.py`)

The quote verifier has been hardened with strict path validation: **any quote citing a path under `docs/` or a generated artifact is automatically REJECTED**.

### Hardened Authentic Quotes Audit (All Passing)

| Target ID | Status | Authentic File Path | Cited Line / Page | Actual Text Found in File |
| :--- | :---: | :--- | :---: | :--- |
| `CDC-POLICY-PUBLIC-DOMAIN` | **PASS** | `data\staging_phase11\quarantine_evidence\cdc_agency_materials_snapshot.html` | Line 27 | <meta name="description" content="Most of the information on the CDC and ATSDR websites is not subject to copyright, is  |
| `CDC-POLICY-EXCEPTIONS` | **PASS** | `data\staging_phase11\quarantine_evidence\cdc_agency_materials_snapshot.html` | Line 191 | <p>There are, however, a few exceptions. A federal government website may have a mix of public domain and copyright-prot |
| `CDC-POLICY-ATTRIBUTION-REQUEST` | **PASS** | `data\staging_phase11\quarantine_evidence\cdc_agency_materials_snapshot.html` | Line 193 | <p>1) Attribution to the agency that developed the material must be provided in your use of the materials.&nbsp; Such at |
| `ODPHP-POLICY-PUBLIC-DOMAIN` | **PASS** | `data\staging_phase11\quarantine_evidence\health_gov_copyright_policy_snapshot.html` | Line 384 | <div class="clearfix text-formatted field field--name-field-basic-text field--type-text-long field--label-hidden field__ |
| `PAGAC-PDF-PAGE2-DISCLAIMER` | **PASS** | `data\staging_phase11\sources_raw\us_hhs_pagac_report_2018.pdf` | Line 2 | The findings of this report are those of the 2018 Physical Activity Guidelines Advisory Committee. They do not necessari |
| `PLOS-PONE-0215877-REAL` | **PASS** | `data\staging_phase11\sources_raw\plos_pone_0215877.html` | Line 885 | This is an open access article distributed under the terms of the Creative Commons Attribution License |
| `OPENSTAX-REAL-LICENSE` | **PASS** | `data\staging_phase11\quarantine_evidence\openstax_ap2e_biomechanics.html` | Line 205 | Textbook content produced by OpenStax is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike License. |
| `OPENSTAX-REAL-AI` | **PASS** | `data\staging_phase11\quarantine_evidence\openstax_ap2e_biomechanics.html` | Line 155 | This book may not be used in the training of large language models or otherwise be ingested into large language models o |
| `OPENSTAX-ADDITIONAL-1` | **PASS** | `data\staging_phase11\quarantine_evidence\openstax_ap2e_biomechanics.html` | Line 154 | This book uses the Creative Commons Attribution-NonCommercial-ShareAlike License, which means that you can reuse and mod |
| `OPENSTAX-ADDITIONAL-2` | **PASS** | `data\staging_phase11\quarantine_evidence\openstax_ap2e_biomechanics.html` | Line 163 | OpenStax-copyrighted images, activities, assessments, and similar components of this book are subject to the same licens |
| `OPENSTAX-ADDITIONAL-3` | **PASS** | `data\staging_phase11\quarantine_evidence\openstax_ap2e_biomechanics.html` | Line 162 | Permission requests: Anyone who intends to incorporate this content (including text, images, and other components) into  |
| `PAGAC-CARDIOMETABOLIC-ADAPTED-LINE-276` | **PASS** | `data\staging_phase11\sources_raw\pagac_2018_part_f_ch5_cardiometabolic.txt` | Line 276 | Source: Adapted from data found in Brown et al., 2016. 20 |
| `PAGAC-CARDIOMETABOLIC-ADAPTED-LINE-298` | **PASS** | `data\staging_phase11\sources_raw\pagac_2018_part_f_ch5_cardiometabolic.txt` | Line 298 | Source: Adapted from data found in Rosenberg et al., 2013. 39 |

### Legacy Quotes Re-Run (Documenting Failures & Path Rejections)

| Legacy Target ID | Status | File Cited | Cited Line | Reason / Actual Text Found |
| :--- | :---: | :--- | :---: | :--- |
| `US-CDC-PA-ADULTS-2022` | **FAIL** | `data\staging_phase11\sources_raw\us_cdc_pa_adults_2022.md` | 14 | NO_EVIDENCE_FOUND (line 14 actually contains: '[Physical Activity Basics](https://www.cdc.gov/physical-activity-basics/about/index.html)') |
| `US-CDC-PA-MEASURING-2022` | **FAIL** | `data\staging_phase11\sources_raw\us_cdc_pa_measuring_2022.md` | 14 | NO_EVIDENCE_FOUND (line 14 actually contains: '[Physical Activity Basics](https://www.cdc.gov/physical-activity-basics/about/index.html)') |
| `US-CDC-PA-OLDER-2022` | **FAIL** | `data\staging_phase11\sources_raw\us_cdc_pa_older_2022.md` | 14 | NO_EVIDENCE_FOUND (line 14 actually contains: '[Physical Activity Basics](https://www.cdc.gov/physical-activity-basics/about/index.html)') |
| `US-CDC-NIOSH-HEAT-2016` | **FAIL** | `data\staging_phase11\sources_raw\us_cdc_niosh_heat_2016.md` | 15 | NO_EVIDENCE_FOUND (line 15 actually contains: '[Heat Stress](https://www.cdc.gov/niosh/heat-stress/about/index.html)') |
| `PLOS-PONE-0215877` | **PASS** | `data\staging_phase11\sources_raw\plos_pone_0215877.html` | 42 | https://doi.org/10.1371/journal.pone.0215877 Published: April 18, 2019 Copyright: © 2019 Li et al. This is an open access article distribute |
| `US-HHS-PAGAC-2018-EXEC` | **FAIL** | `docs\phase11_parent_source_integrity_report.md` | 55 | REJECTED_DISALLOWED_PATH: Evidence path under docs/ or generated file is prohibited; quotations must cite authentic source files. |
| `US-HHS-PAGAC-2018-HIIT` | **FAIL** | `docs\phase11_parent_source_integrity_report.md` | 57 | REJECTED_DISALLOWED_PATH: Evidence path under docs/ or generated file is prohibited; quotations must cite authentic source files. |
| `US-HHS-PAGAC-2018-BRAIN-SLEEP` | **FAIL** | `docs\phase11_parent_source_integrity_report.md` | 58 | REJECTED_DISALLOWED_PATH: Evidence path under docs/ or generated file is prohibited; quotations must cite authentic source files. |
| `US-HHS-PAGAC-2018-CARDIOMETABOLIC` | **FAIL** | `docs\phase11_parent_source_integrity_report.md` | 59 | REJECTED_DISALLOWED_PATH: Evidence path under docs/ or generated file is prohibited; quotations must cite authentic source files. |
| `US-HHS-PAGAC-2018-OLDER-ADULTS` | **FAIL** | `docs\phase11_parent_source_integrity_report.md` | 60 | REJECTED_DISALLOWED_PATH: Evidence path under docs/ or generated file is prohibited; quotations must cite authentic source files. |
| `OPENSTAX-AP2E-LICENSE` | **PASS** | `data\staging_phase11\quarantine_evidence\openstax_ap2e_biomechanics.html` | None | © Jun 12, 2026 OpenStax. Textbook content produced by OpenStax is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike Lic |
| `OPENSTAX-AP2E-AI` | **FAIL** | `data\staging_phase11\quarantine_evidence\openstax_ap2e_biomechanics.html` | None | NO_EVIDENCE_FOUND |


---

## 6. Task 5: Ledger & Quarantine Record Remediation Audit

Audits ledger-only modifications in `data/staging_phase11/intake_registry.json` and `openstax_ap2e_quarantine_record.json` (zero data file modifications):

### 6.1 Third-Party Exclusions Population (Task 5a)
- `US-HHS-PAGAC-2018-CARDIOMETABOLIC`: Populated with authentic line numbers:
  - **Line 276**: `Source: Adapted from data found in Brown et al., 2016. 20`
  - **Line 298**: `Source: Adapted from data found in Rosenberg et al., 2013. 39`
- `US-HHS-PAGAC-2018-OLDER-ADULTS`: Populated with bibliographic reference lines:
  - **Line 419**: `52. Studenski S, Perera S, Patel K, et al. Gait speed and survival in older adults...`
  - **Line 423**: `347. doi:10.1016/j.gerinurse.2016.04.013.`
- `US-ARMY-FM-7-22`: Populated with proprietary trademark exclusions (Pose Method® of Running, Nicholas Romanov).

### 6.2 CDC Rows Policy Alignment (Task 5b)
- `attribution_required`: Set to `"requested by CDC policy"` across all 4 CDC sources.
- `cdc_policy_exceptions`: Added field explicitly quoting and citing CDC Agency Materials policy:
  > *"First, some resources, as well as images, on the CDC and ATSDR websites are restricted in their use because they were developed by government contractors or grantees, or have been licensed by a third party. Second, the U.S. government work designation does not apply to works of state and local governments... Third, copyright laws also differ internationally."*

### 6.3 PAGAC Rows Rights Basis & Verified Evidence (Task 5c)
- `rights_basis`: Set to `SITE_POLICY_BASIS_AUTHORSHIP_UNVERIFIED` across all 7 PAGAC rows.
- `evidence`: Grounded in verified ODPHP policy snapshot:
  - **Verified Sentence**: `"The information presented on odphp.health.gov — including information on odphp.health.gov microsites like MyHealthfinder, Healthy People, and Health Literacy Online — is in the public domain. This means it may be freely distributed and copied — but please include a link to our website and acknowledge ODPHP as the source."`
  - **Policy URL**: `https://odphp.health.gov/copyright-policy`
  - **Snapshot File**: `data/staging_phase11/quarantine_evidence/health_gov_copyright_policy_snapshot.html`
  - **Snapshot SHA-256**: `8d37aaa699a0c79d46fdd5e95850198b10c08a8b7f3afabb39037e30ab92a54a`
  - **Snapshot Timestamp UTC**: `2026-10-16T10:30:25Z`

### 6.4 Timestamp Remediation & Audit Findings (Task 5d)
- Every retrieval timestamp in `intake_registry.json` unbacked by a download log has been replaced with authentic file-system creation time converted to UTC and flagged `FS_TIME`.
- **OpenStax Record Audit**: The previously reported timestamp `2026-10-16T14:49:00Z` in `phase11_1_evidence_addendum.md` was discovered to reflect the local file-modification time of `openstax_anat_phys_2e_raw.txt` (14:49:57), which postdated the repository initialization commit at 10:53Z on Oct 14. This timestamp has been formally corrected to the authentic snapshot creation time `2026-10-16T09:19:39Z (FS_TIME)` in `openstax_ap2e_quarantine_record.json`.

---

## 7. Gate Line & Final Verification

```text
PHASE 11.3 GATE STATUS: GATE CLOSED — DIAGNOSTIC AUDIT COMPLETE
Slice Audit: COMPLETE (all 5 PAGAC slices mapped to authentic PDF pages)
Boundary Quality: COMPLETE (artifact distributions quantified across all 10 accepted docs)
Pillar Keyword Density: COMPLETE (matrix computed without narrative)
Evidence Verification: COMPLETE (all authentic quotes PASS; docs/ paths REJECTED)
Ledger Remediation: COMPLETE (third-party lines, CDC notes, PAGAC site policy, FS_TIME flags)
Pretraining Status: OFF (No model training started, zero weights modified)
```
