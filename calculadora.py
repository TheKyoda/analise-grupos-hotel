import streamlit as st
from datetime import datetime
import math

# --- CONFIGURAÇÕES ---
st.set_page_config(page_title="Análise de Grupos - Hotel", layout="centered")

# --- REGRAS DE NEGÓCIO ---
TARIFAS_POR_TEMPORADA = {
    "alta": 1.3,
    "media": 1.0,
    "baixa": 0.8
}

# --- INTERFACE ---
st.title("🏨 Cálculo de Demanda de Grupos")

with st.form("dados_grupo"):
    col1, col2 = st.columns(2)
    with col1:
        data_entrada = st.date_input("📅 Data de Entrada", datetime.today())
        data_saida = st.date_input("📅 Data de Saída", datetime.today())
        tarifa_media = st.number_input("💰 Tarifa média (R$)", min_value=0.0, value=359.00)
        ocupacao_percentual = st.slider("📈 Ocupação do hotel no período (%)", 0, 100, 50)
    with col2:
        quartos_grupo = st.number_input("🛏️ Quartos solicitados", min_value=0, value=11)
        total_quartos_hotel = st.number_input("🏨 Total de quartos", min_value=0, value=321)
        evento_especial = st.selectbox("🎉 Evento especial?", ["Não", "Sim"])
    submitted = st.form_submit_button("📊 Calcular")

# --- CÁLCULOS ---
if submitted:
    if data_entrada >= data_saida:
        st.error("❌ Data de saída deve ser após a entrada!")
    else:
        mes = data_entrada.month
        temporada = "alta" if mes in [12, 1, 2] else "baixa" if mes in [6, 7] else "media"
        tarifa_base = tarifa_media * TARIFAS_POR_TEMPORADA[temporada]

        # --- Define desconto com base na ocupação
        if ocupacao_percentual <= 40:
            desconto = 0.10
            motivo_desconto = "Baixa ocupação (menor ou igual a 40%) → desconto de 10%"
        elif ocupacao_percentual <= 70:
            desconto = 0.08
            motivo_desconto = "Ocupação média (41 a 70%) → desconto de 8%"
        else:
            desconto = 0.05
            motivo_desconto = "Alta ocupação (maior que 70%) → desconto de 5%"

        # --- Ajuste adicional se for evento especial
        if evento_especial == "Sim":
            desconto = max(desconto - 0.03, 0.02)  # reduz o desconto em 3%

        tarifa_sugerida = tarifa_base * (1 - desconto)

        # Arredondamento
        tarifa_inferior = math.floor(tarifa_sugerida / 10) * 10
        tarifa_superior = math.ceil(tarifa_sugerida / 10) * 10
        st.info(f"↕️ Mínimo: R$ {tarifa_inferior} / Aplicar: R$ {tarifa_superior}")

        noites = (data_saida - data_entrada).days
        receita_total = tarifa_sugerida * quartos_grupo * noites

        # --- RESULTADOS ---
        st.success("✅ **Resultados**")
        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Período", f"{noites} noites")
        col2.metric("📊 Temporada", temporada.capitalize())
        col3.metric("💡 Tarifa Sugerida", f"R$ {tarifa_sugerida:.2f}")

        st.write(f"**Receita Total do Grupo:** R$ {receita_total:,.2f}")

        # Comparação
        st.markdown("### 🔍 Comparação com Tarifa Média")
        variacao_perc = (tarifa_sugerida - tarifa_media) / tarifa_media * 100
        st.write(f"- Tarifa média: R$ {tarifa_media:.2f}")
        st.write(f"- Tarifa sugerida: R$ {tarifa_sugerida:.2f} ({variacao_perc:.1f}%)")
        st.write(f"- **Motivo do desconto:** {motivo_desconto}")
