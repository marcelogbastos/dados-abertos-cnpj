#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do CNPJ Downloader
Script para testar a funcionalidade básica
"""

import sys
import os
from cnpj_downloader import CNPJDownloader

def test_connection():
    """Testa a conexão com o servidor"""
    print("🔍 Testando conexão com o servidor...")
    
    try:
        downloader = CNPJDownloader()
        response = downloader.session.get(downloader.base_url)
        response.raise_for_status()
        print("✅ Conexão estabelecida com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def test_directory_detection():
    """Testa a detecção de diretórios"""
    print("\n📁 Testando detecção de diretórios...")
    
    try:
        downloader = CNPJDownloader()
        latest_dir = downloader.get_latest_directory()
        print(f"✅ Diretório mais recente detectado: {latest_dir}")
        return True
    except Exception as e:
        print(f"❌ Erro na detecção de diretórios: {e}")
        return False

def test_file_listing():
    """Testa a listagem de arquivos"""
    print("\n📄 Testando listagem de arquivos...")
    
    try:
        downloader = CNPJDownloader()
        latest_dir = downloader.get_latest_directory()
        files = downloader.get_files_from_directory(latest_dir)
        
        if files:
            print(f"✅ {len(files)} arquivos encontrados no diretório {latest_dir}")
            print("   Primeiros 3 arquivos:")
            for i, file_info in enumerate(files[:3]):
                print(f"   {i+1}. {file_info['name']}")
            return True
        else:
            print("⚠️  Nenhum arquivo encontrado")
            return False
    except Exception as e:
        print(f"❌ Erro na listagem de arquivos: {e}")
        return False

def test_directories_creation():
    """Testa a criação de diretórios"""
    print("\n📂 Testando criação de diretórios...")
    
    try:
        downloader = CNPJDownloader()
        downloader._create_directories()
        
        if os.path.exists(downloader.download_dir):
            print(f"✅ Diretório de downloads criado: {downloader.download_dir}")
        else:
            print(f"❌ Falha na criação do diretório: {downloader.download_dir}")
            return False
            
        if os.path.exists(downloader.extract_dir):
            print(f"✅ Diretório de extração criado: {downloader.extract_dir}")
        else:
            print(f"❌ Falha na criação do diretório: {downloader.extract_dir}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Erro na criação de diretórios: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🧪 INICIANDO TESTES DO CNPJ DOWNLOADER\n")
    
    tests = [
        ("Conexão", test_connection),
        ("Criação de Diretórios", test_directories_creation),
        ("Detecção de Diretórios", test_directory_detection),
        ("Listagem de Arquivos", test_file_listing),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"--- Teste: {test_name} ---")
        if test_func():
            passed += 1
        print()
    
    print("📊 RESULTADO DOS TESTES")
    print(f"✅ Testes aprovados: {passed}/{total}")
    print(f"❌ Testes falharam: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram! O sistema está funcionando corretamente.")
        print("💡 Você pode agora executar: python cnpj_downloader.py")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique sua conexão com a internet.")
        print("💡 Verifique se você tem acesso à URL da Receita Federal.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 