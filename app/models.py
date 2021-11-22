from app import db
from datetime import datetime

class User(db.Model) :
    id = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    member_flag = db.Column(db.Boolean(), nullable=False, default=True) # 회원 여부

    def __repr__(self) :
        return f'{self.name}({self.id})'

class Credential(db.Model) :
    user_id = db.Column(db.String(30), db.ForeignKey('user.id', onupdate='CASCADE'), primary_key=True)
    cred_ex_id = db.Column(db.String, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# 채팅 정보
class Chatinfo(db.Model) :
    chat_no = db.Column(db.Integer, primary_key=True) # 채팅방 번호(auto_increment)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # 생성 날짜
    user1 = db.Column(db.String(30), db.ForeignKey('user.id', onupdate='CASCADE')) # 대표자
    user2 = db.Column(db.String(30), db.ForeignKey('user.id', onupdate='CASCADE')) # 참여자

    def __repr__(self) :
        return f'{self.chat_no}({self.user1}, {self.user2})'

# 채팅 내용
class Chat(db.Model) :
    chat_no = db.Column(db.Integer, db.ForeignKey('chatinfo.chat_no'), primary_key=True) # 채팅방 번호
    message_no = db.Column(db.Integer, primary_key=True) # 메시지 번호
    message_owner = db.Column(db.String(30), db.ForeignKey('user.id', onupdate='CASCADE')) # 메시지 주인
    message_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # 메시지 날짜
    message = db.Column(db.Text, nullable=False)

    def __repr__(self) :
        return f'{self.message_owner} sent message({self.message_no})'

# 임시용 채팅 기록 데이터베이스
class History2(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=True, default="System")
    message = db.Column('message', db.String)
    #timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)