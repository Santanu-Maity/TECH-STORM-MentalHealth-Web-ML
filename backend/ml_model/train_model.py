"""
train_model.py  –  Mental Health Score ML Model Training
=========================================================
Run:  python ml_model/train_model.py

This script:
1. Loads the dataset (CSV)
2. Engineers features from mood/lifestyle columns
3. Trains a Random Forest classifier
4. Saves model + scaler to ml_model/
5. Prints a classification report

Adjust LABEL_COLUMN and FEATURE_COLUMNS to match your actual dataset.
"""
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline

# ── Config ───────────────────────────────────────────────────────────────────
DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "mental_health_data.csv")
MODEL_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "mental_health_model.pkl")
SCALER_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "scaler.pkl")

# Columns in your CSV that map to MoodLog fields
FEATURE_COLUMNS = [
    "mood_rating",
    "anxiety_level",
    "sleep_hours",
    "sleep_quality",
    "energy_level",
    "social_interaction",
    "stress_level",
    "appetite",
    "concentration",
    "physical_activity_minutes",
]

# Target column: expected values → "excellent", "good", "moderate", "poor", "critical"
LABEL_COLUMN = "mental_health_label"

RANDOM_STATE = 42


# ── Helpers ──────────────────────────────────────────────────────────────────

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived features."""
    df = df.copy()
    # Overall wellbeing composite
    df["wellbeing_composite"] = (
        df["mood_rating"] + df["energy_level"] + df["sleep_quality"]
    ) / 3
    # Distress composite
    df["distress_composite"] = (df["anxiety_level"] + df["stress_level"]) / 2
    # Sleep adequacy flag
    df["adequate_sleep"] = ((df["sleep_hours"] >= 7) & (df["sleep_hours"] <= 9)).astype(int)
    return df


def load_data():
    if not os.path.exists(DATASET_PATH):
        print(f"⚠  Dataset not found at {DATASET_PATH}. Generating synthetic data for demo...")
        return _generate_synthetic_data()

    df = pd.read_csv(DATASET_PATH)
    print(f"✅ Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    missing = [c for c in FEATURE_COLUMNS + [LABEL_COLUMN] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")

    return df


def _generate_synthetic_data(n=2000) -> pd.DataFrame:
    """
    Generate synthetic mental-health records for demonstration.
    Replace this with your real dataset.
    """
    np.random.seed(RANDOM_STATE)
    data = {
        "mood_rating":              np.random.randint(1, 11, n),
        "anxiety_level":            np.random.randint(1, 11, n),
        "sleep_hours":              np.random.uniform(3, 10, n).round(1),
        "sleep_quality":            np.random.randint(1, 11, n),
        "energy_level":             np.random.randint(1, 11, n),
        "social_interaction":       np.random.randint(1, 11, n),
        "stress_level":             np.random.randint(1, 11, n),
        "appetite":                 np.random.randint(1, 11, n),
        "concentration":            np.random.randint(1, 11, n),
        "physical_activity_minutes": np.random.randint(0, 90, n),
    }
    df = pd.DataFrame(data)

    # Rule-based synthetic label
    score = (
        df["mood_rating"] * 2 + df["energy_level"] + df["sleep_quality"] +
        df["concentration"] + df["appetite"] - df["anxiety_level"] * 2 - df["stress_level"]
    )
    bins = [-np.inf, 5, 15, 25, 35, np.inf]
    labels = ["critical", "poor", "moderate", "good", "excellent"]
    df["mental_health_label"] = pd.cut(score, bins=bins, labels=labels)
    return df


# ── Main ─────────────────────────────────────────────────────────────────────

def train():
    df = load_data()
    df = engineer_features(df)
    df = df.dropna(subset=[LABEL_COLUMN])

    all_features = FEATURE_COLUMNS + ["wellbeing_composite", "distress_composite", "adequate_sleep"]
    X = df[all_features].fillna(df[all_features].median())
    y = df[LABEL_COLUMN].astype(str)

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=RANDOM_STATE, stratify=y_enc
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    model.fit(X_train_s, y_train)

    # Cross-validation
    cv_scores = cross_val_score(model, X_train_s, y_train, cv=5, scoring="accuracy")
    print(f"\n📊 CV Accuracy: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

    # Test evaluation
    y_pred = model.predict(X_test_s)
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    # Reverse-encode classes into model
    # Store label mapping inside the model for inference
    model.classes_encoded_ = le.classes_

    # Save artifacts
    os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH), exist_ok=True)
    with open(MODEL_OUTPUT_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(SCALER_OUTPUT_PATH, "wb") as f:
        pickle.dump(scaler, f)

    print(f"\n✅ Model saved to {MODEL_OUTPUT_PATH}")
    print(f"✅ Scaler saved to {SCALER_OUTPUT_PATH}")

    # Feature importances
    importances = pd.Series(model.feature_importances_, index=all_features).sort_values(ascending=False)
    print("\n🔍 Top Feature Importances:")
    print(importances.head(7).to_string())


if __name__ == "__main__":
    train()
