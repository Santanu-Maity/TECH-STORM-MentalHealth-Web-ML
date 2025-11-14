import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import Input from '../../common/Input';
import Button from '../../common/Button';
import Card from '../../common/Card';
import { validateForm } from '../../../utils/validators';
import './LoginForm.css';

const LoginForm = ({ onSuccess, onError }) => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
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
            email: { required: true, email: true },
            password: { required: true },
        });

        if (!validation.isValid) {
            setErrors(validation.errors);
            return;
        }

        setLoading(true);
        setErrors({});

        try {
            // Call backend API
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Login failed');
            }

            // Successful login
            if (onSuccess) {
                onSuccess(data.user, data.token);
            }

            navigate('/dashboard');
        } catch (error) {
            const errorMessage = error.message || 'Login failed. Please try again.';
            setErrors({ submit: errorMessage });

            if (onError) {
                onError(error);
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-form-container">
            <Card className="login-card">
                <div className="login-header">
                    <h1 className="login-title">Welcome Back</h1>
                    <p className="login-subtitle">Sign in to continue your mental wellness journey</p>
                </div>

                <form onSubmit={handleSubmit} className="login-form" noValidate>
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

                    <Input
                        type="password"
                        name="password"
                        label="Password"
                        value={formData.password}
                        onChange={handleChange}
                        error={errors.password}
                        placeholder="Enter your password"
                        required
                        autoComplete="current-password"
                    />

                    {errors.submit && (
                        <div className="login-error" role="alert">
                            {errors.submit}
                        </div>
                    )}

                    <Button
                        type="submit"
                        variant="primary"
                        size="large"
                        loading={loading}
                        className="login-button"
                    >
                        Sign In
                    </Button>
                </form>

                <div className="login-footer">
                    <p className="login-footer-text">
                        Don't have an account?{' '}
                        <Link to="/signup" className="login-link">
                            Sign up
                        </Link>
                    </p>
                </div>
            </Card>
        </div>
    );
};

LoginForm.propTypes = {
    onSuccess: PropTypes.func,
    onError: PropTypes.func,
};

export default LoginForm;
