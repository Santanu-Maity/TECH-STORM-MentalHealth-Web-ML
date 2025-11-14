import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import PropTypes from 'prop-types';
import { FaBars, FaTimes, FaUser, FaSignOutAlt } from 'react-icons/fa';
import './Navbar.css';

const Navbar = ({ user, isAuthenticated, onLogout }) => {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const location = useLocation();

    const toggleMobileMenu = () => {
        setIsMobileMenuOpen(!isMobileMenuOpen);
    };

    const closeMobileMenu = () => {
        setIsMobileMenuOpen(false);
    };

    const isActive = (path) => {
        return location.pathname === path ? 'nav-link-active' : '';
    };

    return (
        <nav className="navbar-custom" role="navigation" aria-label="Main navigation">
            <div className="navbar-container">
                <Link to="/" className="navbar-logo" onClick={closeMobileMenu}>
                    <span className="logo-text">Mental Health Tracker</span>
                </Link>

                <button
                    className="navbar-toggle"
                    onClick={toggleMobileMenu}
                    aria-label="Toggle navigation menu"
                    aria-expanded={isMobileMenuOpen}
                >
                    {isMobileMenuOpen ? <FaTimes /> : <FaBars />}
                </button>

                <div className={`navbar-menu ${isMobileMenuOpen ? 'navbar-menu-open' : ''}`}>
                    {isAuthenticated ? (
                        <>
                            <Link
                                to="/dashboard"
                                className={`navbar-link ${isActive('/dashboard')}`}
                                onClick={closeMobileMenu}
                            >
                                Dashboard
                            </Link>
                            <Link
                                to="/assessment"
                                className={`navbar-link ${isActive('/assessment')}`}
                                onClick={closeMobileMenu}
                            >
                                Assessment
                            </Link>
                            <Link
                                to="/resources"
                                className={`navbar-link ${isActive('/resources')}`}
                                onClick={closeMobileMenu}
                            >
                                Resources
                            </Link>
                            <Link
                                to="/appointments"
                                className={`navbar-link ${isActive('/appointments')}`}
                                onClick={closeMobileMenu}
                            >
                                Appointments
                            </Link>

                            <div className="navbar-divider" />

                            <div className="navbar-user">
                                <Link
                                    to="/profile"
                                    className={`navbar-link navbar-user-link ${isActive('/profile')}`}
                                    onClick={closeMobileMenu}
                                >
                                    <FaUser />
                                    <span>{user?.name || 'Profile'}</span>
                                </Link>
                                <button
                                    className="navbar-link navbar-logout"
                                    onClick={() => {
                                        onLogout();
                                        closeMobileMenu();
                                    }}
                                    aria-label="Logout"
                                >
                                    <FaSignOutAlt />
                                    <span>Logout</span>
                                </button>
                            </div>
                        </>
                    ) : (
                        <>
                            <Link
                                to="/login"
                                className={`navbar-link ${isActive('/login')}`}
                                onClick={closeMobileMenu}
                            >
                                Login
                            </Link>
                            <Link
                                to="/signup"
                                className={`navbar-link navbar-link-primary ${isActive('/signup')}`}
                                onClick={closeMobileMenu}
                            >
                                Sign Up
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

Navbar.propTypes = {
    user: PropTypes.shape({
        name: PropTypes.string,
        email: PropTypes.string,
    }),
    isAuthenticated: PropTypes.bool.isRequired,
    onLogout: PropTypes.func.isRequired,
};

export default Navbar;
