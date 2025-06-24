# 📂 Downloader de Dados Abertos do CNPJ

Este projeto contém um conjunto de scripts Python para baixar, extrair e converter os [Dados Abertos de CNPJ](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj) da Receita Federal para o formato Parquet, otimizado para análise de dados.

Todo o processo é orquestrado com Docker para garantir um ambiente consistente e facilitar a execução.

## 🚀 Como Usar (Docker)

A forma recomendada de usar este projeto é através dos scripts de execução, que gerenciam os contêineres Docker.

### Pré-requisitos
- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Comandos Principais

Abra um terminal na raiz do projeto e execute um dos comandos abaixo.

> **Nota:** No Windows, use `.\\docker-run.ps1`. No Linux ou macOS, use `./docker-run.sh`.

| Comando | Descrição |
|---------|-----------|
| `all` | **(Recomendado)** Executa o pipeline completo: baixa, extrai e converte os dados para Parquet. |
| `download` | Apenas baixa e extrai os arquivos da Receita Federal. |
| `import-parquet` | Converte os arquivos já extraídos para o formato Parquet. |
| `status` | Mostra um resumo dos arquivos já baixados e extraídos. |
| `list [tipo]` | Lista os caminhos dos arquivos de um tipo específico (ex: `list empresas`). |
| `clean` | Apaga todos os dados baixados, extraídos e os arquivos Parquet. |
| `build` | Força a reconstrução das imagens Docker. |
| `shell` | Abre um terminal interativo dentro do contêiner de gerenciamento. |
| `stop` | Para todos os contêineres em execução. |

### Como importar para Parquet

Para converter os arquivos extraídos para o formato Parquet, execute:

**Windows (PowerShell):**
```powershell
.\docker-run.ps1 import-parquet
```

**Linux / macOS:**
```bash
./docker-run.sh import-parquet
```

Os arquivos Parquet serão gerados na pasta `parquet/`.

### Exemplo de Execução Completa

Para executar todo o processo, do download à conversão para Parquet:

**Windows (PowerShell):**
```powershell
.\\docker-run.ps1 all
```

**Linux / macOS:**
```bash
./docker-run.sh all
```

Os arquivos Parquet finais serão salvos no diretório `./parquet`.

## 📁 Estrutura de Diretórios

- `downloads/`: Armazena os arquivos `.zip` baixados da Receita.
- `extracted/`: Contém os arquivos `.csv` extraídos.
- `parquet/`: Guarda os arquivos `.parquet` convertidos, prontos para análise.
- `logs/`: Registra os logs de execução dos processos.
- `metadata.py`: Arquivo central com os layouts e nomes de tabelas dos dados.

## 🔧 Scripts Principais

- `cnpj_downloader.py`: Responsável por encontrar o link mais recente, baixar e extrair os arquivos.
- `cnpj_manager.py`: Fornece comandos auxiliares como `status` e `list`.
- `import_to_parquet.py`: Converte os arquivos de texto para o formato Parquet de forma otimizada.

## ⚠️ Considerações

- **Espaço em Disco:** O conjunto completo de dados CNPJ é extremamente grande (mais de 100 GB). Certifique-se de ter espaço suficiente.
- **Tempo de Execução:** O processo de download e conversão pode levar várias horas, dependendo da sua conexão com a internet e da performance do seu computador.

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
| `help` | Mostrar ajuda |

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
├── parquet/            # Arquivos convertidos para Parquet (ex: empresas.parquet)
├── logs/               # Logs do sistema
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

O sistema oferece as seguintes funcionalidades principais:

- **Download automático dos dados mais recentes do CNPJ**
  - Exemplo:
    ```bash
    ./docker-run.sh download
    # ou
    .\docker-run.ps1 download
    ```

- **Download de um mês específico**
  - Exemplo:
    ```bash
    ./docker-run.sh download-month 2024-01
    # ou
    python cnpj_manager.py download-month --month 2024-01
    ```

- **Extração automática dos arquivos ZIP baixados**
  - Ocorre automaticamente após o download.

- **Verificação de status dos arquivos baixados e extraídos**
  - Exemplo:
    ```bash
    ./docker-run.sh status
    # ou
    .\docker-run.ps1 status
    ```

- **Listagem de arquivos extraídos por tipo de tabela**
  - Exemplo:
    ```bash
    ./docker-run.sh list empresas
    # ou
    .\docker-run.ps1 list estabelecimentos
    ```

- **Limpeza seletiva ou total dos dados (downloads, extraídos, Parquet)**
  - Exemplo:
    ```bash
    ./docker-run.sh clean
    # ou
    .\docker-run.ps1 clean
    ```

- **Conversão eficiente dos arquivos extraídos para o formato Parquet**
  - Exemplo:
    ```bash
    ./docker-run.sh import-parquet
    # ou
    .\docker-run.ps1 import-parquet
    ```
  - Os arquivos Parquet são salvos em `parquet/` e podem ser lidos em Python, Spark, DuckDB, DBeaver, etc.

- **Execução do pipeline completo (download, extração e conversão para Parquet) em um único comando**
  - Exemplo:
    ```bash
    ./docker-run.sh all
    # ou
    .\docker-run.ps1 all
    ```

- **Abertura de shell interativo no container para inspeção avançada**
  - Exemplo:
    ```bash
    ./docker-run.sh shell
    # ou
    .\docker-run.ps1 shell
    ```

- **Logs detalhados de todas as operações**
  - Os logs são salvos em `logs/` e exibidos no console durante a execução.

- **Configuração e execução totalmente automatizadas via Docker Compose**
  - Não é necessário instalar dependências Python localmente.

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

## 📊 Dashboard Interativo

O projeto inclui um dashboard interativo em Streamlit para explorar e visualizar os dados Parquet gerados.

### Como executar o dashboard

Execute o serviço do dashboard de forma independente (não depende de download ou importação):

```sh
docker-compose up dashboard
```

Acesse no navegador:

[http://localhost:8501](http://localhost:8501)

- O dashboard permite visualizar estatísticas, amostras, gráficos e fazer buscas nos dados Parquet.
- Não é necessário rodar download ou importação juntos para visualizar os dados já existentes.