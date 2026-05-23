import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title=“CSV Visualizer”, page_icon=“📊”, layout=“wide”)

st.markdown(”””

<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Space Mono', monospace !important; }
.stApp { background: #0d0d0d; color: #f0f0f0; }
section[data-testid="stSidebar"] { background: #161616; border-right: 1px solid #2a2a2a; }
.metric-card { background: #1a1a1a; border: 1px solid #2e2e2e; border-radius: 12px; padding: 1.2rem 1.5rem; text-align: center; }
.metric-card .label { font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 0.1em; font-family: 'Space Mono', monospace; }
.metric-card .value { font-size: 2rem; font-weight: 700; color: #00ff87; font-family: 'Space Mono', monospace; }
</style>

“””, unsafe_allow_html=True)

st.markdown(”# 📊 CSV Visualizer”)
st.markdown(”<p style='color:#666; font-size:0.95rem; margin-top:-0.5rem;'>Faça upload de um arquivo CSV e explore seus dados com gráficos interativos.</p>”, unsafe_allow_html=True)
st.markdown(”—”)

with st.sidebar:
st.markdown(”### ⚙️ Configurações”)
uploaded_file = st.file_uploader(“Carregar arquivo CSV”, type=[“csv”])
separator = st.selectbox(“Separador”, [”,”, “;”, “|”, “\t”], index=0)
encoding = st.selectbox(“Encoding”, [“utf-8”, “latin-1”, “utf-16”], index=0)
st.markdown(”—”)
st.markdown(”<p style='font-size:0.75rem; color:#555;'>Desenvolvido com Streamlit + Plotly</p>”, unsafe_allow_html=True)

SAMPLE_CSV = “”“Mes,Vendas,Custo,Lucro,Regiao
Jan,15000,9000,6000,Norte
Fev,18000,10500,7500,Sul
Mar,13000,8000,5000,Norte
Abr,21000,12000,9000,Leste
Mai,25000,14000,11000,Sul
Jun,22000,13000,9000,Oeste
Jul,19000,11000,8000,Norte
Ago,28000,16000,12000,Leste
Set,24000,14000,10000,Sul
Out,30000,17000,13000,Oeste
Nov,35000,20000,15000,Leste
Dez,40000,23000,17000,Sul
“””

if uploaded_file is not None:
sep = “\t” if separator == “\t” else separator
try:
df = pd.read_csv(uploaded_file, sep=sep, encoding=encoding)
source_label = f”📂 {uploaded_file.name}”
except Exception as e:
st.error(f”Erro ao ler o arquivo: {e}”)
st.stop()
else:
df = pd.read_csv(io.StringIO(SAMPLE_CSV))
source_label = “📄 Dados de exemplo (carregue seu CSV na barra lateral)”

st.caption(source_label)

num_cols = df.select_dtypes(include=“number”).columns.tolist()
cat_cols = df.select_dtypes(exclude=“number”).columns.tolist()

col1, col2, col3, col4 = st.columns(4)
with col1:
st.markdown(f’<div class="metric-card"><div class="label">Linhas</div><div class="value">{len(df):,}</div></div>’, unsafe_allow_html=True)
with col2:
st.markdown(f’<div class="metric-card"><div class="label">Colunas</div><div class="value">{len(df.columns)}</div></div>’, unsafe_allow_html=True)
with col3:
st.markdown(f’<div class="metric-card"><div class="label">Numéricas</div><div class="value">{len(num_cols)}</div></div>’, unsafe_allow_html=True)
with col4:
st.markdown(f’<div class="metric-card"><div class="label">Categóricas</div><div class="value">{len(cat_cols)}</div></div>’, unsafe_allow_html=True)

st.markdown(”<br>”, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([“📈 Gráficos”, “🗃️ Dados”, “📋 Estatísticas”])

with tab1:
if not num_cols:
st.warning(“Nenhuma coluna numérica encontrada para criar gráficos.”)
else:
left, right = st.columns([1, 2])
with left:
chart_type = st.radio(“Tipo de gráfico”, [“Linha”, “Barras”, “Dispersão”, “Pizza”, “Histograma”, “Box Plot”])
y_col = st.selectbox(“Eixo Y (valores)”, num_cols)
x_col = st.selectbox(“Eixo X”, df.columns.tolist(), index=0)
color_col = st.selectbox(“Cor por categoria (opcional)”, [”— Nenhuma —”] + cat_cols)
color_arg = None if color_col == “— Nenhuma —” else color_col

```
DARK_TEMPLATE = "plotly_dark"
with right:
fig = None
if chart_type == "Linha":
fig = px.line(df, x=x_col, y=y_col, color=color_arg, template=DARK_TEMPLATE, markers=True, color_discrete_sequence=px.colors.qualitative.Safe)
elif chart_type == "Barras":
fig = px.bar(df, x=x_col, y=y_col, color=color_arg, template=DARK_TEMPLATE, barmode="group", color_discrete_sequence=px.colors.qualitative.Safe)
elif chart_type == "Dispersão":
fig = px.scatter(df, x=x_col, y=y_col, color=color_arg, template=DARK_TEMPLATE, color_discrete_sequence=px.colors.qualitative.Safe)
elif chart_type == "Pizza":
fig = px.pie(df, names=x_col, values=y_col, template=DARK_TEMPLATE, color_discrete_sequence=px.colors.qualitative.Safe)
elif chart_type == "Histograma":
fig = px.histogram(df, x=y_col, color=color_arg, template=DARK_TEMPLATE, nbins=20, color_discrete_sequence=px.colors.qualitative.Safe)
elif chart_type == "Box Plot":
fig = px.box(df, x=color_arg, y=y_col, template=DARK_TEMPLATE, color_discrete_sequence=px.colors.qualitative.Safe)
if fig:
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_family="DM Sans", margin=dict(t=30, b=30, l=10, r=10))
st.plotly_chart(fig, use_container_width=True)
```

with tab2:
search = st.text_input(“🔍 Filtrar por valor (busca em texto)”)
display_df = df.copy()
if search:
mask = display_df.astype(str).apply(lambda col: col.str.contains(search, case=False)).any(axis=1)
display_df = display_df[mask]
st.dataframe(display_df, use_container_width=True, height=420)
st.download_button(“⬇️ Baixar CSV filtrado”, display_df.to_csv(index=False).encode(“utf-8”), “dados_filtrados.csv”, “text/csv”)

with tab3:
if num_cols:
st.dataframe(df[num_cols].describe().T.style.format(”{:.2f}”), use_container_width=True)
else:
st.info(“Nenhuma coluna numérica disponível para estatísticas.”)
