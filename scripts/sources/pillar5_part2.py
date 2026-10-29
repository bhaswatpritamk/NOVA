"""Pillar 5 Part 2: Sleep, Recovery, and Physical Activity (Expansion).

Authoritative educational documents drawn from public domain and open-access sources:
- Centers for Disease Control and Prevention (CDC Sleep Guidelines, Public Domain)
- National Institutes of Health / NHLBI (Your Guide to Healthy Sleep, Public Domain)
- Headquarters, Department of the Army (FM 7-22 Sleep Readiness, Public Domain)
- HHS Physical Activity Guidelines Advisory Committee Scientific Report (Public Domain)
"""

DOCUMENTS = [
    {
        "doc_id": "P5_23_SLEEP_DEBT_BANKING",
        "section_title": "SLEEP DEBT ACCUMULATION AND PRE-EMPTIVE SLEEP BANKING KINETICS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_SLEEP_ARCH",
        "text": """Chronic sleep restriction accumulates as 'sleep debt'—the cumulative difference between the biological sleep duration an individual requires and the actual sleep obtained:
1. Cumulative Sleep Debt Degradation:
   - Restricting sleep to 6 hours or fewer per night for 10 to 14 consecutive days produces neurobehavioral and cognitive impairments equivalent to 24 to 48 hours of continuous, acute total sleep deprivation.
   - Slower psychomotor reaction times, impaired split-second tactical decision-making, blunted peripheral motor control, and increased musculoskeletal injury risk (up to 1.7 times higher in chronically sleep-deprived athletes).
2. Sleep Banking (Pre-Emptive Sleep Extension):
   - In anticipation of upcoming periods of unavoidable sleep loss (e.g., intensive training camps, military field operations, cross-timezone travel), extending nocturnal sleep by 1 to 2 hours per night (accumulating 9 to 10 hours daily) for 7 to 10 days builds a neurobiological buffer.
   - Sleep banking attenuates cognitive decline, preserves motor skill accuracy, and maintains sustained endurance capacity during subsequent sleep restriction significantly better than acute recovery sleep alone."""
    },
    {
        "doc_id": "P5_24_REM_MOTOR_LEARNING",
        "section_title": "REM SLEEP AND MOTOR SKILL CONSOLIDATION IN ATHLETIC PERFORMANCE",
        "source_id": "US-NIH-NHLBI-SLEEP",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_SLEEP_ARCH",
        "text": """While Slow-Wave Sleep (SWS) facilitates somatic tissue repair, Rapid Eye Movement (REM) sleep is the primary neurological phase mediating motor skill acquisition, emotional regulation, and neuroplastic memory consolidation:
1. Cortical Replay and Synaptic Plasticity:
   - During REM sleep, hippocampal and motor cortex circuits exhibit coordinated, high-frequency theta wave oscillations (4 to 8 Hz).
   - Motor movement sequences practiced during waking training (e.g., Olympic barbell snatch trajectories, complex footwork drills) are replayed at accelerated speeds within cortical networks, stabilizing synaptic long-term potentiation (LTP).
2. Sleep Spindles in Stage N2 Interaction:
   - Memory consolidation begins in late NREM Stage 2, where sleep spindles gate sensory input and transfer memory traces from the temporary hippocampal buffer to long-term neocortical storage.
   - Subsequent REM sleep integrates these motor traces into existing motor schemas, automating complex movement patterns.
3. REM Deprivation Impact: Restricting sleep to fewer than 6 hours disproportionately truncates the final, longest REM periods of the night, directly impairing technical motor execution, tactical problem-solving, and emotional resilience."""
    },
    {
        "doc_id": "P5_25_CIRCADIAN_MELANOPSIN_LIGHT",
        "section_title": "CIRCADIAN PHOTOBIOLOGY: MELANOPSIN, RETINOHYPOTHALAMIC TRACT, AND SCN",
        "source_id": "US-CDC-SLEEP-2022",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_CIRCADIAN",
        "text": """The master biological clock resides in the suprachiasmatic nucleus (SCN) of the anterior hypothalamus, orchestrating 24-hour circadian rhythms across peripheral organ systems:
1. Retinohypothalamic Transmission:
   - Intrinsically photosensitive retinal ganglion cells (ipRGCs) embedded in the human retina express the photopigment melanopsin, which is maximally sensitive to short-wavelength blue light (460 to 480 nm).
   - Depolarization of ipRGCs sends monosynaptic axonal projections directly along the retinohypothalamic tract to the SCN, independent of visual rod and cone photoreceptors.
2. Pineal Melatonin Suppression:
   - Photic stimulation of the SCN sends inhibitory multisynaptic signals via the superior cervical ganglion to the pineal gland, suppressing the synthesis and secretion of melatonin.
   - In darkness, the SCN removes this inhibition, permitting the rate-limiting enzyme arylalkylamine N-acetyltransferase (AANAT) to convert serotonin into melatonin.
3. Light Hygiene for Recovery:
   - Morning Exposure: Exposure to 10,000 lux natural sunlight for 15 to 30 minutes within 1 hour of waking establishes a robust circadian phase anchor, advancing nocturnal melatonin onset.
   - Evening Mitigation: Exposure to artificial blue light (screens, LED lighting) within 2 hours of bedtime suppresses melatonin by up to 50% to 80%, delaying sleep onset latency and fragmenting deep sleep architecture."""
    },
    {
        "doc_id": "P5_26_HRV_AUTONOMIC_METRICS",
        "section_title": "HEART RATE VARIABILITY (HRV): RMSSD, SDNN, AND AUTONOMIC NERVOUS BALANCE",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_HRV_AUTONOMIC",
        "text": """Heart Rate Variability (HRV)—the continuous physiological fluctuation in the time interval between successive heartbeats (R-R intervals on an electrocardiogram)—provides a non-invasive window into autonomic nervous system regulation:
1. Primary Time-Domain Metrics:
   - Root Mean Square of Successive Differences (rMSSD): Reflects beat-to-beat changes mediated almost exclusively by parasympathetic (vagal) cardiac outflow via the sinoatrial node. High rMSSD signifies robust vagal tone, parasympathetic dominance, and systemic physiological recovery.
   - Standard Deviation of NN Intervals (SDNN): Reflects total autonomic variability, driven by both sympathetic and parasympathetic components over recording epochs.
2. Practical Athlete Monitoring Protocol:
   - Ultra-short morning measurement (60 seconds) taken immediately upon waking in a standardized supine or seated position.
   - Evaluating Trends via 7-day Rolling Averages: An acute drop in rMSSD (> 1.5 standard deviations below the athlete's normal baseline band) signals autonomic fatigue, systemic inflammation, or impending illness, warranting training load reductions.
   - Paradoxical Parasympathetic Hyperactivity: In cases of severe non-functional overreaching, resting heart rate may drop while HRV elevates abnormally—a sign of autonomic exhaustion."""
    },
    {
        "doc_id": "P5_27_ACTIVE_VS_PASSIVE_RECOVERY",
        "section_title": "ACTIVE RECOVERY VS PASSIVE REST: BLOOD FLOW DYNAMICS AND CLEARANCE KINETICS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_RECOVERY_MODALITIES",
        "text": """Choosing between active recovery and passive rest depends on the specific biological objective and time horizon:
1. Active Recovery Protocols:
   - Modality: Low-intensity, non-weight-bearing continuous exercise (cycling, swimming, walking) performed at 30% to 45% of VO2max or < 60% of maximal heart rate for 20 to 30 minutes.
   - Hemodynamic Mechanisms: Rhythmic low-intensity muscle contractions activate the skeletal muscle venous pump, increasing cardiac return and microvascular capillary perfusion to recovering tissues without adding mechanical microtrauma.
   - Metabolic Clearance: Accelerates the transport of circulating lactate to oxidative muscle fibers and hepatocytes, clearing blood lactate significantly faster than passive sitting or lying down.
2. Passive Rest Protocols:
   - Complete physical quiescence, prioritizing psychological detachment, uninterrupted sleep, and gastrointestinal digestion.
   - Indication: Essential following sessions with extreme eccentric muscle damage (severe DOMS) or acute connective tissue strain, where even low-intensity repetitive mechanical loading can prolong inflammatory tissue degradation."""
    },
    {
        "doc_id": "P5_28_HYDROTHERAPY_PROTOCOLS",
        "section_title": "CONTRAST WATER THERAPY: PROTOCOLS AND VASODILATION-VASOCONSTRICTION PUMPING",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_RECOVERY_MODALITIES",
        "text": """Contrast Water Therapy (CWT) utilizes alternating immersion in hot and cold water to manipulate peripheral vascular hemodynamics:
1. Physiological Mechanism:
   - Cold Phase (10°C to 15°C / 50°F to 59°F): Induces acute peripheral vasoconstriction, driving blood inward toward central organs and attenuating local inflammatory edema.
   - Hot Phase (38°C to 40°C / 100°F to 104°F): Induces rapid peripheral vasodilation, increasing blood flow to skin and peripheral musculature.
   - The 'Vascular Pump': Alternating between hot and cold produces cyclic cycles of vasodilation and vasoconstriction, postulated to enhance lymphatic drainage, reduce intramuscular compartment pressure, and decrease perception of muscle stiffness.
2. Standard Operational Protocol:
   - Ratio: 1 minute cold immersion followed by 3 to 4 minutes hot immersion, repeated for 3 to 5 cycles (total time: 15 to 20 minutes).
   - End Condition: End on cold if immediate analgesic relief or inflammation reduction is desired; end on hot if relaxation and bed-time preparation are the objectives."""
    },
    {
        "doc_id": "P5_29_COLD_WATER_IMMERSION_PARADOX",
        "section_title": "COLD WATER IMMERSION (CWI): THE HYPERTROPHY-BLUNTING PARADOX",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_RECOVERY_MODALITIES",
        "text": """Cold Water Immersion (CWI—typically 10 to 15 minutes at 10°C to 12°C) is widely utilized by athletes for acute recovery; however, its application requires strict timing discretion based on training goals:
1. Acute Recovery Benefits:
   - Potent local analgesia through reduced nerve conduction velocity.
   - Attenuation of acute muscular edema, swelling, and subjective sensations of soreness.
   - Highly beneficial during multi-game tournaments, athletic championships, or stage races where immediate short-term physical performance must be repeated within 24 to 48 hours.
2. The Chronic Adaptation Blunting Paradox:
   - When CWI is applied routinely immediately following resistance training sessions, it blunts chronic muscle hypertrophy and long-term strength adaptations.
   - Molecular Mechanisms: Severe hypothermia suppresses p70S6K and ribosomal protein S6 phosphorylation, blunts intracellular mTORC1 signaling, attenuates post-exercise muscle protein synthesis, and suppresses satellite cell proliferation.
3. Evidence-Based Guideline: Avoid regular post-workout cold water immersion during dedicated hypertrophy and strength-building training phases. Reserve CWI for competition phases where immediate performance takes precedence over long-term cellular adaptation."""
    },
    {
        "doc_id": "P5_30_SAUNA_HEAT_THERAPY",
        "section_title": "POST-EXERCISE SAUNA AND HYPERTHERMIC CONDITIONING: VASCULAR AND ENDOCRINE SHIFTS",
        "source_id": "US-ARMY-FM-7-22",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_RECOVERY_MODALITIES",
        "text": """Post-exercise sauna bathing (typically 15 to 30 minutes in a dry Finnish sauna at 80°C to 100°C / 176°F to 212°F) imposes profound acute hyperthermic physiological stress that drives restorative adaptations:
1. Cardiovascular Hemodynamics:
   - Heart rate rises to 120 to 150 beats per minute, resembling moderate-intensity aerobic exercise.
   - Extensive cutaneous vasodilation shunts up to 50% to 70% of cardiac output to the skin, lowering peripheral vascular resistance.
   - Endothelial Shear Stress: Enhanced blood velocity stimulates vascular endothelial nitric oxide synthase (eNOS), improving arterial compliance and systemic blood pressure regulation.
2. Plasma Volume Expansion:
   - Repeated sauna exposure stimulates renal aldosterone and vasopressin pathways, expanding total circulating blood plasma volume by 10% to 15% within 10 to 14 days, improving cardiovascular reserve and endurance performance.
3. Neuroendocrine Responses:
   - Growth Hormone Surge: Serum growth hormone concentrations increase by two- to five-fold following sauna exposure, promoting cellular repair.
   - Brain-Derived Neurotrophic Factor (BDNF): Elevated core temperature stimulates BDNF transcription, supporting neurogenesis and synaptic plasticity."""
    },
    {
        "doc_id": "P5_31_SLEEP_ENVIRONMENT_OPTIMIZATION",
        "section_title": "SLEEP ENVIRONMENT ERGONOMICS: THERMAL, AUDITORY, AND AIR QUALITY PARAMETERS",
        "source_id": "US-NIH-NHLBI-SLEEP",
        "topic_domain": "sleep_recovery_physical_activity",
        "group_id": "GRP_P5_SLEEP_ARCH",
        "text": """Optimizing the physical sleep microenvironment is essential for unhindered progression through deep slow-wave and REM sleep cycles:
1. Ambient Temperature Parameters:
   - Core Temperature Drop: Human sleep initiation is physiologically coupled to a 0.5°C to 1.0°C drop in core body temperature, achieved by dilating peripheral blood vessels in the hands and feet to dissipate heat.
   - Room Temperature: The recommended ambient bedroom temperature is 18°C to 20°C (65°F to 68°F). Ambient temperatures exceeding 24°C (75°F) disrupt thermoregulation, increasing nighttime arousals and significantly reducing Stage 3 slow-wave sleep.
2. Auditory Environment: Ambient background noise exceeding 40 to 45 decibels triggers sympathetic micro-arousals (transient elevations in heart rate and cortical EEG desynchronization) even without conscious waking. Continuous white noise or pink noise masks intermittent disturbances.
3. Air Quality and Carbon Dioxide: High bedroom CO2 concentrations (> 1,200 to 1,500 ppm) resulting from sealed, poorly ventilated rooms impair sleep depth and provoke morning cognitive sluggishness. Adequate bedroom ventilation maintains CO2 below 800 ppm."""
    }
]
