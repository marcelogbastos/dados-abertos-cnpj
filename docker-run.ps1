# Script para executar comandos do CNPJ Downloader com Docker

# --- Configuração ---
$DockerComposeFile = "docker-compose.yml"

# --- Funções Auxiliares ---
function Show-Help {
    Write-Host "CNPJ Downloader - Docker Script" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Uso: .\\docker-run.ps1 [COMANDO]"
    Write-Host ""
    Write-Host "Comandos disponíveis:"
    Write-Host "  build            - Constrói as imagens Docker"
    Write-Host "  download         - Baixa e extrai os arquivos de dados"
    Write-Host "  status           - Verifica o status dos arquivos baixados"
    Write-Host "  import-parquet   - Converte os arquivos extraídos para Parquet"
    Write-Host "  list [tipo]      - Lista arquivos extraídos (filtra por tipo, ex: 'empresas')"
    Write-Host "  clean            - Limpa todos os dados (downloads, extraídos, parquet)"
    Write-Host "  shell            - Abre um shell interativo no container principal"
    Write-Host "  stop             - Para todos os serviços"
    Write-Host "  all              - Executa o pipeline completo: download > import-parquet"
    Write-Host "  help             - Mostra esta mensagem de ajuda"
}

function Build-Images {
    Write-Host "🔨 Construindo imagens Docker..." -ForegroundColor Yellow
    docker-compose -f $DockerComposeFile build
    Write-Host "✅ Imagens construídas com sucesso!" -ForegroundColor Green
}

function Run-Download {
    Write-Host "📥 Baixando e extraindo dados..." -ForegroundColor Yellow
    docker-compose -f $DockerComposeFile run --rm cnpj-downloader
    Write-Host "✅ Download e extração concluídos!" -ForegroundColor Green
}

function Run-Status {
    Write-Host "📊 Verificando status..." -ForegroundColor Yellow
    docker-compose -f $DockerComposeFile run --rm cnpj-manager python cnpj_manager.py status
}

function Import-Parquet {
    Write-Host "📦 Convertendo dados para Parquet..." -ForegroundColor Yellow
    # Garante que o serviço esteja de pé e com a imagem mais recente
    docker-compose -f $DockerComposeFile up --build -d cnpj-parquet
    # Executa o script de importação dentro do container que está rodando
    docker-compose -f $DockerComposeFile exec cnpj-parquet python import_to_parquet.py
    Write-Host "✅ Conversão para Parquet concluída! Arquivos em ./parquet." -ForegroundColor Green
}

function Run-List ($type) {
    Write-Host "🔎 Listando arquivos para o tipo: $type..." -ForegroundColor Yellow
    docker-compose -f $DockerComposeFile run --rm cnpj-manager python cnpj_manager.py list "$type"
}

function Run-Clean {
    Write-Host "🗑️  Limpando todos os dados..." -ForegroundColor Yellow
    docker-compose -f $DockerComposeFile run --rm cnpj-manager python cnpj_manager.py clean-all
    if (Test-Path -Path "parquet") {
        Remove-Item -Recurse -Force parquet/*
        Write-Host "Diretório 'parquet' limpo." -ForegroundColor Yellow
    }
    Write-Host "✅ Limpeza concluída!" -ForegroundColor Green
}

function Run-Shell {
    Write-Host "🐚 Abrindo shell no container 'cnpj-manager'..." -ForegroundColor Yellow
    docker-compose -f $DockerComposeFile run --rm cnpj-manager /bin/bash
}

function Run-Stop {
    Write-Host "🛑 Parando todos os serviços..." -ForegroundColor Yellow
    docker-compose -f $DockerComposeFile down
    Write-Host "✅ Serviços parados!" -ForegroundColor Green
}

# --- Função Principal ---
function Main {
    param($Command, $Args)

    if (-not (Get-Command docker -ErrorAction SilentlyContinue) -or -not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Docker e/ou Docker Compose não estão instalados. Por favor, instale-os para continuar." -ForegroundColor Red
        exit 1
    }

    switch ($Command) {
        "build"          { Build-Images }
        "download"       { Run-Download }
        "status"         { Run-Status }
        "import-parquet" { Import-Parquet }
        "list"           {
            if ($Args.Count -eq 0) {
                Write-Host "Erro: Especifique o tipo de arquivo para listar." -ForegroundColor Red
                exit 1
            }
            Run-List $Args[0]
        }
        "clean"          { Run-Clean }
        "shell"          { Run-Shell }
        "stop"           { Run-Stop }
        "all"            {
            Write-Host "🚀 Executando pipeline completo..." -ForegroundColor Blue
            Run-Download
            Import-Parquet
            Write-Host "🎉 Pipeline concluído com sucesso!" -ForegroundColor Green
        }
        default {
            if ($null -eq $Command -or "" -eq $Command -or "help" -eq $command) {
                Show-Help
            } else {
                Write-Host "❌ Comando inválido: $Command" -ForegroundColor Red
                Show-Help
                exit 1
            }
        }
    }
}

# Executa a função principal, passando os argumentos do script
Main $args[0] $args[1..($args.Length-1)] 