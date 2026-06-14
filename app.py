import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- SVB2 Advanced Core Theme Setup & Responsive Layout ---
st.set_page_config(page_title="SVB2 Pro Ecosystem", page_icon="🧬", layout="wide")

# Force adaptive contrast so letters never bleed or disappear on light/dark backgrounds
st.markdown("""
<style>
    /* Global Dynamic Tokens based on system theme */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-color: #0d1117;
            --text-color: #f0f6fc;
            --card-bg: #161b22;
            --border-color: #30363d;
            --accent-glow: #00f2fe;
            --muted-text: #8b949e;
        }
    }
    @media (prefers-color-scheme: light) {
        :root {
            --bg-color: #f6f8fa;
            --text-color: #24292f;
            --card-bg: #ffffff;
            --border-color: #d0d7de;
            --accent-glow: #059669;
            --muted-text: #57606a;
        }
    }

    /* Override dynamic styles to fix font visibility blending */
    .svb2-title {
        color: var(--text-color) !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em;
    }
    .svb2-card {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 14px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
    }
    .svb2-badge {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border-left: 5px solid var(--accent-glow) !important;
        border-top: 1px solid var(--border-color) !important;
        border-right: 1px solid var(--border-color) !important;
        border-bottom: 1px solid var(--border-color) !important;
        padding: 14px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
    .svb2-metric-val {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        font-family: monospace !important;
        color: var(--text-color) !important;
    }
    .svb2-muted {
        color: var(--muted-text) !important;
        font-size: 0.85rem;
        margin-bottom: 4px;
    }
    .svb2-workout-line {
        margin-bottom: 8px !important;
        line-height: 1.6 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SQLite Persistent Layer Setup ---
def init_database_layer():
    conn = sqlite3.connect('svb2_core.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS system_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)''')
    conn.commit()
    return conn

conn = init_database_layer()

def encrypt_pass(password): 
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- Balanced Multi-Target Indian Local Database Dictionary ---
INDIAN_7DAY_CORE = {
    "Veg": {
        "Monday": "Breakfast: Sattu Shake (30g Sattu powder + Buttermilk) + 50g Roasted Peanuts + 5 Soaked Almonds & 2 Walnuts. | Lunch: Rice/Roti + Thick Dal Tadka + 100g Paneer/Tofu stir fry in 1 tsp Ghee + Salad (High Fibre Broccoli/Carrots). | Evening Snack: 1 Cup Curd (Dahi) + Soaked Chana. | Dinner: Soy Chunks Curry + 2 Chapatis + Green Salad + Half Avocado.",
        "Tuesday": "Breakfast: Oats Upma mixed with High-Fibre Sprouts & green peas + 1 Glass Lassi + Peanut Butter Toast. | Lunch: Rajma Thick Gravy + 1 Bowl Brown Rice + Beetroot & Cucumber Salad. | Evening Snack: Roasted Makhana in Coconut Oil with Pumpkin Seeds. | Dinner: Mixed Vegetable & Paneer Bhurji + 2 Rotis + Buttermilk.",
        "Wednesday": "Breakfast: Moong Dal Cheela (Stuffed with 50g grated Paneer) + Green Chutney + 5 Almonds & 2 Walnuts. | Lunch: Black Chana Curry + Rice/Roti + Cucumber Curd Raita. | Evening Snack: Sattu Drink + Roasted Cumin Powder. | Dinner: Palak Paneer cooked with 1 tsp Ghee + 2 Whole Wheat Rotis.",
        "Thursday": "Breakfast: Peanut Butter Toast (2 Slices) + 1 Glass Cow Milk + 5 Soaked Almonds + Half Avocado. | Lunch: Whole Green Moong Dal + Jowar/Bajra Roti + Cabbage Sabzi cooked in Coconut Oil. | Evening Snack: High-Fibre Sprouts Chaat (Onion, Tomato, Lemon Juice). | Dinner: Tofu or Paneer Kebabs + Vegetable Khichdi + Curd.",
        "Friday": "Breakfast: Besan Cheela with Flaxseeds + 100g Low-fat Curd + 5 Almonds. | Lunch: Lobia Curry + Rice + Large Green Onion & Carrot Salad. | Evening Snack: Handful of Roasted Peanuts & Chana Mixture. | Dinner: Soy Chunk Pulav cooked in 1 tsp Ghee + Mixed Veg Raita.",
        "Saturday": "Breakfast: 1 Bowl Milk Oats + 1 tbsp Chia Seeds + 1 Banana + 2 Walnuts. | Lunch: Dal Makhani (Low Cream) + 2 Roti + Stir Fried High-Fibre Cauliflower & Carrot. | Evening Snack: Buttermilk with Ginger & Cumin Powder. | Dinner: Paneer Butter Masala (Low oil) + 2 Missi Rotis + Cucumber + Avocado slices.",
        "Sunday": "Breakfast: Mixed Sprouts Salad with Pomegranate & Lemon + Sattu Shake + 5 Almonds. | Lunch: Chole Gravy + Jeera Rice + Onion Tomato & High-Fibre Salad. | Evening Snack: Roasted Pumpkin Seeds + Green Tea. | Dinner: Kadhi Chawal / Roti + Paneer chunks pan toasted with Black Pepper in 1 tsp Ghee."
    },
    "Non-Veg": {
        "Monday": "Breakfast: 3 Whole Boiled Eggs + 1 Glass Milk + Handful of Peanuts + 5 Soaked Almonds & 2 Walnuts. | Lunch: Chicken Breast (150g, Stew/Gravy cooked in 1 tsp Ghee) + Brown Rice + High-Fibre Salad. | Evening Snack: 3 Egg White Scramble + Peanut Butter Toast. | Dinner: Fish Curry (Rohu/Bangda) + 2 Chapatis + Half Avocado.",
        "Tuesday": "Breakfast: Chicken Keema Stuffed Roti (2) + 1 Glass Buttermilk + 5 Almonds. | Lunch: Thick Dal Tadka + 3 Egg White Omelette cooked in Coconut Oil + Rice + Veggies. | Evening Snack: Sattu Shake + 2 Boiled Eggs (No Yolk). | Dinner: Grilled/Tandoori Chicken Chunks + 1 Roti + Large High-Fibre Salad Platter.",
        "Wednesday": "Breakfast: 3 Scrambled Eggs in 1 tsp Ghee + 2 Slices Whole Wheat Bread + 5 Almonds & 2 Walnuts. | Lunch: Mutton Keema Gravy + 2 Rotis + Curd Raita. | Evening Snack: Roasted Pumpkin Seeds + 2 Boiled Egg Whites + Half Avocado. | Dinner: Chicken Clear Soup + 150g Baked Fish + Steamed Broccoli/Carrot.",
        "Thursday": "Breakfast: Oats cooked with 3 Egg Whites + 1 Banana + 1 tbsp Peanut Butter. | Lunch: Egg Curry (2 Whole Eggs cooked in Coconut Oil) + Rice/Roti + Cabbage & Onion Sabzi. | Evening Snack: Chicken Salad (Leftover chicken pieces + Lemon + Cucumber). | Dinner: Soya Chunks and Egg White Combo Rice + Mixed Vegetable Raita.",
        "Friday": "Breakfast: 3 Egg White Omelette with Spinach + 1 Glass Fresh Lassi + 5 Almonds. | Lunch: Chicken Biryani (Controlled oil) + 1 Big Bowl High-Fibre Cucumber Raita. | Evening Snack: Roasted Chana + 2 Boiled Egg Whites. | Dinner: Fish Fry (Tawa fried in Coconut Oil) + 2 Whole Wheat Chapatis + Salad.",
        "Saturday": "Breakfast: Sattu Shake + 2 Whole Boiled Eggs + 2 Walnuts. | Lunch: Black Chana Dal + 150g Boneless Chicken Gravy cooked in 1 tsp Ghee + Brown Rice. | Evening Snack: Mixed Seeds + Half Avocado. | Dinner: Minced Meat (Keema) Curry + 2 Rotis + Tossed High-Fibre Salad.",
        "Sunday": "Breakfast: 3 Eggs Omelette with Mushrooms & 1 tsp Ghee + 2 Toast Slices with Peanut Butter. | Lunch: Homestyle Mutton/Chicken Gravy + Rice + Sliced Beetroot & Onion High-Fibre Salad. | Evening Snack: 1 Cup Plain Curd + 30g Almonds. | Dinner: Baked Chicken Chunks + Veggie Salad + Warm Turmeric Milk."
    }
}

# --- Core Algorithmic Session State Initialization ---
if "auth" not in st.session_state:
    st.session_state.auth = {"login": False, "user": "", "role": "User"}

# --- Login & Authentication Gateway Layout ---
if not st.session_state.auth["login"]:
    st.markdown("<h1 class='svb2-title'>🧬 SVB2 — Core Health Panel</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔒 Secure Authorization", "📝 Registration Node"])
    
    with t1:
        u_in = st.text_input("User ID Token", key="l_user")
        p_in = st.text_input("Secure Keyphrase", type="password", key="l_pass")
        if st.button("Authenticate Platform Access"):
            c = conn.cursor()
            c.execute("SELECT role FROM system_users WHERE username=? AND password=?", (u_in, encrypt_pass(p_in)))
            res = c.fetchone()
            if res:
                st.session_state.auth = {"login": True, "user": u_in, "role": res[0]}
                st.rerun()
            else: 
                st.error("Invalid Authentication Parameters Provided.")
            
    with t2:
        u_rg = st.text_input("Create Handle ID", key="r_user")
        p_rg = st.text_input("Create Password", type="password", key="r_pass")
        r_rl = st.selectbox("Baseline Authority Tier", ["User", "Admin"])
        if st.button("Commit Account Registry"):
            if u_rg and p_rg:
                try:
                    c = conn.cursor()
                    c.execute("INSERT INTO system_users (username, password, role) VALUES (?, ?, ?)", (u_rg, encrypt_pass(p_rg), r_rl))
                    conn.commit()
                    st.success("Registration complete! Swap to Login Tab.")
                except sqlite3.IntegrityError: 
                    st.error("Handle registration conflict. Pick another name.")
else:
    usr = st.session_state.auth["user"]
    perm = st.session_state.auth["role"]
    
    with st.sidebar:
        st.markdown("<h2 class='svb2-title' style='color:#059669;'>SVB2 INTEGRATED</h2>", unsafe_allow_html=True)
        st.markdown(f"👤 Account: `{usr}`")
        st.markdown(f"🔑 Tier: `{perm}`")
        if st.button("🔒 Terminate App Session"):
            st.session_state.auth = {"login": False, "user": "", "role": "User"}
            st.rerun()

    if perm == "Admin":
        st.markdown("<h1 class='svb2-title'>👑 Infrastructure Data Table</h1>", unsafe_allow_html=True)
        c = conn.cursor()
        c.execute("SELECT id, username, role FROM system_users")
        st.dataframe(c.fetchall(), use_container_width=True)
    else:
        st.markdown("<h1 class='svb2-title'>🩺 SVB2 — Diagnostics & Clinical Platform</h1>", unsafe_allow_html=True)
        
        in_col, view_col = st.columns([1, 2])
        
        with in_col:
            st.markdown("<h4 class='svb2-title'>📋 Biometric Inputs</h4>", unsafe_allow_html=True)
            g = st.radio("Biological Gender", ["Male", "Female"], horizontal=True)
            a = st.slider("Age Track Range", 16, 95, 26)
            h = st.number_input("Absolute Height (cm)", min_value=120, max_value=240, value=173)
            w = st.number_input("Recorded Body Mass (kg)", min_value=32, max_value=260, value=90)
            gl = st.selectbox("Primary Physical Matrix Target", ["Weight Loss", "Maintain Weight", "Muscle Gain"])
            dt = st.radio("Diet Choice Framework", ["Veg", "Non-Veg"], horizontal=True)
            
            st.write("---")
            st.markdown("<h4 class='svb2-title'>🧠 Neuro-Somatic Inputs</h4>", unsafe_allow_html=True)
            stress = st.select_slider("Subjective Chronic Stress Levels", ["Low", "Moderate (Normal)", "High - Burnout Phase"])
            sleep_hrs = st.slider("Average Circadian Sleep Cycles (Hours)", 4, 10, 7)
            
            meds = st.multiselect(
                "Diagnosed Pathological Markers",
                ["None", "Poor Digestion / Gut Dysbiosis", "Chronic Fatigue Syndrome", "Hair Thinning / Alopecia", "Low Energy Levels"]
            )

        with view_col:
            st.markdown("<h4 class='svb2-title'>📊 Automated Target Quantities</h4>", unsafe_allow_html=True)
            
            # Formulating Calculations
            h_m_unit = h / 100
            calculated_bmi = round(w / (h_m_unit ** 2), 1)
            
            if g == "Male": 
                base_bmr = int((10 * w) + (6.25 * h) - (5 * a) + 5)
            else: 
                base_bmr = int((10 * w) + (6.25 * h) - (5 * a) - 161)
            
            calculated_tdee = int(base_bmr * 1.4) 
            
            if gl == "Weight Loss": 
                target_cal = calculated_tdee - 450
            elif gl == "Muscle Gain": 
                target_cal = calculated_tdee + 450
            else: 
                target_cal = calculated_tdee
            
            # --- Fixed Precise Caloric Distribution Split Formulas ---
            prot_target = int((target_cal * 0.30) / 4)
            fat_target = int((target_cal * 0.25) / 9)
            carb_target = int((target_cal - (prot_target * 4) - (fat_target * 9)) / 4)
            
            # KPI Matrix Grid Configuration (Fully Dynamic Font Protection)
            grid_1, grid_2, grid_3, grid_4 = st.columns(4)
            grid_1.markdown(f"<div class='svb2-card'><div class='svb2-muted'>BMI Index</div><div class='svb2-metric-val'>{calculated_bmi}</div></div>", unsafe_allow_html=True)
            grid_2.markdown(f"<div class='svb2-card'><div class='svb2-muted'>Base BMR</div><div class='svb2-metric-val'>{base_bmr} <span style='font-size:0.8rem;'>kcal</span></div></div>", unsafe_allow_html=True)
            grid_3.markdown(f"<div class='svb2-card'><div class='svb2-muted'>TDEE Burn</div><div class='svb2-metric-val'>{calculated_tdee} <span style='font-size:0.8rem;'>kcal</span></div></div>", unsafe_allow_html=True)
            grid_4.markdown(f"<div class='svb2-card' style='border: 1px solid var(--accent-glow) !important;'><div class='svb2-muted' style='color:var(--accent-glow); font-weight:bold;'>Target Intake</div><div class='svb2-metric-val' style='color:var(--accent-glow);'>{target_cal} <span style='font-size:0.8rem;'>kcal</span></div></div>", unsafe_allow_html=True)
            
            st.info(f"💡 **Calculated Chunks Required:** Protein: `{prot_target}g` | Carbohydrates: `{carb_target}g` | Fats: `{fat_target}g`")
            
            # --- Workout & Cardio Programs Integration Module ---
            st.write("---")
            st.markdown("<h4 class='svb2-title'>🏋️‍♂️ SVB2 Integrated Physical Transformation Mechanics</h4>", unsafe_allow_html=True)
            
            w_tabs = st.tabs(["💪 5-Day PPL Custom Split", "🏃‍♂️ Cardio & Stamina Protocol", "🏸 Competitive Sports Integration"])
            
            # Algorithmic parameter updates based on chosen configuration metrics
            if gl == "Weight Loss":
                focus_title = "Metabolic Conditioning PPL (Fat Loss + Endurance)"
                rep_text_1 = "15-25+ reps"
                rep_text_2 = "High reps/Supersets"
                rest_limit = "30–45 sec short recovery"
            else:
                focus_title = "Powerbuilding / Hypertrophy PPL (Strength + Size Volume)"
                rep_text_1 = "3x6-8 heavy load parameters"
                rep_text_2 = "3x8-10 or 3x10-15 volume sets"
                rest_limit = "60–90 sec rest tracking"
                
            with w_tabs[0]:
                st.markdown(f"""
                <div class='svb2-badge'>
                    <b>⚡ 5-Day Professional Dynamic Routine Layout (Push-Pull-Legs-Push-Pull):</b>
                    <br><b>Current Protocol Focus:</b> {focus_title} | <b>Target Rest Window:</b> {rest_limit}
                </div>
                <div class='svb2-workout-line'>🔹 <b>Monday (Push):</b> Muscles: Chest, shoulders, triceps — Bench ({rep_text_1 if gl == 'Weight Loss' else '3×6-8'}), Shoulder Press ({rep_text_1 if gl == 'Weight Loss' else '3×8-10'}), Flyes (3×10-15), Triceps (3×10-15)</div>
                <div class='svb2-workout-line'>🔹 <b>Tuesday (Pull):</b> Muscles: Back, biceps, rear delts — Rows ({rep_text_1 if gl == 'Weight Loss' else '3×6-8'}), Pull-ups ({rep_text_1 if gl == 'Weight Loss' else '3×8-10'}), Face Pulls (3×10-15), Shrugs (3×8-10)</div>
                <div class='svb2-workout-line'>🔹 <b>Wednesday (Legs):</b> Muscles: Quads, hamstrings, glutes, calves — Squats ({rep_text_1 if gl == 'Weight Loss' else '3×6-8'}), RDLs ({rep_text_1 if gl == 'Weight Loss' else '3×6-8'}), Leg Press (3×8-10), Leg Curls (3×8-10), Calves (3-4 sets)</div>
                <div class='svb2-workout-line'>🔹 <b>Thursday (Push):</b> Muscles: Chest, shoulders, triceps — Incline Press ({rep_text_2}), Lateral Raises ({rep_text_2}), Dips ({rep_text_2}), Overhead Extensions ({rep_text_2})</div>
                <div class='svb2-workout-line'>🔹 <b>Friday (Pull):</b> Muscles: Back, biceps, rear delts — Chin-ups ({rep_text_2}), Single-Arm Rows ({rep_text_2}), Rear Delt Flyes ({rep_text_2}), Hammer Curls ({rep_text_2})</div>
                <div class='svb2-workout-line' style='color:var(--muted-text); font-style: italic;'>⚠️ <b>Saturday & Sunday:</b> Rest and Systematic Recovery Cycles.</div>
                """, unsafe_allow_html=True)
                
            with w_tabs[1]:
                st.markdown("""
                <div class='svb2-badge'>
                    <b>🏃‍♂️ Strategic Caloric Burn & Respiratory Endurance:</b>
                </div>
                <div class='svb2-workout-line'>🏃‍♂️ <b>LISS Cardio:</b> 35 Minutes of Incline Treadmill Walking (Speed: 5.0 km/h, Incline: 6%-8%)</div>
                <div class='svb2-workout-line'>🚴‍♂️ <b>HIIT Cardio:</b> 15 Minutes Stationary Cycle Matrix — 30s sprint / 60s slow recovery pace</div>
                <div class='svb2-workout-line'>👣 <b>Circadian Baseline Step Metrics:</b> Maintain a strict floor of 8,000 to 10,000 tracked steps daily</div>
                """, unsafe_allow_html=True)
                
            with w_tabs[2]:
                st.markdown("""
                <div class='svb2-badge'>
                    <b>🏸 Functional Athletics & Neuromuscular Reflex Vectors:</b>
                </div>
                <div class='svb2-workout-line'>🏸 <b>Recommended Sports Structure:</b> Badminton / Squash or Swimming. Play for 45-60 minutes on Wednesday or Sunday.</div>
                """, unsafe_allow_html=True)

            st.write("---")
            st.markdown("<h4 class='svb2-title'>🩺 Integrated Holistic Protocols</h4>", unsafe_allow_html=True)
            
            if "Poor Digestion / Gut Dysbiosis" in meds:
                st.markdown("<div class='svb2-badge'><b>🥣 Gut Microbiome & Digestion Optimization:</b> Increase fermented enzymes. Consume 150g home-made Curd (Dahi) or Buttermilk twice daily.</div>", unsafe_allow_html=True)
            
            if "Hair Thinning / Alopecia" in meds or gl == "Weight Loss":
                st.markdown("<div class='svb2-badge'><b>💇‍♀️ Follicle Density & Hair Growth Protocol:</b> Hair structure requires Keratin protein. Ensure your daily iron and zinc metrics are protected.</div>", unsafe_allow_html=True)
                
            if "Chronic Fatigue Syndrome" in meds or stress == "High - Burnout Phase":
                st.markdown("<div class='svb2-badge'><b>⚡ Adrenal Fatigue & Neuroendocrine Recovery:</b> Integrate 3g Ashwagandha powder with warm milk before sleep.</div>", unsafe_allow_html=True)

            h2o_target = round((w * 35) / 1000, 1)
            st.success(f"💧 **Hydration Command:** Drink exactly **{h2o_target} Liters** of filtered water daily.")

            # Display Planned Data Matrices
            st.write("---")
            st.markdown("<h4 class='svb2-title'>📅 High-Protein Economical 7-Day Indian Routine (Fibre & Healthy Fats Enriched)</h4>", unsafe_allow_html=True)
            current_diet_matrix = INDIAN_7DAY_CORE[dt]
            for day_node, diet_description in current_diet_matrix.items():
                with st.expander(f"📅 View Menu Parameters for {day_node}"):
                    st.write(diet_description.replace(" | ", "\n\n"))

            # --- Master PDF Blueprint Compilation Execution (Diet, Sleep, Water & Workouts) ---
            st.write("---")
            st.markdown("<h4 class='svb2-title'>📑 Master Blueprint Download Gateway</h4>", unsafe_allow_html=True)
            pdf_out_name = f"{usr}_svb2_master_report.pdf"
            
            if st.button("📑 Generate Master PDF Health & Workout Blueprint"):
                doc_file = SimpleDocTemplate(pdf_out_name, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
                styles_setup = getSampleStyleSheet()
                
                # Custom Document Style Tokens
                style_header = ParagraphStyle('DocHeader', parent=styles_setup['Heading1'], fontSize=22, textColor=colors.HexColor('#059669'), spaceAfter=15)
                style_section = ParagraphStyle('DocSec', parent=styles_setup['Heading2'], fontSize=14, textColor=colors.HexColor('#1e293b'), spaceBefore=12, spaceAfter=6)
                style_body = ParagraphStyle('DocBody', parent=styles_setup['Normal'], fontSize=10, leading=16, spaceAfter=8)
                
                elements_flow = [
                    Paragraph(f"SVB2 MASTER HEALTH & FITNESS BLUEPRINT", style_header),
                    Paragraph(f"<b>Generated On:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", style_body),
                    Paragraph(f"<b>User Profile:</b> {usr} | <b>Gender:</b> {g} | <b>Age:</b> {a} years", style_body),
                    Spacer(1, 10),
                ]
                
                # SECTION 1: CORE BIOMETRIC METRICS TABLE
                elements_flow.append(Paragraph("1. Calculated Caloric & Macro Allocation", style_section))
                metric_table_data = [
                    ["Metric Parameter", "Target Allocation Value"],
                    ["Current BMI Index", f"{calculated_bmi}"],
                    ["Basal Metabolic Rate (BMR)", f"{base_bmr} kcal"],
                    ["Total Daily Energy Expenditure (TDEE)", f"{calculated_tdee} kcal"],
                    ["Target Daily Caloric Intake", f"{target_cal} kcal"],
                    ["Protein Target Split", f"{prot_target} g"],
                    ["Carbohydrates Target Split", f"{carb_target} g"],
                    ["Fats Target Split", f"{fat_target} g"]
                ]
                t_metrics = Table(metric_table_data, colWidths=[230, 230])
                t_metrics.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (1,0), colors.HexColor('#059669')),
                    ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                ]))
                elements_flow.append(t_metrics)
                elements_flow.append(Spacer(1, 12))
                
                # SECTION 2: LIFE RECOVERY PROTOCOLS (WATER & SLEEP)
                elements_flow.append(Paragraph("2. Circadian Recovery & Hydration Parameters", style_section))
                recovery_text = f"""
                • <b>Target Circadian Sleep Frame:</b> Expected strict target of <b>{sleep_hrs} Hours</b> per 24-hour cycle.<br/>
                • <b>Absolute Hydration Target:</b> Drink exactly <b>{h2o_target} Liters</b> of pure water daily.<br/>
                • <b>Somatic Stress Marker Level:</b> System registered as <i>{stress}</i>.
                """
                elements_flow.append(Paragraph(recovery_text, style_body))
                elements_flow.append(Spacer(1, 10))
                
                # SECTION 3: INTEGRATED PHYSICAL TRANSFORMATION WORKOUT MATRIX (PDF Version)
                elements_flow.append(Paragraph("3. Resistance Training & Cardio Splits Blueprint", style_section))
                workout_text = f"""
                <b>A. 5-Day Custom Workout Target System (Phase: {gl}):</b><br/>
                • <b>Workout Focus Type:</b> {focus_title}<br/>
                • <b>Rest Matrix Floor:</b> {rest_limit}<br/><br/>
                • <b>Monday (Push):</b> Muscles: Chest, shoulders, triceps — Bench ({rep_text_1 if gl == 'Weight Loss' else '3×6-8'}), Shoulder Press ({rep_text_1 if gl == 'Weight Loss' else '3×8-10'}), Flyes (3×10-15), Triceps (3×10-15)<br/>
                • <b>Tuesday (Pull):</b> Muscles: Back, biceps, rear delts — Rows ({rep_text_1 if gl == 'Weight Loss' else '3×6-8'}), Pull-ups ({rep_text_1 if gl == 'Weight Loss' else '3×8-10'}), Face Pulls (3×10-15), Shrugs (3×8-10)<br/>
                • <b>Wednesday (Legs):</b> Muscles: Quads, hamstrings, glutes, calves — Squats ({rep_text_1 if gl == 'Weight Loss' else '3×6-8'}), RDLs ({rep_text_1 if gl == 'Weight Loss' else '3×6-8'}), Leg Press (3×8-10), Leg Curls (3×8-10), Calves<br/>
                • <b>Thursday (Push):</b> Muscles: Chest, shoulders, triceps — Incline Press ({rep_text_2}), Lateral Raises ({rep_text_2}), Dips ({rep_text_2}), Overhead Extensions ({rep_text_2})<br/>
                • <b>Friday (Pull):</b> Muscles: Back, biceps, rear delts — Chin-ups ({rep_text_2}), Single-Arm Rows ({rep_text_2}), Rear Delt Flyes ({rep_text_2}), Hammer Curls ({rep_text_2})<br/><br/>
                <b>B. Stamina & Cardio Framework:</b><br/>
                • LISS Cardio: 35 Mins Incline Treadmill Walking (5.0 km/h, 6%-8% incline) post lifting.<br/>
                • HIIT Cardio: 15 Mins Stationary Cycling (30s max sprint / 60s recovery interval).<br/>
                • Daily Target Activity Base: Maintain a floor of 8,000 - 10,000 steps daily.
                """
                elements_flow.append(Paragraph(workout_text, style_body))
                elements_flow.append(Spacer(1, 10))
                
                # SECTION 4: DIET ROUTINE ASSIGNMENTS
                elements_flow.append(Paragraph("4. Economical 7-Day Nutritional Routine Log (Fibre & Fats Enriched)", style_section))
                diet_table_data = [["Day Node", f"Planned Plan Matrix Breakdown ({dt})"]]
                for day, desc in current_diet_matrix.items():
                    clean_desc = desc.replace(" | ", "<br/><br/>")
                    diet_table_data.append([day, Paragraph(clean_desc, style_body)])
                
                t_diet = Table(diet_table_data, colWidths=[70, 430])
                t_diet.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (1,0), colors.HexColor('#1e293b')),
                    ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('FONTNAME', (0,0), (1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                ]))
                elements_flow.append(t_diet)
                
                doc_file.build(elements_flow)
                
                with open(pdf_out_name, "rb") as asset_block:
                    st.download_button(label="📥 Download Master PDF Fitness Blueprint", data=asset_block, file_name=pdf_out_name, mime="application/pdf")
