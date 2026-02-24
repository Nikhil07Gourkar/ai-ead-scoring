import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv("leads.csv")

# Encode industry
le = LabelEncoder()
data["industry"] = le.fit_transform(data["industry"])

# Split features & target
X = data.drop("converted", axis=1)
y = data["converted"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
accuracy = accuracy_score(y_test, preds)

print("Model Accuracy:", accuracy)

# Save model
joblib.dump(model, "model.pkl")
print("Model saved as model.pkl")