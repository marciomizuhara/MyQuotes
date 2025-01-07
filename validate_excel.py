import pandas as pd

# Caminho do arquivo Excel
EXCEL_FILE = 'quotes.xlsx'

def validate_excel():
    try:
        df = pd.read_excel(EXCEL_FILE)
        print(df.head())  # Mostrar as primeiras linhas
        print("\nColunas encontradas no Excel:", df.columns)
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")


if __name__ == '__main__':
    validate_excel()