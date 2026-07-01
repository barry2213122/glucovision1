"""
GLUCOVISION AI
AI-Powered Personalized Diabetes Monitoring & Glucose Prediction System
Educational Prototype Only - Not a Medical Device
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
import math

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GlucoVision AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #ffffff;
}

/* Background - simple dark navy, no fancy gradient */
.stApp {
    background-color: #0d1117;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 2px solid #00d9ff;
}
section[data-testid="stSidebar"] .block-container { padding: 1rem; }

/* All labels and text - bright white, bold */
label, .stTextInput label, .stNumberInput label,
.stSelectbox label, .stSlider label, .stMultiSelect label {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}

p, .stMarkdown p {
    color: #e6edf3 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* Metric cards - solid borders, bright values */
.metric-card {
    background-color: #161b22;
    border: 2px solid #00d9ff;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.metric-value {
    font-size: 1.9rem;
    font-weight: 800;
    color: #00d9ff;
    line-height: 1.2;
}
.metric-label {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #c9d1d9;
    margin-top: 0.3rem;
}
.metric-icon { font-size: 1.3rem; margin-bottom: 0.25rem; }

/* Section headers - each section gets its own bright color, not one matching brand color */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 3px solid #00d9ff;
}
.section-icon {
    width: 36px; height: 36px;
    background-color: #00d9ff;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 0.02em;
}
/* Color variants - cycled across the 10 sections so it doesn't look like one matched brand palette */
.sh-blue   { border-bottom-color: #1e90ff; }
.sh-blue   .section-icon { background-color: #1e90ff; }
.sh-green  { border-bottom-color: #00e676; }
.sh-green  .section-icon { background-color: #00e676; }
.sh-orange { border-bottom-color: #ff9100; }
.sh-orange .section-icon { background-color: #ff9100; }
.sh-pink   { border-bottom-color: #ff2d95; }
.sh-pink   .section-icon { background-color: #ff2d95; }
.sh-purple { border-bottom-color: #a855f7; }
.sh-purple .section-icon { background-color: #a855f7; }
.sh-yellow { border-bottom-color: #ffd60a; }
.sh-yellow .section-icon { background-color: #ffd60a; }
.sh-red    { border-bottom-color: #ff3b3b; }
.sh-red    .section-icon { background-color: #ff3b3b; }
.sh-teal   { border-bottom-color: #00ffc8; }
.sh-teal   .section-icon { background-color: #00ffc8; }

/* Hero header */
.hero-header {
    text-align: center;
    padding: 1.8rem 1rem;
    background-color: #161b22;
    border-radius: 12px;
    border: 3px solid #00e676;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 2.7rem;
    font-weight: 800;
    color: #00d9ff;
    margin: 0;
    letter-spacing: -0.01em;
}
.hero-subtitle {
    font-size: 0.95rem;
    color: #c9d1d9;
    margin: 0.5rem 0 0;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* Disclaimer */
.disclaimer {
    background-color: #3d0a0a;
    border: 3px solid #ff3b3b;
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1.5rem;
    font-size: 0.85rem;
    font-weight: 700;
    color: #ff8080;
}

/* Risk badges */
.risk-low   { color: #00e676; background: #0a2e1a; border: 2px solid #00e676; border-radius:6px; padding:3px 10px; font-size:0.85rem; font-weight:800; }
.risk-medium{ color: #ffd60a; background: #332700; border: 2px solid #ffd60a; border-radius:6px; padding:3px 10px; font-size:0.85rem; font-weight:800; }
.risk-high  { color: #ff3b3b; background: #3d0a0a; border: 2px solid #ff3b3b; border-radius:6px; padding:3px 10px; font-size:0.85rem; font-weight:800; }

/* Streamlit widget overrides */
.stSelectbox > div > div {
    background-color: #161b22 !important;
    border: 2px solid #30363d !important;
    color: #ffffff !important;
}
.stNumberInput > div > div > input {
    background-color: #161b22 !important;
    border: 2px solid #30363d !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}
.stTextInput > div > div > input {
    background-color: #161b22 !important;
    border: 2px solid #30363d !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}
div[data-testid="metric-container"] {
    background-color: #161b22;
    border: 2px solid #30363d;
    border-radius: 8px;
    padding: 0.5rem 1rem;
}
div[data-testid="metric-container"] label {
    color: #c9d1d9 !important;
    font-weight: 700 !important;
}
div[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #00d9ff !important;
    font-weight: 800 !important;
}
.stButton > button {
    background-color: #00e676 !important;
    color: #0d1117 !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 1.5rem !important;
}
.stButton > button:hover {
    background-color: #5cffb0 !important;
}
hr { border-color: #30363d !important; border-width: 1px !important; }

/* Sidebar logo */
.sidebar-logo {
    text-align: center;
    padding: 1rem 0 1.5rem;
    border-bottom: 2px solid #00d9ff;
    margin-bottom: 1.5rem;
}
.sidebar-logo-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: #00d9ff;
}
.sidebar-logo-sub {
    font-size: 0.7rem;
    color: #8b949e;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Nav pills */
.nav-pill {
    display: block;
    padding: 0.5rem 1rem;
    margin: 0.2rem 0;
    border-radius: 6px;
    color: #c9d1d9;
    font-size: 0.88rem;
    font-weight: 700;
    cursor: pointer;
}
.nav-pill:hover { background-color: #21262d; color: #ffffff; }

/* Recommendation cards */
.rec-card {
    background-color: #161b22;
    border: 2px solid #30363d;
    border-left: 5px solid #00d9ff;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.8rem;
    font-size: 0.9rem;
    font-weight: 700;
    color: #e6edf3;
}
.rec-card.rc-0 { border-left-color: #00d9ff; }
.rec-card.rc-1 { border-left-color: #00e676; }
.rec-card.rc-2 { border-left-color: #ffd60a; }
.rec-card.rc-3 { border-left-color: #ff9100; }
.rec-card.rc-4 { border-left-color: #ff2d95; }
.rec-card.rc-5 { border-left-color: #a855f7; }
.rec-card.rc-6 { border-left-color: #1e90ff; }

/* Insight box */
.insight-box {
    background-color: #161b22;
    border: 2px solid #00d9ff;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.insight-value {
    font-size: 2rem;
    font-weight: 800;
    color: #00d9ff;
}

/* Glass card (used in export section) */
.glass-card {
    background-color: #161b22;
    border: 2px solid #30363d;
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}
.glass-card strong { color: #00d9ff; }
</style>
""", unsafe_allow_html=True)

# ─── FOOD DATABASE ─────────────────────────────────────────────────────────────
FOOD_DB = {
    "Roti (1 piece, ~35g)":          {"calories": 104, "carbs": 22, "protein": 3.1, "fat": 0.9},
    "Rice (1 cup cooked, ~200g)":    {"calories": 260, "carbs": 57, "protein": 5.4, "fat": 0.6},
    "Apple (medium, ~182g)":         {"calories": 95,  "carbs": 25, "protein": 0.5, "fat": 0.3},
    "Banana (medium, ~118g)":        {"calories": 105, "carbs": 27, "protein": 1.3, "fat": 0.4},
    "Milk (1 cup, 240ml)":           {"calories": 149, "carbs": 12, "protein": 8.0, "fat": 8.0},
    "Dal (1 cup, ~200g)":            {"calories": 230, "carbs": 40, "protein": 15,  "fat": 1.0},
    "Pizza (1 slice, ~107g)":        {"calories": 285, "carbs": 36, "protein": 12,  "fat": 10},
    "Burger (standard, ~150g)":      {"calories": 354, "carbs": 29, "protein": 20,  "fat": 17},
    "Bread (1 slice, ~25g)":         {"calories": 67,  "carbs": 13, "protein": 2.3, "fat": 0.9},
    "Juice (orange, 1 cup, 240ml)":  {"calories": 112, "carbs": 26, "protein": 1.7, "fat": 0.5},
    "Egg (1 large, boiled)":         {"calories": 78,  "carbs": 0.6,"protein": 6.3, "fat": 5.3},
    "Chapati (1 piece, ~40g)":       {"calories": 120, "carbs": 25, "protein": 3.5, "fat": 1.2},
    "Idli (1 piece, ~39g)":          {"calories": 39,  "carbs": 8,  "protein": 1.8, "fat": 0.2},
    "Dosa (plain, ~55g)":            {"calories": 133, "carbs": 25, "protein": 3.5, "fat": 2.5},
    "Sambar (1 cup, ~240ml)":        {"calories": 102, "carbs": 15, "protein": 5.5, "fat": 2.5},
    "Chicken breast (100g, cooked)": {"calories": 165, "carbs": 0,  "protein": 31,  "fat": 3.6},
    "Paneer (100g)":                 {"calories": 265, "carbs": 3.4,"protein": 18,  "fat": 20},
    "Oats (1 cup cooked, ~234g)":    {"calories": 166, "carbs": 28, "protein": 5.9, "fat": 3.6},
    "Coffee (black, 240ml)":         {"calories": 5,   "carbs": 0,  "protein": 0.3, "fat": 0.1},
    "Tea with milk (240ml)":         {"calories": 30,  "carbs": 3,  "protein": 1.5, "fat": 1.5},
}

INSULIN_TYPES = [
    "No Insulin",
    "Rapid-Acting (e.g., Lispro, Aspart)",
    "Short-Acting (Regular)",
    "Intermediate-Acting (NPH)",
    "Long-Acting (Glargine, Detemir)",
    "Mixed Insulin (70/30)",
]

# ─── HELPER FUNCTIONS ─────────────────────────────────────────────────────────

def calculate_bmi(weight_kg: float, height_cm: float) -> tuple[float, str]:
    """Return (bmi_value, category)."""
    if height_cm <= 0 or weight_kg <= 0:
        return 0.0, "N/A"
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5:   cat = "Underweight"
    elif bmi < 25:   cat = "Normal"
    elif bmi < 30:   cat = "Overweight"
    else:            cat = "Obese"
    return round(bmi, 1), cat


def _smoothstep(edge0: float, edge1: float, x: float) -> float:
    """Smooth S-curve interpolation (cubic: 3x²-2x³) for gradual physiological onset/offset."""
    if edge0 == edge1:
        return 0.0 if x < edge0 else 1.0
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)


INSULIN_ACTION_PROFILE = {
    "No Insulin":                           {"onset": 0,   "peak": 0,   "end": 1},
    "Rapid-Acting (e.g., Lispro, Aspart)":  {"onset": 15,  "peak": 75,  "end": 240},
    "Short-Acting (Regular)":               {"onset": 45,  "peak": 150, "end": 420},
    "Intermediate-Acting (NPH)":            {"onset": 150, "peak": 480, "end": 900},
    "Long-Acting (Glargine, Detemir)":      {"onset": 90,  "peak": 360, "end": 1380},
    "Mixed Insulin (70/30)":                {"onset": 30,  "peak": 180, "end": 720},
}

# How quickly the body's OWN insulin response clears a glucose excursion.
# Type 1 = no endogenous insulin at all; Type 2/Pre = partial; No DM = full.
CARB_RESPONSE_PROFILE = {
    "No Diabetes":      {"peak": 45,  "decay": 90},
    "Prediabetes":      {"peak": 50,  "decay": 115},
    "Type 2 Diabetes":  {"peak": 60,  "decay": 130},
    "Type 1 Diabetes":  {"peak": 60,  "decay": 165},
}


def _cumulative_insulin_fraction(minutes: float, onset: float, peak: float, end: float) -> float:
    """Fraction of a dose's total glucose-lowering effect delivered by `minutes` post-injection."""
    if minutes <= onset: return 0.0
    if minutes <= peak:  return 0.5 * _smoothstep(onset, peak, minutes)
    if minutes <= end:   return 0.5 + 0.5 * _smoothstep(peak, end, minutes)
    return 1.0


def _carb_excursion_fraction(minutes: float, peak: float, decay: float) -> float:
    """Relative glucose excursion (0→1→0) at a given time after eating."""
    if minutes <= peak:
        return _smoothstep(0, peak, minutes)
    return 1.0 - _smoothstep(peak, peak + decay, minutes)


def _estimate_bmr(weight_kg: float, age: int = 35, gender: str = "Male") -> float:
    """
    Mifflin-St Jeor BMR estimate (kcal/day) — how many calories the body
    burns at rest just to keep organs functioning. This energy comes from
    glucose in the blood, so it continuously lowers blood glucose even
    without any activity or insulin. Using a fixed height of 170cm as a
    neutral default since height doesn't shift the result dramatically.
    """
    weight_kg = max(weight_kg, 30.0)
    if gender == "Female":
        bmr = 10 * weight_kg + 6.25 * 170 - 5 * age - 161
    else:
        bmr = 10 * weight_kg + 6.25 * 170 - 5 * age + 5
    return max(1200.0, bmr)


def glucose_prediction_model(
    current_glucose: float,
    carbs_g: float,
    diabetes_type: str,
    insulin_type: str,
    insulin_dose: float,
    time_since_injection_hr: float = 0.0,
    weight_kg: float = 70.0,
    age: int = 35,
    gender: str = "Male",
    calories_kcal: float = 0.0,
    time_since_meal_hr: float = 0.0,
    exercise_type: str = "No Exercise",
    exercise_duration_min: float = 0.0,
) -> dict:
    """
    Educational glucose prediction model — 30 / 60 / 90 / 120 min timepoints.

    Five competing physiological effects:

    1. CARB EXCURSION — carbs raise glucose; curve position depends on
       time_since_meal_hr (if you ate 1 hr ago you are already past the peak).
    2. BMR BURN — resting metabolism consumes glucose; liver offsets ~92% via
       glycogen, so net blood glucose drop is small but real.
    3. EXERCISE — muscles absorb glucose directly without insulin during
       activity, plus an afterburn effect for hours post-workout. Magnitude
       now scales with how long you actually exercised (duration_factor),
       not just which intensity bucket you picked.
    4. INJECTED INSULIN — onset/peak/end curves per insulin type, offset by
       time already elapsed since injection.
    5. WEIGHT-ADJUSTED SENSITIVITY — insulin effect scales with body weight.
    """

    weight_kg = weight_kg if weight_kg and weight_kg > 0 else 70.0

    # ── 1. Carb excursion ────────────────────────────────────────────────────
    carb_factor = {
        "No Diabetes":     1.1,
        "Prediabetes":     1.6,
        "Type 2 Diabetes": 2.2,
        "Type 1 Diabetes": 3.0,
    }.get(diabetes_type, 1.6)

    carb_peak_rise = carbs_g * carb_factor
    carb_profile   = CARB_RESPONSE_PROFILE.get(diabetes_type, CARB_RESPONSE_PROFILE["Prediabetes"])
    meal_elapsed_min = time_since_meal_hr * 60.0

    def _carb_delta_at(future_min: float) -> float:
        """Change in carb excursion from NOW to NOW+future_min.
        Negative if we are already past the peak and coming back down."""
        at_future = _carb_excursion_fraction(
            meal_elapsed_min + future_min, carb_profile["peak"], carb_profile["decay"])
        at_now    = _carb_excursion_fraction(
            meal_elapsed_min, carb_profile["peak"], carb_profile["decay"])
        return carb_peak_rise * (at_future - at_now)

    # ── 2. BMR burn ──────────────────────────────────────────────────────────
    bmr_kcal_day = _estimate_bmr(weight_kg, age, gender)
    blood_vol_dl = max(30.0, weight_kg * 0.7)
    HEPATIC_COMP = 0.08   # liver replaces ~92% of burned glucose from glycogen

    def _bmr_drop(minutes: float) -> float:
        kcal  = bmr_kcal_day * (minutes / 1440)
        grams = (kcal / 4.0) * HEPATIC_COMP
        return (grams * 1000) / blood_vol_dl

    # ── 3. Exercise effect ───────────────────────────────────────────────────
    # Active glucose uptake rate (mg/dL per minute of exercise), by intensity.
    # Calibrated: 30 min light = ~9 mg/dL; moderate = ~21; intense = ~36.
    exercise_rate = {
        "No Exercise":                      0.0,
        "Light (walking, yoga)":            0.30,
        "Moderate (jogging, cycling)":      0.70,
        "Intense (running, gym, sports)":   1.20,
    }.get(exercise_type, 0.0)

    # Post-exercise afterburn: muscles keep absorbing glucose for hours to
    # refill glycogen. Modelled as a decaying extra uptake that halves every
    # 90 minutes. We assume exercise ended ~1 hour before 'now'.
    #
    # FIX: previously `exercise_duration_min` was only checked against 0 to
    # decide whether to apply any effect at all — the actual number of
    # minutes exercised never entered the magnitude calculation, so sliding
    # the duration input around had zero effect on the prediction. Now the
    # afterburn magnitude scales with `duration_factor`: 30 min is treated
    # as the baseline (matches the old fixed effect), more minutes produce
    # a proportionally bigger afterburn, capped at 90 min so an extreme
    # duration doesn't produce an unrealistic runaway drop.
    def _exercise_drop(future_min: float) -> float:
        if exercise_duration_min <= 0 or exercise_type == "No Exercise":
            return 0.0
        hours_post = 1.0 + (future_min / 60.0)   # 1 hr elapsed + future window
        duration_factor = min(exercise_duration_min, 90.0) / 30.0
        afterburn = exercise_rate * 0.30 * duration_factor * (0.5 ** (hours_post / 1.5))
        return afterburn * future_min

    # ── 4. Injected insulin ──────────────────────────────────────────────────
    insulin_factor_map = {
        "No Insulin":                           0,
        "Rapid-Acting (e.g., Lispro, Aspart)": 45,
        "Short-Acting (Regular)":               35,
        "Intermediate-Acting (NPH)":            25,
        "Long-Acting (Glargine, Detemir)":      20,
        "Mixed Insulin (70/30)":                30,
    }
    weight_adj           = max(0.6, min(1.6, 70.0 / weight_kg))
    factor_per_unit      = insulin_factor_map.get(insulin_type, 0) * weight_adj
    total_insulin_effect = factor_per_unit * (insulin_dose or 0)
    ins_profile          = INSULIN_ACTION_PROFILE.get(insulin_type, INSULIN_ACTION_PROFILE["No Insulin"])
    elapsed_min          = max(0.0, time_since_injection_hr) * 60.0

    # ── 5. Combine all effects ───────────────────────────────────────────────
    predictions = {}
    for t in (30, 60, 90, 120):
        carb_delta = _carb_delta_at(t)

        already_delivered = _cumulative_insulin_fraction(
            elapsed_min, ins_profile["onset"], ins_profile["peak"], ins_profile["end"])
        delivered_by_t = _cumulative_insulin_fraction(
            elapsed_min + t, ins_profile["onset"], ins_profile["peak"], ins_profile["end"])
        insulin_delta = total_insulin_effect * max(0.0, delivered_by_t - already_delivered)

        bmr_delta      = _bmr_drop(t)
        exercise_delta = _exercise_drop(t)

        predicted = current_glucose + carb_delta - insulin_delta - bmr_delta - exercise_delta

        # Floor: liver prevents glucose dropping below ~88-95% of fasting
        # baseline unless active insulin is genuinely causing hypoglycemia
        fasting_floor = current_glucose * 0.88 if insulin_delta > 5 else current_glucose * 0.95
        predicted = max(fasting_floor, predicted)
        predictions[t] = round(min(600.0, predicted), 1)

    return predictions


def health_score(
    glucose: float,
    bmi: float,
    diabetes_type: str,
    predicted_peak: float,
    carbs: float,
) -> tuple[float, str]:
    """Compute a 0–100 health score and risk category."""
    score = 100.0

    # Glucose penalty
    if glucose < 70 or glucose > 180:   score -= 25
    elif glucose < 80 or glucose > 140: score -= 12
    elif glucose < 90 or glucose > 120: score -= 5

    # Predicted peak penalty
    if predicted_peak > 200: score -= 20
    elif predicted_peak > 160: score -= 10

    # BMI penalty
    if bmi < 16 or bmi >= 35:   score -= 20
    elif bmi < 18.5 or bmi >= 30: score -= 10
    elif bmi < 17 or bmi >= 27: score -= 4

    # Diabetes type penalty
    dm_penalty = {"No Diabetes": 0, "Prediabetes": 8, "Type 2 Diabetes": 15, "Type 1 Diabetes": 18}
    score -= dm_penalty.get(diabetes_type, 0)

    # High-carb meal penalty
    if carbs > 80: score -= 10
    elif carbs > 50: score -= 5

    score = max(0, min(100, score))

    if score >= 75:  risk = "Low Risk"
    elif score >= 50: risk = "Medium Risk"
    else:             risk = "High Risk"

    return round(score, 1), risk


def get_recommendations(diabetes_type, glucose, predicted_peak, bmi, bmi_cat, carbs) -> list[str]:
    """Generate personalised AI recommendations."""
    recs = []

    # Glucose-based
    if glucose < 70:
        recs.append("⚠️ Current glucose appears low (hypoglycemia range). Consider consuming fast-acting carbohydrates like juice or glucose tablets immediately.")
    elif glucose > 180:
        recs.append("🔴 Current glucose is elevated. Ensure adequate hydration and consult your healthcare provider about medication adjustments.")
    elif 80 <= glucose <= 120:
        recs.append("✅ Your current glucose reading is within a healthy range. Maintain this with consistent meal timing and activity.")

    # Predicted peak
    if predicted_peak > 200:
        recs.append("📈 Glucose is predicted to rise significantly. A 15–20 minute post-meal walk can reduce peak glucose by up to 30%.")
    elif predicted_peak > 160:
        recs.append("📊 Moderate glucose rise predicted. Monitor closely and consider light physical activity after eating.")

    # Diabetes-specific
    if diabetes_type == "Type 1 Diabetes":
        recs.append("💉 As a Type 1 diabetic, consistent carb-counting and insulin-to-carb ratio management is essential. Discuss your I:C ratio with your endocrinologist.")
    elif diabetes_type == "Type 2 Diabetes":
        recs.append("🥗 For Type 2 management, reducing refined carbohydrates and increasing dietary fibre can significantly improve glucose control.")
    elif diabetes_type == "Prediabetes":
        recs.append("🌿 Prediabetes can often be reversed with lifestyle changes. Aim for 150 minutes of moderate exercise per week and reduce sugar intake.")
    else:
        recs.append("✅ No diabetes detected. Maintain a balanced diet and active lifestyle to prevent future risk.")

    # BMI-based
    if bmi_cat == "Obese":
        recs.append("⚖️ BMI indicates obesity, which significantly increases insulin resistance. A 5–10% weight reduction can improve glucose sensitivity meaningfully.")
    elif bmi_cat == "Overweight":
        recs.append("⚖️ Slightly elevated BMI noted. Regular cardiovascular exercise (30 min/day) can help improve metabolic health.")
    elif bmi_cat == "Underweight":
        recs.append("⚖️ BMI indicates underweight status. Adequate caloric intake with balanced nutrition is important for metabolic function.")

    # Carb-based
    if carbs > 80:
        recs.append("🍽️ High carbohydrate intake detected. Consider splitting this meal into smaller portions and pairing carbs with protein and healthy fats to blunt glucose spikes.")
    elif carbs > 50:
        recs.append("🥦 Moderate carb load. Including non-starchy vegetables can help slow carbohydrate absorption.")

    # General wellness
    recs.append("💧 Staying well-hydrated (8–10 glasses of water daily) supports kidney function and glucose regulation.")
    recs.append("😴 Quality sleep (7–9 hours) is crucial for glucose regulation. Poor sleep is linked to increased insulin resistance.")

    return recs[:7]  # Cap at 7 recommendations


def generate_pdf_report(
    patient: dict,
    nutrition: dict,
    glucose_now: float,
    predictions: dict,
    score: float,
    risk: str,
    recommendations: list[str],
    bmi: float,
    bmi_cat: str,
) -> bytes:
    """Generate a professional PDF health report using ReportLab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    elements = []

    # ── Color palette ──
    CYAN   = colors.HexColor('#00d9ff')
    PURPLE = colors.HexColor('#1e90ff')
    DARK   = colors.HexColor('#0f172a')
    SLATE  = colors.HexColor('#1e293b')
    LIGHT  = colors.HexColor('#e2e8f0')
    MUTED  = colors.HexColor('#64748b')
    RED    = colors.HexColor('#ff3b3b')
    GREEN  = colors.HexColor('#00e676')
    AMBER  = colors.HexColor('#ffd60a')

    risk_color = {"Low Risk": GREEN, "Medium Risk": AMBER, "High Risk": RED}.get(risk, AMBER)

    # ── Styles ──
    title_style = ParagraphStyle('Title', parent=styles['Title'],
        fontSize=26, textColor=CYAN, fontName='Helvetica-Bold',
        alignment=TA_CENTER, spaceAfter=4)
    subtitle_style = ParagraphStyle('Sub', parent=styles['Normal'],
        fontSize=9, textColor=MUTED, alignment=TA_CENTER, spaceAfter=2)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'],
        fontSize=13, textColor=CYAN, fontName='Helvetica-Bold',
        spaceBefore=16, spaceAfter=8, borderPad=4)
    body_style = ParagraphStyle('Body', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#334155'),
        spaceAfter=6, leading=16)
    rec_style = ParagraphStyle('Rec', parent=styles['Normal'],
        fontSize=9.5, textColor=colors.HexColor('#1e293b'),
        spaceAfter=5, leading=15, leftIndent=10)
    disclaimer_style = ParagraphStyle('Dis', parent=styles['Normal'],
        fontSize=8, textColor=RED, alignment=TA_CENTER,
        spaceBefore=10, spaceAfter=4, fontName='Helvetica-Bold')

    def spacer(h=0.3): return Spacer(1, h*cm)
    def hr(): return HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=8, spaceBefore=4)

    # ══ HEADER ══
    elements.append(Paragraph("🩺 GLUCOVISION AI", title_style))
    elements.append(Paragraph("AI-Powered Personalized Diabetes Monitoring & Glucose Prediction", subtitle_style))
    elements.append(Paragraph(f"Report Generated: {datetime.now().strftime('%B %d, %Y  |  %H:%M')}", subtitle_style))
    elements.append(spacer(0.4))
    elements.append(hr())

    # ── DISCLAIMER ──
    elements.append(Paragraph(
        "⚠️  EDUCATIONAL PROTOTYPE ONLY — NOT INTENDED FOR DIAGNOSIS, TREATMENT, OR MEDICAL DECISION MAKING",
        disclaimer_style))
    elements.append(hr())

    # ══ PATIENT INFORMATION ══
    elements.append(Paragraph("PATIENT PROFILE", section_style))
    p = patient
    patient_data = [
        ['Full Name', p.get('name','N/A'),   'Age',    f"{p.get('age','N/A')} years"],
        ['Gender',   p.get('gender','N/A'),  'Weight', f"{p.get('weight','N/A')} kg"],
        ['Height',   f"{p.get('height','N/A')} cm", 'Diabetes Status', p.get('diabetes','N/A')],
        ['BMI',      f"{bmi}",               'BMI Category', bmi_cat],
    ]
    t = Table(patient_data, colWidths=[3.5*cm, 5.5*cm, 3.5*cm, 5.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#eff6ff')),
        ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#eff6ff')),
        ('TEXTCOLOR',  (0,0), (0,-1), PURPLE),
        ('TEXTCOLOR',  (2,0), (2,-1), PURPLE),
        ('FONTNAME',   (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',   (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 9),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('PADDING',    (0,0), (-1,-1), 6),
    ]))
    elements.append(t)
    elements.append(spacer())

    # ══ GLUCOSE METRICS ══
    elements.append(Paragraph("GLUCOSE MONITORING", section_style))

    def glucose_status(value):
        """Return (status_label, status_color) for a glucose reading."""
        if value < 70:
            return 'Low', RED
        elif value <= 140:
            return 'Normal', GREEN
        elif value <= 180:
            return 'Moderate', AMBER
        else:
            return 'High', RED

    rows_meta = [
        ('Current Glucose',    glucose_now),
        ('Predicted @ 30 min', predictions.get(30,  glucose_now)),
        ('Predicted @ 60 min', predictions.get(60,  glucose_now)),
        ('Predicted @ 90 min', predictions.get(90,  glucose_now)),
        ('Predicted @ 120 min',predictions.get(120, glucose_now)),
    ]

    glucose_data = [['Metric', 'Value', 'Status']]
    status_colors = []  # parallel list of colors for each data row's Status cell
    for label, val in rows_meta:
        status_label, status_color = glucose_status(val)
        glucose_data.append([label, f"{val} mg/dL", status_label])
        status_colors.append(status_color)

    gt = Table(glucose_data, colWidths=[5*cm, 5.5*cm, 7.5*cm])
    gt_style = [
        ('BACKGROUND', (0,0), (-1,0), DARK),
        ('TEXTCOLOR',  (0,0), (-1,0), CYAN),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 9),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('PADDING',    (0,0), (-1,-1), 7),
        ('ALIGN',      (1,0), (2,-1), 'CENTER'),
        ('FONTNAME',   (2,1), (2,-1), 'Helvetica-Bold'),
    ]
    # Color each Status cell to match its row (row index i+1 since row 0 is the header)
    for i, status_color in enumerate(status_colors):
        gt_style.append(('TEXTCOLOR', (2, i+1), (2, i+1), status_color))
    gt.setStyle(TableStyle(gt_style))
    elements.append(gt)
    elements.append(spacer())

    # ══ NUTRITION SUMMARY ══
    elements.append(Paragraph("NUTRITION SUMMARY", section_style))
    nut_data = [
        ['Nutrient', 'Amount', 'Daily % (approx.)'],
        ['Total Calories', f"{nutrition.get('calories',0):.0f} kcal",
         f"{nutrition.get('calories',0)/2000*100:.0f}%"],
        ['Carbohydrates', f"{nutrition.get('carbs',0):.1f} g",
         f"{nutrition.get('carbs',0)/300*100:.0f}%"],
        ['Protein',        f"{nutrition.get('protein',0):.1f} g",
         f"{nutrition.get('protein',0)/50*100:.0f}%"],
        ['Fat',            f"{nutrition.get('fat',0):.1f} g",
         f"{nutrition.get('fat',0)/65*100:.0f}%"],
    ]
    nt = Table(nut_data, colWidths=[5*cm, 5.5*cm, 7.5*cm])
    nt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK),
        ('TEXTCOLOR',  (0,0), (-1,0), CYAN),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 9),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('PADDING',    (0,0), (-1,-1), 7),
        ('ALIGN',      (1,0), (2,-1), 'CENTER'),
    ]))
    elements.append(nt)
    elements.append(spacer())

    # ══ HEALTH SCORE ══
    elements.append(Paragraph("HEALTH ANALYTICS", section_style))
    score_data = [
        ['Health Score', f"{score} / 100", 'Risk Category', risk],
    ]
    st2 = Table(score_data, colWidths=[4*cm, 5*cm, 4*cm, 5*cm])
    st2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdf4') if risk=='Low Risk'
            else (colors.HexColor('#fffbeb') if risk=='Medium Risk' else colors.HexColor('#fef2f2'))),
        ('FONTNAME',   (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 11),
        ('TEXTCOLOR',  (1,0), (1,0), GREEN if risk=='Low Risk' else (AMBER if risk=='Medium Risk' else RED)),
        ('TEXTCOLOR',  (3,0), (3,0), GREEN if risk=='Low Risk' else (AMBER if risk=='Medium Risk' else RED)),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING',    (0,0), (-1,-1), 10),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(st2)
    elements.append(spacer())

    # ══ RECOMMENDATIONS ══
    elements.append(Paragraph("AI HEALTH RECOMMENDATIONS", section_style))
    for i, rec in enumerate(recommendations, 1):
        clean = rec.replace('⚠️','').replace('🔴','').replace('✅','').replace('📈','') \
                   .replace('📊','').replace('💉','').replace('🥗','').replace('🌿','') \
                   .replace('⚖️','').replace('🍽️','').replace('🥦','').replace('💧','') \
                   .replace('😴','').strip()
        elements.append(Paragraph(f"{i}. {clean}", rec_style))

    elements.append(spacer(0.5))
    elements.append(hr())

    # ══ FOOTER ══
    elements.append(Paragraph(
        "⚠️ DISCLAIMER: This report is generated by an educational AI prototype. "
        "It is NOT a medical diagnosis and should NOT be used for medical decision-making. "
        "Always consult a qualified healthcare professional for medical advice.",
        disclaimer_style))
    elements.append(Paragraph(
        "GlucoVision AI — Educational Prototype | Science Fair Project",
        subtitle_style))

    doc.build(elements)
    buf.seek(0)
    return buf.read()


# ─── PLOTLY CHART HELPERS ─────────────────────────────────────────────────────

CHART_LAYOUT = dict(
    paper_bgcolor='rgba(10,14,26,0)',
    plot_bgcolor='rgba(10,14,26,0)',
    font=dict(family='Inter', color='#94a3b8', size=11),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor='rgba(0,217,255,0.15)', linecolor='rgba(0,217,255,0.25)', zerolinecolor='rgba(0,0,0,0)'),
    yaxis=dict(gridcolor='rgba(0,217,255,0.15)', linecolor='rgba(0,217,255,0.25)', zerolinecolor='rgba(0,0,0,0)'),
)


def glucose_trend_chart(glucose_now: float, predictions: dict) -> go.Figure:
    times = [0, 30, 60, 90, 120]
    values = [glucose_now] + [predictions[t] for t in [30, 60, 90, 120]]
    labels = ['Now', '30m', '60m', '90m', '2hr']

    fig = go.Figure()

    # Normal range band
    fig.add_hrect(y0=70, y1=140, fillcolor='rgba(0,230,118,0.12)',
                  line_color='rgba(0,230,118,0.25)', annotation_text='Normal', annotation_position='right')

    # Prediction line
    fig.add_trace(go.Scatter(
        x=labels, y=values, mode='lines+markers',
        line=dict(color='#00d9ff', width=3, shape='spline'),
        marker=dict(size=9, color='#00d9ff', line=dict(color='#e2e8f0', width=2)),
        fill='tozeroy',
        fillcolor='rgba(0,217,255,0.12)',
        name='Glucose',
    ))
    fig.update_layout(**CHART_LAYOUT, title=dict(
        text='Glucose Trend Forecast', font=dict(size=14, color='#e2e8f0'), x=0.5))
    fig.update_yaxes(title_text='mg/dL')
    fig.update_xaxes(title_text='Time')
    return fig


def nutrition_pie_chart(carbs: float, protein: float, fat: float) -> go.Figure:
    if carbs + protein + fat == 0:
        carbs, protein, fat = 1, 1, 1
    fig = go.Figure(go.Pie(
        labels=['Carbohydrates', 'Protein', 'Fat'],
        values=[carbs, protein, fat],
        hole=0.55,
        marker=dict(colors=['#1e90ff', '#00d9ff', '#a855f7'],
                    line=dict(color='#0a0e1a', width=2)),
        textfont=dict(color='#e2e8f0', size=11),
    ))
    fig.update_layout(**CHART_LAYOUT, title=dict(
        text='Macronutrient Breakdown', font=dict(size=14, color='#e2e8f0'), x=0.5),
        showlegend=True,
        legend=dict(orientation='h', y=-0.1, font=dict(color='#94a3b8')))
    return fig


def risk_gauge(score: float, risk: str) -> go.Figure:
    color = '#00e676' if risk == 'Low Risk' else ('#ffd60a' if risk == 'Medium Risk' else '#ff3b3b')
    fig = go.Figure(go.Indicator(
        mode='gauge+number+delta',
        value=score,
        domain={'x': [0,1], 'y': [0,1]},
        number={'font': {'size': 36, 'color': color, 'family': 'Space Grotesk'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#475569', 'tickfont': {'color': '#475569'}},
            'bar': {'color': color, 'thickness': 0.25},
            'bgcolor': 'rgba(15,23,42,0.5)',
            'borderwidth': 0,
            'steps': [
                {'range': [0,  50], 'color': 'rgba(255,59,59,0.15)'},
                {'range': [50, 75], 'color': 'rgba(255,214,10,0.15)'},
                {'range': [75, 100],'color': 'rgba(0,230,118,0.15)'},
            ],
            'threshold': {'line': {'color': color, 'width': 3},
                          'thickness': 0.8, 'value': score},
        },
        title={'text': 'Health Score', 'font': {'color': '#94a3b8', 'size': 13}},
    ))
    fig.update_layout(**CHART_LAYOUT, height=260)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0))
    return fig


def calorie_summary_chart(food_log: list) -> go.Figure:
    if not food_log:
        fig = go.Figure()
        fig.update_layout(**CHART_LAYOUT, title=dict(text='No foods selected yet', font=dict(color='#475569'), x=0.5))
        return fig

    labels = [f['name'][:20] for f in food_log]
    cals   = [f['calories'] for f in food_log]
    fig = go.Figure(go.Bar(
        x=cals, y=labels, orientation='h',
        marker=dict(
            color=cals, colorscale='Viridis',
            line=dict(color='rgba(0,0,0,0)'),
        ),
        text=[f'{c:.0f} kcal' for c in cals],
        textposition='outside',
        textfont=dict(color='#e2e8f0'),
    ))
    fig.update_layout(**CHART_LAYOUT,
        title=dict(text='Calorie Breakdown by Food', font=dict(size=14, color='#e2e8f0'), x=0.5),
        xaxis_title='Calories (kcal)',
        height=max(250, 60*len(food_log)))
    return fig


def classify_three_month_glucose(avg_glucose: float) -> tuple[str, float, str, str]:
    """
    Estimate a long-term glucose classification from a 3-month average
    reading, using the standard ADA relationship between average glucose
    and HbA1c (the real blood test doctors use, since glucose binds to
    hemoglobin and red blood cells live ~3 months):

        eAG (mg/dL) = 28.7 × HbA1c(%) − 46.7   →   HbA1c = (eAG + 46.7) / 28.7

    Standard diagnostic cut-offs (ADA): Normal <5.7%, Prediabetes 5.7–6.4%,
    Diabetes ≥6.5%. This is an educational ESTIMATE based on self-reported
    readings, not an actual lab HbA1c blood test.
    """
    estimated_a1c = round((avg_glucose + 46.7) / 28.7, 2)
    if estimated_a1c < 5.7:
        return "Likely Normal", estimated_a1c, "risk-low", "🟢"
    elif estimated_a1c < 6.5:
        return "Likely Prediabetes", estimated_a1c, "risk-medium", "🟡"
    else:
        return "Likely Diabetes Range", estimated_a1c, "risk-high", "🔴"


def three_month_trend_chart(dates, values) -> go.Figure:
    """Plot self-reported glucose readings over time against standard
    reference bands, so the trend and classification are visually linked."""
    fig = go.Figure()

    fig.add_hrect(y0=40,  y1=117, fillcolor='rgba(0,230,118,0.10)', line_color='rgba(0,230,118,0.2)',
                  annotation_text='Normal range', annotation_position='right',
                  annotation_font_color='#00e676', annotation_font_size=10)
    fig.add_hrect(y0=117, y1=140, fillcolor='rgba(255,214,10,0.10)', line_color='rgba(255,214,10,0.2)',
                  annotation_text='Prediabetes range', annotation_position='right',
                  annotation_font_color='#ffd60a', annotation_font_size=10)
    fig.add_hrect(y0=140, y1=300, fillcolor='rgba(255,59,59,0.10)', line_color='rgba(255,59,59,0.2)',
                  annotation_text='Diabetes range', annotation_position='right',
                  annotation_font_color='#ff3b3b', annotation_font_size=10)

    fig.add_trace(go.Scatter(
        x=dates, y=values, mode='lines+markers',
        line=dict(color='#00d9ff', width=3),
        marker=dict(size=9, color='#00d9ff', line=dict(color='#ffffff', width=1.5)),
        name='Glucose Reading',
    ))
    fig.update_layout(**CHART_LAYOUT, title=dict(
        text='3-Month Glucose History', font=dict(size=14, color='#ffffff'), x=0.5))
    fig.update_yaxes(title_text='mg/dL')
    fig.update_xaxes(title_text='Date')
    return fig


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <div style="font-size:2.2rem; margin-bottom:0.3rem">🩺</div>
            <div class="sidebar-logo-title">GlucoVision AI</div>
            <div class="sidebar-logo-sub">Glucose Prediction System</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📋 Navigation")
        sections = [
            ("👤", "Patient Profile"),
            ("💉", "Insulin Management"),
            ("🍽️", "Food Intelligence"),
            ("🔬", "Digital Twin"),
            ("📈", "AI Predictions"),
            ("📊", "Visualizations"),
            ("🧠", "Health Analytics"),
            ("💡", "Recommendations"),
            ("🔮", "Future Insights"),
            ("📄", "Export Report"),
        ]
        for icon, name in sections:
            st.markdown(f'<div class="nav-pill">{icon} &nbsp;{name}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style="font-size:0.72rem; color:#475569; text-align:center; padding:0.5rem 0;">
            <strong style="color:#ff3b3b">⚠️ Educational Prototype</strong><br>
            Not a medical device.<br>
            Always consult your doctor.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style="font-size:0.7rem; color:#334155; text-align:center;">
            GlucoVision AI v1.0<br>
            Science Fair Edition 2025
        </div>
        """, unsafe_allow_html=True)


# ─── MAIN APP ─────────────────────────────────────────────────────────────────

def main():
    render_sidebar()

    # ── Hero Header ──
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🩺 GlucoVision AI</div>
        <div class="hero-subtitle">AI-Powered Personalized Diabetes Monitoring & Glucose Prediction System</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Disclaimer ──
    st.markdown("""
    <div class="disclaimer">
        ⚠️ <strong>EDUCATIONAL PROTOTYPE ONLY.</strong>
        This application is designed for science fair demonstration purposes.
        It is NOT intended for diagnosis, treatment, or any medical decision-making.
        Always consult a qualified healthcare professional for medical advice.
    </div>
    """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 1 · PATIENT PROFILE
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="section-header sh-blue">
        <div class="section-icon">👤</div>
        <div class="section-title">SECTION 1 — Patient Profile</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            name   = st.text_input("Full Name", value="", placeholder="Enter your name")
            age    = st.number_input("Age (years)", min_value=0, max_value=120, value=0,
                                     help="Enter your age in years")
            gender = st.selectbox("Gender", ["Select Gender", "Male", "Female", "Other", "Prefer not to say"])
        with col2:
            weight = st.number_input("Weight (kg)", min_value=0.0, max_value=250.0, value=0.0, step=0.5,
                                     help="Enter your weight in kilograms")
            height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, value=0.0, step=0.5,
                                     help="Enter your height in centimetres")
        with col3:
            diabetes_type = st.selectbox(
                "Diabetes Status",
                ["Select Status", "No Diabetes", "Prediabetes", "Type 1 Diabetes", "Type 2 Diabetes"]
            )

        bmi, bmi_cat = calculate_bmi(weight, height)
        bmi_color = {'Normal':'#00e676','Underweight':'#ffd60a','Overweight':'#ffd60a','Obese':'#ff3b3b'}.get(bmi_cat,'#94a3b8')

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("⚖️ BMI", f"{bmi}")
        col_b.metric("🏷️ BMI Category", bmi_cat)
        col_c.metric("🧬 Diabetes Status", diabetes_type.split()[0])

        # ── 3-Month Glucose Trend & Classification (optional, HbA1c-style estimate) ──
        st.markdown("#### 📊 3-Month Glucose Trend Analysis <span style='font-size:0.7rem; color:#8b949e; font-weight:600'>(Optional)</span>", unsafe_allow_html=True)
        st.caption("Add glucose readings spread across the past ~3 months to estimate a long-term classification — similar to how a real HbA1c blood test works, since it reflects average glucose over that period.")

        if "glucose_history_df" not in st.session_state:
            st.session_state.glucose_history_df = pd.DataFrame({
                "Date": pd.Series(dtype="datetime64[ns]"),
                "Glucose (mg/dL)": pd.Series(dtype="float"),
            })

        edited_history = st.data_editor(
            st.session_state.glucose_history_df,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Date": st.column_config.DateColumn(
                    "Date", max_value=datetime.now().date(),
                    help="Date the reading was taken"),
                "Glucose (mg/dL)": st.column_config.NumberColumn(
                    "Glucose (mg/dL)", min_value=40, max_value=600,
                    help="Blood glucose reading in mg/dL"),
            },
            key="glucose_history_editor",
        )

        valid_readings = edited_history.dropna(subset=["Glucose (mg/dL)"])
        valid_readings = valid_readings[valid_readings["Glucose (mg/dL)"] > 0]

        three_month_avg = None
        three_month_a1c = None
        three_month_classification = None

        if len(valid_readings) > 0:
            three_month_avg = float(valid_readings["Glucose (mg/dL)"].mean())
            three_month_classification, three_month_a1c, risk_css_3mo, risk_icon_3mo = \
                classify_three_month_glucose(three_month_avg)

            col_3mo1, col_3mo2, col_3mo3 = st.columns(3)
            col_3mo1.metric("📈 3-Month Avg Glucose", f"{three_month_avg:.0f} mg/dL")
            col_3mo2.metric("🧪 Estimated HbA1c", f"{three_month_a1c}%")
            with col_3mo3:
                st.markdown(f"""
                <div style="padding-top:1.7rem; text-align:center">
                    <span class="{risk_css_3mo}">{risk_icon_3mo} {three_month_classification}</span>
                </div>
                """, unsafe_allow_html=True)

            if len(valid_readings) < 3:
                st.info("ℹ️ Add a few more readings spread across the past 3 months for a more reliable estimate.")

            if diabetes_type not in ("Select Status", "") and three_month_classification is not None:
                selected_simple = diabetes_type.replace("Type 1 ", "").replace("Type 2 ", "")
                if (("Normal" in three_month_classification and diabetes_type != "No Diabetes") or
                    ("Diabetes Range" in three_month_classification and diabetes_type in ("No Diabetes", "Prediabetes")) or
                    ("Prediabetes" in three_month_classification and diabetes_type not in ("Prediabetes",))):
                    st.warning(f"⚠️ This estimate ({three_month_classification}) differs from your selected status above ({diabetes_type}). Consider discussing this with a healthcare provider.")

            trend_sorted = valid_readings.sort_values("Date")
            st.plotly_chart(
                three_month_trend_chart(trend_sorted["Date"], trend_sorted["Glucose (mg/dL)"]),
                use_container_width=True, config={'displayModeBar': False}
            )

            st.caption("⚠️ This is an educational estimate based on the standard average-glucose-to-HbA1c relationship, calculated from self-reported readings — it is **not** an actual lab HbA1c test. Please consult a healthcare provider for real diagnosis.")
        else:
            st.caption("Add at least one glucose reading above (use the **+** row at the bottom of the table) to see your 3-month trend analysis.")

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 2 · INSULIN MANAGEMENT
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="section-header sh-red">
        <div class="section-icon">💉</div>
        <div class="section-title">SECTION 2 — Insulin Management</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if diabetes_type == "No Diabetes":
            insulin_type = "No Insulin"
            st.info("💡 No insulin required — patient has no diabetes.")
            st.write(f"**Insulin Type:** {insulin_type}")
        else:
            insulin_type = st.selectbox("Insulin Type", INSULIN_TYPES)

    with col2:
        if insulin_type == "No Insulin" or diabetes_type == "No Diabetes":
            insulin_dose = 0.0
            st.write("")
            st.write("**Insulin Dose:** N/A")
        else:
            insulin_dose = st.number_input("Insulin Dose (units)", min_value=0.0, max_value=100.0,
                                           value=0.0, step=0.5, help="Enter your insulin dose in units")
    with col3:
        if insulin_type == "No Insulin" or diabetes_type == "No Diabetes":
            time_since_injection = 0.0
            st.write("**Time Since Last Injection:** N/A")
        else:
            time_since_injection = st.number_input("Time Since Last Injection (hours)",
                                                    min_value=0.0, max_value=24.0, value=0.0, step=0.5,
                                                    help="Enter hours since your last injection")

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 3 · FOOD INTELLIGENCE SYSTEM
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="section-header sh-orange">
        <div class="section-icon">🍽️</div>
        <div class="section-title">SECTION 3 — Food Intelligence System</div>
    </div>
    """, unsafe_allow_html=True)

    st.info("🍽️ **Enter what you are eating RIGHT NOW (this one meal only)** — not your full day. The glucose prediction is based on this single meal's effect over the next 2 hours.")

    selected_foods = st.multiselect(
        "Select Foods Consumed",
        options=list(FOOD_DB.keys()),
        default=[],
        help="Select all foods you have consumed in this meal."
    )

    food_log = []
    total_cal = total_carbs = total_protein = total_fat = 0.0

    if selected_foods:
        st.markdown("**🔢 Set Quantity for Each Food:**")
        cols = st.columns(min(len(selected_foods), 3))
        for i, food_name in enumerate(selected_foods):
            with cols[i % 3]:
                qty = st.number_input(f"× {food_name.split('(')[0].strip()}", min_value=0.5, max_value=10.0,
                                      value=1.0, step=0.5, key=f"qty_{i}")
                fd = FOOD_DB[food_name]
                food_log.append({
                    'name': food_name.split('(')[0].strip(),
                    'qty': qty,
                    'calories': fd['calories'] * qty,
                    'carbs':    fd['carbs']    * qty,
                    'protein':  fd['protein']  * qty,
                    'fat':      fd['fat']      * qty,
                })
                total_cal     += fd['calories'] * qty
                total_carbs   += fd['carbs']    * qty
                total_protein += fd['protein']  * qty
                total_fat     += fd['fat']      * qty

        # Nutrition Summary
        st.markdown("**📊 Nutrition Summary:**")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🔥 Calories",      f"{total_cal:.0f} kcal")
        c2.metric("🍞 Carbohydrates", f"{total_carbs:.1f} g")
        c3.metric("💪 Protein",       f"{total_protein:.1f} g")
        c4.metric("🥑 Fat",           f"{total_fat:.1f} g")
    else:
        st.info("👆 Please select at least one food to see nutrition data.")

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 4 · METABOLIC DIGITAL TWIN
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="section-header sh-teal">
        <div class="section-icon">🔬</div>
        <div class="section-title">SECTION 4 — Metabolic Digital Twin</div>
    </div>
    """, unsafe_allow_html=True)

    current_glucose = st.slider(
        "🩸 Current Blood Glucose Level (mg/dL)",
        min_value=40, max_value=400, value=40, step=1,
        help="Drag the slider to enter your current fasting or post-meal glucose reading."
    )

    col_extra1, col_extra2, col_extra3 = st.columns(3)
    with col_extra1:
        time_since_meal_hr = st.number_input(
            "⏱️ Time Since Eating (hours)",
            min_value=0.0, max_value=12.0, value=0.0, step=0.25,
            help="How many hours ago did you eat this meal? 0 = just finished eating now."
        )
    with col_extra2:
        exercise_type = st.selectbox(
            "🏃 Exercise Done Today",
            ["No Exercise", "Light (walking, yoga)", "Moderate (jogging, cycling)", "Intense (running, gym, sports)"],
            help="Exercise directly lowers blood glucose by making muscles absorb it without insulin."
        )
    with col_extra3:
        exercise_duration_min = st.number_input(
            "⏳ Exercise Duration (minutes)",
            min_value=0, max_value=300, value=0, step=5,
            help="How many minutes of exercise did you do? Used to calculate how much glucose your muscles absorbed.",
            disabled=(exercise_type == "No Exercise")
        )

    predictions = glucose_prediction_model(
        current_glucose, total_carbs, diabetes_type, insulin_type, insulin_dose,
        time_since_injection_hr=time_since_injection, weight_kg=weight,
        age=int(age) if age and age > 0 else 35,
        gender=gender if gender not in ("Select Gender",) else "Male",
        calories_kcal=total_cal,
        time_since_meal_hr=time_since_meal_hr,
        exercise_type=exercise_type,
        exercise_duration_min=float(exercise_duration_min),
    )
    predicted_60 = predictions[60]

    hs, risk = health_score(current_glucose, bmi, diabetes_type, max(predictions.values()), total_carbs)

    # Twin panel — 6 metric cards
    st.markdown("**🖥️ Patient Digital Overview:**")
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    glucose_color = '#00e676' if 70 <= current_glucose <= 140 else ('#ffd60a' if current_glucose <= 180 else '#ff3b3b')
    pred_color    = '#00e676' if 70 <= predicted_60 <= 140    else ('#ffd60a' if predicted_60 <= 180    else '#ff3b3b')
    score_color   = '#00e676' if hs >= 75 else ('#ffd60a' if hs >= 50 else '#ff3b3b')

    for col, icon, value, label, color in [
        (c1, '🩸', f'{current_glucose}', 'Current Glucose', glucose_color),
        (c2, '📈', f'{predicted_60}',   'Predicted (60m)', pred_color),
        (c3, '🔥', f'{total_cal:.0f}',  'Calories (kcal)',  '#1e90ff'),
        (c4, '🍞', f'{total_carbs:.0f}','Carbs (g)',         '#a855f7'),
        (c5, '⚖️', f'{bmi}',            'BMI',               '#00d9ff'),
        (c6, '💯', f'{hs}',             'Health Score',      score_color),
    ]:
        col.markdown(f"""
        <div class="metric-card" style="border-color:{color}">
            <div class="metric-icon">{icon}</div>
            <div class="metric-value" style="color:{color}">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 5 · AI GLUCOSE PREDICTION TABLE
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="section-header sh-green">
        <div class="section-icon">📈</div>
        <div class="section-title">SECTION 5 — AI Glucose Prediction</div>
    </div>
    """, unsafe_allow_html=True)

    def glucose_status_label(value):
        """Same Low/Normal/Moderate/High thresholds used in the PDF report."""
        if value < 70:
            return '🔴 Low'
        elif value <= 140:
            return '🟢 Normal'
        elif value <= 180:
            return '🟡 Moderate'
        else:
            return '🟠 High'

    pred_df = pd.DataFrame({
        'Timepoint':      ['Now', '30 Minutes', '60 Minutes', '90 Minutes', '120 Minutes'],
        'Glucose (mg/dL)':[current_glucose, predictions[30], predictions[60], predictions[90], predictions[120]],
        'Status': [glucose_status_label(v) for v in
                   [current_glucose, predictions[30], predictions[60], predictions[90], predictions[120]]]
    })
    st.dataframe(pred_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 6 · ADVANCED VISUALIZATIONS
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="section-header sh-purple">
        <div class="section-icon">📊</div>
        <div class="section-title">SECTION 6 — Advanced Visualizations</div>
    </div>
    """, unsafe_allow_html=True)

    # Row 1: Glucose trend + Nutrition pie
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.plotly_chart(glucose_trend_chart(current_glucose, predictions),
                        use_container_width=True, config={'displayModeBar': False})
    with col_chart2:
        st.plotly_chart(nutrition_pie_chart(total_carbs, total_protein, total_fat),
                        use_container_width=True, config={'displayModeBar': False})

    # Row 2: Calorie summary
    st.plotly_chart(calorie_summary_chart(food_log),
                    use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 7 · AI HEALTH ANALYTICS
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="section-header sh-pink">
        <div class="section-icon">🧠</div>
        <div class="section-title">SECTION 7 — AI Health Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    risk_css = {'Low Risk': 'risk-low', 'Medium Risk': 'risk-medium', 'High Risk': 'risk-high'}[risk]
    risk_icon = {'Low Risk': '🟢', 'Medium Risk': '🟡', 'High Risk': '🔴'}[risk]

    col_h1, col_h2, col_h3 = st.columns(3)
    col_h1.metric("🧮 Health Score", f"{hs} / 100")
    col_h2.metric("🎯 Risk Category", f"{risk_icon} {risk}")
    col_h3.metric("🩺 Diabetes Type", diabetes_type)

    # Risk gauge — single visual for the health score (replaces the old flat bar)
    col_gauge, col_space = st.columns([1, 1.5])
    with col_gauge:
        st.plotly_chart(risk_gauge(hs, risk),
                        use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 8 · AI RECOMMENDATIONS
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="section-header sh-yellow">
        <div class="section-icon">💡</div>
        <div class="section-title">SECTION 8 — AI Health Recommendations</div>
    </div>
    """, unsafe_allow_html=True)

    recs = get_recommendations(diabetes_type, current_glucose,
                               max(predictions.values()), bmi, bmi_cat, total_carbs)

    st.markdown(f"**Personalised for:** {name} &nbsp;|&nbsp; **Status:** {diabetes_type} &nbsp;|&nbsp; **Risk:** <span class='{risk_css}'>{risk_icon} {risk}</span>", unsafe_allow_html=True)
    st.write("")
    for i, rec in enumerate(recs):
        st.markdown(f'<div class="rec-card rc-{i % 7}">{rec}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 9 · FUTURE HEALTH INSIGHT
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="section-header sh-purple">
        <div class="section-icon">🔮</div>
        <div class="section-title">SECTION 9 — Future Health Insight</div>
    </div>
    """, unsafe_allow_html=True)

    pred_120 = predictions[120]
    pct_change = ((pred_120 - current_glucose) / current_glucose) * 100 if current_glucose > 0 else 0
    direction  = "increase" if pct_change > 0 else "decrease"
    direction_icon = "📈" if pct_change > 0 else "📉"
    trend_color = '#ff3b3b' if (pct_change > 15 or pred_120 > 180) else ('#ffd60a' if pct_change > 5 else '#00e676')

    st.markdown(f"""
    <div class="insight-box">
        <div style="font-size:0.8rem; color:#64748b; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem">
            {direction_icon} 2-Hour Glucose Forecast
        </div>
        <div class="insight-value" style="color:{trend_color}">{abs(pct_change):.1f}% {direction}</div>
        <div style="font-size:0.85rem; color:#94a3b8; margin-top:0.5rem; line-height:1.6">
            Based on current inputs, your glucose is predicted to
            <strong style="color:{trend_color}">{direction} by {abs(pct_change):.1f}%</strong>
            in the next 2 hours.<br>
            Current: <strong style="color:#00d9ff">{current_glucose} mg/dL</strong>
            → Predicted: <strong style="color:{trend_color}">{pred_120} mg/dL</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Contextual insight sentences
    if diabetes_type == "No Diabetes" and pct_change > 10:
        st.info("ℹ️ Even without diabetes, a significant post-meal glucose rise is normal. Your body will naturally bring levels back to baseline within 2–3 hours.")
    elif diabetes_type in ["Type 1 Diabetes", "Type 2 Diabetes"] and pred_120 > 180:
        st.warning("⚠️ Glucose is predicted to remain elevated. Consider consulting your healthcare team about adjusting carbohydrate intake or insulin dosage.")
    elif pred_120 < 70:
        st.error("🚨 Glucose may drop into hypoglycemia range. Monitor closely and have fast-acting carbohydrates (juice, glucose tablets) available.")

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 10 · EXPORT REPORT (PDF)
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="section-header sh-blue">
        <div class="section-icon">📄</div>
        <div class="section-title">SECTION 10 — Export Health Report</div>
    </div>
    """, unsafe_allow_html=True)

    col_exp1, col_exp2 = st.columns([2, 1])
    with col_exp1:
        st.markdown("""
        <div class="glass-card" style="padding:1.2rem">
            <strong style="color:#00d9ff">📥 Download PDF Health Report</strong><br>
            <span style="font-size:0.85rem; color:#64748b">
            Your personalised health report includes patient profile, nutrition summary,
            glucose predictions, health score, and AI recommendations.
            </span>
        </div>
        """, unsafe_allow_html=True)

    with col_exp2:
        if st.button("📥 Generate & Download PDF", key="pdf_btn"):
            with st.spinner("🔄 Generating your personalised health report..."):
                patient_info = {
                    'name': name, 'age': age, 'gender': gender,
                    'weight': weight, 'height': height, 'diabetes': diabetes_type,
                }
                nutrition_summary = {
                    'calories': total_cal, 'carbs': total_carbs,
                    'protein': total_protein, 'fat': total_fat,
                }
                pdf_bytes = generate_pdf_report(
                    patient=patient_info,
                    nutrition=nutrition_summary,
                    glucose_now=current_glucose,
                    predictions=predictions,
                    score=hs,
                    risk=risk,
                    recommendations=recs,
                    bmi=bmi,
                    bmi_cat=bmi_cat,
                )
                st.download_button(
                    label="⬇️ Click to Download PDF",
                    data=pdf_bytes,
                    file_name=f"GlucoVision_Report_{name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    key="pdf_download",
                )
                st.success("✅ PDF generated successfully!")

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # FOOTER DISCLAIMER
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div style="text-align:center; padding: 2rem 1rem 1rem; border-top: 1px solid rgba(0,217,255,0.2);">
        <div style="font-size:0.9rem; font-weight:700; color:#ff3b3b; margin-bottom:0.5rem">
            ⚠️ IMPORTANT DISCLAIMER
        </div>
        <div style="font-size:0.8rem; color:#475569; max-width:700px; margin:0 auto; line-height:1.7">
            GlucoVision AI is an <strong style="color:#94a3b8">educational prototype</strong> created for
            science fair demonstration purposes. It is <strong style="color:#ff3b3b">NOT a medical device</strong>
            and is NOT intended for diagnosis, treatment, or any form of medical decision-making.
            The glucose predictions and health scores are generated by simplified educational models
            and do not reflect clinical accuracy. Always consult a qualified healthcare professional
            for any medical concerns.
        </div>
        <div style="font-size:0.72rem; color:#334155; margin-top:1rem">
            GlucoVision AI v1.0 · Science Fair Edition · Built with Streamlit + Plotly + ReportLab
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
