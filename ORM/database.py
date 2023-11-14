# Файл для установки и настройки взаимодействия FastAPI с БД

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Строка подключения sqlite и указание места сохранения в sql_app.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./ORM/sql_orm.db"

# Сам механизм работы с нашей БД
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Сессия. Или же установка соединения с нашей БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Объект через который мы будем наследоваться для создания таблиц в models.py
Base = declarative_base()


# Получение базы данных для взаимодействия
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
