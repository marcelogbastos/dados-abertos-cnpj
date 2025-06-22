# CNPJ Data Downloader

Aplicativo Python para fazer web scraping e download dos dados abertos do CNPJ da Receita Federal.

## 📋 Descrição

Este projeto automatiza o processo de:
1. **Web Scraping** da página oficial da Receita Federal
2. **Identificação** do diretório mais recente (formato YYYY-MM)
3. **Download** de todos os arquivos do diretório
4. **Extração** automática dos arquivos compactados

## 🐳 Docker (Recomendado)

### Pré-requisitos
- Docker
- Docker Compose

### Instalação e Uso com Docker

1. **Clone o repositório**
```bash
git clone https://github.com/marcelogbastos/dados-abertos-cnpj.git
cd dados-abertos-cnpj
```

2. **Construir a imagem Docker**
```bash
# Linux/Mac
./docker-run.sh build

# Windows (PowerShell)
.\docker-run.ps1 build
```

3. **Executar download automático**
```bash
# Linux/Mac
./docker-run.sh download

# Windows (PowerShell)
.\docker-run.ps1 download
```

4. **Verificar status**
```bash
# Linux/Mac
./docker-run.sh status

# Windows (PowerShell)
.\docker-run.ps1 status
```

### Comandos Docker Disponíveis

| Comando | Descrição |
|---------|-----------|
| `build` | Construir a imagem Docker |
| `download` | Download automático do mês mais recente |
| `download-month YYYY-MM` | Download de mês específico |
| `status` | Verificar status dos downloads |
| `test` | Executar testes |
| `clean-downloads` | Limpar arquivos baixados |
| `clean-extracted` | Limpar arquivos extraídos |
| `clean-all` | Limpar todos os arquivos |
| `shell` | Abrir shell no container |
| `logs` | Ver logs do container |
| `stop` | Parar containers |

### Exemplos de Uso com Docker

```bash
# Download do mês mais recente
./docker-run.sh download

# Download de janeiro de 2024
./docker-run.sh download-month 2024-01

# Verificar status
./docker-run.sh status

# Executar testes
./docker-run.sh test

# Limpar downloads antigos
./docker-run.sh clean-downloads
```

### Usando Docker Compose Diretamente

```bash
# Construir e executar download
docker-compose up cnpj-downloader

# Executar em background
docker-compose up -d cnpj-downloader

# Ver logs
docker-compose logs cnpj-downloader

# Parar containers
docker-compose down
```

## 🐍 Instalação Local (Alternativa)

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone ou baixe o projeto**
```bash
git clone https://github.com/marcelogbastos/dados-abertos-cnpj.git
cd dados-abertos-cnpj
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## 📖 Como Usar

### Download Automático (Mês Mais Recente)

Para baixar automaticamente o mês mais recente disponível:

```bash
# Com Docker (recomendado)
./docker-run.sh download

# Local
python cnpj_downloader.py
```

Ou usando o gerenciador:

```bash
# Com Docker
./docker-run.sh download

# Local
python cnpj_manager.py download
```

### Download de Mês Específico

Para baixar um mês específico:

```bash
# Com Docker
./docker-run.sh download-month 2024-01

# Local
python cnpj_manager.py download-month --month 2024-01
```

### Verificar Status

Para verificar o status dos downloads e extrações:

```bash
# Com Docker
./docker-run.sh status

# Local
python cnpj_manager.py status
```

### Limpeza de Arquivos

```bash
# Com Docker
./docker-run.sh clean-downloads
./docker-run.sh clean-extracted
./docker-run.sh clean-all

# Local
python cnpj_manager.py clean-downloads
python cnpj_manager.py clean-extracted
python cnpj_manager.py clean-all
```

## 📁 Estrutura de Diretórios

Após a execução, o projeto criará:

```
dados_abertos_cnpj/
├── downloads/           # Arquivos baixados
│   └── YYYY-MM/        # Organizados por mês
├── extracted/          # Arquivos extraídos
│   └── YYYY-MM/        # Organizados por mês
├── logs/              # Logs do sistema
├── cnpj_downloader.log # Log de execução
├── cnpj_downloader.py  # Script principal
├── cnpj_manager.py     # Script de gerenciamento
├── test_downloader.py  # Script de testes
├── exemplo_uso.py      # Exemplos de uso
├── requirements.txt    # Dependências
├── Dockerfile          # Configuração Docker
├── docker-compose.yml  # Orquestração Docker
├── docker-run.sh       # Script Linux/Mac
├── docker-run.ps1      # Script Windows
└── README.md           # Documentação
```

## 🔧 Funcionalidades

### CNPJDownloader (cnpj_downloader.py)
- **Web Scraping** automático da página da Receita Federal
- **Detecção** do diretório mais recente
- **Download** com barra de progresso
- **Extração** automática de arquivos ZIP
- **Logging** detalhado de todas as operações
- **Tratamento de erros** robusto

### CNPJManager (cnpj_manager.py)
- **Status** dos downloads e extrações
- **Download** de meses específicos
- **Limpeza** seletiva de arquivos
- **Interface** de linha de comando intuitiva

### Docker
- **Containerização** completa da aplicação
- **Volumes** para persistência de dados
- **Scripts** automatizados para Linux/Mac/Windows
- **Orquestração** com Docker Compose

## 📊 Logs

O aplicativo gera logs detalhados em `cnpj_downloader.log` incluindo:
- Progresso dos downloads
- Erros e exceções
- Informações sobre arquivos processados
- Timestamps de todas as operações

## ⚠️ Considerações Importantes

### Espaço em Disco
- Os dados CNPJ são muito grandes (vários GB por mês)
- Certifique-se de ter espaço suficiente antes de iniciar

### Conexão com Internet
- Downloads podem levar muito tempo dependendo da conexão
- O aplicativo inclui pausas para não sobrecarregar o servidor

### Arquivos Temporários
- Arquivos ZIP são mantidos em `downloads/` após extração
- Use `clean-downloads` para liberar espaço se necessário

### Docker
- Certifique-se de que o Docker está instalado e funcionando
- Os volumes Docker mantêm os dados persistentes entre execuções
- Use `docker system prune` para limpar imagens não utilizadas

## 🐛 Solução de Problemas

### Erro de Conexão
```bash
# Verifique sua conexão com a internet
ping arquivos.receitafederal.gov.br
```

### Erro de Permissão
```bash
# No Windows, execute como administrador
# No Linux/Mac, verifique permissões de escrita
ls -la
```

### Erro de Dependências
```bash
# Reinstale as dependências
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

### Erro de Docker
```bash
# Verificar se Docker está rodando
docker --version
docker-compose --version

# Reconstruir imagem
./docker-run.sh build

# Limpar cache Docker
docker system prune
```

## 📝 Exemplos de Uso

### Download do mês atual
```bash
# Docker
./docker-run.sh download

# Local
python cnpj_downloader.py
```

### Verificar o que foi baixado
```bash
# Docker
./docker-run.sh status

# Local
python cnpj_manager.py status
```

### Baixar mês específico
```bash
# Docker
./docker-run.sh download-month 2023-12

# Local
python cnpj_manager.py download-month --month 2023-12
```

### Limpar arquivos antigos
```bash
# Docker
./docker-run.sh clean-downloads

# Local
python cnpj_manager.py clean-downloads
```

## 🔗 Links Úteis

- [Portal de Dados Abertos CNPJ](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica-cnpj)
- [Receita Federal - Dados Abertos](https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 📄 Licença

Este projeto é de código aberto e pode ser usado livremente.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

---

**Desenvolvido para facilitar o acesso aos dados abertos do CNPJ da Receita Federal.** 