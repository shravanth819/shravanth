"""
Authentication Routes Module
Handles signup, login, logout, and user profile management
"""

from flask import request, jsonify, Blueprint
from datetime import datetime
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Create Blueprint for auth routes
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def setup_auth_routes(app, auth, user_db, login_required, admin_required):
    """
    Setup authentication routes
    
    Args:
        app: Flask application instance
        auth: UserAuthenticator instance
        user_db: UserDatabase instance
        login_required: Decorator for protected routes
        admin_required: Decorator for admin routes
    """
    
    # ========================================================================
    # SIGNUP ENDPOINT
    # ========================================================================
    
    @auth_bp.route('/signup', methods=['POST'])
    def signup():
        """
        Register new user
        
        Expected JSON:
        {
            "username": "farmer_john",
            "email": "john@example.com",
            "password": "SecurePass123!",
            "role": "farmer",  # farmer, researcher, officer
            "location": "Bangalore, Karnataka",
            "crop_type": "Rice"
        }
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['username', 'email', 'password']
            missing = [f for f in required_fields if f not in data]
            
            if missing:
                return jsonify({
                    'error': 'Missing required fields',
                    'missing': missing
                }), 400
            
            username = data.get('username').strip()
            email = data.get('email').strip()
            password = data.get('password')
            role = data.get('role', 'farmer')
            location = data.get('location', '')
            crop_type = data.get('crop_type', '')
            
            # Validate username format
            is_valid, msg = auth.validate_username(username)
            if not is_valid:
                return jsonify({
                    'error': 'Invalid username',
                    'details': msg
                }), 400
            
            # Validate email format
            if not auth.validate_email(email):
                return jsonify({
                    'error': 'Invalid email format'
                }), 400
            
            # Validate password strength
            is_valid, msg = auth.validate_password(password)
            if not is_valid:
                return jsonify({
                    'error': 'Password is not strong enough',
                    'requirements': msg
                }), 400
            
            # Validate role
            valid_roles = ['farmer', 'researcher', 'officer', 'admin']
            if role not in valid_roles:
                return jsonify({
                    'error': 'Invalid role',
                    'valid_roles': valid_roles
                }), 400
            
            # Hash password
            password_hash = auth.hash_password(password)
            
            # Create user
            try:
                user = user_db.create_user(
                    username=username,
                    email=email,
                    password_hash=password_hash,
                    role=role,
                    location=location,
                    crop_type=crop_type
                )
            except ValueError as e:
                return jsonify({
                    'error': str(e)
                }), 409  # Conflict - user already exists
            
            # Generate token
            token = auth.generate_token(user['user_id'], user['username'], user['role'])
            
            logger.info(f"New user registered: {username} ({role})")
            
            return jsonify({
                'message': 'User registered successfully',
                'user': {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role'],
                    'location': user['location'],
                    'crop_type': user['crop_type']
                },
                'token': token
            }), 201
        
        except Exception as e:
            logger.error(f"Signup error: {str(e)}")
            return jsonify({
                'error': 'Signup failed',
                'details': str(e)
            }), 500
    
    # ========================================================================
    # LOGIN ENDPOINT
    # ========================================================================
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        """
        Login user
        
        Expected JSON:
        {
            "username": "farmer_john",
            "password": "SecurePass123!"
        }
        
        OR
        
        {
            "email": "john@example.com",
            "password": "SecurePass123!"
        }
        """
        try:
            data = request.get_json()
            
            # Get username or email
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            if not password:
                return jsonify({'error': 'Password is required'}), 400
            
            if not username and not email:
                return jsonify({'error': 'Username or email is required'}), 400
            
            # Get user
            user = None
            if username:
                user = user_db.get_user_by_username(username)
            elif email:
                user = user_db.get_user_by_email(email)
            
            if not user:
                return jsonify({
                    'error': 'Invalid username/email or password'
                }), 401
            
            # Verify password
            if not auth.verify_password(password, user['password_hash']):
                return jsonify({
                    'error': 'Invalid username/email or password'
                }), 401
            
            # Check if user is active
            if not user.get('is_active', True):
                return jsonify({
                    'error': 'Account is deactivated'
                }), 403
            
            # Update last login
            user_db.update_last_login(user['user_id'])
            
            # Generate token
            token = auth.generate_token(user['user_id'], user['username'], user['role'])
            
            logger.info(f"User logged in: {user['username']}")
            
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role'],
                    'location': user['location'],
                    'crop_type': user['crop_type']
                },
                'token': token
            }), 200
        
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return jsonify({
                'error': 'Login failed',
                'details': str(e)
            }), 500
    
    # ========================================================================
    # GET CURRENT USER PROFILE
    # ========================================================================
    
    @auth_bp.route('/profile', methods=['GET'])
    @login_required
    def get_profile():
        """Get current user's profile"""
        try:
            user_id = request.user['user_id']
            user = user_db.get_user_by_id(user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Remove sensitive data
            user_copy = user.copy()
            user_copy.pop('password_hash', None)
            
            return jsonify({
                'user': user_copy
            }), 200
        
        except Exception as e:
            logger.error(f"Get profile error: {str(e)}")
            return jsonify({
                'error': 'Failed to get profile',
                'details': str(e)
            }), 500
    
    # ========================================================================
    # UPDATE USER PROFILE
    # ========================================================================
    
    @auth_bp.route('/profile', methods=['PUT'])
    @login_required
    def update_profile():
        """
        Update user profile
        
        Expected JSON (all fields optional):
        {
            "location": "New Delhi",
            "crop_type": "Wheat",
            "preferences": {
                "theme": "light",
                "language": "hi",
                "notifications_email": true
            }
        }
        """
        try:
            user_id = request.user['user_id']
            data = request.get_json()
            
            # Update allowed fields
            allowed_fields = ['location', 'crop_type', 'preferences']
            update_data = {k: v for k, v in data.items() if k in allowed_fields}
            
            if not update_data:
                return jsonify({'error': 'No valid fields to update'}), 400
            
            # Update user
            user_db.update_user(user_id, **update_data)
            user = user_db.get_user_by_id(user_id)
            
            # Remove sensitive data
            user_copy = user.copy()
            user_copy.pop('password_hash', None)
            
            logger.info(f"User profile updated: {user['username']}")
            
            return jsonify({
                'message': 'Profile updated successfully',
                'user': user_copy
            }), 200
        
        except Exception as e:
            logger.error(f"Update profile error: {str(e)}")
            return jsonify({
                'error': 'Failed to update profile',
                'details': str(e)
            }), 500
    
    # ========================================================================
    # CHANGE PASSWORD
    # ========================================================================
    
    @auth_bp.route('/change-password', methods=['POST'])
    @login_required
    def change_password():
        """
        Change user password
        
        Expected JSON:
        {
            "old_password": "CurrentPassword123!",
            "new_password": "NewPassword456!"
        }
        """
        try:
            user_id = request.user['user_id']
            data = request.get_json()
            
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            
            if not old_password or not new_password:
                return jsonify({
                    'error': 'Both old and new passwords are required'
                }), 400
            
            user = user_db.get_user_by_id(user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Verify old password
            if not auth.verify_password(old_password, user['password_hash']):
                return jsonify({
                    'error': 'Current password is incorrect'
                }), 401
            
            # Validate new password
            is_valid, msg = auth.validate_password(new_password)
            if not is_valid:
                return jsonify({
                    'error': 'New password is not strong enough',
                    'requirements': msg
                }), 400
            
            # Hash new password
            new_password_hash = auth.hash_password(new_password)
            
            # Update password
            user_db.update_user(user_id, password_hash=new_password_hash)
            
            logger.info(f"Password changed for user: {user['username']}")
            
            return jsonify({
                'message': 'Password changed successfully'
            }), 200
        
        except Exception as e:
            logger.error(f"Change password error: {str(e)}")
            return jsonify({
                'error': 'Failed to change password',
                'details': str(e)
            }), 500
    
    # ========================================================================
    # LOGOUT (client-side token deletion)
    # ========================================================================
    
    @auth_bp.route('/logout', methods=['POST'])
    @login_required
    def logout():
        """
        Logout user (client-side token deletion)
        Note: Token is deleted on client side. This endpoint just confirms logout.
        """
        try:
            username = request.user.get('username', 'Unknown')
            logger.info(f"User logged out: {username}")
            
            return jsonify({
                'message': 'Logged out successfully'
            }), 200
        
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return jsonify({
                'error': 'Logout failed'
            }), 500
    
    # ========================================================================
    # ADMIN: GET ALL USERS
    # ========================================================================
    
    @auth_bp.route('/admin/users', methods=['GET'])
    @admin_required
    def get_all_users():
        """Get all users (admin only)"""
        try:
            users = user_db.get_all_users()
            
            # Remove sensitive data
            sanitized_users = [
                {k: v for k, v in u.items() if k != 'password_hash'}
                for u in users
            ]
            
            return jsonify({
                'total_users': len(sanitized_users),
                'users': sanitized_users
            }), 200
        
        except Exception as e:
            logger.error(f"Get users error: {str(e)}")
            return jsonify({
                'error': 'Failed to get users'
            }), 500
    
    # ========================================================================
    # ADMIN: GET USERS BY ROLE
    # ========================================================================
    
    @auth_bp.route('/admin/users/role/<role>', methods=['GET'])
    @admin_required
    def get_users_by_role(role):
        """Get users by role (admin only)"""
        try:
            valid_roles = ['farmer', 'researcher', 'officer', 'admin']
            
            if role not in valid_roles:
                return jsonify({
                    'error': 'Invalid role',
                    'valid_roles': valid_roles
                }), 400
            
            users = user_db.get_users_by_role(role)
            
            # Remove sensitive data
            sanitized_users = [
                {k: v for k, v in u.items() if k != 'password_hash'}
                for u in users
            ]
            
            return jsonify({
                'role': role,
                'count': len(sanitized_users),
                'users': sanitized_users
            }), 200
        
        except Exception as e:
            logger.error(f"Get users by role error: {str(e)}")
            return jsonify({
                'error': 'Failed to get users'
            }), 500
    
    # Register blueprint with app
    app.register_blueprint(auth_bp)
    
    logger.info("Authentication routes registered successfully")
