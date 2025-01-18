from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    cover = db.Column(db.String(200))  # Caminho para a imagem da capa
    quotes = db.relationship('Quote', backref='book', lazy=True, cascade="all, delete")
    summary = db.Column(db.Text)
    rating = db.Column(db.Integer)
    characters = db.relationship('Character', backref='book', lazy=True)

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)


class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.Integer, nullable=True)
    type = db.Column(db.String(50))
    text = db.Column(db.String(500), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    notes = db.Column(db.Text)  # Novo campo para anotações
