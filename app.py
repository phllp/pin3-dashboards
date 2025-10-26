from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from streamlit.components.v1 import html as st_html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 
from sqlalchemy import create_engine, text
import os
import numpy as np 
import json 
from streamlit_plotly_events import plotly_events 

st.set_page_config(page_title="Dashboard ENEM", layout="wide")

# ========================= CSS =========================
st.markdown("""
<style>
@import url('https://fonts.googleazpis.com/css2?family=Poppins:wght@700;800&display=swap');

:root{
  --bg-main:#1e2447;
  --bg-side:#1a2040;
  --panel:#2a3058;
  --stroke:#3a416b;
  --text:#eef1ff;
  --muted:#aab1d3;
  --radius:12px;
  --font: Inter, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
}

header, #MainMenu, footer, div[data-testid="stToolbar"] { display:none !important; }

html, body, [data-testid="stAppViewContainer"], .main, .block-container{
  background:var(--bg-main) !important; color:var(--text) !important; font-family:var(--font) !important;
}
.block-container{ padding-top:14px; }

section[data-testid="stSidebar"]{
  position: sticky; top: 0;
  height: 100vh !important;
  overflow: auto !important;
  background: var(--bg-side) !important;
  border-right: 1px solid var(--stroke);
  padding: 6px 10px 8px 10px;
}

.sidebar-title{
  font-family: Poppins, var(--font);
  font-weight: 800;
  font-size: 24px;
  text-align: center;
  margin: 2px 0 4px 0;
  letter-spacing:.4px;
}
.hr{height:1px; background:var(--stroke); margin:6px 0 8px 0;}

label{
  color: var(--muted) !important;
  font-weight: 600; font-size: 11px !important;
  margin-bottom: 2px !important;
  display: block; /* Garante que a label ocupe a linha */
}
div[data-baseweb="select"] > div{
  background: var(--panel) !important;
  border: 1px solid var(--stroke) !important;
  border-radius: var(--radius) !important;
  min-height: 34px !important;
  padding: 0 8px !important;
}
div[data-baseweb="select"] svg{ width:14px; height:14px; }

div[data-testid="stTextInput"] > div > div {
  background: var(--panel) !important;
  border: 1px solid var(--stroke) !important;
  border-radius: var(--radius) !important;
  min-height: 34px !important;
}
div[data-testid="stTextInput"] input {
  color: var(--text) !important;
  padding: 0 14px !important;
  line-height: 34px !important;
  height: 34px !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: var(--muted) !important;
    opacity: 0.7 !important;
}

div[data-baseweb="select"] > div > div {
    color: var(--text) !important;
}

li[data-baseweb="list-item"] {
    background-color: var(--panel) !important;
    color: var(--text) !important;
}
li[data-baseweb="list-item"]:hover {
    background-color: var(--stroke) !important;
}

.sidebar-group{ margin-bottom: 6px; }

.stButton{ display:flex; justify-content:center; }
.stButton>button{
  height: 34px !important;
  min-width: 140px !important;
  width: 90% !important;
  padding: 4px 10px !important;
  border-radius: 10px !important;
  background:#3a4b86 !important;
  border:1px solid var(--stroke) !important;
  color: var(--text) !important;
  font-weight: 700 !important;
  font-size: 12px !important;
}
.stButton>button:hover{
    background: #4a5b96 !important;
}

.w-kpi-placeholder{ background:var(--panel); border:1px solid var(--stroke); border-radius:var(--radius); height:110px; width:100%; padding: 12px 16px; }
.w-box-placeholder{ background:var(--panel); border:1px solid var(--stroke); border-radius:var(--radius); height:360px; width:100%; padding: 10px; overflow: hidden;}
.w-tall-placeholder{ background:var(--panel); border:1px solid var(--stroke); border-radius:var(--radius); height: calc(360px + 12px + 360px); width:100%; padding: 10px; }

.chart-placeholder-box {
    background-color: var(--panel);
    border: 1px solid var(--stroke);
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--muted);
    padding: 20px;
    text-align: center;
}

.chart-placeholder-box.small {
    height: 340px;
}

.chart-placeholder-box.tall {
    height: 712px;
    min-height: 712px;
}

.section-title{
  font-family: Poppins, var(--font);
  font-size: 24px; font-weight: 800; margin: 6px 0 8px 2px;
}


.kpi-title {
    font-size: 13px;
    color: var(--muted);
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 26px;
    font-weight: 700;
    line-height: 1.1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.kpi-container {
    background: var(--panel);
    border: 1px solid var(--stroke);
    border-radius: var(--radius);
    height: 110px;
    width: 100%;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.kpi-sub-row {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-top: 10px;
    width: 100%;
}
.kpi-sub-col {
    text-align: center;
    flex: 1;
}
.kpi-sub-val {
    font-size: 26px;
    font-weight: 700;
    line-height: 1;
}
.kpi-sub-title {
    font-size: 11px;
    color: var(--muted);
    margin-top: 2px;
}
.kpi-separator {
    width: 1px;
    height: 40px;
    background-color: var(--stroke);
    margin: 0 5px;
}

.lang-kpi-content {
    margin-top: 5px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.lang-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2px;
    padding: 0 5px;
}
.lang-title {
    font-weight: 600;
    font-size: 12px;
    color: var(--text);
}
.lang-value {
    font-weight: 600;
    font-size: 12px;
    color: var(--muted);
}
.progress-bar-container {
    background: var(--stroke);
    border-radius: 10px;
    height: 6px;
    margin: 2px 5px 8px 5px;
    overflow: hidden;
}
.progress-bar-fill {
    background: var(--text);
    height: 100%;
    border-radius: 10px;
    transition: width 0.5s ease-in-out;
}

div[data-testid="stDataFrame"] {
    background-color: var(--panel) !important;
    border: 1px solid var(--stroke) !important;
    border-radius: var(--radius) !important;
    padding: 5px;
    overflow: hidden;
    height: 340px;
    display: flex;
    flex-direction: column;
}

div[data-testid="stDataFrame"] > div {
      flex-grow: 1;
      overflow: auto;
      border: none !important;
}
div[data-testid="stDataFrame"] > div > div > table {
    background-color: transparent !important;
    color: var(--text) !important;
    font-size: 12px;
}
div[data-testid="stDataFrame"] thead th {
    background-color: var(--bg-side) !important;
    color: var(--muted) !important;
    border-bottom: 1px solid var(--stroke) !important;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 10px;
    padding: 6px 8px !important;
    position: sticky;
    top: 0;
    z-index: 1;
}
div[data-testid="stDataFrame"] tbody tr:nth-of-type(even) {
      background-color: rgba(58, 65, 107, 0.3) !important;
}
div[data-testid="stDataFrame"] tbody tr:hover td {
    background-color: rgba(58, 65, 107, 0.7) !important;
    color: var(--text) !important;
}
div[data-testid="stDataFrame"] tbody td {
    color: var(--text) !important;
    border: none !important;
    padding: 6px 8px !important;
}


div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"]:nth-child(1)
> div[data-testid="element-container"]:nth-child(1)
> div[data-testid="stPlotlyChart"],
div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"]:nth-child(1)
> div[data-testid="element-container"]:nth-child(3)
> div[data-testid="stPlotlyChart"] {
    background-color: var(--panel) !important;
    border: 1px solid var(--stroke) !important;
    border-radius: var(--radius) !important;
    padding: 10px;
    overflow: hidden;
    height: 340px !important;
    box-sizing: border-box;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"]:nth-child(2)
> div[data-testid="element-container"]:nth-child(1)
> div[data-testid="stPlotlyChart"] {
    background-color: var(--panel) !important;
    border: 1px solid var(--stroke) !important;
    border-radius: var(--radius) !important;
    padding: 10px;
    overflow: hidden;

    /* (340px + 12px gap + 340px = 692px) + 20px padding = 712px */
    height: 712px !important;
    min-height: 712px !important;
    box-sizing: border-box;
}

.map-placeholder {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    color: var(--muted);
    background-color: var(--panel);
    border-radius: var(--radius);
    padding: 10px;
    min-height: 710px; /* Garante altura mínima */
}
.map-placeholder svg {
    width: 80px;
    height: 80px;
    margin-bottom: 15px;
    opacity: 0.5;
}
.map-placeholder p {
    font-size: 14px;
    text-align: center;
    line-height: 1.4;
}

</style>
""", unsafe_allow_html=True)


# ========================= CONFIGURAÇÃO DO BANCO DE DADOS =========================

DATABASE_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?client_encoding=utf8"
tabela =os.getenv('NOME_TABELA')

# ========================= FUNÇÃO DE CARREGAMENTO DE DADOS E GEOJSON =========================

@st.cache_data(show_spinner=False)
def carregar_geojson_local(filename):
    """ Carrega dados GeoJSON de um arquivo local. """
    try:
        script_dir = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
        filepath = os.path.join(script_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Arquivo GeoJSON '{filename}' não encontrado na pasta do script ({script_dir}). Faça o download e salve-o lá.")

        try:
             with open(filename, 'r', encoding='utf-8') as f:
                  st.info(f"Carregado GeoJSON de: {os.path.abspath(filename)}")
                  return json.load(f)
        except Exception:
             return None
    except json.JSONDecodeError as e:
        st.error(f"Erro ao decodificar GeoJSON local '{filename}': {e}")
        return None
    except Exception as e:
        st.error(f"Erro inesperado ao carregar GeoJSON local '{filename}': {e}")
        return None

@st.cache_data(show_spinner="Carregando dados...")
def carregar_dados_db(_engine):
    """
    Carrega os dados do banco de dados PostgreSQL e o GeoJSON local.
    """
    geojson_data = carregar_geojson_local(os.getenv('LOCAL_GEOJSON_FILENAME'))
    if geojson_data is None:
        st.warning("Não foi possível carregar os dados geográficos para o mapa.")

    try:
        with _engine.connect() as connection:

            query_anos = text(f'SELECT DISTINCT "NU_ANO" FROM "{tabela}" ORDER BY "NU_ANO" DESC')
            query_faixa = text(f'SELECT DISTINCT "TP_FAIXA_ETARIA" FROM "{tabela}" ORDER BY "TP_FAIXA_ETARIA"')
            query_conclusao = text(f'SELECT DISTINCT "TP_ST_CONCLUSAO" FROM "{tabela}" ORDER BY "TP_ST_CONCLUSAO"')

            anos_disponiveis = [str(a[0]) for a in connection.execute(query_anos).fetchall() if a[0] is not None]
            faixas_disponiveis = [f[0] for f in connection.execute(query_faixa).fetchall() if f[0] is not None]
            conclusoes_disponiveis = [c[0] for c in connection.execute(query_conclusao).fetchall() if c[0] is not None]

            colunas_necessarias = [
                "NU_INSCRICAO", "NU_ANO", "TP_FAIXA_ETARIA", "TP_SEXO", "TP_ST_CONCLUSAO",
                "SG_UF_PROVA", "NO_MUNICIPIO_PROVA", 
                "TP_LINGUA", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC",
                "NU_NOTA_MT", "NU_NOTA_REDACAO", "MEDIA_GERAL", "INDICADOR_ABSENTEISMO"
            ]
            colunas_necessarias = sorted(list(set(colunas_necessarias)))
            colunas_query = ", ".join([f'"{col}"' for col in colunas_necessarias])
            query_total = text(f'SELECT {colunas_query} FROM "{tabela}"')

            df = pd.read_sql(query_total, connection)

            if 'NU_ANO' in df.columns:
                df['NU_ANO'] = pd.to_numeric(df['NU_ANO'], errors='coerce').astype('Int64')
            if 'TP_SEXO' in df.columns:
                df['TP_SEXO'] = df['TP_SEXO'].astype(str)
            if 'TP_FAIXA_ETARIA' in df.columns:
                df['TP_FAIXA_ETARIA'] = pd.to_numeric(df['TP_FAIXA_ETARIA'], errors='coerce').astype('Int64')
            if 'TP_ST_CONCLUSAO' in df.columns:
                df['TP_ST_CONCLUSAO'] = pd.to_numeric(df['TP_ST_CONCLUSAO'], errors='coerce').astype('Int64')
            if 'TP_LINGUA' in df.columns:
                 df['TP_LINGUA'] = pd.to_numeric(df['TP_LINGUA'], errors='coerce').astype('Int64')
            for col_nota in ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_GERAL']:
                 if col_nota in df.columns:
                       df[col_nota] = pd.to_numeric(df[col_nota], errors='coerce')

            if 'NO_MUNICIPIO_PROVA' in df.columns:
                df['NO_MUNICIPIO_PROVA'] = df['NO_MUNICIPIO_PROVA'].astype(str).str.strip()

            return df, anos_disponiveis, faixas_disponiveis, conclusoes_disponiveis, geojson_data

    except Exception as e:
        st.error(f"Erro ao conectar ou carregar dados do PostgreSQL: {e}")

        return pd.DataFrame(), [], [], [], geojson_data


@st.cache_data(show_spinner="Buscando municípios...")
def buscar_municipios_por_estado(estado_sigla, _engine):
    """ Busca a lista de municípios para um dado estado no banco de dados. """
    if not estado_sigla or estado_sigla == "Todos":
        return []

    try:
        with _engine.connect() as connection:
            query = text(f'''
                SELECT DISTINCT "NO_MUNICIPIO_PROVA"
                FROM "{tabela}"
                WHERE "SG_UF_PROVA" = :estado
                ORDER BY "NO_MUNICIPIO_PROVA" ASC
            ''')
            result = connection.execute(query, {"estado": estado_sigla})
            municipios = [row[0] for row in result.fetchall() if row[0]]
            return sorted(list(set(municipios)))
    except Exception as e:
        st.error(f"Erro ao buscar municípios para {estado_sigla}: {e}")
        return []

# --- Conectar ao Banco ---
try:
    engine = create_engine(DATABASE_URL)
    # Teste de conexão
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
except Exception as e:
    st.error(f"Falha ao criar 'engine' ou conectar ao SQLAlchemy: {e}")
    st.info("Verifique a string de conexão, usuário, senha, host, porta e se o serviço PostgreSQL está ativo.")
    st.stop()

# --- Carregar Dados e GeoJSON ---
df_principal, anos_disponiveis_db, faixas_disponiveis_num_db, conclusoes_disponiveis_num_db, geojson_brasil = carregar_dados_db(engine)

if df_principal.empty:
    st.error("Nenhum dado foi carregado do banco de dados. Verifique o SCRIPT.py e a conexão.")
    st.stop()


try:
    anos_options_fim = sorted(anos_disponiveis_db, key=int, reverse=True) # Mais recente primeiro para 'Fim'
    anos_options_inicio = sorted(anos_disponiveis_db, key=int, reverse=False) # Mais antigo primeiro para 'Início'

    map_faixa_etaria = {
        1: 'Menor de 17 anos', 2: '17 anos', 3: '18 anos', 4: '19 anos', 5: '20 anos',
        6: '21 anos', 7: '22 anos', 8: '23 anos', 9: '24 anos', 10: '25 anos',
        11: '26-30 anos', 12: '31-35 anos', 13: '36-40 anos', 14: '41-45 anos',
        15: '46-50 anos', 16: '51-55 anos', 17: '56-60 anos', 18: '61-65 anos',
        19: '66-70 anos', 20: 'Maior de 70 anos'
    }

    #verificar isso
    map_conclusao = {
        1: 'Já concluí o Ensino Médio',
        2: 'Estou cursando e concluirei em 2024', 
        3: 'Estou cursando e concluirei após 2024', 
        4: 'Não concluí e não estou cursando'
    }

    faixas_options = ["Todos"] + [map_faixa_etaria.get(f, f"Código {f}") for f in sorted([int(x) for x in faixas_disponiveis_num_db if pd.notna(x)])]
    conclusoes_options = ["Todos"] + [map_conclusao.get(c, f"Código {c}") for c in sorted([int(x) for x in conclusoes_disponiveis_num_db if pd.notna(x)])]

except Exception as e:
    st.error(f"Erro ao preparar opções dos filtros: {e}")
    anos_options_inicio = []
    anos_options_fim = []
    faixas_options = ["Todos"]
    conclusoes_options = ["Todos"]

ano_inicio_default_idx = 0 if anos_options_inicio else 0
ano_fim_default_idx = 0 if anos_options_fim else 0

if 'sel_ano_inicio' not in st.session_state:
    st.session_state.sel_ano_inicio = anos_options_inicio[ano_inicio_default_idx] if anos_options_inicio else None
if 'sel_ano_fim' not in st.session_state:
    st.session_state.sel_ano_fim = anos_options_fim[ano_fim_default_idx] if anos_options_fim else None
if 'sel_estado' not in st.session_state:
    st.session_state.sel_estado = "Todos"
if 'sel_municipio' not in st.session_state:
    st.session_state.sel_municipio = "Todos"
if 'sel_genero' not in st.session_state:
    st.session_state.sel_genero = "Todos"
if 'sel_faixa_etaria' not in st.session_state:
    st.session_state.sel_faixa_etaria = "Todos"
if 'sel_escolaridade' not in st.session_state:
    st.session_state.sel_escolaridade = "Todos"
if 'clicked_estado' not in st.session_state:
    st.session_state.clicked_estado = None
if 'opcoes_municipio' not in st.session_state:
    st.session_state.opcoes_municipio = ["Todos"]


def atualizar_lista_municipios():
    estado_atual = st.session_state.get('sel_estado', "Todos")

    municipios_do_estado = buscar_municipios_por_estado(estado_atual, engine)

    st.session_state.opcoes_municipio = ["Todos"] + municipios_do_estado

    if 'sel_municipio' in st.session_state:
        st.session_state.sel_municipio = "Todos"


with st.sidebar:
    st.markdown("<div class='sidebar-title'>Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    estados_brasileiros = [
        "Todos", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT",
        "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR",
        "SC", "SP", "SE", "TO"
    ]
    genero_opcoes = ["Todos", "Feminino", "Masculino"]


    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    st.markdown("<label>ANO</label>", unsafe_allow_html=True)
    ano_col1, ano_col2 = st.columns(2)
 
    with ano_col1:
        ano_inicio = st.selectbox(
            "Início",
            options=anos_options_inicio,
            label_visibility="collapsed",
            key="sel_ano_inicio"
        )
    with ano_col2:
        ano_fim = st.selectbox(
            "Fim",
            options=anos_options_fim,
            label_visibility="collapsed",
            key="sel_ano_fim"
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Filtro ESTADO---
    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    estado_selecionado = st.selectbox(
        "ESTADO",
        estados_brasileiros,
        key="sel_estado",
        on_change=atualizar_lista_municipios # Chama a função quando o estado muda
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Filtro MUNICÍPIO  ---
    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    municipio_selecionado = st.selectbox(
        "MUNICÍPIO",
        options=st.session_state.opcoes_municipio,
        key="sel_municipio"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    genero_selecionado = st.selectbox("GÊNERO", genero_opcoes, key="sel_genero")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    faixa_etaria_selecionada = st.selectbox(
        "FAIXA ETÁRIA",
        options=faixas_options,
        key="sel_faixa_etaria"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    escolaridade_selecionada = st.selectbox(
        "ESCOLARIDADE", 
        options=conclusoes_options,
        key="sel_escolaridade"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    # --- Botões ---
    
    # Callback para limpar todos os filtros
    def limpar_filtros_callback():
        st.session_state.sel_estado = "Todos"
        st.session_state.sel_genero = "Todos"
        st.session_state.sel_faixa_etaria = "Todos"
        st.session_state.sel_escolaridade = "Todos"
        st.session_state.sel_ano_inicio = anos_options_inicio[ano_inicio_default_idx] if anos_options_inicio else None
        st.session_state.sel_ano_fim = anos_options_fim[ano_fim_default_idx] if anos_options_fim else None
        
        if 'clicked_estado' in st.session_state:
            st.session_state.clicked_estado = None
            
        atualizar_lista_municipios()


    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    st.button("Limpar Filtros", on_click=limpar_filtros_callback)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    st.button("Comparar Grupos")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    gerar_pdf = st.button("Gerar PDF")
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.sel_estado != "Todos" and st.session_state.opcoes_municipio == ["Todos"]:
     atualizar_lista_municipios()


# ========================= FUNÇÕES DE LAYOUT =========================
def gap(h=10):
    st.markdown(f"<div style='height:{h}px'></div>", unsafe_allow_html=True)

def section(title: str):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ========================= FUNÇÕES DE VISUALIZAÇÃO =========================
def criar_kpi(titulo, valor, formato="{:,}"):
    """ Cria o HTML para um KPI simple. """
    valor_formatado = "N/A"
    if pd.notna(valor):
        try:
            if isinstance(valor, (int, np.integer, float, np.floating)):
                if isinstance(valor, (int, np.integer)) or (isinstance(valor, (float, np.floating)) and valor == int(valor)):
                     valor_formatado = "{:,.0f}".format(valor).replace(",", ".")
                else:
                     valor_formatado = "{:,.2f}".format(valor).replace(",", "#").replace(".", ",").replace("#", ".") # Formato brasileiro
            else:
                 valor_formatado = str(valor)
        except Exception as e:
             valor_formatado = "Erro"

    return f"""
    <div class='kpi-container'>
        <div class='kpi-title'>{titulo}</div>
        <div class='kpi-value'>{valor_formatado}</div>
    </div>
    """

def criar_kpi_presenca(titulo, val_pres, val_aus, formato_perc="{:.0%}"):
    """ Cria o HTML para o KPI de Presença/Ausência. """
    val_pres_fmt = "N/A"
    val_aus_fmt = "N/A"
    try:
        if pd.notna(val_pres): val_pres_fmt = formato_perc.format(val_pres)
        if pd.notna(val_aus): val_aus_fmt = formato_perc.format(val_aus)
    except Exception as e:
        pass

    return f"""
    <div class='kpi-container'>
        <div class='kpi-title'>{titulo}</div>
        <div class='kpi-sub-row'>
            <div class='kpi-sub-col'>
                <div class='kpi-sub-val'>{val_pres_fmt}</div>
                <div class='kpi-sub-title'>Presente</div>
            </div>
            <div class='kpi-separator'></div>
            <div class='kpi-sub-col'>
                <div class='kpi-sub-val'>{val_aus_fmt}</div>
                <div class='kpi-sub-title'>Ausente</div>
            </div>
        </div>
    </div>
    """

def criar_kpi_lingua(titulo, val_ing, val_esp, perc_ing, perc_esp, formato_num="{:,}"):
    """ Cria o HTML para o KPI de Língua Estrangeira. """
    val_ing_fmt = "N/A"
    val_esp_fmt = "N/A"
    perc_ing_fmt = "N/A"
    perc_esp_fmt = "N/A"
    barra_ing = 0
    barra_esp = 0

    try:
        if pd.notna(val_ing): val_ing_fmt = formato_num.format(val_ing).replace(",", ".")
        if pd.notna(val_esp): val_esp_fmt = formato_num.format(val_esp).replace(",", ".")
        if pd.notna(perc_ing):
            perc_ing_fmt = f"{perc_ing*100:.0f}%"
            barra_ing = max(0, min(100, perc_ing * 100))
        if pd.notna(perc_esp):
            perc_esp_fmt = f"{perc_esp*100:.0f}%"
            barra_esp = max(0, min(100, perc_esp * 100))
    except Exception as e:
         pass

    return f"""
    <div class='kpi-container'>
        <div class='kpi-title'>{titulo}</div>
        <div class='lang-kpi-content'>
            <div>
                <div class='lang-row'>
                    <span class='lang-title'>Inglês</span>
                    <span class='lang-value'>{val_ing_fmt}</span>
                </div>
                <div class='progress-bar-container'>
                    <div class='progress-bar-fill' style='width: {barra_ing}%;'></div>
                </div>
            </div>
            <div>
                <div class'lang-row'>
                    <span class='lang-title'>Espanhol</span>
                    <span class='lang-value'>{val_esp_fmt}</span>
                </div>
                <div class='progress-bar-container'>
                    <div class='progress-bar-fill' style='width: {barra_esp}%;'></div>
                </div>
            </div>
        </div>
    </div>
    """

def criar_tabela_anual(df_filtrado):
    """ Calcula e retorna o DataFrame para a tabela anual. """
    if df_filtrado.empty or 'NU_ANO' not in df_filtrado.columns:
        return pd.DataFrame(columns=['Ano', 'Total Inscritos', 'Total Confirmados', '% Presentes', '% Ausentes'])

    df_agrupar = df_filtrado.dropna(subset=['NU_ANO'])
    df_agrupar = df_agrupar[pd.to_numeric(df_agrupar['NU_ANO'], errors='coerce').notna()]
    if df_agrupar.empty:
         return pd.DataFrame(columns=['Ano', 'Total Inscritos', 'Total Confirmados', '% Presentes', '% Ausentes'])
    df_agrupar['NU_ANO'] = df_agrupar['NU_ANO'].astype(int)


    df_anual = df_agrupar.groupby('NU_ANO').agg(
        total_inscritos=pd.NamedAgg(column='NU_INSCRICAO', aggfunc='count'),
        total_presentes=pd.NamedAgg(column='INDICADOR_ABSENTEISMO', aggfunc=lambda x: (x == 'Presente').sum()),
        total_ausentes_dia=pd.NamedAgg(column='INDICADOR_ABSENTEISMO', aggfunc=lambda x: (x == 'Ausente em um ou mais dias').sum())
    ).reset_index()

    confirmados_mask = df_agrupar['INDICADOR_ABSENTEISMO'] != 'Ausente em um ou mais dias'
    if confirmados_mask.any():
        df_confirmados_ano = df_agrupar[confirmados_mask].groupby('NU_ANO').size().rename('total_confirmados')
        df_anual = pd.merge(df_anual, df_confirmados_ano, on='NU_ANO', how='left').fillna({'total_confirmados': 0})
    else:
        df_anual['total_confirmados'] = 0

        
    df_anual['total_confirmados'] = df_anual['total_confirmados'].astype(int)


    # % Presentes = Presentes / Total Inscritos
    df_anual['perc_presentes'] = (df_anual['total_presentes'] / df_anual['total_inscritos']).replace([np.inf, -np.inf, np.nan], 0)
    # % Ausentes = Ausentes (pelo menos 1 dia) / Total Inscritos
    df_anual['perc_ausentes'] = (df_anual['total_ausentes_dia'] / df_anual['total_inscritos']).replace([np.inf, -np.inf, np.nan], 0)

    df_anual.rename(columns={
        'NU_ANO': 'Ano',
        'total_inscritos': 'Total Inscritos',
        'total_confirmados': 'Total Confirmados',
        'perc_presentes': '% Presentes',
        'perc_ausentes': '% Ausentes'
    }, inplace=True)

    df_anual = df_anual[['Ano', 'Total Inscritos', 'Total Confirmados', '% Presentes', '% Ausentes']].sort_values(by='Ano', ascending=False)

    return df_anual

# --- FUNÇÃO criar_donut_genero ---
def criar_donut_genero(df_filtrado):
    """ Cria e retorna a figura do gráfico de rosca de gênero. """
    if df_filtrado.empty or 'TP_SEXO' not in df_filtrado.columns or df_filtrado['TP_SEXO'].isnull().all():
        return None

    df_genero_data = df_filtrado.dropna(subset=['TP_SEXO'])
    if df_genero_data.empty:
        return None

    df_genero = df_genero_data['TP_SEXO'].astype(str).value_counts().reset_index()
    if df_genero.empty:
        return None

    df_genero.columns = ['Genero_Code', 'Count']
    df_genero['Genero'] = df_genero['Genero_Code'].map({'F': 'Feminino', 'M': 'Masculino'}).fillna('Não declarado')

    if df_genero.empty:
        return None

    try:
        fig = px.pie(df_genero, names='Genero', values='Count', hole=0.6,
                     color_discrete_map={'Feminino': '#a95aed', 'Masculino': '#4a5b96', 'Não declarado': '#777'})

        fig.update_traces(textposition='outside', textinfo='percent+label',
                          marker=dict(line=dict(color= 'var(--panel)', width=4)),
                          pull=[0.02] * len(df_genero),
                          hovertemplate='<b>%{label}</b><br>Contagem: %{value}<br>Percentual: %{percent}<extra></extra>')

        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='var(--text)', size=11),
            height=320
        )
        return fig
    except Exception as e:
        st.error(f"[Debug] Erro ao criar figura do Donut: {e}")
        return None


# --- FUNÇÃO PARA O MAPA ---
map_centers_zoom = {
    'AC': {'lat': -9.02, 'lon': -70.81, 'zoom': 6}, 'AL': {'lat': -9.57, 'lon': -36.78, 'zoom': 7},
    'AP': {'lat': 1.41, 'lon': -51.77, 'zoom': 6}, 'AM': {'lat': -3.41, 'lon': -65.85, 'zoom': 5},
    'BA': {'lat': -12.96, 'lon': -41.82, 'zoom': 5.5}, 'CE': {'lat': -5.20, 'lon': -39.53, 'zoom': 6.5},
    'DF': {'lat': -15.78, 'lon': -47.92, 'zoom': 8}, 'ES': {'lat': -19.18, 'lon': -40.30, 'zoom': 7},
    'GO': {'lat': -15.82, 'lon': -49.83, 'zoom': 6}, 'MA': {'lat': -5.42, 'lon': -45.44, 'zoom': 5.5},
    'MT': {'lat': -12.64, 'lon': -55.42, 'zoom': 5}, 'MS': {'lat': -20.51, 'lon': -54.52, 'zoom': 6},
    'MG': {'lat': -18.51, 'lon': -44.55, 'zoom': 5.5}, 'PA': {'lat': -3.79, 'lon': -52.48, 'zoom': 5},
    'PB': {'lat': -7.06, 'lon': -36.72, 'zoom': 7}, 'PR': {'lat': -25.25, 'lon': -52.02, 'zoom': 6},
    'PE': {'lat': -8.38, 'lon': -37.86, 'zoom': 6}, 'PI': {'lat': -7.22, 'lon': -42.72, 'zoom': 6},
    'RJ': {'lat': -22.18, 'lon': -42.44, 'zoom': 7}, 'RN': {'lat': -5.81, 'lon': -36.56, 'zoom': 7},
    'RS': {'lat': -30.01, 'lon': -53.53, 'zoom': 6}, 'RO': {'lat': -10.83, 'lon': -63.34, 'zoom': 6},
    'RR': {'lat': 2.73, 'lon': -61.22, 'zoom': 6}, 'SC': {'lat': -27.45, 'lon': -50.21, 'zoom': 6.5},
    'SP': {'lat': -22.19, 'lon': -48.79, 'zoom': 6}, 'SE': {'lat': -10.57, 'lon': -37.38, 'zoom': 7.5},
    'TO': {'lat': -9.46, 'lon': -48.26, 'zoom': 6}
}
BR_CENTER = {"lat": -14.2350, "lon": -51.9253}
BR_ZOOM = 3

def criar_mapa_brasil(df_para_contagem, geojson_data, estado_foco=None):
    """
    Cria e retorna a figura do mapa coroplético do Brasil.
    Usa df_para_contagem para calcular os inscritos por estado.
    Se 'estado_foco' for fornecido, o mapa dará zoom nesse estado.
    """
    if geojson_data is None:
        st.warning("GeoJSON não carregado, não é possível criar o mapa.")
        return None # Retorna None se GeoJSON falhou ao carregar
    
    if df_para_contagem.empty or 'SG_UF_PROVA' not in df_para_contagem.columns:
         st.warning("DataFrame vazio ou sem coluna 'SG_UF_PROVA' para o mapa.")
         return None

    df_mapa_data = df_para_contagem.dropna(subset=['SG_UF_PROVA'])
    if df_mapa_data.empty:
        st.warning("DataFrame sem dados de estado válidos para o mapa.")
        return None

    # Agrupa para obter a contagem por estado
    df_mapa = df_mapa_data.groupby('SG_UF_PROVA').agg(
        contagem_inscritos = pd.NamedAgg(column='NU_INSCRICAO', aggfunc='count')
    ).reset_index()

    if df_mapa.empty:
        st.warning("Agrupamento por estado resultou em dados vazios para o mapa.")
        return None
    
    # Determina o centro e o zoom
    if estado_foco and estado_foco in map_centers_zoom:
        map_zoom = map_centers_zoom[estado_foco]['zoom']
        map_center = {"lat": map_centers_zoom[estado_foco]['lat'], "lon": map_centers_zoom[estado_foco]['lon']}
        opacity_map = {estado: 1.0 if estado == estado_foco else 0.5 for estado in df_mapa['SG_UF_PROVA']}
        marker_opacity = [opacity_map.get(loc, 0.5) for loc in df_mapa['SG_UF_PROVA']]

    else:
        map_zoom = BR_ZOOM
        map_center = BR_CENTER
        marker_opacity = 0.8


    try:
        fig = go.Figure(go.Choroplethmapbox(
            geojson=geojson_data,
            locations=df_mapa['SG_UF_PROVA'],
            featureidkey="properties.sigla",
            z=df_mapa['contagem_inscritos'],
            colorscale="viridis_r",
            zmin=0,
            zmax=df_mapa['contagem_inscritos'].max() if not df_mapa['contagem_inscritos'].empty else 1,
            marker_opacity=marker_opacity,
            marker_line_width=0.5,
            marker_line_color='rgba(42, 48, 88, 0.5)',
            colorbar=dict(
                title=dict(
                    text='Inscritos',
                    font=dict(color='var(--text)')
                ),
                bgcolor='rgba(42, 48, 88, 0.7)',
                tickfont=dict(color='var(--text)')
            ),
            hovertemplate='<b>%{location}</b><br>Inscritos: %{z}<extra></extra>'
        ))

        fig.update_layout(
            mapbox_style="carto-positron", 
            mapbox_zoom=map_zoom,
            mapbox_center=map_center,
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        return fig
    except Exception as e:
        st.error(f"Erro ao criar figura do mapa: {e}")
        return None


# Função placeholder para o mapa (Fallback)
def placeholder_mapa():
    map_icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6"><path fill-rule="evenodd" d="M8.161 2.58a1.875 1.875 0 0 1 1.678 0l4.993 2.498c.106.052.23.052.336 0l4.993-2.498a1.875 1.875 0 0 1 2.349 1.678V15.36a1.875 1.875 0 0 1-1.678 1.846l-4.993 1.248a1.875 1.875 0 0 1-.336 0l-4.993-1.248a1.875 1.875 0 0 0-1.678 0l-4.993 1.248A1.875 1.875 0 0 1 .75 15.36V4.258c0-.751.43-1.43.912-1.745l4.993-2.498a1.875 1.875 0 0 1 1.506.567zM10.5 6a.75.75 0 0 1 .75.75v6.563l2.25-1.125a.75.75 0 0 1 1.002 1.002l-3.75 3.75a.75.75 0 0 1-1.002 0L6.75 13.19l1.002-1.002a.75.75 0 0 1 1.002 0l1 .5V6.75A.75.75 0 0 1 10.5 6z" clip-rule="evenodd" /><path d="M11.96 18.937a1.875 1.875 0 0 1-1.678 0l-4.993-1.248a1.875 1.875 0 0 1-1.506-.567V19.5c0 .933.743 1.705 1.678 1.846l4.993 1.248c.106.026.23.026.336 0l4.993-1.248A1.875 1.875 0 0 0 18.75 19.5v-2.375a1.875 1.875 0 0 1-1.506.567L11.96 18.937z" /></svg>"""
    
    return f"""<div class='map-placeholder'>{map_icon_svg}<p>Mapa Interativo do Brasil<br><small>(Falha ao carregar ou sem dados)</small></p></div>"""

def criar_barras_cidades(df_filtrado):
    """ Cria o gráfico de barras para o Top 10 cidades (municípios) no df_filtrado. """
    if df_filtrado.empty or 'NO_MUNICIPIO_PROVA' not in df_filtrado.columns:
        st.warning("Dados de município não disponíveis para o gráfico de cidades.")
        return None
    
    df_cidades_data = df_filtrado.dropna(subset=['NO_MUNICIPIO_PROVA'])
    df_cidades_data = df_cidades_data[df_cidades_data['NO_MUNICIPIO_PROVA'].str.strip() != '']
    if df_cidades_data.empty:
        st.warning("Nenhum dado de município válido encontrado para o gráfico de cidades.")
        return None

    df_cidades = df_cidades_data.groupby('NO_MUNICIPIO_PROVA').agg(
        Inscritos=pd.NamedAgg(column='NU_INSCRICAO', aggfunc='count')
    ).reset_index().sort_values(by='Inscritos', ascending=False)
    
    # Pega o Top 10
    df_top_cidades = df_cidades.head(10).sort_values(by='Inscritos', ascending=True)
    
    if df_top_cidades.empty:
        st.warning("Não há cidades suficientes para gerar o Top 10.")
        return None
        
    estado_nome = st.session_state.clicked_estado or "Brasil"
    
    try:
        fig = px.bar(df_top_cidades, y='NO_MUNICIPIO_PROVA', x='Inscritos',
                     title=f"Top 10 Cidades em {estado_nome}",
                     color_discrete_sequence=['#f4a261'])
        
        fig.update_traces(hovertemplate='<b>%{y}</b><br>Inscritos: %{x}<extra></extra>')
        
        fig.update_layout(
            showlegend=False,
            margin=dict(t=50, b=10, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='var(--text)', size=11),
            title_font_size=16,
            title_x=0.05,
            title_y=0.95,
            yaxis_title=None,
            xaxis_title="Total de Inscritos",
            height=320
        )
        return fig
    except Exception as e:
        st.error(f"[Debug] Erro ao criar figura Cidades: {e}")
        return None


def criar_barras_medias(df_filtrado):
    """ Cria o gráfico de barras para as médias por área de conhecimento. """
    cols_notas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    if df_filtrado.empty or not all(col in df_filtrado.columns for col in cols_notas):
        return None

    medias = df_filtrado[cols_notas].mean().reset_index()
    medias.columns = ['Area_Code', 'Media']

    map_areas = {
        'NU_NOTA_CN': 'Ciências Nat.',
        'NU_NOTA_CH': 'Ciências Hum.',
        'NU_NOTA_LC': 'Linguagens',
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_REDACAO': 'Redação'
    }
    medias['Area'] = medias['Area_Code'].map(map_areas)

    try:
        fig = px.bar(medias, x='Area', y='Media',
                     title="Média por Área de Conhecimento",
                     color='Area',
                     color_discrete_map={
                         'Ciências Nat.': '#2a9d8f',
                         'Ciências Hum.': '#e9c46a',
                         'Linguagens': '#f4a261',
                         'Matemática': '#e76f51',
                         'Redação': '#a95aed'
                     })

        fig.update_traces(hovertemplate='<b>%{x}</b><br>Média: %{y:.2f}<extra></extra>')

        fig.update_layout(
            showlegend=False,
            margin=dict(t=50, b=10, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='var(--text)', size=11),
            title_font_size=16,
            title_x=0.05,
            title_y=0.95,
            yaxis_title="Média",
            xaxis_title=None,
            height=320 
        )
        return fig
    except Exception as e:
        st.error(f"[Debug] Erro ao criar figura Barras: {e}")
        return None

def criar_histograma_redacao(df_filtrado):
    """ Cria o histograma de dispersão das notas de redação. """
    if df_filtrado.empty or 'NU_NOTA_REDACAO' not in df_filtrado.columns:
        return None

    df_redacao = df_filtrado.dropna(subset=['NU_NOTA_REDACAO'])
    if df_redacao.empty:
        return None

    try:
        fig = px.histogram(df_redacao, x='NU_NOTA_REDACAO',
                             title="Dispersão das Notas de Redação",
                             color_discrete_sequence=['#a95aed'])

        fig.update_traces(hovertemplate='Nota: %{x}<br>Contagem: %{y}<extra></extra>')

        fig.update_layout(
            showlegend=False,
            margin=dict(t=50, b=10, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='var(--text)', size=11),
            title_font_size=16,
            title_x=0.05,
            title_y=0.95,
            yaxis_title="Contagem",
            xaxis_title="Nota da Redação",
            bargap=0.1,
            height=320 
        )
        return fig
    except Exception as e:
        st.error(f"[Debug] Erro ao criar figura Histograma: {e}")
        return None

def criar_heatmap_correlacao(df_filtrado):
    """ Cria o heatmap de correlação entre as áreas. """
    cols_notas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    if df_filtrado.empty or not all(col in df_filtrado.columns for col in cols_notas):
        return None

    df_corr = df_filtrado[cols_notas].dropna()
    if len(df_corr) < 2:
        return None 

    corr = df_corr.corr()

    cols_notas_map = {
        'NU_NOTA_CN': 'Ciências Nat.',
        'NU_NOTA_CH': 'Ciências Hum.',
        'NU_NOTA_LC': 'Linguagens',
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_REDACAO': 'Redação'
    }
    corr.columns = [cols_notas_map.get(c, c) for c in corr.columns]
    corr.index = [cols_notas_map.get(i, i) for i in corr.index]

    try:
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            colorscale='viridis_r',
            text=corr.values,
            texttemplate="%{text:.2f}",
            textfont={"size":10, "color": "white"},
            hovertemplate='<b>%{x}</b> x <b>%{y}</b><br>Correlação: %{z:.2f}<extra></extra>'
        ))

        fig.update_layout(
            title="Correlação entre Áreas de Conhecimento",
            margin=dict(t=50, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='var(--text)', size=11),
            title_font_size=16,
            title_x=0.05,
            title_y=0.98, 
            height=712, # Altura alta
            yaxis_autorange='reversed' # Garante que a diagonal esteja correta
        )
        return fig
    except Exception as e:
        st.error(f"[Debug] Erro ao criar figura Heatmap: {e}")
        return None


def grid_analise_placeholder():
    """Cria a grade de análise vazia (2 caixas + 1 alta)."""
    g1, g2 = st.columns([1.4, 1], gap="small")
    with g1:
        # Usa as classes CSS para os placeholders vazios
        st.markdown("<div class='w-box-placeholder'></div>", unsafe_allow_html=True)
        gap(12)
        st.markdown("<div class='w-box-placeholder'></div>", unsafe_allow_html=True)
    with g2:
        st.markdown("<div class='w-tall-placeholder'></div>", unsafe_allow_html=True)

# --- LÓGICA DE FILTROS ---
# Aplica filtros da sidebar PRIMEIRO
df_sidebar_filtrado = df_principal.copy() if not df_principal.empty else pd.DataFrame() 

# 1. Filtro de Ano (Range) - Sidebar
try:
    # Acessa valores do session_state
    ano_inicio_sel = st.session_state.get('sel_ano_inicio')
    ano_fim_sel = st.session_state.get('sel_ano_fim')
    if ano_inicio_sel and ano_fim_sel and 'NU_ANO' in df_sidebar_filtrado.columns:
        ano_inicio_int = int(ano_inicio_sel)
        ano_fim_int = int(ano_fim_sel)
        if ano_inicio_int > ano_fim_int: ano_inicio_int, ano_fim_int = ano_fim_int, ano_inicio_int # Corrige ordem se necessário
        
        # Garante que a coluna é numérica antes de comparar
        df_sidebar_filtrado['NU_ANO'] = pd.to_numeric(df_sidebar_filtrado['NU_ANO'], errors='coerce')
        df_sidebar_filtrado = df_sidebar_filtrado[
            df_sidebar_filtrado['NU_ANO'].notna() &
            (df_sidebar_filtrado['NU_ANO'] >= ano_inicio_int) &
            (df_sidebar_filtrado['NU_ANO'] <= ano_fim_int)
        ]
except ValueError: st.warning("Anos selecionados inválidos.")
except Exception as e: st.warning(f"Não foi possível aplicar filtro de ano: {e}")

# 2. Filtro de Estado - Sidebar
try:
    # Acessa o valor do estado selecionado diretamente do session_state
    estado_sidebar = st.session_state.get('sel_estado', "Todos")
    if estado_sidebar != "Todos" and 'SG_UF_PROVA' in df_sidebar_filtrado.columns:
        df_sidebar_filtrado = df_sidebar_filtrado[df_sidebar_filtrado['SG_UF_PROVA'] == estado_sidebar]
except Exception as e: st.warning(f"Não foi possível aplicar filtro de estado: {e}")

# 3. Filtro de Município - Sidebar
try:
    # Acessa o valor do município selecionado diretamente do session_state
    municipio_sidebar = st.session_state.get('sel_municipio', "Todos")
    if municipio_sidebar != "Todos" and 'NO_MUNICIPIO_PROVA' in df_sidebar_filtrado.columns:
        df_sidebar_filtrado = df_sidebar_filtrado[df_sidebar_filtrado['NO_MUNICIPIO_PROVA'] == municipio_sidebar]
except Exception as e: st.warning(f"Não foi possível aplicar filtro de município: {e}")


# 4. Filtro de Gênero - Sidebar
try:
    genero_sidebar = st.session_state.get('sel_genero', "Todos")
    if 'TP_SEXO' in df_sidebar_filtrado.columns:
        if genero_sidebar == "Feminino":
            df_sidebar_filtrado = df_sidebar_filtrado[df_sidebar_filtrado['TP_SEXO'] == 'F']
        elif genero_sidebar == "Masculino":
            df_sidebar_filtrado = df_sidebar_filtrado[df_sidebar_filtrado['TP_SEXO'] == 'M']
except Exception as e: st.warning(f"Não foi possível aplicar filtro de gênero: {e}")

# 5. Filtro de Faixa Etária - Sidebar
try:
    faixa_sidebar = st.session_state.get('sel_faixa_etaria', "Todos")
    if faixa_sidebar != "Todos" and 'TP_FAIXA_ETARIA' in df_sidebar_filtrado.columns:
        map_faixa_reverso = {v: k for k, v in map_faixa_etaria.items()}
        codigo_faixa = map_faixa_reverso.get(faixa_sidebar)
        if codigo_faixa is not None:
            # Garante que a coluna é numérica antes de comparar
            df_sidebar_filtrado['TP_FAIXA_ETARIA'] = pd.to_numeric(df_sidebar_filtrado['TP_FAIXA_ETARIA'], errors='coerce')
            df_sidebar_filtrado = df_sidebar_filtrado[df_sidebar_filtrado['TP_FAIXA_ETARIA'].notna() & (df_sidebar_filtrado['TP_FAIXA_ETARIA'] == codigo_faixa)]
except Exception as e: st.warning(f"Não foi possível aplicar filtro de faixa etária: {e}")

# 6. Filtro de Escolaridade - Sidebar
try:
    escolaridade_sidebar = st.session_state.get('sel_escolaridade', "Todos")
    if escolaridade_sidebar != "Todos" and 'TP_ST_CONCLUSAO' in df_sidebar_filtrado.columns:
        map_conclusao_reverso = {v: k for k, v in map_conclusao.items()}
        codigo_conclusao = map_conclusao_reverso.get(escolaridade_sidebar)
        if codigo_conclusao is not None:
             # Garante que a coluna é numérica antes de comparar
            df_sidebar_filtrado['TP_ST_CONCLUSAO'] = pd.to_numeric(df_sidebar_filtrado['TP_ST_CONCLUSAO'], errors='coerce')
            df_sidebar_filtrado = df_sidebar_filtrado[df_sidebar_filtrado['TP_ST_CONCLUSAO'].notna() & (df_sidebar_filtrado['TP_ST_CONCLUSAO'] == codigo_conclusao)]
except Exception as e: st.warning(f"Não foi possível aplicar filtro de escolaridade: {e}")


# ==================================================================
# === LÓGICA DE CROSS-FILTERING (Drill-down do Mapa) ===
# ==================================================================
df_filtrado = df_sidebar_filtrado.copy() # Começa com os filtros da sidebar
filtro_estado_ativo = None # Inicia como None

# Verifica se um estado foi clicado no mapa
if 'clicked_estado' in st.session_state and st.session_state.clicked_estado:
    # Só aplica o filtro do mapa se NENHUM estado estiver selecionado na sidebar
    # E NENHUM município estiver selecionado na sidebar
    if st.session_state.get('sel_estado', "Todos") == "Todos" and \
       st.session_state.get('sel_municipio', "Todos") == "Todos":
        
        filtro_estado_ativo = st.session_state.clicked_estado
        # Aplica o filtro do mapa SOBRE os filtros já aplicados (ano, genero, etc.)
        if 'SG_UF_PROVA' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['SG_UF_PROVA'] == filtro_estado_ativo]
        else:
             st.warning("Coluna 'SG_UF_PROVA' não encontrada para aplicar filtro do mapa.")
             
    else:
        # Se um estado OU município já está selecionado na sidebar, ele tem prioridade.
        st.session_state.clicked_estado = None
        filtro_estado_ativo = None # Garante que a flag seja None
        

# --- CÁLCULO DOS KPIs (Após TODOS os filtros) ---
total_inscritos = df_filtrado.shape[0] if not df_filtrado.empty else 0

total_confirmados = 0
total_presentes = 0
total_ausentes_dia = 0
if 'INDICADOR_ABSENTEISMO' in df_filtrado.columns and not df_filtrado.empty:
      indicador_abs_series = df_filtrado['INDICADOR_ABSENTEISMO'].astype(str)
      total_confirmados = (indicador_abs_series != 'Ausente em um ou mais dias').sum()
      total_presentes = (indicador_abs_series == 'Presente').sum()
      total_ausentes_dia = (indicador_abs_series == 'Ausente em um ou mais dias').sum()


# % Presentes = Presentes / Total Inscritos
perc_presentes = (total_presentes / total_inscritos) if total_inscritos > 0 else 0.0
# % Ausentes = Ausentes (pelo menos 1 dia) / Total Inscritos
perc_ausentes = (total_ausentes_dia / total_inscritos) if total_inscritos > 0 else 0.0


media_geral = df_filtrado['MEDIA_GERAL'].mean() if 'MEDIA_GERAL' in df_filtrado.columns and not df_filtrado.empty else np.nan
media_redacao = df_filtrado['NU_NOTA_REDACAO'].mean() if 'NU_NOTA_REDACAO' in df_filtrado.columns and not df_filtrado.empty else np.nan

total_lingua = 0
cont_ingles = 0
cont_espanhol = 0
if 'TP_LINGUA' in df_filtrado.columns and not df_filtrado.empty:
    lingua_series = df_filtrado['TP_LINGUA'].dropna() # Remove NaN antes de contar
    cont_ingles = (lingua_series == 0).sum()
    cont_espanhol = (lingua_series == 1).sum()
    total_lingua = cont_ingles + cont_espanhol

perc_ingles = (cont_ingles / total_lingua) if total_lingua > 0 else 0.0
perc_espanhol = (cont_espanhol / total_lingua) if total_lingua > 0 else 0.0


# --- LINHA SUPERIOR DE KPIs ---
kpi_cols = st.columns([1, 1, 1.5, 1, 1], gap="small")
with kpi_cols[0]: st.markdown(criar_kpi("Total Inscritos", total_inscritos), unsafe_allow_html=True)
with kpi_cols[1]: st.markdown(criar_kpi("Total Confirmados", total_confirmados), unsafe_allow_html=True)
with kpi_cols[2]: st.markdown(criar_kpi_presenca("% Presentes x Ausentes", perc_presentes, perc_ausentes), unsafe_allow_html=True)
with kpi_cols[3]: st.markdown(criar_kpi("Média Geral", media_geral, formato="{:,.2f}"), unsafe_allow_html=True)
with kpi_cols[4]: st.markdown(criar_kpi("Média Nota da Redação", media_redacao, formato="{:,.2f}"), unsafe_allow_html=True)

gap(8)

# --- LINHA KPI LINGUAGEM ---
kpi_lang_cols = st.columns([1, 3], gap="small")
with kpi_lang_cols[0]: st.markdown(criar_kpi_lingua("Linguagem Estrangeira", cont_ingles, cont_espanhol, perc_ingles, perc_espanhol), unsafe_allow_html=True)


# --- Exibe indicador de filtro ativo (Drill-down) ---
if filtro_estado_ativo:
    st.info(f"Filtro de Drill-Down Ativo: Estado = {filtro_estado_ativo}. Clique no estado novamente no mapa ou em 'Limpar Filtros' para remover.")


# --- SEÇÕES DO DASHBOARD ---
gap(6); section("Análise Geográfica e Demográfica")

# --- Estrutura com Placeholders ---
col1, col2 = st.columns([1.4, 1], gap="small")

with col1:
    placeholder_esquerda_sup = st.empty()
    gap(12)
    placeholder_esquerda_inf = st.empty() # <- Vai conter o Gênero ou Cidades

with col2:
    placeholder_direita = st.empty() # <- Vai conter o Mapa interativo


# --- GERAÇÃO DOS DADOS E FIGURAS (Após filtros) ---
df_tabela = criar_tabela_anual(df_filtrado)

# O mapa usa o df_principal para DESENHAR todos os estados, mas aplica FOCO se houver drilldown
fig_mapa = criar_mapa_brasil(df_principal, geojson_brasil, estado_foco=filtro_estado_ativo)

# Figuras de drill-down (Gênero ou Cidades) são geradas dentro do placeholder

# --- RENDERIZAÇÃO DENTRO DOS PLACEHOLDERS ---

with placeholder_esquerda_sup.container():
    st.dataframe(
         df_tabela,
         use_container_width=True,
         hide_index=True,
         column_config={
             "Ano": st.column_config.NumberColumn(format="%d", width="small"),
             "Total Inscritos": st.column_config.NumberColumn(format="%,d"),
             "Total Confirmados": st.column_config.NumberColumn(format="%,d"),
             "% Presentes": st.column_config.ProgressColumn(format="%.1f%%", min_value=0, max_value=1),
             "% Ausentes": st.column_config.ProgressColumn(format="%.1f%%", min_value=0, max_value=1),
         }
    )

with placeholder_esquerda_inf.container(border=False):
    if filtro_estado_ativo:
        # VISÃO DRILL-DOWN: MOSTRAR CIDADES
        fig_cidades = criar_barras_cidades(df_filtrado) # Usa o df_filtrado pelo estado
        if fig_cidades:
            st.plotly_chart(fig_cidades, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div class="chart-placeholder-box small">Dados de Cidades indisponíveis para este estado.</div>', unsafe_allow_html=True)
    else:
        # VISÃO PADRÃO: MOSTRAR GÊNERO (Usa o df_filtrado pela sidebar/municipio)
        fig_genero = criar_donut_genero(df_filtrado)
        if fig_genero:
             st.plotly_chart(fig_genero, use_container_width=True, config={"displayModeBar": False})
        else:
             # Exibe mensagem dentro de um container com estilo
             st.markdown('<div class="chart-placeholder-box small">Dados de Gênero indisponíveis para os filtros selecionados.</div>', unsafe_allow_html=True)


with placeholder_direita.container(border=False):
    if fig_mapa:
        # Usa plotly_events para capturar cliques
        selected_point = plotly_events(
            fig_mapa,
            click_event=True,
            hover_event=False, # Desativar hover pode ajudar em alguns casos
            key="map_click_event" # Chave única para este evento
        )

        # Lógica de Drill-down / Drill-up
        if selected_point: # Verifica se não é None ou lista vazia
             if isinstance(selected_point, list) and len(selected_point) > 0:
                 point_data = selected_point[0] # Pega o primeiro ponto clicado
                 clicked_location = point_data.get('location') # Tenta pegar a localização (estado)

                 if clicked_location:
                     # 1. Ignora clique se um estado OU município já está filtrado na sidebar
                     if st.session_state.get('sel_estado', "Todos") != "Todos" or \
                        st.session_state.get('sel_municipio', "Todos") != "Todos":
                         st.toast("Limpe os filtros de Estado/Município da sidebar para usar o drill-down do mapa.", icon="ℹ️")
                         # pass # Silenciosamente ignora o clique

                     # 2. Se clicou no mesmo estado que já está ativo no drill-down (Drill-up)
                     elif st.session_state.clicked_estado == clicked_location:
                         st.session_state.clicked_estado = None
                         st.rerun() # Re-executa o script para remover o filtro

                     # 3. Se clicou em um novo estado (Drill-down)
                     else:
                         st.session_state.clicked_estado = clicked_location
                         st.rerun() # Re-executa o script para aplicar o filtro

    else:
        st.markdown(placeholder_mapa(), unsafe_allow_html=True)


gap(18); section("Análise de Desempenho Acadêmico")

fig_barras = criar_barras_medias(df_filtrado)
fig_histograma = criar_histograma_redacao(df_filtrado)
fig_heatmap = criar_heatmap_correlacao(df_filtrado)

col_acad_1, col_acad_2 = st.columns([1.4, 1], gap="small")

with col_acad_1:
    # Gráfico de Barras - Médias
    with st.empty().container(border=False):
        if fig_barras:
            st.plotly_chart(fig_barras, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div class="chart-placeholder-box small">Dados de Média indisponíveis.</div>', unsafe_allow_html=True)

    gap(12)

    # Histograma - Dispersão Redação
    with st.empty().container(border=False):
        if fig_histograma:
            st.plotly_chart(fig_histograma, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div class="chart-placeholder-box small">Dados de Redação indisponíveis.</div>', unsafe_allow_html=True)

with col_acad_2:
    # Heatmap - Correlação
    with st.empty().container(border=False):
        if fig_heatmap:
            st.plotly_chart(fig_heatmap, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div class="chart-placeholder-box tall">Dados de Correlação indisponíveis.</div>', unsafe_allow_html=True)


gap(18); section("Análise por Perfil")
grid_analise_placeholder()

gap(18); section("Análise Socioeconômica")
grid_analise_placeholder()

gap(18); section("Comparativo de Grupos")
grid_analise_placeholder()

# ========================= PDF =========================
if gerar_pdf:
    st_html("""
    <script>
      const w = window.open('', '_blank', 'noopener,noreferrer');
      w.document.write('<html><head><title>Dashboard ENEM PDF</title><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"/>');
      const styles = document.querySelectorAll('style');
      styles.forEach(style => w.document.head.appendChild(style.cloneNode(true)));
      w.document.write('</head><body style="background-color: var(--bg-main) !important;">');
      const mainContent = document.querySelector('.main .block-container');
      if (mainContent) { w.document.write(mainContent.innerHTML); }
      else { w.document.write(document.body.innerHTML); }
      w.document.write('</body></html>');
      w.document.close();
      setTimeout(() => { w.focus(); w.print(); }, 1000);
    </script>
    """, height=0)