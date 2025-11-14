import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import ScoreCard from '../components/dashboard/ScoreCard';
import RecentAssessments from '../components/dashboard/RecentAssessments';
import Button from '../components/common/Button';
import assessmentService from '../services/assessmentService';
import './Dashboard.css';

const Dashboard = () => {
    const { user } = useAuth();
    const [loading, setLoading] = useState(true);
    const [assessments, setAssessments] = useState([]);
    const [currentScore, setCurrentScore] = useState(null);
    const [currentState, setCurrentState] = useState(null);
    const [trend, setTrend] = useState('stable');

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        try {
            setLoading(true);
            // Fetch assessments from backend
            const data = await assessmentService.getAssessments();

            if (data && data.length > 0) {
                setAssessments(data.slice(0, 5)); // Get last 5 assessments

                // Set current score and state from most recent assessment
                const latest = data[0];
                setCurrentScore(latest.result?.score);
                setCurrentState(latest.result?.mentalState);

                // Calculate trend
                if (data.length >= 2) {
                    const previous = data[1];
                    if (latest.result?.score > previous.result?.score) {
                        setTrend('improving');
                    } else if (latest.result?.score < previous.result?.score) {
                        setTrend('declining');
                    } else {
                        setTrend('stable');
                    }
                }
            }
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
            // Use mock data if API fails
            setAssessments([]);
        } finally {
            setLoading(false);
        }
    };

    const handleViewDetails = (assessment) => {
        console.log('View assessment details:', assessment);
        // TODO: Navigate to assessment details page or show modal
    };

    if (loading) {
        return (
            <div className="dashboard-loading">
                <div className="spinner"></div>
                <p>Loading your dashboard...</p>
            </div>
        );
    }

    return (
        <div className="dashboard-container">
            <div className="dashboard-header">
                <div>
                    <h1 className="dashboard-title">Welcome back, {user?.name || 'User'}!</h1>
                    <p className="dashboard-subtitle">Here's your mental wellness overview</p>
                </div>
                <Link to="/assessment">
                    <Button variant="primary" size="large">
                        Take Assessment
                    </Button>
                </Link>
            </div>

            <div className="dashboard-content">
                {currentScore !== null ? (
                    <>
                        <div className="dashboard-score-section">
                            <ScoreCard
                                score={currentScore}
                                mentalState={currentState}
                                trend={trend}
                                lastAssessmentDate={assessments[0]?.timestamp}
                            />
                        </div>

                        <div className="dashboard-assessments-section">
                            <RecentAssessments
                                assessments={assessments}
                                onViewDetails={handleViewDetails}
                            />
                        </div>

                        <div className="dashboard-actions">
                            <Link to="/resources">
                                <Button variant="outline" size="medium">
                                    View Resources
                                </Button>
                            </Link>
                            <Link to="/appointments">
                                <Button variant="outline" size="medium">
                                    Book Appointment
                                </Button>
                            </Link>
                        </div>
                    </>
                ) : (
                    <div className="dashboard-empty">
                        <div className="empty-state">
                            <h2>Start Your Mental Wellness Journey</h2>
                            <p>
                                Take your first assessment to get personalized insights and recommendations
                                for your mental health.
                            </p>
                            <Link to="/assessment">
                                <Button variant="primary" size="large">
                                    Take Your First Assessment
                                </Button>
                            </Link>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
