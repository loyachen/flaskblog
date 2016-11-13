#!/usr/bin/env python

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import ArticleType, Article, User, Menu, ArticleTypeSetting

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


# Global variables to jiajia2 environment:
app.jinja_env.globals['Menu'] = Menu
app.jinja_env.globals['Article'] = Article
app.jinja_env.globals['ArticleType'] = ArticleType


def make_shell_context():
    return dict(db=db, ArticleType=ArticleType, Article=Article, User=User, \
                Menu=Menu, ArticleTypeSetting=ArticleTypeSetting)

manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import User, ArticleTypeSetting, ArticleType

    # upgrade database to the latest version
    upgrade()

    User.insert_admin(email='810959120@qq.com', username='loya', password='00')
    ArticleTypeSetting.insert_system_setting()
    ArticleType.insert_system_articleType()


if __name__ == '__main__':
    manager.run()
