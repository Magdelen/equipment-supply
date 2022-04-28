from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class EquipmentPostForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    title = StringField('Equipment Name', validators=[DataRequired()])
    text = TextAreaField('Equipment Description And Contact Details', validators=[DataRequired()])
    submit = SubmitField('Post')
