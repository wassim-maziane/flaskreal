from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    author = StringField('Auteur', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    submit = SubmitField('Ajouter')

