from app import db, app


def reset_database():
    with app.app_context():
        # Remover o banco de dados existente (se houver)
        import os
        db_path = os.path.join(app.instance_path, 'database.db')
        if os.path.exists(db_path):
            os.remove(db_path)
            print("Banco de dados existente removido.")

        # Criar o banco de dados novamente
        db.create_all()
        print("Novo banco de dados criado com sucesso!")

if __name__ == '__main__':
    reset_database()
