import { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import './Modal.css';

const Modal = ({
    isOpen,
    onClose,
    title,
    children,
    size = 'medium',
    closeOnBackdrop = true,
    closeOnEsc = true,
    showCloseButton = true,
}) => {
    const modalRef = useRef(null);
    const previousFocusRef = useRef(null);

    useEffect(() => {
        if (isOpen) {
            // Store the currently focused element
            previousFocusRef.current = document.activeElement;

            // Focus the modal
            modalRef.current?.focus();

            // Prevent body scroll
            document.body.style.overflow = 'hidden';

            // Handle ESC key
            const handleEsc = (e) => {
                if (closeOnEsc && e.key === 'Escape') {
                    onClose();
                }
            };

            document.addEventListener('keydown', handleEsc);

            return () => {
                document.removeEventListener('keydown', handleEsc);
                document.body.style.overflow = 'unset';

                // Restore focus to the previously focused element
                previousFocusRef.current?.focus();
            };
        }
    }, [isOpen, onClose, closeOnEsc]);

    // Focus trap
    useEffect(() => {
        if (!isOpen) return;

        const modal = modalRef.current;
        if (!modal) return;

        const focusableElements = modal.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        const handleTab = (e) => {
            if (e.key !== 'Tab') return;

            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement?.focus();
                }
            } else {
                if (document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement?.focus();
                }
            }
        };

        modal.addEventListener('keydown', handleTab);

        return () => {
            modal.removeEventListener('keydown', handleTab);
        };
    }, [isOpen]);

    if (!isOpen) return null;

    const handleBackdropClick = (e) => {
        if (closeOnBackdrop && e.target === e.currentTarget) {
            onClose();
        }
    };

    return (
        <div
            className="modal-overlay"
            onClick={handleBackdropClick}
            role="dialog"
            aria-modal="true"
            aria-labelledby={title ? 'modal-title' : undefined}
        >
            <div
                ref={modalRef}
                className={`modal-content modal-${size}`}
                tabIndex={-1}
            >
                {(title || showCloseButton) && (
                    <div className="modal-header">
                        {title && <h2 id="modal-title" className="modal-title">{title}</h2>}
                        {showCloseButton && (
                            <button
                                type="button"
                                className="modal-close"
                                onClick={onClose}
                                aria-label="Close modal"
                            >
                                <span aria-hidden="true">&times;</span>
                            </button>
                        )}
                    </div>
                )}
                <div className="modal-body">{children}</div>
            </div>
        </div>
    );
};

Modal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    title: PropTypes.string,
    children: PropTypes.node.isRequired,
    size: PropTypes.oneOf(['small', 'medium', 'large', 'fullscreen']),
    closeOnBackdrop: PropTypes.bool,
    closeOnEsc: PropTypes.bool,
    showCloseButton: PropTypes.bool,
};

export default Modal;
