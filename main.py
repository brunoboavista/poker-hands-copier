import os
import re
import shutil
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

# Constantes
SOURCE_DIR = os.getenv("SOURCE_DIR")
DEST_DIR = os.getenv("DEST_DIR")
REGEX_T_DIGITS = r"T(\d+)"
REGEX_DATE = r"(\d{4})/(\d{2})/(\d{2}) (\d{2}:\d{2}:\d{2}) BRT"

print(f"\nSource Directory: {SOURCE_DIR}")

def arquivo_deve_ser_copiado(src_path, dest_path):
    if not os.path.exists(dest_path):
        return True
    
    # Verifica se o arquivo de origem foi modificado depois do destino
    if os.path.getmtime(src_path) > os.path.getmtime(dest_path):
        return True
    return False


def copiar_arquivos():
    for filename in os.listdir(SOURCE_DIR):
        src_path = os.path.join(SOURCE_DIR, filename)
        # Lê a primeira linha do arquivo para extrair a data
        with open(src_path, encoding="utf-8") as f:
            primeira_linha = f.readline()
        date_match = re.search(REGEX_DATE, primeira_linha)
        if date_match:
            ano = date_match.group(1)
            mes = str(int(date_match.group(2)))  # Remove zero à esquerda
            dia = str(int(date_match.group(3)))  # Remove zero à esquerda
            dest_dir_ano_mes_dia = os.path.join(DEST_DIR, ano, mes, dia)
            if not os.path.exists(dest_dir_ano_mes_dia):
                os.makedirs(dest_dir_ano_mes_dia)
            dest_path = os.path.join(dest_dir_ano_mes_dia, filename)
            if arquivo_deve_ser_copiado(src_path, dest_path):
                shutil.copy2(src_path, dest_path)
                print(f"Arquivo copiado: {filename} | Data: {ano}-{mes}")
            # else:
            #     print(f"Arquivo já existe e está atualizado: {filename}")
        else:
            print(f"Data não encontrada na primeira linha de {filename}")


if __name__== "__main__":
    copiar_arquivos()
