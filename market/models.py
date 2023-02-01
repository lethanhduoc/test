from market.index import db
from sqlalchemy import Column, Integer, Enum, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin, login_manager
from market.index import bcrypt

class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    name = Column(String(25), nullable=False, unique=True)
    password_hash = Column(String(200), nullable=False)
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __str__(self):
        return self.name


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    products = relationship('Product', backref='category', lazy=True)  # tạo khóa ngoại

    def __str__(self):
        return self.name  # lay ten k lay doi tuong


product_tag = db.Table('product_tag',
                       Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
                       Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))


class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    price = Column(Float, default=0)
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    tags = relationship('Tag', secondary='product_tag', lazy='subquery',
                        backref=backref('products', lazy=True))


class Tag(db.Model):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)  # tên k dc trung nhau

    def __str__(self):
        return self.name

if __name__ == '__main__':
    db.create_all()