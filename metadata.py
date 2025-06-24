"""
Arquivo para centralizar os metadados (leiaute) dos arquivos
de dados abertos do CNPJ da Receita Federal.

Este arquivo é baseado na documentação oficial e em scripts SQL
de projetos da comunidade que já trabalham com esses dados.
"""

# Mapeamento dos tipos de arquivo para nomes de tabelas mais amigáveis
# A chave é o prefixo do arquivo (ex: 'EMPRESAS' de 'K3241.K03200DV.D10710.EMPRESAS1.csv')
# O valor é o nome da tabela que será usada.
TABLE_NAMES = {
    'EMPRECSV': 'empresas',
    'ESTABELE': 'estabelecimentos',
    'SOCIOCSV': 'socios',
    'SIMPLES': 'simples',
    'CNAES': 'cnaes',
    'MUNIC': 'municipios',
    'NATJU': 'naturezas_juridicas',
    'PAIS': 'paises',
    'QUALS': 'qualificacoes_socios',
    'MOTI': 'motivos',
}

# Definição das colunas para cada tipo de arquivo/tabela
# Baseado no arquivo 'NOVOLAYOUTDOSDADOSABERTOSDOCNPJ.pdf' e scripts da comunidade.
LAYOUTS = {
    'empresas': [
        'cnpj_basico',
        'razao_social',
        'natureza_juridica',
        'qualificacao_responsavel',
        'capital_social',
        'porte_empresa',
        'ente_federativo_responsavel'
    ],
    'estabelecimentos': [
        'cnpj_basico',
        'cnpj_ordem',
        'cnpj_dv',
        'identificador_matriz_filial',
        'nome_fantasia',
        'situacao_cadastral',
        'data_situacao_cadastral',
        'motivo_situacao_cadastral',
        'nome_cidade_exterior',
        'pais',
        'data_inicio_atividade',
        'cnae_fiscal_principal',
        'cnae_fiscal_secundaria',
        'tipo_logradouro',
        'logradouro',
        'numero',
        'complemento',
        'bairro',
        'cep',
        'uf',
        'municipio',
        'ddd_1',
        'telefone_1',
        'ddd_2',
        'telefone_2',
        'ddd_fax',
        'correio_eletronico',
        'situacao_especial',
        'data_situacao_especial'
    ],
    'socios': [
        'cnpj_basico',
        'identificador_socio',
        'nome_socio_razao_social',
        'cnpj_cpf_socio',
        'qualificacao_socio',
        'data_entrada_sociedade',
        'pais',
        'representante_legal',
        'nome_representante',
        'qualificacao_representante_legal',
        'faixa_etaria'
    ],
    'simples': [
        'cnpj_basico',
        'opcao_pelo_simples',
        'data_opcao_simples',
        'data_exclusao_simples',
        'opcao_pelo_mei',
        'data_opcao_mei',
        'data_exclusao_mei'
    ],
    'cnaes': [
        'codigo',
        'descricao'
    ],
    'municipios': [
        'codigo',
        'descricao'
    ],
    'naturezas_juridicas': [
        'codigo',
        'descricao'
    ],
    'paises': [
        'codigo',
        'descricao'
    ],
    'qualificacoes_socios': [
        'codigo',
        'descricao'
    ],
    'motivos': [
        'codigo',
        'descricao'
    ]
} 