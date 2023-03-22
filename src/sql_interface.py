import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import datetime

engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False) # エンジンの定義？
Base = sqlalchemy.ext.declarative.declarative_base() # sqlalchemyでデータベースのテーブルを扱うための宣言

# テーブルのフィールドを定義
class Session(Base):
    __tablename__ = 'sessions'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    prompt = sqlalchemy.Column(sqlalchemy.String(500))
    completion = sqlalchemy.Column(sqlalchemy.String(500))
    channel_id = sqlalchemy.Column(sqlalchemy.String(100))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime)

# # for thread
# class Thread(Base):
#     id = sqlalchemy.Column(
#         sqlalchemy.Integer, primary_key=True, autoincrement=True
#     )
#     prompt = sqlalchemy.Column(sqlalchemy.String(500)
#     completion = sqlalchemy.Column(sqlalchemy.String(500))
#     thread_id = sqlalchemy.Column(sqlalchemy.String(100))
#     created_at = sqlalchemy.Column(sqlalchemy.DateTime))

Base.metadata.create_all(engine) # データベースにテーブルを作成
SessionDataBase = sqlalchemy.orm.sessionmaker(bind=engine) # データベースに接続するためのセッションを準備

# 本体
class SessionManager:
    def __init__(self):
        self.session = SessionDataBase()

    def add_record(self, prompt, completion, channel_id):
        # レコードを準備し、セッションを通してデータベースに送る
        s = Session(
            prompt=prompt,
            completion=completion,
            channel_id=channel_id,
            created_at=datetime.datetime.now()
        )
        self.session.add(s)
        self.session.commit()

    def get_pair_list(self, channel_id):
        # channel_idを指定して、promptとcompletionを古い順に取得する
        record_list = self.session.query(Session).filter_by(channel_id=channel_id).order_by(Session.created_at.desc()).limit(10).all() 
        # promptとcompletionのペアの配列を取得する
        pair_list = [(record.prompt, record.completion) for record in record_list]
        return pair_list

    def delete_pair_list(self, channel_id):
        # データベースから指定されたchannel_idのレコードを削除する
        record_list = self.session.query(Session).filter_by(channel_id=channel_id).all()
        for record in record_list:
            self.session.delete(record)
        self.session.commit()

    def get_pair_count(self, channel_id):
        # データベースから指定されたchannel_idのレコードの件数を取得する
        count = self.session.query(Session).filter_by(channel_id=channel_id).count()
        return count
