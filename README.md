# CNPJ Data Downloader

Aplicativo Python para fazer web scraping e download dos dados abertos do CNPJ da Receita Federal.

## 📋 Descrição

Este projeto automatiza o processo de:
1. **Web Scraping** da página oficial da Receita Federal
2. **Identificação** do diretório mais recente (formato YYYY-MM)
3. **Download** de todos os arquivos do diretório
4. **Extração** automática dos arquivos compactados

## 🚀 Instalação

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone ou baixe o projeto**
```bash
git clone <url-do-repositorio>
cd dados_abertos_cnpj
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## 📖 Como Usar

### Download Automático (Mês Mais Recente)

Para baixar automaticamente o mês mais recente disponível:

```bash
python cnpj_downloader.py
```

Ou usando o gerenciador:

```bash
python cnpj_manager.py download
```

### Download de Mês Específico

Para baixar um mês específico:

```bash
python cnpj_manager.py download-month --month 2024-01
```

### Verificar Status

Para verificar o status dos downloads e extrações:

```bash
python cnpj_manager.py status
```

### Limpeza de Arquivos

```bash
# Remover apenas arquivos baixados (mantém extraídos)
python cnpj_manager.py clean-downloads

# Remover apenas arquivos extraídos
python cnpj_manager.py clean-extracted

# Remover todos os arquivos
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
├── cnpj_downloader.log # Log de execução
├── cnpj_downloader.py  # Script principal
├── cnpj_manager.py     # Script de gerenciamento
└── requirements.txt    # Dependências
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

## 📝 Exemplos de Uso

### Download do mês atual
```bash
python cnpj_downloader.py
```

### Verificar o que foi baixado
```bash
python cnpj_manager.py status
```

### Baixar mês específico
```bash
python cnpj_manager.py download-month --month 2023-12
```

### Limpar arquivos antigos
```bash
python cnpj_manager.py clean-downloads
```

## 🔗 Links Úteis

- [Portal de Dados Abertos CNPJ](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica-cnpj)
- [Receita Federal - Dados Abertos](https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/)

## 📄 Licença

Este projeto é de código aberto e pode ser usado livremente.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

---

**Desenvolvido para facilitar o acesso aos dados abertos do CNPJ da Receita Federal.** 