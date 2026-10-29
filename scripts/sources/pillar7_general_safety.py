"""Pillar 7: General Fitness Education and Age-Appropriate Safety.

Authoritative educational documents drawn from public domain and open-access sources:
- U.S. Department of Health and Human Services (Physical Activity Guidelines for Americans, 2nd ed., Public Domain)
- Centers for Disease Control and Prevention (CDC Physical Activity Basics, Public Domain)
- Centers for Disease Control and Prevention (CDC STEADI Older Adult Fall Prevention, Public Domain)
- National Institutes of Health / National Institute on Aging (NIH NIA Exercise & Physical Activity, Public Domain)
- Headquarters, Department of the Army (FM 7-22 Environmental and Safety Readiness, Public Domain)
"""

DOCUMENTS = [
    {
        "doc_id": "P7_01_LIFESPAN_PRESCHOOL",
        "section_title": "PHYSICAL ACTIVITY GUIDELINES ACROSS THE LIFESPAN: PRESCHOOL-AGED CHILDREN (AGES 3-5)",
        "source_id": "US-HHS-PAG-2018",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_LIFESPAN",
        "text": """Physical activity is essential from early childhood to foster healthy growth, motor skill development, and musculoskeletal integrity.
For preschool-aged children (ages 3 through 5 years):
1. Cumulative Daily Activity: Preschool children should be physically active throughout the day to enhance growth and development. Adult caregivers should encourage active play that includes a variety of activity types.
2. Target Volume: A reasonable target is roughly 3 hours of physical activity per day of various intensities (light, moderate, and vigorous), distributed across waking hours.
3. Movement Modalities: Unstructured play, climbing, jumping, running, hopping, and games that challenge balance and spatial awareness.
4. Health Outcomes: Enhanced bone health, healthy weight maintenance, improved cardiometabolic markers, and the fundamental acquisition of gross motor patterns necessary for lifelong physical literacy.
5. Inactivity Boundaries: Sedentary screen time should be restricted according to pediatric public health guidance to promote active physical exploration."""
    },
    {
        "doc_id": "P7_02_LIFESPAN_YOUTH",
        "section_title": "PHYSICAL ACTIVITY GUIDELINES: CHILDREN AND ADOLESCENTS (AGES 6-17)",
        "source_id": "US-HHS-PAG-2018",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_LIFESPAN",
        "text": """Children and adolescents (ages 6 through 17 years) require regular moderate-to-vigorous physical activity to support physiological maturation, cognitive performance, and bone density accretion.
The evidence-based guidelines specify three critical components:
1. Daily Aerobic Volume: Children and adolescents should accumulate at least 60 minutes (1 hour) or more of moderate-to-vigorous physical activity (MVPA) daily.
   - Most of the 60 minutes should be either moderate- or vigorous-intensity aerobic physical activity.
   - Vigorous-intensity physical activity should be included on at least 3 days per week.
2. Muscle-Strengthening Activity: As part of their 60 or more daily minutes, children and adolescents should include muscle-strengthening physical activity (such as climbing trees, playground equipment, bodyweight exercises, or structured resistance training) on at least 3 days per week.
3. Bone-Strengthening Activity: Activities that produce mechanical impact forces on bones (running, jumping rope, basketball, gymnastics) must be incorporated on at least 3 days per week to maximize peak bone mass acquisition during adolescent growth spurts."""
    },
    {
        "doc_id": "P7_03_PEDIATRIC_RESISTANCE_TRAINING",
        "section_title": "PEDIATRIC RESISTANCE TRAINING: EVIDENCE, SAFETY, AND GROWTH PLATE MYTHS",
        "source_id": "US-HHS-PAG-2018",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_PEDIATRIC_TRAINING",
        "text": """Historical concerns that supervised resistance training damages growth plates (epiphyseal plates) or stunts growth in children and adolescents are completely refuted by extensive sports medicine and physiological research.
1. Growth Plate Safety: The cartilaginous epiphyseal plate is susceptible to acute shearing fractures from unsupervised, high-impact collisions or catastrophic lifting accidents; however, comprehensive epidemiological studies show that properly supervised, age-appropriate youth resistance training carries an injury rate significantly lower than common youth team sports (soccer, football, gymnastics).
2. Primary Adaptation Mechanisms: Pre-pubescent children experience strength gains primarily through neural adaptations rather than muscle hypertrophy:
   - Enhanced motor unit recruitment and synchronization.
   - Improved agonist-antagonist co-activation efficiency.
   - Increased central motor drive and intermuscular coordination.
   Post-pubescent adolescents experience both neural and hypertrophic adaptations mediated by circulating sex steroid hormones (testosterone and estrogen).
3. Programming Guidelines:
   - Strict Qualified Adult Supervision: High instructor-to-child ratio focusing exclusively on movement execution.
   - Repetition Ranges: Moderate loads (1 to 3 sets of 8 to 15 repetitions), avoiding 1RM maximal testing.
   - Progression: Technical mastery must precede any load increases."""
    },
    {
        "doc_id": "P7_04_LIFESPAN_ADULTS",
        "section_title": "PHYSICAL ACTIVITY GUIDELINES: ADULTS (AGES 18-64)",
        "source_id": "US-HHS-PAG-2018",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_LIFESPAN",
        "text": """Substantial health benefits accrue to adults who engage in regular physical activity. The U.S. Physical Activity Guidelines establish specific aerobic and muscle-strengthening benchmarks:
1. Aerobic Activity Thresholds:
   - Moderate-Intensity: At least 150 minutes (2 hours and 30 minutes) to 300 minutes (5 hours) a week of moderate-intensity physical activity (e.g., brisk walking at 3.0 to 4.5 mph).
   - Vigorous-Intensity: Or 75 minutes (1 hour and 15 minutes) to 150 minutes (2 hours and 30 minutes) a week of vigorous-intensity aerobic physical activity (e.g., jogging, running, lap swimming).
   - Equivalent Combination: An equivalent combination of moderate- and vigorous-intensity aerobic activity, spread throughout the week. 1 minute of vigorous activity equates to approximately 2 minutes of moderate activity.
2. Muscle-Strengthening Requirements:
   - Adults should also do muscle-strengthening activities of moderate or greater intensity that involve all major muscle groups (legs, hips, back, abdomen, chest, shoulders, and arms) on 2 or more days a week.
3. Dose-Response Relationship: Health benefits (reductions in cardiovascular disease, all-cause mortality, type 2 diabetes, and specific cancers) increase with higher volumes, but the steepest risk reduction curve occurs when transitioning from complete physical inactivity to meeting the baseline threshold."""
    },
    {
        "doc_id": "P7_05_LIFESPAN_OLDER_ADULTS",
        "section_title": "PHYSICAL ACTIVITY GUIDELINES: OLDER ADULTS (AGES 65 AND OLDER)",
        "source_id": "US-HHS-PAG-2018",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_LIFESPAN",
        "text": """For older adults (ages 65 and older), regular physical activity is critical for maintaining functional independence, cognitive function, and preventing debilitating falls.
Older adults should follow the adult guidelines with critical additions:
1. Multicomponent Physical Activity: Older adults should engage in multicomponent physical activity that includes balance training as well as aerobic and muscle-strengthening activities. This combination is proven to prevent falls and reduce fall-related injuries.
2. Relative Intensity: When chronic conditions limit the ability to meet standard adult guidelines, older adults should be as physically active as their abilities and conditions allow. Intensity should be determined relative to the individual's functional fitness level rather than absolute MET values.
3. Fall Prevention Mechanisms: Progressive resistance training counteracts age-related muscle wasting (sarcopenia), while dynamic balance exercises (tandem walking, single-leg stands, heel-to-toe walking) enhance proprioceptive feedback and vestibular coordination.
4. Cognitive Benefits: Regular aerobic and resistance exercise enhances executive cognitive function, spatial memory, and hippocampal plasticity, mitigating neurodegenerative decline."""
    },
    {
        "doc_id": "P7_06_PREGNANCY_POSTPARTUM",
        "section_title": "EXERCISE DURING PREGNANCY AND THE POSTPARTUM PERIOD: GUIDELINES AND PRECAUTIONS",
        "source_id": "US-HHS-PAG-2018",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_SPECIAL_POPULATIONS",
        "text": """Physical activity during pregnancy and the postpartum period confers profound maternal and fetal health benefits, including reduced risk of gestational diabetes, preeclampsia, gestational hypertension, excessive gestational weight gain, and postpartum depression.
1. Guideline Recommendations: Women should do at least 150 minutes (2 hours and 30 minutes) of moderate-intensity aerobic physical activity per week during pregnancy and postpartum, preferably spread throughout the week.
2. Continuity: Women who habitually engaged in vigorous-intensity aerobic activity or resistance training prior to pregnancy can safely continue these activities throughout pregnancy, provided they discuss adaptations with their healthcare provider.
3. Safety Precautions:
   - Supine Position Avoidance: After the first trimester, exercises performed lying flat on the back (supine) should be avoided because the enlarged uterus compresses the inferior vena cava, impairing maternal venous return, cardiac output, and uteroplacental blood flow.
   - Fall and Trauma Risks: Avoid contact sports, activities with high fall risk (horseback riding, downhill skiing, gymnastics), and scuba diving (fetal pulmonary decompression sickness risk).
   - Thermoregulation: Avoid exercising in high heat and humidity; maintain adequate hydration.
4. Warning Signs to Terminate Exercise: Vaginal bleeding, regular painful uterine contractions, amniotic fluid leakage, dizziness, dyspnea prior to exertion, chest pain, or calf pain/swelling."""
    },
    {
        "doc_id": "P7_07_CHRONIC_CONDITIONS",
        "section_title": "EXERCISE IN CHRONIC CONDITIONS: RISK-BENEFIT RATIO AND MODIFICATIONS",
        "source_id": "US-HHS-PAG-2018",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_SPECIAL_POPULATIONS",
        "text": """For adults with chronic conditions (such as hypertension, type 2 diabetes, osteoarthritis, or stable cardiovascular disease) or disabilities, physical activity is a potent therapeutic modality that reduces morbidity and enhances quality of life.
1. Guiding Principle: Some physical activity is significantly better than none. Adults with chronic conditions should avoid physical inactivity.
2. Target: When able, adults with chronic conditions should aim for 150 to 300 minutes of moderate-intensity aerobic activity and 2 or more days of muscle strengthening per week.
3. Condition-Specific Modifications:
   - Osteoarthritis: Low-impact activities (swimming, cycling, water aerobics, brisk walking) reduce joint impact stress while strengthening periarticular musculature to improve joint stability.
   - Type 2 Diabetes: Combining aerobic exercise with progressive resistance training enhances non-insulin-mediated glucose uptake via skeletal muscle GLUT4 translocation, dramatically improving glycemic control.
   - Hypertension: Aerobic and isometric resistance training reduce resting systolic and diastolic blood pressure by 5 to 8 mmHg through enhanced endothelial nitric oxide release and reduced systemic vascular resistance.
4. Safe Customization: Prescriptions must accommodate functional limitations and avoid exacerbating acute flare-ups."""
    },
    {
        "doc_id": "P7_08_PARQ_SCREENING",
        "section_title": "PRE-EXERCISE SCREENING: THE PAR-Q+ AND PARTICIPATION READINESS ALGORITHM",
        "source_id": "US-CDC-PA-2022",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_SCREENING_RISK",
        "text": """Pre-exercise screening identifies individuals with potential medical contraindications to exercise, ensuring safe exercise initiation while minimizing unnecessary barriers to physical activity.
1. The PAR-Q+ (Physical Activity Readiness Questionnaire for Everyone): A validated, 7-question evidence-based self-screening tool:
   - Questions assess chest pain during rest or physical activity, loss of balance due to dizziness or consciousness loss, diagnosed heart conditions, bone or joint problems worsened by exercise, and current cardiovascular medications.
   - If an individual answers 'NO' to all 7 baseline questions, they are cleared for physical activity participation.
   - If an individual answers 'YES' to one or more questions, they proceed to follow-up questions or are directed to a physician for medical clearance.
2. Modern Screening Shift: Contemporary sports medicine paradigms (e.g., ACSM guidelines) emphasize reducing unnecessary medical clearance barriers for asymptomatic individuals, prioritizing screening based on:
   - Current physical activity habits (sedentary vs habitually active).
   - Presence of known cardiovascular, metabolic, or renal disease.
   - Presence of major signs or symptoms suggestive of underlying cardiovascular or metabolic disease."""
    },
    {
        "doc_id": "P7_09_RED_FLAG_SYMPTOMS",
        "section_title": "CARDIOVASCULAR RED FLAGS: SYMPTOMS MANDATING IMMEDIATE EXERCISE CESSATION",
        "source_id": "US-CDC-PA-2022",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_SCREENING_RISK",
        "text": """During physical activity or fitness testing, certain acute clinical signs and symptoms indicate potential life-threatening cardiovascular, neurological, or metabolic emergencies, requiring immediate exercise cessation and urgent medical evaluation:
1. Anginal Pain: Chest discomfort, retrosternal pressure, squeezing, or fullness radiating to the jaw, neck, left arm, or between the shoulder blades.
2. Inappropriate Dyspnea: Severe shortness of breath disproportionate to the workload or uncharacteristic breathlessness during light activity.
3. Syncope and Presyncope: Dizziness, lightheadedness, or sudden loss of consciousness during or immediately following exertion, often signifying acute cerebral hypoperfusion secondary to cardiac dysrhythmia or outflow obstruction.
4. Ataxia and Neurological Symptoms: Staggering gait, uncoordinated movements, confusion, speech difficulties, or visual disturbances.
5. Pathological Heart Rate or Blood Pressure Kinetics:
   - Failure of heart rate to rise with increasing exercise intensity (chronotropic incompetence).
   - Exertional hypotension: A drop in systolic blood pressure (> 10 mmHg) below baseline despite an increase in workload, indicating ventricular pump failure.
   - Exaggerated hypertensive response (> 250 mmHg systolic or > 115 mmHg diastolic)."""
    },
    {
        "doc_id": "P7_10_RAMP_WARMUP_FRAMEWORK",
        "section_title": "THE RAMP WARM-UP FRAMEWORK: PHYSIOLOGICAL SYSTEM PREPARATION",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_WARMUP_COOLDOWN",
        "text": """The RAMP framework (developed by Ian Jeffreys) is an evidence-based system for structuring comprehensive warm-up protocols, systematically transitioning the human organism from rest to peak physical performance:
1. R — Raise:
   - Objective: Elevate core body temperature, muscular temperature, heart rate, respiration rate, and systemic blood flow.
   - Activities: Low-intensity multi-directional locomotion (jogging, skipping, rowing, low-intensity agility drills).
   - Physiology: Warmer muscle tissue lowers cellular viscosity, increases sarcolemmal conduction velocity, and shifts the oxyhemoglobin dissociation curve to the right (Bohr effect), enhancing oxygen unloading to working myocytes.
2. A — Activate:
   - Objective: Engage key stabilizing musculature, particularly the gluteal complex, rotator cuff, scapular retractors, and core musculature.
   - Activities: Glute bridges, band pull-aparts, lateral band walks, bird-dogs.
3. M — Mobilize:
   - Objective: Dynamically move joints through full sport-specific ranges of motion.
   - Activities: Multi-planar lunges with thoracic rotations, inchworms, hip openers.
4. P — Potentiate:
   - Objective: Maximize neuromuscular excitability and post-activation performance enhancement (PAPE) by performing movement-specific drills of increasing intensity.
   - Activities: Submaximal sprint accelerations, medicine ball throws, plyometric jumps, or progressive barbell warm-up sets leading up to working loads."""
    },
    {
        "doc_id": "P7_11_STATIC_STRETCHING_MYTHS",
        "section_title": "STATIC STRETCHING IN WARM-UPS: ACUTE FORCE IMPAIRMENT AND TIMING",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_WARMUP_COOLDOWN",
        "text": """A persistent misconception in exercise education is that prolonged static stretching before training prevents injury and prepares muscles for high-intensity output.
1. Acute Force Loss: Extensive biomechanical and neuromuscular research demonstrates that prolonged static stretching (holds > 45 to 60 seconds per muscle group) immediately prior to maximal exertion induces an acute reduction in:
   - Maximal voluntary isometric force (decreases of 5% to 8%).
   - Barbell velocity and explosive power output.
   - Vertical jump height and sprint acceleration.
2. Mechanisms of Force Deficit:
   - Mechanical: Decreased musculotendinous stiffness (increased compliance) slows mechanical force transmission from contracting sarcomeres across the tendon to the skeleton.
   - Neurological: Inhibition of spinal motoneuron excitability, blunted muscle spindle sensitivity, and autogenic inhibition mediated by Golgi tendon organs.
3. Injury Prevention Evidence: Pre-exercise static stretching has no statistically significant effect on reducing overall overuse or soft-tissue injury incidence.
4. Correct Implementation: Dynamic stretching should be utilized during warm-ups. Prolonged static stretching should be reserved for the cool-down or dedicated flexibility sessions where chronic range-of-motion expansion is the primary objective."""
    },
    {
        "doc_id": "P7_12_COOLDOWN_PHYSIOLOGY",
        "section_title": "COOL-DOWN PHYSIOLOGY: VENOUS POOLING PREVENTION AND AUTONOMIC RESTORATION",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_WARMUP_COOLDOWN",
        "text": """Abrupt cessation of vigorous physical exercise without an active cool-down period imposes acute cardiovascular stress:
1. Prevention of Venous Blood Pooling: During vigorous exercise, rhythmic muscular contractions compress intramuscular veins, operating as the 'skeletal muscle pump' to drive large volumes of venous blood back to the right atrium of the heart against gravity. If intense exercise halts abruptly, systemic vasodilation in peripheral muscular beds persists, but the skeletal muscle pump stops instantly. Blood pools in lower extremity capacitance veins, causing an acute drop in venous return, stroke volume, and cardiac output, resulting in post-exercise orthostatic hypotension, dizziness, or syncope.
2. Active Cool-down Protocol: 5 to 10 minutes of low-intensity continuous exercise (walking, light cycling at < 40% VO2max) maintains the muscle pump while systemic vascular resistance gradually readjusts.
3. Catecholamine and Lactate Clearance: Active recovery accelerates the clearance of circulating catecholamines (epinephrine, norepinephrine) and facilitates hepatic uptake and oxidation of accumulated lactate.
4. Autonomic Transition: Smoothly downregulates sympathetic tone, accelerating parasympathetic vagal reactivation and stabilizing resting heart rate."""
    },
    {
        "doc_id": "P7_13_HEAT_ILLNESS_SPECTRUM",
        "section_title": "EXERTIONAL HEAT ILLNESS: PATHOLOGY OF CRAMPS, EXHAUSTION, AND HEAT STROKE",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_ENVIRONMENTAL_SAFETY",
        "text": """Exercising in hot conditions poses a spectrum of exertional heat illnesses, culminating in exertional heat stroke, a true medical emergency:
1. Exercise-Associated Muscle Cramps (Heat Cramps): Painful, involuntary muscle contractions occurring during or after prolonged exercise in the heat, primarily driven by neuromuscular fatigue combined with extensive sweat and sodium deficits. Managed with rest, passive stretching, and oral sodium/fluid replacement.
2. Heat Exhaustion: Inability to effectively sustain cardiac output due to cardiovascular strain, dehydration, and heavy peripheral vasodilation.
   - Signs and Symptoms: Profuse sweating, pale/clammy skin, dizziness, headache, nausea, tachycardia, orthostatic hypotension. Core body temperature is elevated but remains below 40.5°C (105°F). Mental status remains normal without central nervous system impairment.
3. Exertional Heat Stroke (EHS): A life-threatening hyperthermic emergency defined by two clinical criteria:
   - Core body temperature exceeding 40.5°C (105°F), measured accurately via rectal thermometry.
   - Central Nervous System (CNS) Dysfunction: Confusion, delirium, combative behavior, seizures, ataxia, or coma. Sweating may or may not be present.
4. Emergency Treatment for EHS: 'Cool First, Transport Second'. Immediate whole-body cold-water immersion (ice tub at 1.7°C to 15°C) with continuous vigorous water agitation until core body temperature drops below 39°C (102°F). Rapid immersion drastically reduces morbidity and mortality."""
    },
    {
        "doc_id": "P7_14_WBGT_MONITORING",
        "section_title": "WET-BULB GLOBE TEMPERATURE (WBGT) AND WORKLOAD MODIFICATION",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_ENVIRONMENTAL_SAFETY",
        "text": """Standard ambient air temperature and heat index do not accurately reflect environmental thermal strain during athletic training because they fail to account for radiant heat and air velocity.
The Wet-Bulb Globe Temperature (WBGT) is the gold standard environmental metric utilized by sports organizations and the military:
WBGT Equation:
WBGT = 0.7(Twb) + 0.2(Tg) + 0.1(Tdb)
Where:
- Twb = Wet-Bulb Temperature (measures evaporative cooling capacity).
- Tg = Black Globe Temperature (measures radiant solar heat load).
- Tdb = Dry-Bulb Temperature (standard ambient air temperature).
Operational Activity Categories:
1. Low Risk (WBGT < 25.6°C / 78°F): Normal physical activity; regular fluid intake encouraged.
2. Moderate Risk (WBGT 25.6°C to 27.8°C / 78°F to 82°F): Increased rest-to-work ratios; mandatory water breaks every 20 minutes.
3. High Risk (WBGT 27.9°C to 31.0°C / 82.1°F to 87.9°F): Modify training duration; unacclimatized individuals must reduce physical intensity; gear/armor/heavy padding removed.
4. Extreme Danger (WBGT >= 31.1°C / 88°F): Suspend high-intensity outdoor conditioning drills; shift training to climate-controlled indoor environments or early morning hours."""
    },
    {
        "doc_id": "P7_15_COLD_WEATHER_SAFETY",
        "section_title": "COLD WEATHER EXERCISE SAFETY: HYPOTHERMIA, FROSTBITE, AND CLOTHING SYSTEMS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_ENVIRONMENTAL_SAFETY",
        "text": """Cold weather physical training exposes participants to dual environmental risks: localized tissue freezing (frostbite) and systemic drop in core temperature (hypothermia):
1. Hypothermia Pathophysiology: Occurs when systemic heat loss exceeds heat production, causing core body temperature to fall below 35°C (95°F):
   - Mild (32°C to 35°C): Vigorous shivering, apathy, clumsy speech, peripheral vasoconstriction.
   - Moderate (28°C to 32°C): Shivering ceases, severe confusion, paradoxical undressing, cardiac dysrhythmias.
   - Severe (< 28°C): Unconsciousness, ventricular fibrillation, cardiac arrest.
2. Frostbite: Freezing of skin and underlying tissue, exacerbated by convective wind chill. Most common on exposed peripheral extremities (fingers, toes, nose, ears).
3. The Three-Layer Clothing System:
   - Base Layer: Hydrophobic synthetic fabrics (polyester, polypropylene) or merino wool that wick sweat away from the skin. Avoid cotton ('cotton kills' when wet).
   - Middle (Insulating) Layer: Fleece, wool, or synthetic insulation that traps warm air.
   - Outer (Protective) Layer: Wind- and water-resistant, breathable shell (membrane fabrics) that blocks convective wind chill while permitting vapor escape.
4. Hydration in Cold Weather: Exercise-induced cold diuresis (central blood shift suppressing ADH) combined with respiratory fluid losses via dry cold air causes insidious dehydration."""
    },
    {
        "doc_id": "P7_16_AIR_QUALITY_SAFETY",
        "section_title": "AIR QUALITY INDEX (AQI) AND RESPIRATORY RISKS DURING EXERCISE",
        "source_id": "US-CDC-PA-2022",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_ENVIRONMENTAL_SAFETY",
        "text": """During heavy exercise, minute ventilation increases dramatically from resting levels of 6 to 10 L/min up to 100 to 150 L/min. Additionally, oronasal breathing bypasses the natural filtration and humidification capacity of the nasal mucosa, delivering ambient airborne pollutants deep into alveolar tissue.
The EPA Air Quality Index (AQI) reports levels of primary pollutants (particulate matter PM2.5 and PM10, ground-level ozone, nitrogen dioxide, and carbon monoxide):
1. Moderate (AQI 51 to 100): Acceptable air quality; unusually sensitive individuals should consider reducing prolonged or heavy outdoor exertion.
2. Unhealthy for Sensitive Groups (AQI 101 to 150): People with asthma, chronic obstructive pulmonary disease (COPD), or cardiovascular disease should reduce prolonged outdoor exertion.
3. Unhealthy (AQI 151 to 200): Everyone may begin to experience adverse respiratory effects; outdoor workouts should be relocated indoors or substituted with low-intensity sessions.
4. Very Unhealthy and Hazardous (AQI > 200): All outdoor physical activity should be avoided. Exercise indoors in spaces with high-efficiency particulate air (HEPA) filtration systems."""
    },
    {
        "doc_id": "P7_17_LEGAL_MEDICAL_BOUNDARIES",
        "section_title": "SCOPE OF PRACTICE BOUNDARIES: GENERAL FITNESS EDUCATION VS CLINICAL ADVICE",
        "source_id": "US-HHS-PAG-2018",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_SCOPE_ETHICS",
        "text": """Clear, legally defensible, and ethically rigorous boundaries distinguish general fitness education from individualized clinical medical advice:
1. General Fitness Education:
   - Provides evidence-based information regarding human biomechanics, exercise programming, physiological training adaptations, and public health physical activity guidelines.
   - Explains standard principles of progressive overload, nutritional balance, recovery sleep hygiene, and general equipment safety.
   - Empowers individuals to understand exercise science concepts and apply generalized best practices.
2. Individualized Clinical Medical Advice:
   - Diagnosing specific pathological conditions, structural musculoskeletal injuries, metabolic disorders, or nutritional deficiencies.
   - Prescribing clinical exercise therapy for medical conditions without physician oversight.
   - Prescribing restrictive therapeutic meal plans, medical nutrition therapy, or pharmaceutical dosing.
3. Obligatory Disclaimer and Safety Boundaries: Educational materials and algorithmic fitness systems must explicitly state that fitness content is for educational and informational purposes only and is not a substitute for professional medical examination, diagnosis, or clinical prescription. Individuals with symptoms or chronic conditions must consult qualified medical professionals."""
    },
    {
        "doc_id": "P7_18_FALL_PREVENTION_OLDER_ADULTS",
        "section_title": "FALL PREVENTION IN OLDER ADULTS: THE CDC STEADI ALGORITHM AND BALANCE DRILLS",
        "source_id": "US-CDC-INJURY-PREV",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_FALL_PREVENTION",
        "text": """Falls are the leading cause of fatal and nonfatal injuries among adults aged 65 and older. The CDC STEADI (Stopping Elderly Accidents, Deaths, and Injuries) initiative provides an evidence-based clinical and community framework for fall prevention:
1. Risk Assessment Core: Screening includes three key questions:
   - Have you fallen in the past year?
   - Do you feel unsteady when standing or walking?
   - Do you worry about falling?
2. Objective Functional Mobility Assessments:
   - Timed Up and Go (TUG): Measures the time taken to rise from an armchair, walk 3 meters, turn, return, and sit. A time >= 12 seconds indicates elevated fall risk.
   - 30-Second Chair Stand Test: Counts the number of full unassisted stands in 30 seconds, assessing lower body strength and power.
   - 4-Stage Balance Test: Progressively assesses balance in four standing foot positions (side-by-side, semi-tandem, full tandem, and single-leg stand).
3. Exercise Interventions: Community and home-based multicomponent programs (incorporating progressive balance, gait training, and lower-extremity resistance training, such as Tai Chi or structured physical therapy) reduce fall rates by up to 24% to 30%."""
    },
    {
        "doc_id": "P7_19_SARCOPENIA_DYNAPENIA",
        "section_title": "SARCOPENIA AND DYNAPENIA: PATHOPHYSIOLOGY AND RESISTANCE TRAINING COUNTERMEASURES",
        "source_id": "US-NIH-NIA-EXERCISE",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_AGING_MUSCLE",
        "text": """Aging is associated with progressive, involuntary declines in muscular structure and function, categorized into two distinct clinical entities:
1. Sarcopenia: Age-related loss of skeletal muscle mass and muscular quality. Starting around the fifth decade of life, muscle mass declines by approximately 0.5% to 1.0% per year, primarily through selective atrophy and denervation-induced apoptosis of high-threshold Type II fast-twitch muscle fibers.
2. Dynapenia: Age-related loss of muscle strength and power that outpaces the loss of muscle mass. Dynapenia is driven predominantly by neurological mechanisms:
   - Decreased alpha-motoneuron count and axonal sprouting.
   - Reduced motor unit discharge rate and recruitment threshold elevation.
   - Infiltration of intermuscular adipose tissue and fibrous collagen, degrading muscle contractile quality.
3. Resistance Training as Primary Therapy: High-intensity progressive resistance training (70% to 80% 1RM) remains the single most effective intervention to reverse sarcopenia and dynapenia. Resistance training stimulates satellite cell proliferation, increases myofibrillar protein synthesis, restores motor unit recruitment pathways, and improves daily functional living tasks (stair climbing, chair rising)."""
    },
    {
        "doc_id": "P7_20_EQUIPMENT_MAINTENANCE_SAFETY",
        "section_title": "FACILITY AND EQUIPMENT SAFETY: INSPECTION PROTOCOLS AND HAZARD MITIGATION",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_FACILITY_SAFETY",
        "text": """Maintaining a safe training environment requires systematic inspection of fitness equipment and adherence to operational safety protocols:
1. Cable and Pulley Systems: Weight machine cables must be inspected weekly for fraying, cracked nylon coating, kinked steel strands, or loose terminal bolts. A compromised cable under tension can snap catastrophically, propelling the weight stack or handle into the exerciser.
2. Barbell and Collar Integrity:
   - Barbell Sleeves: Inspect sleeve rotation; sticky or seized bushings/bearings alter rotational inertia, generating unexpected wrist and shoulder torque during cleans or snatches.
   - Barbell Straightness: Roll unweighted bars on a flat surface to detect bending or warping.
   - Mandatory Collars: Spring collars or locking jaw collars must be placed on every barbell loading sleeve to prevent asymmetrical plate sliding during lifts.
3. Bench and Rack Pin Engagement: Verify that safety spotter arms, J-cups, and pop-pins on adjustable benches are fully engaged in their respective adjustment holes before bearing weight.
4. Floor Hygiene and Spacing: Keep lifting platforms, walkways, and dumbbell areas completely free of loose plates, resistance bands, and chalk spills to eliminate tripping hazards."""
    },
    {
        "doc_id": "P7_21_EMERGENCY_ACTION_PLANS",
        "section_title": "EMERGENCY ACTION PLANS (EAP) AND FACILITY LIFE-SAVING PROTOCOLS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_FACILITY_SAFETY",
        "text": """Every fitness facility, athletic organization, and training venue must maintain a venue-specific Emergency Action Plan (EAP) to respond effectively to catastrophic medical events:
1. Automated External Defibrillator (AED) Readiness:
   - Location and Access: The AED must be mounted in a clearly designated, unlocked, and unobstructed location within a 3-minute retrieve-and-apply response time from anywhere in the facility.
   - Maintenance: Monthly battery checks, pad expiration date tracking, and operational status indicator verification.
2. Chain of Command and Roles: Clearly defined staff responsibilities:
   - First Responder: Provides immediate CPR / chest compressions (100 to 120 compressions per minute at 5 to 6 cm depth) and applies the AED.
   - Second Responder: Activates Emergency Medical Services (EMS) via telephone, providing specific facility address, entry door number, and nature of the emergency.
   - Third Responder: Meets the ambulance at the facility entrance or perimeter gate to guide paramedics directly to the victim.
3. Rehearsal Schedule: The EAP must be reviewed and physically rehearsed with all coaches, trainers, and staff at least once every 12 months."""
    },
    {
        "doc_id": "P7_22_OVERTRAINING_PREVENTION_EDUCATION",
        "section_title": "FITNESS EDUCATION: BALANCING AMBITION WITH PHYSIOLOGICAL ADAPTATION",
        "source_id": "US-HHS-PAG-2018",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_SCOPE_ETHICS",
        "text": """A central tenet of foundational fitness education is debunking the pervasive cultural dogma that 'more is always better' or that severe fatigue is a prerequisite for progress.
1. The Homeostatic Reality: Skeletal muscle and connective tissue adaptations are not forged during workouts; workouts merely deliver a targeted mechanical and biochemical stimulus. The actual structural remodeling occurs exclusively during recovery windows when adequate nutrition and restorative sleep are supplied.
2. The Diminishing Returns Law: As weekly training volume expands, the incremental hypertrophic or strength benefit per set progressively flattens, while the systemic fatigue curve steepens exponentially.
3. Autoregulation Education: Lifters must be educated to recognize subjective fatigue signals (persistent joint achiness, disrupted sleep patterns, declining appetite, unprovoked irritability, or loss of lifting velocity) as biological directives to adjust volume or insert a planned deload rather than trying to 'push through'.
4. Long-Term Adherence: Sustainable, injury-free physical progression over years yields vastly superior health and performance outcomes compared to cycles of acute extreme training followed by burnout or injury."""
    }
]
