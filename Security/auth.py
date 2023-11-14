# Пакет авторизации
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

# Добавление нужных частей нашей API
from . import database, schemas, models, utils, oauth2

# Формочка для запроса пароля
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


# Создание роутера
# Роутеры позволяют прописать функции и Url-пути в отдельном файле и всё разом
# подключить в точку входа и основного приложения, т.е. в main.py (Разделяй и властвуй)
router = APIRouter(tags=['Authentication'])


# Можно авторизоваться с помощью своей формы
# В этом случае в postman следует передавать данные в Body->raw->JSON
@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    # Получение пользователя с бд
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    # Проверка наличия пользователя (то что он вернулся из БД)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
        )

    # Проверка верификации, если у пользователя хэш паролей не совпадает -> возвращаем ошибку
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
        )

    # Создаём токен из пользователя что залогинился
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

    # После получения токена следует его скопировать и использовать в postman

    # Проверить правильно JWT токена можно посмотреть по https://jwt.io/ во вкладке Debugger


# Можно авторизоваться с помощью формы OAuth2PasswordRequestForm (email заменяется username)
# В этом случае в postman следует передавать данные в Body->form-data
@router.post('/login/oauth')
def login_oauth(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}