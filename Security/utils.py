# Пакет с отдельными функциями
from passlib.context import CryptContext

# Объект хэширования
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Хэширование
def hash(password: str):
    return pwd_context.hash(password)

# Сравнение паролей по хэшу
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
