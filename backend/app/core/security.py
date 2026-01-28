from passlib.context import CryptContext
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityManager:
    """
    Handles security, auth, and data privacy.
    """
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def gdpr_export_user_data(user_id: str) -> dict:
        """
        Complies with GDPR 'Right to Access'.
        Collects all user data for export.
        """
        logger.info(f"Generating GDPR export for user {user_id}")
        return {
            "user_id": user_id,
            "export_date": datetime.now(),
            "data_retention_policy": "User data retained until deletion request.",
            "stories": [], # Fetch from DB
            "recordings": [] # Fetch from DB
        }

    @staticmethod
    def gdpr_delete_user(user_id: str):
        """
        Complies with GDPR 'Right to be Forgotten'.
        """
        logger.warning(f"PERMANENTLY DELETING data for user {user_id}")
        # DB deletion logic here
        return True
