import { useAuth } from '../hooks/useAuth';
import SignupForm from '../components/auth/SignupForm';

const Signup = () => {
    const { signup } = useAuth();

    const handleSuccess = (userData, token) => {
        signup(userData, token);
    };

    const handleError = (error) => {
        console.error('Signup error:', error);
    };

    return <SignupForm onSuccess={handleSuccess} onError={handleError} />;
};

export default Signup;
