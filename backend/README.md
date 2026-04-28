# TECH STORM – MentalHealth Backend API

A production-ready Flask REST API for the AI-powered Mental Health Counselling Web Application.

---

## 📁 File Structure

```
mentalhealth_backend/
├── app/
│   ├── __init__.py              # App factory, extensions init
│   ├── models/
│   │   └── __init__.py          # All SQLAlchemy ORM models
│   ├── routes/
│   │   ├── auth.py              # Register, login, logout, JWT
│   │   ├── profile.py           # User profile CRUD
│   │   ├── mood.py              # Mood logging
│   │   ├── score.py             # Health score retrieval
│   │   ├── recommendation.py    # Personalised wellness content
│   │   ├── appointment.py       # Doctor listing & booking
│   │   ├── emergency.py         # SOS & crisis resources
│   │   └── dashboard.py         # Analytics & charts data
│   ├── services/
│   │   ├── score_service.py     # ML/rule-based score computation
│   │   ├── recommendation_service.py  # Content recommendation logic
│   │   ├── emergency_service.py # Emergency alert & email
│   │   └── notification_service.py    # Appointment confirmation email
│   └── utils/
│       └── validators.py        # Input validation helpers
├── ml_model/
│   └── train_model.py           # Model training script
├── config.py                    # Dev/Prod/Test configuration
├── run.py                       # Flask app entry point
├── seed.py                      # DB seed: doctors + test user
├── requirements.txt
└── .env.example
```

---

## ⚡ Quick Start

### 1. Clone and set up

```bash
git clone https://github.com/Santanu-Maity/TECH-STORM-MentalHealth-Web-ML.git
cd TECH-STORM-MentalHealth-Web-ML

# Copy backend files into the repo's backend/ folder
# (or work directly inside mentalhealth_backend/)
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env with your values (DB URL, email credentials, secret keys)
```

### 5. Initialise database & seed data

```bash
python seed.py
```

### 6. (Optional) Train the ML model

```bash
# Place your CSV at dataset/mental_health_data.csv
# OR the script auto-generates synthetic data for demo
python ml_model/train_model.py
```

### 7. Run the server

```bash
python run.py
# Server starts at http://localhost:5000
```

---

## 🗺️ API Endpoints

### Auth  `/api/auth`
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register new user |
| POST | `/login` | Login, get JWT tokens |
| POST | `/refresh` | Refresh access token |
| DELETE | `/logout` | Revoke token |
| GET | `/me` | Get current user info |
| PUT | `/change-password` | Change password |

### Profile  `/api/profile`
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Get user profile |
| PUT | `/` | Update user profile |

### Mood Tracking  `/api/mood`
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/` | Log a mood entry (triggers score computation) |
| GET | `/` | List mood logs (paginated, filterable by days) |
| GET | `/today` | Get today's mood log |
| GET | `/<id>` | Get single log |
| DELETE | `/<id>` | Delete log |

### Health Score  `/api/score`
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/latest` | Get latest computed score |
| GET | `/history` | Score history (line chart data) |

### Recommendations  `/api/recommendations`
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Personalised full recommendation set |
| GET | `/quotes?mood=calm` | Motivational quotes |
| GET | `/yoga?level=beginner` | Yoga exercises |
| GET | `/music?mood=uplifting` | Music recommendations |
| GET | `/movies?mood=inspirational` | Movie recommendations |
| GET | `/meditation?duration=10` | Meditation guides |

### Appointments  `/api/appointments`
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/doctors` | List all doctors (filter by specialization/location) |
| GET | `/doctors/<id>` | Get doctor details with available slots |
| POST | `/` | Book an appointment |
| GET | `/` | List user's appointments |
| DELETE | `/<id>` | Cancel appointment |

### Emergency  `/api/emergency`
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sos` | Manual SOS alert |
| GET | `/resources` | Crisis helpline resources (public) |
| GET | `/history` | User's alert history |

### Dashboard  `/api/dashboard`
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/summary?days=30` | Aggregated stats summary |
| GET | `/mood-trend?days=14` | Daily mood trend (chart data) |
| GET | `/score-trend?days=30` | Health score trend |
| GET | `/streak` | Consecutive logging streak |

---

## 🔐 Authentication

All protected endpoints require:
```
Authorization: Bearer <access_token>
```

- Access tokens expire in **2 hours**
- Use `/api/auth/refresh` with the refresh token to get a new one

---

## 🤖 ML Score Logic

When a mood log is submitted:
1. Features are extracted (mood, anxiety, sleep, energy, etc.)
2. If `ml_model/mental_health_model.pkl` exists → ML model predicts
3. Otherwise → weighted rule-based formula is used
4. Score is saved (0–100), risk level classified:
   - **≥70** → Low risk
   - **50–69** → Moderate
   - **30–49** → High
   - **<30** → Critical (auto-triggers emergency alert)

---

## 🚀 Production Deployment (Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "run:app"
```

Use with **Nginx** as a reverse proxy and **PostgreSQL** as the database.

---

## 🧪 Test User (after seed.py)

```
Email: test@example.com
Password: test1234
```
