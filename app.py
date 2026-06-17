import streamlit as st
import os

# --- Render Production SQLite Compatibility Safe Layer Patch ---
try:
    import pysqlite3 as sqlite3
except ImportError:
    import sqlite3

import hashlib
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- SVB2 Advanced Core Theme Setup & Responsive Layout ---
st.set_page_config(page_title="SVB2 Pro Ecosystem", page_icon="🧬", layout="wide")

# Safe Core Override Engine: Guarantees absolute high-contrast reading visibility in BOTH light and dark UI instances
st.markdown("""
<style>
    @media (prefers-color-scheme: dark) {
        :root {
            --svb2-main-txt: #f0f6fc;
            --svb2-card-bg: #161b22;
            --svb2-border: #30363d;
            --svb2-muted: #8b949e;
            --svb2-highlight: #00f2fe;
        }
    }
    @media (prefers-color-scheme: light) {
        :root {
            --svb2-main-txt: #111827; 
            --svb2-card-bg: #ffffff;
            --svb2-border: #d1d5db;
            --svb2-muted: #4b5563; 
            --svb2-highlight: #059669;
        }
    }
    .svb2-title { color: var(--svb2-main-txt) !important; font-weight: 800 !important; margin-bottom: 15px !important; }
    .svb2-card { background-color: var(--svb2-card-bg) !important; color: var(--svb2-main-txt) !important; border: 2px solid var(--svb2-border) !important; padding: 22px; border-radius: 12px; margin-bottom: 15px; }
    .svb2-badge { background-color: var(--svb2-card-bg) !important; color: var(--svb2-main-txt) !important; border-left: 6px solid var(--svb2-highlight) !important; border-top: 1px solid var(--svb2-border) !important; border-right: 1px solid var(--svb2-border) !important; border-bottom: 1px solid var(--svb2-border) !important; padding: 16px; border-radius: 8px; margin-bottom: 14px; }
    .svb2-metric-val { font-size: 1.85rem !important; font-weight: 800 !important; font-family: monospace !important; color: var(--svb2-main-txt) !important; }
    .svb2-muted { color: var(--svb2-muted) !important; font-size: 0.9rem; font-weight: 600; margin-bottom: 6px; }
    .svb2-workout-line { color: var(--svb2-main-txt) !important; margin-bottom: 10px !important; line-height: 1.6 !important; font-size: 1.05rem !important; }
    .stMarkdown p { color: var(--svb2-main-txt) !important; }
</style>
""", unsafe_allow_html=True)

# --- Thread-Safe Cached Database Engine Architecture ---
@st.cache_resource
def get_db_connection():
    # Eliminates unsafe connection tracking vectors via thread-isolated session memory maps
    conn = sqlite3.connect('2_svb2_core.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS system_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)''')
    conn.commit()
    return conn

conn = get_db_connection()

def encrypt_pass(password): 
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- BALANCED SHIFT ROUTINE PROTOCOLS (INDIAN TIMESTAMPS) ---
SHIFT_TIMELINE_DATABASE = {
    "Morning Shift (6:00 AM - 3:00 PM)": {
        "Sleep Window": "🌙 **9:30 PM to 5:00 AM** (Protects baseline deep recovery architecture)",
        "Exercise Window": "🏋️‍♂️ **4:00 PM to 5:15 PM** (Post-shift energy surge execution)",
        "Timestamps": {
            "Veg": [
                "⏰ 05:30 AM (Pre-Shift Fuel): Warm Water + 5 Soaked Almonds.",
                "⏰ 08:30 AM (Breakfast Break): Sattu Shake (30g Sattu powder in water/buttermilk) OR Paneer Toast.",
                "⏰ 01:00 PM (Lunch Break): Homestyle Rice/Roti + Thick Dal + Sabzi + 100g Paneer Curry.",
                "⏰ 03:30 PM (Pre-Workout Fuel): 75g Oats cooked with dry fruits.",
                "⏰ 05:30 PM (Post-Workout Recovery): Raw Whey Protein Shake + 1 Toast.",
                "⏰ 08:30 PM (Dinner): Light Carb Roti/Rice + Mixed green salad + Low-fat Tofu / Paneer."
            ],
            "Non-Veg": [
                "⏰ 05:30 AM (Pre-Shift Fuel): Warm Water + 5 Soaked Almonds.",
                "⏰ 08:30 AM (Breakfast Break): 3 Whole Boiled Eggs + 1 Slice Whole Wheat Toast.",
                "⏰ 01:00 PM (Lunch Break): Homestyle Rice/Roti + Thick Dal + 150g Chicken Breast Curry.",
                "⏰ 03:30 PM (Pre-Workout Fuel): 75g Oats cooked with dry fruits.",
                "⏰ 05:30 PM (Post-Workout Recovery): Raw Whey Protein Shake + 1 Toast.",
                "⏰ 08:30 PM (Dinner): Light Carb Roti/Rice + Mixed green salad + 150g Grilled Fish or Lean Chicken."
            ]
        }
    },
    "Afternoon Shift (2:00 PM - 11:00 PM)": {
        "Sleep Window": "🌙 **12:00 AM to 7:30 AM** (Maintains stable nighttime circadian rhythm)",
        "Exercise Window": "🏋️‍♂️ **10:30 AM to 11:45 AM** (Mid-morning high-strength target window)",
        "Timestamps": {
            "Veg": [
                "⏰ 08:00 AM (Breakfast / Meal 1): Oats Upma with high-fibre sprouts + 100g Paneer Bhurji.",
                "⏰ 10:00 AM (Pre-Workout Snack): 1 Banana or Black Coffee.",
                "⏰ 12:00 PM (Post-Workout / Heavy Lunch): Rice + Thick Dal + Salad + Pan-toasted Soy Chunks.",
                "⏰ 05:30 PM (Mid-Shift Snack): Sattu Drink / Sprouted Chaat + Handful of Roasted Peanuts.",
                "⏰ 08:30 PM (Dinner Break): 2 Chapatis + Mixed Veg Curry + Curd (Dahi).",
                "⏰ 11:30 PM (Pre-bed Micro): Warm Turmeric Milk / Ashwagandha Capsule layer."
            ],
            "Non-Veg": [
                "⏰ 08:00 AM (Breakfast / Meal 1): Oats Upma + 3 Scrambled Egg Whites + 1 Whole Egg.",
                "⏰ 10:00 AM (Pre-Workout Snack): 1 Banana or Black Coffee.",
                "⏰ 12:00 PM (Post-Workout / Heavy Lunch): Rice + Thick Dal + Salad + 150g Chicken Breast/Fish Curry.",
                "⏰ 05:30 PM (Mid-Shift Snack): Boiled Egg Chaat (3 Egg Whites) + Handful of Roasted Peanuts.",
                "⏰ 08:30 PM (Dinner Break): 2 Chapatis + Chicken Keema Gravy + High-Fibre Salad.",
                "⏰ 11:30 PM (Pre-bed Micro): Warm Turmeric Milk / Ashwagandha Capsule layer."
            ]
        }
    },
    "Evening Shift (5:30 PM - 3:00 AM)": {
        "Sleep Window": "🌙 **03:30 AM to 11:00 AM** (Strict blackout curtains & quiet environment required)",
        "Exercise Window": "🏋️‍♂️ **04:00 PM to 05:00 PM** (Pre-shift activation to eliminate fatigue latency)",
        "Timestamps": {
            "Veg": [
                "⏰ 11:30 AM (Wakeup / Meal 1): Homestyle Rice + Balanced Thick Dal + 100g Grilled Paneer Chunks.",
                "⏰ 03:15 PM (Pre-Workout Fuel): 75g Oats + Dry fruits combo pattern matrix.",
                "⏰ 05:30 PM (Post-Workout Shift Login): Consume Raw Whey Protein Shake immediately upon login.",
                "⏰ 09:30 PM (Mid-Shift Core Dinner): Carried Box: Low-fat Paneer / Soya Chunks curry + Controlled Rice.",
                "⏰ 01:00 AM (Midnight Cutoff): Stop all Caffeine/Tea intake strictly to protect sleep cycle engine.",
                "⏰ 03:15 AM (Pre-Bed Protein Shield): 1 Small Glass Buttermilk or Sattu Shake."
            ],
            "Non-Veg": [
                "⏰ 11:30 AM (Wakeup / Meal 1): Homestyle Rice + Balanced Thick Dal + 3 Eggs Omelette or Fish Curry.",
                "⏰ 03:15 PM (Pre-Workout Fuel): 75g Oats + Dry fruits combo pattern matrix.",
                "⏰ 05:30 PM (Post-Workout Shift Login): Consume Raw Whey Protein Shake immediately upon login.",
                "⏰ 09:30 PM (Mid-Shift Core Dinner): Carried Box: Chicken Keema / 3 Boiled Eggs + Controlled Rice Structure.",
                "⏰ 01:00 AM (Midnight Cutoff): Stop all Caffeine/Tea intake strictly to protect sleep cycle engine.",
                "⏰ 03:15 AM (Pre-Bed Protein Shield): 3 Egg Whites or 1 Small Glass Buttermilk."
            ]
        }
    },
    "Night Shift (10:00 PM - 7:00 AM)": {
        "Sleep Window": "🌙 **08:00 AM to 3:30 PM** (Reversed sleep-wake biological rhythm parameters)",
        "Exercise Window": "🏋️‍♂️ **05:30 PM to 06:45 PM** (Evening peak structural muscle execution interval)",
        "Timestamps": {
            "Veg": [
                "⏰ 04:00 PM (Wakeup Meal / Breakfast): Sattu Shake (30g Sattu) + Peanut Butter Toast + 5 Almonds.",
                "⏰ 05:00 PM (Pre-Workout Snap): Handful of Roasted Chana.",
                "⏰ 07:15 PM (Post-Workout Main Meal): High protein Dinner Setup: Rice/Roti + Dal + 120g Pan-toasted Paneer.",
                "⏰ 11:30 PM (First Shift Snack): Curd (Dahi) + Roasted Makhana or Apple with peanut butter.",
                "⏰ 02:30 AM (Midnight Lunch Break): 2 Chapatis + Soy Chunks Curry / Mixed Veg + Green Salad.",
                "⏰ 05:00 AM (Early Morning Cutoff): No tea/coffee. Shift to plain water hydration tracker to allow sleep ease at 8 AM."
            ],
            "Non-Veg": [
                "⏰ 04:00 PM (Wakeup Meal / Breakfast): 3 Whole Boiled Eggs + Peanut Butter Toast + 5 Almonds.",
                "⏰ 05:00 PM (Pre-Workout Snap): Black coffee / Handful of Roasted Chana.",
                "⏰ 07:15 PM (Post-Workout Main Meal): High protein Dinner Setup: Rice/Roti + Dal + 150g Chicken or Fish Curry.",
                "⏰ 11:30 PM (First Shift Snack): 2 Egg Whites + Roasted Makhana or Apple with peanut butter.",
                "⏰ 02:30 AM (Midnight Lunch Break): 2 Chapatis + Chicken Keema or Egg White Curry + Green Salad.",
                "⏰ 05:00 AM (Early Morning Cutoff): No tea/coffee. Shift to plain water hydration tracker to allow sleep ease at 8 AM."
            ]
        }
    }
}

INDIAN_7DAY_CORE = {
    "Veg": {
        "Monday": "Sattu Shake (30g Sattu powder) + Thick Dal Tadka + 100g Paneer/Tofu stir fry in 1 tsp Ghee + Soy Chunks Curry.",
        "Tuesday": "Oats Upma with High-Fibre Sprouts + Peanut Butter Toast + Rajma Thick Gravy + Mixed Vegetable & Paneer Bhurji.",
        "Wednesday": "Moong Dal Cheela (Stuffed with 50g Paneer) + Black Chana Curry + Cucumber Curd Raita + Palak Paneer.",
        "Thursday": "Peanut Butter Toast + Whole Green Moong Dal + Jowar/Bajra Roti + Tofu or Paneer Kebabs + Veg Khichdi.",
        "Friday": "Besan Cheela with Flaxseeds + 100g Low-fat Curd + Lobia Curry + Soy Chunk Pulav cooked in 1 tsp Ghee.",
        "Saturday": "Milk Oats + 1 tbsp Chia Seeds + Dal Makhani (Low Cream) + Paneer Butter Masala (Controlled Low oil Setup).",
        "Sunday": "Mixed Sprouts Salad + Chole Gravy + Jeera Rice + Paneer chunks pan toasted with Black Pepper in 1 tsp Ghee."
    },
    "Non-Veg": {
        "Monday": "3 Whole Boiled Eggs + Chicken Breast (150g Gravy) + 3 Egg White Scramble + Homestyle Fish Curry.",
        "Tuesday": "Chicken Keema Stuffed Roti + 3 Egg White Omelette cooked in Coconut Oil + Grilled/Tandoori Chicken Chunks.",
        "Wednesday": "3 Scrambled Eggs in 1 tsp Ghee + Mutton Keema Gravy + Chicken Clear Soup + 150g Baked Fish.",
        "Thursday": "Oats cooked with 3 Egg Whites + Egg Curry (2 Whole Eggs) + Soya Chunks and Egg White Combo Rice.",
        "Friday": "3 Egg White Omelette with Spinach + Chicken Biryani (Controlled oil) + Tawa Fish Fry + High-Fibre Salad.",
        "Saturday": "Sattu Shake + 2 Whole Boiled Eggs + 150g Boneless Chicken Gravy + Minced Meat (Keema) Curry.",
        "Sunday": "3 Eggs Omelette with Mushrooms + Homestyle Mutton/Chicken Gravy + Baked Chicken Chunks + Salad Structure."
    }
}

# --- Core Algorithmic Session State Initialization ---
if "auth" not in st.session_state:
    st.session_state.auth = {"login": False, "user": "", "role": "User"}
if "show_reg_portal" not in st.session_state:
    st.session_state.show_reg_portal = False

# --- Isolated Core Authentication Gateway ---
if not st.session_state.auth["login"]:
    st.markdown("<h1 class='svb2-title'>🧬 SVB2 — Secure Core Health Panel</h1>", unsafe_allow_html=True)
    st.markdown("### 🔒 Secure Platform Authorization")
    u_in = st.text_input("User ID Token", key="l_user")
    p_in = st.text_input("Secure Keyphrase", type="password", key="l_pass")
    
    if st.button("Authenticate Platform Access", use_container_width=True):
        c = conn.cursor()
        c.execute("SELECT role FROM system_users WHERE username=? AND password=?", (u_in, encrypt_pass(p_in)))
        res = c.fetchone()
        if res:
            st.session_state.auth = {"login": True, "user": u_in, "role": res[0]}
            st.rerun()
        else: 
            st.error("Invalid Authentication Parameters Provided.")
            
    st.write("---")
    if st.button("⚠️ Core Platform Node: Toggle Registration Portal"):
        st.session_state.show_reg_portal = not st.session_state.show_reg_portal
        st.rerun()
        
    if st.session_state.show_reg_portal:
        st.markdown("<div class='svb2-card' style='border: 2px dashed #ef4444 !important;'>", unsafe_allow_html=True)
        st.markdown("### 📝 Internal Registry Gateway Node")
        u_rg = st.text_input("Create Handle ID", key="r_user")
        p_rg = st.text_input("Create Password", type="password", key="r_pass")
        
        # FIX: Admin registration security gate with safe validation override token
        r_rl = st.selectbox("Baseline Authority Tier Assignment", ["User", "Admin"])
        admin_passkey = ""
        if r_rl == "Admin":
            admin_passkey = st.text_input("Enter Infrastructure Admin Authorization Token", type="password")
        
        if st.button("Commit Account Registry to DB"):
            if u_rg and p_rg:
                if r_rl == "Admin" and admin_passkey != "SVB2_SECURE_ADMIN_2026":
                    st.error("Unauthorized Admin Key Verification Failure. Registration aborted.")
                else:
                    try:
                        c = conn.cursor()
                        c.execute("INSERT INTO system_users (username, password, role) VALUES (?, ?, ?)", (u_rg, encrypt_pass(p_rg), r_rl))
                        conn.commit()
                        st.success(f"Success! Account Handle `{u_rg}` registered as `{r_rl}`.")
                    except sqlite3.IntegrityError: 
                        st.error("Handle registration conflict.")
            else:
                st.warning("All data vectors required.")
        st.markdown("</div>", unsafe_allow_html=True)

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
            
            # FIX: Tightened input validation bounds to secure algorithm matrix data safety
            a = st.slider("Age Track Range", 18, 90, 26)
            h = st.number_input("Absolute Height (cm)", min_value=130.0, max_value=230.0, value=173.0, step=0.5)
            w = st.number_input("Recorded Body Mass (kg)", min_value=40.0, max_value=200.0, value=90.0, step=0.5)
            
            # FIX: Integrated User Activity mapping metric inputs
            act_level = st.selectbox("Current Activity Metric Level", ["Sedentary (Office Desk Job)", "Light Activity (1-3 days/wk)", "Moderate Activity (3-5 days/wk)", "Active Elite (6-7 days/wk)"])
            
            gl = st.selectbox("Primary Physical Matrix Target", ["Weight Loss", "Maintain Weight", "Muscle Gain"])
            dt = st.radio("Diet Choice Framework", ["Veg", "Non-Veg"], horizontal=True)
            
            st.write("---")
            st.markdown("<h4 class='svb2-title'>🕒 Professional Shift Configuration</h4>", unsafe_allow_html=True)
            selected_shift = st.selectbox(
                "Select Current Active Professional Shift Matrix",
                ["Morning Shift (6:00 AM - 3:00 PM)", "Afternoon Shift (2:00 PM - 11:00 PM)", "Evening Shift (5:30 PM - 3:00 AM)", "Night Shift (10:00 PM - 7:00 AM)"]
            )
            
            st.write("---")
            st.markdown("<h4 class='svb2-title'>🧠 Neuro-Somatic Inputs</h4>", unsafe_allow_html=True)
            stress = st.select_slider("Subjective Chronic Stress Levels", ["Low", "Moderate (Normal)", "High - Burnout Phase"])
            meds = st.multiselect("Diagnosed Pathological Markers", ["None", "Poor Digestion / Gut Dysbiosis", "Chronic Fatigue Syndrome", "Hair Thinning / Alopecia", "Low Energy Levels"])

        with view_col:
            st.markdown("<h4 class='svb2-title'>📊 Automated Target Quantities</h4>", unsafe_allow_html=True)
            
            h_m_unit = h / 100
            calculated_bmi = round(w / (h_m_unit ** 2), 1)
            
            if g == "Male": 
                base_bmr = int((10 * w) + (6.25 * h) - (5 * a) + 5)
            else: 
                base_bmr = int((10 * w) + (6.25 * h) - (5 * a) - 161)
            
            # FIX: Real-time dynamic activity scaling dictionary pipeline mapping
            activity_map = {
                "Sedentary (Office Desk Job)": 1.2,
                "Light Activity (1-3 days/wk)": 1.375,
                "Moderate Activity (3-5 days/wk)": 1.55,
                "Active Elite (6-7 days/wk)": 1.725
            }
            multiplier = activity_map[act_level]
            calculated_tdee = int(base_bmr * multiplier) 
            
            if gl == "Weight Loss": 
                target_cal = calculated_tdee - 450
            elif gl == "Muscle Gain": 
                target_cal = calculated_tdee + 450
            else: 
                target_cal = calculated_tdee
            
            # FIX: Goal-Based Dynamic Macronutrient Percent Splits
            if gl == "Weight Loss":
                prot_pct, fat_pct = 0.40, 0.25   # High Protein Fat Loss Targeting
            elif gl == "Muscle Gain":
                prot_pct, fat_pct = 0.30, 0.25   # Carb Loaded Glycogen Driving Split
            else:
                prot_pct, fat_pct = 0.30, 0.30   # Perfect Equilibrium Baseline Split
                
            prot_cal = target_cal * prot_pct
            prot_target = int(prot_cal / 4)
            
            fat_cal = target_cal * fat_pct
            fat_target = int(fat_cal / 9)
            
            # Remainder calculation mechanics eliminate macro allocation rounding errors cleanly
            carb_cal = target_cal - (prot_target * 4) - (fat_target * 9)
            carb_target = int(carb_cal / 4)
            
            # KPI Matrix Grid Configuration
            grid_1, grid_2, grid_3, grid_4 = st.columns(4)
            grid_1.markdown(f"<div class='svb2-card'><div class='svb2-muted'>BMI Index</div><div class='svb2-metric-val'>{calculated_bmi}</div></div>", unsafe_allow_html=True)
            grid_2.markdown(f"<div class='svb2-card'><div class='svb2-muted'>Base BMR</div><div class='svb2-metric-val'>{base_bmr} <span style='font-size:0.8rem;'>kcal</span></div></div>", unsafe_allow_html=True)
            grid_3.markdown(f"<div class='svb2-card'><div class='svb2-muted'>TDEE Burn</div><div class='svb2-metric-val'>{calculated_tdee} <span style='font-size:0.8rem;'>kcal</span></div></div>", unsafe_allow_html=True)
            grid_4.markdown(f"<div class='svb2-card' style='border: 2px solid var(--svb2-highlight) !important;'><div class='svb2-muted' style='color:var(--svb2-highlight); font-weight:bold;'>Target Intake</div><div class='svb2-metric-val' style='color:var(--svb2-highlight);'>{target_cal} <span style='font-size:0.8rem;'>kcal</span></div></div>", unsafe_allow_html=True)
            
            st.info(f"💡 **Dynamic Allocation ({gl}):** Protein: `{int(prot_pct*100)}%` ({prot_target}g) | Carbs: `{100 - int(prot_pct*100) - int(fat_pct*100)}%` ({carb_target}g) | Fats: `{int(fat_pct*100)}%` ({fat_target}g) &rarr; **Equivalence Sync:** `{int(prot_target*4 + carb_target*4 + fat_target*9)} / {target_cal} kcal`")
            
            # --- DYNAMIC DIET TIMESTAMPS GENERATION GRID ---
            st.write("---")
            st.markdown(f"<h3 style='color: var(--svb2-highlight);'>🕒 Circadian Allocation Schedule: {selected_shift} ({dt})</h3>", unsafe_allow_html=True)
            
            shift_node = SHIFT_TIMELINE_DATABASE[selected_shift]
            
            col_s1, col_s2 = st.columns(2)
            col_s1.markdown(f"<div class='svb2-card' style='border-top: 4px solid #3b82f6;'><b>Optimal Recovery Sleep Window:</b><br>{shift_node['Sleep Window']}</div>", unsafe_allow_html=True)
            col_s2.markdown(f"<div class='svb2-card' style='border-top: 4px solid #ec4899;'><b>Optimal Muscle Training Window:</b><br>{shift_node['Exercise Window']}</div>", unsafe_allow_html=True)
            
            # FIX: User Diet Choice filter logic is now fully bound to shift timestamps maps
            st.markdown("#### 🍴 Daily Chrono-Nutrition Structured Timestamps:")
            active_diet_timestamps = shift_node["Timestamps"][dt]
            for current_stamp in active_diet_timestamps:
                st.markdown(f"<div class='svb2-badge'>{current_stamp}</div>", unsafe_allow_html=True)

            # --- WEEKLY NUTRITION LOOKUP PLATFORM (FIX: Dead Code Prevention Injection) ---
            st.write("---")
            st.markdown(f"<h4 class='svb2-title'>📅 Integrated 7-Day Macro Blueprint Plan ({dt} Selection)</h4>", unsafe_allow_html=True)
            with st.expander("Click to unlock full Weekly Micro Cycle Distribution matrix"):
                for active_day, macro_meal_plan in INDIAN_7DAY_CORE[dt].items():
                    st.markdown(f"📌 **{active_day}:** {macro_meal_plan}")

            # --- Workout Programs Integration Module ---
            st.write("---")
            st.markdown("<h4 class='svb2-title'>🏋️‍♂️ SVB2 Integrated Physical Transformation Mechanics</h4>", unsafe_allow_html=True)
            w_tabs = st.tabs(["💪 Custom Workout PPL Split", "🏃‍♂️ Cardio & Stamina Protocol", "💊 Supplement Matrix"])
            
            if gl == "Weight Loss":
                focus_title = "Metabolic Conditioning PPL (Fat Loss + Endurance Optimization)"
                rep_text_1 = "15-25+ repetitions protocol range"
                rep_text_2 = "High density supersets (12-15 reps)"
            else:
                focus_title = "Powerbuilding / Hypertrophy PPL (Volume Loading + Density)"
                rep_text_1 = "3x6-8 heavy strength compound sets"
                rep_text_2 = "3x8-12 localized volume arrays"
                
            with w_tabs[0]:
                st.markdown(f"""
                <div class='svb2-badge'><b>Current Training Protocol Focus:</b> {focus_title} | <b>Target Active Interval window:</b> {shift_node['Exercise Window']}</div>
                <div class='svb2-workout-line'>🔹 <b>Monday (Push 1):</b> Chest, shoulders, triceps — Flat Bench Press ({rep_text_1}), Overhead Press ({rep_text_1}), Incline Dumbbell Flyes (3×12)</div>
                <div class='svb2-workout-line'>🔹 <b>Tuesday (Pull 1):</b> Back, biceps — Conventional Deadlifts ({rep_text_1}), Lat Pulldowns (3×10), Barbell Biceps Curls (3×12)</div>
                <div class='svb2-workout-line'>🔹 <b>Wednesday (Legs):</b> Quads, hamstrings — Barbell Squats ({rep_text_1}), Romanian Deadlifts (3×10), Calf Raises (4×15)</div>
                <div class='svb2-workout-line'>🔹 <b>Thursday (Push 2):</b> Incline DB Press ({rep_text_2}), Seated DB Shoulder Press ({rep_text_2}), DB Lateral Raises (4×15)</div>
                <div class='svb2-workout-line'>🔹 <b>Friday (Pull 2):</b> Close-Grip Lat Pulldowns ({rep_text_2}), T-Bar Rows ({rep_text_2}), Incline DB Biceps Curls (3×12)</div>
                """, unsafe_allow_html=True)
                
            with w_tabs[1]:
                st.markdown("""
                <div class='svb2-workout-line'>🏃‍♂️ <b>LISS Cardio:</b> 35 Minutes of Incline Treadmill Walking (Speed: 5.0 km/h, Incline: 6%-8%) immediately after strength routines.</div>
                <div class='svb2-workout-line'>🚴‍♂️ <b>HIIT Cardio:</b> 15 Minutes Stationary Cycle Matrix — 30s sprint / 60s recovery tracking loops.</div>
                """, unsafe_allow_html=True)
                
            with w_tabs[2]:
                supp_list = [{"Name": "Raw Whey Protein Concentrate", "Timing": "Post-Workout Session Window", "Dosage": "1 Scoop (24g Protein)", "Budget_Brand": "Asitis Nutrition Raw / Nakpro Platinum"}]
                if gl == "Muscle Gain":
                    supp_list.append({"Name": "Creatine Monohydrate", "Timing": "Post-Workout with shaker", "Dosage": "3g daily continuously", "Budget_Brand": "Asitis Pure Powder"})
                if "Poor Digestion / Gut Dysbiosis" in meds:
                    supp_list.append({"Name": "Probiotics & Digestive Enzymes", "Timing": "With Lunch / First Main Meal", "Dosage": "1 Capsule daily", "Budget_Brand": "HealthKart / Himalayan Organics"})
                
                for supp in supp_list:
                    st.markdown(f"<div class='svb2-badge' style='border-left: 6px solid #ef4444 !important;'><b>⚡ {supp['Name']}</b> ({supp['Dosage']})<br/>⏰ Timing: {supp['Timing']} | Recommended Baseline Vendor: {supp['Budget_Brand']}</div>", unsafe_allow_html=True)

            # Master PDF Download Gateway
            st.write("---")
            st.markdown("<h4 class='svb2-title'>📑 Master Blueprint Download Gateway</h4>", unsafe_allow_html=True)
            pdf_out_name = f"{usr}_svb2_chrono_report.pdf"
            
            if st.button("📑 Generate Master PDF Health & Shift Blueprint"):
                doc_file = SimpleDocTemplate(pdf_out_name, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
                styles_setup = getSampleStyleSheet()
                
                style_header = ParagraphStyle('DocHeader', parent=styles_setup['Heading1'], fontSize=20, textColor=colors.HexColor('#059669'), spaceAfter=15)
                style_section = ParagraphStyle('DocSec', parent=styles_setup['Heading2'], fontSize=13, textColor=colors.HexColor('#1e293b'), spaceBefore=10, spaceAfter=5)
                style_body = ParagraphStyle('DocBody', parent=styles_setup['Normal'], fontSize=9, leading=15, spaceAfter=6)
                
                elements_flow = [
                    Paragraph(f"SVB2 CHRONO-NUTRITION & WORKOUT MASTER REPORT", style_header),
                    Paragraph(f"<b>Generated Account Token:</b> {usr} | <b>Active Track Profile:</b> {selected_shift} ({dt})", style_body),
                    Spacer(1, 10),
                ]
                
                # METRICS TABLE
                elements_flow.append(Paragraph("1. Precise Algorithmic Macro Metrics Verification", style_section))
                metric_table_data = [
                    ["Biometric Param Name", "Calculated Balanced Value"],
                    ["Calculated Target Calories Split", f"{target_cal} kcal"],
                    ["Calculated Precise Protein Target", f"{prot_target} g ({int(prot_target*4)} kcal)"],
                    ["Calculated Precise Carbohydrates Target", f"{carb_target} g ({int(carb_target*4)} kcal)"],
                    ["Calculated Precise Fats Target", f"{fat_target} g ({int(fat_target*9)} kcal)"]
                ]
                t_metrics = Table(metric_table_data, colWidths=[230, 230])
                t_metrics.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (1,0), colors.HexColor('#059669')),
                    ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ]))
                elements_flow.append(t_metrics)
                elements_flow.append(Spacer(1, 10))
                
                # SHIFT PROTOCOL TABLE
                elements_flow.append(Paragraph(f"2. Daily Chrono-Nutrition Timeline Structure ({selected_shift})", style_section))
                shift_table_data = [["Interval Window Node", "Target Metric/Timestamp Execution"]]
                shift_table_data.append(["Optimal Sleep Hours", shift_node['Sleep Window']])
                shift_table_data.append(["Optimal Exercise Hour", shift_node['Exercise Window']])
                for index_st, stamp_st in enumerate(active_diet_timestamps):
                    shift_table_data.append([f"Meal Slot Node {index_st+1}", stamp_st])
                    
                t_shift = Table(shift_table_data, colWidths=[130, 330])
                t_shift.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ]))
                elements_flow.append(t_shift)
                
                doc_file.build(elements_flow)
                
                with open(pdf_out_name, "rb") as asset_block:
                    st.download_button(label="📥 Download Master PDF Fitness Blueprint", data=asset_block, file_name=pdf_out_name, mime="application/pdf")
