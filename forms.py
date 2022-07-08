from flask_wtf import FlaskForm
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import DataRequired, Length


class ResultsForm(FlaskForm):
    link = URLField('Results link', validators=[DataRequired()])
    startRollNo = StringField('Starting Roll No.', validators=[
        DataRequired(),
        Length(10),
    ])
    endRollNo = StringField('Ending Roll No.', validators=[
        DataRequired(),
        Length(10),
    ])
    filename = StringField('File name', validators=[DataRequired()])
    submit = SubmitField('Download')
