import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import Input from '../../common/Input';
import Button from '../../common/Button';
import Card from '../../common/Card';
import { validateForm } from '../../../utils/validators';
import './SignupForm.css';

const SignupForm = ({ onSuccess, onError }) => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
        age: '',
        acceptTerms: false,
    });
    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value,
        }));
        // Clear error for this field
        if (errors[name]) {
            setErrors((prev) => ({
                ...prev,
                [name]: '',
            }));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validate form
        const validation = validateForm(formData, {
            name: { required: true },
            email: { required: true, email: true },
            password: { required: true, password: true },
            confirmPassword: { required: true, match: 'password' },
            age: { required: true, age: true },
        });

        if (!validation.isValid) {
            setErrors(validation.errors);
            return;
        }

        if (!formData.acceptTerms) {
            setErrors({ acceptTerms: 'You must accept the terms and conditions' });
            return;
        }

        setLoading(true);
        setErrors({});

        try {
            // Call backend API
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/auth/signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: formData.name,
                    email: formData.email,
                    password: formData.password,
                    age: parseInt(formData.age, 10),
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Signup failed');
            }

            // Successful signup
            if (onSuccess) {
                onSuccess(data.user, data.token);
            }

            navigate('/dashboard');
        } catch (error) {
            const errorMessage = error.message || 'Signup failed. Please try again.';
            setErrors({ submit: errorMessage });

            if (onError) {
                onError(error);
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="signup-form-container">
            <Card className="signup-card">
                <div className="signup-header">
                    <h1 className="signup-title">Create Account</h1>
                    <p className="signup-subtitle">Start your mental wellness journey today</p>
                </div>

                <form onSubmit={handleSubmit} className="signup-form" noValidate>
                    <Input
                        type="text"
                        name="name"
                        label="Full Name"
                        value={formData.name}
                        onChange={handleChange}
                        error={errors.name}
                        placeholder="Enter your full name"
                        required
                        autoComplete="name"
                    />

                    <Input
                        type="email"
                        name="email"
                        label="Email Address"
                        value={formData.email}
                        onChange={handleChange}
                        error={errors.email}
                        placeholder="Enter your email"
                        required
                        autoComplete="email"
                    />

                    <div className="signup-row">
                        <Input
                            type="password"
                            name="password"
                            label="Password"
                            value={formData.password}
                            onChange={handleChange}
                            error={errors.password}
                            placeholder="Create password"
                            required
                            autoComplete="new-password"
                        />

                        <Input
                            type="password"
                            name="confirmPassword"
                            label="Confirm Password"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            error={errors.confirmPassword}
                            placeholder="Confirm password"
                            required
                            autoComplete="new-password"
                        />
                    </div>

                    <Input
                        type="number"
                        name="age"
                        label="Age"
                        value={formData.age}
                        onChange={handleChange}
                        error={errors.age}
                        placeholder="Enter your age"
                        required
                        min="13"
                        max="120"
                    />

                    <div className="signup-terms">
                        <input
                            type="checkbox"
                            id="acceptTerms"
                            name="acceptTerms"
                            checked={formData.acceptTerms}
                            onChange={handleChange}
                            aria-describedby={errors.acceptTerms ? 'terms-error' : undefined}
                        />
                        <label htmlFor="acceptTerms">
                            I agree to the{' '}
                            <a href="/terms" className="signup-terms-link" target="_blank" rel="noopener noreferrer">
                                Terms of Service
                            </a>{' '}
                            and{' '}
                            <a href="/privacy" className="signup-terms-link" target="_blank" rel="noopener noreferrer">
                                Privacy Policy
                            </a>
                        </label>
                    </div>
                    {errors.acceptTerms && (
                        <span id="terms-error" className="signup-error" role="alert">
                            {errors.acceptTerms}
                        </span>
                    )}

                    {errors.submit && (
                        <div className="signup-error" role="alert">
                            {errors.submit}
                        </div>
                    )}

                    <Button
                        type="submit"
                        variant="primary"
                        size="large"
                        loading={loading}
                        className="signup-button"
                    >
                        Create Account
                    </Button>
                </form>

                <div className="signup-footer">
                    <p className="signup-footer-text">
                        Already have an account?{' '}
                        <Link to="/login" className="signup-link">
                            Sign in
                        </Link>
                    </p>
                </div>
            </Card>
        </div>
    );
};

SignupForm.propTypes = {
    onSuccess: PropTypes.func,
    onError: PropTypes.func,
};

export default SignupForm;
