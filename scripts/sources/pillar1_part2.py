"""Pillar 1 Part 2: Exercise Science, Physiology, and Biomechanics (Expansion).

Authoritative educational documents drawn from public domain and open-access sources:
- OpenStax Anatomy and Physiology 2e (CC BY 4.0, Betts et al.)
- NASA Human Research Program Evidence Book: Muscle Mass, Strength, and Endurance (Public Domain)
- HHS Physical Activity Guidelines Advisory Committee Scientific Report (Public Domain)
"""

DOCUMENTS = [
    {
        "doc_id": "P1_28_CONNECTIVE_TISSUE_LAYERS",
        "section_title": "SKELETAL MUSCLE FASCIAL ARCHITECTURE: EPIMYSIUM, PERIMYSIUM, AND ENDOMYSIUM",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_SARCOMERE",
        "text": """Skeletal muscle tissue is organized into a hierarchical framework of specialized connective tissue sheaths that provide structural integrity, transmit contractile force to the skeleton, and house neurovascular pathways:
1. Epimysium: A dense, irregular collagenous connective tissue sheath that encapsulates the entire anatomical muscle belly. It separates the muscle from neighboring tissues and organs, providing an outer mechanical barrier that resists overstretching while facilitating low-friction gliding against surrounding fascial planes.
2. Perimysium: Intermediate connective tissue septa that branch inward from the epimysium, compartmentalizing muscle fibers into distinct anatomical bundles called fascicles (containing 10 to 100+ muscle fibers). The perimysial collagen network (predominantly Types I and III collagen) plays a major role in lateral force transmission from individual fibers across costameres to neighboring muscle fibers.
3. Endomysium: A delicate, mesh-like sheath of loose areolar connective tissue encapsulating each individual myocyte (muscle fiber). It lies immediately external to the sarcolemma and basal lamina, providing an optimal extracellular ionic microenvironment and supporting capillaries and nerve terminals that innervate the individual muscle fiber.
At the ends of the muscle belly, the epimysial, perimysial, and endomysial collagen fibers converge and coalesce into dense regular connective tissue, forming tendons or aponeuroses that anchor the muscle into the periosteum of bone."""
    },
    {
        "doc_id": "P1_29_SARCOPLASMIC_RETICULUM_CALCIUM",
        "section_title": "SARCOPLASMIC RETICULUM ARCHITECTURE AND CALCIUM FLUX REGULATION",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_SARCOMERE",
        "text": """The sarcoplasmic reticulum (SR) is an intracellular smooth endoplasmic reticulum specialized for the rapid storage, release, and reuptake of calcium ions (Ca2+), acting as the central regulatory node of excitation-contraction coupling.
Structural components of the SR include:
1. Terminal Cisternae: Expanded sac-like reservoirs of the SR that abut transverse tubules (T-tubules). Together, one transverse tubule and two flanking terminal cisternae form a cellular functional complex termed a 'triad'. Inside the terminal cisternae, calcium is bound at high capacity and low affinity to the acidic storage protein calsequestrin, allowing the SR to sequester millimolar concentrations of calcium without precipitating calcium phosphate crystals.
2. Ryanodine Receptors (RyR1): Giant homotetrameric calcium release channels embedded within the junctional SR membrane. When the T-tubular voltage sensor (dihydropyridine receptor / DHPR / Cav1.1) undergoes conformational change during sarcolemmal action potential depolarization, it physically uncouples RyR1, releasing a massive flux of Ca2+ down its electrochemical gradient into the myoplasm.
3. Longitudinal SR and SERCA Pumps: Sarcoplasmic/Endoplasmic Reticulum Calcium ATPase (SERCA1a in fast-twitch fibers, SERCA2a in slow-twitch fibers) pumps utilize ATP hydrolysis to actively transport cytosolic Ca2+ back into the SR lumen against a 10,000-fold concentration gradient, lowering myoplasmic calcium levels and permitting troponin to re-block myosin binding sites, driving muscular relaxation."""
    },
    {
        "doc_id": "P1_30_ATP_RIGOR_KINETICS",
        "section_title": "ATP ENERGETICS IN THE CROSS-BRIDGE CYCLE AND RIGOR COMPLEX RESOLUTION",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_SARCOMERE",
        "text": """Adenosine triphosphate (ATP) fulfills dual energetic and mechanical roles in skeletal muscle contraction and relaxation:
1. Power Stroke Resolution: Following the conformational power stroke where the myosin head pulls the actin filament toward the M-line, ADP and inorganic phosphate (Pi) dissociate from the nucleotide-binding pocket on the myosin head. In this state, myosin remains tightly and immobolizedly bound to actin—a conformation known as the 'rigor complex'.
2. Cross-Bridge Detachment: The binding of a new ATP molecule to the empty nucleotide pocket of the myosin head induces an allosteric conformational shift in the actin-binding domain, dramatically reducing myosin's affinity for actin and causing immediate detachment.
3. ATP Hydrolysis: Once detached, the intrinsic ATPase domain of the myosin head hydrolyzes the bound ATP into ADP and Pi. The energy released by this exergonic reaction re-cocks the myosin neck linker into a high-energy, pre-power stroke conformation, preparing it to bind the next actin monomer.
Pathophysiological Implication (Rigor Mortis): Following somatic death, cellular respiration halts and intracellular ATP pools deplete to zero. Calcium leaks from the deteriorating sarcoplasmic reticulum into the cytosol, binding troponin and exposing actin sites. Myosin heads bind actin and execute a final power stroke; however, without new ATP to bind the myosin head, the cross-bridges cannot detach. The actin-myosin complexes remain locked in the rigid rigor state until lysosomal autolytic proteases degrade the contractile filaments."""
    },
    {
        "doc_id": "P1_31_JOINT_CLASSIFICATION_KINEMATICS",
        "section_title": "ARTICULAR CLASSIFICATION AND JOINT KINEMATICS: SYNARTHROSES, AMPHIARTHROSES, AND DIARTHROSES",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_JOINT_MECHANICS",
        "text": """Human skeletal articulations (joints) are classified structurally according to connective tissue composition and functionally according to permitted degrees of freedom and mobility:
1. Structural Classification:
   - Fibrous Joints: Adjacent bones united directly by fibrous connective tissue with no articular cavity (e.g., cranial sutures, syndesmoses between radius and ulna, gomphoses anchoring teeth into alveolar sockets).
   - Cartilaginous Joints: Bones united by hyaline cartilage (synchondroses, such as epiphyseal growth plates) or fibrocartilage (symphyses, such as pubic symphysis and intervertebral discs).
   - Synovial Joints: Articulating bone surfaces separated by a fluid-filled joint cavity enclosed within a fibrous articular capsule lined by a synovial membrane.
2. Functional Classification:
   - Synarthroses: Completely immovable joints providing maximal stability and bone fusion (cranial sutures).
   - Amphiarthroses: Slightly movable joints providing moderate shock absorption and structural flexibility (intervertebral symphyses, sacroiliac joints).
   - Diarthroses: Freely movable joints possessing one, two, or three rotational degrees of freedom (uniaxial hinge joints like the humeroulnar joint; biaxial condyloid/saddle joints like the radiocarpal and 1st carpometacarpal joints; multiaxial ball-and-socket joints like the glenohumeral and femoroacetabular joints).
In resistance training, understanding joint degrees of freedom is essential for selecting movement trajectories that align with natural anatomical axes."""
    },
    {
        "doc_id": "P1_32_SYNOVIAL_FLUID_CARTILAGE",
        "section_title": "SYNOVIAL FLUID RHEOLOGY AND ARTICULAR CARTILAGE BIOMECHANICS",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_JOINT_MECHANICS",
        "text": """Articular (hyaline) cartilage covers the epiphyses of articulating bones within diarthrodial joints, providing an ultra-low-friction (coefficient of friction < 0.005), wear-resistant, load-bearing surface.
Biomechanical structure and fluid lubrication mechanics:
1. Extracellular Matrix Composition: Composed of 65% to 80% water, 15% to 22% Type II collagen fibrils, and 4% to 9% proteoglycans (predominantly aggrecan aggregates bound to hyaluronic acid chains). The negative electrical charges on the glycosaminoglycan (chondroitin sulfate and keratan sulfate) side chains exert high osmotic swelling pressure, drawing water into the tissue matrix.
2. Synovial Fluid Rheology: Synovial fluid is an ultrafiltrate of blood plasma containing high concentrations of hyaluronic acid and lubricin synthesized by Type B synoviocytes. It exhibits non-Newtonian, shear-thinning (thixotropic) behavior: under resting or slow movement conditions, its viscosity is high; during rapid joint articulation, its viscosity drops dramatically, minimizing friction.
3. Interstitial Fluid Pressurization: When an axial joint load is applied (such as during a barbell squat), fluid within the porous cartilage matrix is pressurized, supporting > 90% of the compressive load and shielding the solid collagen-proteoglycan matrix from mechanical damage.
4. Chondrocyte Nutrition: Because articular cartilage is completely avascular, aneural, and alymphatic, chondrocytes rely entirely on cyclic compressive loading and unloading during movement to pump synovial fluid in and out of the matrix, delivering glucose and oxygen while removing metabolic wastes."""
    },
    {
        "doc_id": "P1_33_SPINE_BIOMECHANICS_DISCS",
        "section_title": "VERTEBRAL COLUMN BIOMECHANICS: INTERVERTEBRAL DISC MECHANICS AND HOOP STRESS",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_SPINE_BIOMECHANICS",
        "text": """The human vertebral column consists of 24 movable presacral vertebrae cushioned by fibrocartilaginous intervertebral discs (IVDs), structured to bear large compressive axial forces while permitting three-dimensional trunk articulation:
1. Nucleus Pulposus (NP): The gelatinous, highly hydrated central core of the disc, derived embryologically from the notochord. Composed of 70% to 90% water bound to hydrophilic proteoglycans. Under axial compressive loading, the incompressible nucleus pulposus deforms radially in all lateral directions, converting axial compressive force into lateral tensile hoop stress.
2. Annulus Fibrosus (AF): A concentric series of 15 to 25 laminated fibrocartilaginous rings (lamellae) composed of densely packed Type I and II collagen fibers. The collagen fibers within adjacent lamellae run at alternating 60-degree angles to the vertical spinal axis. This criss-cross architectural arrangement enables the annulus to resist extreme tensile hoop stresses generated by the pressurized nucleus pulposus.
3. Flexion-Compression Vulnerability: When the spine is loaded in neutral lordosis, compressive stress is distributed uniformly across the vertebral endplates. However, when axial loading is combined with deep spinal flexion (lumbar rounding), the anterior disc margins are compressed, wedging the disc and driving the pressurized nucleus pulposus posteriorly against the thinner posterior annulus fibrosus, increasing the risk of disc bulging or herniation."""
    },
    {
        "doc_id": "P1_34_LEVER_CLASSES_CALCULATIONS",
        "section_title": "BIOMECHANICAL LEVER SYSTEMS: FIRST, SECOND, AND THIRD CLASS LEVER MECHANICS",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_LEVERS_MOMENTS",
        "text": """Musculoskeletal levers translate muscular contraction (effort) into skeletal movement against external gravity or resistance (load) across a skeletal articulation (fulcrum / pivot point).
Levers are classified into three mechanical configurations:
1. First-Class Lever: The fulcrum lies between the effort force and the load (Effort - Fulcrum - Load). Example: The atlanto-occipital joint of the neck, where the cervical spine acts as the fulcrum, the splenius capitis and trapezius exert downward effort force on the occipital bone, balancing the anterior weight of the cranium. Mechanical advantage can be greater than, equal to, or less than 1.0 depending on relative arm lengths.
2. Second-Class Lever: The load lies between the fulcrum and the effort force (Fulcrum - Load - Effort). Example: Plantar flexion at the ankle during a calf raise, where the metatarsophalangeal joints act as the fulcrum, the downward gravitational weight of the body passes through the tibia/talus, and the triceps surae (gastrocnemius and soleus) exerts upward effort force via the Achilles tendon on the calcaneus. Because the effort arm is always longer than the load arm, mechanical advantage is always greater than 1.0, magnifying force at the expense of range of motion and speed.
3. Third-Class Lever: The effort force is applied between the fulcrum and the load (Fulcrum - Effort - Load). Example: Elbow flexion during a biceps curl, where the humeroulnar joint is the fulcrum, the biceps brachii tendon inserts on the radial tuberosity (effort), and the barbell is held in the hand (load). Because the effort arm is much shorter than the load arm, mechanical advantage is always less than 1.0, requiring enormous muscular force to lift modest external loads, but maximizing movement speed and angular range of motion."""
    },
    {
        "doc_id": "P1_35_MOMENT_ARMS_RESISTANCE_PROFILES",
        "section_title": "MOMENT ARMS, TORQUE VARIATION, AND RESISTANCE PROFILES ACROSS JOINT ROM",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_LEVERS_MOMENTS",
        "text": """Torque (rotational force, measured in Newton-meters / N-m) dictates the rotational demands imposed on a joint during resistance training:
Torque = Force x Moment Arm.
The moment arm is the perpendicular distance from the joint's axis of rotation to the line of action of the applied force:
1. Internal Moment Arm: The perpendicular distance from the joint center of rotation to the line of pull of the contracting muscle tendon. As a joint flexes or extends, the angle of insertion changes, causing the internal moment arm to vary continuously throughout the range of motion (e.g., biceps brachii internal moment arm peaks near 90 to 100 degrees of elbow flexion).
2. External Moment Arm: The perpendicular distance from the joint center of rotation to the line of action of the external load (e.g., the line of gravity acting on a barbell, or the vector of a cable pulley). In a dumbbell lateral raise, the external moment arm of the dumbbell relative to the glenohumeral joint is near zero at the bottom position and reaches its maximum when the arm is parallel to the floor (90 degrees abduction).
3. Strength Profile Matching: For optimal muscular stimulation, the resistance profile of an exercise (the curve of external torque requirements across the ROM) should ideally align with the muscle's natural length-tension and internal moment arm capabilities (the physiological strength curve)."""
    },
    {
        "doc_id": "P1_36_ANAEROBIC_GLYCOLYSIS_STOICHIOMETRY",
        "section_title": "BIOENERGETICS: BIOCHEMICAL STOICHIOMETRY OF ANAEROBIC GLYCOLYSIS",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_BIOENERGETICS",
        "text": """Anaerobic (fast) glycolysis is the enzymatic degradation of glucose or glycogen into pyruvate in the absence of sufficient mitochondrial oxygen, providing high-rate ATP resynthesis during maximal exertion lasting 15 to 120 seconds.
Stoichiometric pathway and regulatory checkpoints:
1. Substrate Entry and Phosphorylation:
   - Blood Glucose: Phosphorylated by hexokinase to glucose-6-phosphate (G6P), consuming 1 molecule of ATP.
   - Muscle Glycogen: Cleaved by glycogen phosphorylase into glucose-1-phosphate and converted to G6P without consuming ATP.
2. The Rate-Limiting Step: Fructose-6-phosphate is phosphorylated to fructose-1,6-bisphosphate by the allosteric enzyme Phosphofructokinase-1 (PFK-1). PFK-1 is allosterically activated by elevated AMP and ADP, and allosterically inhibited by high ATP, citrate, and falling intracellular pH.
3. Cleavage and Oxidation: Fructose-1,6-bisphosphate is cleaved into two triose phosphates (glyceraldehyde-3-phosphate), which are oxidized by glyceraldehyde-3-phosphate dehydrogenase, reducing NAD+ to NADH.
4. Substrate-Level Phosphorylation: High-energy phosphate transfers from 1,3-bisphosphoglycerate and phosphoenolpyruvate (PEP) yield 4 ATP molecules.
Net Energy Yield:
- From Free Glucose: Net yield of 2 ATP per glucose molecule.
- From Muscle Glycogen: Net yield of 3 ATP per glucosyl unit.
Pyruvate Fate: To regenerate cytosolic NAD+ to keep glycolysis functioning, lactate dehydrogenase (LDH) reduces pyruvate to lactate, converting NADH back to NAD+."""
    },
    {
        "doc_id": "P1_37_LACTATE_METABOLISM_SHUTTLE",
        "section_title": "THE LACTATE SHUTTLE AND METABOLIC CLEARANCE KINETICS",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_BIOENERGETICS",
        "text": """Lactate is not a toxic waste product or the primary cause of muscular fatigue; rather, it represents a vital metabolic fuel and signaling molecule linking glycolytic and oxidative energy pathways.
Key physiological mechanisms of the Cell-Cell and Intracellular Lactate Shuttle:
1. Protons and Acidosis: The production of lactate via lactate dehydrogenase actually consumes a myoplasmic proton (pyruvate + NADH + H+ -> lactate + NAD+), actively delaying rather than causing intracellular acidosis. Metabolic acidosis is driven by the rapid turnover of ATP (ATP hydrolysis: ATP -> ADP + Pi + H+), releasing protons faster than cellular buffering systems can absorb them.
2. Monocarboxylate Transporters (MCTs): Lactate and protons are co-transported across the sarcolemma by specialized monocarboxylate transporters:
   - MCT4: Highly expressed in fast-twitch glycolytic fibers, specialized for exporting lactate out of active myocytes into the bloodstream.
   - MCT1: Highly expressed in slow-twitch oxidative fibers and cardiac myocytes, specialized for importing circulating lactate from blood into cells.
3. Oxidative Utilization: Once imported into oxidative myocytes or the myocardium, lactate is converted back to pyruvate by LDH and transported into the mitochondria, entering the Krebs cycle to produce aerobic ATP.
4. The Cori Cycle: Circulating lactate is extracted by hepatocytes in the liver and converted back into glucose via gluconeogenesis, releasing fresh glucose into the circulation."""
    },
    {
        "doc_id": "P1_38_AEROBIC_OXIDATIVE_PHOSPHORYLATION",
        "section_title": "OXIDATIVE BIOENERGETICS: KREBS CYCLE AND MITOCHONDRIAL RESPIRATORY CHAIN",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_BIOENERGETICS",
        "text": """The aerobic oxidative energy system resides within the mitochondria, providing nearly unlimited ATP resynthesis capacity for submaximal physical activity and post-exercise recovery.
1. Entry of Substrates (Acetyl-CoA):
   - Carbohydrates: Pyruvate enters the mitochondrial matrix and is converted to acetyl-CoA by the pyruvate dehydrogenase (PDH) multienzyme complex.
   - Lipids: Fatty acids undergo mitochondrial beta-oxidation, repeatedly cleaving two-carbon acetyl groups into acetyl-CoA.
2. The Tricarboxylic Acid (TCA / Krebs) Cycle: Acetyl-CoA condenses with oxaloacetate to form citrate. Through eight cyclical enzymatic reactions, each acetyl-CoA yields 3 NADH, 1 FADH2, 1 GTP (equivalent to ATP), and 2 CO2 molecules.
3. The Electron Transport Chain (ETC):
   - Electron Transfer: High-energy electrons from NADH and FADH2 pass sequentially through Complexes I, II, III, and IV embedded in the inner mitochondrial membrane.
   - Proton Gradient: Electron transport drives the active pumping of protons (H+) from the mitochondrial matrix into the intermembrane space, generating a steep electrochemical proton gradient (proton-motive force).
   - Chemiosmotic ATP Synthesis: Protons flow back down their electrochemical gradient into the matrix through Complex V (ATP synthase), driving rotational catalysis that phosphorylates ADP and Pi into ATP.
   - Final Electron Acceptor: Molecular oxygen (O2) acts as the terminal electron acceptor, binding protons to form water (H2O). Total ATP yield per mole of glucose is approximately 30 to 32 ATP."""
    },
    {
        "doc_id": "P1_39_CARDIOVASCULAR_FICK_EQUATION",
        "section_title": "CARDIOVASCULAR INTEGRATION: THE FICK EQUATION AND VO2 KINETICS",
        "source_id": "US-HHS-PAGAC-REPORT",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_CARDIOVASCULAR",
        "text": """Maximal oxygen consumption (VO2max) represents the maximal volume of oxygen that the human body can transport and metabolically utilize per unit of time during incremental exhaustive physical exertion.
The physiological determinants of VO2 are governed by the Fick Equation:
VO2 = Q x a-vO2 difference
Where:
- Q = Cardiac Output (L/min) = Heart Rate (beats/min) x Stroke Volume (L/beat).
- a-vO2 difference = Arteriovenous Oxygen Difference (mL O2 / 100 mL blood), reflecting peripheral oxygen extraction by working skeletal muscle tissue.
Central vs Peripheral Factors:
1. Central (Cardiac Delivery): In healthy endurance athletes, VO2max is primarily limited centrally by maximal cardiac output, which is dictated by left ventricular stroke volume. Chronic endurance training induces physiological eccentric ventricular hypertrophy, expanding end-diastolic volume and stroke volume via the Frank-Starling mechanism.
2. Peripheral (Extraction and Utilization): Skeletal muscle capillary density, myoglobin concentration, and mitochondrial enzyme activity determine how efficiently circulating oxygen is extracted from arterial blood, expanding the a-vO2 difference from roughly 5 mL O2 / 100 mL blood at rest up to 15 to 18 mL O2 / 100 mL during maximal exercise."""
    },
    {
        "doc_id": "P1_40_RESPIRATORY_GAS_EXCHANGE",
        "section_title": "PULMONARY MECHANICS: VENTILATORY THRESHOLDS AND RESPIRATORY COMPENSATION",
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "topic_domain": "exercise_science_biomechanics",
        "group_id": "GRP_P1_CARDIOVASCULAR",
        "text": """During incremental exercise, pulmonary ventilation (VE) responds dynamically to arterial blood gas fluctuations and metabolic byproducts:
1. First Ventilatory Threshold (VT1 / Aerobic Threshold):
   - At low to moderate exercise intensities, ventilation rises linearly with oxygen consumption (VO2).
   - As exercise intensity reaches VT1 (roughly 50% to 65% of VO2max), blood lactate begins to rise modestly above resting baseline. Bicarbonate buffering of protons produces non-metabolic carbon dioxide (H+ + HCO3- <-> H2CO3 <-> H2O + CO2).
   - The increased volume of expired CO2 (VCO2) stimulates carotid and central chemoreceptors, causing VE to increase disproportionately relative to VO2, marking the breakpoint where the ventilatory equivalent for oxygen (VE/VO2) begins to rise while VE/VCO2 remains flat.
2. Second Ventilatory Threshold (VT2 / Respiratory Compensation Point / Anaerobic Threshold):
   - At higher intensities (> 75% to 85% of VO2max), metabolic acidosis exceeds bicarbonate buffering capacity, causing blood pH to drop significantly.
   - Acidemia exerts intense drive on arterial chemoreceptors, triggering acute hyperventilation. VE increases disproportionately relative to both VO2 and VCO2 (VE/VCO2 rises sharply).
   - Training between VT1 and VT2 represents the 'tempo / threshold' physiological zone, while training above VT2 is sustainable for only brief intervals."""
    }
]
