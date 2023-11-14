# Схемы необходимы для валидации данных и
# чтобы не засорять основной файл
from pydantic import BaseModel
from typing import Optional

# Стандартная Форма Поста
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Наследование Формы
class PostCreate(PostBase):
    pass

# Переопределю атрибут published,
# чтобы при обновлении не ставилось значение по умолчанию
class UpdatePost(PostBase):
    published: bool


# Модель для возврата данных (чтобы возвращалось не всё, а лишь указанное ниже)
class Post(BaseModel):
    title: str
    content: str
    published: bool

    # В случае ошибки при возврате класса Post следует сконфигурировать
    # orm_mode в классе Config. Нужно это для SQLAlchemy т.к. по умолчанию
    # он работает с словарями, а не с форматом ORM
    class Config:
        orm_mode = True


class Author(BaseModel):
    first_name: str
    name: str

