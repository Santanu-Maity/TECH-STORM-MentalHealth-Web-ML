import PropTypes from 'prop-types';
import { FaArrowUp, FaArrowDown, FaMinus } from 'react-icons/fa';
import Card from '../../common/Card';
import { MENTAL_STATE_COLORS, MENTAL_STATE_LABELS } from '../../../utils/constants';
import { formatDate } from '../../../utils/formatters';
import './ScoreCard.css';

const ScoreCard = ({ score, mentalState, trend, lastAssessmentDate }) => {
    const getTrendIcon = () => {
        if (trend === 'improving') return <FaArrowUp className="trend-icon trend-up" />;
        if (trend === 'declining') return <FaArrowDown className="trend-icon trend-down" />;
        return <FaMinus className="trend-icon trend-stable" />;
    };

    const getTrendText = () => {
        if (trend === 'improving') return 'Improving';
        if (trend === 'declining') return 'Needs Attention';
        return 'Stable';
    };

    const getScoreColor = () => {
        if (score >= 70) return 'var(--color-success)';
        if (score >= 40) return 'var(--color-warning)';
        return 'var(--color-danger)';
    };

    return (
        <Card className="score-card" variant="elevated">
            <div className="score-card-content">
                <div className="score-main">
                    <div className="score-circle" style={{ borderColor: getScoreColor() }}>
                        <span className="score-value" style={{ color: getScoreColor() }}>
                            {score || 'N/A'}
                        </span>
                        <span className="score-label">Score</span>
                    </div>
                </div>

                <div className="score-details">
                    <div className="mental-state">
                        <span className="mental-state-label">Current State</span>
                        <span
                            className="mental-state-value"
                            style={{ color: MENTAL_STATE_COLORS[mentalState] }}
                        >
                            {MENTAL_STATE_LABELS[mentalState] || 'Unknown'}
                        </span>
                    </div>

                    <div className="score-trend">
                        <span className="trend-label">Trend</span>
                        <div className="trend-value">
                            {getTrendIcon()}
                            <span>{getTrendText()}</span>
                        </div>
                    </div>

                    {lastAssessmentDate && (
                        <div className="last-assessment">
                            <span className="last-assessment-label">Last Assessment</span>
                            <span className="last-assessment-date">
                                {formatDate(lastAssessmentDate, 'datetime')}
                            </span>
                        </div>
                    )}
                </div>
            </div>
        </Card>
    );
};

ScoreCard.propTypes = {
    score: PropTypes.number,
    mentalState: PropTypes.string,
    trend: PropTypes.oneOf(['improving', 'stable', 'declining']),
    lastAssessmentDate: PropTypes.string,
};

export default ScoreCard;
