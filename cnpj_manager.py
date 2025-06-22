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
    
    download_dir = "downloads"
    extract_dir = "extracted"
    
    # Verificar diretório de downloads
    if os.path.exists(download_dir):
        print(f"📁 Diretório de Downloads: {download_dir}")
        download_size = get_directory_size(download_dir)
        print(f"   Tamanho total: {format_size(download_size)}")
        
        # Listar subdiretórios (meses)
        for item in os.listdir(download_dir):
            item_path = os.path.join(download_dir, item)
            if os.path.isdir(item_path):
                item_size = get_directory_size(item_path)
                file_count = len([f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))])
                print(f"   └── {item}: {file_count} arquivos, {format_size(item_size)}")
    else:
        print(f"❌ Diretório de Downloads não encontrado: {download_dir}")
    
    print()
    
    # Verificar diretório de extração
    if os.path.exists(extract_dir):
        print(f"📁 Diretório de Extração: {extract_dir}")
        extract_size = get_directory_size(extract_dir)
        print(f"   Tamanho total: {format_size(extract_size)}")
        
        # Listar subdiretórios (meses)
        for item in os.listdir(extract_dir):
            item_path = os.path.join(extract_dir, item)
            if os.path.isdir(item_path):
                item_size = get_directory_size(item_path)
                file_count = len([f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))])
                print(f"   └── {item}: {file_count} arquivos, {format_size(item_size)}")
    else:
        print(f"❌ Diretório de Extração não encontrado: {extract_dir}")
    
    print()
    
    # Verificar log
    log_file = "cnpj_downloader.log"
    if os.path.exists(log_file):
        log_size = os.path.getsize(log_file)
        print(f"📄 Arquivo de Log: {log_file} ({format_size(log_size)})")
    else:
        print(f"❌ Arquivo de Log não encontrado: {log_file}")

def clean_downloads():
    """Remove arquivos baixados (mantém apenas extraídos)"""
    download_dir = "downloads"
    if os.path.exists(download_dir):
        import shutil
        shutil.rmtree(download_dir)
        print(f"🗑️  Diretório de downloads removido: {download_dir}")
    else:
        print(f"❌ Diretório de downloads não encontrado: {download_dir}")

def clean_extracted():
    """Remove arquivos extraídos"""
    extract_dir = "extracted"
    if os.path.exists(extract_dir):
        import shutil
        shutil.rmtree(extract_dir)
        print(f"🗑️  Diretório de extração removido: {extract_dir}")
    else:
        print(f"❌ Diretório de extração não encontrado: {extract_dir}")

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

def main():
    parser = argparse.ArgumentParser(description="Gerenciador de Downloads CNPJ")
    parser.add_argument('action', choices=['status', 'download', 'download-month', 'clean-downloads', 'clean-extracted', 'clean-all'],
                       help='Ação a ser executada')
    parser.add_argument('--month', type=str, help='Mês específico para download (formato: YYYY-MM)')
    
    args = parser.parse_args()
    
    if args.action == 'status':
        show_status()
    
    elif args.action == 'download':
        print("🚀 Iniciando download do mês mais recente...")
        downloader = CNPJDownloader()
        downloader.run()
    
    elif args.action == 'download-month':
        if not args.month:
            print("❌ Especifique o mês com --month (formato: YYYY-MM)")
            return
        download_specific_month(args.month)
    
    elif args.action == 'clean-downloads':
        response = input("⚠️  Tem certeza que deseja remover todos os downloads? (y/N): ")
        if response.lower() == 'y':
            clean_downloads()
        else:
            print("❌ Operação cancelada")
    
    elif args.action == 'clean-extracted':
        response = input("⚠️  Tem certeza que deseja remover todos os arquivos extraídos? (y/N): ")
        if response.lower() == 'y':
            clean_extracted()
        else:
            print("❌ Operação cancelada")
    
    elif args.action == 'clean-all':
        response = input("⚠️  Tem certeza que deseja remover TODOS os arquivos? (y/N): ")
        if response.lower() == 'y':
            clean_downloads()
            clean_extracted()
        else:
            print("❌ Operação cancelada")

if __name__ == "__main__":
    main() 