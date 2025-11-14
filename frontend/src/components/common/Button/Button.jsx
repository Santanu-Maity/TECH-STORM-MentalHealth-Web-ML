import PropTypes from 'prop-types';
import './Button.css';

const Button = ({
    children,
    variant = 'primary',
    size = 'medium',
    disabled = false,
    loading = false,
    type = 'button',
    onClick,
    className = '',
    ariaLabel,
    ...props
}) => {
    const buttonClasses = [
        'btn-custom',
        `btn-${variant}`,
        `btn-${size}`,
        loading && 'btn-loading',
        disabled && 'btn-disabled',
        className,
    ]
        .filter(Boolean)
        .join(' ');

    return (
        <button
            type={type}
            className={buttonClasses}
            onClick={onClick}
            disabled={disabled || loading}
            aria-label={ariaLabel || (typeof children === 'string' ? children : undefined)}
            aria-busy={loading}
            {...props}
        >
            {loading && (
                <span className="btn-spinner" aria-hidden="true">
                    <span className="spinner-border spinner-border-sm" role="status"></span>
                </span>
            )}
            <span className={loading ? 'btn-content-loading' : 'btn-content'}>
                {children}
            </span>
        </button>
    );
};

Button.propTypes = {
    children: PropTypes.node.isRequired,
    variant: PropTypes.oneOf(['primary', 'secondary', 'danger', 'success', 'outline']),
    size: PropTypes.oneOf(['small', 'medium', 'large']),
    disabled: PropTypes.bool,
    loading: PropTypes.bool,
    type: PropTypes.oneOf(['button', 'submit', 'reset']),
    onClick: PropTypes.func,
    className: PropTypes.string,
    ariaLabel: PropTypes.string,
};

export default Button;
