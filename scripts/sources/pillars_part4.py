"""Pillars Part 4: Comprehensive Expansion Across All 7 Nova-Fit Pillars.

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
        "doc_id": "P1_46_RATE_CODING_DOUBLETS",
        "section_title": "MOTOR UNIT RATE CODING AND THE PHYSIOLOGY OF MOTOR NEURON DOUBLETS",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_MOTOR_UNITS",
        "text": """Graduation of skeletal muscle force is mediated by two primary neural control strategies: motor unit recruitment (Henneman's size principle) and rate coding (discharge frequency):
1. Discharge Frequency (Rate Coding):
   - Motor units typically discharge action potentials at frequencies ranging from 8 to 12 Hz at recruitment onset, scaling up to 30 to 60 Hz during maximal voluntary contractions.
   - At higher discharge frequencies, successive twitch contractions summate before muscle relaxation can occur, producing a smooth, fused tetanic contraction that generates 3 to 5 times more force than an isolated twitch.
2. Motor Neuron Doublets (High-Frequency Initial Bursts):
   - During rapid, ballistic contractions requiring maximal rate of force development (RFD), motor neurons discharge an initial pair of action potentials with an extremely short inter-spike interval (< 10 milliseconds, corresponding to an instantaneous frequency > 100 to 200 Hz).
   - This 'doublet' induces the 'catchlike property' of skeletal muscle: a rapid surge in sarcoplasmic calcium saturation that stiffens cross-bridges, producing an explosive rise in early force that persists throughout subsequent lower-frequency stimulation.
3. Training Adaptations: Explosive ballistic training increases the incidence of initial doublets during rapid motor tasks."""
    },
    {
        "doc_id": "P1_47_FORCE_TIME_IMPULSE",
        "section_title": "THE FORCE-TIME CURVE AND MATHEMATICAL IMPULSE IN ATHLETIC LOCOMOTION",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_LEVERS_MOMENTS",
        "text": """In human locomotion, sprinting, and jumping, performance is dictated not simply by peak force, but by the mathematical impulse generated against the ground:
1. Mathematical Definition of Impulse:
   Impulse (J) = Integral of Force (F) over Time (dt) = Delta Momentum = Mass x Delta Velocity.
   - Ground Reaction Force (GRF) applied over the foot contact time directly determines the change in the athlete's center of mass velocity.
2. The Contact Time Constraint:
   - Maximal isometric force production requires approximately 300 to 400 milliseconds to develop fully.
   - In contrast, ground contact times during elite sprinting are roughly 80 to 100 milliseconds; long jump takeoffs last ~120 ms; change-of-direction cuts last ~150 to 200 ms.
   - Consequently, athletes rarely reach peak absolute force during functional locomotion; athletic success depends on the area under the force-time curve during the first 100 milliseconds—the Rate of Force Development (RFD) and early impulse.
3. Resistance Training Translation: Training must balance maximal absolute strength (elevating the peak of the curve) with explosive ballistic training (steepening the early slope of the curve)."""
    },
    {
        "doc_id": "P1_48_MYOTENDINOUS_JUNCTION",
        "section_title": "THE MYOTENDINOUS JUNCTION (MTJ): ULTRASTRUCTURE AND MECHANICAL SHEAR DISSIPATION",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_CONNECTIVE_TISSUE",
        "text": """The myotendinous junction (MTJ) represents the specialized anatomical transition zone where intracellular contractile sarcomeres anchor into extracellular tendon collagen fibers:
1. Folding and Interdigitations:
   - A planar, blunt junction between muscle and tendon would concentrate tensile forces, predisposing the interface to catastrophic peeling failure.
   - At the MTJ, the terminal sarcolemma forms extensive, finger-like invaginations and longitudinal foldings (interdigitations), expanding the total contact surface area by 10- to 20-fold.
   - This geometry converts direct tensile stress into low-magnitude shear stress distributed across the entire folded membrane, protecting the junction against mechanical tearing.
2. Molecular Anchoring Complexes:
   - Dystrophin-Glycoprotein Complex (DGC) and Integrin Alpha7-Beta1 Complexes: Span the sarcolemma, connecting terminal intracellular actin filaments to laminin and Type IV collagen in the basal lamina, which in turn anchors to Type I and III tendon collagen fibrils.
3. Strain Vulnerability: Despite its folded architecture, the MTJ remains the most frequent site of acute muscle strain injuries during high-velocity eccentric loading (e.g., biceps femoris strain in sprinting)."""
    },
    {
        "doc_id": "P1_49_CROSS_EDUCATION_NEURAL",
        "section_title": "THE CROSS-EDUCATION PHENOMENON: CONTRALATERAL STRENGTH TRANSFER",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_MOTOR_UNITS",
        "text": """Cross-education describes the clinical and neuromuscular phenomenon wherein unilateral resistance training of one limb produces a significant increase in the strength of the opposite, untrained contralateral limb:
1. Magnitude of Strength Transfer:
   - On average, the untrained contralateral limb gains approximately 50% to 60% of the relative strength gained by the trained limb (roughly an 8% to 12% absolute strength increase in the untrained limb) in the complete absence of muscle hypertrophy.
2. Neurological Mechanisms:
   - Cortical Motor Spillover: High-intensity unilateral voluntary motor contractions activate not only the contralateral primary motor cortex (M1), but also induce 'spillover' excitation across the corpus callosum into the ipsilateral motor cortex, supplementary motor area (SMA), and premotor cortex.
   - Attenuation of Interhemispheric Inhibition: Unilateral training downregulates transcallosal inhibitory pathways that normally suppress contralateral motor output.
   - Spinal Motoneuron Adaptations: Increases descending corticospinal drive and motor unit recruitment in spinal pathways supplying the untrained limb.
3. Clinical Utility: Highly valuable during unilateral limb casting, orthopedic rehabilitation, or post-stroke hemiparesis to preserve strength and limit atrophy in immobilized limbs."""
    },
    {
        "doc_id": "P1_50_SATELLITE_CELL_NICHE",
        "section_title": "SKELETAL MUSCLE SATELLITE CELLS AND THE MYONUCLEAR DOMAIN HYPOTHESIS",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_SARCOMERE",
        "text": """Skeletal muscle fibers are giant, multinucleated syncytia whose nuclei (myonuclei) are post-mitotic and incapable of cell division:
1. The Satellite Cell Niche:
   - Satellite cells are quiescent myogenic stem cells nestled in a specialized microenvironmental niche between the sarcolemma and the basal lamina of each muscle fiber.
   - In the resting state, satellite cells express the paired-box transcription factor Pax7.
2. Activation and Differentiation:
   - Mechanical strain or sarcolemmal microtrauma triggers the release of local autocrine and paracrine growth factors (hepatocyte growth factor / HGF, IGF-1, fibroblast growth factors / FGFs).
   - Activated satellite cells upregulate the myogenic regulatory factor MyoD and proliferate. A portion self-renews to maintain the stem cell pool, while the remainder differentiate into myoblasts, align, and fuse with the existing damaged or growing muscle fiber, donating their nuclei.
3. The Myonuclear Domain Ceiling:
   - The 'myonuclear domain hypothesis' posits that each individual myonucleus can govern the transcriptional needs of only a finite volume of cytoplasm.
   - When muscle hypertrophy expands fiber cross-sectional area beyond 15% to 20% over baseline, satellite cell fusion and new myonuclear accretion become obligatory to support continued myofibrillar protein synthesis."""
    },

    # -------------------------------------------------------------------------
    # Pillar 2: Strength Training Principles and Programming
    # -------------------------------------------------------------------------
    {
        "doc_id": "P2_42_WESTSIDE_CONJUGATE_METHODS",
        "section_title": "THE CONJUGATE METHOD: MAX EFFORT, DYNAMIC EFFORT, AND REPETITION EFFORT",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_PERIODIZATION",
        "text": """Developed by Louie Simmons at Westside Barbell (adapted from Soviet athletic methodologies), the Conjugate Method trains multiple athletic qualities concurrently within each weekly microcycle using three distinct training methods:
1. Maximal Effort Method (MEM):
   - Execution: Lifting a maximal load (>= 90% to 100% 1RM) for a 1 to 3 repetition maximum.
   - Adaptation: Maximizes central motor unit recruitment, rate coding, and intermuscular coordination. To prevent CNS accommodation, the primary exercise variation (e.g., box squat vs safety squat bar vs deficit deadlift) is rotated every 1 to 3 weeks.
2. Dynamic Effort Method (DEM):
   - Execution: Moving submaximal loads (50% to 60% 1RM + 25% accommodating band or chain resistance) with maximal concentric acceleration for multiple low-rep sets (e.g., 8 to 10 sets of 2 to 3 reps with 60s rest).
   - Adaptation: Maximizes rate of force development (RFD) and kinetic bar velocity.
3. Repetition Effort Method (REM):
   - Execution: Lifting submaximal loads (60% to 80% 1RM) for higher repetitions (8 to 15+ reps) taken near muscular failure.
   - Adaptation: Stimulates myofibrillar hypertrophy, strengthens connective tissues, and addresses muscular weak points in accessory movements."""
    },
    {
        "doc_id": "P2_43_TRIPHASIC_TRAINING_SYSTEM",
        "section_title": "TRIPHASIC TRAINING: EXPLOITING ECCENTRIC, ISOMETRIC, AND CONCENTRIC PHASES",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_PERIODIZATION",
        "text": """Developed by Cal Dietz, Triphasic Training structures dynamic athletic movements into three distinct biological contraction phases trained sequentially across dedicated mesocycles:
1. Block 1: Eccentric Focus (2 to 3 weeks):
   - Execution: Slow, controlled eccentric lowering (typically 5 to 6 seconds) with heavy loads (75% to 85% 1RM), followed by explosive concentric drive.
   - Adaptation: Increases muscle stiffness, titin compliance, tendon strength, and trains the nervous system to absorb and store kinetic energy during athletic deceleration.
2. Block 2: Isometric Focus (2 to 3 weeks):
   - Execution: Fast eccentric drop, followed by an aggressive 3 to 4 second static pause at the bottom transition point, before explosive concentric drive.
   - Adaptation: Eliminates passive elastic energy, training the nervous system to instantly stop downward momentum and recruit motor units from zero velocity (dynamic-to-static motor transitions).
3. Block 3: Concentric Focus (2 to 3 weeks):
   - Execution: Pure reactive velocity and RFD, executing explosive concentric movements without pauses or slow tempos, fully realizing the athletic transfer of the previous blocks."""
    },
    {
        "doc_id": "P2_44_MINIMUM_EFFECTIVE_DOSE",
        "section_title": "MINIMUM EFFECTIVE DOSE (MED) FOR STRENGTH AND MUSCLE MAINTENANCE",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_VOLUME_DOSE",
        "text": """During competitive sports seasons, demanding work cycles, or military deployments, maintaining accumulated strength and muscle mass requires dramatically less volume than initially required to build them:
1. Volume Reductions for Maintenance:
   - Research demonstrates that existing muscular strength and hypertrophy can be maintained for up to 12 to 32 weeks with as little as 1/3 to 1/4 of previous training volume.
   - A single high-quality session per week (e.g., 2 to 3 hard sets per major movement pattern) is sufficient to maintain adaptations in young adults; older adults may require 2 sessions per week.
2. The Critical Intensity Anchor:
   - Volume (sets) can be drastically reduced, but intensity (load % 1RM and proximity to failure) must be strictly maintained.
   - If training sets are reduced to 1 or 2 sets per exercise, those sets must still be performed at high loads (>= 75% to 85% 1RM) and taken to within 1 to 2 RIR.
   - Dropping both volume and intensity simultaneously induces rapid neuromuscular detraining."""
    },
    {
        "doc_id": "P2_45_EXERCISE_ORDERING_PHYSIOLOGY",
        "section_title": "EXERCISE ORDERING: COMPLEX MULTI-JOINT LIFTS PRIOR TO ISOLATION",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_SET_CONFIGURATIONS",
        "text": """The sequence in which exercises are performed within a workout fundamentally impacts total mechanical work, power output, and safety:
1. The Primary Ordering Rule:
   - Multi-joint, high-skill compound exercises (squats, deadlifts, Olympic cleans, overhead presses) should always precede single-joint isolation exercises (leg extensions, lateral raises, biceps curls).
   - Rationale: Multi-joint lifts demand complex neuromuscular coordination and spinal stabilization from core musculature. Fatiguing spinal stabilizers or synergists first (pre-exhaustion) degrades kinematic stability during subsequent heavy compound lifts, increasing spinal shear and injury risk.
2. Power and Velocity Precedence:
   - High-velocity explosive movements (plyometrics, Olympic lifts, sprint accelerations) must be placed at the very beginning of the session immediately following the warm-up, when central nervous system drive is fresh and free from metabolic acidosis.
3. Priority Principle:
   - Exercises performed earliest in the workout consistently demonstrate the greatest longitudinal strength and hypertrophy gains compared to exercises performed at the end of the session."""
    },

    # -------------------------------------------------------------------------
    # Pillar 3: Exercise Technique and Safe Equipment Use
    # -------------------------------------------------------------------------
    {
        "doc_id": "P3_43_LOW_BAR_SQUAT_KINEMATICS",
        "section_title": "LOW-BAR BACK SQUAT: POSTERIOR CHAIN BIOMECHANICS AND SACRAL MOMENTS",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "exercise_technique_safety",
        "group_id": "GRP_P3_SQUAT",
        "text": """The low-bar back squat positions the barbell across the posterior deltoids along the spine of the scapula, approximately 2 to 3 inches lower than the high-bar position:
1. Center of Mass and Torso Incline:
   - To keep the barbell balanced directly over the midfoot, the lower bar placement requires the lifter to lean the torso forward into a more inclined angle (roughly 45 to 55 degrees to the horizontal).
2. Moment Arm Distribution:
   - Shorter Knee Moment Arm: The forward torso incline shifts the pelvis further backward, resulting in less forward knee translation and a shorter external moment arm on the knee joint.
   - Longer Hip Moment Arm: The external moment arm relative to the hip joint axis expands significantly.
3. Muscular Recruitment:
   - Dramatically increases mechanical load on the posterior chain: gluteus maximus, hamstrings, and adductor magnus.
   - Handled Loads: Most lifters can lift roughly 5% to 10% more weight in the low-bar squat compared to high-bar due to the increased recruitment of the powerful hip musculature.
   - Spinal Consideration: Generates higher lumbar extensor torque, demanding immense isometric contraction of the erector spinae and rigid intra-abdominal bracing."""
    },
    {
        "doc_id": "P3_44_SUMO_DEADLIFT_MECHANICS",
        "section_title": "SUMO DEADLIFT: HIP EXTERNAL ROTATION AND LUMBAR SHEAR REDUCTION",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "exercise_technique_safety",
        "group_id": "GRP_P3_DEADLIFT",
        "text": """The sumo deadlift utilizes a wide stance with feet rotated externally, placing the arms inside the knees:
1. Kinematic Comparison with Conventional Deadlift:
   - Torso Angle: The sumo deadlift permits a significantly more upright torso angle (roughly 60 to 70 degrees vs 45 degrees in conventional).
   - Barbell Distance: Because the hips can be positioned closer horizontally to the barbell in the sagittal plane, the external moment arm on the lumbar spine and L5-S1 intervertebral disc is reduced by approximately 10% to 15%.
   - Vertical Displacement: The wide foot stance shortens the vertical distance the barbell must travel to reach lockout by roughly 20% to 25%.
2. Joint and Muscle Demands:
   - Demands extreme active hip abduction and external rotation mobility.
   - Higher Quadriceps and Adductor Recruitment: Knee flexion angles are deeper at the start, placing high demands on the vastus medialis, vastus lateralis, and adductor magnus.
   - Hip Anatomy Compatibility: Lifters with deep, forward-facing acetabula may experience bony femoral-acetabular impingement in wide sumo stances, making conventional or semi-sumo setups biomechanically superior for their anatomy."""
    },
    {
        "doc_id": "P3_45_PARALLEL_BAR_DIP_SAFETY",
        "section_title": "PARALLEL BAR DIPS: GLENOHUMERAL CAPSULAR STRAIN AND DEPTH BOUNDARIES",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "exercise_technique_safety",
        "group_id": "GRP_P3_PRESS",
        "text": """The parallel bar dip is a potent compound pushing movement for the pectoralis major and triceps brachii, but requires strict boundary control to protect the shoulder joint:
1. The Danger of Excessive Depth:
   - As the body descends past 90 degrees of elbow flexion, the humerus moves into extreme extension (hyperextension) behind the plane of the scapula.
   - In deep humeral extension under bodyweight load, the humeral head translates anteriorly with immense force, stretching and stressing the thin anterior glenohumeral capsule, the labrum, and the anterior deltoid tendon.
2. Technical Safety Guidelines:
   - Safe Depth Threshold: The descent must terminate when the upper arm is parallel to the floor (elbows at 90 degrees flexion). Descending deeper provides negligible additional muscular hypertrophy while escalating capsular and acromioclavicular (AC) joint injury risk.
   - Torso Lean: Leaning the torso forward at roughly 30 degrees with knees bent shifts load onto the pectoralis major; keeping the torso vertical biases the triceps.
   - Scapular Position: Maintain active scapular depression and retraction throughout; never allow shoulders to shrug up into the ears at the bottom."""
    },

    # -------------------------------------------------------------------------
    # Pillar 4: Nutrition Fundamentals and Hydration
    # -------------------------------------------------------------------------
    {
        "doc_id": "P4_44_MAGNESIUM_ATP_CHELATION",
        "section_title": "MICRONUTRIENT METABOLISM: MAGNESIUM-ATP CHELATION AND KINASE ENZYMES",
        "source_id": "US-NIH-ODS-SUPP",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_MICRONUTRIENTS",
        "text": """Magnesium (Mg2+) is an essential intracellular divalent cation that acts as an obligate cofactor in over 300 enzymatic reactions:
1. Chelation with ATP (The Mg-ATP Complex):
   - In cellular bioenergetics, biologically active ATP does not exist as free ATP4-; it exists almost exclusively chelated with a magnesium ion as Mg-ATP2-.
   - The divalent magnesium ion binds to the negatively charged oxygen atoms on the beta and gamma phosphate groups of ATP, neutralizing repulsive charges and stabilizing the molecule in a conformation that allows kinase enzymes (such as creatine kinase, phosphofructokinase, and hexokinase) to transfer phosphate groups.
2. Muscle Contraction and Neuromuscular Transmission:
   - Magnesium acts as a physiological calcium antagonist: it competes with Ca2+ for binding sites on troponin C and regulates the gating of sarcoplasmic reticulum calcium release channels.
   - Low cellular magnesium promotes intracellular calcium accumulation, hyper-irritability of the motor endplate, and muscle cramping.
3. Recommended Intake and Athletic Losses: Adults require 310 to 420 mg/day; strenuous exercise increases urinary and sweat magnesium excretion by 10% to 20%."""
    },
    {
        "doc_id": "P4_45_CASEIN_MICELLAR_KINETICS",
        "section_title": "CASEIN MICELLAR BIOCHEMISTRY: SLOW AMINO ACID ABSORPTION AND NOCTURNAL ANTICATABOLISM",
        "source_id": "USDA-HHS-DGA-2020",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_PROTEIN_MPS",
        "text": """Bovine milk protein comprises approximately 80% casein and 20% whey, exhibiting contrasting digestive pharmacokinetics:
1. Micellar Structure and Gastric Clotting:
   - Casein exists naturally in milk as large, colloidal spherical aggregates termed 'micelles', stabilized by hydrophobic interactions and colloidal calcium phosphate.
   - Upon entering the acidic environment of the stomach (gastric pH 1.5 to 2.0), the enzyme pepsin cleaves the hydrophilic kappa-casein surface layer. The destabilized micelles precipitate and coagulate into a dense, gelatinous clot or curd.
2. Sustained Aminoacidemia:
   - This gastric clot empties very slowly from the stomach into the duodenum over an extended 6- to 8-hour period.
   - Unlike whey (which produces a rapid, transient spike in amino acids that returns to baseline within 3 hours), micellar casein induces a moderate, sustained plateau of hyperaminoacidemia lasting 7+ hours.
3. Clinical Utility for Sleep:
   - Consuming 30 to 40 grams of micellar casein protein 30 minutes before sleep sustains elevated muscle protein synthesis rates and suppresses whole-body protein breakdown throughout the overnight fasting window."""
    },
    {
        "doc_id": "P4_46_GI_DISTRESS_ENDURANCE",
        "section_title": "EXERCISE-INDUCED GASTROINTESTINAL SYNDROME: SPLANCHNIC HYPOPERFUSION AND CARBS",
        "source_id": "US-NIH-ODS-SUPP",
        "topic_domain": "nutrition_fundamentals_hydration",
        "group_id": "GRP_P4_CARBS_METABOLISM",
        "text": """Gastrointestinal (GI) distress (cramping, nausea, bloating, ischemic diarrhea) affects 30% to 70% of endurance athletes, driven by physiological and nutritional factors:
1. Exercise-Induced Splanchnic Hypoperfusion:
   - During heavy endurance exercise, sympathetic vasoconstriction shunts up to 60% to 80% of splanchnic blood flow away from the stomach and intestines toward working skeletal muscles and the skin for thermoregulation.
   - Splanchnic ischemia injures epithelial enterocytes, loosening tight junctions and increasing intestinal permeability ('leaky gut'), allowing endotoxins to enter circulation.
2. Dual-Transportable Carbohydrates:
   - Intestinal absorption of glucose is mediated exclusively by the Sodium-Glucose Cotransporter 1 (SGLT1), which saturates at roughly 60 grams per hour. Consuming > 60 g/hr of pure glucose leaves unabsorbed carbohydrates in the intestinal lumen, causing osmotic water influx and bloating.
   - Fructose is absorbed independently via the facilitative glucose transporter GLUT5.
   - Combining glucose (or maltodextrin) and fructose in a 2:1 or 1:0.8 ratio utilizes both transporters simultaneously, allowing carbohydrate absorption rates to reach 90 to 120 grams per hour with minimal GI distress."""
    },

    # -------------------------------------------------------------------------
    # Pillar 5: Sleep, Recovery, and Physical Activity
    # -------------------------------------------------------------------------
    {
        "doc_id": "P5_34_SLEEP_RESTRICTION_INSULIN",
        "section_title": "SLEEP RESTRICTION AND METABOLIC DYSFUNCTION: INSULIN RESISTANCE AND GLUT4",
        "source_id": "US-CDC-SLEEP-2022",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_ENDOCRINE",
        "text": """Sleep restriction provokes acute, profound metabolic derangements in peripheral glucose metabolism:
1. Impairment of Insulin Sensitivity:
   - Restricting sleep to 4 to 5 hours per night for just 4 consecutive days reduces whole-body insulin sensitivity by 30% to 40%, producing an acute metabolic state resembling clinical pre-diabetes.
2. Cellular Mechanisms in Skeletal Muscle:
   - Sleep debt elevates nocturnal sympathetic tone, sustaining elevated free fatty acid (FFA) concentrations in plasma. High FFAs induce intracellular insulin signaling defects:
     * Blunts the phosphorylation of Insulin Receptor Substrate 1 (IRS-1) and Akt.
     * Inhibits the translocation of glucose transporter type 4 (GLUT4) storage vesicles to the sarcolemma.
     * Myocytes fail to take up circulating glucose effectively in response to postprandial insulin surges.
3. Appetite Dysregulation:
   - Sleep loss suppresses circulating leptin (the satiety hormone) by 15% to 20% while elevating ghrelin (the orexigenic hunger hormone) by 25% to 30%, driving intense cravings for hyper-palatable, calorie-dense carbohydrates."""
    },
    {
        "doc_id": "P5_35_PERCUSSIVE_MASSAGE_THERAPY",
        "section_title": "PERCUSSIVE THERAPY AND FOAM ROLLING: NEUROSENSORY MODULATION VS TISSUE ALTERATION",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_RECOVERY_MODALITIES",
        "text": """Percussive massage guns and foam rollers are popular recovery tools; understanding their true physiological mechanism is essential for proper implementation:
1. The Mechanical Myth:
   - Dense human fascia (e.g., the iliotibial band / IT band) has tensile stiffness comparable to steel wire; producing even a 1% structural elongation requires mechanical forces exceeding 9,000 Newtons—far beyond what human therapists, foam rollers, or massage guns can exert. Foam rollers do not 'break up scar tissue' or physically lengthen fascia.
2. The True Neurosensory Mechanism (Gate Control Theory):
   - Mechanical vibration and rolling pressure stimulate low-threshold, rapidly adapting mechanoreceptors in the skin and subcutaneous fascia (Pacini and Meissner corpuscles) and Ruffini endings.
   - Large-diameter, myelinated sensory A-beta afferents transmit non-painful tactile and vibratory signals to the dorsal horn of the spinal cord.
   - These signals activate inhibitory interneurons that 'close the gate' against slower, unmyelinated pain signals carried by nociceptive C fibers (Melzack and Wall's Gate Control Theory of Pain).
   - The result is acute transient analgesia, reduced muscle tone, and increased pain pressure threshold lasting 15 to 30 minutes, facilitating greater active range of motion without impairing neuromuscular power output."""
    },

    # -------------------------------------------------------------------------
    # Pillar 6: Training Adaptations, Fatigue, and Load Management
    # -------------------------------------------------------------------------
    {
        "doc_id": "P6_33_FIBER_TYPE_OVERSHOOT",
        "section_title": "FIBER TYPE CONVERSIONS AND THE POST-TAPERING 'OVERSHOOT' PHENOMENON",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "training_adaptations_fatigue_load",
        "group_id": "GRP_P6_STRUCTURAL_ADAPTATIONS",
        "text": """Chronic resistance and endurance training induce predictable phenotypic shifts in skeletal muscle myosin heavy chain (MHC) gene expression:
1. Training Directionality (Type IIx to Type IIa):
   - Untrained individuals typically have roughly 10% to 15% pure, highly fatigable fast-glycolytic Type IIx fibers.
   - With regular resistance training, repetitive mechanical and metabolic stimuli trigger an almost universal down-regulation of pure MHC-IIx expression and an upregulation of the more fatigue-resistant fast-oxidative MHC-IIa phenotype.
   - After months of training, Type IIx fiber percentage typically drops to near zero (< 1%).
2. The Detraining / Tapering 'Overshoot' Phenomenon:
   - When training volume is drastically reduced during a structured 2- to 3-week taper or complete unloading period, a rapid transcriptional rebound occurs:
   - Muscle fibers rapidly revert from MHC-IIa back toward MHC-IIx. In fact, Type IIx expression often 'overshoots' baseline pre-training levels, reaching 15% to 25% of total fiber composition.
   - This surge in pure Type IIx fibers endows the muscle with exceptional maximal shortening velocity and explosive power output, providing the physiological foundation for peak athletic tapering."""
    },
    {
        "doc_id": "P6_34_INTERNAL_LOAD_TRIMP",
        "section_title": "BANISTER'S HEART RATE TRIMP: QUANTIFYING NON-LINEAR CARDIOVASCULAR STRAIN",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "training_adaptations_fatigue_load",
        "group_id": "GRP_P6_LOAD_MONITORING",
        "text": """Banister's Training Impulse (TRIMP) quantifies internal cardiovascular load by integrating workout duration with an exponential heart rate weighting factor:
1. Mathematical Equation:
   TRIMP (Arbitrary Units) = Duration (min) x Delta HR ratio x y
   Where:
   - Delta HR ratio = (HR_exercise - HR_rest) / (HR_max - HR_rest), representing fractional heart rate reserve.
   - y = Exponential weighting factor = 0.64 x e^(1.92 x Delta HR ratio) for males (and e^(1.67 x ratio) for females).
2. The Physiological Rationale for Exponential Weighting:
   - Exercising at 90% of heart rate reserve produces far more systemic metabolic fatigue, sympathetic nervous system drive, and glycogen depletion per minute than exercising at 50% of heart rate reserve.
   - Linear metrics falsely treat 60 minutes at 50% HRR as equal to 30 minutes at 100% HRR. The exponential weighting factor mathematically mirrors the exponential rise in blood lactate accumulation as exercise intensity exceeds the second ventilatory threshold."""
    },

    # -------------------------------------------------------------------------
    # Pillar 7: General Fitness Education and Age-Appropriate Safety
    # -------------------------------------------------------------------------
    {
        "doc_id": "P7_31_PREGNANCY_CONTRAINDICATIONS",
        "section_title": "PREGNANCY AND EXERCISE: ABSOLUTE VS RELATIVE CLINICAL CONTRAINDICATIONS",
        "source_id": "US-HHS-PAG-2018",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_SPECIAL_POPULATIONS",
        "text": """While physical activity is safe and strongly recommended for most pregnant women, certified fitness professionals and educational algorithms must recognize strict clinical boundaries:
1. Absolute Contraindications (Exercise Must NOT Be Performed):
   - Hemodynamically significant maternal heart disease.
   - Restrictive lung disease.
   - Incompetent cervix or cerclage placement.
   - Multiple gestation at risk for premature labor.
   - Persistent second- or third-trimester vaginal bleeding.
   - Placenta previa after 26 weeks of gestation.
   - Premature labor during the current pregnancy.
   - Ruptured amniotic membranes.
   - Preeclampsia or pregnancy-induced hypertension.
   - Severe maternal anemia.
2. Relative Contraindications (Requires Direct Obstetric Clearance):
   - Severe eating disorders or severe malnutrition.
   - Mild/moderate cardiovascular disease.
   - Uncontrolled type 1 diabetes, thyroid disease, or hypertension.
   - Extreme morbid obesity or extreme underweight (BMI < 12).
   - Recurrent pregnancy loss history."""
    },
    {
        "doc_id": "P7_32_OLDER_ADULT_POWER_TRAINING",
        "section_title": "HIGH-VELOCITY RESISTANCE TRAINING IN OLDER ADULTS: FALL PREVENTION DYNAMICS",
        "source_id": "US-NIH-NIA-EXERCISE",
        "topic_domain": "general_fitness_education_safety",
        "group_id": "GRP_P7_AGING_MUSCLE",
        "text": """In geriatric populations, muscle power (Force x Velocity) declines nearly twice as rapidly as maximal muscle strength (Force alone):
1. The Biomechanics of Fall Recovery:
   - When an older adult trips or catches a toe while walking, recovering balance requires taking a rapid, forceful recovery step within 100 to 200 milliseconds.
   - If muscular power and velocity of contraction are diminished, the individual cannot position the foot forward quickly enough to widen the base of support, resulting in a fall.
2. High-Velocity Resistance (Power) Training:
   - Protocol: Performing the concentric phase of resistance exercises (leg press, chair rises, chest press) as rapidly as possible at light-to-moderate loads (40% to 60% 1RM), followed by a controlled 2- to 3-second eccentric return.
   - Adaptations: Selectively recruits high-threshold Type II motor units, increases motor unit firing frequency, enhances rate of force development, and significantly outperforms slow-tempo resistance training in reducing clinical fall incidence."""
    }
]
