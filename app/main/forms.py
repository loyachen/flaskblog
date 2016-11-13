# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


class CommentForm(Form):
    name = StringField('昵称', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                            Email()])
    content = TextAreaField('内容', validators=[DataRequired(), Length(1, 1024)])
    follow = StringField(validators=[DataRequired()])
