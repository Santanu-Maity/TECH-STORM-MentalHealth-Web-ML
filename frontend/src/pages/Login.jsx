import { useAuth } from '../hooks/useAuth';
import LoginForm from '../components/auth/LoginForm';

const Login = () => {
    const { login } = useAuth();

    const handleSuccess = (userData, token) => {
        login(userData, token);
    };

    const handleError = (error) => {
        console.error('Login error:', error);
    };

    return <LoginForm onSuccess={handleSuccess} onError={handleError} />;
};

export default Login;
