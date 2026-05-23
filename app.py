import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide",
)

# ── Estilo customizado ──────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Inter:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Syne', sans-serif !important;
    }
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    .metric-card {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 16px;
        padding: 20px 24px;
        backdrop-filter: blur(10px);
    }
    .metric-label {
        font-size: 0.78rem;
        color: rgba(255,255,255,0.55);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 4px;
    }
    .metric-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.9rem;
        font-weight: 800;
        color: #fff;
    }
    .metric-delta {
        font-size: 0.82rem;
        color: #6ee7b7;
        margin-top: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.markdown("## 📊 Dashboard de Vendas Anuais")
st.markdown("Visualização interativa gerada a partir de um arquivo **CSV**.")
st.markdown("---")

# ── Upload ou uso do CSV padrão ─────────────────────────────────────────────
uploaded = st.file_uploader("📁 Faça upload de um CSV (opcional)", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"Arquivo **{uploaded.name}** carregado com sucesso!")
else:
    df = pd.read_csv("dados.csv")
    st.info("Usando o arquivo **dados.csv** de exemplo. Você pode fazer upload do seu próprio CSV acima.")

# ── Preview do dado ─────────────────────────────────────────────────────────
with st.expander("🔍 Visualizar dados brutos"):
    st.dataframe(df, use_container_width=True)

st.markdown("### 📈 Gráfico de Área — Vendas, Despesas e Lucro")

# ── Seletor de colunas ───────────────────────────────────────────────────────
colunas_numericas = df.select_dtypes(include="number").columns.tolist()
colunas_texto     = df.select_dtypes(exclude="number").columns.tolist()

col_x = st.selectbox("Eixo X (categoria)", options=colunas_texto + colunas_numericas,
                     index=0 if colunas_texto else 0)

col_y = st.multiselect("Séries (eixo Y)", options=colunas_numericas,
                       default=colunas_numericas[:3] if len(colunas_numericas) >= 3 else colunas_numericas)

if not col_y:
    st.warning("Selecione ao menos uma série para o gráfico.")
    st.stop()

# ── Paleta de cores ──────────────────────────────────────────────────────────
CORES = ["#818cf8", "#34d399", "#f472b6", "#fb923c", "#facc15"]

# ── Gráfico de Área com Plotly ───────────────────────────────────────────────
fig = go.Figure()

for i, serie in enumerate(col_y):
    cor = CORES[i % len(CORES)]
    fig.add_trace(go.Scatter(
        x=df[col_x],
        y=df[serie],
        name=serie.capitalize(),
        mode="lines",
        fill="tozeroy",
        line=dict(color=cor, width=2.5),
        fillcolor=cor.replace(")", ", 0.15)").replace("rgb", "rgba") if "rgb" in cor
                  else cor + "26",  # hex + 15% alpha
        hovertemplate=f"<b>%{{x}}</b><br>{serie.capitalize()}: R$ %{{y:,.0f}}<extra></extra>",
    ))

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="rgba(255,255,255,0.8)", family="Inter"),
    legend=dict(
        orientation="h", y=1.08, x=0.5, xanchor="center",
        bgcolor="rgba(255,255,255,0.05)",
        bordercolor="rgba(255,255,255,0.1)",
        borderwidth=1,
    ),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        linecolor="rgba(255,255,255,0.1)",
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        linecolor="rgba(255,255,255,0.1)",
        tickprefix="R$ ",
        tickformat=",.0f",
    ),
    margin=dict(t=40, b=20, l=10, r=10),
    height=420,
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)

# ── Cards de métricas ────────────────────────────────────────────────────────
st.markdown("### 🧮 Resumo do Período")
cols = st.columns(len(col_y))

for i, (col, serie in zip(cols, col_y)):
    total  = df[serie].sum()
    media  = df[serie].mean()
    maximo = df[serie].max()
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{serie.capitalize()}</div>
        <div class="metric-value">R$ {total:,.0f}</div>
        <div class="metric-delta">
            Média: R$ {media:,.0f} &nbsp;|&nbsp; Pico: R$ {maximo:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Desenvolvido com Streamlit + Plotly | Aula 18 — Gráficos")
