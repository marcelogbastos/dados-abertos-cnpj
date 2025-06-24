import os
import pandas as pd
import streamlit as st
import pyarrow.parquet as pq

PARQUET_DIR = 'parquet'

st.set_page_config(page_title='CNPJ Parquet Dashboard', layout='wide')
st.title('📊 Dashboard de Estatísticas dos Arquivos Parquet do CNPJ')

if not os.path.exists(PARQUET_DIR):
    st.error(f"Diretório '{PARQUET_DIR}' não encontrado.")
    st.stop()

parquet_files = [f for f in os.listdir(PARQUET_DIR) if f.endswith('.parquet')]

if not parquet_files:
    st.warning('Nenhum arquivo Parquet encontrado na pasta ./parquet.')
    st.stop()

stats = []
for fname in sorted(parquet_files):
    fpath = os.path.join(PARQUET_DIR, fname)
    try:
        pf = pq.ParquetFile(fpath)
        n_rows = pf.metadata.num_rows
        n_cols = pf.metadata.num_columns
        col_names = pf.schema.names
        colunas_disp = ', '.join(col_names)
    except Exception as e:
        n_rows = None
        n_cols = None
        colunas_disp = 'Erro'
    size_mb = os.path.getsize(fpath) / (1024*1024)
    stats.append({
        'Tabela': fname.replace('.parquet',''),
        'Arquivo': fname,
        'Registros': n_rows,
        'Colunas': n_cols,
        'Colunas disponíveis': colunas_disp,
        'Tamanho (MB)': size_mb
    })

# Cria DataFrame para facilitar ordenação
stats_df = pd.DataFrame(stats)
# Ordena por Registros, depois Colunas, depois Tamanho (MB)
stats_df = stats_df.sort_values(['Registros', 'Colunas', 'Tamanho (MB)'], ascending=[False, False, False])

# Formatação: ponto para milhar, vírgula para decimal (apenas para exibição)
def format_num(val, dec=0):
    if pd.isna(val):
        return 'Erro'
    if isinstance(val, int):
        return f"{val:,}".replace(",", ".")
    if isinstance(val, float):
        return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return val

stats_df_viz = stats_df.copy()
stats_df_viz['Registros'] = stats_df_viz['Registros'].apply(format_num)
stats_df_viz['Colunas'] = stats_df_viz['Colunas'].apply(format_num)
stats_df_viz['Tamanho (MB)'] = stats_df_viz['Tamanho (MB)'].apply(lambda x: format_num(x, 2))

st.subheader('Resumo das Tabelas')
st.dataframe(stats_df_viz, hide_index=True) 