from flask import Flask, render_template, request, redirect, url_for
from models import db, Book, Quote
from sqlalchemy.sql.expression import func
from sqlalchemy.sql import text
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def random_quotes():
    """Exibe citações aleatórias na página inicial."""
    search_query = request.args.get('search')
    if search_query:
        quotes = Quote.query.join(Book).filter(
            (Quote.text.contains(search_query)) |
            (Book.title.contains(search_query)) |
            (Book.author.contains(search_query))
        ).all()
    else:
        quotes = Quote.query.order_by(func.random()).all()
    return render_template('index.html', quotes=quotes)


@app.route('/all')
def all_quotes():
    search_query = request.args.get('search')
    books = Book.query.all()  # Carrega todos os livros para a galeria

    if search_query:
        quotes = Quote.query.join(Book).filter(
            (Quote.text.contains(search_query)) |
            (Book.title.contains(search_query)) |
            (Book.author.contains(search_query)) |
            (Quote.notes.contains(search_query))
        ).order_by(Quote.id.desc()).all()
    else:
        quotes = Quote.query.order_by(Quote.id.desc()).all()

    return render_template('index.html', quotes=quotes, books=books)


@app.route('/gallery')
def gallery_view():
    """Exibe uma galeria com as capas dos livros."""
    books = Book.query.all()
    return render_template('gallery.html', books=books)


@app.route('/type/<int:type_id>')
def filter_by_type(type_id):
    """Filtra citações por tipo respeitando os parâmetros atuais da URL."""
    search_query = request.args.get('search', '')
    view_mode = request.args.get('view', '')

    # Base query com filtro por tipo
    quotes = Quote.query.filter_by(type=type_id)
    books = Book.query.all()

    # Aplicar busca, se existir
    if search_query:
        quotes = quotes.join(Book).filter(
            (Quote.text.contains(search_query)) |
            (Book.title.contains(search_query)) |
            (Book.author.contains(search_query))
        )

    # Buscar citações filtradas
    quotes = quotes.all()

    # Respeitar a visualização atual (gallery ou table)
    if view_mode == 'gallery':
        return render_template('index.html', books=books, view='gallery')

    return render_template('index.html', quotes=quotes, books=books, view='table')





@app.route('/add_quote', methods=['GET', 'POST'])
def add_quote():
    if request.method == 'POST':
        page = request.form['page']
        type = request.form['type']
        text = request.form['text']
        book_title = request.form['book']
        author = request.form['author']
        cover = request.form['cover']

        # Buscar ou criar livro
        book = Book.query.filter_by(title=book_title).first()
        if not book:
            book = Book(title=book_title, author=author, cover=cover)
            db.session.add(book)
            db.session.commit()

        # Adicionar quote
        new_quote = Quote(
            page=page,
            type=type,
            text=text,
            book_id=book.id
        )
        db.session.add(new_quote)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_quote.html')


@app.route('/update_note', methods=['POST'])
def update_note():
    data = request.get_json()
    quote_id = data.get('quote_id')
    new_note = data.get('note')

    if quote_id is None:
        return {'status': 'error', 'message': 'ID da citação não fornecido'}, 400

    quote = Quote.query.get(quote_id)
    if not quote:
        return {'status': 'error', 'message': 'Citação não encontrada'}, 404

    if new_note == '':  # Exclusão de nota
        quote.notes = None
        message = 'Nota removida com sucesso'
    else:  # Edição ou Salvamento de nota
        quote.notes = new_note.strip()
        message = 'Nota atualizada com sucesso'

    db.session.commit()
    return {'status': 'success', 'message': message}




@app.route('/sql-query', methods=['GET', 'POST'])
def sql_query():
    if request.method == 'POST':
        query = request.form.get('sql_query')
        try:
            result = db.session.execute(text(query))
            results = [dict(row) for row in result]
        except Exception as e:
            return f"Erro: {e}"
    return render_template('index.html', sql_results=results)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
