import databases
import sqlalchemy
from pydantic import BaseModel, Field
from datetime import datetime


class Product(BaseModel):
    id: int = Field(qt=0)
    product_name: str = Field(title='product_name', min_length=2, max_length=20)
    description: str | None = Field(title='description', max_length=2048, default=None)
    price: float = Field(title='price', qe=0)


class User(BaseModel):
    id: int = Field(qt=0)
    firstname: str = Field(title='firstname', min_length=2, max_length=20)
    lastname: str = Field(title='lastname', max_length=20)
    email: str = Field(title='email', max_length=128, pattern="([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)")
    password: str = Field(title='password', min_length=4)


class Order(BaseModel):
    id: int = Field(qt=0)
    user_id: int = Field(qt=0)
    product_id: int = Field(qt=0)
    date_at: datetime
    status: int = Field(qt=0, lt=8)


DB_URL = "sqlite:///hw6/db/my_db.db"
db = databases.Database(DB_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column("firstname", sqlalchemy.String(20)),
    sqlalchemy.Column("lastname", sqlalchemy.String(20)),
    sqlalchemy.Column("email", sqlalchemy.String(128), unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(2048)),
)
products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column("product_name", sqlalchemy.String(20)),
    sqlalchemy.Column("description", sqlalchemy.String(2048)),
    sqlalchemy.Column("price", sqlalchemy.FLOAT),
)
orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column("product_id", sqlalchemy.ForeignKey('products.id')),
    sqlalchemy.Column("date_at", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.INTEGER),
)

engine = sqlalchemy.create_engine(DB_URL, connect_args={'check_same_thread': False})
metadata.create_all(engine)
