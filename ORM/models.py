# Файл со структурой нашей БД

# Берем механизм взаимодействия из database
from .database import Base

# Добавление полей
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


# Сама модель (таблица) БД
class Post(Base):
    # Задаём название таблицы в БД (но обращаться в коде будем через название класса)
    __tablename__ = "posts"

    # Указываем атрибуты таблицы
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=True, server_default='TRUE')  # , default=True
    rating = Column(Integer, nullable=True)

    # Установка поля для связи многие (посты) к одному (автору)
    owner_id = Column(Integer, ForeignKey("authors.id"))
    # Связка объекта Post с объектом из класса Author, для удобного обращения к связанным объектам
    owner = relationship("Author", back_populates="posts")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    name = Column(String, nullable=False)

    # Связка с объекта Author с объектами из класса Post, для удобного обращения к связанным объектам
    posts = relationship("Post", back_populates="owner")
