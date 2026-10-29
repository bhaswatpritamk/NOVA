"""Pillar 2: Strength Training Principles and Programming.

Authoritative educational documents drawn from public domain and open-access sources:
- Headquarters, Department of the Army (FM 7-22 and ATP 7-22.02, Public Domain)
- Centers for Disease Control and Prevention (CDC RTG guidelines, Public Domain)
- HHS Physical Activity Guidelines Advisory Committee Report (Public Domain)
"""

DOCUMENTS = [
    {
        "doc_id": "P2_01_PROGRESSIVE_OVERLOAD_PHYSIOLOGY",
        "section_title": "THE PHYSIOLOGICAL FOUNDATIONS OF PROGRESSIVE OVERLOAD",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_OVERLOAD",
        "text": """Progressive overload represents the foundational physiological principle governing all structured physical conditioning and resistance training adaptations.
Under the principle of homeostasis, human biological systems seek to maintain internal physiological equilibrium; when an external mechanical or metabolic stressor is encountered, the body adapts specifically to mitigate that stress during subsequent exposures.
For skeletal muscle tissue to undergo continual neuromuscular and hypertrophic remodeling, it must encounter mechanical stimuli that exceed the threshold to which it is currently accustomed.
If training loads, volume, or movement intensity remain static across successive training cycles, the adaptive biological stimulus attenuates, resulting in physiological stagnation (adaptation plateau).
At the cellular level, mechanical tension applied across the sarcomere stimulates mechanosensitive focal adhesion complexes and integrins embedded in the costameric sarcolemma.
This mechanical signal activates intracellular phosphorylation cascades, principally the mechanistic target of rapamycin complex 1 (mTORC1) pathway.
Upregulated mTORC1 signaling accelerates ribosomal translation of messenger RNA (mRNA) into new contractile myofibrillar proteins, shifting the balance of muscle protein turnover toward net positive accretion."""
    },
    {
        "doc_id": "P2_02_PROGRESSION_LOAD_ADVANCEMENT",
        "section_title": "PROGRESSION STRATEGIES: LOAD ADVANCEMENT AND PERCENTAGE TITRATION",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_OVERLOAD",
        "text": """Progressive overload can be operationalized through several distinct training variables, beginning with external load advancement.
Load progression involves systematically increasing the absolute external resistance (barbell, dumbbell, or machine load in kilograms or pounds) while holding repetition and set volume constant.
For example, an athlete performing 3 sets of 5 repetitions at 100 kg advances the load to 102.5 kg once all prescribed repetitions are successfully completed with technically sound movement quality.
A widely utilized practical implementation is the '2-for-2 rule':
If an athlete can complete two or more repetitions beyond the target repetition goal in the final set of an exercise for two consecutive training workouts, load should be increased in the subsequent session.
Typical load increments range from 2.5% to 5% (approximately 1 to 2.5 kg / 2.5 to 5 lb for upper-body isolation exercises, and 2.5 to 5 kg / 5 to 10 lb for multi-joint lower-body compound movements).
Attempting overly aggressive load increments frequently induces compensatory technical breakdown, increases joint shear stress, and elevates acute injury risk."""
    },
    {
        "doc_id": "P2_03_PROGRESSION_REPS_AND_SETS",
        "section_title": "PROGRESSION STRATEGIES: REPETITION RANGES AND SET ACCUMULATION",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_OVERLOAD",
        "text": """When absolute load increments are unavailable or when intermediate progression is desired, athletes utilize repetition and set volume titration.
A highly effective method is the double progression system within a specified repetition bracket, such as 3 sets of 8 to 12 repetitions:
1. The athlete selects a load with which they can achieve 8 repetitions across all working sets (e.g., 80 kg for 3 sets of 8 reps).
2. In subsequent sessions, the load remains fixed at 80 kg while the lifter attempts to add repetitions (e.g., 9, 8, 8 reps, advancing over multiple workouts to 12, 12, 12 reps).
3. Once the upper bound of the repetition bracket (3 sets of 12 reps) is successfully conquered with strict biomechanical form, the external load is advanced by 2.5% to 5%, resetting repetitions to the lower bound of 8 reps.
Set accumulation progression involves maintaining both load and repetition targets while adding working sets across weeks (e.g., progressing from 3 sets of 10 reps in week 1 to 4 sets in week 2 and 5 sets in week 3), incrementally driving adaptive weekly volume before introducing a deload."""
    },
    {
        "doc_id": "P2_04_PROGRESSION_TEMPO_AND_ROM",
        "section_title": "PROGRESSION STRATEGIES: TEMPO, ECCENTRIC DURATION, AND RANGE OF MOTION",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_OVERLOAD",
        "text": """Progressive overload can be achieved without increasing external load or repetition count through deliberate manipulation of movement tempo and Range of Motion (ROM).
Movement tempo is conventionally annotated as a four-digit code (e.g., 3-1-1-0):
- The first digit indicates the eccentric lowering duration in seconds (3 seconds).
- The second digit represents the isometric pause duration in the stretched transition position (1 second).
- The third digit denotes the concentric lifting phase duration (1 second or explosive X).
- The fourth digit indicates the isometric pause in the contracted lockout position (0 seconds).
Extending the eccentric lowering phase from 1 second to 3 or 4 seconds eliminates compensatory momentum, increases total Time Under Tension (TUT), and substantially elevates mechanical tension per repetition.
Similarly, progressing range of motion—such as increasing squat depth from above parallel to full hip-crease depth below the knee, or performing deficit deadlifts from a 2-inch elevated platform—forces muscle fibers to generate force through longer operating sarcomere lengths, stimulating longitudinal sarcomerogenesis."""
    },
    {
        "doc_id": "P2_05_PROGRESSION_REST_INTERVALS",
        "section_title": "PROGRESSION STRATEGIES: REST INTERVAL DENSITY AND METABOLIC STRESS",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_OVERLOAD",
        "text": """Training density represents the volume of work executed per unit of time: Density = Work Volume / Total Session Time.
Manipulating rest intervals between working sets serves as a distinct progression vector to target muscular endurance, metabolic conditioning, and cardiovascular recovery:
By systematically reducing passive rest intervals between sets (for example, reducing rest from 120 seconds down to 90, 75, and 60 seconds while preserving external load and repetition volume), the athlete imposes greater intracellular metabolic stress.
Metabolic stress is characterized by the accumulation of hydrogen ions (H+), inorganic phosphate (Pi), and lactate within active myocytes, paired with localized tissue hypoxia and transient vascular occlusion.
This metabolic milieu promotes the release of local autocrine and paracrine growth factors, stimulates cell swelling (cellular hydration that exerts mechanical pressure on the sarcolemma), and increases muscle fiber recruitment through fatigue of lower-threshold motor units.
Conversely, when maximal strength and power are the primary objectives, rest intervals should be lengthened (3 to 5 minutes) to ensure complete phosphocreatine replenishment and avoid premature peripheral fatigue."""
    },
    {
        "doc_id": "P2_06_INTENSITY_ZONES_MAXIMAL_STRENGTH",
        "section_title": "TRAINING INTENSITY ZONES: MAXIMAL STRENGTH (1 TO 5 REPETITIONS)",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_INTENSITY",
        "text": """Training intensity zones are categorized based on percentages of an individual's one-repetition maximum (1RM) and corresponding repetition targets.
The maximal strength zone encompasses loads between 85% and 100% of 1RM, typically permitting between 1 and 5 repetitions per set.
The primary physiological objective of this zone is maximal neural drive:
High mechanical tension requires the central nervous system to maximize motor unit recruitment across the entire available motoneuron pool, fire motor units at high discharge frequencies (rate coding), enhance motor unit synchronization, and downregulate autogenic Golgi tendon organ inhibitory reflexes.
Because neural adaptations predominate, maximal strength can improve with modest muscular hypertrophy in early phases.
Rest intervals of 3 to 5 minutes between sets are mandatory in this zone to permit 95% to 100% resynthesis of intracellular phosphocreatine (PCr) stores and restore central motor cortex drive.
Volume in this zone must be managed carefully: working sets are typically kept between 3 and 6 sets, as excessive high-intensity loading rapidly accumulates systemic central nervous system fatigue and joint connective tissue stress."""
    },
    {
        "doc_id": "P2_07_INTENSITY_ZONES_HYPERTROPHY",
        "section_title": "TRAINING INTENSITY ZONES: MUSCULAR HYPERTROPHY (6 TO 12 REPETITIONS)",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_INTENSITY",
        "text": """The muscular hypertrophy zone encompasses external loads between 65% and 85% of 1RM, conventionally allowing between 6 and 12 repetitions per set.
This zone is widely recognized as the most efficient compromise for maximizing structural muscle tissue cross-sectional area:
It applies sufficiently high mechanical tension across sarcomeres to recruit high-threshold motor units under Henneman's size principle, while simultaneously generating substantial metabolic stress and adequate time under tension (typically 20 to 45 seconds per working set).
The combination of high mechanical strain, microcellular sarcomeric disruption, and metabolite accumulation provides an optimal intracellular trigger for mTORC1 pathway activation and muscle protein synthesis.
Rest intervals in the hypertrophy zone typically range from 2 to 3 minutes for multi-joint compound movements (such as squats, presses, and rows) and 60 to 90 seconds for single-joint isolation exercises.
While muscular hypertrophy can be induced across a wide spectrum of repetition ranges (from 5 up to 30 repetitions) provided sets are taken sufficiently close to muscular failure, the 6 to 12 rep zone provides superior efficiency per unit of training time."""
    },
    {
        "doc_id": "P2_08_INTENSITY_ZONES_ENDURANCE",
        "section_title": "TRAINING INTENSITY ZONES: MUSCULAR ENDURANCE (15+ REPETITIONS)",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_INTENSITY",
        "text": """The muscular endurance zone utilizes loads below 65% of 1RM, allowing 15, 20, or more continuous repetitions per set.
The physiological objective of muscular endurance training is enhancing the ability of skeletal muscle to resist fatigue during repeated submaximal contractions against external resistance.
Cellular adaptations in this zone target bioenergetic economy and substrate delivery:
Muscle fibers increase capillary density around contracting myocytes, elevate intramuscular mitochondrial volume and oxidative enzyme activity, and upregulate intracellular buffering capacity (including carnosine and bicarbonate buffers) to neutralize hydrogen ion (H+) accumulation.
Rest intervals in this zone are intentionally brief (typically 30 to 60 seconds), keeping cardiovascular output and metabolic clearance pathways elevated.
While low-load training to failure can stimulate hypertrophy in both Type I and Type II fibers comparable to heavier training, it generates substantial perceived discomfort, elevated ratings of perceived exertion, and prolonged neuromuscular recovery timelines due to peripheral calcium release impairment."""
    },
    {
        "doc_id": "P2_09_NEURAL_ADAPTATIONS_EARLY_PHASE",
        "section_title": "NEUROLOGICAL ADAPTATIONS DURING EARLY-PHASE RESISTANCE TRAINING",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_ADAPTATIONS",
        "text": """During the initial 4 to 8 weeks of resistance training in previously untrained individuals, dramatic increases in muscular strength occur with negligible changes in macroscopic muscle fiber cross-sectional area.
These early-phase strength gains are mediated almost entirely by neurological adaptations within the central and peripheral nervous systems:
1. Increased motor unit recruitment: The motor cortex develops the capacity to recruit a larger percentage of the available motor unit pool in agonist muscles during maximal voluntary contraction.
2. Enhanced rate coding: The firing frequency of active motor units increases, accelerating the rate of force development (RFD).
3. Motor unit synchronization: Motor units discharge more synchronously at the onset of contraction, delivering rapid mechanical power.
4. Decreased antagonist co-activation: Electromyographic (EMG) studies demonstrate that the nervous system selectively inhibits opposing antagonist muscle groups (e.g., reducing hamstring co-contraction during quadriceps-dominant leg extensions), decreasing internal mechanical resistance.
5. Improved intermuscular coordination: Enhanced synergy among prime movers, synergists, and stabilizers allows smoother, more efficient force transfer along the kinetic chain."""
    },
    {
        "doc_id": "P2_10_STRUCTURAL_HYPERTROPHY_MODES",
        "section_title": "STRUCTURAL MUSCLE ADAPTATIONS: MYOFIBRILLAR VS SARCOPLASMIC HYPERTROPHY",
        "source_id": "OPENSTAX-AP-MUSCLE",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P2_ADAPTATIONS",
        "text": """Beyond the initial neural adaptation phase, chronic progressive resistance training induces macroscopic skeletal muscle hypertrophy through structural remodeling of individual myocytes.
Exercise physiology distinguishes between two interconnected modes of muscular hypertrophy:
1. Myofibrillar hypertrophy: Characterized by the synthesis and addition of new contractile protein filaments (actin, myosin, troponin, tropomyosin) inside the myocyte.
Contractile proteins are added both in parallel (increasing the cross-sectional area and packing density of individual myofibrils, directly raising peak force generation capacity) and in series (adding sarcomeres along the length of myofibrils, particularly in response to high-tension eccentric loading).
2. Sarcoplasmic hypertrophy: Characterized by the expansion of non-contractile cellular components within the cytoplasm, including glycogen granules, intracellular water, metabolic enzymes, and the sarcoplasmic reticulum.
While sarcoplasmic expansion increases total muscle volume, it does not proportionally increase maximal isometric force output.
In living human athletes, both forms of hypertrophy occur concurrently as a unified physiological adaptation to heavy resistance training, with mechanical tension predominantly driving myofibrillar accretion and high-volume metabolic stress augmenting sarcoplasmic storage."""
    },
    {
        "doc_id": "P2_11_RPE_AND_RIR_FRAMEWORKS",
        "section_title": "AUTOREGULATION FRAMEWORKS: REPETITIONS IN RESERVE AND THE RPE SCALE",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_AUTOREGULATION",
        "text": """Traditional percentage-based programming (prescribing exact loads based on a previously tested 1RM) fails to account for daily fluctuations in neuromuscular readiness, sleep quality, psychological stress, and systemic fatigue.
To address this limitation, modern strength science utilizes autoregulation frameworks based on Repetitions in Reserve (RIR) and the modified Borg Rating of Perceived Exertion (RPE) scale:
The RPE scale ranges from 1 to 10, directly anchored to proximity to momentary muscular failure:
- RPE 10: Absolute maximum effort; zero additional repetitions could be completed (0 RIR).
- RPE 9.5: No additional repetitions possible, but a minor load increment could have been moved.
- RPE 9: 1 repetition remaining in reserve before failure (1 RIR).
- RPE 8.5: Definitely 1 repetition remaining, possibly 2.
- RPE 8: 2 repetitions remaining in reserve (2 RIR).
- RPE 7: 3 repetitions remaining in reserve; bar velocity is brisk (3 RIR).
- RPE 6: Warm-up weight; 4 or more repetitions remaining in reserve.
By prescribing training sets as '3 sets of 8 reps @ RPE 8' (or 2 RIR), the athlete adjusts the day's barbell load to reflect their actual real-time physiological capacity, matching the target stimulus without overshooting into excessive fatigue."""
    },
    {
        "doc_id": "P2_12_FAILURE_VS_NON_FAILURE",
        "section_title": "EVIDENCE EVALUATION: TRAINING TO FAILURE VERSUS NON-FAILURE PROXIMITY",
        "source_id": "US-HHS-PAGAC-2018",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_AUTOREGULATION",
        "text": """A persistent debate in exercise programming concerns whether sets must be taken to absolute momentary muscular failure (0 RIR) to stimulate maximal strength and muscular hypertrophy.
Comprehensive systematic reviews and meta-analyses in exercise science demonstrate that training to momentary muscular failure on every working set is not necessary to maximize muscle hypertrophy and may be counterproductive:
When working sets are performed within 1 to 3 repetitions of failure (RPE 7 to 9 / RIR 1 to 3), the degree of muscle fiber recruitment and hypertrophic signaling is statistically equivalent to sets taken to complete failure.
Importantly, terminating sets with 1 to 3 RIR confers major physiological advantages:
1. Systemic fatigue and central nervous system depletion are reduced by 30% to 50%, allowing higher aggregate training volume across the microcycle.
2. Muscle damage (sarcolemmal microtrauma and creatine kinase leakage) is substantially moderated, accelerating recovery timelines back to 24 to 48 hours.
3. The risk of acute compensatory biomechanical breakdown during multi-joint lifts (such as lumbar flexion in the deadlift or knee valgus in the squat) is minimized.
Training to absolute failure should be reserved sparingly for single-joint isolation exercises (e.g., bicep curls, lateral raises) on the final set of a training session."""
    },
    {
        "doc_id": "P2_13_WEEKLY_VOLUME_SWEET_SPOT",
        "section_title": "TRAINING VOLUME QUANTIFICATION: THE 10 TO 20 WEEKLY SET SWEET SPOT",
        "source_id": "US-CDC-RTG-2023",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_VOLUME",
        "text": """Training volume is the primary driver of resistance training adaptations, conventionally quantified as the number of 'hard sets' (sets performed within 1 to 3 RIR of failure) performed per muscle group per week.
Extensive dose-response research establishes an inverted-U relationship between weekly set volume and muscular hypertrophy:
- Minimum Effective Dose: In untrained or recreational individuals, performing as few as 1 to 4 hard sets per muscle group per week is sufficient to produce measurable strength and hypertrophic gains.
- Optimal Adaptive Range: For trained athletes seeking to maximize muscle accretion, empirical evidence demonstrates an optimal sweet spot of 10 to 20 hard working sets per muscle group per week.
- Exceeding Maximum Recoverable Volume (MRV): Progressing volume beyond 20 to 25 weekly sets per muscle group typically yields diminishing marginal returns and eventually negative adaptations.
Excessive set volume generates junk volume—sets performed in a state of high fatigue where motor unit recruitment is compromised and mechanical tension per fiber is reduced—leading to non-functional overreaching, chronic connective tissue inflammation, and delayed recovery."""
    },
    {
        "doc_id": "P2_14_TRAINING_FREQUENCY_MPS",
        "section_title": "TRAINING FREQUENCY AND THE MUSCLE PROTEIN SYNTHESIS TIME COURSE",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_FREQUENCY",
        "text": """Training frequency describes how often a muscle group or movement pattern is trained within a given weekly microcycle.
In untrained individuals, a single bout of resistance training elevates Muscle Protein Synthesis (MPS) for up to 48 to 72 hours post-exercise.
However, in experienced, resistance-trained athletes, the temporal window of elevated MPS is significantly compressed, typically peaking at 12 to 24 hours post-workout and returning to baseline within 24 to 36 hours.
Consequently, partitioning weekly training volume across higher frequencies—training each muscle group 2 to 3 times per week rather than concentrating all volume into a single weekly session—offers distinct physiological advantages:
Distributing 12 weekly sets into two sessions of 6 sets (or three sessions of 4 sets) maintains higher movement quality, greater bar velocity, and higher average mechanical tension across every working set.
Conversely, cramming 12 to 15 sets into a single 'body-part split' workout results in progressive intra-session fatigue, wherein sets 8 through 15 suffer significant load decrements and technical deterioration."""
    },
    {
        "doc_id": "P2_15_SPLIT_FULL_BODY",
        "section_title": "WORKOUT SPLIT ARCHITECTURE: FULL-BODY 3-DAY ROUTINES",
        "source_id": "US-CDC-RTG-2023",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_SPLITS",
        "text": """Workout split architecture organizes training days and exercise selections to achieve balanced volume distribution and adequate recovery across the weekly microcycle.
A full-body training split schedules 2 to 3 non-consecutive workout sessions per week (e.g., Monday, Wednesday, Friday), with each session targeting all major muscle groups:
A typical full-body workout comprises 4 to 6 multi-joint compound exercises:
1. One lower-body knee-dominant movement (e.g., barbell back squat or leg press).
2. One lower-body hip-dominant movement (e.g., Romanian deadlift or kettlebell swing).
3. One upper-body horizontal pressing movement (e.g., barbell bench press or push-up).
4. One upper-body horizontal pulling movement (e.g., bent-over barbell row or cable row).
5. One vertical pressing or pulling movement (e.g., overhead press or pull-up).
6. Core stabilization or isolation accessory work.
Full-body splits are exceptionally time-efficient for general fitness, novice lifters, and busy professionals: they stimulate muscle protein synthesis across all muscle groups three times weekly, provide 48 hours of complete recovery between bouts, and minimize severe delayed onset muscle soreness (DOMS)."""
    },
    {
        "doc_id": "P2_16_SPLIT_UPPER_LOWER",
        "section_title": "WORKOUT SPLIT ARCHITECTURE: UPPER/LOWER 4-DAY SPLITS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_SPLITS",
        "text": """The Upper/Lower training split divides workouts into dedicated upper-body days and lower-body days, typically programmed across a 4-day weekly schedule (e.g., Monday: Upper A, Tuesday: Lower A, Thursday: Upper B, Friday: Lower B).
This architecture provides an ideal balance of volume, intensity, and recovery for intermediate and advanced lifters:
Upper-body sessions train the pectoralis major, anterior and lateral deltoids, latissimus dorsi, rhomboids, trapezius, and arm musculature (biceps and triceps) through alternating pressing and pulling movements.
Lower-body sessions train the quadriceps, hamstrings, gluteus maximus, calves, and lumbar erectors through squats, deadlifts, lunges, and hip thrusts.
Key advantages of the Upper/Lower split include:
1. High frequency: Each muscle group is trained twice per week, maintaining elevated muscle protein synthesis throughout the microcycle.
2. Complete local recovery: The upper body rests completely while the lower body trains, and vice versa, providing 72 to 96 hours of recovery between sessions for the same muscle group.
3. Manageable session duration: Dividing volume across 4 days keeps individual workouts between 45 and 60 minutes, limiting excessive intra-session glycogen depletion and mental fatigue."""
    },
    {
        "doc_id": "P2_17_SPLIT_PUSH_PULL_LEGS",
        "section_title": "WORKOUT SPLIT ARCHITECTURE: PUSH/PULL/LEGS 6-DAY SPLITS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_SPLITS",
        "text": """The Push/Pull/Legs (PPL) split organizes exercises according to functional anatomical movement synergies across a 3-day cycle, repeated once or twice weekly:
- Push Day: Targets upper-body pushing musculature—pectoralis major, anterior deltoids, and triceps brachii—using bench presses, overhead presses, incline dumbbell presses, dips, and triceps pushdowns.
- Pull Day: Targets upper-body pulling musculature—latissimus dorsi, middle/lower trapezius, rhomboids, posterior deltoids, and biceps brachii—using barbell rows, pull-ups, face pulls, and dumbbell curls.
- Legs Day: Targets lower-body musculature—quadriceps, hamstrings, gluteus maximus, and gastrocnemius/soleus—using squats, Romanian deadlifts, split squats, and calf raises.
When executed as a 6-day split (Push/Pull/Legs/Rest/Push/Pull/Legs), PPL accommodates high total weekly set volumes (15 to 22 sets per muscle group).
However, the demanding frequency requires exceptional attention to nutritional surplus, sleep hygiene (8+ hours nightly), and autoregulated fatigue monitoring to prevent systemic overreaching."""
    },
    {
        "doc_id": "P2_18_PERIODIZATION_CONCEPTS",
        "section_title": "PRINCIPLES OF PERIODIZATION: MANAGING FITNESS AND FATIGUE CYCLES",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_PERIODIZATION",
        "text": """Periodization is the systematic, cyclical planning of training variables (volume, intensity, frequency, exercise selection) designed to maximize specific physical adaptations while minimizing the risk of overtraining syndrome and athletic stagnation.
Periodization structures training across hierarchical temporal divisions:
1. Multi-Year Plan: A long-range development plan spanning 2 to 4 years (e.g., an Olympic quadrennial cycle).
2. Macrocycle: The overarching annual training plan, typically lasting 6 to 12 months, leading to a peak athletic competition or primary goal.
3. Mesocycle: A discrete training phase lasting 3 to 8 weeks, dedicated to a specific physiological adaptation (e.g., hypertrophy mesocycle, maximal strength mesocycle, power/peaking mesocycle).
4. Microcycle: The immediate short-term training block, typically lasting 7 days (one calendar week), detailing daily workouts and recovery intervals.
5. Training Session: The single daily workout composed of warm-up, core training blocks, and cool-down.
By varying the training stimulus across mesocycles, periodization exploits Selye's General Adaptation Syndrome, ensuring that periods of high fatigue are systematically balanced by recovery phases that yield supercompensation."""
    },
    {
        "doc_id": "P2_19_LINEAR_PERIODIZATION",
        "section_title": "PERIODIZATION MODELS: CLASSIC LINEAR PROGRESSION",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_PERIODIZATION",
        "text": """Classic linear periodization (traditionally attributed to Soviet sports scientist Leonid Matveyev) structures training through an inverse relationship between volume and intensity over time:
The model progresses sequentially from high initial training volume paired with low intensity toward low training volume paired with high intensity:
- Phase 1 (General Preparation / Hypertrophy): Weeks 1 to 4 utilize high volume (4 to 5 sets of 10 to 15 reps) at 60% to 70% 1RM to build muscular cross-sectional area, work capacity, and connective tissue resilience.
- Phase 2 (Basic Strength): Weeks 5 to 8 shift to moderate volume (3 to 4 sets of 5 to 8 reps) at 75% to 85% 1RM, converting structural hypertrophy into enhanced force production.
- Phase 3 (Strength / Power): Weeks 9 to 12 progress to low volume (3 to 5 sets of 2 to 4 reps) at 85% to 95% 1RM, maximizing motor unit recruitment and rate coding.
- Phase 4 (Peaking / Realization): Weeks 13 to 14 reduce volume drastically while performing 1 to 2 maximal reps (>95% 1RM) prior to competition.
Linear periodization is highly effective for peaking for a single targeted event, though it can lead to decay of earlier adaptations (e.g., losing hypertrophy during extended peaking phases)."""
    },
    {
        "doc_id": "P2_20_UNDULATING_PERIODIZATION",
        "section_title": "PERIODIZATION MODELS: DAILY UNDULATING PERIODIZATION (DUP)",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_PERIODIZATION",
        "text": """Daily Undulating Periodization (DUP) addresses the limitation of linear periodization by varying volume and intensity from session to session within the same weekly microcycle, rather than across multi-month phases.
In a classic 3-day DUP schedule for the primary compound lifts (squat, bench press, deadlift):
- Day 1 (Hypertrophy Day): 4 sets of 8 to 10 repetitions @ 70% to 75% 1RM with 2 minutes rest, emphasizing metabolic stress and work capacity.
- Day 2 (Strength Day): 4 sets of 4 to 6 repetitions @ 80% to 85% 1RM with 3 minutes rest, emphasizing mechanical tension and neural drive.
- Day 3 (Power / Speed Day): 5 sets of 2 to 3 repetitions @ 60% to 65% 1RM performed with maximal concentric velocity, emphasizing rate of force development.
Scientific comparisons between linear and undulating periodization consistently show that DUP produces equivalent or superior maximal strength gains in trained lifters:
By continually oscillating between intensity zones, DUP prevents neuromuscular accommodation, maintains all physical qualities simultaneously without decay, and provides greater psychological variety."""
    },
    {
        "doc_id": "P2_21_BLOCK_PERIODIZATION",
        "section_title": "PERIODIZATION MODELS: BLOCK PERIODIZATION AND RESIDUAL TRAINING EFFECTS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_PERIODIZATION",
        "text": """Block periodization (pioneered by sports scientists Vladimir Issurin and Yuri Verkhoshansky) organizes training into concentrated, highly focused mesocycle blocks of 2 to 4 weeks duration.
Each block focuses on a minimal number of compatible targeted abilities, exploiting the biological concept of the 'residual training effect'—the retention of physiological adaptations after the cessation of training:
1. Accumulation Block (2 to 4 weeks): Concentrated high-volume, low-intensity training targeting basic motor qualities, aerobic capacity, structural hypertrophy, and movement technique.
2. Transmutation Block (2 to 4 weeks): Concentrated specialized training at moderate volume and high intensity (75% to 90% 1RM), transforming generalized structural gains into sport-specific strength and anaerobic endurance.
3. Realization Block (1 to 2 weeks): Low-volume peaking and tapering phase (loads >90% 1RM, long rest), dissipating accumulated fatigue while realizing maximal neuromuscular power.
Because residual effects for aerobic capacity (30 +/- 5 days) and maximal strength (30 +/- 5 days) persist longer than peak power (5 +/- 3 days), block periodization allows athletes to stack multiple successive peaks throughout a competitive season."""
    },
    {
        "doc_id": "P2_22_DELOAD_PROGRAMMING",
        "section_title": "THE DELOAD MICROCYCLE: PHYSIOLOGICAL MECHANISMS AND PROTOCOLS",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_DELOAD",
        "text": """A deload is a planned, temporary reduction in overall training stress designed to dissipate accumulated neuromuscular fatigue, permit connective tissue remodeling, and facilitate supercompensation.
During demanding multi-week training blocks, fatigue masks physical fitness: while underlying physiological adaptations are occurring, elevated central fatigue, joint inflammation, and glycogen depletion degrade observable performance.
A structured deload should be programmed every 4 to 8 weeks, or introduced proactively when subjective readiness metrics (grip strength, morning HRV, sleep quality, joint ache) indicate accumulated overreaching.
The standard empirical deload protocol modifies training variables as follows:
- Training Volume: Reduced by 40% to 50% (e.g., executing 2 working sets per exercise instead of 4).
- Training Intensity: Maintained at moderate-to-high levels (70% to 80% 1RM, or roughly RPE 6 to 7), avoiding heavy singles to failure.
Maintaining intensity preserves motor unit recruitment patterns and neuromuscular familiarity with loads, while the drastic volume cut slashes systemic fatigue.
Athletes emerge from a properly executed deload with restored endocrine balance, normalized autonomic tone, and renewed strength capacity."""
    },
    {
        "doc_id": "P2_23_EXERCISE_SELECTION_ORDER",
        "section_title": "EXERCISE SELECTION HIERARCHY AND INTRA-SESSION ORDERING RULES",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_EXERCISE_SELECTION",
        "text": """The ordering of exercises within a resistance training session significantly impacts technical safety, mechanical power output, and total volume load.
Evidence-based strength training follows a strict hierarchical ordering principle:
1. Power and Explosive Movements First: Olympic lifts (snatches, cleans, jerks), plyometric jumps, and medicine ball throws demand maximal rate of force development and complex neuromuscular coordination; they must be executed first when the central nervous system is fully rested.
2. Multi-Joint Compound Structural Lifts Second: Heavy bilateral compound movements involving large muscle masses (barbell squats, deadlifts, bench presses, overhead presses) should precede isolation movements. Performing isolation work beforehand pre-exhausts synergistic stabilizers, compromising spinal and joint control during heavy compound loading.
3. Assistance and Supplemental Exercises Third: Secondary compound and unilateral movements (Romanian deadlifts, lunges, dumbbell presses, rows, pull-ups) follow primary strength work.
4. Single-Joint Isolation and Core Work Last: Bicep curls, tricep extensions, lateral raises, and direct abdominal stabilization work are performed at the end of the session, where local fatigue does not compromise structural joint stability."""
    },
    {
        "doc_id": "P2_24_BILATERAL_DEFICIT_UNILATERAL",
        "section_title": "THE BILATERAL DEFICIT AND UNILATERAL RESISTANCE TRAINING",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_EXERCISE_SELECTION",
        "text": """The bilateral deficit describes the physiological phenomenon whereby the maximal force generated by two limbs contracting simultaneously is less than the mathematical sum of the forces produced by each limb contracting unilaterally:
Force(Bilateral) < Force(Left Unilateral) + Force(Right Unilateral).
For example, an athlete who can execute a single-leg Bulgarian split squat with 50 kg in each hand (100 kg total external load per leg) may only back squat 170 kg bilaterally, rather than 200 kg.
The neurological basis of the bilateral deficit involves neural inhibition across the corpus callosum and interhemispheric motor cortex during simultaneous bilateral motor commands, alongside balance and stability constraints.
Integrating unilateral resistance training (Bulgarian split squats, single-leg Romanian deadlifts, single-arm dumbbell presses) into a comprehensive program confers major training benefits:
1. It eliminates inter-limb strength asymmetries, reducing unilateral injury risk.
2. It recruits deep stabilizing musculature (e.g., gluteus medius, quadratus lumborum) that remains under-stimulated in bilateral machines.
3. It exposes the spine to reduced total compressive load while imposing massive unilateral mechanical tension on active muscle fibers."""
    },
    {
        "doc_id": "P2_25_ACCOMMODATING_RESISTANCE",
        "section_title": "ACCOMMODATING RESISTANCE: VARIABLE RESISTANCE WITH BANDS AND CHAINS",
        "source_id": "US-ARMY-ATP-7-22",
        "topic_domain": "strength_training_programming",
        "group_id": "GRP_P2_VARIABLE_RESISTANCE",
        "text": """Conventional barbell training applies a constant gravitational resistance load throughout the movement; however, due to shifting musculoskeletal lever arms, human force-producing capacity varies continuously across the joint range of motion (the ascending strength curve).
In the barbell squat and bench press, an athlete is mechanically weakest at the bottom transition point (the sticking point) and mechanically strongest near complete lockout.
Accommodating resistance incorporates elastic resistance bands or heavy suspended steel chains attached to the barbell to match the external resistance to the human strength curve:
With chains, as the lifter descends into the bottom of a squat, chain links coil onto the floor, reducing the effective load at the biomechanically vulnerable sticking point; as the lifter ascends toward lockout, chain links lift off the floor, progressively increasing the load.
With elastic bands, resistance increases linearly in accordance with Hooke's law (Force = k x delta_x), forcing the athlete to accelerate forcefully through the entire concentric phase rather than decelerating near lockout.
Accommodating resistance enhances rate of force development (RFD), reduces joint stress in extreme stretched positions, and provides potent neurological stimulus for explosive strength athletes."""
    }
]
