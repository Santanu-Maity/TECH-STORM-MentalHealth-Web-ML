import PropTypes from 'prop-types';
import './Input.css';

const Input = ({
    type = 'text',
    label,
    name,
    value,
    onChange,
    onBlur,
    placeholder,
    error,
    disabled = false,
    required = false,
    className = '',
    rows = 4,
    ...props
}) => {
    const inputId = name || `input-${Math.random().toString(36).substr(2, 9)}`;
    const hasError = Boolean(error);

    const inputClasses = [
        'input-field',
        hasError && 'input-error',
        disabled && 'input-disabled',
        className,
    ]
        .filter(Boolean)
        .join(' ');

    const renderInput = () => {
        if (type === 'textarea') {
            return (
                <textarea
                    id={inputId}
                    name={name}
                    value={value}
                    onChange={onChange}
                    onBlur={onBlur}
                    placeholder={placeholder}
                    disabled={disabled}
                    required={required}
                    rows={rows}
                    className={inputClasses}
                    aria-invalid={hasError}
                    aria-describedby={hasError ? `${inputId}-error` : undefined}
                    {...props}
                />
            );
        }

        return (
            <input
                type={type}
                id={inputId}
                name={name}
                value={value}
                onChange={onChange}
                onBlur={onBlur}
                placeholder={placeholder}
                disabled={disabled}
                required={required}
                className={inputClasses}
                aria-invalid={hasError}
                aria-describedby={hasError ? `${inputId}-error` : undefined}
                {...props}
            />
        );
    };

    return (
        <div className="input-wrapper">
            {label && (
                <label htmlFor={inputId} className="input-label">
                    {label}
                    {required && <span className="input-required" aria-label="required">*</span>}
                </label>
            )}
            {renderInput()}
            {error && (
                <span id={`${inputId}-error`} className="input-error-message" role="alert">
                    {error}
                </span>
            )}
        </div>
    );
};

Input.propTypes = {
    type: PropTypes.oneOf(['text', 'email', 'password', 'number', 'tel', 'url', 'textarea']),
    label: PropTypes.string,
    name: PropTypes.string,
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    onChange: PropTypes.func,
    onBlur: PropTypes.func,
    placeholder: PropTypes.string,
    error: PropTypes.string,
    disabled: PropTypes.bool,
    required: PropTypes.bool,
    className: PropTypes.string,
    rows: PropTypes.number,
};

export default Input;
