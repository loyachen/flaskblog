import os


class Config():
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    # 配置mysql路径 此处一般使用环境变量代替，增加安全性
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@10.0.0.12/flaskblog'
    ARTICLES_PER_PAGE = 10
    COMMENTS_PER_PAGE = 6
    SECRET_KEY = 'secret key to protect from csrf'
    WTF_CSRF_SECRET_KEY = 'random key for form'

    @staticmethod
    def init_app(app):
        pass
