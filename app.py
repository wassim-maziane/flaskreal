"""

Pour visualiser tous les éléments de notre application, il est nécessaire d'avoir accès à Internet,
car nous avons utilisé des liens Bootstrap pour la mise en forme et l'affichage de certaines fonctionnalités.

"""
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from forms.forms import BookForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<Le livre {self.title}>'

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            genre=form.genre.data
        )
        db.session.add(book)
        db.session.commit()
        flash('Le livre est ajouté avec succès!',"success")
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)

    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.genre = form.genre.data
        db.session.commit()
        flash('Le livre a été mis à jour avec succès!',"success")
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, book=book)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Le livre est supprimé avec succès!',"success")
    return redirect(url_for('index'))

@app.route('/search')
def search():

    query = request.args.get('query')
    books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
    return render_template('search.html', query=query, books=books)

if __name__ == '__main__':
    app.run(debug=True)

