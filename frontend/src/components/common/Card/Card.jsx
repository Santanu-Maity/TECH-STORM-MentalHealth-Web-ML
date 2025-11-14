import PropTypes from 'prop-types';
import './Card.css';

const Card = ({
    children,
    title,
    header,
    footer,
    variant = 'default',
    className = '',
    onClick,
    ...props
}) => {
    const cardClasses = [
        'card-custom',
        `card-${variant}`,
        onClick && 'card-clickable',
        className,
    ]
        .filter(Boolean)
        .join(' ');

    return (
        <div
            className={cardClasses}
            onClick={onClick}
            role={onClick ? 'button' : undefined}
            tabIndex={onClick ? 0 : undefined}
            onKeyPress={onClick ? (e) => e.key === 'Enter' && onClick(e) : undefined}
            {...props}
        >
            {(header || title) && (
                <div className="card-header">
                    {title && <h3 className="card-title">{title}</h3>}
                    {header}
                </div>
            )}
            <div className="card-body">{children}</div>
            {footer && <div className="card-footer">{footer}</div>}
        </div>
    );
};

Card.propTypes = {
    children: PropTypes.node.isRequired,
    title: PropTypes.string,
    header: PropTypes.node,
    footer: PropTypes.node,
    variant: PropTypes.oneOf(['default', 'elevated', 'outlined', 'flat']),
    className: PropTypes.string,
    onClick: PropTypes.func,
};

export default Card;
