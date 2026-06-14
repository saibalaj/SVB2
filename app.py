import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# --- Enterprise CSS Architecture Layout Control (SVB2) ---
st.set_page_config(page_title="SVB2 Pro", page_icon="🧬", layout="wide")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #0f141c; color: #e2e8f0; }
    [data-testid="stSidebar"] { background-color: #1a202c; }
    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white; font-weight: bold; border: none; border-radius: 8px; width: 100%; padding: 12px;
    }
    .metric-card {
        background: #1e293b; padding: 20px; border-radius: 10px;
        border: 1px solid #334155; margin-bottom: 12px;
    }
    .clinical-card {
        background: #1e1b4b; padding: 18px; border-radius: 8px;
        border-left: 5px solid #6366f1; margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- SQLite Persistent Layer Setup ---
def init_database_layer():
    conn = sqlite3.connect('svb2_core.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS system_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS performance_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, weight REAL, log_date TEXT)''')
    conn.commit()
    return conn

conn = init_database_layer()

def encrypt_pass(password): return hashlib.sha256(str.encode(password)).hexdigest()

# --- Balanced Multi-Target Indian Local Database Dictionary ---
INDIAN_7DAY_CORE = {
    "Veg": {
        "Monday": "🌅 Breakfast: Sattu Shake (30g Sattu powder + Water/Buttermilk) [High Protein, Cheap] + 50g Roasted Peanuts.\n\n🏙️ Lunch: Rice/Roti + Thick Dal Tadka + 100g Paneer/Tofu stir fry.\n\n🌆 Evening Snack: 1 Cup Curd (Dahi) + Soaked Chana.\n\n🌃 Dinner: Soy Chunks Curry (50g Soy blocks) + 2 Chapatis + Green Salad.",
        "Tuesday": "🌅 Breakfast: Oats Upma mixed with Sprouts and green peas + 1 Glass Lassi.\n\n🏙️ Lunch: Rajma (Kidney Beans) Thick Gravy + 1 Bowl Brown Rice + Beetroot Salad.\n\n🌆 Evening Snack: Roasted Makhana with Pumpkin Seeds (Zinc for Testosterone).\n\n🌃 Dinner: Mixed Vegetable & Paneer Bhurji + 2 Rotis + Buttermilk.",
        "Wednesday": "🌅 Breakfast: Moong Dal Cheela (Stuffed with 50g grated Paneer) + Green Chutney.\n\n🏙️ Lunch: Black Chana (Kala Chana) Curry + Rice/Roti + Cucumber Curd Raita.\n\n🌆 Evening Snack: Sattu Drink with Roasted Cumin Powder.\n\n🌃 Dinner: Palak Paneer (Spinach & Paneer) [Iron for Hair Growth] + 2 Whole Wheat Rotis.",
        "Thursday": "🌅 Breakfast: Peanut Butter Toast (2 Slices) + 1 Glass Cow Milk + 5 Soaked Almonds.\n\n🏙️ Lunch: Whole Green Moong Dal + Jowar/Bajra Roti + Cabbage Sabzi.\n\n🌆 Evening Snack: Sprouts Chaat (Onion, Tomato, Lemon Juice for Vitamin C).\n\n🌃 Dinner: Tofu or Paneer Kebabs (Pan Fried) + Vegetable Khichdi + Curd.",
        "Friday": "🌅 Breakfast: Besan Cheela with Flaxseeds + 100g Low-fat Curd.\n\n🏙️ Lunch: Lobia (Black Eyed Peas) Curry + Rice + Large Green Onion Salad.\n\n🌆 Evening Snack: Handful of Roasted Peanuts & Chana Mixture.\n\n🌃 Dinner: Soy Chunk Pulav + Mixed Veg Raita + Mint Leaves Chutney.",
        "Saturday": "🌅 Breakfast: 1 Bowl Milk Oats + 1 Tablespoon Chia Seeds + 1 Banana [Sleep Induction].\n\n🏙️ Lunch: Dal Makhani (Low Cream) + 2 Roti + Stir Fried Cauliflower & Carrot.\n\n🌆 Evening Snack: Buttermilk with Ginger & Cumin Powder.\n\n🌃 Dinner: Paneer Butter Masala (Homemade, low oil) + 2 Missi Rotis + Cucumber.",
        "Sunday": "🌅 Breakfast: Mixed Sprouts Salad with Pomegranate & Lemon + Sattu Shake.\n\n🏙️ Lunch: Choled (Chickpeas) Gravy + Zeera Rice + Onion Tomato Salad.\n\n🌆 Evening Snack: Roasted Pumpkin Seeds + Green Tea.\n\n🌃 Dinner: Kadhi Chawal / Roti + Paneer chunks pan toasted with Black Pepper."
    },
    "Non-Veg": {
        "Monday": "🌅 Breakfast: 3 Whole Boiled Eggs + 1 Glass Milk + Handful of Peanuts [Budget Testosterone Booster].\n\n🏙️ Lunch: Chicken Breast (150g, Stew/Gravy) + Brown Rice + Salad.\n\n🌆 Evening Snack: 3 Egg White Scramble with onions and green chilies.\n\n🌃 Dinner: Fish Curry (Rohu/Bangda - Omega 3 for Hair & Joints) + 2 Chapatis.",
        "Tuesday": "🌅 Breakfast: Chicken Keema Stuffed Roti (2) + 1 Glass Buttermilk.\n\n🏙️ Lunch: Thick Dal Tadka + 3 Egg White Omelette + Rice + Veggies.\n\n🌆 Evening Snack: Sattu Shake + 2 Boiled Eggs (No Yolk).\n\n🌃 Dinner: Grilled/Tandoori Chicken Chunks + 1 Roti + Large Salad Platter.",
        "Wednesday": "🌅 Breakfast: 3 Scrambled Eggs + 2 Slices Whole Wheat Bread + 5 Almonds.\n\n🏙️ Lunch: Mutton Keema or Dense Lean Meat Gravy + 2 Rotis + Curd Raita.\n\n🌆 Evening Snack: Roasted Pumpkin Seeds + 2 Boiled Egg Whites.\n\n🌃 Dinner: Chicken Clear Soup + 150g Baked Fish + Steamed Broccoli/Carrot.",
        "Thursday": "🌅 Breakfast: Oats cooked with 1 scoop Whey or 3 Egg Whites + 1 Banana.\n\n🏙️ Lunch: Egg Curry (2 Whole Eggs) + Rice/Roti + Cabbage & Onion Sabzi.\n\n🌆 Evening Snack: Chicken Salad (Leftover chicken pieces + Lemon + Cucumber).\n\n🌃 Dinner: Soya Chunks and Egg White Combo Rice + Mixed Vegetable Raita.",
        "Friday": "🌅 Breakfast: 3 Egg White Omelette with Spinach + 1 Glass Fresh Lassi.\n\n🏙️ Lunch: Chicken Biryani (Homemade, controlled oil) + 1 Big Bowl Cucumber Raita.\n\n🌆 Evening Snack: Roasted Chana + 2 Boiled Egg Whites.\n\n🌃 Dinner: Fish Fry (Tawa fried, low oil) + 2 Whole Wheat Chapatis + Salad.",
        "Saturday": "🌅 Breakfast: Sattu Shake + 2 Whole Boiled Eggs [High energy, Zero fatigue].\n\n🏙️ Lunch: Black Chana Dal + 150g Boneless Chicken Gravy + Brown Rice.\n\n🌆 Evening Snack: Mixed Seeds (Pumpkin, Sunflower) + Milk Tea (No sugar).\n\n🌃 Dinner: Minced Meat (Keema) Curry + 2 Rotis + Tossed Salad.",
        "Sunday": "🌅 Breakfast: 3 Eggs Omelette with Mushrooms [Vitamin D & Zinc] + 2 Toast Slices.\n\n🏙️ Lunch: Homestyle Mutton/Chicken Gravy + Rice + Sliced Beetroot & Onion.\n\n🌆 Evening Snack: 1 Cup Plain Curd + 30g Almonds.\n\n🌃 Dinner: Baked Chicken Chunks + Veggie Salad + Warm Turmeric Milk [Sleep Support]."
    }
}

# --- Core Algorithmic Session State Initialization ---
if "auth" not in st.session_state:
    st.session_state.auth = {"login": False, "user": "", "role": "User"}

# --- Login & Authentication Gateway Layout ---
if not st.session_state.auth["login"]:
    st.title("🛡️ SVB2 - Secure Gateway")
    t1, t2 = st.tabs(["🔒 Secure Login", "📝 New Account Access Creation"])
    
    with t1:
        u_in = st.text_input("Username Identifier", key="l_user")
        p_in = st.text_input("Password Secure String", type="password", key="l_pass")
        if st.button("Authenticate System Nodes"):
            c = conn.cursor()
            c.execute("SELECT role FROM system_users WHERE username=? AND password=?", (u_in, encrypt_pass(p_in)))
            res = c.fetchone()
            if res:
                st.session_state.auth = {"login": True, "user": u_in, "role": res[0]}
                st.rerun()
            else: st.error("Invalid Authentication Parameters Provided.")
            
    with t2:
        u_rg = st.text_input("Choose Unique Handle", key="r_user")
        p_rg = st.text_input("Set Multi-Character Passphrase", type="password", key="r_pass")
        r_rl = st.selectbox("Assign Baseline Authorization Level", ["User", "Admin"])
        if st.button("Commit Node Entry to Database"):
            if u_rg and p_rg:
                try:
                    c = conn.cursor()
                    c.execute("INSERT INTO system_users (username, password, role) VALUES (?, ?, ?)", (u_rg, encrypt_pass(p_rg), r_rl))
                    conn.commit()
                    st.success("Entry Saved Successfully! Check Login Tab.")
                except sqlite3.IntegrityError: st.error("Target Handle Already Reserved.")
else:
    # --- Contextual Execution Variables ---
    usr = st.session_state.auth["user"]
    perm = st.session_state.auth["role"]
    
    with st.sidebar:
        st.markdown(f"### SVB2 Pro")
        st.markdown(f"👤 Active Session: `{usr}`")
        st.markdown(f"🔑 Clearance: `{perm}`")
        if st.button("🔒 Terminate App Session"):
            st.session_state.auth = {"login": False, "user": "", "role": "User"}
            st.rerun()

    if perm == "Admin":
        st.title("👑 SVB2 - Infrastructure Admin Management Panel")
        c = conn.cursor()
        c.execute("SELECT id, username, role FROM system_users")
        st.dataframe(c.fetchall(), use_container_width=True)
    else:
        st.title("🩺 SVB2 - Clinical Dietitian & Diagnostics Platform")
        
        in_col, view_col = st.columns([1, 2])
        
        with in_col:
            st.subheader("📋 Advanced Medical Screener Profiles")
            g = st.radio("Biological Gender", ["Male", "Female"], horizontal=True)
            a = st.slider("Age Track Range", 16, 95, 27)
            h = st.number_input("Absolute Height (cm)", min_value=120, max_value=240, value=173)
            w = st.number_input("Recorded Body Mass (kg)", min_value=32, max_value=260, value=75)
            gl = st.selectbox("Primary Physical Matrix Target", ["Weight Loss", "Maintain Weight", "Muscle Gain"])
            dt = st.radio("Diet Choice Framework", ["Veg", "Non-Veg"], horizontal=True)
            
            st.write("---")
            st.subheader("🧠 Neuro-Somatic Inputs")
            stress = st.select_slider("Subjective Chronic Stress Levels", ["Low", "Moderate (Normal)", "High - Burnout Phase"])
            sleep_hrs = st.slider("Average Circadian Sleep Cycles (Hours)", 4, 10, 7)
            
            meds = st.multiselect(
                "Diagnosed Pathological Markers / System Conflicts",
                ["None", "Poor Digestion / Gut Dysbiosis", "Chronic Fatigue Syndrome", "Hair Thinning / Alopecia", "Low Energy Levels"]
            )
            
            # Historical SQLite Database Logs Trigger Section
            st.write("---")
            st.subheader("📉 Structural Log Node Updates")
            up_w = st.number_input("Log Instantaneous Weight Point (kg)", min_value=30.0, max_value=250.0, step=0.1, value=float(w))
            if st.button("Commit Datapoint To SQL Disk"):
                c = conn.cursor()
                c.execute("INSERT INTO performance_logs (username, weight, log_date) VALUES (?, ?, ?)", (usr, up_w, datetime.now().strftime('%Y-%m-%d')))
                conn.commit()
                st.toast("Biometric Frame Sync Complete!")

        with view_col:
            st.subheader("📊 Algorithmic Diagnostics & Macro Allocations")
            
            # Processing Mathematical Formulations
            h_m_unit = h / 100
            calculated_bmi = round(w / (h_m_unit ** 2), 1)
            
            if g == "Male": base_bmr = int((10 * w) + (6.25 * h) - (5 * a) + 5)
            else: base_bmr = int((10 * w) + (6.25 * h) - (5 * a) - 161)
            
            calculated_tdee = int(base_bmr * 1.4) 
            
            if gl == "Weight Loss": target_cal = calculated_tdee - 450
            elif gl == "Muscle Gain": target_cal = calculated_tdee + 450
            else: target_cal = calculated_tdee
            
            prot_target = int((target_cal * 0.32) / 4)
            carb_target = int((target_cal * 0.43) / 4)
            fat_target = int((target_cal * 0.25) / 9)
            
            # Visual Matrix Block
            grid_1, grid_2, grid_3, grid_4 = st.columns(4)
            grid_1.markdown(f"<div class='metric-card'><h5>Calculated BMI</h5><h3>{calculated_bmi}</h3></div>", unsafe_allow_html=True)
            grid_2.markdown(f"<div class='metric-card'><h5>Base BMR</h5><h3>{base_bmr} kcal</h3></div>", unsafe_allow_html=True)
            grid_3.markdown(f"<div class='metric-card'><h5>TDEE Burn</h5><h3>{calculated_tdee} kcal</h3></div>", unsafe_allow_html=True)
            grid_4.markdown(f"<div class='metric-box' style='background:#1e1b4b; padding:20px; border-radius:10px; border:1px solid #6366f1;'><h5>Target Intake</h5><h3>{target_cal} kcal</h3></div>", unsafe_allow_html=True)
            
            st.info(f"💡 **Target High-Protein Targets Required:** Protein: `{prot_target}g` | Carbohydrates: `{carb_target}g` | Fats: `{fat_target}g`")
            
            # Dynamic Neuro-Clinical Rules Mapping Engine
            st.write("---")
            st.subheader("🩺 SVB2 Integrated Holistic Protocols")
            
            if "Poor Digestion / Gut Dysbiosis" in meds:
                st.markdown("<div class='clinical-card'><b>🥣 Gut Microbiome & Digestion Optimization:</b> Increase fermented enzymes. Consume 150g home-made Curd (Dahi) or Buttermilk twice daily. Avoid wheat completely for 10 days; replace with Jowar or Rice. Drink warm water with fennel seeds post meals.</div>", unsafe_allow_html=True)
            
            if "Hair Thinning / Alopecia" in meds or gl == "Weight Loss":
                st.markdown("<div class='clinical-card'><b>💇‍♀️ Follicle Density & Hair Growth Protocol:</b> Hair structure requires Keratin protein. Your current budget-rich profile includes Curry leaves, Flaxseeds, and Eggs/Soya. Ensure your daily iron and zinc metrics are protected via pumpkin seeds.</div>", unsafe_allow_html=True)
                
            if "Chronic Fatigue Syndrome" in meds or stress == "High - Burnout Phase":
                st.markdown("<div class='clinical-card'><b>⚡ Adrenal Fatigue & Neuroendocrine Recovery:</b> Your cortisol curve is high, dropping energy markers. Integrate <b>Ashwagandha powder</b> (3g with warm milk before sleep). Increase hydration baseline. Avoid caffeine intake after 2:00 PM.</div>", unsafe_allow_html=True)

            if g == "Male":
                st.markdown("<div class='clinical-card' style='border-left-color: #10b981;'><b>🧪 Endogenous Testosterone Optimization Matrix:</b> Free testosterone profiles drop due to micronutrient deficiency. Ensure adequate intake of healthy cholesterol (Egg yolks or Peanuts) alongside magnesium-dense seeds. Avoid processed seed oils completely.</div>", unsafe_allow_html=True)

            h2o_target = round((w * 35) / 1000, 1)
            st.success(f"💧 **Hydration Command:** Drink exactly **{h2o_target} Liters** of filtered water daily to accelerate fat loss parameters.")

            # Display Planned Data Matrices
            st.write("---")
            st.subheader("📅 High-Protein Economical 7-Day Indian Routine Execution")
            current_diet_matrix = INDIAN_7DAY_CORE[dt]
            for day_node, diet_description in current_diet_matrix.items():
                with st.expander(f"📅 View Menu Parameters for {day_node}"):
                    st.write(diet_description)
            
            # Generate Internal Line Graph Trends
            st.write("---")
            st.subheader("📈 Historical Mass Calibration Vectors")
            c = conn.cursor()
            c.execute("SELECT weight, log_date FROM performance_logs WHERE username=? ORDER BY log_date ASC", (usr,))
            logged_series = c.fetchall()
            if logged_series:
                series_data = {node[1]: node[0] for node in logged_series}
                st.line_chart(series_data)
            else: st.info("No recorded trends stored in database yet.")

            # Dynamic Report Generation Execution Flow Blocks
            st.write("---")
            pdf_out_name = f"{usr}_svb2_report.pdf"
            if st.button("📑 Compile Encrypted PDF Health Diagnostic Record"):
                doc_file = SimpleDocTemplate(pdf_out_name, pagesize=letter)
                styles_setup = getSampleStyleSheet()
                elements_flow = [
                    Paragraph(f"SVB2 Clinical Assessment Breakdown", styles_setup['Heading1']),
                    Spacer(1, 12),
                    Paragraph(f"Target Patient Identity: {usr}", styles_setup['Normal']),
                    Paragraph(f"Computed Body Mass Index: {calculated_bmi}", styles_setup['Normal']),
                    Paragraph(f"Calculated Target Caloric Requirement: {target_cal} kcal/day", styles_setup['Normal']),
                    Paragraph(f"Assigned Protein Allocation Parameter: {prot_target}g", styles_setup['Normal']),
                ]
                doc_file.build(elements_flow)
                
                with open(pdf_out_name, "rb") as asset_block:
                    st.download_button(label="📥 Download Compiled Local PDF Assessment", data=asset_block, file_name=pdf_out_name, mime="application/pdf")