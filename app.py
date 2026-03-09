import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# Leer Excel
# -------------------------------
df = pd.read_excel("reto_cuatachos.xlsx")

# Columnas de semanas y rankings
semanas = ["Semana 1","Semana 2","Semana 3","Semana 4",
           "Semana 5","Semana 6","Semana 7","Semana 8"]
rank_semanas = ["Ranking 1","Ranking 2","Ranking 3","Ranking 4",
                "Ranking 5","Ranking 6","Ranking 7","Ranking 8"]

total_minutos = df[semanas].sum().sum()

# -------------------------------
# Título de la app
# -------------------------------
st.title("🏃 Cuatachos Wrapped")
st.write("¡Tu resumen del reto hasta el mes 2!")

# -------------------------------
# Selección de nombre
# -------------------------------
nombre = st.selectbox("Selecciona tu nombre", df["Nombre"])
row = df[df["Nombre"] == nombre].iloc[0]

minutos = row[semanas]
rankings = row[rank_semanas]

# -------------------------------
# Ranking general y mejor posiciones
# -------------------------------
ranking_general = row["Ranking general"]

mejor_pos_mes1 = rankings[:4].min()
mejor_pos_mes2 = rankings[4:].min()

# -------------------------------
# Estadísticas básicas
# -------------------------------
mejor_tiempo = minutos.max()
promedio_general = minutos.mean()
desviacion = minutos.std()
porcentaje_total = minutos.sum() / total_minutos * 100

# Promedios por mes
prom_mes1 = minutos[:4].mean()
prom_mes2 = minutos[4:].mean()

# Semanas en 0
semanas_cero = (minutos == 0).sum()

# Semanas en #1
semanas_num1 = (rankings == 1).sum()

# -------------------------------
# Mostrar estadísticas
# -------------------------------
st.header(f"Hola {nombre}! 👋")

st.subheader("🔥 Estadísticas principales")
st.write(f"Mejor tiempo en una semana: **{mejor_tiempo} minutos**")
st.write(f"Promedio general semanal: **{promedio_general:.1f} minutos**")
st.write(f"Desviación estándar: **{desviacion:.2f}**")
st.write(f"Contribución al total: **{porcentaje_total:.2f}%**")
st.write(f"Posición en ranking general: **#{ranking_general}** 🏅")
st.write(f"Mejor posición mes 1: **#{mejor_pos_mes1}**")
st.write(f"Mejor posición mes 2: **#{mejor_pos_mes2}**")

# Semanas en 0
if semanas_cero == 0:
    st.success("¡Ejercitaste todas las semanas! 🔥")
else:
    st.warning(f"Tuviste {semanas_cero} semanas en 0 minutos, ¡pero sabemos que puedes mejorar!")

# Semanas en #1
if semanas_num1 > 0:
    st.success(f"Estuviste {semanas_num1} veces en el #1 semanal 🏆")
else:
    st.info("Aún no has alcanzado el #1 semanal, ¡pero llegará!")

# -------------------------------
# Gráfica de minutos por semana
# -------------------------------
st.subheader("📊 Minutos por semana")
fig, ax = plt.subplots()
minutos.plot(kind="bar", ax=ax, color="#ff69b4")
ax.set_ylabel("Minutos")
ax.set_xlabel("Semana")
st.pyplot(fig)

# -------------------------------
# Promedios por mes y comparación
# -------------------------------
st.subheader("📈 Promedios por mes")
st.write(f"Promedio mes 1: **{prom_mes1:.1f} minutos**")
st.write(f"Promedio mes 2: **{prom_mes2:.1f} minutos**")

if prom_mes2 > prom_mes1:
    st.success("¡Mejoraste en el segundo mes! 🚀")
elif prom_mes2 < prom_mes1:
    st.info("Tu rendimiento bajó un poco en el segundo mes. 💪 Vamos a mejorar!")
else:
    st.info("Mantienes un ritmo constante entre los meses. 👌")