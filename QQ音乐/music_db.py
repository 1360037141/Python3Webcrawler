from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('mysql+pymysql://root:1234@localhost:3306/test1?charset=utf8')
DBsession = sessionmaker(bind=engine)
SQLsession = DBsession()
Base = declarative_base()

class song(Base):
    __tablename__='song'
    song_id=Column(Integer,primary_key=True,autoincrement=True)
    song_name=Column(String(64))
    song_ablum=Column(String(64))
    song_mid=Column(String(50))
    song_singer=Column(String(50))
Base.metadata.create_all(engine)

def insert_data(songs):
    engine=create_engine('mysql+pymysql://root:1234@localhost:3306/test1?charset=utf8')
    DBsession=sessionmaker(bind=engine)
    SQLsession=DBsession()
    data=song(
        song_name= songs['songname'],
        song_ablum= songs['albumname'],
        song_mid=songs['songmid'],
        song_singer= songs['song_singer']
    )
    SQLsession.add(data)
    SQLsession.commit()

