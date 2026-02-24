from fastapi.responses import HTMLResponse
from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("model.pkl")
@app.get("/app", response_class=HTMLResponse)
def premium_ui():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AI Lead Scoring</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-gradient-to-r from-indigo-900 via-purple-900 to-indigo-800 flex items-center justify-center min-h-screen">

<div class="bg-white/10 backdrop-blur-lg p-8 rounded-2xl shadow-2xl w-96 text-white">

<h1 class="text-2xl font-bold text-center mb-6">AI Lead Scoring</h1>

<input id="industry" class="w-full p-2 mb-3 rounded bg-white/20" placeholder="Industry (1-5)">
<input id="revenue" class="w-full p-2 mb-3 rounded bg-white/20" placeholder="Revenue">
<input id="employees" class="w-full p-2 mb-3 rounded bg-white/20" placeholder="Employees">
<input id="website_visits" class="w-full p-2 mb-3 rounded bg-white/20" placeholder="Website Visits">
<input id="email_opens" class="w-full p-2 mb-3 rounded bg-white/20" placeholder="Email Opens">
<input id="ad_clicks" class="w-full p-2 mb-4 rounded bg-white/20" placeholder="Ad Clicks">

<button onclick="predict()" 
class="w-full bg-indigo-500 hover:bg-indigo-600 transition p-2 rounded font-semibold">
Predict Lead Score
</button>

<div class="mt-6 hidden" id="resultBox">
    <p class="text-center text-lg font-semibold" id="priorityText"></p>
    <div class="w-full bg-gray-300 rounded-full h-4 mt-3">
        <div id="progressBar" class="h-4 rounded-full transition-all duration-500"></div>
    </div>
    <p class="text-center mt-2" id="scoreText"></p>
</div>

</div>

<script>
async function predict() {

const params = new URLSearchParams({
industry: document.getElementById("industry").value,
revenue: document.getElementById("revenue").value,
employees: document.getElementById("employees").value,
website_visits: document.getElementById("website_visits").value,
email_opens: document.getElementById("email_opens").value,
ad_clicks: document.getElementById("ad_clicks").value
});

const response = await fetch("/predict?" + params, { method: "POST" });
const data = await response.json();

document.getElementById("resultBox").classList.remove("hidden");

const score = data.lead_score;
const priority = data.priority;

document.getElementById("scoreText").innerText = "Score: " + score + "%";
document.getElementById("priorityText").innerText = "Priority: " + priority;

const bar = document.getElementById("progressBar");
bar.style.width = score + "%";

if (priority === "High") {
bar.className = "h-4 rounded-full bg-green-500 transition-all duration-500";
}
else if (priority === "Medium") {
bar.className = "h-4 rounded-full bg-yellow-500 transition-all duration-500";
}
else {
bar.className = "h-4 rounded-full bg-red-500 transition-all duration-500";
}
}
</script>

</body>
</html>
"""

@app.post("/predict")
def predict_lead(
    industry: int,
    revenue: int,
    employees: int,
    website_visits: int,
    email_opens: int,
    ad_clicks: int
):

    input_data = np.array([[industry, revenue, employees,
                            website_visits, email_opens, ad_clicks]])

    prediction = model.predict_proba(input_data)[0][1]
    score = int(prediction * 100)

    if score > 70:
        priority = "High"
    elif score > 40:
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "lead_score": score,
        "priority": priority
    }