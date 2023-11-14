# Пакет для авторизации через oauth2.0 с помощью JWT аутентификации

# Установка пакета с JWT token
# pip install "python-jose[cryptography]"
from jose import JWTError, jwt

from datetime import datetime, timezone, timedelta

from . import schemas

# Секретный ключ для установки начального значения
# SECRET_KEY

# Алгоритм хэширования HS256 - метод хэширования: SHA-256
# Algorithm

# Время действия токена (в минутах)
# Expriation time

# Вбил рандомный секретный ключ просто стуча по клавиатуре
SECRET_KEY = "fjd932u8a8u89dqu3o9r23jrlkfv09fdugmr2l0audah4t4pxnmcnz5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Создание токена авторизации из секретного ключа
def create_access_token(data: dict):
    # Копия данных
    to_encode = data.copy()

    # Время просрочки токена
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Указание время просрочки
    to_encode.update({"exp": expire})

    # Кодирование токена с секретным ключом и данными через указанные алгоритм
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Проверка токена в функцию вписываем сам токен и
# переменную в которой будет ошибка,
# которая будет вызываться в случае неправильных данных

def verify_access_token(token: str, credentials_exception):
    try:
        # Декодирование токена
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Получение ID пользователя
        id: str = payload.get("user_id")

        # Проверяем наличие ID
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


# -------------------
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Установка адресации на авторизацию по пути,
# по сути это ссылается на метод login в пакете auth
# может быть полезно при использовании swagger, чтобы он брал наш метод, а не что-нибудь другое
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login/oauth')


# -------------------

# Проверка авторизации пользователя
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Указание ошибки
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # проверяем токен через метод verify (выше), если что-то не так,
    # то, указанная ошибка в credentials_exception будет вызвана
    return verify_access_token(token, credentials_exception)
