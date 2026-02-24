import pandas as pd
import numpy as np
import os

np.random.seed(42)

# Create dataset
data = pd.DataFrame({
    "industry": np.random.choice(["IT", "Finance", "Retail"], 1000),
    "revenue": np.random.randint(100000, 10000000, 1000),
    "employees": np.random.randint(5, 500, 1000),
    "website_visits": np.random.randint(1, 50, 1000),
    "email_opens": np.random.randint(0, 20, 1000),
    "ad_clicks": np.random.randint(0, 15, 1000)
})

# Realistic probability-based conversion
prob = (
    0.00000002 * data["revenue"] +
    0.01 * data["website_visits"] +
    0.015 * data["email_opens"] +
    0.008 * data["ad_clicks"]
)

prob = np.clip(prob, 0, 0.9)

data["converted"] = (np.random.rand(1000) < prob).astype(int)

# Save in same folder as script
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "leads.csv")

data.to_csv(file_path, index=False)

print("Dataset saved at:", file_path)
print("Dataset generated successfully!")