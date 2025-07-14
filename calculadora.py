import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt

# --- CONFIGURAÇÕES ---
st.set_page_config(page_title="Análise de Grupos - Hotel", layout="centered")

# --- REGRAS DE NEGÓCIO ---
DESCONTO_PADRAO_GRUPO = 0.1  # 15% OFF para grupos (incentivo comercial)
TARIFAS_POR_TEMPORADA = {
    "alta": 1.3,  # +30% na alta temporada
    "media": 1.0,
    "baixa": 0.8  # -20% na baixa
}

# --- INTERFACE ---
st.title("🏨 Cálculo de Demanda de Grupos")

with st.form("dados_grupo"):
    col1, col2 = st.columns(2)
    with col1:
        data_entrada = st.date_input("📅 Data de Entrada", datetime.today())
        data_saida = st.date_input("📅 Data de Saída", datetime.today())
        tarifa_media = st.number_input("💰 Tarifa média (R$)", min_value=0.0, value=359.00)
    with col2:
        quartos_grupo = st.number_input("🛏️ Quartos solicitados", min_value=0, value=11)
        total_quartos_hotel = st.number_input("🏨 Total de quartos", min_value=0, value=321)
        evento_especial = st.selectbox("🎉 Evento especial?", ["Não", "Sim"])
    submitted = st.form_submit_button("📊 Calcular")

# --- CÁLCULOS ---
if submitted:
    # Validações
    if data_entrada >= data_saida:
        st.error("❌ Data de saída deve ser após a entrada!")
    else:
        # 1. Define temporada
        mes = data_entrada.month
        temporada = "alta" if mes in [12, 1, 2] else "baixa" if mes in [6, 7] else "media"

        # 2. Calcula tarifa base ajustada pela temporada
        tarifa_base = tarifa_media * TARIFAS_POR_TEMPORADA[temporada]

        # 3. Aplica desconto padrão para grupos (a menos que seja evento especial)
        if evento_especial == "Não":
            tarifa_sugerida = tarifa_base * (1 - DESCONTO_PADRAO_GRUPO)
            motivo_desconto = f"Desconto comercial de {DESCONTO_PADRAO_GRUPO * 100:.0f}%"
        else:
            tarifa_sugerida = tarifa_base  * (1.1 - DESCONTO_PADRAO_GRUPO)
            motivo_desconto = "Evento especial: 5% "

        # 4. Calcula noites e receita total
        noites = (data_saida - data_entrada).days
        receita_total = tarifa_sugerida * quartos_grupo * noites

        # --- EXIBE RESULTADOS ---
        st.success("✅ **Resultados**")

        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Período", f"{noites} noites")
        col2.metric("📊 Temporada", temporada.capitalize())
        col3.metric("💡 Tarifa Sugerida", f"R$ {tarifa_sugerida:.2f}", motivo_desconto)

        st.write(f"**Receita Total do Grupo:** R$ {receita_total:,.2f}")

        # Comparação com tarifa média
        st.markdown("### 🔍 Comparação com Tarifa Média")
        st.write(f"- Tarifa média do período: R$ {tarifa_media:.2f}")
        st.write(
            f"- Tarifa sugerida para o grupo: R$ {tarifa_sugerida:.2f} ({(tarifa_sugerida - tarifa_media) / tarifa_media * 100:.1f}%)")

        if tarifa_sugerida >= tarifa_media and evento_especial == "Não":
            st.warning("⚠️ **Atenção!** Tarifa igual/média pode desincentivar a venda via comercial.")

            if tarifa_sugerida >= tarifa_media and evento_especial == "Não":
                st.warning("⚠️ **Atenção!** Tarifa igual/média pode desincentivar a venda via comercial.")
