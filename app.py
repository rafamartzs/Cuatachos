import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# Leer Excel
# -------------------------------
df = pd.read_excel("reto_cuatachos.xlsx")

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
nombre = st.selectbox("Selecciona tu nombre", df["Nombre"], index=None)

if nombre:
    row = df[df["Nombre"] == nombre].iloc[0]
    minutos = row[semanas]
    rankings = row[rank_semanas]

    # -------------------------------
    # Ranking general y mejor posiciones
    # -------------------------------
    ranking_general = row["Ranking general"]
    ranking_mes1 = row["Ranking Mens. 1"]
    ranking_mes2 = row["Ranking Mens. 2"]

    # -------------------------------
    # Estadísticas básicas
    # -------------------------------
    mejor_tiempo = minutos.max()
    semana_mejor = minutos.idxmax()
    prom_general = minutos.mean()
    desviacion = minutos.std()
    porcentaje_total = minutos.sum() / total_minutos * 100

    # Promedios por mes
    prom_mes1 = minutos[:4].mean()
    prom_mes2 = minutos[4:].mean()

    # Semanas en 0
    semanas_cero = (minutos == 0).sum()

    # Semanas en #1
    semanas_num1 = [i+1 for i,v in enumerate(rankings) if v==1]

    # Mejor tiempo general entre todos
    tiempos_mes1 = df[semanas[:4]].max(axis=1).sort_values(ascending=False)
    tiempos_mes2 = df[semanas[4:8]].max(axis=1).sort_values(ascending=False)
    tiempos_totales = df[semanas].max(axis=1).sort_values(ascending=False)

    pos_mejor_mes1 = tiempos_mes1.index.get_loc(row.name) + 1
    pos_mejor_mes2 = tiempos_mes2.index.get_loc(row.name) + 1
    pos_mejor_total = tiempos_totales.index.get_loc(row.name) + 1

    # Brinco máximo
    difs = minutos.diff().abs()
    brinco_max = difs.max()
    semana_brinco = difs.idxmax()

    # -------------------------------
    # Mostrar estadísticas
    # -------------------------------
    st.header(f"Hola {nombre}! 👋")

    st.subheader("🔥 Estadísticas principales")
    st.write(f"Mejor tiempo en una semana: **{mejor_tiempo} minutos** (Semana {semana_mejor[-1]})")
    st.write(f"Promedio general semanal: **{prom_general:.1f} minutos**")
    st.write(f"Desviación estándar: **{desviacion:.2f}**")
    st.write(f"Contribución al total: **{porcentaje_total:.2f}%**")
    st.write(f"Posición en ranking general: **#{ranking_general}** 🏅")
    st.write(f"Ranking mes 1: **#{ranking_mes1}** {'⬆️' if ranking_mes1 < ranking_mes2 else '⬇️' if ranking_mes1 > ranking_mes2 else '➡️'}")
    st.write(f"Ranking mes 2: **#{ranking_mes2}**")
    
    st.write(f"¡Felicidades! Ostentas el {pos_mejor_mes1}° mejor tiempo del mes 1, el {pos_mejor_mes2}° del mes 2 y el {pos_mejor_total}° general.")

    # Semanas en 0
    if semanas_cero == 0:
        st.success("¡Ejercitaste todas las semanas! 🔥")
    else:
        st.warning(f"Tuviste {semanas_cero} semanas en 0 minutos, ¡pero sabemos que puedes mejorar!")

    # Semanas en #1 (MVP)
    if semanas_num1:
        st.success(f"¡Fuiste MVP en las semanas {', '.join(map(str,semanas_num1))}! 🏆")
    else:
        st.info("Aún no has alcanzado el #1 semanal, ¡pero llegará!")

    # Estabilidad
    if desviacion < 15:
        st.success("¡Felicidades! Eres de los atletas más estables 😎")

    # Brinco máximo
    st.info(f"Tu mayor activación entre semanas consecutivas fue de {brinco_max} minutos, en {semana_brinco}.")

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
        st.info("Tu rendimiento bajó un poco en el segundo mes. 💪 ¡Vamos a mejorar!")
    else:
        st.info("Mantienes un ritmo constante entre los meses. 👌")

    # -------------------------------
    # Gráfica de minutos por ranking mes 2 (para todos)
    # -------------------------------
    st.subheader("📊 Ranking de minutos Mes 2 (todos los atletas)")
    df_mes2 = df[["Nombre"] + semanas[4:8]].copy()
    df_mes2["Total Mes2"] = df_mes2[semanas[4:8]].sum(axis=1)
    df_mes2_sorted = df_mes2.sort_values("Total Mes2", ascending=False)
    colors = ["#ff69b4" if n == nombre else "#1f77b4" for n in df_mes2_sorted["Nombre"]]
    fig2, ax2 = plt.subplots(figsize=(10,5))
    ax2.bar(df_mes2_sorted["Nombre"], df_mes2_sorted["Total Mes2"], color=colors)
    ax2.set_ylabel("Minutos Mes 2")
    ax2.set_xlabel("Atletas")
    ax2.set_title("Ranking de minutos Mes 2")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig2)

    # -------------------------------
    # Gráfica de minutos totales generales (para todos)
    # -------------------------------
    st.subheader("📊 Ranking de minutos Total General (todos los atletas)")
    df_total = df[["Nombre"] + semanas].copy()
    df_total["Total General"] = df_total[semanas].sum(axis=1)
    df_total_sorted = df_total.sort_values("Total General", ascending=False)
    colors_total = ["#ff69b4" if n == nombre else "#1f77b4" for n in df_total_sorted["Nombre"]]
    fig3, ax3 = plt.subplots(figsize=(10,5))
    ax3.bar(df_total_sorted["Nombre"], df_total_sorted["Total General"], color=colors_total)
    ax3.set_ylabel("Minutos Totales")
    ax3.set_xlabel("Atletas")
    ax3.set_title("Ranking de minutos Total General")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig3)