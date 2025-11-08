import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv("../dataset/dataset.csv")

# Encode categorical features
label_encoders = {}
for column in ["gender", "introvert_extrovert", "relationship_status", "mental_state"]:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Features (X) and Target (y)
X = df.drop(columns=["mental_state"])
y = df["mental_state"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("../backend/model.pkl", "wb"))

print("✅ Model trained and saved as model.pkl successfully!")
