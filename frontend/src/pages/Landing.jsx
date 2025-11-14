import { Link } from 'react-router-dom';
import Button from '../components/common/Button';

const Landing = () => {
    return (
        <div className="container" style={{ paddingTop: '4rem', paddingBottom: '4rem' }}>
            <div style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
                <h1 style={{ fontSize: '3rem', marginBottom: '1.5rem', color: 'var(--color-primary-blue)' }}>
                    Welcome to Mental Health Tracker
                </h1>
                <p style={{ fontSize: '1.25rem', marginBottom: '2rem', color: 'var(--color-text-secondary)' }}>
                    Track your mental wellness, get AI-powered insights, and access personalized resources
                    to support your mental health journey.
                </p>
                <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
                    <Link to="/signup">
                        <Button variant="primary" size="large">
                            Get Started
                        </Button>
                    </Link>
                    <Link to="/login">
                        <Button variant="outline" size="large">
                            Login
                        </Button>
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default Landing;
