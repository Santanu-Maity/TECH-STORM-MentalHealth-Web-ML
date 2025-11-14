import { useState } from 'react';
import PropTypes from 'prop-types';
import { FaExclamationTriangle, FaPhone, FaComments } from 'react-icons/fa';
import Modal from '../Modal';
import Button from '../Button';
import { EMERGENCY_CONTACTS } from '../../../utils/constants';
import './EmergencyButton.css';

const EmergencyButton = ({ variant = 'floating' }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => {
        setIsModalOpen(true);
        // Log emergency event for follow-up
        console.log('Emergency help accessed at:', new Date().toISOString());
    };

    const closeModal = () => {
        setIsModalOpen(false);
    };

    const handleCall = (number) => {
        window.location.href = `tel:${number}`;
    };

    return (
        <>
            <button
                className={`emergency-button emergency-${variant}`}
                onClick={openModal}
                aria-label="Emergency help - Get immediate support"
                title="Emergency Help"
            >
                <FaExclamationTriangle />
                {variant === 'inline' && <span>Emergency Help</span>}
            </button>

            <Modal
                isOpen={isModalOpen}
                onClose={closeModal}
                size="medium"
                closeOnBackdrop={false}
            >
                <div className="emergency-modal-content">
                    <div className="emergency-modal-icon">
                        <FaExclamationTriangle />
                    </div>

                    <h2 className="emergency-modal-title">Emergency Support</h2>

                    <p className="emergency-modal-description">
                        If you're in crisis or need immediate help, please reach out to one of these resources.
                        You're not alone, and help is available 24/7.
                    </p>

                    <div className="emergency-contacts">
                        <div className="emergency-contact-card">
                            <div className="emergency-contact-title">
                                <FaPhone />
                                <span>National Suicide Prevention Lifeline</span>
                            </div>
                            <div className="emergency-contact-number">
                                {EMERGENCY_CONTACTS.CRISIS_HOTLINE}
                            </div>
                            <p className="emergency-contact-description">
                                Free, confidential support 24/7 for people in distress
                            </p>
                        </div>

                        <div className="emergency-contact-card">
                            <div className="emergency-contact-title">
                                <FaComments />
                                <span>Crisis Text Line</span>
                            </div>
                            <div className="emergency-contact-number">
                                {EMERGENCY_CONTACTS.CRISIS_TEXT}
                            </div>
                            <p className="emergency-contact-description">
                                Text support available 24/7 - free and confidential
                            </p>
                        </div>

                        <div className="emergency-contact-card">
                            <div className="emergency-contact-title">
                                <FaPhone />
                                <span>Emergency Services</span>
                            </div>
                            <div className="emergency-contact-number">
                                {EMERGENCY_CONTACTS.EMERGENCY}
                            </div>
                            <p className="emergency-contact-description">
                                For immediate life-threatening emergencies
                            </p>
                        </div>
                    </div>

                    <div className="emergency-actions">
                        <Button
                            variant="danger"
                            size="large"
                            onClick={() => handleCall(EMERGENCY_CONTACTS.CRISIS_HOTLINE)}
                        >
                            <FaPhone /> Call Crisis Hotline Now
                        </Button>
                        <Button
                            variant="outline"
                            size="medium"
                            onClick={closeModal}
                        >
                            Close
                        </Button>
                    </div>

                    <div className="emergency-disclaimer">
                        <p className="emergency-disclaimer-text">
                            <strong>Important:</strong> This application is not a substitute for professional
                            medical advice, diagnosis, or treatment. If you're experiencing a medical emergency,
                            please call {EMERGENCY_CONTACTS.EMERGENCY} immediately.
                        </p>
                    </div>
                </div>
            </Modal>
        </>
    );
};

EmergencyButton.propTypes = {
    variant: PropTypes.oneOf(['floating', 'inline']),
};

export default EmergencyButton;
