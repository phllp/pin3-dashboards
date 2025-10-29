from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from streamlit.components.v1 import html as st_html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 

import os
import numpy as np 

from db.connection import get_engine

st.set_page_config(page_title="Dashboard ENEM", layout="wide")


with open("styles.css") as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)



tabela =os.getenv('NOME_TABELA')



from db.queries import carregar_dados_db, buscar_municipios_por_estado


engine = get_engine()
    
df_principal, anos_disponiveis_db, faixas_disponiveis_num_db, conclusoes_disponiveis_num_db, geojson_brasil = carregar_dados_db(engine)

if df_principal.empty:
    st.error("Nenhum dado foi carregado do banco de dados. Verifique o SCRIPT.py e a conexão.")
    st.stop()


try:
    anos_options_fim = sorted(anos_disponiveis_db, key=int, reverse=True)
    anos_options_inicio = sorted(anos_disponiveis_db, key=int, reverse=False)

    map_faixa_etaria = {
        1: 'Menor de 17 anos', 2: '17 anos', 3: '18 anos', 4: '19 anos', 5: '20 anos',
        6: '21 anos', 7: '22 anos', 8: '23 anos', 9: '24 anos', 10: '25 anos',
        11: '26-30 anos', 12: '31-35 anos', 13: '36-40 anos', 14: '41-45 anos',
        15: '46-50 anos', 16: '51-55 anos', 17: '56-60 anos', 18: '61-65 anos',
        19: '66-70 anos', 20: 'Maior de 70 anos'
    }

    map_conclusao = {
        1: 'Já concluí o Ensino Médio',
        2: 'Estou cursando e concluirei em 2024', 
        3: 'Estou cursando e concluirei após 2024', 
        4: 'Não concluí e não estou cursando'
    }

    map_raca = {
        0: 'Não declarado',
        1: 'Branca',
        2: 'Preta',
        3: 'Parda',
        4: 'Amarela',
        5: 'Indígena'
    }

    map_treineiro = {
        0: 'Não (Oficial)',
        1: 'Sim (Treineiro)'
    }

    map_renda_full = {
        'A': 'Nenhuma renda', 'B': 'Até 1 SM', 'C': 'De 1 a 1.5 SM', 'D': 'De 1.5 a 2 SM',
        'E': 'De 2 a 2.5 SM', 'F': 'De 2.5 a 3 SM', 'G': 'De 3 a 4 SM', 'H': 'De 4 a 5 SM',
        'I': 'De 5 a 6 SM', 'J': 'De 6 a 7 SM', 'K': 'De 7 a 8 SM', 'L': 'De 8 a 9 SM',
        'M': 'De 9 a 10 SM', 'N': 'De 10 a 12 SM', 'O': 'De 12 a 15 SM', 'P': 'De 15 a 20 SM',
        'Q': 'Acima de 20 SM'
    }

    map_renda_numerico = {
        'A': 0.0, 'B': 1.0, 'C': 1.25, 'D': 1.75, 'E': 2.25, 'F': 2.75,
        'G': 3.5, 'H': 4.5, 'I': 5.5, 'J': 6.5, 'K': 7.5, 'L': 8.5,
        'M': 9.5, 'N': 11.0, 'O': 13.5, 'P': 17.5, 'Q': 20.0 
    }

    map_escolaridade_pais_full = {
        'A': 'Nunca estudou',
        'B': 'Não completou a 4ª série',
        'C': 'Completou a 4ª série',
        'D': 'Completou a 8ª série',
        'E': 'Completou o Ensino Médio',
        'F': 'Completou a Graduação',
        'G': 'Completou a Pós-Graduação',
        'H': 'Não sabe'
    }

    faixas_options = ["Todos"] + [map_faixa_etaria.get(f, f"Código {f}") for f in sorted([int(x) for x in faixas_disponiveis_num_db if pd.notna(x)])]
    conclusoes_options = ["Todos"] + [map_conclusao.get(c, f"Código {c}") for c in sorted([int(x) for x in conclusoes_disponiveis_num_db if pd.notna(x)])]

except Exception as e:
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
        st.selectbox("Início", options=anos_options_inicio, label_visibility="collapsed", key="sel_ano_inicio")
    with ano_col2:
        st.selectbox("Fim", options=anos_options_fim, label_visibility="collapsed", key="sel_ano_fim")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    st.selectbox("ESTADO", estados_brasileiros, key="sel_estado", on_change=atualizar_lista_municipios)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    st.selectbox("MUNICÍPIO", options=st.session_state.opcoes_municipio, key="sel_municipio")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    st.selectbox("GÊNERO", genero_opcoes, key="sel_genero")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    st.selectbox("FAIXA ETÁRIA", options=faixas_options, key="sel_faixa_etaria")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-group'>", unsafe_allow_html=True)
    st.selectbox("ESCOLARIDADE", options=conclusoes_options, key="sel_escolaridade")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    def limpar_filtros_callback():
        st.session_state.sel_estado = "Todos"
        st.session_state.sel_genero = "Todos"
        st.session_state.sel_faixa_etaria = "Todos"
        st.session_state.sel_escolaridade = "Todos"
        st.session_state.sel_ano_inicio = anos_options_inicio[ano_inicio_default_idx] if anos_options_inicio else None
        st.session_state.sel_ano_fim = anos_options_fim[ano_fim_default_idx] if anos_options_fim else None
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


def gap(h=10):
    st.markdown(f"<div style='height:{h}px'></div>", unsafe_allow_html=True)

def section(title: str):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

def criar_kpi(titulo, valor, formato="{:,}"):
    valor_formatado = "N/A"
    if pd.notna(valor):
        try:
            if isinstance(valor, (int, np.integer, float, np.floating)):
                if isinstance(valor, (int, np.integer)) or (isinstance(valor, (float, np.floating)) and valor == int(valor)):
                     valor_formatado = "{:,.0f}".format(valor).replace(",", ".")
                else:
                     valor_formatado = "{:,.2f}".format(valor).replace(",", "#").replace(".", ",").replace("#", ".")
            else:
                 valor_formatado = str(valor)
        except Exception as e:
             valor_formatado = "Erro"
    return f"<div class='kpi-container'><div class='kpi-title'>{titulo}</div><div class='kpi-value'>{valor_formatado}</div></div>"

def criar_kpi_presenca(titulo, val_pres, val_aus, formato_perc="{:.0%}"):
    val_pres_fmt = "N/A"; val_aus_fmt = "N/A"
    try:
        if pd.notna(val_pres): val_pres_fmt = formato_perc.format(val_pres)
        if pd.notna(val_aus): val_aus_fmt = formato_perc.format(val_aus)
    except Exception as e: pass
    return f"<div class='kpi-container'><div class='kpi-title'>{titulo}</div><div class='kpi-sub-row'><div class='kpi-sub-col'><div class='kpi-sub-val'>{val_pres_fmt}</div><div class='kpi-sub-title'>Presente</div></div><div class='kpi-separator'></div><div class='kpi-sub-col'><div class='kpi-sub-val'>{val_aus_fmt}</div><div class='kpi-sub-title'>Ausente</div></div></div></div>"

def criar_kpi_lingua(titulo, val_ing, val_esp, perc_ing, perc_esp, formato_num="{:,}"):
    val_ing_fmt = "N/A"; val_esp_fmt = "N/A"; perc_ing_fmt = "N/A"; perc_esp_fmt = "N/A"; barra_ing = 0; barra_esp = 0
    try:
        if pd.notna(val_ing): val_ing_fmt = formato_num.format(val_ing).replace(",", ".")
        if pd.notna(val_esp): val_esp_fmt = formato_num.format(val_esp).replace(",", ".")
        if pd.notna(perc_ing): perc_ing_fmt = f"{perc_ing*100:.0f}%"; barra_ing = max(0, min(100, perc_ing * 100))
        if pd.notna(perc_esp): perc_esp_fmt = f"{perc_esp*100:.0f}%"; barra_esp = max(0, min(100, perc_esp * 100))
    except Exception as e: pass
    return f"<div class='kpi-container'><div class='kpi-title'>{titulo}</div><div class='lang-kpi-content'><div><div class='lang-row'><span class='lang-title'>Inglês</span><span class='lang-value'>{val_ing_fmt}</span></div><div class='progress-bar-container'><div class='progress-bar-fill' style='width: {barra_ing}%;'></div></div></div><div><div class='lang-row'><span class='lang-title'>Espanhol</span><span class='lang-value'>{val_esp_fmt}</span></div><div class='progress-bar-container'><div class='progress-bar-fill' style='width: {barra_esp}%;'></div></div></div></div></div>"

def criar_tabela_anual(df_filtrado):
    if df_filtrado.empty or 'NU_ANO' not in df_filtrado.columns: return pd.DataFrame(columns=['Ano', 'Total Inscritos', 'Total Confirmados', '% Presentes', '% Ausentes'])
    df_agrupar = df_filtrado.dropna(subset=['NU_ANO']); df_agrupar = df_agrupar[pd.to_numeric(df_agrupar['NU_ANO'], errors='coerce').notna()]
    if df_agrupar.empty: return pd.DataFrame(columns=['Ano', 'Total Inscritos', 'Total Confirmados', '% Presentes', '% Ausentes'])
    df_agrupar['NU_ANO'] = df_agrupar['NU_ANO'].astype(int)
    df_anual = df_agrupar.groupby('NU_ANO').agg(total_inscritos=pd.NamedAgg(column='NU_INSCRICAO', aggfunc='count'), total_presentes=pd.NamedAgg(column='INDICADOR_ABSENTEISMO', aggfunc=lambda x: (x == 'Presente').sum()), total_ausentes_dia=pd.NamedAgg(column='INDICADOR_ABSENTEISMO', aggfunc=lambda x: (x == 'Ausente em um ou mais dias').sum())).reset_index()
    confirmados_mask = df_agrupar['INDICADOR_ABSENTEISMO'] != 'Ausente em um ou mais dias'
    if confirmados_mask.any(): df_confirmados_ano = df_agrupar[confirmados_mask].groupby('NU_ANO').size().rename('total_confirmados'); df_anual = pd.merge(df_anual, df_confirmados_ano, on='NU_ANO', how='left').fillna({'total_confirmados': 0})
    else: df_anual['total_confirmados'] = 0
    df_anual['total_confirmados'] = df_anual['total_confirmados'].astype(int)
    df_anual['perc_presentes'] = (df_anual['total_presentes'] / df_anual['total_inscritos']).replace([np.inf, -np.inf, np.nan], 0)
    df_anual['perc_ausentes'] = (df_anual['total_ausentes_dia'] / df_anual['total_inscritos']).replace([np.inf, -np.inf, np.nan], 0)
    df_anual.rename(columns={'NU_ANO': 'Ano', 'total_inscritos': 'Total Inscritos', 'total_confirmados': 'Total Confirmados', 'perc_presentes': '% Presentes', 'perc_ausentes': '% Ausentes'}, inplace=True)
    return df_anual[['Ano', 'Total Inscritos', 'Total Confirmados', '% Presentes', '% Ausentes']].sort_values(by='Ano', ascending=False)

def criar_donut_genero(df_filtrado):
    if df_filtrado.empty or 'TP_SEXO' not in df_filtrado.columns or df_filtrado['TP_SEXO'].isnull().all(): return None
    df_genero_data = df_filtrado.dropna(subset=['TP_SEXO']); 
    if df_genero_data.empty: return None
    df_genero = df_genero_data['TP_SEXO'].astype(str).value_counts().reset_index(); 
    if df_genero.empty: return None
    df_genero.columns = ['Genero_Code', 'Count']; df_genero['Genero'] = df_genero['Genero_Code'].map({'F': 'Feminino', 'M': 'Masculino'}).fillna('Não declarado')
    if df_genero.empty: return None
    try:
        fig = px.pie(df_genero, names='Genero', values='Count', hole=0.6, color_discrete_map={'Feminino': '#a95aed', 'Masculino': '#4a5b96', 'Não declarado': '#777'})
        fig.update_traces(textposition='outside', textinfo='percent+label', marker=dict(line=dict(color= 'var(--panel)', width=4)), pull=[0.02] * len(df_genero), hovertemplate='<b>%{label}</b><br>Contagem: %{value}<br>Percentual: %{percent}<extra></extra>')
        fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--text)', size=11), height=320)
        return fig
    except Exception as e: return None

map_centers_zoom = {'AC': {'lat': -9.02, 'lon': -70.81, 'zoom': 6}, 'AL': {'lat': -9.57, 'lon': -36.78, 'zoom': 7}, 'AP': {'lat': 1.41, 'lon': -51.77, 'zoom': 6}, 'AM': {'lat': -3.41, 'lon': -65.85, 'zoom': 5}, 'BA': {'lat': -12.96, 'lon': -41.82, 'zoom': 5.5}, 'CE': {'lat': -5.20, 'lon': -39.53, 'zoom': 6.5}, 'DF': {'lat': -15.78, 'lon': -47.92, 'zoom': 8}, 'ES': {'lat': -19.18, 'lon': -40.30, 'zoom': 7}, 'GO': {'lat': -15.82, 'lon': -49.83, 'zoom': 6}, 'MA': {'lat': -5.42, 'lon': -45.44, 'zoom': 5.5}, 'MT': {'lat': -12.64, 'lon': -55.42, 'zoom': 5}, 'MS': {'lat': -20.51, 'lon': -54.52, 'zoom': 6}, 'MG': {'lat': -18.51, 'lon': -44.55, 'zoom': 5.5}, 'PA': {'lat': -3.79, 'lon': -52.48, 'zoom': 5}, 'PB': {'lat': -7.06, 'lon': -36.72, 'zoom': 7}, 'PR': {'lat': -25.25, 'lon': -52.02, 'zoom': 6}, 'PE': {'lat': -8.38, 'lon': -37.86, 'zoom': 6}, 'PI': {'lat': -7.22, 'lon': -42.72, 'zoom': 6}, 'RJ': {'lat': -22.18, 'lon': -42.44, 'zoom': 7}, 'RN': {'lat': -5.81, 'lon': -36.56, 'zoom': 7}, 'RS': {'lat': -30.01, 'lon': -53.53, 'zoom': 6}, 'RO': {'lat': -10.83, 'lon': -63.34, 'zoom': 6}, 'RR': {'lat': 2.73, 'lon': -61.22, 'zoom': 6}, 'SC': {'lat': -27.45, 'lon': -50.21, 'zoom': 6.5}, 'SP': {'lat': -22.19, 'lon': -48.79, 'zoom': 6}, 'SE': {'lat': -10.57, 'lon': -37.38, 'zoom': 7.5}, 'TO': {'lat': -9.46, 'lon': -48.26, 'zoom': 6}}
BR_CENTER = {"lat": -14.2350, "lon": -51.9253}; BR_ZOOM = 3

def criar_mapa_brasil(df_para_contagem, geojson_data):
    if geojson_data is None: return None
    if df_para_contagem.empty or 'SG_UF_PROVA' not in df_para_contagem.columns: return None
    df_mapa_data = df_para_contagem.dropna(subset=['SG_UF_PROVA']); 
    if df_mapa_data.empty: return None
    df_mapa = df_mapa_data.groupby('SG_UF_PROVA').agg(contagem_inscritos = pd.NamedAgg(column='NU_INSCRICAO', aggfunc='count')).reset_index()
    if df_mapa.empty: return None
    
    map_zoom = BR_ZOOM
    map_center = BR_CENTER
    marker_opacity = 0.8 

    try:
        fig = go.Figure(go.Choroplethmapbox(
            geojson=geojson_data, locations=df_mapa['SG_UF_PROVA'], featureidkey="properties.sigla",
            z=df_mapa['contagem_inscritos'], colorscale="viridis_r", zmin=0,
            zmax=df_mapa['contagem_inscritos'].max() if not df_mapa['contagem_inscritos'].empty else 1,
            marker_opacity=marker_opacity, marker_line_width=0.5, marker_line_color='rgba(42, 48, 88, 0.5)',
            colorbar=dict(title=dict(text='Inscritos', font=dict(color='var(--text)')), bgcolor='rgba(42, 48, 88, 0.7)', tickfont=dict(color='var(--text)')),
            hovertemplate='<b>%{location}</b><br>Inscritos: %{z}<extra></extra>'
        ))
        fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=map_zoom, mapbox_center=map_center, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig
    except Exception as e: return None

def placeholder_mapa():
    map_icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6"><path fill-rule="evenodd" d="M8.161 2.58a1.875 1.875 0 0 1 1.678 0l4.993 2.498c.106.052.23.052.336 0l4.993-2.498a1.875 1.875 0 0 1 2.349 1.678V15.36a1.875 1.875 0 0 1-1.678 1.846l-4.993 1.248a1.875 1.875 0 0 1-.336 0l-4.993-1.248a1.875 1.875 0 0 0-1.678 0l-4.993 1.248A1.875 1.875 0 0 1 .75 15.36V4.258c0-.751.43-1.43.912-1.745l4.993-2.498a1.875 1.875 0 0 1 1.506.567zM10.5 6a.75.75 0 0 1 .75.75v6.563l2.25-1.125a.75.75 0 0 1 1.002 1.002l-3.75 3.75a.75.75 0 0 1-1.002 0L6.75 13.19l1.002-1.002a.75.75 0 0 1 1.002 0l1 .5V6.75A.75.75 0 0 1 10.5 6z" clip-rule="evenodd" /><path d="M11.96 18.937a1.875 1.875 0 0 1-1.678 0l-4.993-1.248a1.875 1.875 0 0 1-1.506-.567V19.5c0 .933.743 1.705 1.678 1.846l4.993 1.248c.106.026.23.026.336 0l4.993-1.248A1.875 1.875 0 0 0 18.75 19.5v-2.375a1.875 1.875 0 0 1-1.506.567L11.96 18.937z" /></svg>"""
    return f"""<div class='map-placeholder'>{map_icon_svg}<p>Mapa Interativo do Brasil<br><small>(Falha ao carregar ou sem dados)</small></p></div>"""

def criar_barras_cidades(df_filtrado):
    if df_filtrado.empty or 'NO_MUNICIPIO_PROVA' not in df_filtrado.columns: return None
    df_cidades_data = df_filtrado.dropna(subset=['NO_MUNICIPIO_PROVA']); df_cidades_data = df_cidades_data[df_cidades_data['NO_MUNICIPIO_PROVA'].str.strip() != '']
    if df_cidades_data.empty: return None
    df_cidades = df_cidades_data.groupby('NO_MUNICIPIO_PROVA').agg(Inscritos=pd.NamedAgg(column='NU_INSCRICAO', aggfunc='count')).reset_index().sort_values(by='Inscritos', ascending=False)
    df_top_cidades = df_cidades.head(10).sort_values(by='Inscritos', ascending=True)
    if df_top_cidades.empty: return None
    estado_nome = st.session_state.get('sel_estado', "Todos") 
    if estado_nome == "Todos": estado_nome = "Brasil"
    try:
        fig = px.bar(df_top_cidades, y='NO_MUNICIPIO_PROVA', x='Inscritos', title=f"Top 10 Cidades em {estado_nome}", color_discrete_sequence=['#f4a261'])
        fig.update_traces(hovertemplate='<b>%{y}</b><br>Inscritos: %{x}<extra></extra>')
        fig.update_layout(showlegend=False, margin=dict(t=50, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--text)', size=11), title_font_size=16, title_x=0.05, title_y=0.95, yaxis_title=None, xaxis_title="Total de Inscritos", height=320)
        return fig
    except Exception as e: return None

def criar_barras_medias(df_filtrado):
    cols_notas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    if df_filtrado.empty or not all(col in df_filtrado.columns for col in cols_notas): return None
    medias = df_filtrado[cols_notas].mean().reset_index(); medias.columns = ['Area_Code', 'Media']
    map_areas = {'NU_NOTA_CN': 'Ciências Nat.', 'NU_NOTA_CH': 'Ciências Hum.', 'NU_NOTA_LC': 'Linguagens', 'NU_NOTA_MT': 'Matemática', 'NU_NOTA_REDACAO': 'Redação'}
    medias['Area'] = medias['Area_Code'].map(map_areas)
    try:
        fig = px.bar(medias, x='Area', y='Media', title="Média por Área de Conhecimento", color='Area', color_discrete_map={'Ciências Nat.': '#2a9d8f', 'Ciências Hum.': '#e9c46a', 'Linguagens': '#f4a261', 'Matemática': '#e76f51', 'Redação': '#a95aed'})
        fig.update_traces(hovertemplate='<b>%{x}</b><br>Média: %{y:.2f}<extra></extra>')
        fig.update_layout(showlegend=False, margin=dict(t=50, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--text)', size=11), title_font_size=16, title_x=0.05, title_y=0.95, yaxis_title="Média", xaxis_title=None, height=320)
        return fig
    except Exception as e: return None

def criar_histograma_redacao(df_filtrado):
    if df_filtrado.empty or 'NU_NOTA_REDACAO' not in df_filtrado.columns: return None
    df_redacao = df_filtrado.dropna(subset=['NU_NOTA_REDACAO']); 
    if df_redacao.empty: return None
    try:
        fig = px.histogram(df_redacao, x='NU_NOTA_REDACAO', title="Dispersão das Notas de Redação", color_discrete_sequence=['#a95aed'])
        fig.update_traces(hovertemplate='Nota: %{x}<br>Contagem: %{y}<extra></extra>')
        fig.update_layout(showlegend=False, margin=dict(t=50, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--text)', size=11), title_font_size=16, title_x=0.05, title_y=0.95, yaxis_title="Contagem", xaxis_title="Nota da Redação", bargap=0.1, height=320)
        return fig
    except Exception as e: return None

def criar_heatmap_correlacao(df_filtrado):
    cols_notas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    if df_filtrado.empty or not all(col in df_filtrado.columns for col in cols_notas): return None
    df_corr = df_filtrado[cols_notas].dropna(); 
    if len(df_corr) < 2: return None 
    corr = df_corr.corr()
    cols_notas_map = {'NU_NOTA_CN': 'Ciências Nat.', 'NU_NOTA_CH': 'Ciências Hum.', 'NU_NOTA_LC': 'Linguagens', 'NU_NOTA_MT': 'Matemática', 'NU_NOTA_REDACAO': 'Redação'}
    corr.columns = [cols_notas_map.get(c, c) for c in corr.columns]; corr.index = [cols_notas_map.get(i, i) for i in corr.index]
    try:
        fig = go.Figure(data=go.Heatmap(z=corr.values, x=corr.columns, y=corr.index, colorscale='viridis_r', text=corr.values, texttemplate="%{text:.2f}", textfont={"size":10, "color": "white"}, hovertemplate='<b>%{x}</b> x <b>%{y}</b><br>Correlação: %{z:.2f}<extra></extra>'))
        fig.update_layout(title="Correlação entre Áreas de Conhecimento", margin=dict(t=50, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--text)', size=11), title_font_size=16, title_x=0.05, title_y=0.98, height=712, yaxis_autorange='reversed')
        return fig
    except Exception as e: return None

def criar_barras_conclusao(df_filtrado):
    if df_filtrado.empty or 'TP_ST_CONCLUSAO' not in df_filtrado.columns: return None
    df_data = df_filtrado.dropna(subset=['TP_ST_CONCLUSAO']); 
    if df_data.empty: return None
    df_grouped = df_data['TP_ST_CONCLUSAO'].value_counts().reset_index(); df_grouped.columns = ['Codigo', 'Count']; df_grouped['Percentual'] = (df_grouped['Count'] / df_grouped['Count'].sum()) * 100; df_grouped['Label'] = df_grouped['Codigo'].map(map_conclusao)
    df_grouped = df_grouped.sort_values(by='Codigo')
    try:
        fig = px.bar(df_grouped, x='Label', y='Percentual', title="Percentagem de Nível de Escolaridade", color_discrete_sequence=['#a95aed'])
        fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside', hovertemplate='<b>%{x}</b><br>Percentual: %{y:.1f}%<br>Contagem: %{customdata[0]}<extra></extra>', customdata=df_grouped[['Count']])
        fig.update_layout(showlegend=False, margin=dict(t=50, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--text)', size=11), title_font_size=16, title_x=0.05, title_y=0.95, yaxis_title="Percentual (%)", xaxis_title=None, xaxis=dict(showticklabels=False), height=320)
        return fig
    except Exception as e: return None

def criar_donut_raca(df_filtrado):
    if df_filtrado.empty or 'TP_COR_RACA' not in df_filtrado.columns: return None
    df_data = df_filtrado.dropna(subset=['TP_COR_RACA']); 
    if df_data.empty: return None
    df_grouped = df_data['TP_COR_RACA'].value_counts().reset_index(); df_grouped.columns = ['Codigo', 'Count']; df_grouped['Label'] = df_grouped['Codigo'].map(map_raca)
    colors_raca = {'Preta': '#e76f51', 'Branca': '#4a5b96', 'Parda': '#a95aed', 'Amarela': '#2a9d8f', 'Indígena': '#f4a261', 'Não declarado': '#777'}
    try:
        fig = px.pie(df_grouped, names='Label', values='Count', hole=0.6, title="Percentual de raça", color='Label', color_discrete_map=colors_raca)
        fig.update_traces(textposition='outside', textinfo='percent+label', marker=dict(line=dict(color='var(--panel)', width=4)), pull=[0.02] * len(df_grouped), hovertemplate='<b>%{label}</b><br>Contagem: %{value}<br>Percentual: %{percent}<extra></extra>')
        fig.update_layout(showlegend=False, margin=dict(t=50, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--text)', size=11), title_font_size=16, title_x=0.05, title_y=0.95, height=320)
        return fig
    except Exception as e: return None

def criar_donut_treineiro(df_filtrado):
    if df_filtrado.empty or 'IN_TREINEIRO' not in df_filtrado.columns: return None
    df_data = df_filtrado.dropna(subset=['IN_TREINEIRO']); 
    if df_data.empty: return None
    df_grouped = df_data['IN_TREINEIRO'].value_counts().reset_index(); df_grouped.columns = ['Codigo', 'Count']; df_grouped['Label'] = df_grouped['Codigo'].map(map_treineiro)
    colors_treineiro = {'Não (Oficial)': '#5bc0de', 'Sim (Treineiro)': '#f4a261'}
    try:
        fig = px.pie(df_grouped, names='Label', values='Count', hole=0.6, title="Indicador de treineiro", color='Label', color_discrete_map=colors_treineiro)
        fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='var(--panel)', width=4)), hovertemplate='<b>%{label}</b><br>Contagem: %{value}<br>Percentual: %{percent}<extra></extra>')
        fig.update_layout(showlegend=False, margin=dict(t=50, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--text)', size=11), title_font_size=16, title_x=0.05, title_y=0.95, height=320)
        return fig
    except Exception as e: return None

def criar_barras_faixa_etaria_agrupada(df_filtrado):
    if df_filtrado.empty or 'TP_FAIXA_ETARIA' not in df_filtrado.columns: return None
    df_data = df_filtrado.dropna(subset=['TP_FAIXA_ETARIA']); 
    if df_data.empty: return None
    def agrupar_faixa(codigo):
        if codigo <= 2: return 'Menos de 18 anos'; 
        if codigo <= 8: return 'Entre 18 e 23 anos'; 
        if codigo <= 11: return 'Entre 24 e 30 anos'; 
        return 'Mais de 30 anos'
    df_data['Faixa_Agrupada'] = df_data['TP_FAIXA_ETARIA'].apply(agrupar_faixa)
    df_grouped = df_data['Faixa_Agrupada'].value_counts().reset_index(); df_grouped.columns = ['Label', 'Count']; df_grouped['Percentual'] = (df_grouped['Count'] / df_grouped['Count'].sum()) * 100
    order = ['Menos de 18 anos', 'Entre 18 e 23 anos', 'Entre 24 e 30 anos', 'Mais de 30 anos']
    try:
        fig = px.bar(df_grouped, x='Label', y='Percentual', title="Percentual Faixa Etária", color_discrete_sequence=['#a95aed'], category_orders={'Label': order})
        fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside', hovertemplate='<b>%{x}</b><br>Percentual: %{y:.1f}%<br>Contagem: %{customdata[0]}<extra></extra>', customdata=df_grouped[['Count']])
        fig.update_layout(showlegend=False, margin=dict(t=50, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--text)', size=11), title_font_size=16, title_x=0.05, title_y=0.95, yaxis_title="Percentual (%)", xaxis_title=None, xaxis=dict(tickangle=0), height=320)
        return fig
    except Exception as e: return None

def criar_donut_renda_familiar(df_filtrado):
    if df_filtrado.empty or 'Q_RENDA' not in df_filtrado.columns: return None
    df_data = df_filtrado.dropna(subset=['Q_RENDA']); 
    if df_data.empty: return None
    def agrupar_renda_prototipo(codigo):
        if pd.isna(codigo): return 'Não informado'; 
        if codigo in ['A', 'nan', 'N/A', '<NA>', 'None']: return 'Não informado'; 
        if codigo == 'B': return 'Até 1 salário mínimo'; 
        if codigo in ['C', 'D', 'E', 'F']: return 'Entre 1 e 3 salários'; 
        if codigo in ['G', 'H', 'I']: return 'Entre 3 e 6 salários'; 
        if codigo in ['J','K','L','M','N','O','P','Q']: return 'Acima de 6 salários'; 
        return 'Não informado'
    df_data['Renda_Agrupada'] = df_data['Q_RENDA'].apply(agrupar_renda_prototipo)
    df_grouped = df_data['Renda_Agrupada'].value_counts().reset_index(); df_grouped.columns = ['Label', 'Count']
    colors_renda = {'Até 1 salário mínimo': '#4a5b96', 'Entre 1 e 3 salários': '#e76f51', 'Entre 3 e 6 salários': '#a95aed', 'Acima de 6 salários': '#2a9d8f', 'Não informado': '#f4a261'}
    order = ['Até 1 salário mínimo', 'Entre 1 e 3 salários', 'Entre 3 e 6 salários', 'Acima de 6 salários', 'Não informado']
    df_grouped['Label'] = pd.Categorical(df_grouped['Label'], categories=order, ordered=True); df_grouped = df_grouped.sort_values('Label')
    try:
        fig = px.pie(df_grouped, names='Label', values='Count', hole=0.6, title="Percentual de faixa de renda familiar", color='Label', color_discrete_map=colors_renda)
        fig.update_traces(textposition='outside', textinfo='percent+label', marker=dict(line=dict(color='var(--panel)', width=4)), hovertemplate='<b>%{label}</b><br>Contagem: %{value}<br>Percentual: %{percent}<extra></extra>')
        fig.update_layout(showlegend=False, margin=dict(t=50, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--text)', size=11), title_font_size=16, title_x=0.05, title_y=0.95, height=320)
        return fig
    except Exception as e: return None

def criar_scatter_renda_media(df_filtrado):
    if df_filtrado.empty or 'Q_RENDA' not in df_filtrado.columns or 'MEDIA_GERAL' not in df_filtrado.columns: return None
    df_data = df_filtrado.dropna(subset=['Q_RENDA', 'MEDIA_GERAL']); 
    if df_data.empty: return None
    df_data['Renda_Num'] = df_data['Q_RENDA'].map(map_renda_numerico)
    df_agg = df_data.groupby('Renda_Num')['MEDIA_GERAL'].mean().reset_index()
    df_agg.rename(columns={'Renda_Num': 'Faixa de Renda (Salários Mínimos)', 'MEDIA_GERAL': 'Nota Média'}, inplace=True)
    try:
        fig = px.scatter(df_agg, x='Faixa de Renda (Salários Mínimos)', y='Nota Média', title="Renda Familiar x Nota Média", color_discrete_sequence=['#a95aed'], trendline="ols", trendline_color_override="#f4a261")
        fig.update_traces(hovertemplate='Renda: ~%{x:.1f} SM<br>Nota Média: %{y:.2f}<extra></extra>')
        fig.update_layout(margin=dict(t=50, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--text)', size=11), title_font_size=16, title_x=0.05, title_y=0.95, height=320)
        return fig
    except Exception as e: return None

def criar_barras_escolaridade_pais(df_filtrado, coluna, titulo):
    if df_filtrado.empty or coluna not in df_filtrado.columns: return None
    df_data = df_filtrado.dropna(subset=[coluna]); 
    if df_data.empty: return None
    def agrupar_escolaridade_prototipo(codigo):
        if pd.isna(codigo): return 'Não Informado'; 
        if codigo in ['H', 'I', 'nan', 'N/A', '<NA>', 'None']: return 'Não Informado'; 
        if codigo in ['A', 'B']: return 'Fundamental Incompleto'; 
        if codigo in ['C', 'D']: return 'Fundamental Completo'; 
        if codigo == 'E': return 'Médio Completo'; 
        if codigo == 'F': return 'Superior Completo'; 
        if codigo == 'G': return 'Pós-graduação'; 
        return 'Não Informado'
    df_data['Escolaridade_Agrupada'] = df_data[coluna].apply(agrupar_escolaridade_prototipo)
    df_grouped = df_data['Escolaridade_Agrupada'].value_counts().reset_index(); df_grouped.columns = ['Label', 'Count']; df_grouped['Percentual'] = (df_grouped['Count'] / df_grouped['Count'].sum()) * 100
    order = ['Não Informado', 'Fundamental Incompleto', 'Fundamental Completo', 'Médio Completo', 'Superior Completo', 'Pós-graduação']
    try:
        fig = px.bar(df_grouped, x='Label', y='Percentual', title=titulo, color_discrete_sequence=['#a95aed'], category_orders={'Label': order})
        fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside', hovertemplate='<b>%{x}</b><br>Percentual: %{y:.1f}%<br>Contagem: %{customdata[0]}<extra></extra>', customdata=df_grouped[['Count']])
        fig.update_layout(showlegend=False, margin=dict(t=50, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--text)', size=11), title_font_size=16, title_x=0.05, title_y=0.95, yaxis_title="Percentual (%)", xaxis_title=None, xaxis=dict(tickangle=0), height=320)
        return fig
    except Exception as e: return None

def grid_analise_placeholder():
    g1, g2 = st.columns([1.4, 1], gap="small")
    with g1: st.markdown("<div class='w-box-placeholder'></div>", unsafe_allow_html=True); gap(12); st.markdown("<div class='w-box-placeholder'></div>", unsafe_allow_html=True)
    with g2: st.markdown("<div class='w-tall-placeholder'></div>", unsafe_allow_html=True)


df_filtrado = df_principal.copy() 

try:
    ano_inicio_sel = st.session_state.get('sel_ano_inicio'); ano_fim_sel = st.session_state.get('sel_ano_fim')
    if ano_inicio_sel and ano_fim_sel and 'NU_ANO' in df_filtrado.columns:
        ano_inicio_int = int(ano_inicio_sel); ano_fim_int = int(ano_fim_sel)
        if ano_inicio_int > ano_fim_int: ano_inicio_int, ano_fim_int = ano_fim_int, ano_inicio_int
        df_filtrado['NU_ANO'] = pd.to_numeric(df_filtrado['NU_ANO'], errors='coerce')
        df_filtrado = df_filtrado[df_filtrado['NU_ANO'].notna() & (df_filtrado['NU_ANO'] >= ano_inicio_int) & (df_filtrado['NU_ANO'] <= ano_fim_int)]
except ValueError: pass
except Exception as e: pass

try:
    estado_sidebar = st.session_state.get('sel_estado', "Todos")
    if estado_sidebar != "Todos" and 'SG_UF_PROVA' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['SG_UF_PROVA'] == estado_sidebar]
except Exception as e: pass

try:
    municipio_sidebar = st.session_state.get('sel_municipio', "Todos")
    if municipio_sidebar != "Todos" and 'NO_MUNICIPIO_PROVA' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['NO_MUNICIPIO_PROVA'] == municipio_sidebar]
except Exception as e: pass

try:
    genero_sidebar = st.session_state.get('sel_genero', "Todos")
    if 'TP_SEXO' in df_filtrado.columns:
        if genero_sidebar == "Feminino": df_filtrado = df_filtrado[df_filtrado['TP_SEXO'] == 'F']
        elif genero_sidebar == "Masculino": df_filtrado = df_filtrado[df_filtrado['TP_SEXO'] == 'M']
except Exception as e: pass

try:
    faixa_sidebar = st.session_state.get('sel_faixa_etaria', "Todos")
    if faixa_sidebar != "Todos" and 'TP_FAIXA_ETARIA' in df_filtrado.columns:
        map_faixa_reverso = {v: k for k, v in map_faixa_etaria.items()}
        codigo_faixa = map_faixa_reverso.get(faixa_sidebar)
        if codigo_faixa is not None:
            df_filtrado['TP_FAIXA_ETARIA'] = pd.to_numeric(df_filtrado['TP_FAIXA_ETARIA'], errors='coerce')
            df_filtrado = df_filtrado[df_filtrado['TP_FAIXA_ETARIA'].notna() & (df_filtrado['TP_FAIXA_ETARIA'] == codigo_faixa)]
except Exception as e: pass

try:
    escolaridade_sidebar = st.session_state.get('sel_escolaridade', "Todos")
    if escolaridade_sidebar != "Todos" and 'TP_ST_CONCLUSAO' in df_filtrado.columns:
        map_conclusao_reverso = {v: k for k, v in map_conclusao.items()}
        codigo_conclusao = map_conclusao_reverso.get(escolaridade_sidebar)
        if codigo_conclusao is not None:
            df_filtrado['TP_ST_CONCLUSAO'] = pd.to_numeric(df_filtrado['TP_ST_CONCLUSAO'], errors='coerce')
            df_filtrado = df_filtrado[df_filtrado['TP_ST_CONCLUSAO'].notna() & (df_filtrado['TP_ST_CONCLUSAO'] == codigo_conclusao)]
except Exception as e: pass


total_inscritos = df_filtrado.shape[0] if not df_filtrado.empty else 0
total_confirmados = 0; total_presentes = 0; total_ausentes_dia = 0
if 'INDICADOR_ABSENTEISMO' in df_filtrado.columns and not df_filtrado.empty:
      indicador_abs_series = df_filtrado['INDICADOR_ABSENTEISMO'].astype(str)
      total_confirmados = (indicador_abs_series != 'Ausente em um ou mais dias').sum()
      total_presentes = (indicador_abs_series == 'Presente').sum()
      total_ausentes_dia = (indicador_abs_series == 'Ausente em um ou mais dias').sum()
perc_presentes = (total_presentes / total_inscritos) if total_inscritos > 0 else 0.0
perc_ausentes = (total_ausentes_dia / total_inscritos) if total_inscritos > 0 else 0.0
media_geral = df_filtrado['MEDIA_GERAL'].mean() if 'MEDIA_GERAL' in df_filtrado.columns and not df_filtrado.empty else np.nan
media_redacao = df_filtrado['NU_NOTA_REDACAO'].mean() if 'NU_NOTA_REDACAO' in df_filtrado.columns and not df_filtrado.empty else np.nan
total_lingua = 0; cont_ingles = 0; cont_espanhol = 0
if 'TP_LINGUA' in df_filtrado.columns and not df_filtrado.empty:
    lingua_series = df_filtrado['TP_LINGUA'].dropna()
    cont_ingles = (lingua_series == 0).sum(); cont_espanhol = (lingua_series == 1).sum()
    total_lingua = cont_ingles + cont_espanhol
perc_ingles = (cont_ingles / total_lingua) if total_lingua > 0 else 0.0
perc_espanhol = (cont_espanhol / total_lingua) if total_lingua > 0 else 0.0

kpi_cols = st.columns([1, 1, 1.5, 1, 1], gap="small")
with kpi_cols[0]: st.markdown(criar_kpi("Total Inscritos", total_inscritos), unsafe_allow_html=True)
with kpi_cols[1]: st.markdown(criar_kpi("Total Confirmados", total_confirmados), unsafe_allow_html=True)
with kpi_cols[2]: st.markdown(criar_kpi_presenca("% Presentes x Ausentes", perc_presentes, perc_ausentes), unsafe_allow_html=True)
with kpi_cols[3]: st.markdown(criar_kpi("Média Geral", media_geral, formato="{:,.2f}"), unsafe_allow_html=True)
with kpi_cols[4]: st.markdown(criar_kpi("Média Nota da Redação", media_redacao, formato="{:,.2f}"), unsafe_allow_html=True)
gap(8)
kpi_lang_cols = st.columns([1, 3], gap="small")
with kpi_lang_cols[0]: st.markdown(criar_kpi_lingua("Linguagem Estrangeira", cont_ingles, cont_espanhol, perc_ingles, perc_espanhol), unsafe_allow_html=True)


gap(6); section("Análise Geográfica e Demográfica")
col1, col2 = st.columns([1.4, 1], gap="small")

with col1:
    placeholder_esquerda_sup = st.empty()
    gap(12)
    placeholder_esquerda_inf = st.empty()
with col2:
    placeholder_direita = st.empty()

df_tabela = criar_tabela_anual(df_filtrado)
fig_mapa = criar_mapa_brasil(df_principal, geojson_brasil) 

with placeholder_esquerda_sup.container():
    st.dataframe(df_tabela, use_container_width=True, hide_index=True, column_config={"Ano": st.column_config.NumberColumn(format="%d", width="small"), "Total Inscritos": st.column_config.NumberColumn(format="%,d"), "Total Confirmados": st.column_config.NumberColumn(format="%,d"), "% Presentes": st.column_config.ProgressColumn(format="%.1f%%", min_value=0, max_value=1), "% Ausentes": st.column_config.ProgressColumn(format="%.1f%%", min_value=0, max_value=1)})

with placeholder_esquerda_inf.container(border=False):
    fig_genero = criar_donut_genero(df_filtrado)
    if fig_genero:
         st.plotly_chart(fig_genero, use_container_width=True, config={"displayModeBar": False})
    else:
         st.markdown('<div class="chart-placeholder-box small">Dados de Gênero indisponíveis.</div>', unsafe_allow_html=True)

with placeholder_direita.container(border=False):
    if fig_mapa:
        st.plotly_chart(fig_mapa, use_container_width=True, config={"displayModeBar": False}) 
    else:
        st.markdown(placeholder_mapa(), unsafe_allow_html=True)

gap(18); section("Análise de Desempenho Acadêmico")
fig_barras = criar_barras_medias(df_filtrado)
fig_histograma = criar_histograma_redacao(df_filtrado)
fig_heatmap = criar_heatmap_correlacao(df_filtrado)
col_acad_1, col_acad_2 = st.columns([1.4, 1], gap="small")
with col_acad_1:
    with st.empty().container(border=False):
        if fig_barras: st.plotly_chart(fig_barras, use_container_width=True, config={"displayModeBar": False})
        else: st.markdown('<div class="chart-placeholder-box small">Dados de Média indisponíveis.</div>', unsafe_allow_html=True)
    gap(12)
    with st.empty().container(border=False):
        if fig_histograma: st.plotly_chart(fig_histograma, use_container_width=True, config={"displayModeBar": False})
        else: st.markdown('<div class="chart-placeholder-box small">Dados de Redação indisponíveis.</div>', unsafe_allow_html=True)
with col_acad_2:
    with st.empty().container(border=False):
        if fig_heatmap: st.plotly_chart(fig_heatmap, use_container_width=True, config={"displayModeBar": False})
        else: st.markdown('<div class="chart-placeholder-box tall">Dados de Correlação indisponíveis.</div>', unsafe_allow_html=True)

gap(18); section("Análise por Perfil")
fig_conclusao = criar_barras_conclusao(df_filtrado)
fig_raca = criar_donut_raca(df_filtrado)
fig_treineiro = criar_donut_treineiro(df_filtrado)
fig_faixa_agrupada = criar_barras_faixa_etaria_agrupada(df_filtrado)
perfil_col1, perfil_col2 = st.columns([1, 1], gap="small")
with perfil_col1:
    with st.empty().container(border=False):
        if fig_conclusao: st.plotly_chart(fig_conclusao, use_container_width=True, config={"displayModeBar": False})
        else: st.markdown('<div class="chart-placeholder-box small">Dados de Escolaridade indisponíveis.</div>', unsafe_allow_html=True)
    gap(12)
    with st.empty().container(border=False):
        if fig_treineiro: st.plotly_chart(fig_treineiro, use_container_width=True, config={"displayModeBar": False})
        else: st.markdown('<div class="chart-placeholder-box small">Dados de Treineiro indisponíveis.</div>', unsafe_allow_html=True)
with perfil_col2:
    with st.empty().container(border=False):
        if fig_raca: st.plotly_chart(fig_raca, use_container_width=True, config={"displayModeBar": False})
        else: st.markdown('<div class="chart-placeholder-box small">Dados de Raça indisponíveis.</div>', unsafe_allow_html=True)
    gap(12)
    with st.empty().container(border=False):
        if fig_faixa_agrupada: st.plotly_chart(fig_faixa_agrupada, use_container_width=True, config={"displayModeBar": False})
        else: st.markdown('<div class="chart-placeholder-box small">Dados de Faixa Etária indisponíveis.</div>', unsafe_allow_html=True)

gap(18); section("Análise Socioeconômica")
fig_donut_renda = criar_donut_renda_familiar(df_filtrado)
fig_scatter_renda = criar_scatter_renda_media(df_filtrado)
fig_barras_pai = criar_barras_escolaridade_pais(df_filtrado, 'Q_ESCOLARIDADE_PAI', 'Porcentagem de escolaridade paterna')
fig_barras_mae = criar_barras_escolaridade_pais(df_filtrado, 'Q_ESCOLARIDADE_MAE', 'Porcentagem de escolaridade materna')
socio_col1, socio_col2 = st.columns([1, 1], gap="small")
with socio_col1:
    with st.empty().container(border=False):
        if fig_donut_renda: st.plotly_chart(fig_donut_renda, use_container_width=True, config={"displayModeBar": False})
        else: st.markdown('<div class="chart-placeholder-box small">Dados de Renda Familiar indisponíveis.</div>', unsafe_allow_html=True)
    gap(12)
    with st.empty().container(border=False):
        if fig_barras_pai: st.plotly_chart(fig_barras_pai, use_container_width=True, config={"displayModeBar": False})
        else: st.markdown('<div class="chart-placeholder-box small">Dados de Escolaridade Paterna indisponíveis.</div>', unsafe_allow_html=True)
with socio_col2:
    with st.empty().container(border=False):
        if fig_scatter_renda: st.plotly_chart(fig_scatter_renda, use_container_width=True, config={"displayModeBar": False})
        else: st.markdown('<div class="chart-placeholder-box small">Dados de Renda x Média indisponíveis.</div>', unsafe_allow_html=True)
    gap(12)
    with st.empty().container(border=False):
        if fig_barras_mae: st.plotly_chart(fig_barras_mae, use_container_width=True, config={"displayModeBar": False})
        else: st.markdown('<div class="chart-placeholder-box small">Dados de Escolaridade Materna indisponíveis.</div>', unsafe_allow_html=True)

gap(18); section("Comparativo de Grupos")
grid_analise_placeholder()

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