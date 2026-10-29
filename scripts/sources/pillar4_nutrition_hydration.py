"""Pillar 4: Nutrition Fundamentals and Hydration.

Authoritative educational documents drawn from public domain and open-access sources:
- USDA & HHS Dietary Guidelines for Americans 2020-2025 (Public Domain)
- National Institutes of Health / Office of Dietary Supplements (ODS, Public Domain)
- CDC / NIOSH Criteria on Hydration and Heat Stress (Public Domain)
- CDC Division of Nutrition, Physical Activity, and Obesity (DNPAO, Public Domain)
"""

DOCUMENTS = [
    {
        "doc_id": "P4_01_ENERGY_BALANCE_TDEE",
        "section_title": "THERMODYNAMIC ENERGY BALANCE AND COMPONENTS OF TOTAL DAILY ENERGY EXPENDITURE",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_ENERGY",
        "text": """Energy balance is the fundamental physical principle governing long-term changes in human body mass and composition, grounded in the first law of thermodynamics:
Delta Body Energy Stores = Energy Intake - Energy Expenditure.
Total Daily Energy Expenditure (TDEE) is partitioned into four distinct biological components:
1. Basal Metabolic Rate (BMR) / Resting Energy Expenditure (REE): Comprises 60% to 75% of TDEE in sedentary individuals, representing the obligate energy cost of maintaining basic cellular homeostasis, central nervous system respiration, cardiovascular circulation, and organ function at rest.
2. Thermic Effect of Food (TEF): Represents roughly 8% to 10% of total energy intake, reflecting the caloric expenditure required to digest, absorb, transport, and metabolize ingested macronutrients (highest for protein at 20-30%, moderate for carbohydrates at 5-10%, lowest for dietary fats at 0-3%).
3. Non-Exercise Activity Thermogenesis (NEAT): Accounts for 10% to 20% of TDEE, encompassing spontaneous daily physical movements such as walking, fidgeting, maintaining posture, stair climbing, and occupational tasks. NEAT exhibits profound inter-individual variability (differing by up to 1,000 to 2,000 kcal/day).
4. Exercise Activity Thermogenesis (EAT): Comprises 5% to 15% of TDEE in recreational lifters, representing the deliberate energetic cost of structured resistance training and cardiovascular exercise."""
    },
    {
        "doc_id": "P4_02_CALORIC_SURPLUS_HYPERTROPHY",
        "section_title": "ENERGY INTAKE FOR HYPERTROPHY: THE CALORIC SURPLUS THRESHOLD",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_ENERGY",
        "text": """Muscular hypertrophy is an energetically demanding biological process requiring substantial cellular energy for ribosomal biogenesis, transcription, translation, and accretion of new contractile myofibrillar tissue.
Establishing a mild hypercaloric state—where energy intake moderately exceeds Total Daily Energy Expenditure (TDEE)—creates an optimal metabolic environment for lean tissue growth:
A modest caloric surplus of approximately 200 to 400 kcal per day above maintenance energy expenditure provides sufficient substrate to maximize muscle protein synthesis rates while minimizing excessive adipose tissue accumulation.
This caloric surplus typically yields a gradual, sustainable weight gain of roughly 0.25% to 0.5% of total body mass per week in intermediate lifters (approximately 0.5 to 1.0 kg / 1 to 2 lb per month).
Attempting overly aggressive caloric surpluses (often termed 'dirty bulking' exceeding 500 to 1,000 kcal/day above maintenance) does not accelerate muscle protein synthesis beyond its physiological ceiling; instead, the excess caloric energy is partitioned predominantly into subcutaneous and visceral adipose depots, requiring extended dieting phases later that risk catabolizing hard-won muscle mass."""
    },
    {
        "doc_id": "P4_03_CALORIC_DEFICIT_FAT_LOSS",
        "section_title": "ENERGY INTAKE FOR FAT LOSS: CALORIC DEFICITS AND LEAN MASS RETENTION",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_ENERGY",
        "text": """Body fat reduction requires a sustained hypocaloric state, where daily energy intake is less than Total Daily Energy Expenditure, forcing the endocrine system to mobilize stored endogenous lipids via lipolysis.
To preserve fat-free skeletal muscle mass and athletic performance during a fat loss phase, the rate of weight loss and the depth of the caloric deficit must be carefully managed:
A moderate caloric deficit of 300 to 500 kcal per day below maintenance—yielding a steady rate of body mass reduction between 0.5% and 1.0% of total body weight per week—is the gold standard for athletes.
Severe, crash-dieting caloric deficits (exceeding 750 to 1,000 kcal/day, or losing >1.5% of body mass per week) induce deleterious neuroendocrine and metabolic adaptations:
1. Marked elevation in circulating cortisol paired with significant suppression of total and free testosterone, luteinizing hormone (LH), and thyroid hormones (triiodothyronine T3).
2. Accelerated breakdown of skeletal muscle myofibrillar proteins via the ubiquitin-proteasome proteolytic pathway to provide substrate for hepatic gluconeogenesis.
3. Substantial reduction in resting metabolic rate (adaptive thermogenesis) and severe depression of spontaneous NEAT."""
    },
    {
        "doc_id": "P4_04_PROTEIN_REQUIREMENTS_ATHLETES",
        "section_title": "DIETARY PROTEIN REQUIREMENTS FOR RESISTANCE-TRAINED POPULATIONS",
        "source_id": "US-NIH-ODS-PERF",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_PROTEIN",
        "text": """Dietary protein supplies the essential amino acids (EAAs) that serve as mandatory building blocks for muscle protein accretion, cellular repair, enzyme synthesis, and structural remodeling following resistance training.
While the standard Recommended Dietary Allowance (RDA) for sedentary adults is established at 0.8 grams per kilogram of body weight per day (g/kg/day), this baseline intake is designed merely to prevent clinical nutritional deficiency states in sedentary populations and is inadequate for athletes engaging in intense physical training.
Extensive scientific consensus from clinical nitrogen balance studies and contemporary Indicator Amino Acid Oxidation (IAAO) research establishes that to maximize skeletal muscle hypertrophy and strength gains:
Resistance-trained individuals require a daily protein intake ranging between 1.6 and 2.2 grams per kilogram of body weight per day (approximately 0.73 to 1.0 grams per pound of body weight per day).
Consuming protein within this empirical range ensures full saturation of the muscle protein synthesis machinery, promotes positive daily nitrogen balance, and supports optimal recovery of muscular and connective tissues."""
    },
    {
        "doc_id": "P4_05_PROTEIN_HYPOCALORIC_PHASES",
        "section_title": "ELEVATED PROTEIN REQUIREMENTS DURING HYPOCALORIC DEFICIT PHASES",
        "source_id": "US-NIH-ODS-PERF",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_PROTEIN",
        "text": """During hypocaloric phases (caloric restriction aimed at reducing body fat), skeletal muscle tissue is placed under elevated catabolic risk.
When endogenous energy reserves are depleted, whole-body muscle protein breakdown (MPB) rates rise, and amino acids are increasingly oxidized as metabolic fuel or converted to glucose in the liver.
Consequently, empirical protein requirements rise significantly above baseline training levels during a caloric deficit:
Research indicates that resistance-trained individuals in an energy deficit should elevate their daily protein intake to 2.0 to 2.4 g/kg/day (and in exceptionally lean athletes preparing for competition, up to 2.3 to 3.1 g/kg of fat-free mass per day).
Elevated protein intake during caloric restriction confers three distinct physiological benefits:
1. Protein Sparing: Provides abundant exogenous amino acids, suppressing the catabolism of endogenous myofibrillar tissue.
2. Superior Satiety: Protein stimulates the release of gut satiety hormones (peptide YY, cholecystokinin CCK, glucagon-like peptide-1 GLP-1) while suppressing the hunger hormone ghrelin.
3. High Thermic Effect: Protein possesses a Thermic Effect of Food (TEF) of 20% to 30%, meaning nearly a quarter of ingested protein calories are dissipated as metabolic heat during processing."""
    },
    {
        "doc_id": "P4_06_AMINO_ACID_PROFILE",
        "section_title": "ESSENTIAL AMINO ACIDS AND THE BRANCHED-CHAIN AMINO ACID TRIO",
        "source_id": "US-NIH-ODS-PERF",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_PROTEIN",
        "text": """Dietary proteins are composed of 20 standard amino acids, categorized physiologically into non-essential, conditionally essential, and essential amino acids:
The 9 Essential Amino Acids (EAAs)—histidine, isoleucine, leucine, lysine, methionine, phenylalanine, threonine, tryptophan, and valine—cannot be synthesized de novo by human enzymatic pathways and must be obtained entirely through the diet.
Among the EAAs, the three Branched-Chain Amino Acids (BCAAs)—leucine, isoleucine, and valine—possess aliphatic branched carbon side chains and are metabolized directly within skeletal muscle tissue rather than primarily in the liver.
Crucially, isolated BCAA supplementation is physiologically inferior to consuming intact protein sources or complete EAA mixtures:
While leucine initiates the intracellular signal for protein synthesis, all 9 EAAs must be present in adequate concentrations in the sarcoplasm to serve as physical building blocks for new polypeptide chains.
In the absence of a complete pool of all EAAs, muscle protein synthesis terminates prematurely, and the body may break down endogenous muscle proteins to supply the missing essential amino acids."""
    },
    {
        "doc_id": "P4_07_LEUCINE_TRIGGER_MTOR",
        "section_title": "THE LEUCINE TRIGGER THRESHOLD AND MTORC1 ACTIVATION KINETICS",
        "source_id": "US-NIH-ODS-PERF",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_PROTEIN",
        "text": """Within the pool of essential amino acids, L-leucine functions not only as a structural building block but as an indispensable biochemical metabolic trigger.
Intracellular leucine concentrations are monitored inside myocytes by specialized sestrin2 nutrient sensors.
When sarcoplasmic leucine levels reach the 'leucine trigger threshold'—typically requiring approximately 2.5 to 3.0 grams of leucine in a single feeding (equivalent to 25 to 40 grams of high-quality intact animal or enriched plant protein)—sestrin2 releases its inhibition on the GATOR2 protein complex.
This event facilitates the activation of Rag GTPases, which recruit the mechanistic target of rapamycin complex 1 (mTORC1) to the lysosomal membrane where it is activated by Rheb.
Active mTORC1 phosphorylates downstream translational effectors, principally p70S6 kinase (p70S6K) and eukaryotic initiation factor 4E-binding protein 1 (4E-BP1).
This phosphorylation cascade unlocks the ribosomal machinery, initiating translation of mRNA into new contractile proteins.
Meals that fail to achieve the leucine threshold (e.g., small 5 to 10 gram protein snacks) stimulate significantly weaker and transient MPS responses."""
    },
    {
        "doc_id": "P4_08_MPS_KINETICS_MUSCLE_FULL",
        "section_title": "MUSCLE PROTEIN SYNTHESIS KINETICS AND THE REFRACTORY MUSCLE-FULL EFFECT",
        "source_id": "US-NIH-ODS-PERF",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_PROTEIN",
        "text": """Following the ingestion of a protein bolus containing sufficient leucine and essential amino acids, Muscle Protein Synthesis (MPS) follows a characteristic temporal kinetic trajectory:
In resting and post-exercise muscle, MPS rates accelerate rapidly, peaking between 60 and 90 minutes post-prandial at rates two to three times baseline.
However, by 2 to 3 hours post-feeding, MPS rates decline back toward basal resting levels, even if circulating plasma amino acid concentrations and intracellular leucine levels remain highly elevated (hyperaminoacidemia).
This physiological phenomenon is known as the refractory 'muscle-full effect': once myocytes have synthesized a specific quota of protein, the translational machinery becomes temporarily refractory to further amino acid stimulation.
Because of this refractory period, continuously consuming small protein doses every hour or sipping amino acids throughout the day does not sustain elevated protein synthesis.
Instead, allowing plasma amino acid levels to return toward baseline between distinct, substantial protein feedings optimizes the oscillatory responsiveness of the mTORC1 pathway across the day."""
    },
    {
        "doc_id": "P4_09_PROTEIN_DISTRIBUTION",
        "section_title": "OPTIMAL DAILY PROTEIN DISTRIBUTION AND MEAL SPACING PROTOCOLS",
        "source_id": "US-NIH-ODS-PERF",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_PROTEIN",
        "text": """To optimize 24-hour skeletal muscle protein accretion based on the muscle-full effect and leucine threshold kinetics, total daily protein intake should be evenly distributed across multiple distinct feedings.
Scientific evidence supports partitioning daily protein into 3 to 5 evenly spaced meals throughout the waking hours, separated by approximately 3 to 5 hours:
Each individual meal should provide approximately 0.40 to 0.55 grams of protein per kilogram of body weight (typically 25 to 45 grams of protein per feeding for most athletes):
- A practical 4-meal distribution schedule:
  * Breakfast (08:00): 0.45 g/kg protein.
  * Lunch (12:30): 0.45 g/kg protein.
  * Afternoon / Post-Workout (17:00): 0.45 g/kg protein.
  * Pre-Sleep Dinner / Snack (21:30): 0.45 to 0.55 g/kg protein (incorporating slow-digesting micellar casein or dairy proteins to sustain overnight aminoacidemia during nocturnal sleep).
Consuming the vast majority of daily protein in a single massive evening sitting (e.g., 120 grams in one meal and negligible protein earlier) produces suboptimal total daily protein synthesis compared to an evenly distributed feeding pattern."""
    },
    {
        "doc_id": "P4_10_PROTEIN_QUALITY_SCORING",
        "section_title": "PROTEIN QUALITY EVALUATION: DIAAS AND PDCAAS SCORING SYSTEMS",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_PROTEIN",
        "text": """Protein quality is assessed scientifically through validated scoring indices that quantify essential amino acid profile and gastrointestinal digestibility:
Historically, the Protein Digestibility-Corrected Amino Acid Score (PDCAAS) served as the standard metric; however, PDCAAS suffered from critical limitations, such as truncating scores at 1.00 and measuring fecal digestibility, which overlooks microbial amino acid fermentation in the large intestine.
The Food and Agriculture Organization (FAO) recommends the Digestible Indispensable Amino Acid Score (DIAAS) as the superior contemporary standard:
DIAAS measures true ileal amino acid digestibility at the end of the small intestine for each individual essential amino acid, without truncation.
Foods are classified based on DIAAS:
- Excellent Quality (DIAAS > 100%): Whey protein isolate, whole eggs, cow's milk, bovine muscle (beef), and micellar casein.
- High Quality (DIAAS 75% to 99%): Soy protein isolate, pea protein isolate, poultry, and fish.
- Moderate to Low Quality (DIAAS < 75%): Unprocessed grains, wheat gluten, legumes, and seeds, which are frequently limited in specific amino acids such as lysine, methionine, or threonine."""
    },
    {
        "doc_id": "P4_11_PLANT_VS_ANIMAL_PROTEIN",
        "section_title": "PLANT-BASED VERSUS ANIMAL-BASED PROTEIN AND COMPLEMENTARY PROFILES",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_PROTEIN",
        "text": """Athletes consuming plant-based (vegan or vegetarian) diets can achieve muscular hypertrophy and strength adaptations fully comparable to omnivorous athletes, provided appropriate dietary strategies are implemented.
Plant-based protein sources present distinct nutritional characteristics compared to animal proteins:
1. Amino Acid Limitations: Most individual plant proteins contain a lower proportion of one or more essential amino acids. For instance, cereal grains (wheat, rice, oats) are limited in lysine but rich in methionine, whereas legumes (beans, lentils, peas) are rich in lysine but limited in sulfur-containing amino acids (methionine and cysteine).
2. Lower Leucine Density: Plant proteins typically contain 6% to 8% leucine by weight, compared to 10% to 13% in dairy and whey proteins.
3. Lower Digestibility: Intact plant cellular walls (cellulose, fiber) and anti-nutritional factors (phytates, tannins) slightly reduce enzymatic digestion.
Plant-based athletes overcome these differences by:
- Consuming complementary plant proteins across the day (e.g., combining legumes with whole grains).
- Increasing total daily protein intake toward the higher bound of recommended ranges (1.8 to 2.4 g/kg/day).
- Utilizing purified plant isolates (pea and brown rice protein blends) that match the amino acid profile of whey."""
    },
    {
        "doc_id": "P4_12_CARBOHYDRATES_PHYSIOLOGY",
        "section_title": "DIETARY CARBOHYDRATES: THE PRIMARY FUEL FOR ANAEROBIC GLYCOLYSIS",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_CARBOHYDRATES",
        "text": """Dietary carbohydrates are the indispensable energetic substrate for high-intensity muscular work, anaerobic sprint intervals, and strenuous resistance training.
Following digestion and absorption, carbohydrates are stored endogenously as glycogen:
- Intramuscular Glycogen: Represents approximately 400 to 600 grams of glycogen stored directly within skeletal muscle tissue in trained individuals (equivalent to 1,600 to 2,400 kcal of rapidly accessible energy). Intramuscular glycogen lacks the enzyme glucose-6-phosphatase; consequently, muscle glycogen cannot enter the bloodstream and is utilized strictly by the host myocyte.
- Hepatic (Liver) Glycogen: Represents roughly 80 to 100 grams of glycogen (320 to 400 kcal), which is broken down via glycogenolysis to maintain systemic blood glucose homeostasis (normoglycemia at 70 to 100 mg/dL).
During high-volume resistance training (performing multiple sets of 8 to 15 repetitions), muscle glycogen is rapidly depleted, falling by 30% to 40% in targeted muscle groups over a single 45-minute workout, driving intracellular fatigue if carbohydrate replenishment is inadequate."""
    },
    {
        "doc_id": "P4_13_CARBOHYDRATE_REQUIREMENTS",
        "section_title": "CARBOHYDRATE INTAKE GUIDELINES FOR RESISTANCE AND POWER ATHLETES",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_CARBOHYDRATES",
        "text": """Dietary carbohydrate recommendations for athletes are calibrated to training volume, metabolic expenditure, and the duration of high-intensity physical exertion:
1. Low-Intensity or Skill-Based Training: 3 to 5 grams per kilogram of body weight per day (g/kg/day).
2. Moderate-Volume Resistance and Power Training: 4 to 7 g/kg/day (typically 300 to 550 grams daily for a 75 kg athlete). This intake supports full daily glycogen re-synthesis, maintains intracellular hydration, and preserves glycolytic work capacity across successive workouts.
3. High-Volume Endurance / Concurrent Training: 7 to 10 g/kg/day during heavy competitive blocks exceeding 2 to 3 hours of daily training.
The Dietary Guidelines for Americans recommend that carbohydrates comprise 45% to 65% of Total Daily Energy Expenditure (the Acceptable Macronutrient Distribution Range, AMDR).
Athletes should emphasize nutrient-dense carbohydrate sources—whole grains (oats, brown rice, quinoa), tubers (sweet potatoes, potatoes), fruits, and legumes—which provide complex starches alongside dietary fiber (28 to 38 g/day), B-vitamins, and essential antioxidant minerals."""
    },
    {
        "doc_id": "P4_14_GLYCOGEN_RESYNTHESIS",
        "section_title": "GLYCOGEN RESYNTHESIS KINETICS AND POST-EXERCISE REPLENISHMENT",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_CARBOHYDRATES",
        "text": """Following exhausting resistance or endurance exercise, the rate of glycogen resynthesis follows two distinct metabolic phases:
1. Rapid Insulin-Independent Phase (First 30 to 60 Minutes): Contraction-induced translocation of glucose transporter type 4 (GLUT4) vesicles to the sarcolemma persists in the immediate post-workout window, independent of insulin.
Concurrently, glycogen depletion stimulates the activation of glycogen synthase phosphatase, activating glycogen synthase.
Consuming high-glycemic carbohydrates during this window (1.0 to 1.2 grams per kilogram per hour) produces rapid glycogen resynthesis rates of 5 to 8 mmol/kg/hr.
2. Insulin-Dependent Phase: Beyond 60 minutes, glucose uptake requires insulin signaling.
Co-ingesting protein alongside carbohydrates (e.g., 0.8 g/kg carbohydrate + 0.3 to 0.4 g/kg protein) exerts a synergistic insulinotropic effect: amino acids stimulate pancreatic beta-cell insulin secretion, producing equivalent or superior glycogen storage rates compared to carbohydrates alone.
Complete replenishment of depleted muscle glycogen stores typically requires 20 to 24 hours of consistent carbohydrate consumption."""
    },
    {
        "doc_id": "P4_15_DIETARY_FATS_PHYSIOLOGY",
        "section_title": "DIETARY FATS: ESSENTIAL FATTY ACIDS, CELL MEMBRANES, AND JOINT HEALTH",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_FATS",
        "text": """Dietary lipids are indispensable macronutrients serving critical structural, hormonal, and metabolic roles in physical health and exercise adaptation:
Fats provide a concentrated energetic density of 9 kcal per gram, serve as the primary fuel source during rest and low-intensity aerobic activity (Zone 1/2), and are essential for the gastrointestinal absorption of fat-soluble vitamins (A, D, E, K).
At the cellular level, polyunsaturated fatty acids (PUFAs) are incorporated directly into the phospholipid bilayer of the sarcolemma and organelle membranes, modulating membrane fluidity, insulin receptor sensitivity, and ion transport kinetics.
Humans cannot synthesize two essential fatty acid families:
1. Omega-6 Linoleic Acid (LA), found in nuts, seeds, and vegetable oils.
2. Omega-3 Alpha-Linolenic Acid (ALA), found in flaxseeds, walnuts, and chia seeds.
Long-chain marine omega-3 fatty acids—eicosapentaenoic acid (EPA) and docosahexaenoic acid (DHA)—serve as precursors for specialized pro-resolving mediators (resolvins, protectins, maresins) that actively terminate excessive systemic inflammation, accelerate muscle tissue recovery, and reduce delayed onset muscle soreness (DOMS)."""
    },
    {
        "doc_id": "P4_16_DIETARY_FATS_HORMONES",
        "section_title": "DIETARY FATS: STEROID HORMONE SYNTHESIS AND THE 15-20% MINIMUM FLOOR",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_FATS",
        "text": """Beyond cellular structure, dietary cholesterol and saturated/monounsaturated fatty acids serve as the obligate biochemical precursors for the synthesis of steroid hormones, including testosterone, estrogen, progesterone, and cortisol.
Clinical nutritional trials consistently demonstrate that when athletes restrict dietary fat below 15% to 20% of total daily calories (or below 0.6 g/kg/day):
Circulating levels of total testosterone, free testosterone, and androstenedione decline significantly, accompanied by impaired lipid-soluble vitamin status.
The Acceptable Macronutrient Distribution Range (AMDR) for dietary fat is established at 20% to 35% of total daily energy intake (typically 0.8 to 1.2 grams per kilogram of body weight per day for athletes).
Athletes should emphasize monounsaturated fats (extra virgin olive oil, avocados, almonds) and polyunsaturated fats (fatty cold-water fish like salmon and mackerel) while limiting saturated fat to less than 10% of total calories to maintain healthy cardiovascular lipid profiles (LDL-C and apolipoprotein B).
Dietary fat should never be eliminated from an athletic nutritional plan."""
    },
    {
        "doc_id": "P4_17_HYDRATION_PHYSIOLOGY",
        "section_title": "HYDRATION PHYSIOLOGY AND THE 2% DEHYDRATION PERFORMANCE THRESHOLD",
        "source_id": "CDC-NIOSH-HYDRATE",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_HYDRATION",
        "text": """Water comprises approximately 60% to 70% of total adult human body mass and roughly 75% to 80% of skeletal muscle tissue volume.
During physical exercise, metabolic heat production increases by 15- to 20-fold above resting levels; to prevent hyperthermia, the body dissipates heat primarily through the evaporation of sweat from the skin surface.
When sweat losses exceed fluid intake, hypohydration (dehydration) ensues, producing profound physiological impairments:
1. Plasma Volume Reduction: Intravascular blood volume declines, decreasing venous return to the heart and lowering stroke volume.
2. Cardiovascular Drift: To maintain cardiac output (Q = Stroke Volume x Heart Rate), heart rate increases progressively by 3 to 6 beats/min for every 1% of body weight lost to sweat.
3. Performance Decrement: Dehydration exceeding 2% of total body mass (e.g., a 1.5 kg fluid loss in a 75 kg athlete) significantly degrades aerobic endurance capacity, elevates core body temperature, accelerates glycogen depletion, and reduces muscular endurance in multi-rep resistance sets.
Dehydration exceeding 4% to 5% reduces maximal muscular power and sharply increases the risk of exertional heat illnesses."""
    },
    {
        "doc_id": "P4_18_SWEAT_RATE_CALCULATION",
        "section_title": "SWEAT RATE DETERMINATION: PRE- AND POST-WORKOUT PROTOCOLS",
        "source_id": "CDC-NIOSH-HYDRATE",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_HYDRATION",
        "text": """Because individual sweat rates vary widely based on body mass, genetics, environmental temperature, relative humidity, and training intensity (ranging from 0.5 up to 2.5+ liters per hour), athletes should calculate their personal sweat rate under representative training conditions:
The standardized sweat rate calculation protocol:
1. Pre-Exercise Weigh-In: Weigh the athlete naked (or in minimal dry clothing) immediately prior to exercise on a calibrated digital scale (Weight_pre in kg).
2. Training Session: Execute a 60-minute training session at target intensity, recording the exact volume of fluid consumed during the workout (Fluid_consumed in liters).
3. Urine Volume: If urination occurs during the session, capture or estimate urine volume (Urine_volume in liters).
4. Post-Exercise Weigh-In: Towel off all sweat completely and re-weigh in identical clothing (Weight_post in kg).
Calculation Formula:
Sweat Rate (L/hr) = [Weight_pre (kg) - Weight_post (kg)] + Fluid_consumed (L) - Urine_volume (L).
Knowing this rate enables athletes to construct individualized fluid replacement strategies that prevent fluid deficits exceeding 2% of body mass."""
    },
    {
        "doc_id": "P4_19_PRE_EXERCISE_HYDRATION",
        "section_title": "PRE-EXERCISE HYDRATION GUIDELINES AND EUHYDRATION VERIFICATION",
        "source_id": "CDC-NIOSH-HYDRATE",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_HYDRATION",
        "text": """The primary objective of pre-exercise hydration is to commence physical exertion in a state of euhydration (normal total body water content) with normal electrolyte concentrations.
Athletes should initiate hydration protocols hours in advance of training:
- 4 Hours Prior to Exercise: Slowly consume 5 to 7 mL of fluid per kilogram of body weight (approximately 375 to 525 mL / 12 to 18 oz for a 75 kg athlete).
- 2 Hours Prior to Exercise: If the individual has not voided urine, or if urine remains dark and concentrated (urine specific gravity > 1.020), consume an additional 3 to 5 mL/kg (roughly 225 to 375 mL).
Consuming fluid well in advance allows sufficient time for gastrointestinal absorption, distribution across fluid compartments, and renal excretion of any temporary excess fluid.
Athletes can easily verify euhydration using the Armstrong 8-level Urine Color Chart: urine should resemble pale straw or light lemonade (levels 1 to 3); dark, amber urine (levels 5 to 8) indicates significant hypohydration requiring fluid replenishment."""
    },
    {
        "doc_id": "P4_20_INTRA_WORKOUT_FLUIDS",
        "section_title": "INTRA-WORKOUT HYDRATION AND CARBOHYDRATE-ELECTROLYTE REPLACEMENT",
        "source_id": "CDC-NIOSH-HYDRATE",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_HYDRATION",
        "text": """During exercise, the goal of fluid ingestion is to maintain hydration without over-drinking, preventing fluid deficits from exceeding 2% of baseline body mass.
For resistance training sessions lasting less than 60 minutes in temperate environments, plain water consumed ad libitum (according to thirst, typically 400 to 800 mL per hour consumed in small boluses of 150 to 250 mL every 15 to 20 minutes) is entirely sufficient.
However, during extended training sessions exceeding 60 to 90 minutes, or when exercising in hot, humid environments:
Consuming a 6% to 8% carbohydrate-electrolyte solution (providing 30 to 60 grams of rapidly digestible carbohydrates such as maltodextrin, glucose, or sucrose per hour, paired with 300 to 600 mg/L of sodium) provides distinct benefits:
1. Maintains Blood Glucose: Sparing liver glycogen reserves and sustaining central nervous system motor output.
2. Enhances Fluid Absorption: Intestinal glucose-sodium co-transporters (SGLT1) accelerate water absorption across the jejunal mucosa via osmotic drag.
3. Replaces Electrolyte Losses: Mitigating sweat sodium depletion."""
    },
    {
        "doc_id": "P4_21_POST_EXERCISE_REHYDRATION",
        "section_title": "POST-EXERCISE REHYDRATION PROTOCOLS AND FLUID VOLUME FORMULAS",
        "source_id": "CDC-NIOSH-HYDRATE",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_HYDRATION",
        "text": """Following strenuous physical training, rapid and complete restoration of fluid and electrolyte balance is vital, particularly when subsequent workouts are scheduled within the next 12 to 24 hours.
Because the kidneys continuously produce urine during the recovery period (obligate renal fluid losses), consuming a fluid volume merely equal to the sweat lost is insufficient to restore euhydration.
Evidence-based sports hydration guidelines prescribe consuming 125% to 150% of the total body mass lost during the workout:
Rehydration Volume = Body Mass Deficit (kg) x 1.25 to 1.50 Liters.
For example, if an athlete weighs 80.0 kg before training and 79.0 kg immediately after (a 1.0 kg sweat deficit), they should ingest 1.25 to 1.50 liters of fluid over the subsequent 2 to 4 hours.
Importantly, rehydration fluids must contain sodium (either within the beverage or through accompanying salted meals):
Drinking large volumes of plain, sodium-free water rapidly dilutes plasma osmolality, which shuts down pituitary vasopressin (antidiuretic hormone ADH) release, triggering premature diuresis and flushing the water out in urine before cellular rehydration can occur."""
    },
    {
        "doc_id": "P4_22_ELECTROLYTES_HYPONATREMIA",
        "section_title": "ELECTROLYTE HOMEOSTASIS AND EXERTIONAL HYPONATREMIA PATHOPHYSIOLOGY",
        "source_id": "CDC-NIOSH-HYDRATE",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_HYDRATION",
        "text": """Electrolytes—principally sodium (Na+), potassium (K+), chloride (Cl-), and magnesium (Mg2+)—are charged minerals essential for generating trans-membrane electrical potentials and propagating neuromuscular action potentials.
Sodium is the predominant osmotically active cation in extracellular fluid (normal serum range: 135 to 145 mmol/L), while potassium is the primary intracellular cation.
Sodium is the major electrolyte lost in human sweat, with concentrations typically ranging between 20 to 60 mmol/L (roughly 500 to 1,500 mg of sodium per liter of sweat).
A life-threatening clinical risk in athletic hydration is Exertional Hyponatremia (EAH), defined as a serum sodium concentration below 135 mmol/L resulting from over-drinking hypotonic fluids (plain water) that exceeds the renal excretory capacity.
As extracellular osmolality plummets, water moves down the osmotic gradient into intracellular compartments, causing cerebral edema (brain swelling).
Early symptoms include headache, nausea, malaise, and confusion; severe cases progress to seizures, coma, non-cardiogenic pulmonary edema, and death.
Athletes must avoid drinking beyond thirst or gaining weight during prolonged exercise."""
    },
    {
        "doc_id": "P4_23_MICRONUTRIENTS_IRON",
        "section_title": "MICRONUTRIENT BIOLOGY: IRON HOMEOSTASIS, FERRITIN, AND ATHLETIC HEALTH",
        "source_id": "US-NIH-ODS-PERF",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_MICRONUTRIENTS",
        "text": """Iron is an essential micronutrient serving as an indispensable functional constituent of hemoglobin (which transports oxygen in red blood cells), myoglobin (which stores and diffuses oxygen in skeletal myocytes), and cytochromes within the mitochondrial electron transport chain.
Active athletes—particularly female athletes and long-distance runners—exhibit elevated susceptibility to iron deficiency due to multiple factors:
- Exercise-Induced Hepcidin Elevation: Intense physical exertion triggers systemic secretion of interleukin-6 (IL-6), which stimulates hepatic production of hepcidin, a hormone that degrades ferroportin and blocks intestinal iron absorption for 3 to 6 hours post-exercise.
- Mechanical Foot-Strike Hemolysis: The physical impact of running crushes erythrocytes in the plantar capillaries.
- Sweat and Gastrointestinal Blood Losses: Micro-ischemia during prolonged exertion can produce subtle fecal occult blood loss.
Iron status should be evaluated clinically by measuring serum ferritin (reflecting intracellular iron stores) alongside hemoglobin:
Ferritin levels below 30 ng/mL indicate non-anemic iron deficiency, which degrades mitochondrial enzyme synthesis and impairs aerobic power output even before full-blown anemia develops."""
    },
    {
        "doc_id": "P4_24_MICRONUTRIENTS_CALCIUM_VITD",
        "section_title": "MICRONUTRIENTS: CALCIUM AND VITAMIN D SYNERGY IN BONE AND MUSCLE",
        "source_id": "US-NIH-ODS-PERF",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_MICRONUTRIENTS",
        "text": """Calcium and Vitamin D operate in tight physiological synergy to maintain skeletal structural integrity, regulate neuromuscular excitability, and mediate cross-bridge cycling:
The adult human body contains approximately 1,000 to 1,200 grams of calcium, 99% of which is stored as hydroxyapatite crystals in the skeletal matrix.
The remaining 1% of calcium resides in extracellular fluid and the sarcoplasm, where it acts as a critical second messenger triggering cross-bridge attachment and glycogen phosphorylase activation.
Vitamin D (1,25-dihydroxyvitamin D3 / calcitriol) is a steroid hormone synthesized endogenously when cutaneous 7-dehydrocholesterol absorbs solar ultraviolet B (UVB) radiation, or obtained through dietary sources and supplements.
Calcitriol binds to vitamin D receptors (VDR) in the intestinal enterocytes, upregulating calbindin proteins that increase active calcium absorption from 10-15% up to 30-40%.
Furthermore, VDRs are expressed directly within skeletal muscle myocytes, where vitamin D modulates myoblast proliferation, sarcoplasmic calcium handling, and Type II muscle fiber cross-sectional area.
Athletes should maintain serum 25-hydroxyvitamin D [25(OH)D] concentrations above 30 ng/mL (75 nmol/L) to prevent stress fractures and maintain optimal muscular force generation."""
    },
    {
        "doc_id": "P4_25_SUPPLEMENTS_CREATINE",
        "section_title": "EVIDENCE-BASED SUPPLEMENTS: CREATINE MONOHYDRATE BIOCHEMISTRY",
        "source_id": "US-NIH-ODS-PERF",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_SUPPLEMENTS",
        "text": """Creatine monohydrate is the most extensively researched, physiologically validated, and effective ergogenic dietary supplement available for enhancing high-intensity exercise capacity and muscular hypertrophy.
Synthesized endogenously in the liver and kidneys from arginine, glycine, and methionine (roughly 1 g/day) and obtained through red meat and fish, creatine is stored in skeletal muscle (95% of total body pool), with roughly 65% in the phosphorylated form as phosphocreatine (PCr).
Supplementing with creatine monohydrate elevates total intramuscular creatine stores by 15% to 30% and PCr stores by 10% to 40%.
This enhanced pool accelerates the resynthesis of ATP during short-duration, high-intensity efforts (sets of 1 to 10 repetitions), allowing athletes to complete 1 to 2 additional repetitions per working set.
Dosing Protocols:
1. Fast Loading Protocol: 20 grams per day (divided into four 5 g doses) for 5 to 7 days, followed by a continuous maintenance dose of 3 to 5 grams per day.
2. Slow Steady Protocol: 3 to 5 grams per day continuously, achieving identical intramuscular saturation over 21 to 28 days without gastrointestinal distress.
Extensive clinical trials confirm that creatine monohydrate is remarkably safe in healthy individuals, with zero evidence of renal dysfunction or cramping."""
    },
    {
        "doc_id": "P4_26_SUPPLEMENTS_CAFFEINE",
        "section_title": "EVIDENCE-BASED SUPPLEMENTS: CAFFEINE DOSING, PHARMACOKINETICS, AND LIMITATIONS",
        "source_id": "US-NIH-ODS-PERF",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_SUPPLEMENTS",
        "text": """Caffeine (1,3,7-trimethylxanthine) is a potent central nervous system stimulant with robust scientific evidence supporting its ergogenic efficacy across endurance, maximal strength, and ballistic power tasks.
Pharmacologically, caffeine crosses the blood-brain barrier rapidly and acts as a competitive antagonist of adenosine A1 and A2A receptors in the brain.
By blocking adenosine from binding, caffeine suppresses feelings of fatigue, elevates dopamine and norepinephrine neurotransmission, enhances motor unit recruitment firing rates, and reduces the subjective Rating of Perceived Exertion (RPE) during exercise.
Dosing Guidelines:
- Optimal Ergogenic Dose: 3 to 6 milligrams per kilogram of body weight (approximately 225 to 450 mg for a 75 kg athlete), ingested 45 to 60 minutes prior to exercise.
- Supramaximal Doses (>9 mg/kg): Do not confer additional performance benefits and frequently provoke adverse effects, including tremors, anxiety, tachycardia, gastrointestinal upset, and impaired motor coordination.
Safety Limitations:
Caffeine exhibits an elimination half-life of 4 to 6 hours; consuming high doses of caffeine within 8 to 10 hours of sleep severely disrupts slow-wave sleep (SWS) and suppresses nocturnal growth hormone secretion, impairing somatic recovery."""
    },
    {
        "doc_id": "P4_27_SUPPLEMENTS_BETA_ALANINE",
        "section_title": "EVIDENCE-BASED SUPPLEMENTS: BETA-ALANINE AND INTRACELLULAR CARNOSINE BUFFERING",
        "source_id": "US-NIH-ODS-PERF",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_SUPPLEMENTS",
        "text": """Beta-alanine is a non-proteinogenic amino acid that functions as the rate-limiting precursor in the intracellular synthesis of the cytoplasmic dipeptide carnosine (beta-alanyl-L-histidine).
Carnosine is stored in high concentrations within skeletal muscle myocytes (particularly Type II fast-twitch fibers), where its imidazole ring functions as an intracellular physicochemical buffer, binding excess free hydrogen ions (H+) during high-intensity anaerobic glycolysis.
By buffering protons, carnosine delays the onset of intracellular acidosis, preventing the inhibition of phosphofructokinase (PFK) and mitigating fatigue during sustained maximal efforts lasting between 1 and 4 minutes (e.g., 400-meter sprints, high-repetition resistance sets, combat sports rounds).
Dosing Protocol:
Chronic daily supplementation of 3.2 to 6.4 grams per day for 4 to 8 weeks is required to increase muscle carnosine stores by 40% to 80%.
Timing relative to exercise is irrelevant, as benefits depend on cumulative muscle loading over weeks.
Side Effect Profile:
Ingesting single doses exceeding 1.6 grams commonly induces acute paresthesia—a harmless, transient tingling or prickling sensation across the face, neck, and hands caused by beta-alanine binding to MrgprD receptors on sensory neurons.
Paresthesia can be completely prevented by dividing daily intake into smaller 1.0 to 1.6 g doses or utilizing sustained-release formulations."""
    },
    {
        "doc_id": "P4_28_SUPPLEMENTS_SODIUM_BICARBONATE",
        "section_title": "EVIDENCE-BASED SUPPLEMENTS: SODIUM BICARBONATE AND EXTRACELLULAR BUFFERING",
        "source_id": "US-NIH-ODS-PERF",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_SUPPLEMENTS",
        "text": """While carnosine acts as an intracellular buffer inside myocytes, sodium bicarbonate (NaHCO3) functions as a potent extracellular buffer in the blood plasma.
Intense anaerobic exercise drives massive efflux of hydrogen ions (H+) and lactate from active muscle cells into the capillary circulation via monocarboxylate transporters (MCTs).
Ingesting sodium bicarbonate acutely increases blood plasma bicarbonate concentration ([HCO3-]) and elevates blood pH (inducing mild metabolic alkalosis).
This expanded extracellular buffering capacity creates an enhanced transmembrane hydrogen ion gradient, accelerating the efflux of H+ out of contracting muscle fibers and delaying the development of intracellular acidosis during exhaustive bouts lasting 1 to 3 minutes.
Dosing and Administration:
The standard validated ergogenic dose is 0.2 to 0.3 grams per kilogram of body weight (roughly 15 to 22.5 grams for a 75 kg athlete), consumed 60 to 90 minutes prior to competition alongside 500 mL of water and a small carbohydrate meal.
Clinical Caution:
The primary limitation of sodium bicarbonate is severe gastrointestinal distress, including acute osmotic diarrhea, abdominal cramping, and nausea.
Athletes should split the dose across 30-minute intervals or utilize enteric-coated capsules to bypass stomach acidity."""
    }
]
