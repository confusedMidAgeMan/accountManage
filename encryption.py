from cryptography.fernet import Fernet
import base64
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptionManager:
    def __init__(self):
        self.salt = b'account_manager_salt'  # 固定盐值
        
    def generate_key(self, master_key: str) -> bytes:
        """根据用户输入的主密钥生成加密密钥"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
        return key

    def encrypt_password(self, password: str, master_key: str) -> str:
        """加密密码"""
        key = self.generate_key(master_key)
        f = Fernet(key)
        encrypted_password = f.encrypt(password.encode())
        return encrypted_password.decode()

    def decrypt_password(self, encrypted_password: str, master_key: str) -> str:
        """解密密码"""
        try:
            key = self.generate_key(master_key)
            f = Fernet(key)
            decrypted_password = f.decrypt(encrypted_password.encode())
            return decrypted_password.decode()
        except Exception:
            raise ValueError("密钥错误或数据已损坏") 