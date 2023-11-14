import uvicorn
from fastapi import FastAPI, Response, status, HTTPException, Depends

from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine, get_db

# pip install passlib
# pip install bcrypt
# Шифрование пароля
from passlib.context import CryptContext

# Использование пакета с функциями utils.py
from . import utils

# Использование пакета с функциями utils.py
from . import auth

from . import oauth2

# Создание механизма шифрования
# Также можно перенести любые отдельные куски кода (особенно повторяющиеся) в utils.py
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

# Дополнительный роутер взятый из auth
app.include_router(auth.router)



@app.get("/users", status_code=status.HTTP_201_CREATED)
def all_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Перед созданием хэшируемые пароль
    # hashed_password = pwd_context.hash(user.password)
    # user.password = hashed_password

    # Использование функции из utils.py
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Создание пользователя
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist"
        )

    return user


#----------- Проверка работы токенов и авторизации ----------

# Обычное получение данных
@app.get("/posts")
async def all_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return {"data": posts}


# Обычное создание
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):

    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"message": "post created", "data": new_post}


# Получение данных по авторизации
# Для прохождения авторизации через Postman необходимо во вкладке Headers
# добавить новый ключ "Authorization" и в его значение указать "Bearer <токен>" (без кавычек)

# токен возвращается при авторизации

# Для установки проверки укажем в параметрах (oauth2.get_current_user)
@app.get("/posts/verify")
async def all_posts_verify(
        db: Session = Depends(get_db),
        get_current_user: int = Depends(oauth2.get_current_user)):

    posts = db.query(models.Post).all()

    return {"data": posts}

@app.post("/posts/verify", status_code=status.HTTP_201_CREATED)
async def create_post(
        post: schemas.PostBase,
        db: Session = Depends(get_db),
        get_current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"message": "post created", "data": new_post}



if __name__ == "__main__":
    uvicorn.run(app)
