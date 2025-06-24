# -*- coding: utf-8 -*-
"""
Script para converter os dados abertos do CNPJ (extraídos) para o formato Parquet.

Este script lê os metadados do arquivo metadata.py, processa os arquivos de texto
em lotes (chunks) para otimizar o uso de memória e os salva em formato Parquet
com compressão, ideal para análise de dados.
"""
import os
import glob
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import logging
from datetime import datetime
import pytz  # Adicionado para timezone

# Importa os metadados
from metadata import LAYOUTS, TABLE_NAMES

# --- Configurações ---
EXTRACTED_DIR = 'extracted'
PARQUET_DIR = 'parquet'
CHUNKSIZE = 100000  # Processa 100.000 linhas por vez (ajuste conforme a RAM)
LOG_DIR = 'logs'

# --- Configuração do Logging ---
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"parquet_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Remove handlers antigos para evitar logs duplicados
if logger.hasHandlers():
    logger.handlers.clear()

class SaoPauloFormatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp, pytz.timezone('America/Sao_Paulo'))
        return dt

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            s = dt.isoformat()
        return s

formatter = SaoPauloFormatter('%(asctime)s [%(levelname)s] - %(message)s')
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def process_files_to_parquet():
    """
    Lê os arquivos de texto da pasta 'extracted', converte em DataFrames
    e salva em formato Parquet, um arquivo por tipo de tabela.
    """
    logger.info("Iniciando processo de conversão para Parquet.")
    os.makedirs(PARQUET_DIR, exist_ok=True)

    if not os.path.exists(EXTRACTED_DIR):
        logger.error(f"Diretório de extração não encontrado: {EXTRACTED_DIR}")
        return

    # Itera sobre cada tipo de tabela definido nos metadados
    for table_name in LAYOUTS.keys():
        logger.info(f"--- Processando tabela: {table_name} ---")

        type_key = next((k for k, v in TABLE_NAMES.items() if v == table_name), None)
        if not type_key:
            logger.warning(f"Nenhuma chave de tipo de arquivo encontrada para a tabela {table_name}. Pulando.")
            continue

        search_pattern = os.path.join(EXTRACTED_DIR, '**', f'*{type_key}*')
        files_to_process = glob.glob(search_pattern, recursive=True)

        if not files_to_process:
            logger.warning(f"Nenhum arquivo encontrado para a tabela '{table_name}'. Pulando.")
            continue

        logger.info(f"Encontrados {len(files_to_process)} arquivo(s) para '{table_name}'.")

        parquet_path = os.path.join(PARQUET_DIR, f'{table_name}.parquet')
        
        # Define o schema do PyArrow com todas as colunas como string
        try:
            pa_schema = pa.schema([(col, pa.string()) for col in LAYOUTS[table_name]])
        except KeyError:
            logger.warning(f"Layout para a tabela '{table_name}' não encontrado. Pulando.")
            continue
            
        parquet_writer = None
        total_rows = 0

        try:
            # Abre o ParquetWriter uma vez por tabela
            parquet_writer = pq.ParquetWriter(parquet_path, pa_schema, compression='snappy')

            for file_path in files_to_process:
                logger.info(f"Lendo arquivo: {os.path.basename(file_path)}")
                
                reader = pd.read_csv(
                    file_path,
                    sep=';',
                    header=None,
                    names=LAYOUTS[table_name],
                    dtype=str,
                    encoding='latin-1',
                    chunksize=CHUNKSIZE,
                    keep_default_na=False,
                    na_values=['']
                )

                for i, chunk in enumerate(reader):
                    logger.info(f"- {table_name} - Processando lote {i+1} ({len(chunk)} linhas)")
                    total_rows += len(chunk)
                    
                    # Converte o chunk do pandas para uma Tabela do Arrow e escreve no arquivo
                    table = pa.Table.from_pandas(chunk, schema=pa_schema, preserve_index=False)
                    parquet_writer.write_table(table)
            
            if total_rows > 0:
                logger.info(f"Arquivo Parquet '{parquet_path}' criado com sucesso.")
                logger.info(f"Total de {total_rows} linhas processadas para a tabela '{table_name}'.")

        except Exception as e:
            logger.error(f"Erro ao processar a tabela '{table_name}': {e}", exc_info=True)
        finally:
            # Garante que o writer seja fechado
            if parquet_writer:
                parquet_writer.close()

    logger.info("--- Processo de conversão para Parquet concluído. ---")

if __name__ == "__main__":
    try:
        process_files_to_parquet()
    except Exception as e:
        logger.critical(f"Ocorreu um erro fatal no script: {e}", exc_info=True) 