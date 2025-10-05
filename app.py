# ===========================================================
# AREANDINA - PROYECTO DE CÁLCULO INTEGRAL
# Modelo Matemático de Pérdida o Ganancia de Peso (Método RK4)
# Versión Profesional - Hugging Face / Streamlit
# ===========================================================

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io
import datetime
from config import DB_USERNAME, DB_TOKEN, ALGUNA_CLAVE

def dW_dt(t, W, C_ingesta, C_gasto):
    return (C_ingesta - C_gasto) / 7700.0

def runge_kutta_peso(W0, C_ingesta, C_gasto, dias, h=1):
    t, W = 0.0, W0
    resultados = [(t, W)]
    pasos = int(dias / h)
    for _ in range(pasos):
        k1 = h * dW_dt(t, W, C_ingesta, C_gasto)
        k2 = h * dW_dt(t + h/2, W + k1/2, C_ingesta, C_gasto)
        k3 = h * dW_dt(t + h/2, W + k2/2, C_ingesta, C_gasto)
        k4 = h * dW_dt(t + h, W + k3, C_ingesta, C_gasto)
        W += (k1 + 2*k2 + 2*k3 + k4) / 6.0
        t += h
        resultados.append((t, W))
    return resultados

def estimar_gasto(peso, edad):
    return 22 * peso + 1.5 * edad

def calcular_ingesta_recomendada(W0, W_obj, dias, gasto):
    delta = W_obj - W0
    total_kcal = delta * 7700.0
    return gasto + (total_kcal / max(1, dias))

def generar_dieta(W0, W_obj):
    if W_obj < W0:
        tipo = "Pérdida de peso"
        dieta = [
            "Déficit calórico controlado de 400–600 kcal/día.",
            "Desayuno: avena con claras de huevo y frutas frescas.",
            "Almuerzo: pollo o pescado + arroz integral + ensalada.",
            "Cena: verduras al vapor con proteína magra.",
            "Snacks: yogur natural, manzana o frutos secos."
        ]
    elif W_obj > W0:
        tipo = "Ganancia de peso"
        dieta = [
            "Superávit calórico de 300–500 kcal/día.",
            "Desayuno: avena con leche y frutos secos.",
            "Almuerzo: pasta o arroz + carne magra + aguacate.",
            "Cena: arroz + pescado + verduras.",
            "Snacks: batidos proteicos o mantequilla de maní."
        ]
    else:
        tipo = "Mantenimiento"
        dieta = ["Mantén tu ingesta equilibrada y realiza ejercicio moderado."]
    return tipo, dieta

def recomendaciones():
    return [
        "Aumenta o reduce calorías de forma gradual.",
        "Combina ejercicios cardiovasculares con fuerza.",
        "Duerme entre 7 y 9 horas cada noche.",
        "Mantén una buena hidratación (mínimo 2 L/día).",
        "Consulta a un profesional de nutrición si es necesario."
    ]

st.set_page_config(
    page_title="Areandina - Proyecto de Cálculo Integral",
    page_icon="💚",
    layout="centered"
)

st.markdown("""
<style>
.main {
    background: white;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
h1, h2, h3 { color: #007a3d; }
.stButton>button {
    background-color: #007a3d;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #00994c;
}
</style>
""", unsafe_allow_html=True)

st.image("https://upload.wikimedia.org/wikipedia/commons/0/07/Logo_Areandina.png", width=180)
st.title("Areandina – Proyecto de Cálculo Integral")
st.markdown("### Modelo Matemático de Pérdida o Ganancia de Peso (Método RK4) 💪")

with st.form("simulacion_form"):
    st.subheader("Ingrese sus datos:")
    nombre = st.text_input("Nombre completo", "Oscar González")
    edad = st.number_input("Edad (años)", min_value=10, max_value=100, value=25)
    W0 = st.number_input("Peso inicial (kg)", min_value=30.0, max_value=200.0, value=80.0)
    W_obj = st.number_input("Peso objetivo (kg)", min_value=30.0, max_value=200.0, value=75.0)
    C_ing = st.number_input("Calorías ingeridas diarias (kcal)", min_value=1000.0, max_value=6000.0, value=1800.0)
    dias = st.number_input("Días de simulación", min_value=5, max_value=365, value=30)
    ejecutar = st.form_submit_button("Simular")

if ejecutar:
    C_gas = estimar_gasto(W0, edad)
    C_rec = calcular_ingesta_recomendada(W0, W_obj, dias, C_gas)
    resultados = runge_kutta_peso(W0, C_rec, C_gas, dias)
    Wf = resultados[-1][1]

    tipo, dieta = generar_dieta(W0, W_obj)
    recoms = recomendaciones()

    st.success(f"✅ Simulación completada para {nombre}")
    st.write(f"**Peso inicial:** {W0:.2f} kg")
    st.write(f"**Peso estimado al finalizar:** {Wf:.2f} kg")
    st.write(f"**Calorías recomendadas:** {C_rec:.0f} kcal/día")
    st.write(f"**Tipo de objetivo:** {tipo}")

    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot([t for t, _ in resultados],
            [W for _, W in resultados],
            marker="o", color="#007a3d", linewidth=2)
    ax.set_title(f"Evolución del peso de {nombre}")
    ax.set_xlabel("Días")
    ax.set_ylabel("Peso (kg)")
    ax.grid(alpha=0.3)
    st.pyplot(fig)

    st.markdown("### 🥗 Plan de dieta recomendado:")
    for d in dieta:
        st.markdown(f"- {d}")

    st.markdown("### 💡 Recomendaciones generales:")
    for r in recoms:
        st.markdown(f"- {r}")

    df = pd.DataFrame({
        "Día": [int(t) for t, _ in resultados],
        "Peso (kg)": [round(W, 2) for _, W in resultados]
    })
    resumen = io.StringIO()
    resumen.write("AREANDINA - PROYECTO DE CÁLCULO INTEGRAL\n")
    resumen.write(f"Simulación: {datetime.datetime.now():%d/%m/%Y %H:%M}\n")
    resumen.write(f"Nombre: {nombre}\nEdad: {edad}\nPeso inicial: {W0} kg\nPeso final estimado: {Wf:.2f} kg\n")
    resumen.write(f"Calorías recomendadas: {C_rec:.0f} kcal/día\nObjetivo: {tipo}\n\n")
    df.to_csv(resumen, index=False, sep=';', decimal=',')

    st.download_button(
        label="📥 Descargar informe en CSV",
        data=resumen.getvalue(),
        file_name=f"Simulacion_{nombre.replace(' ', '_')}.csv",
        mime="text/csv"
    )

st.divider()
st.caption("© 2025 | Fundación Universitaria del Área Andina – Proyecto Académico de Cálculo Integral (Método RK4)")
