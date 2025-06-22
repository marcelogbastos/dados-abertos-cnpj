#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNPJ Data Downloader
Web scraper para baixar dados abertos do CNPJ da Receita Federal
"""

import os
import re
import requests
import zipfile
import logging
from datetime import datetime
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cnpj_downloader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CNPJDownloader:
    def __init__(self, base_url="https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Criar diretórios se não existirem
        self.download_dir = "downloads"
        self.extract_dir = "extracted"
        self._create_directories()
    
    def _create_directories(self):
        """Cria os diretórios necessários"""
        for directory in [self.download_dir, self.extract_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"Diretório criado: {directory}")
    
    def get_latest_directory(self):
        """Obtém o diretório mais recente (yyyy-mm) da página"""
        try:
            logger.info("Obtendo lista de diretórios...")
            response = self.session.get(self.base_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Padrão para diretórios yyyy-mm
            pattern = re.compile(r'^\d{4}-\d{2}/$')
            
            directories = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and pattern.match(href):
                    # Extrair a data do diretório
                    date_str = href.rstrip('/')
                    try:
                        date_obj = datetime.strptime(date_str, '%Y-%m')
                        directories.append((date_obj, href))
                    except ValueError:
                        continue
            
            if not directories:
                raise Exception("Nenhum diretório válido encontrado")
            
            # Ordenar por data e pegar o mais recente
            directories.sort(reverse=True)
            latest_dir = directories[0][1]
            
            logger.info(f"Diretório mais recente encontrado: {latest_dir}")
            return latest_dir
            
        except Exception as e:
            logger.error(f"Erro ao obter diretório mais recente: {e}")
            raise
    
    def get_files_from_directory(self, directory):
        """Obtém lista de arquivos de um diretório específico"""
        try:
            url = urljoin(self.base_url, directory)
            logger.info(f"Obtendo arquivos do diretório: {url}")
            
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            files = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and not href.endswith('/') and not href.startswith('?'):
                    # Verificar se é um arquivo (não é diretório)
                    file_url = urljoin(url, href)
                    files.append({
                        'name': href,
                        'url': file_url
                    })
            
            logger.info(f"Encontrados {len(files)} arquivos no diretório")
            return files
            
        except Exception as e:
            logger.error(f"Erro ao obter arquivos do diretório: {e}")
            raise
    
    def download_file(self, file_info, directory_name):
        """Download de um arquivo específico"""
        try:
            file_name = file_info['name']
            file_url = file_info['url']
            
            # Criar subdiretório para o mês
            month_dir = os.path.join(self.download_dir, directory_name.rstrip('/'))
            if not os.path.exists(month_dir):
                os.makedirs(month_dir)
            
            file_path = os.path.join(month_dir, file_name)
            
            # Verificar se arquivo já existe
            if os.path.exists(file_path):
                logger.info(f"Arquivo já existe, pulando: {file_name}")
                return file_path
            
            logger.info(f"Baixando: {file_name}")
            
            # Download com barra de progresso
            response = self.session.get(file_url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(file_path, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=file_name) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            
            logger.info(f"Download concluído: {file_name}")
            return file_path
            
        except Exception as e:
            logger.error(f"Erro ao baixar arquivo {file_name}: {e}")
            raise
    
    def extract_file(self, file_path, directory_name):
        """Extrai um arquivo compactado"""
        try:
            if not file_path.endswith('.zip'):
                logger.info(f"Arquivo não é ZIP, pulando extração: {file_path}")
                return
            
            # Criar diretório de extração
            extract_month_dir = os.path.join(self.extract_dir, directory_name.rstrip('/'))
            if not os.path.exists(extract_month_dir):
                os.makedirs(extract_month_dir)
            
            file_name = os.path.basename(file_path)
            logger.info(f"Extraindo: {file_name}")
            
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Listar conteúdo antes de extrair
                file_list = zip_ref.namelist()
                logger.info(f"Arquivo contém {len(file_list)} itens")
                
                # Extrair com barra de progresso
                for file_info in tqdm(zip_ref.infolist(), desc=f"Extraindo {file_name}"):
                    zip_ref.extract(file_info, extract_month_dir)
            
            logger.info(f"Extração concluída: {file_name}")
            
        except Exception as e:
            logger.error(f"Erro ao extrair arquivo {file_path}: {e}")
            raise
    
    def run(self):
        """Executa o processo completo de download e extração"""
        try:
            logger.info("Iniciando processo de download dos dados CNPJ")
            
            # 1. Obter diretório mais recente
            latest_directory = self.get_latest_directory()
            
            # 2. Obter lista de arquivos
            files = self.get_files_from_directory(latest_directory)
            
            if not files:
                logger.warning("Nenhum arquivo encontrado para download")
                return
            
            # 3. Download dos arquivos
            downloaded_files = []
            for file_info in files:
                try:
                    file_path = self.download_file(file_info, latest_directory)
                    downloaded_files.append(file_path)
                    # Pequena pausa para não sobrecarregar o servidor
                    time.sleep(1)
                except Exception as e:
                    logger.error(f"Falha no download de {file_info['name']}: {e}")
                    continue
            
            # 4. Extração dos arquivos
            logger.info("Iniciando extração dos arquivos...")
            for file_path in downloaded_files:
                try:
                    self.extract_file(file_path, latest_directory)
                except Exception as e:
                    logger.error(f"Falha na extração de {file_path}: {e}")
                    continue
            
            logger.info("Processo concluído com sucesso!")
            logger.info(f"Arquivos baixados: {len(downloaded_files)}")
            logger.info(f"Diretório de downloads: {self.download_dir}")
            logger.info(f"Diretório de extração: {self.extract_dir}")
            
        except Exception as e:
            logger.error(f"Erro durante execução: {e}")
            raise

def main():
    """Função principal"""
    try:
        downloader = CNPJDownloader()
        downloader.run()
    except KeyboardInterrupt:
        logger.info("Processo interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 