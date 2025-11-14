// Email validation
export const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

// Password validation
export const isValidPassword = (password) => {
    return password && password.length >= 8;
};

// Phone number validation (basic)
export const isValidPhone = (phone) => {
    const phoneRegex = /^[\d\s\-\+\(\)]+$/;
    return phone && phoneRegex.test(phone) && phone.replace(/\D/g, '').length >= 10;
};

// Age validation
export const isValidAge = (age) => {
    const ageNum = parseInt(age, 10);
    return !isNaN(ageNum) && ageNum >= 13 && ageNum <= 120;
};

// Required field validation
export const isRequired = (value) => {
    if (typeof value === 'string') {
        return value.trim().length > 0;
    }
    return value !== null && value !== undefined && value !== '';
};

// Number range validation
export const isInRange = (value, min, max) => {
    const num = parseFloat(value);
    return !isNaN(num) && num >= min && num <= max;
};

// Assessment input validation
export const validateAssessmentInput = (name, value) => {
    const ranges = {
        sleepHours: { min: 0, max: 24 },
        workStress: { min: 1, max: 10 },
        screenTime: { min: 0, max: 24 },
        exerciseHours: { min: 0, max: 24 },
        foodQuality: { min: 1, max: 5 },
        financialStress: { min: 1, max: 5 },
    };

    if (ranges[name]) {
        return isInRange(value, ranges[name].min, ranges[name].max);
    }

    return true;
};

// Form validation helper
export const validateForm = (formData, rules) => {
    const errors = {};

    Object.keys(rules).forEach((field) => {
        const value = formData[field];
        const fieldRules = rules[field];

        if (fieldRules.required && !isRequired(value)) {
            errors[field] = 'This field is required';
            return;
        }

        if (fieldRules.email && value && !isValidEmail(value)) {
            errors[field] = 'Please enter a valid email address';
            return;
        }

        if (fieldRules.password && value && !isValidPassword(value)) {
            errors[field] = 'Password must be at least 8 characters';
            return;
        }

        if (fieldRules.phone && value && !isValidPhone(value)) {
            errors[field] = 'Please enter a valid phone number';
            return;
        }

        if (fieldRules.age && value && !isValidAge(value)) {
            errors[field] = 'Please enter a valid age (13-120)';
            return;
        }

        if (fieldRules.min !== undefined && fieldRules.max !== undefined) {
            if (!isInRange(value, fieldRules.min, fieldRules.max)) {
                errors[field] = `Value must be between ${fieldRules.min} and ${fieldRules.max}`;
                return;
            }
        }

        if (fieldRules.match && value !== formData[fieldRules.match]) {
            errors[field] = 'Values do not match';
            return;
        }
    });

    return {
        isValid: Object.keys(errors).length === 0,
        errors,
    };
};
