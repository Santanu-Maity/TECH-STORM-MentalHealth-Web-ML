import pandas as pd
import numpy as np
import random

# -------------------------------
# 🎯 Purpose: Generate realistic mental health dataset
# -------------------------------

np.random.seed(42)

n_samples = 500

# Feature generation
data = {
    "age": np.random.randint(18, 60, n_samples),
    "gender": np.random.choice(["male", "female", "other"], n_samples),
    "sleep_hours": np.random.randint(3, 10, n_samples),
    "food_quality": np.random.randint(1, 6, n_samples),
    "exercise_hours": np.random.randint(0, 3, n_samples),
    "work_stress": np.random.randint(1, 11, n_samples),
    "screen_time": np.random.randint(2, 16, n_samples),
    "health_issues": np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
    "social_interaction": np.random.randint(1, 6, n_samples),
    "introvert_extrovert": np.random.choice(["introvert", "extrovert"], n_samples),
    "financial_stress": np.random.randint(1, 6, n_samples),
    "relationship_status": np.random.choice(["single", "in_relationship", "married"], n_samples),
    "academic_pressure": np.random.randint(1, 11, n_samples),
    "job_satisfaction": np.random.randint(1, 11, n_samples),
    "family_support": np.random.randint(1, 6, n_samples),
    "sleep_quality": np.random.randint(1, 6, n_samples),
    "physical_pain": np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
    "anxiety_level": np.random.randint(1, 11, n_samples),
    "depression_level": np.random.randint(1, 11, n_samples),
    "optimism_score": np.random.randint(1, 11, n_samples)
}

df = pd.DataFrame(data)

# -------------------------------
# 🌿 Generate mental_state labels using logical rules
# -------------------------------
def determine_mental_state(row):
    # Weighted mental health score
    score = 0
    score += (8 - row["sleep_hours"]) * 1.0
    score += (5 - row["food_quality"]) * 0.8
    score += row["work_stress"] * 0.8
    score += row["academic_pressure"] * 0.6
    score += row["financial_stress"] * 0.7
    score += row["depression_level"] * 0.9
    score += row["anxiety_level"] * 0.8
    score += row["screen_time"] * 0.4
    score += (1 if row["health_issues"] == 1 else 0) * 1.2
    score += (1 if row["physical_pain"] == 1 else 0) * 0.8
    score -= row["exercise_hours"] * 1.0
    score -= row["social_interaction"] * 0.6
    score -= row["family_support"] * 0.6
    score -= row["optimism_score"] * 1.0
    score -= row["job_satisfaction"] * 0.4

    # Determine label
    if score < 10:
        return "happy"
    elif score < 15:
        return "stable"
    elif score < 20:
        return "stressed"
    elif score < 25:
        return "anxious"
    else:
        return "depressed"

# Apply function to dataset
df["mental_state"] = df.apply(determine_mental_state, axis=1)

# Save dataset
df.to_csv("dataset.csv", index=False)
print("✅ dataset.csv generated successfully with 500 realistic entries!")
