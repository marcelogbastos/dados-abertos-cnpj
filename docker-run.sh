#!/bin/bash

# Script para executar comandos do CNPJ Downloader com Docker

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Arquivo de compose
DOCKER_COMPOSE_FILE="docker-compose.yml"

# --- Funções Auxiliares ---
show_help() {
    echo -e "${BLUE}CNPJ Downloader - Docker Script${NC}"
    echo ""
    echo "Uso: $0 [COMANDO]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  build            - Constrói as imagens Docker"
    echo "  download         - Baixa e extrai os arquivos de dados"
    echo "  status           - Verifica o status dos arquivos baixados"
    echo "  import-parquet   - Converte os arquivos extraídos para Parquet"
    echo "  list [tipo]      - Lista arquivos extraídos (filtra por tipo, ex: 'empresas')"
    echo "  clean            - Limpa todos os dados (downloads, extraídos, parquet)"
    echo "  shell            - Abre um shell interativo no container principal"
    echo "  stop             - Para todos os serviços"
    echo "  all              - Executa o pipeline completo: download > import-parquet"
    echo "  help             - Mostra esta mensagem de ajuda"
}

build_images() {
    echo -e "${YELLOW}🔨 Construindo imagens Docker...${NC}"
    docker-compose -f $DOCKER_COMPOSE_FILE build
    echo -e "${GREEN}✅ Imagens construídas com sucesso!${NC}"
}

run_download() {
    echo -e "${YELLOW}📥 Baixando e extraindo dados...${NC}"
    docker-compose -f $DOCKER_COMPOSE_FILE run --rm cnpj-downloader
    echo -e "${GREEN}✅ Download e extração concluídos!${NC}"
}

run_status() {
    echo -e "${YELLOW}📊 Verificando status...${NC}"
    docker-compose -f $DOCKER_COMPOSE_FILE run --rm cnpj-manager python cnpj_manager.py status
}

import_parquet() {
    echo -e "${YELLOW}📦 Convertendo dados para Parquet...${NC}"
    # Garante que o serviço esteja de pé e com a imagem mais recente
    docker-compose -f $DOCKER_COMPOSE_FILE up --build -d cnpj-parquet
    # Executa o script de importação dentro do container que está rodando
    docker-compose -f $DOCKER_COMPOSE_FILE exec cnpj-parquet python import_to_parquet.py
    echo -e "${GREEN}✅ Conversão para Parquet concluída! Arquivos em ./parquet.${NC}"
}

run_list() {
    echo -e "${YELLOW}🔎 Listando arquivos para o tipo: $1...${NC}"
    docker-compose -f $DOCKER_COMPOSE_FILE run --rm cnpj-manager python cnpj_manager.py list "$1"
}

run_clean() {
    echo -e "${YELLOW}🗑️  Limpando todos os dados...${NC}"
    docker-compose -f $DOCKER_COMPOSE_FILE run --rm cnpj-manager python cnpj_manager.py clean-all
    # Remove também os arquivos parquet
    if [ -d "parquet" ]; then
        rm -rf parquet/*
        echo -e "${YELLOW}Diretório 'parquet' limpo.${NC}"
    fi
    echo -e "${GREEN}✅ Limpeza concluída!${NC}"
}

run_shell() {
    echo -e "${YELLOW}🐚 Abrindo shell no container 'cnpj-manager'...${NC}"
    docker-compose -f $DOCKER_COMPOSE_FILE run --rm cnpj-manager /bin/bash
}

run_stop() {
    echo -e "${YELLOW}🛑 Parando todos os serviços...${NC}"
    docker-compose -f $DOCKER_COMPOSE_FILE down
    echo -e "${GREEN}✅ Serviços parados!${NC}"
}

# --- Função Principal ---
main() {
    if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker e/ou Docker Compose não estão instalados. Por favor, instale-os para continuar.${NC}"
        exit 1
    fi

    COMMAND=$1
    shift || true # Remove o comando da lista de argumentos

    case "$COMMAND" in
        build) build_images ;;
        download) run_download ;;
        status) run_status ;;
        import-parquet) import_parquet ;;
        list)
            if [ -z "$1" ]; then
                echo -e "${RED}Erro: Especifique o tipo de arquivo para listar.${NC}"
                exit 1
            fi
            run_list "$1"
            ;;
        clean) run_clean ;;
        shell) run_shell ;;
        stop) run_stop ;;
        all)
            echo -e "${BLUE}🚀 Executando pipeline completo...${NC}"
            run_download
            import_parquet
            echo -e "${GREEN}🎉 Pipeline concluído com sucesso!${NC}"
            ;;
        help|--help|-h|"")
            show_help
            ;;
        *)
            echo -e "${RED}❌ Comando inválido: $COMMAND${NC}"
            show_help
            exit 1
            ;;
    esac
}

main "$@" 