"""Script to build the held-out fitness evaluation benchmark for Project Nova-Fit Phase 8.

Generates data/benchmark/fitness_eval_benchmark.json containing original,
reviewed evaluation items across all 7 pillars and 8 distinct question archetypes.
Verifies zero contamination against the training corpus.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from nova.benchmark import (
    BenchmarkQuestion,
    BenchmarkQuestionType,
    BenchmarkRubric,
    FitnessEvaluationBenchmark,
)


BENCHMARK_QUESTIONS = [
    # =========================================================================
    # PILLAR 1: Exercise Science, Physiology, and Biomechanics
    # =========================================================================
    BenchmarkQuestion(
        question_id="BENCH_P1_FACT_01",
        pillar="exercise_science_biomechanics",
        question_type=BenchmarkQuestionType.BASIC_FACTUAL,
        prompt="What are the primary contractile proteins involved in the cross-bridge cycle of skeletal muscle contraction, and which one contains the ATPase enzyme?",
        expected_key_points=[
            "Actin and myosin are the primary contractile proteins",
            "Actin forms the thin filaments and myosin forms the thick filaments",
            "The globular heads of myosin contain the ATPase enzyme that hydrolyzes ATP",
        ],
        acceptable_alternatives=[
            "Mention of regulatory proteins troponin and tropomyosin modulating actin-myosin interaction"
        ],
        unacceptable_or_unsafe_points=[
            "Claiming actin has ATPase activity",
            "Claiming filaments physically contract in length rather than sliding",
        ],
        source_references=["OpenStax Anatomy and Physiology 2e, Section 10.2 & 10.3"],
        canonical_reference_answer=(
            "The primary contractile proteins in skeletal muscle are actin and myosin. "
            "Actin forms the backbone of thin filaments, whereas myosin aggregates into thick filaments. "
            "The globular heads of the myosin heavy chains possess the enzymatic ATPase activity, which binds "
            "and hydrolyzes adenosine triphosphate (ATP) into ADP and inorganic phosphate to energize the cross-bridge power stroke."
        ),
    ),
    BenchmarkQuestion(
        question_id="BENCH_P1_MECH_01",
        pillar="exercise_science_biomechanics",
        question_type=BenchmarkQuestionType.MECHANISTIC,
        prompt="Explain Henneman's size principle and how motor units are recruited as muscular contraction force increases from low to maximal intensity.",
        expected_key_points=[
            "Motor units are recruited in order of increasing somatic motor neuron size",
            "Small, low-threshold Type I (slow-twitch) motor units are recruited first at low force demands",
            "Larger, higher-threshold Type IIa and Type IIx (fast-twitch) motor units are recruited as force requirements increase or fatigue ensues",
            "Orderly recruitment minimizes fatigue during sustained submaximal activities and optimizes metabolic efficiency",
        ],
        acceptable_alternatives=[
            "Discussing derecruitment order (last hired, first fired in reverse order)"
        ],
        unacceptable_or_unsafe_points=[
            "Claiming fast-twitch fibers are always recruited before slow-twitch fibers during normal voluntary contraction"
        ],
        source_references=["OpenStax Anatomy and Physiology 2e, Section 10.4"],
        canonical_reference_answer=(
            "Henneman's size principle dictates that under voluntary muscle contraction, motor units are recruited in a precise, "
            "orderly sequence dictated by the size of their motor neuron cell bodies. Small motor neurons with lower recruitment "
            "thresholds innervating fatigue-resistant Type I (slow-twitch) fibers fire first during low-force tasks. "
            "As force demands rise—or as active fibers fatigue—progressively larger motor neurons with higher excitation thresholds "
            "are recruited, engaging Type IIa and eventually high-threshold Type IIx (fast-twitch) glycolytic fibers for maximal force generation."
        ),
    ),

    # =========================================================================
    # PILLAR 2: Strength Training Principles and Programming
    # =========================================================================
    BenchmarkQuestion(
        question_id="BENCH_P2_SCEN_01",
        pillar="strength_training_programming",
        question_type=BenchmarkQuestionType.WORKOUT_PLANNING_SCENARIO,
        prompt="Design a balanced 3-day full-body resistance training template for a healthy novice lifter aiming for general strength and hypertrophy, adhering to evidence-based overload principles.",
        expected_key_points=[
            "3 non-consecutive training days per week (e.g., Monday, Wednesday, Friday) allowing 48 hours between sessions",
            "Compound multi-joint movements covering major movement patterns: squat/knee-flexion, hinge/posterior chain, upper push (horizontal/vertical), upper pull (horizontal/vertical)",
            "Moderate repetition ranges suitable for a novice: roughly 6 to 12 repetitions per set, with 2 to 3 working sets per exercise",
            "Appropriate proximity to failure: maintaining 1 to 3 repetitions in reserve (RIR) rather than grinding to failure",
            "A structured plan for progressive overload (e.g., adding small increments of load or reps when target volume is achieved with good form)",
        ],
        acceptable_alternatives=[
            "A/B alternating workout structure across 3 sessions"
        ],
        unacceptable_or_unsafe_points=[
            "Prescribing maximal 1RM testing on day one",
            "Prescribing excessive high-volume daily failure training without deloads",
        ],
        source_references=["U.S. Army FM 7-22 Chapter 5; CDC Guidelines on Muscle Strengthening"],
        canonical_reference_answer=(
            "A foundational 3-day full-body program should be scheduled on non-consecutive days (e.g., Mon/Wed/Fri). "
            "Each session targets major fundamental movement patterns with compound exercises: Day A incorporates barbell or goblet squats (3x8-10), "
            "dumbbell bench press (3x8-10), seated cable rows (3x10-12), and Romanian deadlifts (2x10). Day B incorporates trap bar deadlifts (3x6-8), "
            "overhead dumbbell press (3x8-10), lat pulldowns (3x10-12), and walking lunges (2x10/leg). All sets should be executed with 1 to 2 "
            "repetitions in reserve (RIR). Overload is achieved by incrementally adding 2.5-5 lbs to upper body or 5-10 lbs to lower body lifts "
            "once the upper rep boundary is achieved across all sets with strict technique."
        ),
    ),
    BenchmarkQuestion(
        question_id="BENCH_P2_NUM_01",
        pillar="strength_training_programming",
        question_type=BenchmarkQuestionType.NUMERICAL_REASONING,
        prompt="If an athlete has a tested 1-repetition maximum (1RM) of 140 kg on the back squat, calculate the exact working load for a session programmed at 75% of 1RM, and estimate the expected repetition range they can complete with that load.",
        expected_key_points=[
            "Working load calculation: 140 kg * 0.75 = 105.0 kg",
            "Expected repetition range at 75% 1RM: approximately 8 to 10 repetitions to momentary muscular failure (or 6 to 8 reps keeping 2 RIR)",
        ],
        acceptable_alternatives=[
            "7 to 11 repetitions depending on individual fiber type distribution and training status"
        ],
        unacceptable_or_unsafe_points=[
            "Incorrect arithmetic (e.g., calculating 115 kg or 95 kg)",
            "Stating 75% 1RM corresponds to 1 to 3 repetitions or over 20 repetitions",
        ],
        source_references=["U.S. Army ATP 7-22.02 Conditioning Drills"],
        canonical_reference_answer=(
            "To calculate the training load: 140 kg * 0.75 = 105.0 kg. "
            "In sports science loading charts, 75% of 1RM typically corresponds to a repetition capacity of approximately 10 repetitions "
            "at momentary muscular failure. In a structured training block, the athlete would typically perform sets of 7 to 8 repetitions with 105 kg, "
            "preserving 2 to 3 repetitions in reserve (RIR) to manage fatigue."
        ),
    ),

    # =========================================================================
    # PILLAR 3: Exercise Technique and Safe Equipment Use
    # =========================================================================
    BenchmarkQuestion(
        question_id="BENCH_P3_SAFE_01",
        pillar="exercise_technique_safety",
        question_type=BenchmarkQuestionType.SAFETY_SENSITIVE_REFERRAL,
        prompt="A 45-year-old beginner client reports experiencing sharp, pinching anterior hip pain during deep barbell squats that persists when walking and sharp pain radiating down the left leg. How should you respond and modify their training?",
        expected_key_points=[
            "Immediately stop performing movements that provoke sharp, pinching, or radiating pain",
            "Explicitly advise the client to consult a qualified physician or physical therapist for clinical orthopedic evaluation",
            "Explain that radiating pain can indicate neurovascular or discogenic involvement and sharp pinching can indicate impingement or labral pathology",
            "Do not attempt to medically diagnose the condition or prescribe corrective rehabilitation exercises for an undiagnosed nerve symptom",
        ],
        acceptable_alternatives=[
            "Suggesting temporary gentle pain-free mobility or non-aggravating low-impact walking if approved by clinician"
        ],
        unacceptable_or_unsafe_points=[
            "Telling the client to push through the pain or stretch more aggressively into the painful impingement zone",
            "Attempting to diagnose a specific lumbar disc herniation or labral tear without medical credentials",
        ],
        source_references=["NIAMS Sports Injuries Prevention; CDC Injury Prevention"],
        canonical_reference_answer=(
            "You must immediately advise the client to stop deep squats and any exercises provoking sharp hip pain or radiating neurological symptoms. "
            "Radiating leg pain and sharp anterior hip impingement are clinical red flags that require evaluation by a qualified medical professional "
            "(such as a physical therapist or sports medicine physician) to rule out structural pathology such as lumbar radiculopathy or femoroacetabular "
            "impingement/labral injury. As a fitness professional, you must not diagnose medical conditions. Temporarily replace the squat pattern "
            "with pain-free, non-radiating alternatives only after clinical clearance."
        ),
    ),

    # =========================================================================
    # PILLAR 4: Nutrition Fundamentals and Hydration
    # =========================================================================
    BenchmarkQuestion(
        question_id="BENCH_P4_NUM_01",
        pillar="nutrition_fundamentals_hydration",
        question_type=BenchmarkQuestionType.NUMERICAL_REASONING,
        prompt="Calculate the daily protein target in grams for an 80 kg resistance-trained athlete aiming to maximize muscle hypertrophy, using standard evidence-based intake ranges of 1.6 to 2.2 g/kg/day.",
        expected_key_points=[
            "Lower bound calculation: 80 kg * 1.6 g/kg = 128 grams/day",
            "Upper bound calculation: 80 kg * 2.2 g/kg = 176 grams/day",
            "Recommended target range: 128 to 176 grams of high-quality protein per day",
        ],
        acceptable_alternatives=[
            "Rounding to 130 - 180 grams/day",
            "Mention of distributing protein across 3 to 5 meals throughout the day"
        ],
        unacceptable_or_unsafe_points=[
            "Arithmetic errors (e.g., calculating 80 grams or 300 grams)",
            "Stating that intake above 0.8 g/kg is toxic for healthy individuals",
        ],
        source_references=["USDA-HHS Dietary Guidelines 2020-2025; NIH ODS Sports Nutrition"],
        canonical_reference_answer=(
            "For an 80 kg athlete targeting 1.6 to 2.2 g/kg/day: "
            "Lower range: 80 kg * 1.6 g/kg = 128 grams. "
            "Upper range: 80 kg * 2.2 g/kg = 176 grams. "
            "The athlete should consume between 128 and 176 grams of protein daily, distributed relatively evenly across 3 to 4 meals "
            "(e.g., 30 to 45 grams per meal) to optimize muscle protein synthesis."
        ),
    ),
    BenchmarkQuestion(
        question_id="BENCH_P4_UNCERT_01",
        pillar="nutrition_fundamentals_hydration",
        question_type=BenchmarkQuestionType.UNCERTAINTY_CONFLICTING_EVIDENCE,
        prompt="Is consuming a high-protein shake within 30 minutes immediately post-workout mandatory to prevent muscle loss, or does the scientific evidence show a different requirement?",
        expected_key_points=[
            "The rigid 30-minute 'anabolic window' is not mandatory according to contemporary sports nutrition consensus",
            "The muscle protein synthesis response remains sensitized to amino acid availability for at least 24 to 48 hours post-exercise",
            "Total daily protein intake and distribution across meals is significantly more important for hypertrophy than immediate post-workout timing",
            "Immediate intake is only critical if the athlete trained in a fasted state several hours prior",
        ],
        acceptable_alternatives=[
            "Acknowledging that consuming protein post-workout is practical and convenient, even if not biologically urgent within 30 minutes"
        ],
        unacceptable_or_unsafe_points=[
            "Claiming that missing the 30-minute window wastes the entire workout or causes immediate severe muscle loss"
        ],
        source_references=["NIH ODS Sports Nutrition; ISSN Position Stand: Nutrient Timing"],
        canonical_reference_answer=(
            "Contemporary scientific evidence indicates that the classic 30-minute 'anabolic window' is largely a sports folklore oversimplification. "
            "While muscle protein synthesis is elevated post-exercise, this heightened sensitivity persists for 24 to 48 hours. "
            "Systematic reviews demonstrate that meeting total daily protein targets (1.6-2.2 g/kg) and spacing protein across the day "
            "is the primary driver of muscular adaptations. Immediate consumption within 30 minutes is only advantageous if the athlete trained "
            "in a prolonged fasted state where amino acid availability was depleted prior to the session."
        ),
    ),

    # =========================================================================
    # PILLAR 5: Sleep, Recovery, and Physical Activity
    # =========================================================================
    BenchmarkQuestion(
        question_id="BENCH_P5_FACT_01",
        pillar="sleep_recovery_physical_activity",
        question_type=BenchmarkQuestionType.BASIC_FACTUAL,
        prompt="What is the general recommended sleep duration for healthy adults to support physical recovery and general health, and during which sleep stage does the majority of nocturnal growth hormone secretion occur?",
        expected_key_points=[
            "Recommended sleep duration for healthy adults is 7 to 9 hours per night (with athletes frequently benefiting from 8 to 10 hours)",
            "Nocturnal growth hormone secretion occurs primarily during slow-wave sleep (Stage N3 non-REM / deep sleep)",
        ],
        acceptable_alternatives=[
            "CDC recommendation of at least 7 hours per night"
        ],
        unacceptable_or_unsafe_points=[
            "Recommending less than 5 hours as optimal for athletic adaptation",
            "Stating growth hormone is secreted primarily during REM dreaming sleep",
        ],
        source_references=["US-CDC-SLEEP-2022; US-NIH-NHLBI-SLEEP"],
        canonical_reference_answer=(
            "The CDC and National Sleep Foundation recommend that healthy adults obtain 7 to 9 hours of quality sleep per 24-hour period, "
            "with hard-training athletic populations frequently requiring 8 to 10 hours to optimize systemic recovery. "
            "The vast majority of pulsatile nocturnal growth hormone release occurs during slow-wave sleep (Stage N3 non-REM, or deep sleep), "
            "which predominates in the first third of the sleep cycle."
        ),
    ),

    # =========================================================================
    # PILLAR 6: Training Adaptations, Fatigue, and Load Management
    # =========================================================================
    BenchmarkQuestion(
        question_id="BENCH_P6_MECH_01",
        pillar="training_adaptations_fatigue_load",
        question_type=BenchmarkQuestionType.MECHANISTIC,
        prompt="What is the physiological cause of Delayed Onset Muscle Soreness (DOMS), and why is lactic acid accumulation an incorrect explanation?",
        expected_key_points=[
            "DOMS is caused by microstructural disruption to sarcomeres and extracellular matrix (especially from unaccustomed eccentric contractions)",
            "Mechanical damage triggers an inflammatory repair response involving prostaglandin release, immune cell infiltration, and edema that peaks 24 to 72 hours later",
            "Lactic acid (lactate) is cleared from muscle and blood back to resting levels within 30 to 60 minutes post-exercise, long before DOMS appears",
            "Lactate is a metabolic intermediate and energy substrate, not a persistent muscle toxin",
        ],
        acceptable_alternatives=[
            "Mentioning disruption of Z-discs as a specific histological hallmark of eccentric damage"
        ],
        unacceptable_or_unsafe_points=[
            "Affirming the myth that lactic acid remains trapped in muscle tissue for 48 hours to cause soreness"
        ],
        source_references=["OpenStax Anatomy and Physiology 2e, Section 10.5; NIH NIAMS"],
        canonical_reference_answer=(
            "Delayed Onset Muscle Soreness (DOMS) results from microscopic structural damage to sarcomere Z-discs and surrounding connective tissue, "
            "provoked primarily by unaccustomed high-force eccentric muscular contractions. This micro-trauma initiates an acute local inflammatory response "
            "characterized by leukocyte infiltration, fluid accumulation (edema), and sensitization of mechanical nociceptors, which peaks 24 to 72 hours post-exercise. "
            "Lactic acid accumulation is physiological folklore: blood and intramuscular lactate concentrations return to baseline within 30 to 60 minutes post-workout. "
            "Lactate is shuttled into mitochondria or the bloodstream to serve as an oxidative fuel substrate, playing zero role in 48-hour DOMS."
        ),
    ),
    BenchmarkQuestion(
        question_id="BENCH_P6_INSUFF_01",
        pillar="training_adaptations_fatigue_load",
        question_type=BenchmarkQuestionType.INSUFFICIENT_INFORMATION,
        prompt="I have been lifting weights and my performance stopped improving. Tell me what deload program I should follow and how much weight to take off.",
        expected_key_points=[
            "Explicitly identify that critical training information is missing before a specific deload protocol can be recommended",
            "Ask for key missing variables: current training volume and frequency, duration of stagnation, intensity (% 1RM/RIR), fatigue symptoms (sleep, joint aches, mood), nutrition and energy balance",
            "Explain that performance stagnation can result from under-recovery (overreaching), insufficient stimulus (lack of progressive overload), or caloric deficit, not solely systemic overtraining",
            "Provide general guidelines for a deload (e.g., reducing volume by 30-50% while maintaining load intensity) only as a broad concept, pending details",
        ],
        acceptable_alternatives=[
            "Suggesting a temporary volume reduction while gathering the needed context"
        ],
        unacceptable_or_unsafe_points=[
            "Prescribing a rigid, specific deload prescription without asking any clarifying questions about the user's program or condition"
        ],
        missing_variables_required=[
            "Current training program and volume",
            "Intensity and proximity to failure",
            "Sleep quality and dietary caloric intake",
            "Specific lifts stalled and duration of plateau",
        ],
        source_references=["U.S. Army FM 7-22 Chapter 5; ATP 7-22.02 Load Management"],
        canonical_reference_answer=(
            "Before prescribing a specific deload protocol, more context is needed regarding your training and recovery variables. "
            "Please clarify: 1) What is your current weekly set volume and exercise frequency? 2) How long has performance stalled? "
            "3) What are your sleep duration, stress levels, and daily nutritional intake (caloric surplus, maintenance, or deficit)? "
            "Stagnation can stem from inadequate recovery requiring a volume reduction, or from an insufficient training stimulus or caloric deficit. "
            "Generally, a deload involves reducing weekly set volume by roughly 40-50% while maintaining movement patterns and moderate intensity for one week, "
            "but the exact prescription depends on your training profile."
        ),
    ),

    # =========================================================================
    # PILLAR 7: General Fitness Education and Age-Appropriate Safety
    # =========================================================================
    BenchmarkQuestion(
        question_id="BENCH_P7_FACT_01",
        pillar="general_fitness_education_safety",
        question_type=BenchmarkQuestionType.BASIC_FACTUAL,
        prompt="According to the Physical Activity Guidelines for Americans (2nd Edition), what are the minimum weekly physical activity recommendations for substantial health benefits in adults?",
        expected_key_points=[
            "At least 150 to 300 minutes of moderate-intensity aerobic physical activity per week, OR",
            "At least 75 to 150 minutes of vigorous-intensity aerobic physical activity per week (or an equivalent combination)",
            "Muscle-strengthening activities involving all major muscle groups on 2 or more days per week",
        ],
        acceptable_alternatives=[
            "Mention that spreading activity throughout the week is recommended and that moving more and sitting less provides additional benefits"
        ],
        unacceptable_or_unsafe_points=[
            "Stating that muscle strengthening is optional or only for bodybuilders",
            "Stating less than 30 minutes total activity per week is sufficient for standard adult guidelines",
        ],
        source_references=["US-HHS-PAG-2018; US-CDC-PA-2022"],
        canonical_reference_answer=(
            "According to federal health guidelines (HHS Physical Activity Guidelines for Americans, 2nd Edition), "
            "adults require a weekly volume of 150 to 300 minutes of moderate-intensity physical activity, "
            "or alternatively 75 to 150 minutes of vigorous aerobic exercise (or an equivalent combination). "
            "In addition, adults should perform full-body resistance exercise on at least two separate days per week."
        ),
    ),
    BenchmarkQuestion(
        question_id="BENCH_P7_UNANS_01",
        pillar="general_fitness_education_safety",
        question_type=BenchmarkQuestionType.UNANSWERABLE_EVIDENCE_LACKING,
        prompt="Which brand of detox tea and electro-stimulation sweat belt will melt away 10 pounds of abdominal fat in 7 days without changing my diet?",
        expected_key_points=[
            "Explicitly reject the premise: no scientific evidence supports detox teas or sweat belts for selective abdominal fat loss",
            "Explain that 'spot reduction' of fat is biologically impossible; adipose tissue loss occurs systemically through sustained energy deficit",
            "Clarify that 'detox teas' often contain laxatives or diuretics that cause temporary water loss, not adipose reduction, with potential dehydration risks",
            "State clearly that sustainable body composition change requires dietary caloric management and regular physical activity",
        ],
        acceptable_alternatives=[
            "Warning against the health risks of unverified herbal detox supplements"
        ],
        unacceptable_or_unsafe_points=[
            "Recommending any commercial detox tea or fat-burning wrap product",
            "Validating that 10 pounds of fat can be safely lost in 7 days without diet changes",
        ],
        source_references=["CDC Physical Activity Basics; NIH ODS Supplements; HHS Dietary Guidelines"],
        canonical_reference_answer=(
            "No brand of detox tea or electro-stimulation sweat belt can produce selective abdominal fat loss. "
            "From an exercise science and metabolic perspective, 'spot reduction' is an empirical impossibility: fat is mobilized systemically "
            "from adipose stores across the entire body under the direction of systemic hormones and a sustained net caloric deficit. "
            "Detox teas often contain unverified herbal stimulants or diuretics that cause transient fluid loss and electrolyte depletion, "
            "not genuine fat reduction. Safe, sustainable body composition alteration requires a balanced nutritional approach and progressive exercise."
        ),
    ),
]


def build_benchmark() -> None:
    """Build and validate the held-out fitness evaluation benchmark."""
    benchmark = FitnessEvaluationBenchmark(questions=BENCHMARK_QUESTIONS, version="1.0.0")
    print(f"Created benchmark with {len(benchmark.questions)} questions.")
    print("Archetype distribution:", benchmark.get_type_counts())
    print("Pillar distribution:", benchmark.get_pillar_counts())

    # Contamination & Leakage check against expanded training corpus
    train_corpus_path = REPO_ROOT / "data" / "approved" / "expanded_train_corpus.txt"
    if train_corpus_path.is_file():
        train_text = train_corpus_path.read_text(encoding="utf-8")
        clean, leakage = benchmark.verify_no_leakage(train_text, n_gram_len=8)
        if not clean:
            print("WARNING: Contamination detected between benchmark and training corpus:")
            for lk in leakage:
                print("  ", lk)
            raise ValueError(f"Benchmark contamination detected: {len(leakage)} matches.")
        else:
            print("Contamination check PASSED: 0 n-gram leakage matches between benchmark and training corpus.")
    else:
        print("Note: expanded_train_corpus.txt not found for contamination check.")

    out_path = REPO_ROOT / "data" / "benchmark" / "fitness_eval_benchmark.json"
    benchmark.save(out_path)
    print(f"Saved benchmark to {out_path}")


if __name__ == "__main__":
    build_benchmark()
