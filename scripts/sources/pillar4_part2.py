"""Pillar 4 Part 2: Nutrition Fundamentals and Hydration (Expansion).

Authoritative educational documents drawn from public domain and open-access sources:
- U.S. Department of Agriculture & U.S. Department of Health and Human Services (Dietary Guidelines for Americans 2020-2025, Public Domain)
- National Institutes of Health, Office of Dietary Supplements (Dietary Supplements for Exercise, Public Domain)
- Centers for Disease Control and Prevention (Water & Healthier Drinks, Public Domain)
"""

DOCUMENTS = [
    {
        "doc_id": "P4_29_DIETARY_FIBER_SCFA",
        "section_title": "DIETARY FIBER CLASSIFICATION, FERMENTATION, AND SHORT-CHAIN FATTY ACIDS",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_CARBS_METABOLISM",
        "text": """Dietary fiber comprises non-digestible soluble and insoluble carbohydrates and lignin intrinsic to plant matrices:
1. Classification:
   - Soluble (Viscous / Fermentable) Fiber (pectins, beta-glucans, psyllium, inulin): Dissolves in water to form a viscous gel in the gastrointestinal tract. Delays gastric emptying, blunts postprandial glucose surges, and binds bile acids in the small intestine, facilitating hepatic excretion and lowering circulating LDL-cholesterol.
   - Insoluble Fiber (cellulose, hemicellulose, lignin): Does not dissolve in water; increases fecal bulk, accelerates colonic transit time, and prevents diverticular disease and constipation.
2. Colonic Fermentation and Short-Chain Fatty Acids (SCFAs):
   - In the cecum and colon, anaerobic microbiota ferment prebiotic soluble fibers into short-chain fatty acids, predominantly acetate, propionate, and butyrate.
   - Butyrate serves as the primary metabolic energy substrate for colonic epithelial cells (colonocytes), maintaining intestinal mucosal barrier integrity and preventing systemic translocation of endotoxins (lipopolysaccharides).
   - Acetate and propionate are absorbed into the portal circulation, where propionate inhibits hepatic cholesterol synthesis and acetate acts as a signaling ligand modulating systemic lipid metabolism and appetite regulation.
3. Recommended Intake: 14 grams of fiber per 1,000 kcal consumed (roughly 28 to 38 g/day for adults)."""
    },
    {
        "doc_id": "P4_30_GLYCEMIC_INDEX_LOAD",
        "section_title": "GLYCEMIC INDEX AND GLYCEMIC LOAD: POSTPRANDIAL INSULINEMIC PROFILES",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_CARBS_METABOLISM",
        "text": """The impact of carbohydrate ingestion on blood glucose and insulin kinetics is evaluated through two metrics:
1. Glycemic Index (GI): Ranks carbohydrate-containing foods based on the incremental area under the 2-hour postprandial blood glucose curve (iAUC) compared against an equal 50-gram carbohydrate portion of pure glucose or white bread (standardized to 100):
   - High GI (>= 70): Rapidly digested and absorbed; causes steep spikes in blood glucose and insulin (e.g., maltodextrin, white rice, baked potatoes).
   - Moderate GI (56 to 69): Moderate absorption curve (e.g., sucrose, whole-wheat bread).
   - Low GI (<= 55): Slowly digested; causes gradual, sustained glucose release (e.g., legumes, intact oats, non-starchy vegetables).
2. Glycemic Load (GL): Incorporates both carbohydrate quality (GI) and the actual quantity of carbohydrates in a typical serving:
   GL = (GI x Grams of Available Carbohydrate in Serving) / 100.
3. Athletic Application:
   - Pre-Exercise (2 to 4 hours prior): Low-to-moderate GI foods maintain stable euglycemia without triggering rebound reactive hypoglycemia.
   - Immediate Post-Exercise: High GI carbohydrates accelerate glycogen synthase activation, maximizing the rate of muscle glycogen resynthesis during the initial 2-hour recovery window."""
    },
    {
        "doc_id": "P4_31_LIPID_CLASSES_FATTY_ACIDS",
        "section_title": "LIPID BIOCHEMISTRY: SATURATED, MONOUNSATURATED, AND OMEGA-3/6 POLYUNSATURATED FATTY ACIDS",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_FATS_HORMONES",
        "text": """Dietary lipids serve as energy-dense substrates (9 kcal/g), structural components of cell membranes, and precursors to steroid hormones and lipid signaling molecules:
1. Saturated Fatty Acids (SFAs): Hydrocarbon chains containing zero double bonds. High intake (especially palmitic acid C16:0 and myristic acid C14:0) downregulates hepatic LDL receptors, increasing circulating LDL-cholesterol. Guidelines recommend limiting SFAs to < 10% of total daily caloric intake.
2. Monounsaturated Fatty Acids (MUFAs): Possess a single double bond (predominantly oleic acid 18:1 n-9, found in olive oil and avocados). MUFAs enhance cell membrane fluidity, improve insulin sensitivity, and lower cardiovascular risk.
3. Polyunsaturated Fatty Acids (PUFAs) and Essential Fatty Acids:
   - Omega-6 Family (Linoleic acid 18:2 n-6): Converted to arachidonic acid, giving rise to pro-inflammatory 2-series prostaglandins and 4-series leukotrienes necessary for acute immune responses.
   - Omega-3 Family (Alpha-linolenic acid / ALA 18:3 n-3): Elongated into eicosapentaenoic acid (EPA 20:5 n-3) and docosahexaenoic acid (DHA 22:6 n-3). EPA and DHA give rise to anti-inflammatory resolvins, protectins, and 3-series prostaglandins, downregulating chronic systemic inflammation and supporting neuromuscular membrane conduction."""
    },
    {
        "doc_id": "P4_32_PROTEIN_QUALITY_DIAAS",
        "section_title": "PROTEIN QUALITY SCORING: PDCAAS VS DIGESTIBLE INDISPENSABLE AMINO ACID SCORE (DIAAS)",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_PROTEIN_MPS",
        "text": """Assessing dietary protein quality requires evaluating indispensable (essential) amino acid content relative to human physiological needs and true digestive absorption efficiency:
1. Protein Digestibility-Corrected Amino Acid Score (PDCAAS):
   - Historically used since 1991. Based on fecal digestibility measurements in rats.
   - Major Limitation: Fecal measurement fails to account for microbial fermentation of unabsorbed amino acids in the large intestine, falsely overestimating protein absorption. Furthermore, scores are truncated at 1.00, masking differences between superior proteins (e.g., whey and soy both scored 1.00).
2. Digestible Indispensable Amino Acid Score (DIAAS):
   - The modern standard established by the FAO. Measures true ileal digestibility at the terminal ileum before colonic microbial fermentation.
   - Scores are calculated individually for each essential amino acid and are not truncated:
     DIAAS = 100 x lowest value of [mg of digestible dietary indispensable amino acid in 1 g of test protein / mg of same amino acid in 1 g of reference protein].
   - High-Quality Rankings: Milk protein isolate (DIAAS 1.30-1.40), whey isolate (1.25), egg (1.18), beef (1.10). Plant proteins often score lower (soy isolate 0.90, pea 0.70, rice 0.45) due to limiting amino acids (methionine, lysine, or leucine).
3. Complementary Plant Proteins: Combining legumes (rich in lysine, low in methionine) with grains (rich in methionine, low in lysine) produces a complete amino acid profile."""
    },
    {
        "doc_id": "P4_33_ANABOLIC_RESISTANCE_AGING",
        "section_title": "ANABOLIC RESISTANCE IN AGING: THE ELEVATED LEUCINE THRESHOLD",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_PROTEIN_MPS",
        "text": """As individuals age past the fifth decade of life, skeletal muscle exhibits 'anabolic resistance'—a blunted muscle protein synthesis (MPS) response to equivalent doses of hyperaminoacidemia and hyperinsulinemia:
1. Cellular Mechanisms of Anabolic Resistance:
   - Sestrin2 Desensitization: The intracellular leucine sensor Sestrin2 requires higher cytosolic leucine concentrations to release its inhibition on GATOR2, delaying mTORC1 activation.
   - Splanchnic Extraction: Increased first-pass splanchnic extraction of ingested amino acids in the gut and liver leaves fewer circulating amino acids for peripheral musculature.
   - Microvascular Dysfunction: Impaired endothelial nitric oxide signaling reduces muscle perfusion following meal ingestion.
2. Overcoming Anabolic Resistance with the Elevated Leucine Threshold:
   - In young adults, 20 grams of high-quality protein containing ~2.0 grams of leucine maximally stimulates MPS.
   - In older adults (>= 60 years), 35 to 45 grams of protein containing 3.5 to 4.0 grams of leucine per bolus is required to trigger robust mTORC1 phosphorylation and overcome the anabolic resistance threshold.
   - Combining meal protein intake with resistance exercise primes the muscle, lowering the leucine threshold back toward youthful sensitivity levels."""
    },
    {
        "doc_id": "P4_34_NUTRIENT_TIMING_WINDOW",
        "section_title": "THE 'ANABOLIC WINDOW' RE-EVALUATED: PERI-WORKOUT TIMING VS DAILY TOTALS",
        "source_id": "US-NIH-ODS-SUPP",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_PROTEIN_MPS",
        "text": """A persistent dogma in sports nutrition is the concept of a narrow 30-minute 'anabolic window' immediately post-workout, during which protein and carbohydrates must be consumed to prevent muscle breakdown:
1. Chronobiology of Muscle Protein Synthesis:
   - Following a resistance training session, the sensitivity of skeletal muscle to amino acid ingestion remains significantly elevated for 24 to 48 hours.
   - The immediate post-exercise state is characterized by elevated muscle protein breakdown (MPB); however, MPB is promptly suppressed by minor elevations in circulating insulin (achievable with modest carbohydrate or protein intake).
2. Systematic Evidence:
   - High-rigor meta-analyses demonstrate that when total daily protein intake (1.6 to 2.2 g/kg/day) is matched, consuming protein immediately post-workout versus several hours later produces no statistically significant difference in chronic muscle hypertrophy or strength.
3. Practical Application:
   - The 'window of opportunity' is a broad period of roughly 4 to 6 hours centered around the training bout.
   - Consuming a protein-rich meal (0.40 to 0.55 g/kg) 1 to 2 hours pre-workout ensures circulating amino acids remain elevated throughout the workout and immediate recovery phase, rendering immediate post-workout ingestion less critical."""
    },
    {
        "doc_id": "P4_35_HYDRATION_ASSESSMENT_METRICS",
        "section_title": "HYDRATION STATUS ASSESSMENT: URINE SPECIFIC GRAVITY AND BODY MASS VARIATIONS",
        "source_id": "US-CDC-HYDRATION-2022",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_HYDRATION",
        "text": """Accurate assessment of hydration status requires utilizing validated clinical markers rather than subjective thirst perception alone:
1. Acute Body Mass Fluctuation (The Gold Standard for Acute Sweating):
   - 1 kilogram of acute body mass lost during an exercise bout equates to approximately 1 liter of sweat loss.
   - Percentage body weight loss indicates dehydration severity:
     * Mild Hypohydration: 1% to 2% loss (aerobic performance begins to degrade).
     * Moderate Dehydration: 3% to 5% loss (marked reductions in strength, endurance, cognitive function, and thermoregulatory capacity).
     * Severe Dehydration: > 6% loss (elevated risk of exertional heat stroke and circulatory collapse).
2. Urine Specific Gravity (USG):
   - Measured using an optical or digital refractometer to evaluate urine density relative to pure water (1.000):
     * Well-Hydrated (Euhydrated): USG < 1.020.
     * Hypohydrated: USG 1.020 to 1.029.
     * Severely Dehydrated: USG >= 1.030.
3. Armstrong Urine Color Scale: An 8-point validated color chart. Pale straw to clear urine (scores 1-3) indicates euhydration; dark amber to brownish urine (scores 6-8) indicates significant dehydration."""
    },
    {
        "doc_id": "P4_36_SWEAT_RATE_CALCULATION",
        "section_title": "SWEAT RATE CALCULATION: INDIVIDUALIZING REHYDRATION PROTOCOLS",
        "source_id": "US-CDC-HYDRATION-2022",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_HYDRATION",
        "text": """Sweat rates vary enormously among athletes (ranging from 0.5 to > 2.5 L/hr) based on genetics, body mass, metabolic rate, environmental temperature, humidity, and acclimatization:
1. Mathematical Sweat Rate Equation:
   Sweat Rate (L/hr) = [Pre-Exercise Mass (kg) - Post-Exercise Mass (kg) + Fluid Consumed (L) - Urine Output (L)] / Exercise Duration (hours).
   Example:
   - Pre-exercise weight: 80.0 kg.
   - Post-exercise weight: 78.5 kg (Mass loss = 1.5 kg).
   - Fluid consumed during workout: 0.5 L.
   - Urine output: 0.0 L.
   - Duration: 1.5 hours.
   - Total sweat loss = 1.5 kg + 0.5 L = 2.0 L.
   - Sweat Rate = 2.0 L / 1.5 hr = 1.33 L/hr.
2. Fluid Replacement Target:
   - During Exercise: Aim to replace roughly 60% to 80% of sweat losses (e.g., 800 to 1,000 mL/hr in this example) consumed in small boluses (150 to 250 mL every 15 to 20 minutes) to avoid gastrointestinal discomfort.
   - Post-Exercise: To achieve full rehydration, athletes must consume 125% to 150% of the remaining fluid deficit over 2 to 4 hours, compensating for ongoing obligatory renal urine output."""
    },
    {
        "doc_id": "P4_37_HYPONATREMIA_PATHOPHYSIOLOGY",
        "section_title": "EXERCISE-ASSOCIATED HYPONATREMIA (EAH): PATHOPHYSIOLOGY AND HAZARDS OF OVERDRINKING",
        "source_id": "US-CDC-HYDRATION-2022",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_HYDRATION",
        "text": """While dehydration is common, Exercise-Associated Hyponatremia (EAH) represents a potentially fatal fluid-electrolyte emergency caused by excessive consumption of hypotonic fluids:
1. Clinical Definition: Serum sodium concentration ([Na+]) falling below 135 mmol/L during or within 24 hours of prolonged physical activity (critical emergency when [Na+] < 125 mmol/L).
2. Primary Pathophysiology:
   - The primary driver is overdrinking water or hypotonic sports beverages at a rate exceeding renal excretion capacity (> 800 to 1,000 mL/hr).
   - Non-osmotic secretion of Arginine Vasopressin (AVP / Antidiuretic Hormone / ADH) triggered by stress, nausea, pain, or exercise prevents the kidneys from excreting free water.
   - Extracellular fluid becomes hypo-osmolar; water flows down its osmotic gradient into intracellular compartments, causing cerebral edema (brain swelling within the rigid cranium).
3. Clinical Presentation:
   - Early: Bloating, puffy fingers, nausea, vomiting, progressive throbbing headache.
   - Severe: Confusion, disorientation, seizures, non-cardiogenic pulmonary edema, respiratory arrest, and coma.
4. Emergency Treatment: Urgent administration of 100 mL boluses of 3% hypertonic saline to acutely raise intravascular osmolarity and draw water out of swelling brain tissue. Standard isotonic saline or oral water is strictly contraindicated."""
    },
    {
        "doc_id": "P4_38_MICRONUTRIENTS_IRON_FERRITIN",
        "section_title": "MICRONUTRIENT METABOLISM IN ATHLETES: IRON, FERRITIN, AND HEPCIDIN KINETICS",
        "source_id": "US-NIH-ODS-SUPP",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_MICRONUTRIENTS",
        "text": """Iron is an indispensable trace mineral central to oxygen transport, mitochondrial cellular respiration, and athletic work capacity:
1. Functional Pools:
   - Hemoglobin (65% of body iron): Transports oxygen in erythrocytes.
   - Myoglobin (10%): Facilitates intramuscular oxygen diffusion from sarcolemma to mitochondria.
   - Cytochromes and Iron-Sulfur Proteins: Catalyze electron transfer in Complexes I-IV of the mitochondrial respiratory chain.
2. The Hepcidin Regulatory Cascade:
   - Heavy physical exercise triggers a release of interleukin-6 (IL-6), which stimulates the liver to produce and secrete the peptide hormone hepcidin.
   - Hepcidin binds to the cellular iron exporter ferroportin on enterocytes and macrophages, inducing its internalization and lysosomal degradation.
   - Consequently, intestinal iron absorption and macrophage iron recycling are blocked for 3 to 6 hours post-exercise. Iron supplements must therefore be ingested well away from exercise windows (e.g., morning on resting days).
3. Athletic Iron Losses: Foot-strike hemolysis in runners, sweat iron losses, gastrointestinal micro-bleeding, and hematuria. Serum ferritin should be monitored; levels < 30 ng/mL in female athletes and < 40 ng/mL in male athletes indicate non-anemic iron deficiency that blunts oxidative adaptation."""
    },
    {
        "doc_id": "P4_39_CREATINE_MONOHYDRATE_BIOENERGETICS",
        "section_title": "CREATINE MONOHYDRATE: PHARMACOKINETICS, BRAIN BIOENERGETICS, AND PROTOCOLS",
        "source_id": "US-NIH-ODS-SUPP",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_SUPPLEMENTS",
        "text": """Creatine is a nitrogenous organic acid synthesized endogenously from arginine, glycine, and methionine, and stored primarily (95%) in skeletal muscle as free creatine and phosphocreatine (PCr):
1. Mechanism of Ergogenic Action:
   - PCr acts as a rapid, high-energy phosphate donor to ADP via the creatine kinase reaction, immediately resynthesizing ATP during maximal, explosive muscular contractions (0 to 10 seconds).
   - Expanding intramuscular total creatine stores by 20% to 40% accelerates PCr resynthesis during recovery intervals, increasing high-intensity exercise capacity and total volume-load.
2. Dosing Protocols:
   - Rapid Loading Protocol: 20 grams per day (divided into four 5-gram doses) for 5 to 7 days, followed by a maintenance dose of 3 to 5 grams per day. Maximizes muscle saturation within 1 week.
   - Slow Loading Protocol: 3 to 5 grams per day continuously for 28 days. Achieves identical intramuscular saturation levels as the rapid protocol without initial gastrointestinal distress or rapid water retention.
3. Emerging Neurological Evidence: Creatine crosses the blood-brain barrier via the SLC6A8 transporter, buffering cerebral ATP during acute sleep deprivation, cognitive fatigue, and mitigating mild traumatic brain injury (concussion) pathophysiology."""
    },
    {
        "doc_id": "P4_40_CAFFEINE_PHARMACOKINETICS",
        "section_title": "CAFFEINE ERGOGENICS: ADENOSINE RECEPTOR ANTAGONISM AND DOSING STRATEGIES",
        "source_id": "US-NIH-ODS-SUPP",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_SUPPLEMENTS",
        "text": """Caffeine (1,3,7-trimethylxanthine) is the most widely investigated and validated central nervous system stimulant in sports performance:
1. Primary Pharmacological Mechanism:
   - Structurally resembles the endogenous neuromodulator adenosine.
   - Competitive Antagonism of A1 and A2A Adenosine Receptors: By competitively binding to adenosine receptors in the central nervous system without activating them, caffeine prevents adenosine from exerting its normal inhibitory, sleep-inducing, and pain-sensitizing effects.
   - Downstream Effects: Increases central dopaminergic and noradrenergic transmission, elevates motor unit recruitment velocity, lowers perceived exertion (RPE) at submaximal workloads, and attenuates exercise-induced muscle pain perception.
2. Pharmacokinetics:
   - Rapid Absorption: Peak plasma concentrations are reached 30 to 60 minutes following oral ingestion.
   - Elimination Half-Life: Averages 4 to 6 hours in healthy adults, metabolized hepatically via the cytochrome P450 enzyme CYP1A2 into paraxanthine (84%), theobromine (12%), and theophylline (4%).
3. Dosing Guidelines:
   - Ergogenic Window: 3 to 6 mg/kg of body mass, consumed approximately 60 minutes prior to athletic performance. Doses exceeding 9 mg/kg do not provide additional ergogenic benefits and provoke adverse tachycardia, tremors, gastrointestinal distress, and anxiety."""
    }
]
