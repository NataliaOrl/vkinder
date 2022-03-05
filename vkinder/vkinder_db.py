import sqlalchemy as sq
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import name, password, host

Base = declarative_base()
engine = sq.create_engine(f'postgresql+psycopg2://{name}:{password}@{host}/vkinder_db', client_encoding='utf8')
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    user_id = sq.Column(sq.Integer, unique=True)


class FavorList(Base):
    __tablename__ = 'favorites'
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, unique=True)
    url_photo = sq.Column(sq.String)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))


class BlackList(Base):
    __tablename__ = 'black list'
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, unique=True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))


def register_user(user_id):
    try:
        new_user = User(user_id=user_id)
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False


def check_db_user(id_owner):
    owner_user = session.query(User).filter_by(user_id=id_owner).first()
    return owner_user


def check_db_favor(id):
    favor_user = session.query(FavorList).filter_by(user_id=id).first()
    return favor_user


def check_db_block(id):
    block_user = session.query(BlackList).filter_by(user_id=id).first()
    return block_user


def add_user_favor(user_id, url_photo):
    user = FavorList(
        user_id=user_id,
        url_photo=url_photo)
    session.add(user)
    session.commit()


def add_user_block(user_id):
    user = BlackList(
        user_id=user_id)
    session.add(user)
    session.commit()


def create():
    Base.metadata.create_all(engine)


def drop():
    Base.metadata.drop_all(engine)
