// ──────────────────────────────────────────────────────────────────────────────
// GLUCOVISION AI - Frontend JavaScript
// Replaces Python backend with Groq API integration
// Local storage for Patient Profile and Insulin Management sections
// ──────────────────────────────────────────────────────────────────────────────

// ─── FOOD DATABASE ──────────────────────────────────────────────────────────────
const FOOD_DB = {
    "Roti (1 piece, ~35g)":          { calories: 104, carbs: 22, protein: 3.1, fat: 0.9 },
    "Rice (1 cup cooked, ~200g)":    { calories: 260, carbs: 57, protein: 5.4, fat: 0.6 },
    "Apple (medium, ~182g)":         { calories: 95,  carbs: 25, protein: 0.5, fat: 0.3 },
    "Banana (medium, ~118g)":        { calories: 105, carbs: 27, protein: 1.3, fat: 0.4 },
    "Milk (1 cup, 240ml)":           { calories: 149, carbs: 12, protein: 8.0, fat: 8.0 },
    "Dal (1 cup, ~200g)":            { calories: 230, carbs: 40, protein: 15,  fat: 1.0 },
    "Pizza (1 slice, ~107g)":        { calories: 285, carbs: 36, protein: 12,  fat: 10 },
    "Burger (standard, ~150g)":      { calories: 354, carbs: 29, protein: 20,  fat: 17 },
    "Bread (1 slice, ~25g)":         { calories: 67,  carbs: 13, protein: 2.3, fat: 0.9 },
    "Juice (orange, 1 cup, 240ml)":  { calories: 112, carbs: 26, protein: 1.7, fat: 0.5 },
    "Egg (1 large, boiled)":         { calories: 78,  carbs: 0.6, protein: 6.3, fat: 5.3 },
    "Chapati (1 piece, ~40g)":       { calories: 120, carbs: 25, protein: 3.5, fat: 1.2 },
    "Idli (1 piece, ~39g)":          { calories: 39,  carbs: 8,  protein: 1.8, fat: 0.2 },
    "Dosa (plain, ~55g)":            { calories: 133, carbs: 25, protein: 3.5, fat: 2.5 },
    "Sambar (1 cup, ~240ml)":        { calories: 102, carbs: 15, protein: 5.5, fat: 2.5 },
    "Chicken breast (100g, cooked)": { calories: 165, carbs: 0,  protein: 31,  fat: 3.6 },
    "Paneer (100g)":                 { calories: 265, carbs: 3.4, protein: 18,  fat: 20 },
    "Oats (1 cup cooked, ~234g)":    { calories: 166, carbs: 28, protein: 5.9, fat: 3.6 },
    "Coffee (black, 240ml)":         { calories: 5,   carbs: 0,  protein: 0.3, fat: 0.1 },
    "Tea with milk (240ml)":         { calories: 30,  carbs: 3,  protein: 1.5, fat: 1.5 },
};

// ─── INSULIN TYPES ──────────────────────────────────────────────────────────────
const INSULIN_TYPES = [
    "No Insulin",
    "Rapid-Acting (e.g., Lispro, Aspart)",
    "Short-Acting (Regular)",
    "Intermediate-Acting (NPH)",
    "Long-Acting (Glargine, Detemir)",
    "Mixed Insulin (70/30)",
];

// ─── LOCAL STORAGE KEYS ─────────────────────────────────────────────────────────
const STORAGE_KEYS = {
    PATIENT_PROFILE: 'glucovision_patient_profile',
    INSULIN_MANAGEMENT: 'glucovision_insulin_management',
    GROQ_API_KEY: 'glucovision_groq_api_key',
    GLUCOSE_HISTORY: 'glucovision_glucose_history'
};

// ─── GLOBAL VARIABLES ───────────────────────────────────────────────────────────
let glucoseChart = null;
let predictionData = null;

// ──────────────────────────────────────────────────────────────────────────────
// INITIALIZATION
// ──────────────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function() {
    // Load saved data from local storage
    loadPatientProfile();
    loadInsulinManagement();
    loadGroqApiKey();
    loadGlucoseHistory();
    
    // Populate food select dropdown
    populateFoodSelect();
    
    // Setup event listeners
    setupEventListeners();
    
    // Calculate BMI initially if data exists
    calculateBMI();
});

// ──────────────────────────────────────────────────────────────────────────────
// LOCAL STORAGE FUNCTIONS
// ──────────────────────────────────────────────────────────────────────────────

function savePatientProfile() {
    const profile = {
        name: document.getElementById('patient-name').value,
        age: document.getElementById('patient-age').value,
        gender: document.getElementById('patient-gender').value,
        weight: document.getElementById('patient-weight').value,
        height: document.getElementById('patient-height').value,
        diabetesType: document.getElementById('patient-diabetes-type').value
    };
    localStorage.setItem(STORAGE_KEYS.PATIENT_PROFILE, JSON.stringify(profile));
}

function loadPatientProfile() {
    const saved = localStorage.getItem(STORAGE_KEYS.PATIENT_PROFILE);
    if (saved) {
        const profile = JSON.parse(saved);
        document.getElementById('patient-name').value = profile.name || '';
        document.getElementById('patient-age').value = profile.age || '';
        document.getElementById('patient-gender').value = profile.gender || '';
        document.getElementById('patient-weight').value = profile.weight || '';
        document.getElementById('patient-height').value = profile.height || '';
        document.getElementById('patient-diabetes-type').value = profile.diabetesType || '';
        calculateBMI();
    }
}

function saveInsulinManagement() {
    const insulin = {
        type: document.getElementById('insulin-type').value,
        dose: document.getElementById('insulin-dose').value,
        timeSinceInjection: document.getElementById('time-since-injection').value
    };
    localStorage.setItem(STORAGE_KEYS.INSULIN_MANAGEMENT, JSON.stringify(insulin));
}

function loadInsulinManagement() {
    const saved = localStorage.getItem(STORAGE_KEYS.INSULIN_MANAGEMENT);
    if (saved) {
        const insulin = JSON.parse(saved);
        document.getElementById('insulin-type').value = insulin.type || 'No Insulin';
        document.getElementById('insulin-dose').value = insulin.dose || '';
        document.getElementById('time-since-injection').value = insulin.timeSinceInjection || '';
        updateInsulinFields();
    }
}

function saveGroqApiKey(key) {
    localStorage.setItem(STORAGE_KEYS.GROQ_API_KEY, key);
}

function loadGroqApiKey() {
    const saved = localStorage.getItem(STORAGE_KEYS.GROQ_API_KEY);
    if (saved) {
        document.getElementById('groq-api-key').value = saved;
    }
}

function saveGlucoseHistory() {
    const rows = document.querySelectorAll('#glucose-history-table tbody tr');
    const history = [];
    rows.forEach(row => {
        const dateInput = row.querySelector('.glucose-date');
        const valueInput = row.querySelector('.glucose-value');
        if (dateInput && valueInput && valueInput.value) {
            history.push({
                date: dateInput.value,
                glucose: parseFloat(valueInput.value)
            });
        }
    });
    localStorage.setItem(STORAGE_KEYS.GLCOSE_HISTORY, JSON.stringify(history));
    return history;
}

function loadGlucoseHistory() {
    const saved = localStorage.getItem(STORAGE_KEYS.GLCOSE_HISTORY);
    if (saved) {
        const history = JSON.parse(saved);
        const tbody = document.querySelector('#glucose-history-table tbody');
        tbody.innerHTML = '';
        
        if (history.length > 0) {
            history.forEach(item => {
                addGlucoseRow(item.date, item.glucose);
            });
        } else {
            // Add one empty row
            addGlucoseRow();
        }
        calculateThreeMonthMetrics();
    }
}

function clearAllData() {
    if (confirm('Are you sure you want to clear all saved data? This cannot be undone.')) {
        localStorage.removeItem(STORAGE_KEYS.PATIENT_PROFILE);
        localStorage.removeItem(STORAGE_KEYS.INSULIN_MANAGEMENT);
        localStorage.removeItem(STORAGE_KEYS.GROQ_API_KEY);
        localStorage.removeItem(STORAGE_KEYS.GLCOSE_HISTORY);
        location.reload();
    }
}

// ──────────────────────────────────────────────────────────────────────────────
// EVENT LISTENERS
// ──────────────────────────────────────────────────────────────────────────────

function setupEventListeners() {
    // Patient Profile inputs - auto-save on change
    ['patient-name', 'patient-age', 'patient-gender', 'patient-weight', 
     'patient-height', 'patient-diabetes-type'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', () => {
                savePatientProfile();
                if (id === 'patient-weight' || id === 'patient-height') {
                    calculateBMI();
                }
                if (id === 'patient-diabetes-type') {
                    updateInsulinFields();
                }
            });
        }
    });

    // Insulin Management inputs - auto-save on change
    ['insulin-type', 'insulin-dose', 'time-since-injection'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', () => {
                saveInsulinManagement();
                if (id === 'insulin-type') {
                    updateInsulinFields();
                }
            });
        }
    });

    // Groq API Key - auto-save
    const apiKeyInput = document.getElementById('groq-api-key');
    if (apiKeyInput) {
        apiKeyInput.addEventListener('change', (e) => {
            saveGroqApiKey(e.target.value);
        });
    }

    // Food selection
    const foodSelect = document.getElementById('food-select');
    if (foodSelect) {
        foodSelect.addEventListener('change', handleFoodSelection);
    }

    // Navigation pills
    document.querySelectorAll('.nav-pill').forEach(pill => {
        pill.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.nav-pill').forEach(p => p.classList.remove('active'));
            this.classList.add('active');
            
            const targetId = this.getAttribute('href').substring(1);
            document.getElementById(targetId).scrollIntoView({ behavior: 'smooth' });
        });
    });
}

// ──────────────────────────────────────────────────────────────────────────────
// PATIENT PROFILE FUNCTIONS
// ──────────────────────────────────────────────────────────────────────────────

function calculateBMI() {
    const weight = parseFloat(document.getElementById('patient-weight').value);
    const height = parseFloat(document.getElementById('patient-height').value);
    
    if (weight > 0 && height > 0) {
        const bmi = weight / ((height / 100) ** 2);
        const roundedBMI = Math.round(bmi * 10) / 10;
        
        let category = 'N/A';
        if (bmi < 18.5) category = 'Underweight';
        else if (bmi < 25) category = 'Normal';
        else if (bmi < 30) category = 'Overweight';
        else category = 'Obese';
        
        document.getElementById('bmi-value').textContent = roundedBMI;
        document.getElementById('bmi-category').textContent = category;
        
        const diabetesType = document.getElementById('patient-diabetes-type').value;
        document.getElementById('diabetes-status-display').textContent = 
            diabetesType ? diabetesType.split(' ')[0] : '--';
    }
}

function addGlucoseRow(date = '', glucose = '') {
    const tbody = document.querySelector('#glucose-history-table tbody');
    const row = document.createElement('tr');
    row.innerHTML = `
        <td><input type="date" class="glucose-date" value="${date}"></td>
        <td><input type="number" class="glucose-value" min="40" max="600" placeholder="mg/dL" value="${glucose}"></td>
        <td><button class="btn-remove" onclick="removeRow(this)">✕</button></td>
    `;
    tbody.appendChild(row);
    
    // Add event listener to new input
    const valueInput = row.querySelector('.glucose-value');
    valueInput.addEventListener('input', () => {
        saveGlucoseHistory();
        calculateThreeMonthMetrics();
    });
    
    const dateInput = row.querySelector('.glucose-date');
    dateInput.addEventListener('change', () => {
        saveGlucoseHistory();
        calculateThreeMonthMetrics();
    });
}

function removeRow(button) {
    const row = button.closest('tr');
    const tbody = document.querySelector('#glucose-history-table tbody');
    
    // Don't remove the last row
    if (tbody.querySelectorAll('tr').length > 1) {
        row.remove();
        saveGlucoseHistory();
        calculateThreeMonthMetrics();
    }
}

function calculateThreeMonthMetrics() {
    const rows = document.querySelectorAll('#glucose-history-table tbody tr');
    const readings = [];
    
    rows.forEach(row => {
        const dateInput = row.querySelector('.glucose-date');
        const valueInput = row.querySelector('.glucose-value');
        if (dateInput && valueInput && valueInput.value && parseFloat(valueInput.value) > 0) {
            readings.push(parseFloat(valueInput.value));
        }
    });
    
    if (readings.length > 0) {
        const avg = readings.reduce((a, b) => a + b, 0) / readings.length;
        const estimatedA1c = (avg + 46.7) / 28.7; // Standard formula
        
        let classification = 'Normal';
        if (avg >= 126) classification = 'Diabetes Range';
        else if (avg >= 100) classification = 'Prediabetes Range';
        
        document.getElementById('three-month-avg').textContent = Math.round(avg) + ' mg/dL';
        document.getElementById('estimated-a1c').textContent = estimatedA1c.toFixed(1) + '%';
        document.getElementById('three-month-classification').textContent = classification;
        
        document.getElementById('three-month-metrics').style.display = 'grid';
    } else {
        document.getElementById('three-month-metrics').style.display = 'none';
    }
}

// ──────────────────────────────────────────────────────────────────────────────
// INSULIN MANAGEMENT FUNCTIONS
// ──────────────────────────────────────────────────────────────────────────────

function updateInsulinFields() {
    const diabetesType = document.getElementById('patient-diabetes-type').value;
    const insulinType = document.getElementById('insulin-type').value;
    const doseInput = document.getElementById('insulin-dose');
    const timeInput = document.getElementById('time-since-injection');
    const infoBox = document.getElementById('insulin-info');
    
    if (diabetesType === 'No Diabetes' || insulinType === 'No Insulin') {
        doseInput.disabled = true;
        timeInput.disabled = true;
        doseInput.value = '';
        timeInput.value = '';
        infoBox.style.display = 'block';
        infoBox.innerHTML = '💡 No insulin required — patient has no diabetes.';
    } else {
        doseInput.disabled = false;
        timeInput.disabled = false;
        infoBox.style.display = 'none';
    }
    
    saveInsulinManagement();
}

// ──────────────────────────────────────────────────────────────────────────────
// FOOD INTELLIGENCE FUNCTIONS
// ──────────────────────────────────────────────────────────────────────────────

function populateFoodSelect() {
    const select = document.getElementById('food-select');
    Object.keys(FOOD_DB).forEach(food => {
        const option = document.createElement('option');
        option.value = food;
        option.textContent = food;
        select.appendChild(option);
    });
}

function handleFoodSelection() {
    const select = document.getElementById('food-select');
    const selectedFoods = Array.from(select.selectedOptions).map(opt => opt.value);
    const quantitiesDiv = document.getElementById('food-quantities');
    const nutritionSummary = document.getElementById('nutrition-summary');
    
    if (selectedFoods.length === 0) {
        quantitiesDiv.innerHTML = '';
        nutritionSummary.style.display = 'none';
        return;
    }
    
    let html = '<div class="form-row">';
    selectedFoods.forEach((food, index) => {
        const foodName = food.split('(')[0].trim();
        html += `
            <div class="form-group">
                <label>× ${foodName}</label>
                <input type="number" class="food-qty" data-food="${food}" 
                       min="0.5" max="10" step="0.5" value="1" 
                       onchange="calculateNutrition()">
            </div>
        `;
    });
    html += '</div>';
    
    quantitiesDiv.innerHTML = html;
    calculateNutrition();
}

function calculateNutrition() {
    const qtyInputs = document.querySelectorAll('.food-qty');
    let totalCal = 0, totalCarbs = 0, totalProtein = 0, totalFat = 0;
    
    qtyInputs.forEach(input => {
        const food = input.dataset.food;
        const qty = parseFloat(input.value) || 0;
        const nutrition = FOOD_DB[food];
        
        totalCal += nutrition.calories * qty;
        totalCarbs += nutrition.carbs * qty;
        totalProtein += nutrition.protein * qty;
        totalFat += nutrition.fat * qty;
    });
    
    document.getElementById('total-calories').textContent = Math.round(totalCal) + ' kcal';
    document.getElementById('total-carbs').textContent = totalCarbs.toFixed(1) + ' g';
    document.getElementById('total-protein').textContent = totalProtein.toFixed(1) + ' g';
    document.getElementById('total-fat').textContent = totalFat.toFixed(1) + ' g';
    
    document.getElementById('nutrition-summary').style.display = 'grid';
}

// ──────────────────────────────────────────────────────────────────────────────
// GROQ API INTEGRATION
// ──────────────────────────────────────────────────────────────────────────────

async function predictGlucose() {
    const apiKey = document.getElementById('groq-api-key').value.trim();
    
    if (!apiKey) {
        alert('Please enter your Groq API key.');
        return;
    }
    
    // Gather all input data
    const currentGlucose = parseFloat(document.getElementById('current-glucose').value) || 0;
    const diabetesType = document.getElementById('patient-diabetes-type').value || 'Not specified';
    const insulinType = document.getElementById('insulin-type').value || 'No Insulin';
    const insulinDose = parseFloat(document.getElementById('insulin-dose').value) || 0;
    const timeSinceInjection = parseFloat(document.getElementById('time-since-injection').value) || 0;
    const weight = parseFloat(document.getElementById('patient-weight').value) || 70;
    const age = parseInt(document.getElementById('patient-age').value) || 35;
    const gender = document.getElementById('patient-gender').value || 'Male';
    
    // Get nutrition data
    let totalCarbs = 0;
    const qtyInputs = document.querySelectorAll('.food-qty');
    qtyInputs.forEach(input => {
        const food = input.dataset.food;
        const qty = parseFloat(input.value) || 0;
        totalCarbs += FOOD_DB[food].carbs * qty;
    });
    
    const exerciseType = document.getElementById('exercise-type').value || 'No Exercise';
    const exerciseDuration = parseInt(document.getElementById('exercise-duration').value) || 0;
    const timeSinceMeal = parseFloat(document.getElementById('time-since-meal').value) || 0;
    
    if (currentGlucose <= 0) {
        alert('Please enter your current blood glucose level.');
        return;
    }
    
    // Show loading state
    document.getElementById('prediction-loading').style.display = 'block';
    document.getElementById('prediction-results').style.display = 'none';
    
    // Build prompt for Groq API
    const prompt = `You are an AI-powered diabetes health assistant. Based on the following patient data, predict their blood glucose levels at 30, 60, 90, and 120 minutes from now. Provide realistic predictions based on physiological principles.

PATIENT DATA:
- Current Blood Glucose: ${currentGlucose} mg/dL
- Diabetes Status: ${diabetesType}
- Age: ${age} years
- Gender: ${gender}
- Weight: ${weight} kg
- Insulin Type: ${insulinType}
- Insulin Dose: ${insulinDose} units
- Time Since Insulin Injection: ${timeSinceInjection} hours
- Carbohydrates Consumed: ${totalCarbs.toFixed(1)} grams
- Time Since Meal: ${timeSinceMeal} hours
- Exercise Type: ${exerciseType}
- Exercise Duration: ${exerciseDuration} minutes

Provide your response in the following EXACT JSON format (no additional text):
{
    "prediction_30min": <number>,
    "prediction_60min": <number>,
    "prediction_90min": <number>,
    "prediction_120min": <number>,
    "insight": "<brief explanation of the prediction and any relevant health insights>"
}

Ensure predictions are physiologically realistic. For example:
- If no diabetes and normal insulin function, glucose should return to baseline within 2 hours
- If Type 1 or Type 2 diabetes, glucose may remain elevated longer
- Insulin should lower glucose predictions
- Carbohydrates should raise glucose predictions
- Exercise should lower glucose predictions`;

    try {
        const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'llama-3.1-70b-versatile',
                messages: [
                    {
                        role: 'system',
                        content: 'You are an expert AI health assistant specializing in diabetes management and glucose prediction. You provide accurate, physiologically-based predictions and helpful health insights. Always respond with valid JSON only when asked for predictions.'
                    },
                    {
                        role: 'user',
                        content: prompt
                    }
                ],
                temperature: 0.3,
                max_tokens: 500
            })
        });
        
        if (!response.ok) {
            throw new Error(`API request failed with status ${response.status}`);
        }
        
        const data = await response.json();
        const content = data.choices[0].message.content.trim();
        
        // Parse JSON from response (handle potential markdown code blocks)
        let jsonStr = content;
        if (content.includes('```json')) {
            jsonStr = content.split('```json')[1].split('```')[0].trim();
        } else if (content.includes('```')) {
            jsonStr = content.split('```')[1].split('```')[0].trim();
        }
        
        const prediction = JSON.parse(jsonStr);
        
        // Display results
        displayPredictionResults(prediction);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to get prediction from Groq API. Please check your API key and try again.\n\nError: ' + error.message);
        document.getElementById('prediction-loading').style.display = 'none';
    }
}

function displayPredictionResults(prediction) {
    document.getElementById('prediction-loading').style.display = 'none';
    document.getElementById('prediction-results').style.display = 'block';
    
    document.getElementById('pred-30min').textContent = Math.round(prediction.prediction_30min);
    document.getElementById('pred-60min').textContent = Math.round(prediction.prediction_60min);
    document.getElementById('pred-90min').textContent = Math.round(prediction.prediction_90min);
    document.getElementById('pred-120min').textContent = Math.round(prediction.prediction_120min);
    document.getElementById('ai-prediction-insight').textContent = prediction.insight;
    
    // Store for chart and risk assessment
    predictionData = {
        current: parseFloat(document.getElementById('current-glucose').value),
        predictions: [
            prediction.prediction_30min,
            prediction.prediction_60min,
            prediction.prediction_90min,
            prediction.prediction_120min
        ]
    };
    
    // Update chart
    updateGlucoseChart();
    
    // Update risk assessment
    updateRiskAssessment(prediction);
    
    // Generate recommendations
    generateRecommendations(prediction);
}

// ──────────────────────────────────────────────────────────────────────────────
// RISK ASSESSMENT & RECOMMENDATIONS
// ──────────────────────────────────────────────────────────────────────────────

function updateRiskAssessment(prediction) {
    const diabetesType = document.getElementById('patient-diabetes-type').value;
    const currentGlucose = predictionData.current;
    const maxPredicted = Math.max(...predictionData.predictions);
    const minPredicted = Math.min(...predictionData.predictions);
    
    let riskLevel = 'low';
    let riskText = 'Low Risk';
    
    // Check for hypoglycemia risk
    if (minPredicted < 70) {
        riskLevel = 'high';
        riskText = 'High Risk - Hypoglycemia Warning';
    }
    // Check for hyperglycemia risk
    else if (maxPredicted > 250 || (diabetesType.includes('Type 1') && maxPredicted > 200)) {
        riskLevel = 'high';
        riskText = 'High Risk - Hyperglycemia Warning';
    }
    // Check for moderate risk
    else if (maxPredicted > 180 || minPredicted < 80) {
        riskLevel = 'medium';
        riskText = 'Moderate Risk - Monitor Closely';
    }
    
    const riskDisplay = document.getElementById('risk-display');
    riskDisplay.innerHTML = `<span class="risk-${riskLevel}">${riskText}</span>`;
}

function generateRecommendations(prediction) {
    const diabetesType = document.getElementById('patient-diabetes-type').value;
    const insulinType = document.getElementById('insulin-type').value;
    const exerciseType = document.getElementById('exercise-type').value;
    const currentGlucose = predictionData.current;
    const predictions = predictionData.predictions;
    
    const recommendations = [];
    
    // Glucose trend-based recommendations
    if (predictions[3] > currentGlucose + 30) {
        recommendations.push({
            type: 'warning',
            text: '⚠️ Your glucose is predicted to rise significantly. Consider monitoring closely and consult your healthcare provider about appropriate interventions.'
        });
    } else if (predictions[3] < currentGlucose - 30) {
        recommendations.push({
            type: 'warning',
            text: '⚠️ Your glucose is predicted to drop. Keep fast-acting carbohydrates nearby and monitor for hypoglycemia symptoms.'
        });
    }
    
    // Diabetes-specific recommendations
    if (diabetesType === 'Type 1 Diabetes') {
        recommendations.push({
            type: 'info',
            text: '💡 For Type 1 Diabetes: Ensure you have your rapid-acting insulin available if needed. Never skip meals after insulin administration.'
        });
    } else if (diabetesType === 'Type 2 Diabetes') {
        recommendations.push({
            type: 'info',
            text: '💡 For Type 2 Diabetes: Regular physical activity and balanced meals can help improve insulin sensitivity over time.'
        });
    }
    
    // Exercise recommendations
    if (exerciseType !== 'No Exercise') {
        recommendations.push({
            type: 'positive',
            text: '✅ Great job staying active! Exercise helps improve glucose control. Remember to monitor your glucose before and after physical activity.'
        });
    } else {
        recommendations.push({
            type: 'suggestion',
            text: '💡 Consider adding light physical activity like a 15-minute walk after meals to help with glucose management.'
        });
    }
    
    // Insulin reminders
    if (insulinType !== 'No Insulin') {
        recommendations.push({
            type: 'reminder',
            text: '📌 Insulin Reminder: Always take insulin as prescribed by your healthcare provider. Never adjust doses without medical supervision.'
        });
    }
    
    // General health recommendation
    recommendations.push({
        type: 'general',
        text: '🩺 Regular monitoring and maintaining a log of your glucose readings can help you and your healthcare provider make better treatment decisions.'
    });
    
    // Display recommendations
    const container = document.getElementById('recommendations-list');
    container.innerHTML = '';
    
    recommendations.forEach((rec, index) => {
        const div = document.createElement('div');
        div.className = `rec-card rc-${index % 7}`;
        div.textContent = rec.text;
        container.appendChild(div);
    });
    
    // Update AI insights section
    const insightsBox = document.getElementById('ai-insights');
    insightsBox.innerHTML = `
        <p style="margin-bottom: 1rem;"><strong>AI Analysis Summary:</strong></p>
        <p>${prediction.insight}</p>
        <p style="margin-top: 1rem; font-size: 0.85rem; color: #8b949e;">
            ⚠️ Remember: These are AI-generated educational insights only. Always consult with qualified healthcare professionals for medical advice.
        </p>
    `;
}

// ──────────────────────────────────────────────────────────────────────────────
// CHART VISUALIZATION
// ──────────────────────────────────────────────────────────────────────────────

function updateGlucoseChart() {
    const ctx = document.getElementById('glucose-chart').getContext('2d');
    
    if (!predictionData) return;
    
    const labels = ['Current', '30 min', '60 min', '90 min', '120 min'];
    const data = [predictionData.current, ...predictionData.predictions];
    
    // Normal glucose range for reference
    const normalRange = [70, 140];
    
    if (glucoseChart) {
        glucoseChart.destroy();
    }
    
    glucoseChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Predicted Glucose (mg/dL)',
                data: data,
                borderColor: '#00d9ff',
                backgroundColor: 'rgba(0, 217, 255, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#00d9ff',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#ffffff',
                        font: {
                            family: 'Inter',
                            size: 14,
                            weight: '700'
                        }
                    }
                },
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            yMin: normalRange[0],
                            yMax: normalRange[0],
                            borderColor: '#00e676',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                content: 'Lower Normal (70)',
                                enabled: true,
                                position: 'start',
                                color: '#00e676'
                            }
                        },
                        line2: {
                            type: 'line',
                            yMin: normalRange[1],
                            yMax: normalRange[1],
                            borderColor: '#ffd60a',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                content: 'Upper Normal (140)',
                                enabled: true,
                                position: 'start',
                                color: '#ffd60a'
                            }
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: '#30363d'
                    },
                    ticks: {
                        color: '#c9d1d9',
                        font: {
                            family: 'Inter',
                            size: 12,
                            weight: '600'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Glucose (mg/dL)',
                        color: '#00d9ff',
                        font: {
                            family: 'Inter',
                            size: 14,
                            weight: '700'
                        }
                    }
                },
                x: {
                    grid: {
                        color: '#30363d'
                    },
                    ticks: {
                        color: '#c9d1d9',
                        font: {
                            family: 'Inter',
                            size: 12,
                            weight: '600'
                        }
                    }
                }
            }
        }
    });
}

// ──────────────────────────────────────────────────────────────────────────────
// EXPORT REPORT
// ──────────────────────────────────────────────────────────────────────────────

function exportReport() {
    const patientName = document.getElementById('patient-name').value || 'Unknown';
    const date = new Date().toLocaleDateString();
    
    const reportContent = `
GLUCOVISION AI - HEALTH REPORT
==============================
Generated: ${date}

PATIENT INFORMATION:
-------------------
Name: ${patientName}
Age: ${document.getElementById('patient-age').value || 'N/A'}
Gender: ${document.getElementById('patient-gender').value || 'N/A'}
Weight: ${document.getElementById('patient-weight').value || 'N/A'} kg
Height: ${document.getElementById('patient-height').value || 'N/A'} cm
Diabetes Status: ${document.getElementById('patient-diabetes-type').value || 'N/A'}

INSULIN MANAGEMENT:
------------------
Insulin Type: ${document.getElementById('insulin-type').value || 'N/A'}
Insulin Dose: ${document.getElementById('insulin-dose').value || 'N/A'} units
Time Since Last Injection: ${document.getElementById('time-since-injection').value || 'N/A'} hours

CURRENT STATUS:
--------------
Current Glucose: ${document.getElementById('current-glucose').value || 'N/A'} mg/dL
Exercise: ${document.getElementById('exercise-type').value || 'No Exercise'} (${document.getElementById('exercise-duration').value || '0'} minutes)

PREDICTIONS:
-----------
${predictionData ? `
30 minutes:  ${Math.round(predictionData.predictions[0])} mg/dL
60 minutes:  ${Math.round(predictionData.predictions[1])} mg/dL
90 minutes:  ${Math.round(predictionData.predictions[2])} mg/dL
120 minutes: ${Math.round(predictionData.predictions[3])} mg/dL
` : 'No predictions generated yet.'}

DISCLAIMER:
----------
This report is for educational purposes only and is not a medical device.
Always consult healthcare professionals for medical advice, diagnosis, or treatment.
`;
    
    // Create and download file
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `GlucoVision_Report_${patientName.replace(/\s+/g, '_')}_${date.replace(/\//g, '-')}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
