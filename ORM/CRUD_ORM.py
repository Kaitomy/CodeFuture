import uvicorn
from fastapi import FastAPI, Response, status, HTTPException, Depends

from sqlalchemy.orm import Session

# Подключаем элементы из других файлов
from .database import engine, get_db
from . import models, schemas

# Метод для создания БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)


# Получение каталога постов
# С помощью db обращаемся к процессу взаимодействия с БД черезе метод get_db
@app.get("/posts")
async def all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# Использование валидационной формы
# В этом случае необходимо указывать параметр response_model, чтобы возвращаемые
# данные имели представление схемы Post.
# Если возвращается список, то следует схему вложить в тип данных list.
# Также возвращаемые данные должны состоять из объектов БД (не нужно делать словарь)
@app.get("/posts/valid", response_model=list[schemas.Post])
async def all_posts_valid(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


# Получение конкретной новости
@app.get("/posts/{id}")
async def one_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Проверяем возвращаемой записи, если её нет, то выводим ошибку
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    return {"data": post}


# Получение валидационной новости
@app.get("/posts/valid/{id}", response_model=schemas.Post)
async def one_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    return post


# Также валидационные формочки можно использовать не только формата для возврата,
# но и для проверки полученных данных
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())

    # Добавление новой записи в БД
    db.add(new_post)
    # Подтверждение транзакции и сохранение состояния БД
    db.commit()
    # Обновление новой записи для получения id
    db.refresh(new_post)

    return {"message": "post created", "data": new_post}


#  Валидационный возврат данных
@app.post("/posts/valid", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post_valid(post: schemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Изменение
@app.put("/posts/{id}")
async def update_full_post(id: int, post_upd: schemas.PostBase, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    post.update(post_upd.model_dump(), synchronize_session=False)
    db.commit()

    return {"data": "post updated"}


# Удаление
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    post.delete(synchronize_session=False)
    db.commit()

    return {"data": f"post id: {id} deleted"}

# Вывод автора
@app.get("/author", response_model=list[schemas.Author])
async def all_posts_valid(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()

    return authors

# Создание автора
@app.post("/author", status_code=status.HTTP_201_CREATED)
async def create_author(author: schemas.Author, db: Session = Depends(get_db)):
    new_author = models.Author(**author.model_dump())


    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return {"message": "author created", "data": new_author}


# Соединение данных
@app.put("/connection/{id_post}/{id_author}")
async def update_full_post(id_post: int, id_author: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id_post)
    author = db.query(models.Post).filter(models.Author.id == id_author)

    # Проверка
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    # Проверка
    if author.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"author with id: {id} does not exist"
        )

    # Указание посту автора, который пост и написал
    post.first().owner_id = author.first().id
    db.commit()

    return {"data": "post connected"}


if __name__ == "__main__":
    uvicorn.run(app)
