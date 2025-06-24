#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNPJ Manager
Script de gerenciamento para downloads de dados CNPJ
"""

import os
import sys
import argparse
import json
from datetime import datetime
from cnpj_downloader import CNPJDownloader
from metadata import TABLE_NAMES  # Importa os nomes das tabelas

# Diretórios padrão
DOWNLOAD_DIR = "downloads"
EXTRACT_DIR = "extracted"
LOG_FILE = "cnpj_downloader.log"

def get_directory_size(directory):
    """Calcula o tamanho total de um diretório"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def format_size(size_bytes):
    """Formata tamanho em bytes para formato legível"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def show_status():
    """Mostra o status dos downloads e extrações"""
    print("=== STATUS DOS DADOS CNPJ ===\n")
    
    # Verificar diretório de downloads
    if os.path.exists(DOWNLOAD_DIR):
        print(f"📁 Diretório de Downloads: {DOWNLOAD_DIR}")
        download_size = get_directory_size(DOWNLOAD_DIR)
        print(f"   Tamanho total: {format_size(download_size)}")
        
        # Listar subdiretórios (meses)
        for item in sorted(os.listdir(DOWNLOAD_DIR)):
            item_path = os.path.join(DOWNLOAD_DIR, item)
            if os.path.isdir(item_path):
                item_size = get_directory_size(item_path)
                file_count = len([f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))])
                print(f"   └── {item}: {file_count} arquivos, {format_size(item_size)}")
    else:
        print(f"❌ Diretório de Downloads não encontrado: {DOWNLOAD_DIR}")
    
    print()
    
    # Verificar diretório de extração
    if os.path.exists(EXTRACT_DIR):
        print(f"📁 Diretório de Extração: {EXTRACT_DIR}")
        extract_size = get_directory_size(EXTRACT_DIR)
        print(f"   Tamanho total: {format_size(extract_size)}")
        
        # Listar subdiretórios (meses) e tipos de arquivo
        for month_dir in sorted(os.listdir(EXTRACT_DIR)):
            month_path = os.path.join(EXTRACT_DIR, month_dir)
            if os.path.isdir(month_path):
                item_size = get_directory_size(month_path)
                file_count = len([f for f in os.listdir(month_path) if os.path.isfile(os.path.join(month_path, f))])
                print(f"   └── {month_dir}: {file_count} arquivos, {format_size(item_size)}")
                
                # Contar arquivos por tipo (usando TABLE_NAMES)
                file_types = {}
                for f in os.listdir(month_path):
                    for type_key in TABLE_NAMES.keys():
                        if type_key in f.upper():
                            file_types[type_key] = file_types.get(type_key, 0) + 1
                
                for type_name, count in sorted(file_types.items()):
                    print(f"       ├── {TABLE_NAMES[type_name]}: {count} arquivo(s)")

    else:
        print(f"❌ Diretório de Extração não encontrado: {EXTRACT_DIR}")
    
    print()
    
    # Verificar log
    if os.path.exists(LOG_FILE):
        log_size = os.path.getsize(LOG_FILE)
        print(f"📄 Arquivo de Log: {LOG_FILE} ({format_size(log_size)})")
    else:
        print(f"❌ Arquivo de Log não encontrado: {LOG_FILE}")

def clean_downloads():
    """Remove arquivos baixados"""
    if os.path.exists(DOWNLOAD_DIR):
        import shutil
        shutil.rmtree(DOWNLOAD_DIR)
        print(f"🗑️  Diretório de downloads removido: {DOWNLOAD_DIR}")
    else:
        print(f"❌ Diretório de downloads não encontrado: {DOWNLOAD_DIR}")

def clean_extracted():
    """Remove arquivos extraídos"""
    if os.path.exists(EXTRACT_DIR):
        import shutil
        shutil.rmtree(EXTRACT_DIR)
        print(f"🗑️  Diretório de extração removido: {EXTRACT_DIR}")
    else:
        print(f"❌ Diretório de extração não encontrado: {EXTRACT_DIR}")

def download_specific_month(year_month):
    """Download de um mês específico (formato: YYYY-MM)"""
    try:
        # Validar formato
        datetime.strptime(year_month, '%Y-%m')
        
        downloader = CNPJDownloader()
        
        # Modificar para baixar mês específico
        directory = f"{year_month}/"
        
        print(f"📥 Baixando dados do mês: {year_month}")
        
        # Obter arquivos do diretório específico
        files = downloader.get_files_from_directory(directory)
        
        if not files:
            print(f"❌ Nenhum arquivo encontrado para {year_month}")
            return
        
        # Download dos arquivos
        downloaded_files = []
        for file_info in files:
            try:
                file_path = downloader.download_file(file_info, directory)
                downloaded_files.append(file_path)
            except Exception as e:
                print(f"❌ Erro no download de {file_info['name']}: {e}")
                continue
        
        # Extração dos arquivos
        print("📦 Extraindo arquivos...")
        for file_path in downloaded_files:
            try:
                downloader.extract_file(file_path, directory)
            except Exception as e:
                print(f"❌ Erro na extração de {file_path}: {e}")
                continue
        
        print(f"✅ Download e extração concluídos para {year_month}")
        
    except ValueError:
        print("❌ Formato inválido. Use YYYY-MM (exemplo: 2024-01)")
    except Exception as e:
        print(f"❌ Erro: {e}")

def list_files(file_type=None):
    """Lista arquivos extraídos, opcionalmente filtrando por tipo"""
    if not os.path.exists(EXTRACT_DIR):
        print(f"❌ Diretório de extração não encontrado: {EXTRACT_DIR}")
        return
        
    print(f"📂 Listando arquivos em {EXTRACT_DIR}:\n")

    all_files = []
    for root, _, files in os.walk(EXTRACT_DIR):
        for name in files:
            all_files.append(os.path.join(root, name))
    
    if file_type:
        # Normalizar tipo para busca
        type_key_to_find = None
        for key, value in TABLE_NAMES.items():
            if file_type.lower() == value.lower():
                type_key_to_find = key
                break
        
        if not type_key_to_find:
            print(f"❌ Tipo de arquivo inválido: {file_type}")
            print(f"   Tipos válidos: {', '.join(sorted(TABLE_NAMES.values()))}")
            return
            
        filtered_files = [f for f in all_files if type_key_to_find in os.path.basename(f).upper()]
        
        if not filtered_files:
            print(f"Nenhum arquivo encontrado para o tipo: {file_type}")
        else:
            for f in sorted(filtered_files):
                print(f"- {f}")
    else:
        if not all_files:
            print("Nenhum arquivo extraído encontrado.")
        else:
            for f in sorted(all_files):
                print(f"- {f}")

def main():
    """Função principal para gerenciar os dados"""
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    if command == "status":
        show_status()
    elif command == "clean-all":
        clean_downloads()
        clean_extracted()
    elif command == "clean-downloads":
        clean_downloads()
    elif command == "clean-extracted":
        clean_extracted()
    elif command == "download" and len(sys.argv) > 2:
        download_specific_month(sys.argv[2])
    elif command == "list":
        file_type = sys.argv[2] if len(sys.argv) > 2 else None
        list_files(file_type)
    else:
        show_help()

def show_help():
    """Mostra a ajuda do script"""
    print("Uso: python cnpj_manager.py <comando> [argumento]")
    print("\nComandos disponíveis:")
    print("  status               - Mostra o status dos downloads e extrações")
    print("  clean-all            - Remove os diretórios 'downloads' e 'extracted'")
    print("  clean-downloads      - Remove o diretório 'downloads'")
    print("  clean-extracted      - Remove o diretório 'extracted'")
    print("  download <YYYY-MM>   - Baixa e extrai dados de um mês específico")
    print("  list [tipo]          - Lista arquivos extraídos (filtra por tipo, ex: 'empresas')")
    print("  help                 - Mostra esta ajuda")

if __name__ == "__main__":
    main() 