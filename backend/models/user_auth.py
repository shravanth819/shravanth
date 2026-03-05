"""
User Authentication Module
Handles user registration, login, password encryption, and session management
"""

from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import os
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional

class UserAuthenticator:
    """Handles user authentication and password security"""
    
    def __init__(self, secret_key: str = None):
        """Initialize authenticator with secret key for JWT"""
        self.secret_key = secret_key or os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
        self.token_expiry_hours = 24
    
    # ========================================================================
    # PASSWORD MANAGEMENT
    # ========================================================================
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using werkzeug security
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password safe for storage
        """
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        return generate_password_hash(password, method='pbkdf2:sha256')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verify a password against its hash
        
        Args:
            password: Plain text password to verify
            hashed: Hashed password from database
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return check_password_hash(hashed, password)
        except:
            return False
    
    # ========================================================================
    # TOKEN MANAGEMENT (JWT)
    # ========================================================================
    
    def generate_token(self, user_id: str, username: str, role: str = 'user') -> str:
        """
        Generate JWT token for authenticated user
        
        Args:
            user_id: Unique user identifier
            username: Username
            role: User role (farmer, researcher, officer, admin)
            
        Returns:
            JWT token string
        """
        payload = {
            'user_id': user_id,
            'username': username,
            'role': role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=self.token_expiry_hours)
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token to verify
            
        Returns:
            Decoded token data if valid, None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token expired
        except jwt.InvalidTokenError:
            return None  # Invalid token
    
    # ========================================================================
    # USER VALIDATION
    # ========================================================================
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate password strength
        
        Requirements:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        """
        issues = []
        
        if len(password) < 8:
            issues.append("Password must be at least 8 characters")
        
        if not any(c.isupper() for c in password):
            issues.append("Password must contain uppercase letter")
        
        if not any(c.islower() for c in password):
            issues.append("Password must contain lowercase letter")
        
        if not any(c.isdigit() for c in password):
            issues.append("Password must contain digit")
        
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            issues.append("Password must contain special character")
        
        if issues:
            return False, "; ".join(issues)
        
        return True, "Password is strong"
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """Validate username format"""
        import re
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(username) > 20:
            return False, "Username must not exceed 20 characters"
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return False, "Username can only contain letters, numbers, underscore, hyphen"
        
        return True, "Username is valid"



class UserDatabase:
    """SQLAlchemy persistent database wrapper for auth routes"""

    def _to_dict(self, user):
        return {
            'user_id': str(user.id),
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash,
            'role': user.role,
            'location': user.location,
            'crop_type': user.default_crop_type,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'is_active': user.is_active,
            'preferences': {
                'language': user.preferred_language,
                'notifications_email': user.email_notifications,
                'theme': user.theme_preference
            }
        }

    def create_user(self, username: str, email: str, password_hash: str, 
                   role: str = 'farmer', location: str = '', crop_type: str = '') -> Dict:
        from database.models import User
        from database.db import db
        if User.query.filter_by(username=username).first():
            raise ValueError("Username already exists")
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already registered")
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
            location=location,
            default_crop_type=crop_type
        )
        db.session.add(user)
        db.session.commit()
        return self._to_dict(user)
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        from database.models import User
        user = User.query.filter_by(username=username).first()
        return self._to_dict(user) if user else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        from database.models import User
        user = User.query.filter_by(email=email).first()
        return self._to_dict(user) if user else None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        from database.models import User
        try:
            uid = int(user_id) if str(user_id).isdigit() else int(str(user_id).replace('user_', ''))
            user = User.query.get(uid)
            return self._to_dict(user) if user else None
        except:
            return None
    
    def update_user(self, user_id: str, **kwargs) -> Optional[Dict]:
        from database.models import User
        from database.db import db
        try:
            uid = int(user_id) if str(user_id).isdigit() else int(str(user_id).replace('user_', ''))
            user = User.query.get(uid)
            if not user:
                return None
            protected_fields = ['id', 'password_hash', 'created_at', 'username', 'email']
            for key, value in kwargs.items():
                if key not in protected_fields and hasattr(user, key):
                    setattr(user, key, value)
                elif key == 'crop_type':
                    user.default_crop_type = value
            db.session.commit()
            return self._to_dict(user)
        except:
            return None
    
    def update_last_login(self, user_id: str) -> bool:
        from database.models import User
        from database.models import LoginHistory
        from database.db import db
        try:
            uid = int(user_id) if str(user_id).isdigit() else int(str(user_id).replace('user_', ''))
            user = User.query.get(uid)
            if user:
                history = LoginHistory(user_id=uid)
                db.session.add(history)
                db.session.commit()
                return True
            return False
        except:
            return False
    
    def change_password(self, user_id: str, old_password_hash: str, 
                       new_password_hash: str) -> bool:
        from database.models import User
        from database.db import db
        try:
            uid = int(user_id) if str(user_id).isdigit() else int(str(user_id).replace('user_', ''))
            user = User.query.get(uid)
            if not user:
                return False
            if not UserAuthenticator.verify_password(old_password_hash, user.password_hash):
                return False
            user.password_hash = new_password_hash
            db.session.commit()
            return True
        except:
            return False
    
    def get_all_users(self) -> list:
        from database.models import User
        return [self._to_dict(u) for u in User.query.all()]
    
    def get_users_by_role(self, role: str) -> list:
        from database.models import User
        return [self._to_dict(u) for u in User.query.filter_by(role=role).all()]



# ============================================================================
# GLOBAL INSTANCES
# ============================================================================

# Initialize authenticator and database
auth = UserAuthenticator()
user_db = UserDatabase()


# ============================================================================
# HELPER FUNCTIONS FOR FLASK INTEGRATION
# ============================================================================

def login_required(f):
    """Decorator to protect routes - requires valid JWT token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Missing authorization token'}), 401
        
        try:
            # Extract token from "Bearer <token>"
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({'error': 'Invalid authorization header'}), 401
        
        # Verify token
        payload = auth.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add user info to request context
        request.user = payload
        
        return f(*args, **kwargs)
    
    return decorated_function


def admin_required(f):
    """Decorator to protect admin routes"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify
        
        # Check if user has admin role
        if request.user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
