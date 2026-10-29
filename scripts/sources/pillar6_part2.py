"""Pillar 6 Part 2: Training Adaptations, Fatigue, and Load Management (Expansion).

Authoritative educational documents drawn from public domain and open-access sources:
- Headquarters, Department of the Army (FM 7-22 Holistic Health and Fitness, Public Domain)
- National Aeronautics and Space Administration (NASA Human Research Program, Public Domain)
- OpenStax Anatomy and Physiology 2e (CC BY 4.0, Betts et al.)
- U.S. Department of Health and Human Services (PAGAC Scientific Report, Public Domain)
"""

DOCUMENTS = [
    {
        "doc_id": "P6_25_SUPERCOMPENSATION_TIMELINES",
        "section_title": "SUPERCOMPENSATION DYNAMICS: TEMPORAL DISPARITIES ACROSS BIOLOGICAL SYSTEMS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "training_adaptations_fatigue_load",
        "group_id": "GRP_P6_ADAPTATION_MODELS",
        "text": """Supercompensation—the adaptive rebound of physiological capacity above pre-stressor baseline—does not unfold at a uniform biological rate across organ systems:
1. Energetic Restoration (12 to 48 hours):
   - Intramuscular phosphocreatine (PCr) stores replenish rapidly (complete recovery within 5 to 15 minutes post-exercise).
   - Glycogen stores replenish within 24 to 48 hours when carbohydrate intake is adequate (5 to 8 g/kg/day).
2. Contractile Protein Synthesis and Hypertrophy (36 to 72 hours):
   - Muscle protein synthesis (MPS) rates peak between 12 and 24 hours post-workout and return to baseline around 36 to 48 hours. Structural repair of damaged sarcomeric Z-discs and myofilament synthesis requires 48 to 72 hours.
3. Central Nervous System and Autonomic Recovery (24 to 72+ hours):
   - Spinal motoneuron excitability and motor cortex corticospinal drive recover within 24 to 48 hours after submaximal training; however, high-volume eccentric training or maximal 1RM attempts can suppress central motor drive for 72 to 96 hours.
4. Dense Connective Tissue Remodeling (72 to 120+ hours):
   - Collagen synthesis in tendons, ligaments, and osteocytes peaks between 48 and 72 hours, but complete matrix cross-linking and remodeling requires multiple days. Training the same movement pattern too frequently can outpace connective tissue healing."""
    },
    {
        "doc_id": "P6_26_RATE_FORCE_DEVELOPMENT",
        "section_title": "RATE OF FORCE DEVELOPMENT (RFD): EARLY NEURAL VS LATE STRUCTURAL DETERMINANTS",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "training_adaptations_fatigue_load",
        "group_id": "GRP_P6_NEUROMUSCULAR_RFD",
        "text": """Rate of Force Development (RFD)—the rate at which contractile force rises during the initial phase of muscle action (Delta Force / Delta Time)—is a critical determinant of explosive athletic performance:
1. Early Phase RFD (< 100 ms from contraction onset):
   - In most athletic movements (sprinting ground contact times: 80 to 100 ms; Olympic barbell change-of-direction: 100 to 150 ms), the muscle does not have enough time to reach peak maximal force (which requires 300 to 400 ms).
   - Early RFD is governed almost exclusively by neural mechanisms:
     * Motor unit recruitment velocity: Firing frequency (doublet firing of > 100 Hz at contraction onset).
     * Maximal central motor drive and synchronized motoneuron discharge.
2. Late Phase RFD (> 200 ms from contraction onset):
   - Governed by morphological and architectural characteristics:
     * Muscle cross-sectional area (PCSA) and maximal absolute strength (1RM).
     * Tendon stiffness: Stiffer tendons transmit myofilament force instantly to the skeleton without mechanical lag.
     * Myosin heavy chain (MHC) isoform distribution: Higher percentage of fast-twitch Type IIx and IIa fibers increases cross-bridge cycling velocity."""
    },
    {
        "doc_id": "P6_27_SARCOPLASMIC_VS_MYOFIBRILLAR",
        "section_title": "SARCOPLASMIC VS MYOFIBRILLAR HYPERTROPHY: ULTRASTRUCTURAL REALITIES",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "training_adaptations_fatigue_load",
        "group_id": "GRP_P6_STRUCTURAL_ADAPTATIONS",
        "text": """Skeletal muscle hypertrophy encompasses two ultrastructural adaptations that can occur in varying proportions:
1. Myofibrillar Hypertrophy:
   - Characterized by an increase in the size and number of contractile myofibrils (actin and myosin protein filaments) packed within the myocyte.
   - Increases the specific tension of the muscle (force produced per unit of cross-sectional area).
   - Stimulated primarily by high-load mechanical tension (> 75% 1RM) and progressive resistance training.
2. Sarcoplasmic Hypertrophy:
   - Characterized by an expansion of the non-contractile elements within the muscle fiber, including the sarcoplasmic fluid, glycogen stores, sarcoplasmic reticulum, and metabolic enzymes.
   - Cross-sectional muscle volume increases without a proportional increase in maximal isometric force production, reducing specific tension.
   - Stimulated by higher-repetition, fatigue-oriented training (15 to 25+ reps) that places high metabolic demands on intracellular glycolytic pathways and glycogen storage capacity.
3. Physiological Synergy: In practical athletic training, pure isolated sarcoplasmic or myofibrillar hypertrophy does not occur; all progressive resistance training stimulates both pathways simultaneously to varying degrees."""
    },
    {
        "doc_id": "P6_28_OVERTRAINING_SUBTYPES",
        "section_title": "OVERTRAINING SYNDROME SUBTYPES: SYMPATHETIC VS PARASYMPATHETIC PRESENTATIONS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "training_adaptations_fatigue_load",
        "group_id": "GRP_P6_OVERTRAINING",
        "text": """Overtraining Syndrome (OTS) presents in two distinct clinical neuroendocrine forms based on autonomic nervous system balance:
1. Sympathetic Overtraining Syndrome (Basedow-type):
   - More common in explosive, power, and sprint athletes subjected to excessive high-intensity training with inadequate rest.
   - Clinical Manifestations: Restlessness, hyperexcitability, insomnia, nocturnal sweating, elevated resting heart rate (tachycardia), delayed heart rate recovery, loss of appetite, weight loss, and emotional irritability.
   - Neuroendocrine State: Hyperactive basal sympathetic tone, elevated resting catecholamines, and blunted adrenal responsiveness to acute stress.
2. Parasympathetic Overtraining Syndrome (Addisonoid-type):
   - More common in endurance athletes subjected to chronic, excessive training volume.
   - Clinical Manifestations: Profound lethargy, chronic fatigue, depressive mood, bradycardia (unusually low resting heart rate), orthostatic hypotension, normal sleep duration but waking unrefreshed, and severe performance drop.
   - Neuroendocrine State: Exhaustion of the hypothalamic-pituitary-adrenal (HPA) axis, blunted cortisol output, low circulating catecholamines, and peripheral tissue insensitivity to catecholamine stimulation. Requires months of complete athletic rest and clinical intervention."""
    },
    {
        "doc_id": "P6_29_BFR_OCCLUSION_PHYSIOLOGY",
        "section_title": "BLOOD FLOW RESTRICTION (BFR) TRAINING: METABOLIC ACCUMULATION AND MOTOR RECRUITMENT",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "training_adaptations_fatigue_load",
        "group_id": "GRP_P6_CONCURRENT_TRAINING",
        "text": """Blood Flow Restriction (BFR) training combines low-load resistance exercise (20% to 30% 1RM) with partial arterial inflow and complete venous outflow occlusion using pneumatic cuffs:
1. Hemodynamic Mechanisms:
   - Arterial Inflow: Preserved at roughly 50% to 80% of arterial occlusion pressure (AOP).
   - Venous Outflow: 100% occluded, trapping deoxygenated blood within the working muscle.
2. Physiological Cascades:
   - Hypoxia and Accelerated Fatigue: Rapid deoxygenation creates severe local hypoxia. Slow-twitch Type I oxidative fibers quickly exhaust their intracellular oxygen and fail.
   - Premature Henneman Size Principle Recruitment: To sustain force output, the central nervous system is forced to recruit high-threshold Type II fast-twitch motor units despite the light external load.
   - Cellular Swelling: Massive accumulation of metabolic byproducts (lactate, H+, Pi) draws fluid into myocytes, exerting intracellular hydrostatic pressure that stretches the sarcolemma, activating anabolic mechanotransduction signaling (mTORC1) and satellite cells.
3. Clinical Utility: Induces muscle hypertrophy and strength gains comparable to heavy resistance training without exposing recovering joints, tendons, or post-surgical tissues to high mechanical shear and compressive forces."""
    },
    {
        "doc_id": "P6_30_EIB_RESPIRATORY_SAFETY",
        "section_title": "EXERCISE-INDUCED BRONCHOCONSTRICTION (EIB): HYPEROSMOLAR MECHANISMS AND MITIGATION",
        "source_id": "US-HHS-PAGAC-REPORT",
        "topic_domain": "training_adaptations_fatigue_load",
        "group_id": "GRP_P6_ENVIRONMENTAL_STRESS",
        "text": """Exercise-Induced Bronchoconstriction (EIB) describes the acute, transient narrowing of lower airways provoked by vigorous exercise, occurring in up to 10% to 20% of the general population and up to 50% of elite winter athletes:
1. Pathophysiological Mechanism (The Osmotic Hypothesis):
   - High minute ventilation during exercise requires rapid humidification and warming of large volumes of inhaled air.
   - Water evaporates rapidly from the airway surface liquid (ASL) lining the bronchial epithelium faster than it can be replaced.
   - Dehydration of the ASL creates a hyperosmolar environment, drawing water out of bronchial epithelial cells and submucosal mast cells.
   - Cell shrinkage triggers mast cell degranulation, releasing inflammatory mediators (histamine, leukotrienes, prostaglandins) that provoke smooth muscle contraction around the bronchioles.
2. Clinical Symptoms: Wheezing, chest tightness, coughing, and shortness of breath typically peaking 5 to 15 minutes post-exercise.
3. Mitigation Strategies:
   - Pre-Exercise Warm-up: An interval-based warm-up (e.g., 6 to 8 bouts of 30-second high-intensity sprints with 2-minute recoveries) induces a 'refractory period' of reduced bronchial reactivity lasting up to 2 hours.
   - Environmental Barriers: Heat-exchange masks when training in cold, dry air."""
    }
]
