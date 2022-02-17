import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from base_bot import write_msg

Base = declarative_base()
engine = sq.create_engine('postgresql+psycopg2://postgres:password@localhost:5432/vkinder_db', client_encoding='utf8')
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

class Favor_list(Base):
    __tablename__ = 'favorites'
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, unique=True)
    url_photo = sq.Column(sq.String)

class Black_list(Base):
    __tablename__ = 'black list'
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, unique=True)

def check_db_favor(id):
    favor_user = session.query(Favor_list).filter_by(user_id=id).first()
    return favor_user

def check_db_block(id):
    block_user = session.query(Black_list).filter_by(user_id=id).first()
    return block_user

def add_user_favor(user_id, url_photo):
    user = Favor_list(
    user_id=user_id,
    url_photo=url_photo)
    session.add(user)
    session.commit()

def add_user_block(user_id):
    user = Black_list(
    user_id=user_id)
    session.add(user)
    session.commit()

def send_favorites(user_id):
    for user, photo in session.query(Favor_list.user_id, Favor_list.url_photo): 
        n = photo.split(',')
        write_msg(user_id, f"Ссылка на страницу пользователя: https://vk.com/id{user}\n"           
                           f"Фотографии пользователя с наибольшим количеством лайков:\n{n[0]}\n{n[1]}\n{n[2]}\n")

def create():
    Base.metadata.create_all(engine)


def drop():
    Base.metadata.drop_all(engine)



