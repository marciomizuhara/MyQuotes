import pandas as pd
from openpyxl import Workbook
from app import db, app
from models import Book, Quote
import time

# Caminhos dos arquivos
INPUT_FILE = r'N:/Donwloads/My Clippings.txt'
EXCEL_FILE = r'N:/Donwloads/quotes.xlsx'


# -------------------------------
# 1️⃣ Lógica de Processamento do Kindle
# -------------------------------

def get_type_and_note(note):
    """
    Determina o tipo com base na palavra-chave no conteúdo
    e retorna também o texto restante como nota.
    """
    note = note.strip()
    lower_note = note.lower()

    if lower_note.startswith('verde'):
        return 3, note[5:].strip()
    if lower_note.startswith('vermelho'):
        return 1, note[8:].strip()
    if lower_note.startswith('azul'):
        return 4, note[4:].strip()
    if lower_note.startswith('amarelo'):
        return 2, note[7:].strip()

    return 0, ''


def process_clippings():
    # Criar planilha Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Valid Quotes"
    ws.append(['Page', 'Type', 'Quote', 'Author', 'Book', 'Note'])  # Removida coluna 'Cover'

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_data = f.read()

    blocks = raw_data.split('==========')
    entries = []
    last_highlight = None

    for i in range(len(blocks)):
        block = blocks[i].strip()
        if not block:
            continue

        lines = block.split('\n')
        lines = [line.strip() for line in lines if line.strip()]

        if len(lines) < 2:
            continue

        book_info = lines[0]
        if '(' in book_info and ')' in book_info:
            book_title = book_info.split('(')[0].strip()
            author = book_info.split('(')[-1].replace(')', '').strip()
        else:
            book_title = book_info.strip()
            author = 'Unknown'

        meta_info = lines[1]
        page = None
        if 'page' in meta_info.lower():
            page_part = [p for p in meta_info.split('|') if 'page' in p.lower()]
            if page_part:
                try:
                    page = int(page_part[0].split()[-1])
                except ValueError:
                    page = None

        content = '\n'.join(lines[2:]).strip()
        note_type, note_text = get_type_and_note(content)

        if note_type > 0 and last_highlight:
            last_highlight['type'] = note_type
            last_highlight['note'] = note_text
            entries.append(last_highlight)
            last_highlight = None
            continue

        if 'highlight' in meta_info.lower():
            last_highlight = {
                'page': page,
                'type': 0,
                'quote': content,
                'note': '',
                'author': author,
                'book': book_title
            }

    for entry in entries:
        ws.append([
            entry['page'],
            entry['type'],
            entry['quote'].strip(),
            entry['author'],
            entry['book'],
            entry['note'].strip()
        ])

    wb.save(EXCEL_FILE)
    print(f"✅ Arquivo Excel salvo com sucesso: {EXCEL_FILE}")


# -------------------------------
# 2️⃣ Lógica de Importação para o Banco
# -------------------------------

def import_from_excel():
    with app.app_context():
        try:
            df = pd.read_excel(EXCEL_FILE)

            for index, row in df.iterrows():
                if pd.isna(row['Book']) or pd.isna(row['Quote']):
                    print(f"🛑 Linha {index + 1}: Dados incompletos, pulando...")
                    continue

                # Busca por livro existente com comparação robusta
                book = Book.query.filter(
                    Book.title.ilike(row['Book'].strip()),
                    Book.author.ilike(row['Author'].strip()) if pd.notna(row['Author']) else True
                ).first()

                if not book:
                    # Criar livro caso não exista
                    book = Book(
                        title=row['Book'].strip(),
                        author=row['Author'].strip() if pd.notna(row['Author']) else 'Unknown'
                    )
                    db.session.add(book)
                    db.session.commit()
                    print(f"📚 Livro criado: {book.title} - Autor: {book.author}")

                # Busca por citação existente para evitar duplicação
                existing_quote = Quote.query.filter(
                    Quote.text.ilike(row['Quote'].strip()),
                    Quote.book_id == book.id
                ).first()

                if existing_quote:
                    # Atualizar notas se necessário
                    if pd.notna(row['Note']) and (
                            not existing_quote.notes or existing_quote.notes.strip() != row['Note'].strip()):
                        existing_quote.notes = row['Note'].strip()
                        db.session.commit()
                        print(f"🔄 Nota atualizada para citação existente: {existing_quote.text}")
                    else:
                        print(f"⚠️ Citação duplicada encontrada, sem alterações. (Linha {index + 1})")
                    continue

                # Criar nova citação
                quote = Quote(
                    page=int(row['Page']) if pd.notna(row['Page']) else None,
                    type=row['Type'] if pd.notna(row['Type']) else '0',
                    text=row['Quote'].strip(),
                    notes=row['Note'].strip() if pd.notna(row['Note']) else '',
                    book_id=book.id
                )
                db.session.add(quote)
                print(f"✅ Citação adicionada ao livro: {book.title}")

            db.session.commit()
            print("🚀 Importação concluída com sucesso!")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro: {e}")


# -------------------------------
# 3️⃣ Execução Unificada
# -------------------------------

if __name__ == '__main__':
    print("🔄 Processando My Clippings...")
    process_clippings()

    print("⏳ Aguardando para garantir que o arquivo esteja salvo...")
    time.sleep(2)

    print("📥 Importando para o banco de dados...")
    import_from_excel()
