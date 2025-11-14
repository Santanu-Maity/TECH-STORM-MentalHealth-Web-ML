// Mental Health States
export const MENTAL_STATES = {
    HAPPY: 'happy',
    STABLE: 'stable',
    ANXIOUS: 'anxious',
    STRESSED: 'stressed',
    DEPRESSED: 'depressed',
};

// Mental State Colors
export const MENTAL_STATE_COLORS = {
    [MENTAL_STATES.HAPPY]: '#7ED321',
    [MENTAL_STATES.STABLE]: '#4A90E2',
    [MENTAL_STATES.ANXIOUS]: '#F5A623',
    [MENTAL_STATES.STRESSED]: '#F8E71C',
    [MENTAL_STATES.DEPRESSED]: '#BD10E0',
};

// Mental State Labels
export const MENTAL_STATE_LABELS = {
    [MENTAL_STATES.HAPPY]: 'Happy',
    [MENTAL_STATES.STABLE]: 'Stable',
    [MENTAL_STATES.ANXIOUS]: 'Anxious',
    [MENTAL_STATES.STRESSED]: 'Stressed',
    [MENTAL_STATES.DEPRESSED]: 'Depressed',
};

// Personality Types
export const PERSONALITY_TYPES = {
    INTROVERT: 'introvert',
    EXTROVERT: 'extrovert',
};

// Assessment Input Ranges
export const ASSESSMENT_RANGES = {
    SLEEP_HOURS: { min: 0, max: 24 },
    WORK_STRESS: { min: 1, max: 10 },
    SCREEN_TIME: { min: 0, max: 24 },
    EXERCISE_HOURS: { min: 0, max: 24 },
    FOOD_QUALITY: { min: 1, max: 5 },
    FINANCIAL_STRESS: { min: 1, max: 5 },
};

// Time Ranges for Charts
export const TIME_RANGES = {
    WEEK: 'week',
    MONTH: 'month',
    THREE_MONTHS: '3months',
    YEAR: 'year',
};

// API Endpoints
export const API_ENDPOINTS = {
    // Auth
    SIGNUP: '/api/auth/signup',
    LOGIN: '/api/auth/login',
    LOGOUT: '/api/auth/logout',
    VERIFY: '/api/auth/verify',

    // User
    PROFILE: '/api/user/profile',
    PREFERENCES: '/api/user/preferences',

    // Assessments
    PREDICT: '/api/predict',
    ASSESSMENTS: '/api/assessments',

    // Recommendations
    RECOMMENDATIONS: '/api/recommendations',

    // Appointments
    DOCTORS: '/api/doctors',
    APPOINTMENTS: '/api/appointments',

    // Resources
    RESOURCES: '/api/resources',
};

// Local Storage Keys
export const STORAGE_KEYS = {
    AUTH_TOKEN: 'authToken',
    USER: 'user',
    ASSESSMENT_DRAFT: 'assessmentDraft',
    PREFERENCES: 'preferences',
    THEME: 'theme',
};

// Emergency Contacts
export const EMERGENCY_CONTACTS = {
    CRISIS_HOTLINE: '988',
    EMERGENCY: '911',
    CRISIS_TEXT: 'Text HOME to 741741',
};

// Resource Categories
export const RESOURCE_CATEGORIES = {
    MEDITATION: 'meditation',
    YOGA: 'yoga',
    MUSIC: 'music',
    READING: 'reading',
    BREATHING: 'breathing',
    EXERCISE: 'exercise',
};

// Appointment Status
export const APPOINTMENT_STATUS = {
    PENDING: 'pending',
    CONFIRMED: 'confirmed',
    COMPLETED: 'completed',
    CANCELLED: 'cancelled',
};

// Validation Messages
export const VALIDATION_MESSAGES = {
    REQUIRED: 'This field is required',
    EMAIL_INVALID: 'Please enter a valid email address',
    PASSWORD_MIN_LENGTH: 'Password must be at least 8 characters',
    PASSWORD_MISMATCH: 'Passwords do not match',
    PHONE_INVALID: 'Please enter a valid phone number',
    AGE_INVALID: 'Please enter a valid age',
};
