from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class ScriptureForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', widget=TextArea(), validators=[DataRequired()])
    link = StringField('Scripture link', validators=[ DataRequired()])
    submit = SubmitField('Upload New Scripture Reading')


class UpdateForm(FlaskForm):
    field1 = StringField('People Contributed', validators=[DataRequired()])
    field2 = StringField('Money Accrued', validators=[DataRequired()])
    field3 = StringField('Bibles Bought', validators=[DataRequired()])
    field4 = StringField('Bibles Distributed', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('New Update')