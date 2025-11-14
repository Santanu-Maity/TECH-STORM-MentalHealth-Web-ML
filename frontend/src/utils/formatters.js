// Date formatting
export const formatDate = (date, format = 'short') => {
    if (!date) return '';

    const d = new Date(date);

    if (isNaN(d.getTime())) return '';

    const options = {
        short: { month: 'short', day: 'numeric', year: 'numeric' },
        long: { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' },
        time: { hour: '2-digit', minute: '2-digit' },
        datetime: {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        },
    };

    return d.toLocaleDateString('en-US', options[format] || options.short);
};

// Time ago formatting
export const formatTimeAgo = (date) => {
    if (!date) return '';

    const now = new Date();
    const past = new Date(date);
    const diffInSeconds = Math.floor((now - past) / 1000);

    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
    if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 604800)} weeks ago`;

    return formatDate(date);
};

// Score formatting
export const formatScore = (score) => {
    if (score === null || score === undefined) return 'N/A';
    return Math.round(score);
};

// Percentage formatting
export const formatPercentage = (value, decimals = 0) => {
    if (value === null || value === undefined) return 'N/A';
    return `${(value * 100).toFixed(decimals)}%`;
};

// Phone number formatting
export const formatPhoneNumber = (phone) => {
    if (!phone) return '';

    const cleaned = phone.replace(/\D/g, '');

    if (cleaned.length === 10) {
        return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
    }

    return phone;
};

// Capitalize first letter
export const capitalize = (str) => {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

// Truncate text
export const truncate = (text, maxLength = 100) => {
    if (!text || text.length <= maxLength) return text;
    return `${text.slice(0, maxLength)}...`;
};

// Format mental state label
export const formatMentalState = (state) => {
    if (!state) return '';
    return capitalize(state);
};

// Format duration (minutes to hours/minutes)
export const formatDuration = (minutes) => {
    if (!minutes || minutes < 0) return '0 min';

    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;

    if (hours === 0) return `${mins} min`;
    if (mins === 0) return `${hours} hr`;
    return `${hours} hr ${mins} min`;
};

// Format number with commas
export const formatNumber = (num) => {
    if (num === null || num === undefined) return '0';
    return num.toLocaleString('en-US');
};

// Format assessment value for display
export const formatAssessmentValue = (key, value) => {
    const formatters = {
        sleepHours: (v) => `${v} hours`,
        workStress: (v) => `${v}/10`,
        screenTime: (v) => `${v} hours`,
        exerciseHours: (v) => `${v} hours`,
        foodQuality: (v) => `${v}/5`,
        financialStress: (v) => `${v}/5`,
        personalityType: (v) => capitalize(v),
    };

    return formatters[key] ? formatters[key](value) : value;
};
