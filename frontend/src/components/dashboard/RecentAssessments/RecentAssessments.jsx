import PropTypes from 'prop-types';
import Card from '../../common/Card';
import { MENTAL_STATE_COLORS, MENTAL_STATE_LABELS } from '../../../utils/constants';
import { formatTimeAgo } from '../../../utils/formatters';
import './RecentAssessments.css';

const RecentAssessments = ({ assessments, onViewDetails }) => {
    if (!assessments || assessments.length === 0) {
        return (
            <Card title="Recent Assessments" variant="elevated">
                <div className="no-assessments">
                    <p>No assessments yet. Take your first assessment to get started!</p>
                </div>
            </Card>
        );
    }

    return (
        <Card title="Recent Assessments" variant="elevated">
            <div className="assessments-list">
                {assessments.map((assessment) => (
                    <div
                        key={assessment.id}
                        className="assessment-item"
                        onClick={() => onViewDetails && onViewDetails(assessment)}
                        role="button"
                        tabIndex={0}
                        onKeyPress={(e) => e.key === 'Enter' && onViewDetails && onViewDetails(assessment)}
                    >
                        <div className="assessment-header">
                            <span
                                className="assessment-state"
                                style={{ color: MENTAL_STATE_COLORS[assessment.result?.mentalState] }}
                            >
                                {MENTAL_STATE_LABELS[assessment.result?.mentalState] || 'Unknown'}
                            </span>
                            <span className="assessment-time">{formatTimeAgo(assessment.timestamp)}</span>
                        </div>

                        <div className="assessment-score">
                            <span className="score-label">Score:</span>
                            <span className="score-number">{assessment.result?.score || 'N/A'}</span>
                        </div>

                        <div className="assessment-metrics">
                            <div className="metric">
                                <span className="metric-label">Sleep:</span>
                                <span className="metric-value">{assessment.inputs?.sleepHours}h</span>
                            </div>
                            <div className="metric">
                                <span className="metric-label">Stress:</span>
                                <span className="metric-value">{assessment.inputs?.workStress}/10</span>
                            </div>
                            <div className="metric">
                                <span className="metric-label">Exercise:</span>
                                <span className="metric-value">{assessment.inputs?.exerciseHours}h</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </Card>
    );
};

RecentAssessments.propTypes = {
    assessments: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.string.isRequired,
            timestamp: PropTypes.string.isRequired,
            inputs: PropTypes.object,
            result: PropTypes.shape({
                mentalState: PropTypes.string,
                score: PropTypes.number,
            }),
        })
    ),
    onViewDetails: PropTypes.func,
};

export default RecentAssessments;
