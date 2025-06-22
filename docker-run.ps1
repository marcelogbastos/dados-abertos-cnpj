# Script PowerShell para executar comandos do CNPJ Downloader com Docker

param(
    [Parameter(Position=0)]
    [string]$Command,
    
    [Parameter(Position=1)]
    [string]$Month
)

# Função para mostrar ajuda
function Show-Help {
    Write-Host "CNPJ Downloader - Docker Script (PowerShell)" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Uso: .\docker-run.ps1 [COMANDO] [OPÇÕES]"
    Write-Host ""
    Write-Host "Comandos disponíveis:"
    Write-Host "  build           - Construir a imagem Docker"
    Write-Host "  download        - Executar download automático"
    Write-Host "  download-month  - Download de mês específico (ex: .\docker-run.ps1 download-month 2024-01)"
    Write-Host "  status          - Verificar status dos downloads"
    Write-Host "  test            - Executar testes"
    Write-Host "  clean-downloads - Limpar arquivos baixados"
    Write-Host "  clean-extracted - Limpar arquivos extraídos"
    Write-Host "  clean-all       - Limpar todos os arquivos"
    Write-Host "  shell           - Abrir shell no container"
    Write-Host "  logs            - Ver logs do container"
    Write-Host "  stop            - Parar containers"
    Write-Host "  help            - Mostrar esta ajuda"
    Write-Host ""
    Write-Host "Exemplos:"
    Write-Host "  .\docker-run.ps1 build"
    Write-Host "  .\docker-run.ps1 download"
    Write-Host "  .\docker-run.ps1 download-month 2024-01"
    Write-Host "  .\docker-run.ps1 status"
    Write-Host "  .\docker-run.ps1 test"
}

# Função para construir imagem
function Build-Image {
    Write-Host "🔨 Construindo imagem Docker..." -ForegroundColor Yellow
    docker-compose build
    Write-Host "✅ Imagem construída com sucesso!" -ForegroundColor Green
}

# Função para executar download
function Run-Download {
    Write-Host "📥 Iniciando download automático..." -ForegroundColor Yellow
    docker-compose run --rm cnpj-downloader python cnpj_downloader.py
}

# Função para download de mês específico
function Run-DownloadMonth {
    param([string]$Month)
    
    if ([string]::IsNullOrEmpty($Month)) {
        Write-Host "❌ Erro: Especifique o mês (formato: YYYY-MM)" -ForegroundColor Red
        Write-Host "Exemplo: .\docker-run.ps1 download-month 2024-01"
        exit 1
    }
    
    Write-Host "📥 Baixando dados do mês: $Month" -ForegroundColor Yellow
    docker-compose run --rm cnpj-downloader python cnpj_manager.py download-month --month $Month
}

# Função para verificar status
function Run-Status {
    Write-Host "📊 Verificando status..." -ForegroundColor Yellow
    docker-compose run --rm cnpj-manager python cnpj_manager.py status
}

# Função para executar testes
function Run-Test {
    Write-Host "🧪 Executando testes..." -ForegroundColor Yellow
    docker-compose run --rm cnpj-test python test_downloader.py
}

# Função para limpeza
function Run-Clean {
    param([string]$Type)
    
    switch ($Type) {
        "downloads" {
            Write-Host "🗑️  Limpando downloads..." -ForegroundColor Yellow
            docker-compose run --rm cnpj-manager python cnpj_manager.py clean-downloads
        }
        "extracted" {
            Write-Host "🗑️  Limpando arquivos extraídos..." -ForegroundColor Yellow
            docker-compose run --rm cnpj-manager python cnpj_manager.py clean-extracted
        }
        "all" {
            Write-Host "🗑️  Limpando todos os arquivos..." -ForegroundColor Yellow
            docker-compose run --rm cnpj-manager python cnpj_manager.py clean-all
        }
        default {
            Write-Host "❌ Opção de limpeza inválida" -ForegroundColor Red
            exit 1
        }
    }
}

# Função para abrir shell
function Run-Shell {
    Write-Host "🐚 Abrindo shell no container..." -ForegroundColor Yellow
    docker-compose run --rm cnpj-downloader /bin/bash
}

# Função para ver logs
function Run-Logs {
    Write-Host "📄 Mostrando logs..." -ForegroundColor Yellow
    docker-compose logs cnpj-downloader
}

# Função para parar containers
function Run-Stop {
    Write-Host "🛑 Parando containers..." -ForegroundColor Yellow
    docker-compose down
    Write-Host "✅ Containers parados!" -ForegroundColor Green
}

# Verificar se Docker está instalado
function Test-Docker {
    try {
        $null = Get-Command docker -ErrorAction Stop
        $null = Get-Command docker-compose -ErrorAction Stop
    }
    catch {
        Write-Host "❌ Docker ou Docker Compose não está instalado!" -ForegroundColor Red
        exit 1
    }
}

# Função principal
function Main {
    Test-Docker
    
    switch ($Command) {
        "build" { Build-Image }
        "download" { Run-Download }
        "download-month" { Run-DownloadMonth $Month }
        "status" { Run-Status }
        "test" { Run-Test }
        "clean-downloads" { Run-Clean "downloads" }
        "clean-extracted" { Run-Clean "extracted" }
        "clean-all" { Run-Clean "all" }
        "shell" { Run-Shell }
        "logs" { Run-Logs }
        "stop" { Run-Stop }
        { $_ -in @("help", "-h", "--help") -or [string]::IsNullOrEmpty($_) } { Show-Help }
        default {
            Write-Host "❌ Comando inválido: $Command" -ForegroundColor Red
            Write-Host ""
            Show-Help
            exit 1
        }
    }
}

# Executar função principal
Main 