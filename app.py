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
# Premios automáticos
# -------------------------------
indice_estable = df[semanas].std(axis=1).idxmin()               # Más estable
max_brincos = df[semanas].diff(axis=1).abs().max(axis=1)
indice_brinco = max_brincos.idxmax()                            # Mayor brinco
indice_dominante = df[semanas].sum(axis=1).idxmax()            # Más minutos
indice_consistente = (df[semanas]==0).sum(axis=1).idxmin()     # Menos semanas en 0
indice_rey_semanal = (df[rank_semanas]==1).sum(axis=1).idxmax() # Más semanas en #1

# -------------------------------
# Mejor tiempo rankings
# -------------------------------
df["Mejor Semana Mes1"] = df[semanas[:4]].max(axis=1)
df["Mejor Semana Mes2"] = df[semanas[4:]].max(axis=1)
df["Mejor Semana General"] = df[semanas].max(axis=1)

df["Rank Mejor Tiempo M1"] = df["Mejor Semana Mes1"].rank(method='min', ascending=False).astype(int)
df["Rank Mejor Tiempo M2"] = df["Mejor Semana Mes2"].rank(method='min', ascending=False).astype(int)
df["Rank Mejor Tiempo General"] = df["Mejor Semana General"].rank(method='min', ascending=False).astype(int)

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
    mejor_pos_mes1 = rankings[:4].min()
    mejor_pos_mes2 = rankings[4:].min()

    # -------------------------------
    # Estadísticas básicas
    # -------------------------------
    mejor_tiempo = minutos.max()
    promedio_general = minutos.mean()
    desviacion = minutos.std()
    porcentaje_total = minutos.sum() / total_minutos * 100
    prom_mes1 = minutos[:4].mean()
    prom_mes2 = minutos[4:].mean()
    semanas_cero = (minutos == 0).sum()
    semanas_num1 = (rankings == 1).sum()

    # -------------------------------
    # Mejor tiempo y semana correspondiente
    # -------------------------------
    mejor_tiempo_m1 = minutos[:4].max()
    semana_mejor_m1 = minutos[:4].idxmax()

    mejor_tiempo_m2 = minutos[4:].max()
    semana_mejor_m2 = minutos[4:].idxmax()

    mejor_tiempo_gen = minutos.max()
    semana_mejor_gen = minutos.idxmax()

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

    # -------------------------------
    # Mensaje de estabilidad
    # -------------------------------
    if desviacion < 15:
        st.success("🏅 ¡Felicidades! Eres de los atletas más estables")

    # -------------------------------
    # Premios automáticos
    # -------------------------------
    if nombre == df.loc[indice_estable, "Nombre"]:
        st.success(f"🏅 ¡Felicidades! Eres el atleta más estable, con desviación estándar de {desviacion:.2f} minutos")

    if nombre == df.loc[indice_brinco, "Nombre"]:
        salto_max = minutos.diff().abs().max()
        semana1 = minutos.diff().abs().idxmax()
        st.info(f"⚡ Fuiste el atleta que más se activó, con un salto de {salto_max:.0f} minutos en {semana1}")

    if nombre == df.loc[indice_dominante, "Nombre"]:
        st.success(f"🔥 Eres el dominador del reto con un total de {minutos.sum()} minutos")

    if nombre == df.loc[indice_consistente, "Nombre"]:
        st.success("💪 ¡Consistencia perfecta! No tuviste semanas en 0 minutos")

    if nombre == df.loc[indice_rey_semanal, "Nombre"]:
        st.info(f"🏆 Eres el rey/reina del podio semanal con {semanas_num1} semanas en #1")

    # -------------------------------
    # Mejor tiempo rankings
    # -------------------------------
    rank_m1 = df.loc[df["Nombre"] == nombre, "Rank Mejor Tiempo M1"].values[0]
    rank_m2 = df.loc[df["Nombre"] == nombre, "Rank Mejor Tiempo M2"].values[0]
    rank_gen = df.loc[df["Nombre"] == nombre, "Rank Mejor Tiempo General"].values[0]

    st.info(f"⏱ ¡Felicidades! Ostentas el {rank_m1}{'º' if rank_m1!=1 else 'er'} mejor tiempo del mes 1, "
            f"el {rank_m2}{'º' if rank_m2!=1 else 'er'} mejor del mes 2 y "
            f"el {rank_gen}{'º' if rank_gen!=1 else 'er'} mejor general")

    # -------------------------------
    # Mostrar semana y minutos de mejor tiempo
    # -------------------------------
    st.info(f"🥇 Mejor semana mes 1: **{semana_mejor_m1}** con **{mejor_tiempo_m1} minutos**")
    st.info(f"🥇 Mejor semana mes 2: **{semana_mejor_m2}** con **{mejor_tiempo_m2} minutos**")
    st.info(f"🥇 Mejor semana general: **{semana_mejor_gen}** con **{mejor_tiempo_gen} minutos**")

    # -------------------------------
    # Semanas en 0
    # -------------------------------
    if semanas_cero == 0:
        st.success("¡Ejercitaste todas las semanas! 🔥")
    else:
        st.warning(f"Tuviste {semanas_cero} semanas en 0 minutos, ¡pero sabemos que puedes mejorar!")

    # -------------------------------
    # Gráfica de minutos por semana
    # -------------------------------
    st.subheader("📊 Minutos por semana")
    fig, ax = plt.subplots(figsize=(8,4))
    minutos.plot(kind="bar", ax=ax, color="#ff69b4")
    ax.set_ylabel("Minutos")
    ax.set_xlabel("Semana")
    ax.set_title(f"Minutos de {nombre} semana a semana")
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