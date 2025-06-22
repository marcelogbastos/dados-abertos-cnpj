#!/bin/bash

# Script para executar comandos do CNPJ Downloader com Docker

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para mostrar ajuda
show_help() {
    echo -e "${BLUE}CNPJ Downloader - Docker Script${NC}"
    echo ""
    echo "Uso: $0 [COMANDO] [OPÇÕES]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  build           - Construir a imagem Docker"
    echo "  download        - Executar download automático"
    echo "  download-month  - Download de mês específico (ex: $0 download-month 2024-01)"
    echo "  status          - Verificar status dos downloads"
    echo "  test            - Executar testes"
    echo "  clean-downloads - Limpar arquivos baixados"
    echo "  clean-extracted - Limpar arquivos extraídos"
    echo "  clean-all       - Limpar todos os arquivos"
    echo "  shell           - Abrir shell no container"
    echo "  logs            - Ver logs do container"
    echo "  stop            - Parar containers"
    echo "  help            - Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 build"
    echo "  $0 download"
    echo "  $0 download-month 2024-01"
    echo "  $0 status"
    echo "  $0 test"
}

# Função para construir imagem
build_image() {
    echo -e "${YELLOW}🔨 Construindo imagem Docker...${NC}"
    docker-compose build
    echo -e "${GREEN}✅ Imagem construída com sucesso!${NC}"
}

# Função para executar download
run_download() {
    echo -e "${YELLOW}📥 Iniciando download automático...${NC}"
    docker-compose run --rm cnpj-downloader python cnpj_downloader.py
}

# Função para download de mês específico
run_download_month() {
    if [ -z "$1" ]; then
        echo -e "${RED}❌ Erro: Especifique o mês (formato: YYYY-MM)${NC}"
        echo "Exemplo: $0 download-month 2024-01"
        exit 1
    fi
    echo -e "${YELLOW}📥 Baixando dados do mês: $1${NC}"
    docker-compose run --rm cnpj-downloader python cnpj_manager.py download-month --month "$1"
}

# Função para verificar status
run_status() {
    echo -e "${YELLOW}📊 Verificando status...${NC}"
    docker-compose run --rm cnpj-manager python cnpj_manager.py status
}

# Função para executar testes
run_test() {
    echo -e "${YELLOW}🧪 Executando testes...${NC}"
    docker-compose run --rm cnpj-test python test_downloader.py
}

# Função para limpeza
run_clean() {
    case "$1" in
        "downloads")
            echo -e "${YELLOW}🗑️  Limpando downloads...${NC}"
            docker-compose run --rm cnpj-manager python cnpj_manager.py clean-downloads
            ;;
        "extracted")
            echo -e "${YELLOW}🗑️  Limpando arquivos extraídos...${NC}"
            docker-compose run --rm cnpj-manager python cnpj_manager.py clean-extracted
            ;;
        "all")
            echo -e "${YELLOW}🗑️  Limpando todos os arquivos...${NC}"
            docker-compose run --rm cnpj-manager python cnpj_manager.py clean-all
            ;;
        *)
            echo -e "${RED}❌ Opção de limpeza inválida${NC}"
            exit 1
            ;;
    esac
}

# Função para abrir shell
run_shell() {
    echo -e "${YELLOW}🐚 Abrindo shell no container...${NC}"
    docker-compose run --rm cnpj-downloader /bin/bash
}

# Função para ver logs
run_logs() {
    echo -e "${YELLOW}📄 Mostrando logs...${NC}"
    docker-compose logs cnpj-downloader
}

# Função para parar containers
run_stop() {
    echo -e "${YELLOW}🛑 Parando containers...${NC}"
    docker-compose down
    echo -e "${GREEN}✅ Containers parados!${NC}"
}

# Verificar se Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker não está instalado!${NC}"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Compose não está instalado!${NC}"
        exit 1
    fi
}

# Função principal
main() {
    check_docker
    
    case "$1" in
        "build")
            build_image
            ;;
        "download")
            run_download
            ;;
        "download-month")
            run_download_month "$2"
            ;;
        "status")
            run_status
            ;;
        "test")
            run_test
            ;;
        "clean-downloads")
            run_clean "downloads"
            ;;
        "clean-extracted")
            run_clean "extracted"
            ;;
        "clean-all")
            run_clean "all"
            ;;
        "shell")
            run_shell
            ;;
        "logs")
            run_logs
            ;;
        "stop")
            run_stop
            ;;
        "help"|"-h"|"--help"|"")
            show_help
            ;;
        *)
            echo -e "${RED}❌ Comando inválido: $1${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Executar função principal
main "$@" 