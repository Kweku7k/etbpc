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
    field1 = StringField('field1', validators=[DataRequired()])
    field2 = StringField('field2', validators=[DataRequired()])
    field3 = StringField('field3', validators=[DataRequired()])
    field4 = StringField('field4', validators=[DataRequired()])
    date = StringField('date', validators=[DataRequired()])
    submit = SubmitField('New Update')