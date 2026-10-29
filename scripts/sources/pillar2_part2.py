"""Pillar 2 Part 2: Strength Training Principles and Programming (Expansion).

Authoritative educational documents drawn from public domain and open-access sources:
- Headquarters, Department of the Army (FM 7-22 Holistic Health and Fitness, Public Domain)
- Centers for Disease Control and Prevention (CDC Resistance Training Guidelines, Public Domain)
- NASA Human Research Program Evidence Book: Muscle Mass, Strength, and Endurance (Public Domain)
- OpenStax Anatomy and Physiology 2e (CC BY 4.0, Betts et al.)
"""

DOCUMENTS = [
    {
        "doc_id": "P2_26_MUSCLE_ARCHITECTURE_PCSA",
        "section_title": "MUSCLE ARCHITECTURE: PENNATION ANGLE AND PHYSIOLOGICAL CROSS-SECTIONAL AREA",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_MUSCLE_ARCHITECTURE",
        "text": """The maximum force-generating capacity of a skeletal muscle is determined primarily by its internal architectural arrangement rather than its anatomical volume alone:
1. Anatomical Cross-Sectional Area (ACSA) vs Physiological Cross-Sectional Area (PCSA):
   - ACSA is the cross-sectional area of a muscle cut perpendicular to its longitudinal anatomical axis.
   - PCSA is the total area of all muscle fibers cut perpendicular to their individual fiber orientation:
     PCSA = (Muscle Mass x cos(theta)) / (Muscle Density x Fiber Length)
     Where theta represents the pennation angle. PCSA directly correlates with maximal isometric force production (roughly 20 to 30 N/cm2 of specific tension).
2. Pennation Angle (theta): The angle between the longitudinal axis of individual muscle fibers and the central aponeurosis/tendon of pull.
   - Parallel / Fusiform Muscles (e.g., biceps brachii, sartorius): Pennation angle is near zero; fibers run parallel to the line of pull, optimizing contraction velocity and maximal shortening excursion.
   - Pennate Muscles (unipennate like tibialis posterior, bipennate like rectus femoris, multipennate like deltoid): Fibers insert at an angle to the tendon. This geometric arrangement allows a vastly greater packing density of sarcomeres within a given muscle volume, dramatically increasing total PCSA and peak force output at a minor trigonometric cosine force-transfer penalty.
3. Training Adaptations: Heavy resistance training increases both fiber diameter (hypertrophy) and pennation angle, further expanding total functional PCSA."""
    },
    {
        "doc_id": "P2_27_SAID_PRINCIPLE_DOMAINS",
        "section_title": "THE SAID PRINCIPLE: SPECIFIC ADAPTATIONS TO IMPOSED DEMANDS ACROSS THREE DOMAINS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_OVERLOAD",
        "text": """The Specific Adaptations to Imposed Demands (SAID) principle states that the human body adapts with high specificity to the exact biological, mechanical, and environmental stressors imposed upon it.
Specificity manifests across three distinct physiological domains:
1. Biomechanical Specificity: Adaptations are specific to the joint angles, range of motion, muscle action types (concentric, eccentric, isometric), and planes of motion trained:
   - Quarter squats produce peak force adaptations specifically in deep knee extension angles, transferring poorly to deep knee flexion angles.
   - Closed-kinetic-chain multi-joint lifts train intermuscular stabilization patterns that do not transfer directly from open-kinetic-chain isolated machine movements.
2. Neuromuscular Specificity: The central nervous system adapts specifically to the movement velocity, motor unit recruitment threshold, and rate of force development demanded by the exercise:
   - High-load low-velocity training maximizes maximal force output (1RM) through maximal motor unit recruitment.
   - Low-load high-velocity ballistic training maximizes explosive rate of force development and motor unit discharge frequency.
3. Metabolic Specificity: Adaptations in mitochondrial density, buffering capacity, and enzymatic activity occur specifically in the bioenergetic pathways stressed by the training work-to-rest intervals (phosphagen, fast glycolytic, or oxidative pathways)."""
    },
    {
        "doc_id": "P2_28_CLUSTER_SETS_PHYSIOLOGY",
        "section_title": "CLUSTER SET CONFIGURATIONS: INTRA-SET REST AND VELOCITY PRESERVATION",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_SET_CONFIGURATIONS",
        "text": """Cluster set configurations structure traditional continuous working sets by inserting short, standardized intra-set rest intervals (typically 15 to 45 seconds) between small clusters of repetitions (1 to 3 reps):
1. Traditional Set Structure: 1 set of 8 continuous repetitions (e.g., 8 reps at 75% 1RM), followed by 3 minutes of inter-set rest. As repetitions progress, metabolic byproducts accumulate, bar velocity drops by 30% to 50%, and mechanical form deteriorates.
2. Cluster Set Structure: The same 8 repetitions are performed as 4 clusters of 2 repetitions (2+2+2+2), separated by 20 seconds of intra-set rest, followed by 3 minutes between full sets.
3. Physiological Mechanisms of Advantage:
   - Phosphocreatine (PCr) Resynthesis: The 20-second intra-set buffer allows partial resynthesis of intramuscular PCr stores (which have a rapid recovery half-life of roughly 30 seconds), maintaining high ATP availability.
   - Neuromuscular Quality: Mean concentric barbell velocity and peak power output remain significantly higher throughout all repetitions, mitigating intra-set velocity loss.
   - Technical Consistency: Reduces fatigue-induced kinematics breakdown, preserving technical execution during complex barbell lifts (cleans, squats, bench press)."""
    },
    {
        "doc_id": "P2_29_VELOCITY_BASED_TRAINING",
        "section_title": "VELOCITY-BASED TRAINING (VBT): PROFILES, ZONES, AND AUTOREGULATION",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_VBT_AUTOREGULATION",
        "text": """Velocity-Based Training (VBT) utilizes real-time linear position transducers or optical cameras to measure concentric barbell velocity, providing an objective, autoregulated method for prescribing resistance training load and managing fatigue:
1. The Load-Velocity Relationship: In barbell exercises, there is an inverse linear relationship between external load (% 1RM) and mean concentric velocity (m/s). For example, in the back squat:
   - 100% 1RM (Minimum Velocity Threshold / MVT): ~0.30 m/s.
   - 80% 1RM: ~0.55 m/s.
   - 60% 1RM: ~0.80 m/s.
2. Daily Readiness Assessment: An athlete performs warm-up sets at a standardized submaximal load (e.g., 60% of estimated 1RM). If concentric velocity is 0.06 m/s above baseline, the athlete is primed, and working loads can be increased. If velocity is 0.06 m/s below baseline, residual fatigue is present, and working loads should be reduced.
3. Intra-Set Fatigue Cut-Offs: Instead of prescribing a fixed repetition target, the coach prescribes a velocity loss threshold:
   - 10% to 20% Velocity Loss: Optimizes maximal strength and power while minimizing metabolic fatigue and neuromuscular damage.
   - 30% to 40% Velocity Loss: Maximizes muscular hypertrophy by driving motor units deeper into metabolic fatigue, requiring longer recovery timelines."""
    },
    {
        "doc_id": "P2_30_ECCENTRIC_OVERLOAD_TITIN",
        "section_title": "ECCENTRIC OVERLOAD MECHANISMS AND TITIN STIFFNESS MODULATION",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_MUSCLE_ACTIONS",
        "text": """Eccentric muscle actions (active lengthening under load) produce uniquely potent neuromuscular, structural, and molecular adaptations that cannot be replicated by concentric actions alone:
1. Supramaximal Force Capacity: A muscle can resist approximately 20% to 40% more force during an eccentric action than it can produce during a maximal concentric action. This is achieved at lower metabolic energy cost (ATP consumption is 4 to 5 times lower during eccentric contractions).
2. The Winding Filament Theory and Titin: In addition to actin and myosin, the giant structural filament titin acts as a molecular spring. Upon calcium activation, titin's PEVK domain binds calcium, increasing its stiffness, and winding around the thin actin filament as cross-bridges rotate. This generates substantial passive mechanical force during lengthening, preventing sarcomere overextension.
3. Sarcomerogenesis in Series: Chronic eccentric overload forces sarcomeres to add in series along the length of the muscle fiber. Adding sarcomeres in series shifts the optimal length-tension relationship to longer muscle lengths, protecting the muscle against future strain injuries during eccentric stretch-shortening cycles."""
    },
    {
        "doc_id": "P2_31_ISOMETRIC_TRAINING_MODALITIES",
        "section_title": "ISOMETRIC TRAINING: OVERCOMING VS YIELDING ISOMETRICS AND ANGLE SPECIFICITY",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_MUSCLE_ACTIONS",
        "text": """Isometric muscle actions occur when contractile tension is generated without macroscopic changes in muscle-tendon unit length or joint angle:
1. Overcoming Isometrics (Concentric Isometrics): The lifter attempts to push or pull against an immovable external barrier (e.g., pulling a barbell into immovable safety pins).
   - Neuromuscular Drive: Stimulates maximal voluntary motor unit recruitment, firing rate, and maximal rate of force development (RFD).
2. Yielding Isometrics (Eccentric Isometrics): The lifter holds a submaximal or supramaximal load in a static position against gravity, actively resisting joint collapse (e.g., holding a paused squat or heavy barbell hold).
   - Fatigue Characteristics: Stimulates prolonged intramuscular ischemia, metabolic occlusion, and tendon stiffness adaptations.
3. Joint Angle Specificity: Isometric strength gains are specific to the joint angle at which the training occurs, with an overflow of approximately +/- 10 to 15 degrees. To build strength across a full range of motion, multi-angle isometric protocols (e.g., testing at 45, 90, and 120 degrees of joint articulation) are required."""
    },
    {
        "doc_id": "P2_32_REST_INTERVAL_PHYSIOLOGY",
        "section_title": "REST INTERVAL DURATION: METABOLIC RESTORATION VS VOLUME ACCUMULATION",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_REST_PERIODS",
        "text": """The duration of inter-set rest intervals profoundly influences metabolic recovery, subsequent repetition performance, and chronic neuromuscular adaptations:
1. Short Rest Intervals (30 to 60 seconds): Historically promoted for hypertrophy due to acute spikes in circulating growth hormone. However, exercise science demonstrates that transient acute endocrine spikes do not correlate with long-term hypertrophy. Short rest intervals impair performance on subsequent sets, causing significant repetition drops (e.g., 10 reps on set 1, dropping to 6 reps on set 2, and 4 reps on set 3 at constant load), reducing cumulative mechanical volume-load.
2. Long Rest Intervals (2.5 to 5 minutes): Allows near-complete phosphocreatine (PCr) resynthesis (~95% recovered within 3 minutes), restoration of intracellular pH, and clearance of central nervous system adenosine. Lifters can maintain target repetition counts and high mechanical tension across multiple working sets.
3. Clinical Summary: Meta-analyses demonstrate that longer rest intervals (>= 2 minutes for compound multi-joint lifts) result in superior muscle strength and equal or superior muscle hypertrophy compared to short rest intervals, solely through the facilitation of higher cumulative training volume."""
    },
    {
        "doc_id": "P2_33_UNDULATING_PERIODIZATION",
        "section_title": "DAILY AND WEEKLY UNDULATING PERIODIZATION (DUP / WUP) FRAMEWORKS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_PERIODIZATION",
        "text": """Undulating periodization introduces frequent, systematic fluctuations in training volume and intensity within a microcycle or mesocycle, preventing neurological accommodation:
1. Daily Undulating Periodization (DUP): Intensity and volume vary on a daily basis within the same week. For example, a lifter squatting 3 times per week might execute:
   - Monday (Hypertrophy Day): Moderate load (70% 1RM), 4 sets of 8 to 10 reps, 2 min rest.
   - Wednesday (Power / Speed Day): Light-to-moderate load (60% 1RM), 5 sets of 3 explosive reps, focus on bar speed.
   - Friday (Maximal Strength Day): Heavy load (85% to 90% 1RM), 4 sets of 3 reps, 3 to 5 min rest.
2. Weekly Undulating Periodization (WUP): Volume and intensity remain constant within a week but undulate from one week to the next (e.g., Week 1: 12 reps, Week 2: 8 reps, Week 3: 4 reps, Week 4: 10 reps).
3. Scientific Efficacy: DUP has repeatedly demonstrated superiority over classic linear periodization for intermediate and advanced lifters, primarily because multiple fitness qualities (hypertrophy, neuromuscular coordination, explosive power) are stimulated concurrently without allowing any quality to detrain."""
    },
    {
        "doc_id": "P2_34_BLOCK_PERIODIZATION_SYSTEM",
        "section_title": "BLOCK PERIODIZATION: ACCUMULATION, TRANSMUTATION, AND REALIZATION PHASES",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_PERIODIZATION",
        "text": """Developed by Vladimir Issurin, Block Periodization replaced traditional complex multi-target periodization with concentrated, sequential mesocycle blocks focused on minimal, highly compatible physiological targets:
1. Accumulation Block (2 to 4 weeks): Focuses on expanding morphological and aerobic foundations:
   - Primary Stimulus: High training volume, moderate intensity (60% to 75% 1RM).
   - Adaptations: Muscle hypertrophy, capillarization, connective tissue remodeling, and aerobic base expansion.
2. Transmutation Block (2 to 4 weeks): Converts the general adaptations into sport-specific athletic qualities:
   - Primary Stimulus: Moderate volume, high intensity (75% to 90% 1RM) performed under sport-specific velocity and fatigue conditions.
   - Adaptations: Maximal strength, rate of force development, anaerobic threshold, and movement-specific motor patterns.
3. Realization (Peaking) Block (8 to 14 days): Promotes rapid fatigue dissipation and neuromuscular peaking:
   - Primary Stimulus: Low volume (50% reduction), high intensity (>= 90% 1RM or competition pace), maximum recovery.
   - Adaptations: Full supercompensation, maximum motor unit firing rate, and competitive readiness."""
    },
    {
        "doc_id": "P2_35_VOLUME_DOSE_RESPONSE",
        "section_title": "WEEKLY SET VOLUME DOSE-RESPONSE RELATIONSHIPS IN HYPERTROPHY AND STRENGTH",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_VOLUME_DOSE",
        "text": """Weekly volume—quantified as the total number of challenging, hard sets (sets taken to within 0 to 3 RIR) per muscle group per week—exhibits a dose-response relationship characterized by diminishing marginal returns and an ultimate ceiling:
1. Tier 1: Maintenance Volume (< 5 sets/week): Sufficient to maintain existing muscular mass and strength in recreationally trained individuals, especially if intensity of effort is high.
2. Tier 2: Low-to-Moderate Volume (5 to 9 sets/week): Generates reliable strength and hypertrophic gains in novice and early intermediate lifters.
3. Tier 3: Optimal Overload Volume (10 to 20 sets/week): The evidence-based sweet spot for maximizing hypertrophic adaptations in intermediate to advanced lifters. Volume is distributed across 2 to 3 sessions per week to optimize per-session muscle protein synthesis stimulation.
4. Tier 4: Excessive Volume (> 20 to 25+ sets/week): Enters the zone of 'junk volume' where incremental muscle protein synthesis gains are negligible, but systemic fatigue, joint inflammation, and recovery time requirements rise exponentially.
Per-Session Ceiling: Performing more than 8 to 10 hard sets for a single muscle group in a single workout yields diminishing returns due to intracellular anabolic signaling saturation."""
    },
    {
        "doc_id": "P2_36_DETRAINING_MUSCLE_MEMORY",
        "section_title": "DETRAINING KINETICS AND THE PHYSIOLOGICAL MECHANISMS OF MUSCLE MEMORY",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_DETRAINING",
        "text": """Cessation of resistance training triggers physiological detraining; however, re-training previously trained muscle occurs significantly faster than initial adaptation—a phenomenon termed 'muscle memory'.
Biological timelines and cellular mechanisms:
1. Short-Term Detraining (1 to 3 weeks):
   - Muscular Strength: Highly maintained; minimal loss of maximal force output.
   - Glycogen and Water: Muscle cross-sectional area may appear to decrease rapidly (by 5% to 8%) within 7 to 14 days, but this is driven by intramuscular glycogen depletion and water loss rather than true myofibrillar contractile protein degradation.
2. Long-Term Detraining (4+ weeks):
   - Neurological Deconditioning: Reductions in central motor drive, motor unit recruitment threshold elevation, and decreased firing frequency occur first.
   - Myofibrillar Atrophy: Protein degradation exceeds protein synthesis, resulting in loss of contractile filaments and fiber diameter reduction.
3. The Cellular Mechanism of Muscle Memory: During initial hypertrophy, satellite cells proliferate and donate new nuclei (myonuclei) to growing muscle fibers to maintain the myonuclear domain size. Research demonstrates that during subsequent detraining and atrophy, these acquired myonuclei do not undergo apoptotic destruction; they remain permanently retained within the muscle syncytium. Upon re-training, these pre-existing myonuclei immediately resume high-volume protein transcription, restoring muscle mass in a fraction of the time."""
    },
    {
        "doc_id": "P2_37_AUTOREGULATION_RPE_VS_PERCENTAGES",
        "section_title": "AUTOREGULATION FRAMEWORKS: INTEGRATING RPE/RIR WITH PERCENTAGE-BASED PROGRAMS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_VBT_AUTOREGULATION",
        "text": """Rigid percentage-based programming (prescribing exact barbell loads based on a historical 1RM tested weeks prior) fails to account for daily biological fluctuations in neuromuscular readiness, sleep quality, and psychological stress.
Autoregulation adjusts training loads dynamically based on real-time daily capacity:
1. The 1RM Fluctuates Daily: An athlete's true daily 1RM fluctuates by +/- 5% to 10% on any given day based on systemic fatigue and recovery state. A prescribed 85% load on a day when capacity is 10% below normal effectively becomes a 95% near-maximal effort, distorting prescribed fatigue.
2. Integrating Percentages with RPE Stops:
   - Method 1 (Percentage with Target RIR): Prescribe '80% 1RM for 4 sets of 5 repetitions @ 2 RIR'. If the weight feels too heavy on set 2 (reaching 0 RIR), load is reduced by 3% to 5% to maintain the intended biological stimulus.
   - Method 2 (RPE Target with Top Single): The athlete works up to a single repetition at RPE 8 (roughly 90% of daily capacity). The working weight for the day's volume sets is then calculated as a fixed percentage (e.g., 80%) of that day's top single.
3. Objective Autoregulation: Combining subjective RIR targets with objective barbell velocity monitoring creates a closed-loop system ensuring exact physiological stimulus delivery."""
    }
]
