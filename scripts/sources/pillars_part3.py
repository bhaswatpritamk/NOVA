"""Pillars Part 3: Advanced Topics Across All 7 Nova-Fit Pillars.

Authoritative educational documents drawn from public domain and open-access sources:
- U.S. Department of Health and Human Services (Physical Activity Guidelines, Public Domain)
- Centers for Disease Control and Prevention (CDC Exercise and Health Basics, Public Domain)
- Headquarters, Department of the Army (FM 7-22 and ATP 7-22.02, Public Domain)
- National Institutes of Health / NHLBI / NIA (Public Domain)
- OpenStax Anatomy and Physiology 2e (CC BY 4.0, Betts et al.)
- NASA Human Research Program Evidence Book (Public Domain)
"""

DOCUMENTS = [
    # -------------------------------------------------------------------------
    # Pillar 1: Exercise Science, Physiology, and Biomechanics
    # -------------------------------------------------------------------------
    {
        "doc_id": "P1_41_GTO_AUTOGENIC_INHIBITION",
        "section_title": "GOLGI TENDON ORGANS AND PROPRIOCEPTION: AUTOGENIC INHIBITION KINETICS",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_PROPRIOCEPTION",
        "text": """Proprioception within the musculoskeletal system is governed by two complementary mechanoreceptors: muscle spindles and Golgi tendon organs (GTOs):
1. Anatomical Architecture of the GTO:
   - Located at the myotendinous junction, arranged strictly in series with extrafusal muscle fibers (unlike muscle spindles, which are arranged in parallel).
   - Each GTO consists of braided collagen bundles enclosed within a capsule, innervated by a rapidly conducting Type Ib sensory afferent nerve fiber.
2. Mechanotransduction and Autogenic Inhibition:
   - When a muscle contracts forcefully, active tensile strain pinches the Ib nerve endings between the braided collagen strands, depolarizing the afferent nerve.
   - Type Ib fibers project to the dorsal horn of the spinal cord, synapsing on inhibitory interneurons. These interneurons release gamma-aminobutyric acid (GABA) and glycine onto alpha-motoneurons innervating the homonymous (contracting) muscle.
   - This autogenic inhibition acts as a protective neuromuscular circuit breaker, reflexively downregulating muscle activation if tension threatens to tear tendon or bone.
3. Training Adaptations: Heavy progressive resistance training desensitizes GTO inhibitory feedback, allowing higher maximal voluntary force production."""
    },
    {
        "doc_id": "P1_42_RECIPROCAL_INHIBITION",
        "section_title": "RECIPROCAL INHIBITION AND ANTAGONIST CO-ACTIVATION IN JOINT STABILITY",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_PROPRIOCEPTION",
        "text": """Smooth, coordinated skeletal movement relies on reciprocal inhibition—a neural mechanism that relaxes opposing musculature during agonist contraction:
1. The Reciprocal Inhibition Pathway:
   - When an agonist muscle contracts, its muscle spindle Type Ia afferents fire into the spinal cord.
   - Collateral branches of these Ia afferents synapse on inhibitory Ia interneurons, which hyperpolarize and inhibit the alpha-motoneurons of the antagonist muscle.
   - Example: During rapid quadriceps contraction in knee extension, reciprocal inhibition relaxes the hamstrings to prevent mechanical resistance against the intended movement.
2. Antagonist Co-Activation:
   - In unstable, high-load, or novel motor tasks, the central nervous system partially overrides reciprocal inhibition to produce simultaneous antagonist co-activation (e.g., quadriceps and hamstrings contracting together).
   - Co-activation increases joint compressive forces, stabilizes articular surfaces, prevents aberrant joint translation, and enhances joint stiffness.
   - With motor learning and skill acquisition, unnecessary antagonist co-activation is pruned away, reducing internal resistance and enhancing mechanical efficiency."""
    },
    {
        "doc_id": "P1_43_SCAPULOHUMERAL_RHYTHM",
        "section_title": "SCAPULOHUMERAL RHYTHM: KINEMATIC INTEGRATION IN SHOULDER ABDUCTION",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_JOINT_MECHANICS",
        "text": """Full overhead elevation of the arm (180 degrees of abduction or flexion) requires coordinated kinematic coupling between the glenohumeral joint and the scapulothoracic articulation—termed scapulohumeral rhythm:
1. The 2:1 Kinematic Ratio:
   - For every 3 degrees of total arm elevation, approximately 2 degrees occurs as glenohumeral abduction, and 1 degree occurs as scapulothoracic upward rotation (an overall 2:1 ratio).
   - The Setting Phase (Initial 0 to 30 degrees): Movement is almost exclusively glenohumeral, while the scapula seeks a stable anchoring position on the thoracic wall.
   - Beyond 30 Degrees: The scapula rotates upward smoothly at a constant 2:1 ratio with the humerus.
2. Scapular Force Couples:
   - Upward rotation is driven by a coordinated muscular force couple: the upper trapezius, lower trapezius, and serratus anterior pull in synergistic directions.
   - If the serratus anterior or lower trapezius is weak, upward rotation lags behind humeral elevation, reducing the subacromial space and causing subacromial impingement of the supraspinatus tendon and subacromial bursa against the acromion process."""
    },
    {
        "doc_id": "P1_44_PATELLOFEMORAL_STRESS_KINEMATICS",
        "section_title": "PATELLOFEMORAL JOINT BIOMECHANICS: CONTACT AREA AND RETROPATELLAR STRESS",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_JOINT_MECHANICS",
        "text": """The patella acts as a biomechanical lever, increasing the internal moment arm of the quadriceps tendon relative to the tibiofemoral joint center of rotation:
1. Retropatellar Contact Area Dynamics:
   - At full knee extension (0 degrees), the patella rests superior to the femoral trochlear groove with minimal contact area.
   - As the knee flexes, the patella engages the trochlea, and contact area expands progressively, reaching its maximum between 60 and 90 degrees of knee flexion.
2. Stress Distribution Across Exercise Modalities:
   - Stress = Force / Area.
   - Closed-Kinetic-Chain (Squats, Leg Press): Compressive force increases as knee flexion deepens; however, because patellofemoral contact area also expands significantly, retropatellar stress (pressure per unit area) is distributed across a large cartilaginous surface, peaking around 90 degrees flexion.
   - Open-Kinetic-Chain (Seated Knee Extensions): The external moment arm of the ankle resistance pad is greatest at full extension (0 degrees), where patellofemoral contact area is smallest. Consequently, open-chain knee extensions generate high retropatellar stress between 0 and 30 degrees of extension."""
    },
    {
        "doc_id": "P1_45_NACHEMSON_DISC_PRESSURE",
        "section_title": "INTRADISCAL PRESSURE KINETICS: NACHEMSON'S POSTURAL COMPRESSION HIERARCHY",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_SPINE_BIOMECHANICS",
        "text": """Alf Nachemson's pioneering in vivo pressure measurements inside the human L3-L4 intervertebral disc established how spinal posture and external loading dictate lumbar disc compression:
1. Postural Pressure Hierarchy (Standardized to Standing at 100%):
   - Supine lying down: 25% (unloads the disc, permitting rehydration and fluid imbibition).
   - Standing erect with neutral posture: 100%.
   - Seated upright with back support: 140%.
   - Standing and bending forward at the waist (spinal flexion): 150%.
   - Seated and slouching forward (seated lumbar flexion): 185%.
   - Standing, bending forward, and lifting an external load with bent back: > 220% to 300+%.
2. Biomechanical Implications for Resistance Training:
   - Sitting exerts higher baseline disc pressure than standing because the pelvis tilts posteriorly, flattening normal lumbar lordosis.
   - Lifting loads with a flexed lumbar spine dramatically amplifies anterior disc compression and posterior tensile strain.
   - Maintaining neutral lordosis during deadlifts and squats utilizes the erector spinae and intra-abdominal pressure to share compressive and shear forces, protecting disc integrity."""
    },

    # -------------------------------------------------------------------------
    # Pillar 2: Strength Training Principles and Programming
    # -------------------------------------------------------------------------
    {
        "doc_id": "P2_38_ACCOMMODATING_RESISTANCE_CHAINS",
        "section_title": "ACCOMMODATING RESISTANCE: BIOMECHANICAL PHYSICS OF VARIABLE RESISTANCE BANDS AND CHAINS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_VARIABLE_RESISTANCE",
        "text": """In standard barbell exercises (e.g., squat, bench press), the lifter's leverage and mechanical advantage improve as the lift approaches lockout:
1. The Ascending Strength Curve Dilemma:
   - Because leverage improves near completion, standard barbell loads are limited by the sticking point at the bottom of the movement. Consequently, the top lockout portion of the lift remains submaximally loaded.
2. Chains as Accommodating Resistance:
   - Heavy chains attached to the barbell rest on the floor in the bottom position, reducing barbell load at the sticking point.
   - As the barbell ascends, links lift off the floor link-by-link, linearly increasing total load precisely as the lifter's mechanical advantage improves.
3. Elastic Bands (Hooke's Law: F = -kx):
   - Elastic bands stretch as the bar rises, exponentially increasing tension toward lockout.
   - Band Tension Acceleration: Bands accelerate the barbell downward during the eccentric phase, forcing the lifter to recruit motor units faster to brake the descending bar (overspeed eccentrics), enhancing stretch-shortening cycle potentiation and rate of force development."""
    },
    {
        "doc_id": "P2_39_FRENCH_CONTRAST_PAPE",
        "section_title": "THE FRENCH CONTRAST METHOD AND POST-ACTIVATION PERFORMANCE ENHANCEMENT (PAPE)",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_COMPLEX_TRAINING",
        "text": """Post-Activation Performance Enhancement (PAPE) describes the acute enhancement of explosive muscular force and power output following a heavy conditioning contraction:
1. Physiological Mechanism of PAPE:
   - Phosphorylation of Myosin Regulatory Light Chains: Heavy contractions activate myosin light chain kinase (MLCK), which phosphorylates regulatory light chains on the myosin neck. This increases cross-bridge sensitivity to calcium ions, producing more force at submaximal calcium concentrations.
   - Elevated Spinal Motoneuron Excitability: Enhanced central motor drive and Hoffmann reflex (H-reflex) amplitude.
2. The French Contrast Method:
   - A 4-exercise complex performed in rapid succession with 20 seconds between exercises:
     1. Heavy Compound Lift (80% to 90% 1RM for 2-3 reps) -> Establishes maximal PAPE.
     2. Plyometric Jump (e.g., hurdle hops for 3-4 reps) -> Utilizes potentiation.
     3. Drop-Jump / Depth-Jump (from 30 to 45 cm box) -> Trains explosive reactive strength.
     4. Accelerated / Band-Assisted Jump (overspeed unloading) -> Trains maximal contraction velocity.
   - Yields dramatic adaptations in rate of force development and reactive power."""
    },
    {
        "doc_id": "P2_40_APRE_AUTOREGULATION_SYSTEM",
        "section_title": "AUTOREGULATED PROGRESSIVE RESISTANCE EXERCISE (APRE) PROTOCOLS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_VBT_AUTOREGULATION",
        "text": """Developed by Bryan Mann, Autoregulated Progressive Resistance Exercise (APRE) is an objective, repetition-performance-based system for adjusting weekly loads:
1. The Three Primary Protocols:
   - APRE-10: Designed for hypertrophy and muscular endurance (target: 10 reps).
   - APRE-6: Designed for basic strength and hypertrophy (target: 6 reps).
   - APRE-3: Designed for maximal strength and power (target: 3 reps).
2. Four-Set Structure (Example: APRE-6):
   - Set 1: 50% of estimated 6RM for 10 reps (Warm-up).
   - Set 2: 75% of estimated 6RM for 6 reps (Potentiation).
   - Set 3 (The Test Set): 100% of estimated 6RM for maximum repetitions to failure.
   - Set 4 (The Adjusted Set): Load is adjusted based on Set 3 performance using standardized conversion tables:
     * 0 to 3 reps: Reduce load by 2.5 to 5.0 kg.
     * 4 to 5 reps: Reduce load by 1.0 to 2.5 kg.
     * 6 to 7 reps: Keep load unchanged.
     * 8 to 11 reps: Increase load by 2.5 to 5.0 kg.
     * 12+ reps: Increase load by 5.0 to 7.5 kg.
   - The adjusted weight for Set 4 becomes the new estimated working weight for the subsequent week, ensuring seamless progression matching individual biological adaptation rates."""
    },
    {
        "doc_id": "P2_41_BILATERAL_DEFICIT_PHENOMENON",
        "section_title": "THE BILATERAL DEFICIT: NEUROLOGICAL INTERACTION IN UNILATERAL VS BILATERAL FORCE",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_MUSCLE_ACTIONS",
        "text": """The Bilateral Deficit (BLD) describes the neuromuscular phenomenon where the maximal force generated by two limbs contracting simultaneously (bilaterally) is significantly less than the sum of forces produced by each limb contracting independently (unilaterally):
Bilateral Deficit Index = [Bilateral Force / (Right Unilateral Force + Left Unilateral Force)] x 100.
If the index is < 100%, a bilateral deficit is present (typically 80% to 95% in untrained or unilaterally trained individuals).
Neurological Mechanisms:
1. Interhemispheric Cortical Inhibition: Simultaneous activation of both motor cortices across the corpus callosum produces cross-inhibition, reducing descending corticospinal motor drive to each limb.
2. Motoneuron Recruitment Limitations: Alpha-motoneuron discharge frequency and motor unit synchronization are constrained when neural drive must be distributed bilaterally.
Training Specificity:
- Habitual bilateral training (Olympic weightlifting, powerlifting) eliminates or reverses the deficit into a 'bilateral facilitation' (> 100%).
- Unilateral training (split squats, single-leg presses) maximizes absolute force output per limb, effectively overloading individual muscle-tendon complexes with reduced central fatigue."""
    },

    # -------------------------------------------------------------------------
    # Pillar 3: Exercise Technique and Safe Equipment Use
    # -------------------------------------------------------------------------
    {
        "doc_id": "P3_40_FRONT_SQUAT_MECHANICS",
        "section_title": "FRONT SQUAT KINEMATICS: ANTERIOR DELTOID RACK AND SPINAL SHEAR REDUCTION",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "exercise_technique_safety",
        "group_id": "GRP_P3_SQUAT",
        "text": """The barbell front squat places the barbell across the anterior shoulders, fundamentally altering trunk kinematics and joint torque demands compared to the back squat:
1. The Front Rack Setup:
   - Position: The bar rests securely in the muscular groove formed by the anterior deltoids, clavicles, and elevated thoracic cage.
   - Clean Grip: Two to three fingers under the bar with wrists extended; elbows held high and parallel to the platform throughout the repetition.
   - Alternative Grips: Cross-arm grip or strap grip for lifters with limited wrist extension or lat dorsi flexibility.
2. Torso Angle and Spinal Biomechanics:
   - The anterior barbell position forces the lifter to maintain a strictly upright, near-vertical torso (trunk angle roughly 75 to 85 degrees to the horizontal). Any forward torso flexion causes the barbell to roll forward off the anterior deltoids and drop.
   - Reduced Lumbar Shear: The vertical trunk alignment dramatically shortens the external moment arm on the lumbar spine, reducing lumbar shear forces by 25% to 35% compared to back squats handling equivalent relative loads.
3. Quadriceps Overload: Requires greater anterior knee translation and deeper knee flexion angles, placing high mechanical demands on the vastus lateralis, medialis, and intermedius."""
    },
    {
        "doc_id": "P3_41_HEX_BAR_DEADLIFT",
        "section_title": "HEX BAR (TRAP BAR) DEADLIFT: HYBRID KNEE-HIP EXTENSION AND SACRAL UNLOADING",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "exercise_technique_safety",
        "group_id": "GRP_P3_DEADLIFT",
        "text": """The hexagonal trap bar deadlift alters starting kinematics by placing the lifter inside the perimeter of the frame:
1. Center of Gravity Alignment:
   - In a conventional straight-bar deadlift, the bar is constrained anterior to the shins, creating an obligatory external moment arm relative to the lumbar spine and hip joint centers.
   - The trap bar's neutral hand placement aligns the barbell sleeves and external resistance directly in line with the lifter's midfoot and anatomical center of gravity.
2. Hybrid Mechanics (Squat-Hinge Blend):
   - The trap bar allows greater forward knee translation and deeper knee flexion (roughly 100 degrees vs 80 degrees in straight bar), distributing joint torque evenly between the knee extensors (quadriceps) and hip extensors (gluteals and hamstrings).
   - Peak lumbar flexion moments are reduced by approximately 15% to 20%, making the trap bar deadlift the safest heavy pulling modality for individuals with lumbar disc pathology.
3. Velocity and Power Superiority: Because the bar path is strictly vertical without shin collision, lifters achieve significantly higher concentric barbell velocities and peak power outputs across all percentages of 1RM."""
    },
    {
        "doc_id": "P3_42_FARMERS_WALK_CARRIES",
        "section_title": "LOADED CARRIES: FARMER'S WALK BIOMECHANICS AND LATERAL CORE INTEGRITY",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "exercise_technique_safety",
        "group_id": "GRP_P3_POSTERIOR_CHAIN",
        "text": """Loaded carries (such as the bilateral Farmer's Walk or unilateral Suitcase Carry) train functional structural stiffness and anti-lateral flexion:
1. Anti-Lateral Flexion Mechanics (Quadratus Lumborum Integration):
   - In a unilateral suitcase carry, an asymmetrical load held in one hand exerts a lateral bending moment on the lumbar spine toward that side.
   - The contralateral quadratus lumborum, external oblique, and internal oblique must contract isometrically with immense force to maintain a level pelvis and vertical spine.
2. Scapulothoracic and Grip Demands:
   - Heavy loads held at the sides pull the shoulder girdle downward into depression and protraction.
   - The trapezius (upper, middle), levator scapulae, and rhomboids must sustain prolonged isometric tension to stabilize the shoulder girdle, building neck and upper-back structural integrity.
   - Long finger flexors (flexor digitorum profundus and superficialis) undergo intense isometric loading, rapidly expanding grip endurance.
3. Gait Kinematics: Walking with loads forces shortened, deliberate strides with flat-foot heel strikes to avoid abrupt vertical accelerations that threaten spinal stability."""
    },

    # -------------------------------------------------------------------------
    # Pillar 4: Nutrition Fundamentals and Hydration
    # -------------------------------------------------------------------------
    {
        "doc_id": "P4_41_RED_S_ENERGY_AVAILABILITY",
        "section_title": "RELATIVE ENERGY DEFICIENCY IN SPORT (RED-S) AND LOW ENERGY AVAILABILITY",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_ENERGY",
        "text": """Relative Energy Deficiency in Sport (RED-S)—broadened from the female athlete triad—describes the systemic multi-organ pathology resulting from chronic Low Energy Availability (LEA):
1. Mathematical Energy Availability (EA):
   EA = [Daily Energy Intake (kcal) - Exercise Energy Expenditure (kcal)] / Fat-Free Mass (FFM in kg).
   - Optimal EA: >= 45 kcal/kg FFM/day. Supports basal physiological functions, cellular repair, and athletic adaptation.
   - Subclinical LEA: 30 to 45 kcal/kg FFM/day.
   - Clinical LEA Threshold: < 30 kcal/kg FFM/day. The body enters energy conservation mode, systematically shutting down non-essential physiological processes.
2. Physiological Consequences of RED-S:
   - Endocrine: Suppression of the hypothalamic-pituitary-gonadal (HPG) axis (amenorrhea/oligomenorrhea in females, suppressed testosterone and libido in males); blunted thyroid hormones (low free T3).
   - Skeletal: Elevated bone resorption and blunted bone formation, causing rapid bone mineral density loss and recurring stress fractures.
   - Metabolic and Immunological: Depressed resting metabolic rate, chronic systemic inflammation, frequent infections, and impaired recovery."""
    },
    {
        "doc_id": "P4_42_CARB_PERIODIZATION_PROTOCOLS",
        "section_title": "CARBOHYDRATE PERIODIZATION: 'FUEL FOR THE WORK REQUIRED' FRAMEWORK",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_CARBS_METABOLISM",
        "text": """Carbohydrate periodization—moving away from static daily carbohydrate targets toward dynamic matching of carbohydrate intake to training demand ('Fuel for the Work Required'):
1. The Physiology of 'Train Low':
   - Exercising with low muscle glycogen (e.g., fasting morning sessions or twice-a-day training without intervening carbohydrates) amplifies cellular metabolic stress.
   - High AMP/ATP ratio and low glycogen activate AMPK and p38 MAPK, which upregulate PGC-1alpha transcription, stimulating greater mitochondrial biogenesis and fat oxidation enzymes than training with full glycogen.
2. The Critical Caveat:
   - High-intensity interval workouts, technical barbell lifting, and competitive events demand high glycolytic flux; performing these sessions in a glycogen-depleted state impairs power output, elevates muscle protein catabolism, suppresses immune function, and compromises movement mechanics.
3. Daily Matching Protocols:
   - Low-Intensity Recovery Days: 2 to 3 g/kg/day carbohydrate.
   - Moderate Training Days (60 min mixed): 4 to 6 g/kg/day.
   - High-Intensity / Double-Session Days: 7 to 10 g/kg/day."""
    },
    {
        "doc_id": "P4_43_SODIUM_BICARBONATE_BUFFERING",
        "section_title": "SODIUM BICARBONATE ERGOGENICS: EXTRACELLULAR BUFFERING AND PROTOCOLS",
        "source_id": "US-NIH-ODS-SUPP",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_SUPPLEMENTS",
        "text": """Sodium bicarbonate (NaHCO3) is an evidence-based extracellular buffering agent proven to enhance performance in high-intensity exercise lasting 60 seconds to 10 minutes:
1. Buffering Mechanism:
   - Intense anaerobic glycolysis generates protons (H+), driving myoplasmic pH down toward 6.5.
   - Ingesting sodium bicarbonate elevates blood bicarbonate concentration ([HCO3-]) from ~24 mmol/L up to 30 to 32 mmol/L, raising extracellular pH (alkalosis).
   - This steepens the trans-sarcolemmal H+ electrochemical gradient, accelerating the extrusion of protons out of contracting myocytes via monocarboxylate transporters (MCTs), delaying intracellular acidosis and preserving cross-bridge function.
2. Dosing Protocols and Gastrointestinal Mitigation:
   - Ergogenic Dose: 0.2 to 0.3 grams per kg of body mass, consumed 60 to 120 minutes prior to exercise.
   - Gastrointestinal Distress Risk: Bicarbonate reacts with stomach gastric acid to produce large volumes of carbon dioxide gas (CO2), causing nausea, bloating, abdominal cramping, and explosive osmotic diarrhea.
   - Mitigation: Split dosing into 3 to 4 smaller boluses consumed alongside a small high-carbohydrate meal (e.g., bread or rice) over a 2-hour window, or utilizing delayed-release enteric-coated capsules."""
    },

    # -------------------------------------------------------------------------
    # Pillar 5: Sleep, Recovery, and Physical Activity
    # -------------------------------------------------------------------------
    {
        "doc_id": "P5_32_JET_LAG_CHRONOBIOLOGY",
        "section_title": "CHRONOBIOLOGY OF JET LAG: CIRCADIAN PHASE DELAYS VS ADVANCES ACROSS TIMEZONES",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_CIRCADIAN",
        "text": """Jet lag (circadian desynchronosis) occurs when rapid trans-meridian travel creates an abrupt mismatch between internal circadian rhythmicity and the external environmental light-dark cycle:
1. Westward vs Eastward Travel Asymmetry:
   - Westward Travel (Phase Delay): 'Lengthens' the day. Human intrinsic circadian period is slightly longer than 24 hours (~24.2 hours); hence, delaying bedtime is biologically easier, requiring roughly 1 day of recovery per 1.5 time zones crossed.
   - Eastward Travel (Phase Advance): 'Shortens' the day, forcing the circadian clock to advance. Requires roughly 1 full day of acclimatization per time zone crossed.
2. Circadian Phase Response Curve (PRC) Interventions:
   - Eastward Travel: Seek bright sunlight in the destination morning (advances circadian phase); strictly wear blue-blocking sunglasses during destination evening.
   - Westward Travel: Seek bright sunlight in the late afternoon/evening (delays circadian phase); avoid bright light early in the morning.
3. Melatonin Timing: Low-dose exogenous melatonin (0.5 to 3 mg) taken at the destination bedtime facilitates rapid phase alignment."""
    },
    {
        "doc_id": "P5_33_NAPPING_PHYSIOLOGY",
        "section_title": "NAPPING KINETICS: THE 20-MINUTE POWER NAP VS THE 90-MINUTE SLEEP CYCLE",
        "source_id": "US-CDC-SLEEP-2022",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_SLEEP_ARCH",
        "text": """Daytime naps represent an effective physiological countermeasure against accumulated sleep debt and afternoon circadian alertness dips (the postprandial dip around 13:00 to 15:00):
1. The 20 to 30 Minute Power Nap:
   - Restricts sleep to NREM Stages 1 and 2 (N1 and N2).
   - Lowers homeostatic sleep pressure (clearing cerebral adenosine), restores psychomotor reaction times, and enhances alertness.
   - Critical Safety Margin: Waking before entering Stage 3 slow-wave sleep prevents 'sleep inertia'—the grogginess, disorientation, and impaired cognitive function that occurs when abruptly awakened from deep delta-wave sleep.
2. The 90-Minute Full Sleep Cycle Nap:
   - Allows the brain to progress through a complete ultradian cycle: N1 -> N2 -> N3 (SWS) -> REM sleep.
   - Delivers both somatic growth hormone tissue repair (from SWS) and motor skill memory consolidation (from REM), followed by natural waking from light sleep without sleep inertia.
3. Timing Cutoff: Naps must conclude before 15:00 to 16:00 to avoid diminishing nocturnal homeostatic sleep drive."""
    },

    # -------------------------------------------------------------------------
    # Pillar 6: Training Adaptations, Fatigue, and Load Management
    # -------------------------------------------------------------------------
    {
        "doc_id": "P6_31_EWMA_ACWR_MODELING",
        "section_title": "EXPONENTIALLY WEIGHTED MOVING AVERAGES (EWMA) IN WORKLOAD MODELING",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "training_adaptations_fatigue_load",
        "group_id": "GRP_P6_LOAD_MONITORING",
        "text": """While rolling average Acute:Chronic Workload Ratios (ACWR) treat every day within a 7-day or 28-day window with equal mathematical weight, physiological decay occurs continuously.
The Exponentially Weighted Moving Average (EWMA) model provides superior biological fidelity:
1. Mathematical Weighting Decay:
   - EWMA assigns exponentially greater mathematical weight to workloads performed in the most recent days, decaying older workloads gradually:
     EWMA_today = Workload_today x lambda + (1 - lambda) x EWMA_yesterday.
   - The decay constant lambda is calculated as:
     lambda = 2 / (N + 1), where N represents the time decay window (e.g., 7 days for acute, 28 days for chronic).
2. Biological Accuracy:
   - A punishing, high-volume workout completed yesterday exerts vastly greater residual neuromuscular and inflammatory fatigue than a workout completed 6 days ago.
   - Rolling averages falsely show an abrupt drop in fatigue on day 8 when that workout falls off the cliff; EWMA smoothly decays the workload, eliminating artificial spikes and drops."""
    },
    {
        "doc_id": "P6_32_TENDON_HYSTERESIS_SSC",
        "section_title": "TENDON HYSTERESIS AND ELASTIC ENERGY RECOIL IN THE STRETCH-SHORTENING CYCLE",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "training_adaptations_fatigue_load",
        "group_id": "GRP_P6_CONNECTIVE_TISSUE",
        "text": """Tendons operate as highly efficient biological springs, cyclically storing and returning mechanical energy during locomotion, jumping, and sprinting:
1. The Stretch-Shortening Cycle (SSC):
   - During the eccentric braking phase of a jump or sprint stride, contracting muscle fascicles remain nearly isometric, while the compliant tendon (e.g., Achilles tendon) undergoes rapid tensile elongation, absorbing kinetic energy as mechanical strain energy.
   - During the immediate concentric rebound, the tendon recoils violently, releasing stored elastic energy at power outputs exceeding the maximal metabolic capacity of the muscle alone.
2. Tendon Hysteresis:
   - The percentage of mechanical energy lost as heat during the stretch-recoil cycle:
     Hysteresis = (Energy Absorbed - Energy Returned) / Energy Absorbed.
   - Healthy human tendons exhibit remarkably low hysteresis (roughly 5% to 10%), returning 90% to 95% of stored elastic strain energy.
3. Training Adaptations: High-velocity plyometric training increases tendon cross-sectional stiffness, reducing tendon strain during maximal loading and accelerating elastic recoil velocity."""
    },

    # -------------------------------------------------------------------------
    # Pillar 7: General Fitness Education and Age-Appropriate Safety
    # -------------------------------------------------------------------------
    {
        "doc_id": "P7_29_PEH_HYPERTENSION_EXERCISE",
        "section_title": "POST-EXERCISE HYPOTENSION (PEH): MECHANISMS AND HYPERTENSION MANAGEMENT",
        "source_id": "US-HHS-PAG-2018",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_SPECIAL_POPULATIONS",
        "text": """Post-Exercise Hypotension (PEH) describes the sustained, clinically significant reduction in systemic arterial blood pressure that persists for 12 to 24 hours following a single bout of moderate aerobic or resistance exercise:
1. Hemodynamic Mechanisms:
   - Persistent Peripheral Vasodilation: Sustained release of endothelial vasodilators (nitric oxide, histamine, adenosine, and prostaglandins) reduces systemic vascular resistance.
   - Sympathetic Vascular Downregulation: Decreased sympathetic outflow from the central rostral ventrolateral medulla to peripheral vascular beds.
   - Blood pressure typically drops by 5 to 8 mmHg systolic and 3 to 5 mmHg diastolic in hypertensive individuals.
2. Clinical Value in Hypertension:
   - Performing daily moderate-intensity aerobic exercise (e.g., 30 minutes of brisk walking) harnesses this transient PEH effect continuously, maintaining lower 24-hour ambulatory blood pressure and reducing long-term stroke and myocardial infarction risk.
3. Safety Precaution: Hypertensive individuals must avoid prolonged isometric straining (straining against immovable loads with closed glottis) which causes transient, dangerous blood pressure spikes (> 250 mmHg)."""
    },
    {
        "doc_id": "P7_30_OSTEOARTHRITIS_JOINT_PUMPING",
        "section_title": "EXERCISE IN OSTEOARTHRITIS: CARTILAGE NUTRITION AND PERIARTICULAR STABILIZATION",
        "source_id": "US-NIH-NIA-EXERCISE",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_AGING_MUSCLE",
        "text": """A common misconception is that physical activity 'wears out' arthritic joints and that individuals with osteoarthritis should rest to preserve cartilage:
1. Biological Reality of Cartilage Nutrition:
   - Articular cartilage has zero blood supply; it relies exclusively on cyclic joint compression and decompression to circulate synovial fluid, delivering oxygen and glucose to chondrocytes and removing inflammatory cytokines.
   - Prolonged joint immobilization leads to cartilage starvation, matrix softening (chondromalacia), and joint capsule contracture.
2. Muscle Strengthening as a Shock Absorber:
   - Strong periarticular muscles (e.g., quadriceps in knee osteoarthritis) act as dynamic shock absorbers, attenuating peak impact forces transmitted across the articular surface by up to 30% to 50%.
3. Exercise Prescription:
   - Low-impact aerobic conditioning (cycling, swimming, elliptical) combined with progressive resistance training and range-of-motion stretching significantly reduces arthritic joint pain and enhances functional mobility without accelerating joint degradation."""
    }
]
