import streamlit as st
import os
import hashlib
import sqlite3
from datetime import datetime, date, timedelta
from io import BytesIO

# ============================================================
# SQLITE COMPATIBILITY
# ============================================================
try:
    import pysqlite3 as sqlite3
except ImportError:
    import sqlite3

# ============================================================
# PDF
# ============================================================
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="HealthTrack",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# SYSTEM THEME + MODERN CSS
# ============================================================
st.markdown(
    """
<style>

:root {
    --app-radius: 18px;
    --app-shadow: 0 8px 30px rgba(0,0,0,0.08);
}

@media (prefers-color-scheme: light) {
    :root {
        --bg: #f6f8fb;
        --card: #ffffff;
        --card-soft: #f8fafc;
        --text: #111827;
        --muted: #64748b;
        --border: #e2e8f0;
        --primary: #16a34a;
        --primary-soft: #dcfce7;
        --secondary: #2563eb;
        --warning: #d97706;
        --danger: #dc2626;
        --input: #ffffff;
    }
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg: #0b1120;
        --card: #111827;
        --card-soft: #172033;
        --text: #f8fafc;
        --muted: #94a3b8;
        --border: #263449;
        --primary: #4ade80;
        --primary-soft: #12351f;
        --secondary: #60a5fa;
        --warning: #fbbf24;
        --danger: #f87171;
        --input: #111827;
    }
}

/* Main application */
.stApp {
    background: var(--bg);
    color: var(--text);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Text */
h1, h2, h3, h4, h5, h6,
p, label,
.stMarkdown,
.stText,
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: var(--text) !important;
}

.small-muted {
    color: var(--muted) !important;
    font-size: 0.88rem;
}

/* Cards */
.health-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--app-radius);
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: var(--app-shadow);
}

.health-card-soft {
    background: var(--card-soft);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 15px;
}

/* Header */
.health-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 25px;
}

.health-logo {
    width: 58px;
    height: 58px;
    border-radius: 17px;
    background: linear-gradient(135deg, #16a34a, #22c55e);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white !important;
    font-size: 30px;
    font-weight: 800;
    box-shadow: 0 8px 20px rgba(22,163,74,0.25);
}

.health-title {
    font-size: 2rem;
    font-weight: 850;
    color: var(--text) !important;
    margin: 0;
}

.health-subtitle {
    color: var(--muted) !important;
    margin: 3px 0 0 0;
}

/* Metrics */
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    box-shadow: var(--app-shadow);
    min-height: 125px;
}

.metric-label {
    color: var(--muted) !important;
    font-size: 0.88rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.metric-value {
    color: var(--text) !important;
    font-size: 1.8rem;
    font-weight: 850;
}

.metric-unit {
    color: var(--muted) !important;
    font-size: 0.85rem;
}

/* Macro cards */
.macro-card {
    border-radius: 15px;
    padding: 18px;
    background: var(--card);
    border: 1px solid var(--border);
}

.macro-title {
    font-size: 0.9rem;
    color: var(--muted) !important;
    font-weight: 700;
}

.macro-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--text) !important;
}

/* Progress */
.progress-container {
    width: 100%;
    background: var(--border);
    height: 10px;
    border-radius: 999px;
    overflow: hidden;
    margin-top: 10px;
}

.progress-bar {
    height: 100%;
    background: var(--primary);
    border-radius: 999px;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 999px;
    background: var(--primary-soft);
    color: var(--primary) !important;
    font-weight: 700;
    font-size: 0.8rem;
}

/* Workout */
.workout-line {
    padding: 13px 15px;
    border-left: 4px solid var(--primary);
    background: var(--card-soft);
    border-radius: 8px;
    margin-bottom: 9px;
    color: var(--text) !important;
}

/* Tables */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
.stSelectbox div,
.stMultiSelect div {
    border-radius: 10px !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    border-radius: 10px;
    font-weight: 700;
    min-height: 42px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--card);
    border-right: 1px solid var(--border);
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Mobile */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    .health-title {
        font-size: 1.5rem;
    }

    .health-logo {
        width: 48px;
        height: 48px;
        font-size: 24px;
    }

    .metric-value {
        font-size: 1.4rem;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE
# ============================================================
@st.cache_resource
def get_db_connection():
    conn = sqlite3.connect(
        "healthtrack.db",
        check_same_thread=False,
    )

    cursor = conn.cursor()

    # Users
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS system_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'User',
            created_at TEXT
        )
        """
    )

    # User profiles
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            gender TEXT,
            age INTEGER,
            height REAL,
            activity TEXT,
            goal TEXT,
            diet TEXT,
            shift TEXT,
            updated_at TEXT
        )
        """
    )

    # Weight
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weight_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            weight REAL NOT NULL,
            log_date TEXT NOT NULL,
            notes TEXT
        )
        """
    )

    # Food / macros
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS food_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            meal_type TEXT,
            food_name TEXT NOT NULL,
            calories REAL DEFAULT 0,
            protein REAL DEFAULT 0,
            carbs REAL DEFAULT 0,
            fat REAL DEFAULT 0,
            log_date TEXT NOT NULL,
            created_at TEXT
        )
        """
    )

    # Exercise
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS exercise_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            exercise_name TEXT NOT NULL,
            category TEXT,
            sets INTEGER DEFAULT 0,
            reps INTEGER DEFAULT 0,
            weight_used REAL DEFAULT 0,
            duration INTEGER DEFAULT 0,
            calories_burned REAL DEFAULT 0,
            notes TEXT,
            log_date TEXT NOT NULL,
            created_at TEXT
        )
        """
    )

    # Daily targets
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            calories INTEGER,
            protein REAL,
            carbs REAL,
            fat REAL,
            target_date TEXT NOT NULL,
            UNIQUE(username, target_date)
        )
        """
    )

    conn.commit()
    return conn


conn = get_db_connection()


# ============================================================
# HELPERS
# ============================================================
def encrypt_pass(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def execute_query(query, params=(), fetch=False, many=False):
    cursor = conn.cursor()

    if many:
        cursor.executemany(query, params)
    else:
        cursor.execute(query, params)

    if fetch:
        return cursor.fetchall()

    conn.commit()
    return None


def today_string():
    return date.today().isoformat()


def safe_progress(current, target):
    if target <= 0:
        return 0

    return min(max(current / target, 0), 1)


def progress_html(current, target):
    pct = safe_progress(current, target)
    return f"""
    <div class="progress-container">
        <div class="progress-bar" style="width:{pct * 100:.1f}%"></div>
    </div>
    """


def app_header(title="HealthTrack", subtitle="Nutrition • Fitness • Progress"):
    st.markdown(
        f"""
        <div class="health-header">
            <div class="health-logo">♥</div>
            <div>
                <div class="health-title">{title}</div>
                <div class="health-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SHIFT DATA
# ============================================================
SHIFT_TIMELINE_DATABASE = {
    "Morning Shift (6:00 AM - 3:00 PM)": {
        "Sleep Window": "🌙 9:30 PM to 5:00 AM",
        "Exercise Window": "🏋️ 4:00 PM to 5:15 PM",
        "Timestamps": {
            "Veg": [
                "⏰ 05:30 AM: Warm Water + 5 Soaked Almonds.",
                "⏰ 08:30 AM: Sattu Shake OR Paneer Toast.",
                "⏰ 01:00 PM: Rice/Roti + Dal + Sabzi + 100g Paneer.",
                "⏰ 03:30 PM: 75g Oats + Dry Fruits.",
                "⏰ 05:30 PM: Whey Protein + Toast.",
                "⏰ 08:30 PM: Roti/Rice + Salad + Tofu/Paneer.",
            ],
            "Non-Veg": [
                "⏰ 05:30 AM: Warm Water + 5 Soaked Almonds.",
                "⏰ 08:30 AM: 3 Whole Eggs + Whole Wheat Toast.",
                "⏰ 01:00 PM: Rice/Roti + Dal + Sabzi + 150g Chicken.",
                "⏰ 03:30 PM: 75g Oats + Dry Fruits.",
                "⏰ 05:30 PM: Whey Protein + Toast.",
                "⏰ 08:30 PM: Roti/Rice + Salad + Fish/Chicken.",
            ],
        },
    },
    "Afternoon Shift (2:00 PM - 11:00 PM)": {
        "Sleep Window": "🌙 12:00 AM to 7:30 AM",
        "Exercise Window": "🏋️ 10:30 AM to 11:45 AM",
        "Timestamps": {
            "Veg": [
                "⏰ 08:00 AM: Oats Upma + Sprouts + Paneer Bhurji.",
                "⏰ 10:00 AM: Banana or Black Coffee.",
                "⏰ 12:00 PM: Rice + Dal + Salad + Soy Chunks.",
                "⏰ 05:30 PM: Sattu Drink / Sprouted Chaat.",
                "⏰ 08:30 PM: 2 Chapatis + Mixed Veg + Curd.",
                "⏰ 11:30 PM: Warm Turmeric Milk.",
            ],
            "Non-Veg": [
                "⏰ 08:00 AM: Oats Upma + Eggs.",
                "⏰ 10:00 AM: Banana or Black Coffee.",
                "⏰ 12:00 PM: Rice + Dal + Salad + Chicken/Fish.",
                "⏰ 05:30 PM: Boiled Egg Chaat.",
                "⏰ 08:30 PM: Chapatis + Chicken + Salad.",
                "⏰ 11:30 PM: Warm Turmeric Milk.",
            ],
        },
    },
    "Evening Shift (5:30 PM - 3:00 AM)": {
        "Sleep Window": "🌙 03:30 AM to 11:00 AM",
        "Exercise Window": "🏋️ 04:00 PM to 05:00 PM",
        "Timestamps": {
            "Veg": [
                "⏰ 11:30 AM: Rice + Dal + Paneer.",
                "⏰ 03:15 PM: 75g Oats + Dry Fruits.",
                "⏰ 05:30 PM: Whey Protein.",
                "⏰ 09:30 PM: Paneer/Soya + Controlled Rice.",
                "⏰ 01:00 AM: Stop caffeine.",
                "⏰ 03:15 AM: Buttermilk/Sattu.",
            ],
            "Non-Veg": [
                "⏰ 11:30 AM: Rice + Dal + Eggs/Fish.",
                "⏰ 03:15 PM: 75g Oats + Dry Fruits.",
                "⏰ 05:30 PM: Whey Protein.",
                "⏰ 09:30 PM: Chicken/Eggs + Controlled Rice.",
                "⏰ 01:00 AM: Stop caffeine.",
                "⏰ 03:15 AM: Buttermilk/Egg Whites.",
            ],
        },
    },
    "Night Shift (10:00 PM - 7:00 AM)": {
        "Sleep Window": "🌙 08:00 AM to 3:30 PM",
        "Exercise Window": "🏋️ 05:30 PM to 06:45 PM",
        "Timestamps": {
            "Veg": [
                "⏰ 04:00 PM: Sattu Shake + Peanut Butter Toast.",
                "⏰ 05:00 PM: Roasted Chana.",
                "⏰ 07:15 PM: Rice/Roti + Dal + Paneer.",
                "⏰ 11:30 PM: Curd + Makhana/Apple.",
                "⏰ 02:30 AM: Chapatis + Soy Curry.",
                "⏰ 05:00 AM: Water only.",
            ],
            "Non-Veg": [
                "⏰ 04:00 PM: Eggs + Peanut Butter Toast.",
                "⏰ 05:00 PM: Black Coffee / Roasted Chana.",
                "⏰ 07:15 PM: Rice/Roti + Dal + Chicken/Fish.",
                "⏰ 11:30 PM: Egg Whites + Makhana.",
                "⏰ 02:30 AM: Chapatis + Chicken/Egg Curry.",
                "⏰ 05:00 AM: Water only.",
            ],
        },
    },
}


# ============================================================
# 7 DAY DIET
# ============================================================
INDIAN_7DAY_CORE = {
    "Veg": {
        "Monday": "Sattu Shake + Thick Dal Tadka + Paneer/Tofu Stir Fry + Soy Chunks Curry.",
        "Tuesday": "Oats Upma + Sprouts + Peanut Butter Toast + Rajma + Paneer Bhurji.",
        "Wednesday": "Moong Dal Cheela + Paneer + Black Chana + Raita + Palak Paneer.",
        "Thursday": "Peanut Butter Toast + Green Moong Dal + Jowar/Bajra Roti + Paneer Kebabs.",
        "Friday": "Besan Cheela + Curd + Lobia Curry + Soy Chunk Pulav.",
        "Saturday": "Milk Oats + Chia + Dal Makhani + Paneer.",
        "Sunday": "Sprouts Salad + Chole + Jeera Rice + Paneer.",
    },
    "Non-Veg": {
        "Monday": "3 Eggs + Chicken Breast + Egg White Scramble + Fish Curry.",
        "Tuesday": "Chicken Keema Roti + Egg Omelette + Grilled Chicken.",
        "Wednesday": "Scrambled Eggs + Mutton Keema + Chicken Soup + Baked Fish.",
        "Thursday": "Oats + Egg Whites + Egg Curry + Soya Rice.",
        "Friday": "Egg White Omelette + Chicken Biryani + Tawa Fish + Salad.",
        "Saturday": "Sattu Shake + Eggs + Chicken Gravy + Keema Curry.",
        "Sunday": "Egg Omelette + Chicken/Mutton Gravy + Baked Chicken + Salad.",
    },
}


# ============================================================
# SESSION
# ============================================================
if "auth" not in st.session_state:
    st.session_state.auth = {
        "login": False,
        "user": "",
        "role": "User",
    }

if "show_reg_portal" not in st.session_state:
    st.session_state.show_reg_portal = False


# ============================================================
# AUTHENTICATION
# ============================================================
if not st.session_state.auth["login"]:

    app_header(
        "HealthTrack",
        "Nutrition • Fitness • Progress"
    )

    st.markdown(
        """
        <div class="health-card">
            <h3>🔐 Secure Login</h3>
            <p class="small-muted">
                Sign in to access your nutrition and fitness dashboard.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    u_in = st.text_input("Username", key="login_user")
    p_in = st.text_input("Password", type="password", key="login_pass")

    if st.button("Sign In", use_container_width=True):

        result = execute_query(
            """
            SELECT role
            FROM system_users
            WHERE username=? AND password=?
            """,
            (u_in, encrypt_pass(p_in)),
            fetch=True,
        )

        if result:
            st.session_state.auth = {
                "login": True,
                "user": u_in,
                "role": result[0][0],
            }
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.write("---")

    if st.button("Create New Account", use_container_width=True):
        st.session_state.show_reg_portal = (
            not st.session_state.show_reg_portal
        )

    if st.session_state.show_reg_portal:

        st.markdown(
            """
            <div class="health-card">
                <h3>📝 Create Account</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        u_rg = st.text_input("New Username", key="reg_user")
        p_rg = st.text_input(
            "New Password",
            type="password",
            key="reg_pass",
        )

        r_rl = st.selectbox(
            "Account Type",
            ["User", "Admin"],
        )

        admin_passkey = ""

        if r_rl == "Admin":
            admin_passkey = st.text_input(
                "Admin Authorization Token",
                type="password",
            )

        if st.button(
            "Create Account",
            use_container_width=True,
        ):

            if not u_rg or not p_rg:
                st.warning("Please complete all fields.")

            elif (
                r_rl == "Admin"
                and admin_passkey != "SVB2_SECURE_ADMIN_2026"
            ):
                st.error("Invalid admin authorization token.")

            else:
                try:
                    execute_query(
                        """
                        INSERT INTO system_users
                        (username, password, role, created_at)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            u_rg,
                            encrypt_pass(p_rg),
                            r_rl,
                            datetime.now().isoformat(),
                        ),
                    )

                    st.success(
                        f"Account `{u_rg}` created successfully."
                    )

                except sqlite3.IntegrityError:
                    st.error("Username already exists.")


# ============================================================
# MAIN APPLICATION
# ============================================================
else:

    usr = st.session_state.auth["user"]
    perm = st.session_state.auth["role"]

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------
    with st.sidebar:

        st.markdown(
            """
            <div style="
                display:flex;
                align-items:center;
                gap:10px;
                margin-bottom:20px;
            ">
                <div class="health-logo"
                     style="width:42px;height:42px;font-size:20px;">
                    ♥
                </div>
                <div>
                    <strong>HealthTrack</strong><br>
                    <span class="small-muted">
                        Fitness Platform
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"👤 **User:** `{usr}`")
        st.markdown(f"🔑 **Role:** `{perm}`")

        st.write("---")

        if perm == "User":

            page = st.radio(
                "Navigation",
                [
                    "🏠 Dashboard",
                    "📊 Macro Tracker",
                    "🏋️ Exercise Tracker",
                    "⚖️ Weight Tracker",
                    "🍽 Diet Plan",
                    "🕒 Shift Nutrition",
                    "💪 Workout Plan",
                    "📈 Progress",
                    "📄 PDF Report",
                ],
            )

        else:

            page = st.radio(
                "Navigation",
                [
                    "👑 Admin Dashboard",
                    "🏠 User Dashboard",
                ],
            )

        st.write("---")

        if st.button(
            "🔒 Logout",
            use_container_width=True,
        ):
            st.session_state.auth = {
                "login": False,
                "user": "",
                "role": "User",
            }
            st.rerun()

    # ========================================================
    # ADMIN
    # ========================================================
    if perm == "Admin" and page == "👑 Admin Dashboard":

        app_header(
            "Admin Dashboard",
            "System administration and user management",
        )

        users = execute_query(
            """
            SELECT id, username, role, created_at
            FROM system_users
            ORDER BY id DESC
            """,
            fetch=True,
        )

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Registered Users</div>
                <div class="metric-value">{len(users)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("### 👥 Registered Accounts")

        st.dataframe(
            users,
            column_config={
                0: "ID",
                1: "Username",
                2: "Role",
                3: "Created",
            },
            use_container_width=True,
        )

        st.write("### 📊 Platform Statistics")

        total_food = execute_query(
            "SELECT COUNT(*) FROM food_logs",
            fetch=True,
        )[0][0]

        total_exercise = execute_query(
            "SELECT COUNT(*) FROM exercise_logs",
            fetch=True,
        )[0][0]

        total_weights = execute_query(
            "SELECT COUNT(*) FROM weight_logs",
            fetch=True,
        )[0][0]

        a, b, c = st.columns(3)

        a.metric("Food Entries", total_food)
        b.metric("Workout Entries", total_exercise)
        c.metric("Weight Entries", total_weights)

    # ========================================================
    # USER DASHBOARD
    # ========================================================
    elif page in ["🏠 Dashboard", "🏠 User Dashboard"]:

        app_header(
            "HealthTrack",
            "Your personal nutrition & fitness dashboard",
        )

        # Profile
        profile = execute_query(
            """
            SELECT gender, age, height, activity, goal, diet, shift
            FROM user_profiles
            WHERE username=?
            """,
            (usr,),
            fetch=True,
        )

        # Today's macros
        food_today = execute_query(
            """
            SELECT
                COALESCE(SUM(calories),0),
                COALESCE(SUM(protein),0),
                COALESCE(SUM(carbs),0),
                COALESCE(SUM(fat),0)
            FROM food_logs
            WHERE username=? AND log_date=?
            """,
            (usr, today_string()),
            fetch=True,
        )[0]

        calories_today = food_today[0]
        protein_today = food_today[1]
        carbs_today = food_today[2]
        fat_today = food_today[3]

        # Exercise
        exercise_today = execute_query(
            """
            SELECT
                COALESCE(SUM(duration),0),
                COALESCE(SUM(calories_burned),0)
            FROM exercise_logs
            WHERE username=? AND log_date=?
            """,
            (usr, today_string()),
            fetch=True,
        )[0]

        exercise_minutes = exercise_today[0]
        exercise_calories = exercise_today[1]

        # Latest weight
        latest_weight = execute_query(
            """
            SELECT weight
            FROM weight_logs
            WHERE username=?
            ORDER BY log_date DESC, id DESC
            LIMIT 1
            """,
            (usr,),
            fetch=True,
        )

        weight_value = (
            latest_weight[0][0]
            if latest_weight
            else 0
        )

        # ----------------------------------------------------
        # Metrics
        # ----------------------------------------------------
        c1, c2, c3, c4 = st.columns(4)

        c1.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">🔥 Calories Today</div>
                <div class="metric-value">{int(calories_today)}</div>
                <span class="metric-unit">kcal</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c2.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">🥩 Protein</div>
                <div class="metric-value">{protein_today:.0f}</div>
                <span class="metric-unit">grams</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c3.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">🏋️ Exercise</div>
                <div class="metric-value">{exercise_minutes:.0f}</div>
                <span class="metric-unit">minutes</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c4.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">⚖️ Current Weight</div>
                <div class="metric-value">
                    {weight_value if weight_value else "--"}
                </div>
                <span class="metric-unit">kg</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        # ----------------------------------------------------
        # Quick actions
        # ----------------------------------------------------
        st.markdown(
            """
            <div class="health-card">
                <h3>Today's Progress</h3>
                <p class="small-muted">
                    Track your meals, macros, workouts and weight
                    from the navigation menu.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        p1, p2 = st.columns(2)

        with p1:

            st.markdown(
                f"""
                <div class="health-card-soft">
                    <b>🥩 Protein Intake</b>
                    <div style="font-size:1.4rem;margin-top:8px;">
                        {protein_today:.0f} g
                    </div>
                    {progress_html(protein_today, 150)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with p2:

            st.markdown(
                f"""
                <div class="health-card-soft">
                    <b>🏃 Exercise</b>
                    <div style="font-size:1.4rem;margin-top:8px;">
                        {exercise_minutes:.0f} minutes
                    </div>
                    {progress_html(exercise_minutes, 60)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Recent meals
        st.write("### 🍽 Recent Meals")

        recent_food = execute_query(
            """
            SELECT meal_type, food_name, calories,
                   protein, carbs, fat, log_date
            FROM food_logs
            WHERE username=?
            ORDER BY id DESC
            LIMIT 5
            """,
            (usr,),
            fetch=True,
        )

        if recent_food:
            st.dataframe(
                recent_food,
                column_config={
                    0: "Meal",
                    1: "Food",
                    2: "Calories",
                    3: "Protein",
                    4: "Carbs",
                    5: "Fat",
                    6: "Date",
                },
                use_container_width=True,
            )
        else:
            st.info(
                "No food entries yet. Open Macro Tracker to add your first meal."
            )

    # ========================================================
    # MACRO TRACKER
    # ========================================================
    elif page == "📊 Macro Tracker":

        app_header(
            "Macro Tracker",
            "Track calories, protein, carbohydrates and fat",
        )

        # Today's totals
        totals = execute_query(
            """
            SELECT
                COALESCE(SUM(calories),0),
                COALESCE(SUM(protein),0),
                COALESCE(SUM(carbs),0),
                COALESCE(SUM(fat),0)
            FROM food_logs
            WHERE username=? AND log_date=?
            """,
            (usr, today_string()),
            fetch=True,
        )[0]

        cal, pro, carb, fat = totals

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("🔥 Calories", f"{cal:.0f} kcal")
        c2.metric("🥩 Protein", f"{pro:.0f} g")
        c3.metric("🍚 Carbs", f"{carb:.0f} g")
        c4.metric("🥑 Fat", f"{fat:.0f} g")

        st.write("---")

        st.markdown("### ➕ Add Food")

        with st.form("food_form", clear_on_submit=True):

            f1, f2 = st.columns(2)

            with f1:

                meal_type = st.selectbox(
                    "Meal",
                    [
                        "Breakfast",
                        "Lunch",
                        "Snack",
                        "Dinner",
                        "Pre-Workout",
                        "Post-Workout",
                    ],
                )

                food_name = st.text_input(
                    "Food / Meal Name"
                )

                food_date = st.date_input(
                    "Date",
                    value=date.today(),
                )

            with f2:

                food_calories = st.number_input(
                    "Calories (kcal)",
                    min_value=0.0,
                    value=0.0,
                    step=10.0,
                )

                food_protein = st.number_input(
                    "Protein (g)",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                )

                food_carbs = st.number_input(
                    "Carbohydrates (g)",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                )

                food_fat = st.number_input(
                    "Fat (g)",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                )

            submitted = st.form_submit_button(
                "➕ Add Meal",
                use_container_width=True,
            )

            if submitted:

                if not food_name.strip():
                    st.error("Enter a food name.")

                else:

                    execute_query(
                        """
                        INSERT INTO food_logs
                        (
                            username,
                            meal_type,
                            food_name,
                            calories,
                            protein,
                            carbs,
                            fat,
                            log_date,
                            created_at
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            usr,
                            meal_type,
                            food_name,
                            food_calories,
                            food_protein,
                            food_carbs,
                            food_fat,
                            food_date.isoformat(),
                            datetime.now().isoformat(),
                        ),
                    )

                    st.success("Meal added successfully.")
                    st.rerun()

        st.write("---")

        st.markdown("### 📋 Food History")

        food_history = execute_query(
            """
            SELECT
                id,
                meal_type,
                food_name,
                calories,
                protein,
                carbs,
                fat,
                log_date
            FROM food_logs
            WHERE username=?
            ORDER BY log_date DESC, id DESC
            LIMIT 100
            """,
            (usr,),
            fetch=True,
        )

        if food_history:

            st.dataframe(
                food_history,
                column_config={
                    0: "ID",
                    1: "Meal",
                    2: "Food",
                    3: "Calories",
                    4: "Protein",
                    5: "Carbs",
                    6: "Fat",
                    7: "Date",
                },
                use_container_width=True,
            )

        else:
            st.info("No meals recorded yet.")

    # ========================================================
    # EXERCISE TRACKER
    # ========================================================
    elif page == "🏋️ Exercise Tracker":

        app_header(
            "Exercise Tracker",
            "Track workouts, sets, reps, duration and calories",
        )

        today_exercise = execute_query(
            """
            SELECT
                COALESCE(SUM(duration),0),
                COALESCE(SUM(calories_burned),0)
            FROM exercise_logs
            WHERE username=? AND log_date=?
            """,
            (usr, today_string()),
            fetch=True,
        )[0]

        c1, c2 = st.columns(2)

        c1.metric(
            "⏱ Exercise Today",
            f"{today_exercise[0]:.0f} min",
        )

        c2.metric(
            "🔥 Calories Burned",
            f"{today_exercise[1]:.0f} kcal",
        )

        st.write("---")

        st.markdown("### ➕ Log Exercise")

        with st.form("exercise_form", clear_on_submit=True):

            e1, e2 = st.columns(2)

            with e1:

                exercise_name = st.text_input(
                    "Exercise Name",
                    placeholder="Bench Press",
                )

                category = st.selectbox(
                    "Category",
                    [
                        "Strength",
                        "Cardio",
                        "Walking",
                        "Running",
                        "Cycling",
                        "Sports",
                        "Mobility",
                        "Other",
                    ],
                )

                exercise_date = st.date_input(
                    "Date",
                    value=date.today(),
                )

                duration = st.number_input(
                    "Duration (minutes)",
                    min_value=0,
                    value=30,
                    step=5,
                )

            with e2:

                sets = st.number_input(
                    "Sets",
                    min_value=0,
                    value=3,
                    step=1,
                )

                reps = st.number_input(
                    "Reps",
                    min_value=0,
                    value=10,
                    step=1,
                )

                weight_used = st.number_input(
                    "Weight Used (kg)",
                    min_value=0.0,
                    value=0.0,
                    step=2.5,
                )

                calories_burned = st.number_input(
                    "Calories Burned",
                    min_value=0.0,
                    value=0.0,
                    step=10.0,
                )

            notes = st.text_area(
                "Workout Notes",
                placeholder="How did the workout feel?",
            )

            save_exercise = st.form_submit_button(
                "💾 Save Workout",
                use_container_width=True,
            )

            if save_exercise:

                if not exercise_name.strip():
                    st.error("Enter an exercise name.")

                else:

                    execute_query(
                        """
                        INSERT INTO exercise_logs
                        (
                            username,
                            exercise_name,
                            category,
                            sets,
                            reps,
                            weight_used,
                            duration,
                            calories_burned,
                            notes,
                            log_date,
                            created_at
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            usr,
                            exercise_name,
                            category,
                            sets,
                            reps,
                            weight_used,
                            duration,
                            calories_burned,
                            notes,
                            exercise_date.isoformat(),
                            datetime.now().isoformat(),
                        ),
                    )

                    st.success("Workout saved.")
                    st.rerun()

        st.write("---")

        st.markdown("### 📋 Workout History")

        workout_history = execute_query(
            """
            SELECT
                id,
                exercise_name,
                category,
                sets,
                reps,
                weight_used,
                duration,
                calories_burned,
                log_date
            FROM exercise_logs
            WHERE username=?
            ORDER BY log_date DESC, id DESC
            LIMIT 100
            """,
            (usr,),
            fetch=True,
        )

        if workout_history:

            st.dataframe(
                workout_history,
                column_config={
                    0: "ID",
                    1: "Exercise",
                    2: "Category",
                    3: "Sets",
                    4: "Reps",
                    5: "Weight",
                    6: "Minutes",
                    7: "Calories",
                    8: "Date",
                },
                use_container_width=True,
            )

        else:
            st.info("No workouts recorded yet.")

    # ========================================================
    # WEIGHT TRACKER
    # ========================================================
    elif page == "⚖️ Weight Tracker":

        app_header(
            "Weight Tracker",
            "Monitor your body-weight trend",
        )

        latest = execute_query(
            """
            SELECT weight, log_date
            FROM weight_logs
            WHERE username=?
            ORDER BY log_date DESC, id DESC
            LIMIT 1
            """,
            (usr,),
            fetch=True,
        )

        if latest:
            st.metric(
                "Current Weight",
                f"{latest[0][0]:.1f} kg",
            )
        else:
            st.info("No weight has been recorded yet.")

        st.write("---")

        with st.form("weight_form", clear_on_submit=True):

            weight = st.number_input(
                "Weight (kg)",
                min_value=30.0,
                max_value=300.0,
                value=70.0,
                step=0.1,
            )

            weight_date = st.date_input(
                "Date",
                value=date.today(),
            )

            notes = st.text_input(
                "Notes",
                placeholder="Morning weight, after workout, etc.",
            )

            save_weight = st.form_submit_button(
                "⚖️ Save Weight",
                use_container_width=True,
            )

            if save_weight:

                execute_query(
                    """
                    INSERT INTO weight_logs
                    (username, weight, log_date, notes)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        usr,
                        weight,
                        weight_date.isoformat(),
                        notes,
                    ),
                )

                st.success("Weight recorded.")
                st.rerun()

        st.write("---")

        history = execute_query(
            """
            SELECT log_date, weight, notes
            FROM weight_logs
            WHERE username=?
            ORDER BY log_date ASC
            """,
            (usr,),
            fetch=True,
        )

        if history:

            import pandas as pd

            df = pd.DataFrame(
                history,
                columns=[
                    "Date",
                    "Weight",
                    "Notes",
                ],
            )

            st.line_chart(
                df.set_index("Date")["Weight"]
            )

            st.dataframe(
                df.sort_values(
                    "Date",
                    ascending=False,
                ),
                use_container_width=True,
            )

    # ========================================================
    # DIET PLAN
    # ========================================================
    elif page == "🍽 Diet Plan":

        app_header(
            "7-Day Indian Diet Plan",
            "Structured nutrition plan",
        )

        diet_choice = st.radio(
            "Diet Type",
            ["Veg", "Non-Veg"],
            horizontal=True,
        )

        for day, meal in INDIAN_7DAY_CORE[diet_choice].items():

            st.markdown(
                f"""
                <div class="health-card-soft">
                    <span class="badge">{day}</span>
                    <p>{meal}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ========================================================
    # SHIFT NUTRITION
    # ========================================================
    elif page == "🕒 Shift Nutrition":

        app_header(
            "Shift Nutrition",
            "Meal timing aligned with your work schedule",
        )

        selected_shift = st.selectbox(
            "Select Shift",
            list(SHIFT_TIMELINE_DATABASE.keys()),
        )

        diet_type = st.radio(
            "Diet",
            ["Veg", "Non-Veg"],
            horizontal=True,
        )

        shift_data = SHIFT_TIMELINE_DATABASE[
            selected_shift
        ]

        a, b = st.columns(2)

        a.markdown(
            f"""
            <div class="health-card">
                <b>🌙 Sleep Window</b>
                <p>{shift_data["Sleep Window"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        b.markdown(
            f"""
            <div class="health-card">
                <b>🏋️ Exercise Window</b>
                <p>{shift_data["Exercise Window"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### 🍴 Meal Schedule")

        for meal in shift_data["Timestamps"][diet_type]:

            st.markdown(
                f"""
                <div class="health-card-soft">
                    {meal}
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ========================================================
    # WORKOUT PLAN
    # ========================================================
    elif page == "💪 Workout Plan":

        app_header(
            "Workout Plan",
            "Strength, cardio and conditioning",
        )

        tabs = st.tabs(
            [
                "💪 Strength",
                "🏃 Cardio",
                "🧘 Recovery",
            ]
        )

        with tabs[0]:

            workout = [
                (
                    "Monday — Push",
                    "Bench Press, Overhead Press, Incline Dumbbell Press, Lateral Raises, Triceps",
                ),
                (
                    "Tuesday — Pull",
                    "Deadlift, Lat Pulldown, Barbell Row, Face Pulls, Biceps Curls",
                ),
                (
                    "Wednesday — Legs",
                    "Squats, Romanian Deadlift, Leg Press, Leg Curl, Calf Raises",
                ),
                (
                    "Thursday — Push",
                    "Incline Press, Shoulder Press, Cable Fly, Lateral Raises, Triceps",
                ),
                (
                    "Friday — Pull",
                    "Lat Pulldown, T-Bar Row, Seated Row, Rear Delts, Biceps",
                ),
            ]

            for day, exercises in workout:

                st.markdown(
                    f"""
                    <div class="workout-line">
                        <b>{day}</b><br>
                        {exercises}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with tabs[1]:

            st.markdown(
                """
                <div class="workout-line">
                    🏃 <b>LISS:</b>
                    30–40 minutes walking or cycling.
                </div>

                <div class="workout-line">
                    🚴 <b>HIIT:</b>
                    15–20 minutes with work/recovery intervals.
                </div>

                <div class="workout-line">
                    🚶 <b>Daily Walking:</b>
                    Track steps and active minutes.
                </div>
                """,
                unsafe_allow_html=True,
            )

        with tabs[2]:

            st.markdown(
                """
                <div class="workout-line">
                    🧘 5–10 minutes mobility work.
                </div>

                <div class="workout-line">
                    😴 Prioritize sufficient sleep and recovery.
                </div>

                <div class="workout-line">
                    💧 Maintain regular hydration.
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ========================================================
    # PROGRESS
    # ========================================================
    elif page == "📈 Progress":

        app_header(
            "Progress Dashboard",
            "Your long-term nutrition and fitness history",
        )

        import pandas as pd

        # Weight
        weights = execute_query(
            """
            SELECT log_date, weight
            FROM weight_logs
            WHERE username=?
            ORDER BY log_date ASC
            """,
            (usr,),
            fetch=True,
        )

        if weights:

            st.markdown("### ⚖️ Weight Progress")

            weight_df = pd.DataFrame(
                weights,
                columns=[
                    "Date",
                    "Weight",
                ],
            )

            st.line_chart(
                weight_df.set_index("Date")
            )

        else:

            st.info(
                "Add weight entries to see your weight trend."
            )

        # Macros
        macro_history = execute_query(
            """
            SELECT
                log_date,
                SUM(calories),
                SUM(protein),
                SUM(carbs),
                SUM(fat)
            FROM food_logs
            WHERE username=?
            GROUP BY log_date
            ORDER BY log_date ASC
            """,
            (usr,),
            fetch=True,
        )

        if macro_history:

            st.markdown("### 🍽 Nutrition History")

            macro_df = pd.DataFrame(
                macro_history,
                columns=[
                    "Date",
                    "Calories",
                    "Protein",
                    "Carbs",
                    "Fat",
                ],
            )

            st.line_chart(
                macro_df.set_index("Date")[
                    [
                        "Protein",
                        "Carbs",
                        "Fat",
                    ]
                ]
            )

            st.dataframe(
                macro_df,
                use_container_width=True,
            )

        # Exercise
        exercise_history = execute_query(
            """
            SELECT
                log_date,
                SUM(duration),
                SUM(calories_burned)
            FROM exercise_logs
            WHERE username=?
            GROUP BY log_date
            ORDER BY log_date ASC
            """,
            (usr,),
            fetch=True,
        )

        if exercise_history:

            st.markdown("### 🏋️ Exercise History")

            exercise_df = pd.DataFrame(
                exercise_history,
                columns=[
                    "Date",
                    "Minutes",
                    "Calories Burned",
                ],
            )

            st.bar_chart(
                exercise_df.set_index("Date")[
                    ["Minutes"]
                ]
            )

            st.dataframe(
                exercise_df,
                use_container_width=True,
            )

    # ========================================================
    # PDF REPORT
    # ========================================================
    elif page == "📄 PDF Report":

        app_header(
            "Health Report",
            "Generate a printable nutrition and fitness report",
        )

        # Get data
        food = execute_query(
            """
            SELECT
                COALESCE(SUM(calories),0),
                COALESCE(SUM(protein),0),
                COALESCE(SUM(carbs),0),
                COALESCE(SUM(fat),0)
            FROM food_logs
            WHERE username=?
            """,
            (usr,),
            fetch=True,
        )[0]

        exercise = execute_query(
            """
            SELECT
                COALESCE(SUM(duration),0),
                COALESCE(SUM(calories_burned),0)
            FROM exercise_logs
            WHERE username=?
            """,
            (usr,),
            fetch=True,
        )[0]

        latest_weight = execute_query(
            """
            SELECT weight
            FROM weight_logs
            WHERE username=?
            ORDER BY log_date DESC, id DESC
            LIMIT 1
            """,
            (usr,),
            fetch=True,
        )

        current_weight = (
            latest_weight[0][0]
            if latest_weight
            else "Not recorded"
        )

        if st.button(
            "📄 Generate PDF Report",
            use_container_width=True,
        ):

            pdf_buffer = BytesIO()

            doc = SimpleDocTemplate(
                pdf_buffer,
                pagesize=letter,
                rightMargin=30,
                leftMargin=30,
                topMargin=30,
                bottomMargin=30,
            )

            styles = getSampleStyleSheet()

            header_style = ParagraphStyle(
                "Header",
                parent=styles["Heading1"],
                fontSize=21,
                textColor=colors.HexColor("#16a34a"),
                spaceAfter=15,
            )

            section_style = ParagraphStyle(
                "Section",
                parent=styles["Heading2"],
                fontSize=14,
                textColor=colors.HexColor("#334155"),
                spaceBefore=12,
                spaceAfter=7,
            )

            body_style = ParagraphStyle(
                "Body",
                parent=styles["Normal"],
                fontSize=9,
                leading=14,
            )

            elements = []

            elements.append(
                Paragraph(
                    "HEALTHTRACK FITNESS & NUTRITION REPORT",
                    header_style,
                )
            )

            elements.append(
                Paragraph(
                    f"<b>User:</b> {usr}<br/>"
                    f"<b>Generated:</b> {datetime.now().strftime('%d %B %Y %H:%M')}",
                    body_style,
                )
            )

            elements.append(Spacer(1, 15))

            # Nutrition
            elements.append(
                Paragraph(
                    "1. Nutrition Summary",
                    section_style,
                )
            )

            nutrition_table = [
                ["Metric", "Total"],
                ["Calories", f"{food[0]:.0f} kcal"],
                ["Protein", f"{food[1]:.1f} g"],
                ["Carbohydrates", f"{food[2]:.1f} g"],
                ["Fat", f"{food[3]:.1f} g"],
            ]

            table = Table(
                nutrition_table,
                colWidths=[250, 210],
            )

            table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.HexColor("#16a34a"),
                        ),
                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, 0),
                            colors.white,
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.HexColor("#cbd5e1"),
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            7,
                        ),
                    ]
                )
            )

            elements.append(table)

            # Exercise
            elements.append(
                Paragraph(
                    "2. Exercise Summary",
                    section_style,
                )
            )

            exercise_table = [
                ["Metric", "Total"],
                [
                    "Exercise Duration",
                    f"{exercise[0]:.0f} minutes",
                ],
                [
                    "Calories Burned",
                    f"{exercise[1]:.0f} kcal",
                ],
            ]

            ex_table = Table(
                exercise_table,
                colWidths=[250, 210],
            )

            ex_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.HexColor("#2563eb"),
                        ),
                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, 0),
                            colors.white,
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.HexColor("#cbd5e1"),
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            7,
                        ),
                    ]
                )
            )

            elements.append(ex_table)

            # Weight
            elements.append(
                Paragraph(
                    "3. Current Weight",
                    section_style,
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Current Weight:</b> {current_weight} kg",
                    body_style,
                )
            )

            elements.append(Spacer(1, 15))

            elements.append(
                Paragraph(
                    "This report is intended for personal fitness tracking "
                    "and should not replace advice from a qualified healthcare "
                    "professional.",
                    body_style,
                )
            )

            doc.build(elements)

            pdf_buffer.seek(0)

            st.download_button(
                label="📥 Download HealthTrack PDF",
                data=pdf_buffer,
                file_name=f"{usr}_healthtrack_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
