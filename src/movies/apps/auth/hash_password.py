from passlib.context import CryptContext

# Создаем объект контекста для хеширования паролей с использованием bcrypt
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для хеширования пароля
def hash_password(password: str) -> str:
    return password_context.hash(password)

# Функция для проверки соответствия открытого пароля и его хеша
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)
