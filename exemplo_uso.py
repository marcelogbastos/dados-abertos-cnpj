#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de Uso do CNPJ Downloader
Demonstra diferentes formas de usar o sistema
"""

import os
import sys
from cnpj_downloader import CNPJDownloader
from cnpj_manager import show_status

def exemplo_download_automatico():
    """Exemplo de download automático do mês mais recente"""
    print("=== EXEMPLO 1: DOWNLOAD AUTOMÁTICO ===")
    print("Baixando o mês mais recente disponível...")
    
    try:
        downloader = CNPJDownloader()
        downloader.run()
        print("✅ Download automático concluído!")
    except Exception as e:
        print(f"❌ Erro no download automático: {e}")

def exemplo_download_mes_especifico():
    """Exemplo de download de mês específico"""
    print("\n=== EXEMPLO 2: DOWNLOAD DE MÊS ESPECÍFICO ===")
    print("Baixando dados de janeiro de 2024...")
    
    try:
        downloader = CNPJDownloader()
        directory = "2024-01/"
        
        # Obter arquivos do diretório específico
        files = downloader.get_files_from_directory(directory)
        
        if not files:
            print("❌ Nenhum arquivo encontrado para 2024-01")
            return
        
        print(f"📁 Encontrados {len(files)} arquivos")
        
        # Download de apenas 2 arquivos para exemplo
        for i, file_info in enumerate(files[:2]):
            print(f"📥 Baixando {file_info['name']}...")
            file_path = downloader.download_file(file_info, directory)
            
            # Extrair o arquivo
            print(f"📦 Extraindo {file_info['name']}...")
            downloader.extract_file(file_path, directory)
        
        print("✅ Download de mês específico concluído!")
        
    except Exception as e:
        print(f"❌ Erro no download de mês específico: {e}")

def exemplo_verificar_status():
    """Exemplo de verificação de status"""
    print("\n=== EXEMPLO 3: VERIFICAÇÃO DE STATUS ===")
    show_status()

def exemplo_listar_diretorios():
    """Exemplo de listagem de diretórios disponíveis"""
    print("\n=== EXEMPLO 4: LISTAGEM DE DIRETÓRIOS ===")
    
    try:
        downloader = CNPJDownloader()
        response = downloader.session.get(downloader.base_url)
        response.raise_for_status()
        
        from bs4 import BeautifulSoup
        import re
        from datetime import datetime
        
        soup = BeautifulSoup(response.content, 'html.parser')
        pattern = re.compile(r'^\d{4}-\d{2}/$')
        
        directories = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and pattern.match(href):
                date_str = href.rstrip('/')
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m')
                    directories.append((date_obj, href))
                except ValueError:
                    continue
        
        directories.sort(reverse=True)
        
        print("📅 Diretórios disponíveis (últimos 10):")
        for i, (date_obj, directory) in enumerate(directories[:10]):
            print(f"   {i+1}. {directory} ({date_obj.strftime('%B %Y')})")
        
    except Exception as e:
        print(f"❌ Erro ao listar diretórios: {e}")

def exemplo_configuracao_personalizada():
    """Exemplo de configuração personalizada"""
    print("\n=== EXEMPLO 5: CONFIGURAÇÃO PERSONALIZADA ===")
    
    # Criar downloader com configurações personalizadas
    downloader = CNPJDownloader()
    
    # Modificar diretórios
    downloader.download_dir = "meus_downloads"
    downloader.extract_dir = "meus_dados"
    
    # Criar diretórios personalizados
    for directory in [downloader.download_dir, downloader.extract_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Diretório personalizado criado: {directory}")
    
    print("✅ Configuração personalizada aplicada!")

def main():
    """Função principal com menu de exemplos"""
    print("🚀 EXEMPLOS DE USO DO CNPJ DOWNLOADER\n")
    
    exemplos = [
        ("Download Automático", exemplo_download_automatico),
        ("Download de Mês Específico", exemplo_download_mes_especifico),
        ("Verificar Status", exemplo_verificar_status),
        ("Listar Diretórios", exemplo_listar_diretorios),
        ("Configuração Personalizada", exemplo_configuracao_personalizada),
    ]
    
    while True:
        print("\nEscolha um exemplo para executar:")
        for i, (nome, _) in enumerate(exemplos, 1):
            print(f"  {i}. {nome}")
        print("  0. Sair")
        
        try:
            escolha = input("\nDigite sua escolha (0-5): ").strip()
            
            if escolha == "0":
                print("👋 Saindo...")
                break
            
            escolha = int(escolha)
            if 1 <= escolha <= len(exemplos):
                nome, funcao = exemplos[escolha - 1]
                print(f"\n{'='*50}")
                print(f"Executando: {nome}")
                print('='*50)
                funcao()
                input("\nPressione Enter para continuar...")
            else:
                print("❌ Escolha inválida!")
                
        except ValueError:
            print("❌ Digite um número válido!")
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main() 