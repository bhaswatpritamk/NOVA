"""Pillars Part 5: Capstone Corpus Expansion Across All 7 Nova-Fit Pillars.

Authoritative educational documents drawn from public domain and open-access sources:
- OpenStax Anatomy and Physiology 2e (CC BY 4.0, Betts et al.)
- U.S. Department of Health and Human Services (Physical Activity Guidelines, Public Domain)
- Centers for Disease Control and Prevention (CDC Guidelines, Public Domain)
- Headquarters, Department of the Army (FM 7-22 and ATP 7-22.02, Public Domain)
- National Institutes of Health / NHLBI / NIA / ODS (Public Domain)
- NASA Human Research Program Evidence Book (Public Domain)
"""

DOCUMENTS = [
    # -------------------------------------------------------------------------
    # Pillar 1: Exercise Science, Physiology, and Biomechanics
    # -------------------------------------------------------------------------
    {
        "doc_id": "P1_51_HILLS_FORCE_VELOCITY_EQUATION",
        "section_title": "HILL'S HYPERBOLIC FORCE-VELOCITY EQUATION AND MECHANICAL POWER LIMITS",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_SARCOMERE",
        "text": """Archibald V. Hill's fundamental thermodynamic experiments established the inverse hyperbolic relationship between concentric muscle force and shortening velocity:
1. Mathematical Formulation:
   (F + a)(v + b) = (F0 + a)b
   Where:
   - F = Concentric contractile force.
   - v = Shortening velocity.
   - F0 = Maximal isometric force (at zero shortening velocity).
   - a and b = Thermodynamic empirical constants of energy dissipation.
2. Cross-Bridge Mechanics:
   - At high shortening velocities, cross-bridges must attach, execute power strokes, and detach at rapid cycling rates. The finite rate constant of detachment (g) means some cross-bridges exert negative drag, reducing net concentric force.
   - At slow shortening velocities or isometric conditions, maximum cross-bridges remain simultaneously bound in the force-generating state.
3. Power Output Curve:
   - Mechanical Power (P) = Force (F) x Velocity (v).
   - Because force decreases hyperbolically as velocity increases, peak mechanical power output occurs at an intermediate force and velocity (approximately 30% to 35% of F0 and 30% of maximal shortening velocity v_max)."""
    },
    {
        "doc_id": "P1_52_PENNATION_GEAR_RATIO",
        "section_title": "VARIABLE PENNATION GEAR RATIOS DURING RAPID CONTRACTION DYNAMICS",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_MOTOR_UNITS",
        "text": """Pennate skeletal muscles possess an architectural dynamic termed the 'variable gear ratio' (architectural gear ratio / AGR):
1. Planar vs Architectural Rotation:
   - The architectural gear ratio is defined as:
     AGR = Velocity of Whole Muscle Shortening / Velocity of Individual Muscle Fiber Shortening.
   - During low-load, high-velocity contractions, muscle fibers rotate actively to greater pennation angles (belly bulges and thickens), allowing the entire muscle tendon unit to shorten significantly faster than the individual fibers shorten along their own axes (AGR > 1.0).
2. High-Load Gear Shifting:
   - Under heavy mechanical loads or high resisting forces, the increased intramuscular fluid pressure resists muscle bulging and limits fiber rotation.
   - Fiber rotation is constrained; AGR shifts toward 1.0, transmitting maximum linear tensile force directly to the central aponeurosis.
3. Functional Significance: This variable biological gearing enables pennate muscles to automatically optimize mechanical output for either rapid movement velocity or maximal force production depending on external mechanical demands."""
    },
    {
        "doc_id": "P1_53_TENSION_TIME_INTEGRAL",
        "section_title": "TENSION-TIME INTEGRAL AND METABOLIC EFFICIENCY IN MUSCULAR WORK",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_LEVERS_MOMENTS",
        "text": """The biological energetic cost of resistance training is fundamentally governed by the Tension-Time Integral (TTI):
1. Mathematical Expression:
   TTI = Integral of Muscle Force (F) over Time of Contraction (dt).
   - TTI quantifies the cumulative mechanical exposure of the sarcomere and surrounding connective tissues across a repetition or set.
2. Cross-Bridge Cycling and ATP Expenditure:
   - Hydrolysis of one ATP molecule occurs with each complete cross-bridge power stroke and detachment cycle.
   - In isometric contractions, zero external mechanical work is performed (Work = Force x Displacement = 0); however, significant metabolic energy is consumed to sustain active cross-bridge cycling and run sarcoplasmic reticulum SERCA calcium reuptake pumps.
3. Hypertrophic Signaling:
   - High mechanical tension applied over sufficient time under tension (elevated TTI) is the master driver of focal adhesion kinase and costameric mechanosensitive cascades that stimulate mTORC1."""
    },

    # -------------------------------------------------------------------------
    # Pillar 2: Strength Training Principles and Programming
    # -------------------------------------------------------------------------
    {
        "doc_id": "P2_46_WAVE_LOADING_POTENTIATION",
        "section_title": "WAVE LOADING MESOCYCLES: SYSTEMATIC MOTOR UNIT POTENTIATION",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_SET_CONFIGURATIONS",
        "text": """Wave loading exploits Post-Activation Performance Enhancement (PAPE) within a single workout session by cycling through descending-repetition 'waves' of increasing intensity:
1. Wave Structure (Example: 3/2/1 Protocol):
   - Wave 1 (Potentiation Wave):
     * Set 1: 3 reps @ 82.5% 1RM (3 min rest)
     * Set 2: 2 reps @ 85.0% 1RM (3 min rest)
     * Set 3: 1 rep @ 87.5% 1RM (3 to 4 min rest)
   - Wave 2 (Realization Wave):
     * Set 4: 3 reps @ 85.0% 1RM (exceeds Wave 1 Set 1 load)
     * Set 5: 2 reps @ 87.5% 1RM
     * Set 6: 1 rep @ 90.0% to 92.5% 1RM
2. Neurological Mechanism:
   - The heavy single at the culmination of Wave 1 maximally excites spinal motoneurons and phosphorylates myosin regulatory light chains.
   - When the lifter drops back to 3 repetitions to begin Wave 2, the CNS perceives the weight as significantly lighter, allowing the lifter to handle heavier loads with greater bar velocity than possible during straight sets."""
    },
    {
        "doc_id": "P2_47_DROP_SETS_METABOLIC_FATIGUE",
        "section_title": "INTENSIFICATION TECHNIQUES: DROP SETS, REST-PAUSE, AND MOTOR UNIT EXHAUSTION",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_SET_CONFIGURATIONS",
        "text": """Intensification techniques extend working sets beyond the normal point of concentric muscular failure:
1. Drop Sets (Descending Sets):
   - Execution: A set is performed to muscular failure (e.g., 8 reps at 75% 1RM). The load is immediately reduced by 20% to 25% without rest, and repetitions continue to failure. A second drop may follow.
   - Physiology: Lowering the load allows fatigued high-threshold motor units to continue contracting while recruiting remaining intermediate motor units under conditions of severe metabolic acidosis and cellular swelling.
2. Rest-Pause Training (Doggcrapp Methodology):
   - Execution: A set to failure (e.g., 8 to 10 reps), followed by 15 seconds of rest (10 to 12 deep breaths), followed by continuing repetitions to failure (typically 3 to 4 reps), followed by another 15 seconds of rest and a final effort (1 to 2 reps).
   - Time Efficiency: Condenses 3 distinct near-failure stimulation thresholds into roughly 60 seconds of total work.
3. Fatigue Caution: These techniques impose extreme neuromuscular and muscle damage stress and should be used sparingly (on the final set of an exercise) to prevent non-functional overreaching."""
    },
    {
        "doc_id": "P2_48_CAT_ACCELERATION_TRAINING",
        "section_title": "COMPENSATORY ACCELERATION TRAINING (CAT): MAXIMIZING FORCE AT ALL LOADS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_OVERLOAD",
        "text": """Developed by Fred Hatfield, Compensatory Acceleration Training (CAT) is a lifting philosophy requiring the athlete to deliberately accelerate the barbell with maximal voluntary effort throughout the entire concentric range of motion:
1. The Physics of CAT (Newton's Second Law: F = m x a):
   - When lifting a submaximal load (e.g., 70% 1RM), an athlete can choose to lift casually at constant velocity, exerting only enough force to match the weight of the bar (F = m x g).
   - Alternatively, under CAT, the lifter intentionally accelerates the barbell with maximal explosive intent (a > 0), maximizing total applied force (F = m(g + a)).
2. Neuromuscular Recruitment:
   - Deliberate maximal acceleration forces the nervous system to recruit high-threshold Type II motor units from the very onset of the repetition, regardless of the lighter external load.
   - Eliminates the natural deceleration that occurs during submaximal lifts as mechanical advantage improves near lockout, training rate of force development throughout the entire movement path."""
    },

    # -------------------------------------------------------------------------
    # Pillar 3: Exercise Technique and Safe Equipment Use
    # -------------------------------------------------------------------------
    {
        "doc_id": "P3_46_BOX_SQUAT_BIOMECHANICS",
        "section_title": "THE BOX SQUAT: ELIMINATING ECCENTRIC REBOUND AND ENSURING DEPTH",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "exercise_technique_safety",
        "group_id": "GRP_P3_SQUAT",
        "text": """The box squat uses a sturdy, height-calibrated box to break the kinetic chain and enforce consistent depth:
1. Technical Execution:
   - Descent: The lifter sits backward horizontally toward the box, maintaining vertical shins and wide knee push, keeping the lumbar spine locked in rigid lordosis.
   - Transition: Upon contacting the box, the lifter pauses for 1 to 2 seconds, maintaining full torso bracing and intra-abdominal pressure. The lifter releases hip flexor tension while keeping spinal erectors and abdominal wall rigid ('relaxed hips, tight core').
   - Ascent: The lifter explodes upward off the box without rocking or forward momentum.
2. Biomechanical Utilities:
   - Stretch-Shortening Cycle Decoupling: Eliminates elastic tendon rebound, forcing pure static-to-dynamic concentric force production.
   - Knee Shear Elimination: Perpendicular shins minimize patellofemoral compressive force, making box squats ideal for lifters recovering from patellar tendinopathy.
   - Depth Calibration: Enforces a standardized, objective depth threshold on every single repetition."""
    },
    {
        "doc_id": "P3_47_OVERHEAD_PRESS_LOCKOUT",
        "section_title": "BARBELL OVERHEAD PRESS: THE BAR CLEARANCE PATH AND ACTIVE SHOULDER ELEVATION",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "exercise_technique_safety",
        "group_id": "GRP_P3_PRESS",
        "text": """The strict standing overhead barbell press demands precise sagittal plane bar trajectory and core stabilization:
1. The Starting Rack Position:
   - Barbell rests on the anterior deltoids and clavicles; forearms strictly vertical beneath the bar with wrists straight; feet shoulder-width apart; gluteals and quadriceps contracted isometrically to create a rigid pelvic base.
2. The Head Clearance Path:
   - To allow the bar to ascend in a straight vertical line over the midfoot without striking the chin, the lifter tilts the head slightly backward at the cervical spine.
   - As soon as the bar passes the forehead, the lifter pushes the head and upper torso forward through the 'window' created by the arms, returning the head to neutral.
3. The Active Overhead Lockout:
   - At terminal lockout, the bar is stacked vertically directly over the glenohumeral joints, cervical spine, and midfoot.
   - Active Shrug: The lifter must actively elevate the scapulae ('shrug up' toward the ears) using the upper trapezius and serratus anterior. Active upward scapular rotation clears the subacromial space, preventing impingement of the supraspinatus tendon."""
    },
    {
        "doc_id": "P3_48_CABLE_CROSSOVER_RESISTANCE",
        "section_title": "CABLE RESISTANCE PROFILES: CONSTANT TENSION AND CONTINUOUS ADDUCTION TORQUE",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "exercise_technique_safety",
        "group_id": "GRP_P3_EQUIPMENT_SAFETY",
        "text": """Understanding the difference between free weight gravity-based resistance and cable pulley mechanics:
1. The Dumbbell Fly Flaw:
   - In a supine dumbbell chest fly, gravity acts strictly downward in a vertical line of action.
   - At the bottom of the movement (arms abducted horizontally), the external moment arm relative to the glenohumeral joint is maximal, creating extreme mechanical stretch on the pectoralis major.
   - However, at the top contracted position (arms perpendicular to the floor), the line of gravity passes directly through the shoulder joint center; the external moment arm is zero, completely unloading the pectoralis major at peak adduction.
2. The Cable Pulley Advantage:
   - Cables exert tension along the exact line of the cable vector, independent of gravity.
   - By angling the cable pulleys, the lifter maintains a high external moment arm and intense mechanical resistance across the entire range of motion, providing peak tension precisely at terminal horizontal adduction where the pectoralis major is fully shortened."""
    },

    # -------------------------------------------------------------------------
    # Pillar 4: Nutrition Fundamentals and Hydration
    # -------------------------------------------------------------------------
    {
        "doc_id": "P4_47_EAA_REQUIREMENTS_NINE",
        "section_title": "ESSENTIAL AMINO ACID REQUIREMENTS: THE NINE INDISPENSABLE SUBSTRATES",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_PROTEIN_MPS",
        "text": """Of the 20 proteogenic amino acids, nine cannot be synthesized de novo by human cellular metabolism and are classified as Essential Amino Acids (EAAs):
1. The Nine EAAs and Daily Basal Requirements (mg/kg/day):
   - Leucine: 39 to 55 mg/kg (primary anabolic trigger).
   - Isoleucine: 20 mg/kg (branched-chain; glucose uptake).
   - Valine: 26 mg/kg (branched-chain; muscle metabolism).
   - Lysine: 30 mg/kg (connective tissue collagen synthesis and carnitine production).
   - Methionine: 15 mg/kg (sulfur-containing; initiator of translation, precursor to cysteine).
   - Phenylalanine: 25 mg/kg (aromatic; precursor to tyrosine, dopamine, epinephrine).
   - Threonine: 15 mg/kg (mucin synthesis and intestinal barrier maintenance).
   - Tryptophan: 4 mg/kg (precursor to serotonin and melatonin).
   - Histidine: 10 mg/kg (precursor to histamine and carnosine).
2. The Inefficacy of Isolated BCAAs:
   - Ingesting branched-chain amino acids (leucine, isoleucine, valine) in isolation triggers mTORC1 via leucine; however, because muscle protein synthesis requires all 20 amino acids to build new myofibrils, the absence of the other six EAAs halts protein translation.
   - Muscle tissue is forced to catabolize its own proteins to supply the missing EAAs, resulting in zero net anabolic gain."""
    },
    {
        "doc_id": "P4_48_FAT_SOLUBLE_VITAMINS",
        "section_title": "FAT-SOLUBLE VITAMINS (A, D, E, K): ABSORPTION, ADIPOSE STORAGE, AND TOXICITY",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_MICRONUTRIENTS",
        "text": """Vitamins A, D, E, and K are non-polar hydrophobic micronutrients requiring dietary lipid co-ingestion for physiological absorption:
1. Digestive Absorption Kinetics:
   - In the small intestine, fat-soluble vitamins partition into mixed lipid micelles alongside monoglycerides and fatty acids, facilitated by bile salts.
   - Enterocytes package them into chylomicrons for exocytosis into mesenteric lacteals and lymphatic circulation, bypassing direct hepatic portal transport.
   - Consuming a very-low-fat diet (< 15% of total energy) severely impairs fat-soluble vitamin absorption, leading to subclinical deficiencies.
2. Functional Roles in Athletic Physiology:
   - Vitamin A (Retinoids): Vision, epithelial cellular differentiation, and immune defense.
   - Vitamin D (Calcitriol): Calcium homeostasis, bone mineral density, and skeletal muscle contractility.
   - Vitamin E (Alpha-tocopherol): Lipophilic antioxidant protecting polyunsaturated fatty acids in the sarcolemma against exercise-induced lipid peroxidation.
   - Vitamin K (Phylloquinone / Menaquinone): Essential cofactor for gamma-glutamyl carboxylase, activating osteocalcin for bone mineralization and clotting factors.
3. Storage and Toxicity Risks: Unlike water-soluble vitamins (B and C) which are excreted renally, excess fat-soluble vitamins are sequestered in hepatocytes and adipose depots, posing potential hypervitaminosis toxicity risks with mega-dose supplementation (especially Vitamin A and D)."""
    },
    {
        "doc_id": "P4_49_POTASSIUM_MEMBRANE_POTENTIAL",
        "section_title": "POTASSIUM ELECTROLYTE PHYSIOLOGY: RESTING MEMBRANE POTENTIAL AND CARDIAC RHYTHM",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_HYDRATION",
        "text": """Potassium (K+) is the predominant intracellular cation (intracellular concentration ~140 to 150 mmol/L vs extracellular concentration 3.5 to 5.0 mmol/L):
1. Establishment of the Resting Membrane Potential (RMP):
   - The trans-sarcolemmal potassium concentration gradient, established by Na+/K+ ATPase pumps and maintained by background potassium leak channels (K_ir), dictates the resting membrane potential:
     RMP is calculated via the Goldman-Hodgkin-Katz equation (typically -70 to -90 mV in skeletal and cardiac myocytes).
2. Exercise-Induced Potassium Shifts:
   - Repetitive muscular contractions release intracellular K+ into the interstitial space and plasma. Plasma potassium rises during maximal exertion up to 6.0 mmol/L, acting as a local vasodilator to increase muscle blood flow.
   - Rapid post-exercise clearance back into myocytes is mediated by beta-2 adrenergic stimulation and insulin.
3. Imbalance Pathophysiology:
   - Hypokalemia (< 3.5 mmol/L): Hyperpolarizes membrane potentials, causing muscle weakness, hyporeflexia, and dangerous cardiac arrhythmias (ventricular ectopy, flattened T-waves).
   - Dietary Target: Adults require 2,600 to 3,400 mg/day, obtained primarily from fruits, vegetables, legumes, and dairy."""
    },

    # -------------------------------------------------------------------------
    # Pillar 5: Sleep, Recovery, and Physical Activity
    # -------------------------------------------------------------------------
    {
        "doc_id": "P5_36_CHRONOTYPE_GENETICS_PER3",
        "section_title": "CHRONOTYPE GENETICS: PER3 POLYMORPHISMS AND ATHLETIC PERFORMANCE TIMING",
        "source_id": "US-CDC-SLEEP-2022",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_CIRCADIAN",
        "text": """Individual variations in natural sleep-wake timing (chronotype) are genetically grounded and profoundly influence diurnal athletic performance peaks:
1. Genetic Foundations (PER3 Polymorphisms):
   - The Period Circadian Regulator 3 (PER3) gene contains a variable-number tandem repeat (VNTR) polymorphism:
     * PER3(5/5) Homozygotes: Strongly predisposed to morning chronotypes ('larks'). They exhibit earlier morning cortisol awakening responses, earlier core temperature peaks, and perform maximally in early morning competitions.
     * PER3(4/4) Individuals: Strongly predisposed to evening chronotypes ('owls'). They exhibit delayed melatonin release, later core temperature acrophases, and peak athletic performance late in the afternoon or evening.
2. Diurnal Neuromuscular Fluctuation:
   - Regardless of chronotype, peak anaerobic power, maximal isometric force, and joint flexibility naturally peak in the late afternoon (16:00 to 19:00), coinciding with the diurnal peak in core body temperature (elevated temperature increases nerve conduction velocity and cellular enzymatic activity).
   - Evening chronotypes scheduled for early morning competitions experience significant performance deficits, requiring pre-warming strategies and light therapy to advance their circadian phase."""
    },
    {
        "doc_id": "P5_37_OBSTRUCTIVE_SLEEP_APNEA",
        "section_title": "OBSTRUCTIVE SLEEP APNEA (OSA) IN ATHLETES: HYPOXEMIA AND SURGICAL/CPAP PROTOCOLS",
        "source_id": "US-NIH-NHLBI-SLEEP",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_SLEEP_ARCH",
        "text": """Obstructive Sleep Apnea (OSA) is an underdiagnosed sleep pathology prevalent not only in sedentary individuals, but also in heavy strength, power, and contact athletes:
1. Pathophysiological Mechanisms:
   - Recurrent nocturnal collapse or obstruction of the pharyngeal airway during sleep, resulting in partial (hypopneas) or complete (apneas) cessation of airflow lasting >= 10 seconds.
   - Apnea-Hypopnea Index (AHI): Quantifies the number of events per hour of sleep (mild: 5-14; moderate: 15-29; severe: >= 30).
   - Intermittent Nocturnal Hypoxemia: Blood oxygen saturation (SpO2) repeatedly plummets (often < 80%), triggering intense sympathetic nervous system surges, nighttime hypertension, and cortical micro-arousals that fragment Stage 3 slow-wave sleep.
2. Athletic Risk Factors:
   - Large neck circumference (> 17 inches / 43 cm in males), high body mass index, and hypertrophy of soft palate and tongue tissues.
3. Systemic Consequences:
   - Severe daytime hypersomnolence, blunted pulsatile growth hormone secretion, elevated resting cortisol, suppressed testosterone, elevated cardiovascular disease risk, and impaired athletic recovery.
4. Gold Standard Therapy: Continuous Positive Airway Pressure (CPAP) therapy mechanically splints the airway open with pressurized air, eliminating apneas and restoring normal deep sleep architecture."""
    },

    # -------------------------------------------------------------------------
    # Pillar 6: Training Adaptations, Fatigue, and Load Management
    # -------------------------------------------------------------------------
    {
        "doc_id": "P6_35_FOSTER_MONOTONY_STRAIN",
        "section_title": "FOSTER'S MONOTONY AND TRAINING STRAIN: PREDICTING MALADAPTATION",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "training_adaptations_fatigue_load",
        "group_id": "GRP_P6_LOAD_MONITORING",
        "text": """Carl Foster developed mathematical indices derived from daily session-RPE load to identify high-risk training structures that induce non-functional overreaching and illness:
1. Training Monotony:
   - Measures the lack of daily variation in training load across a 7-day microcycle:
     Monotony = Mean Daily Training Load / Standard Deviation of Daily Training Load.
   - High Monotony (> 2.0): Occurs when every day consists of roughly the same hard training load without designated light recovery days. High monotony combined with high absolute volume is the single strongest statistical predictor of upper respiratory illness and overreaching in athletes.
2. Training Strain:
   - Quantifies the cumulative biological stress experienced by the organism:
     Strain = Total Weekly Training Load x Monotony.
3. Programming Solution:
   - Insert deliberate low-load recovery days (e.g., alternating between 800 AU hard days and 200 AU active recovery days). This increases the standard deviation of daily loads, keeping Monotony safely below 1.5 and preventing excessive Strain."""
    },
    {
        "doc_id": "P6_36_ULTRASTRUCTURAL_ZDISC_DAMAGE",
        "section_title": "ULTRASTRUCTURAL MYOFIBRILLAR DAMAGE: Z-DISC STREAMING AND DESMIN DEGRADATION",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "training_adaptations_fatigue_load",
        "group_id": "GRP_P6_FATIGUE_MECHANISMS",
        "text": """High-intensity eccentric resistance training inflicts microscopic structural disruption across the sarcomeric ultrastructure, observable via transmission electron microscopy:
1. Z-Disc Streaming:
   - The Z-disc is the dense proteinaceous anchoring plate (composed primarily of alpha-actinin) that delineates individual sarcomeric boundaries and anchors thin actin filaments.
   - Severe eccentric strain pulls sarcomeres beyond their optimal filament overlap. Unequal mechanical stress causes the Z-discs to smear, broaden, and disrupt—a phenomenon termed 'Z-disc streaming'.
2. Desmin and Intermediate Filament Lysis:
   - Desmin is an essential intermediate filament protein that forms an intracellular lattice linking adjacent myofibrils laterally to each other and anchoring them to the costameres at the sarcolemma.
   - Unaccustomed eccentric contractions activate intracellular calcium-activated neutral proteases (calpains), which selectively degrade desmin. Loss of desmin disrupts lateral force transmission, leading to an immediate 20% to 50% drop in maximal voluntary force production.
3. Autophagy and Remodeling: Damaged myofibrillar proteins are ubiquitinated and cleared via the 26S proteasome and autophagosomes, followed by the synthesis and insertion of fresh alpha-actinin and desmin within 5 to 7 days."""
    },

    # -------------------------------------------------------------------------
    # Pillar 7: General Fitness Education and Age-Appropriate Safety
    # -------------------------------------------------------------------------
    {
        "doc_id": "P7_33_ACSM_SCREENING_ALGORITHM",
        "section_title": "THE ACSM PRE-PARTICIPATION SCREENING ALGORITHM: EVIDENCE-BASED LOGIC TREE",
        "source_id": "US-CDC-PA-2022",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_SCREENING_RISK",
        "text": """The American College of Sports Medicine (ACSM) updated its pre-participation screening algorithm to remove unnecessary medical clearance barriers while accurately identifying high-risk individuals:
1. The 3-Step Decision Logic:
   - Step 1: Identify current physical activity habits:
     * Does the individual participate in regular exercise (at least 30 minutes of moderate-intensity physical activity on 3 or more days per week for at least the past 3 months)?
   - Step 2: Identify known cardiovascular (CV), metabolic, or renal disease (e.g., prior myocardial infarction, coronary revascularization, type 1 or 2 diabetes, chronic kidney disease).
   - Step 3: Identify signs or symptoms suggestive of underlying CV, metabolic, or renal disease (angina, dyspnea at rest or with mild exertion, dizziness or syncope, orthopnea, ankle edema, palpitations, intermittent claudication, known heart murmur, unusual fatigue).
2. Actionable Stratification:
   - Non-Exerciser, No Disease, No Symptoms: Medical clearance not necessary; can initiate light to moderate exercise and progress.
   - Non-Exerciser, Known Disease, Asymptomatic: Medical clearance recommended prior to initiating exercise.
   - Any Individual with Signs/Symptoms: Medical clearance mandatory regardless of current physical activity status."""
    },
    {
        "doc_id": "P7_34_AED_OPERATION_PROTOCOLS",
        "section_title": "AUTOMATED EXTERNAL DEFIBRILLATOR (AED) PROTOCOLS: BIPHASIC WAVEFORMS AND TIMING",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_FACILITY_SAFETY",
        "text": """Sudden Cardiac Arrest (SCA) during exercise is most commonly caused by ventricular fibrillation (VF) or pulseless ventricular tachycardia (VT):
1. The Survival Window:
   - For every minute that defibrillation is delayed during VF cardiac arrest, the probability of survival decreases by 7% to 10%.
   - Applying an AED within 3 to 5 minutes of collapse yields survival rates exceeding 50% to 70%.
2. Step-by-Step AED Operational Execution:
   - Step 1: Power ON the AED immediately.
   - Step 2: Bare the victim's chest; dry any sweat or moisture with a towel.
   - Step 3: Apply the self-adhesive electrode pads in the standard anterolateral position:
     * Pad 1: Right upper chest, immediately below the clavicle.
     * Pad 2: Left lower chest, along the mid-axillary line below the pectoral muscle.
   - Step 4: Stand CLEAR while the AED analyzes the cardiac rhythm (ensuring no one touches the victim to avoid artifact interference).
   - Step 5: If a shock is advised, announce 'STAND CLEAR' loudly, verify visual clearance, and press the Shock button.
   - Step 6: Immediately resume high-quality CPR (30 compressions to 2 ventilations at 100-120 compressions/min) starting with chest compressions without pausing to check for a pulse."""
    },
    {
        "doc_id": "P7_35_WIND_CHILL_HYPOTHERMIA",
        "section_title": "WIND CHILL INDEX: CONVECTIVE HEAT DISSIPATION AND FROSTBITE THRESHOLDS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_ENVIRONMENTAL_SAFETY",
        "text": """Exercising in cold environments exposes the human body to convective heat loss that accelerates as air velocity increases:
1. The Physics of the Wind Chill Index (WCI):
   - The body maintains a thin, microscopic boundary layer of warmed, humidified air immediately adjacent to the skin.
   - Wind sweeps this insulating boundary layer away, continuously exposing skin to cold ambient air and accelerating convective heat loss.
   - The National Weather Service Wind Chill Temperature formula calculates the equivalent temperature felt on exposed skin based on ambient temperature and wind speed.
2. Clinical Frostbite Risk Thresholds:
   - Wind Chill > -15°F (-26°C): Low risk of frostbite for healthy, properly clothed individuals.
   - Wind Chill -18°F to -35°F (-28°C to -37°C): Frostbite can occur on exposed skin within 30 minutes.
   - Wind Chill < -35°F (-37°C): Frostbite can occur on exposed skin within 10 to 15 minutes.
3. Cold Exercise Management:
   - When the wind chill drops below -18°F (-28°C), outdoor training should be curtailed or relocated indoors. If training outdoors, all skin must be covered with wind-impermeable fabrics, neoprene face masks, and thermal mittens."""
    }
]
