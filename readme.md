https://glucovision1-hewqwap5atbmofrkbreapn.streamlit.app/


PROMPT:
Build me a Streamlit web app called "GlucoVision AI" — an educational, non-medical diabetes glucose prediction and monitoring prototype. It must be clearly labeled throughout as an educational prototype, NOT a medical device, with prominent disclaimers.
Core functionality — 10 sections in this order:

Patient Profile — name, age, gender, weight (kg), height (cm), diabetes status (No Diabetes / Prediabetes / Type 1 / Type 2). Auto-calculate BMI and category. Include an optional 3-month glucose history log (date + reading table) that estimates HbA1c using the standard formula HbA1c = (avg_glucose + 46.7) / 28.7 and classifies as Normal/Prediabetes/Diabetes range, with a trend chart.
Insulin Management — insulin type (rapid, short, intermediate, long-acting, mixed, or none), dose in units, hours since last injection. Skip if "No Diabetes."
Food Intelligence — a small food database (10–20 common items with calories/carbs/protein/fat per serving), multi-select with adjustable quantities, auto-summed nutrition totals.
Metabolic Digital Twin — current glucose slider, time since eating, exercise type (none/light/moderate/intense) and duration in minutes. Display a 6-metric overview panel (current glucose, predicted 60-min glucose, calories, carbs, BMI, health score).
AI Glucose Prediction — predict glucose at 30/60/90/120 minutes using a model that combines FIVE competing physiological effects:

Carb excursion: carbs raise glucose along a smooth peak-then-decay curve (use smoothstep interpolation, not linear/step functions), scaled by diabetes type (Type 1 most sensitive, No Diabetes least).
Injected insulin: onset/peak/end action curves specific to insulin type, offset by elapsed time since injection, weight-adjusted.
Resting metabolism (BMR): use Mifflin-St Jeor to estimate daily BMR, convert a small fraction of burned calories to a glucose-equivalent drop. IMPORTANT: distribute this drop across extracellular fluid volume (~2 dL per kg body weight, NOT blood plasma alone which is ~0.7 dL/kg — that's a 3x-too-small volume that will make BMR effects wildly overshoot), and use a hepatic compensation factor around 0.03 (liver replaces ~97% of burned glucose) so the net effect is only a few mg/dL over 2 hours, not tens of mg/dL.
Exercise: active glucose uptake during exercise plus a decaying "afterburn" effect for hours after. The afterburn magnitude MUST scale with actual exercise duration in minutes (not just which intensity bucket was picked) — normalize so 30 minutes is a baseline multiplier of 1x, scaling proportionally up to a cap around 90 minutes.
Apply a physiological floor so glucose can't unrealistically crash without real insulin present — but keep this floor loose enough (test at multiple exercise durations/intensities and multiple starting glucose values) that it doesn't clamp every effect to the same flat value regardless of exercise or time elapsed. Validate numerically that changing exercise duration and time elapsed both visibly change the output before finalizing constants.


Advanced Visualizations — Plotly charts: glucose trend forecast line chart, nutrition macro pie chart, calorie bar chart per food item.
AI Health Analytics — 0–100 health score based on glucose range, predicted peak, BMI, diabetes type, and carb load. Risk category (Low/Medium/High) with a gauge chart.
AI Recommendations — generate contextual bullet recommendations based on current glucose, predicted peak, diabetes type, BMI category, and carb intake.
Future Health Insight — a summary box showing % change from current to 2-hour predicted glucose with contextual warnings for hypo/hyperglycemia risk.
Export Report — generate a downloadable PDF health report via ReportLab, matching the app's visual style, including patient info, nutrition summary, glucose predictions table, health score, and recommendations, plus the same non-medical disclaimer.

Design requirements:

Dark theme (navy/black background), cyan/green accent colors, bold readable typography.
Distinct accent color per section header so it doesn't look monotone.
Prominent red disclaimer banner near the top and in the footer: educational prototype only, not for diagnosis or treatment, consult a healthcare professional.
Sidebar with navigation list and app branding.

Also provide:

A requirements.txt (streamlit, pandas, numpy, plotly, reportlab).
Before finalizing, sanity-check the prediction model numerically at a few test cases (varying exercise duration, varying time-since-meal, varying starting glucose) to confirm each input variable actually changes the output — don't just assume the formulas work, verify them with printed test ou
