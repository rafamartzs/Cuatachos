import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# Leer Excel
# -------------------------------
df = pd.read_excel("reto_cuatachos.xlsx")

# Columnas
semanas = ["Semana 1","Semana 2","Semana 3","Semana 4",
           "Semana 5","Semana 6","Semana 7","Semana 8"]

rank_semanas = ["Ranking 1","Ranking 2","Ranking 3","Ranking 4",
                "Ranking 5","Ranking 6","Ranking 7","Ranking 8"]

total_minutos = df[semanas].sum().sum()

# -------------------------------
# Premios automáticos
# -------------------------------

indice_estable = df[semanas].std(axis=1).idxmin()

max_brincos = df[semanas].diff(axis=1).abs().max(axis=1)
indice_brinco = max_brincos.idxmax()

indice_dominante = df[semanas].sum(axis=1).idxmax()

indice_consistente = (df[semanas]==0).sum(axis=1).idxmin()

indice_rey_semanal = (df[rank_semanas]==1).sum(axis=1).idxmax()

# -------------------------------
# Ranking mejores tiempos
# -------------------------------

df["Mejor Semana Mes1"] = df[semanas[:4]].max(axis=1)
df["Mejor Semana Mes2"] = df[semanas[4:]].max(axis=1)
df["Mejor Semana General"] = df[semanas].max(axis=1)

df["Rank Mejor Tiempo M1"] = df["Mejor Semana Mes1"].rank(method='min', ascending=False).astype(int)
df["Rank Mejor Tiempo M2"] = df["Mejor Semana Mes2"].rank(method='min', ascending=False).astype(int)
df["Rank Mejor Tiempo General"] = df["Mejor Semana General"].rank(method='min', ascending=False).astype(int)

# -------------------------------
# Título
# -------------------------------

st.title("🏃 Cuatachos Wrapped")
st.write("¡Tu resumen del reto hasta el mes 2!")

# -------------------------------
# Selector con Salón de la Fama
# -------------------------------

opciones = ["🏆 Salón de la Fama"] + df["Nombre"].tolist()
nombre = st.selectbox("Selecciona tu nombre", opciones, index=None)

# =================================================
# SALÓN DE LA FAMA
# =================================================

if nombre == "🏆 Salón de la Fama":

    st.header("🏆 Salón de la Fama del Reto Cuatachos")

    # Récord absoluto
    mejor_tiempo = df[semanas].max().max()
    idx = df[semanas].max(axis=1).idxmax()
    atleta_mejor = df.loc[idx,"Nombre"]

    st.subheader("🔥 Récord absoluto")
    st.write(f"El mejor tiempo semanal es **{mejor_tiempo} minutos**, logrado por **{atleta_mejor}**")

    # Más estable
    df["std_temp"] = df[semanas].std(axis=1)
    atleta_estable = df.loc[df["std_temp"].idxmin(),"Nombre"]

    st.write(f"🎯 Atleta más estable: **{atleta_estable}**")

    # Constancia perfecta
    constantes = df[(df[semanas]==0).sum(axis=1)==0]["Nombre"].tolist()

    if constantes:
        st.write("💪 Atletas con consistencia perfecta:")
        st.write(", ".join(constantes))
    else:
        st.write("Nadie ha logrado consistencia perfecta aún.")

    # Rey/Reina del podio
    df["num1_temp"] = (df[rank_semanas]==1).sum(axis=1)

    idx = df["num1_temp"].idxmax()

    atleta_rey = df.loc[idx,"Nombre"]
    semanas_num1 = df.loc[idx,"num1_temp"]

    st.write(f"👑 Rey/Reina del podio: **{atleta_rey}** con **{semanas_num1} semanas en #1**")

    # MVP semanal
    st.subheader("🥇 MVPs semanales")

    for semana in semanas:

        idx = df[semana].idxmax()
        atleta = df.loc[idx,"Nombre"]
        tiempo = df.loc[idx,semana]

        st.write(f"{semana}: **{atleta}** con {tiempo} minutos")

    # Top 3 Mes 1
    st.subheader("🏅 Top 3 Mes 1")

    mes1 = df.copy()
    mes1["total_temp"] = mes1[semanas[:4]].sum(axis=1)
    top3 = mes1.sort_values("total_temp",ascending=False).head(3)

    for i,row in top3.iterrows():
        st.write(f"{row['Nombre']} — {row['total_temp']} minutos")

    # Top 3 Mes 2
    st.subheader("🏅 Top 3 Mes 2")

    mes2 = df.copy()
    mes2["total_temp"] = mes2[semanas[4:]].sum(axis=1)
    top3 = mes2.sort_values("total_temp",ascending=False).head(3)

    for i,row in top3.iterrows():
        st.write(f"{row['Nombre']} — {row['total_temp']} minutos")

    # Top 3 General
    st.subheader("🏆 Top 3 General")

    total = df.copy()
    total["total_temp"] = total[semanas].sum(axis=1)
    top3 = total.sort_values("total_temp",ascending=False).head(3)

    for i,row in top3.iterrows():
        st.write(f"{row['Nombre']} — {row['total_temp']} minutos")

    # Mayor brinco
    diffs = df[semanas].diff(axis=1)

    mayor_brinco = diffs.max().max()
    idx = diffs.stack().idxmax()

    atleta = df.loc[idx[0],"Nombre"]

    st.subheader("⚡ Mayor activación")
    st.write(f"**{atleta}** con un salto de **{mayor_brinco} minutos** entre semanas consecutivas")

    # Mayor bajón
    mayor_bajon = diffs.min().min()
    idx = diffs.stack().idxmin()

    atleta = df.loc[idx[0],"Nombre"]

    st.subheader("📉 Mayor bajón")
    st.write(f"**{atleta}** con una caída de **{abs(mayor_bajon)} minutos** entre semanas consecutivas")

# =================================================
# PANEL INDIVIDUAL
# =================================================

if nombre and nombre != "🏆 Salón de la Fama":

    row = df[df["Nombre"] == nombre].iloc[0]

    minutos = row[semanas]
    rankings = row[rank_semanas]

    ranking_general = row["Ranking general"]
    ranking_mes1 = row["Ranking Mens. 1"]
    ranking_mes2 = row["Ranking Mens. 2"]

    mejor_tiempo = minutos.max()
    semana_mejor = minutos.idxmax()

    prom_general = minutos.mean()

    desviacion = minutos.std()

    porcentaje_total = minutos.sum() / total_minutos * 100

    semanas_cero = (minutos == 0).sum()

    semanas_num1 = [i+1 for i,v in enumerate(rankings) if v==1]

    difs = minutos.diff().abs()
    brinco_max = difs.max()
    semana_brinco = difs.idxmax()

    # Mejor semana mes 1
    mejor_tiempo_m1 = row[semanas[:4]].max()
    semana_mejor_m1 = row[semanas[:4]].idxmax()

    # Mejor semana mes 2
    mejor_tiempo_m2 = row[semanas[4:]].max()
    semana_mejor_m2 = row[semanas[4:]].idxmax()

    # Mejor semana general
    mejor_tiempo_gen = row[semanas].max()
    semana_mejor_gen = row[semanas].idxmax()

    st.header(f"¡Hola, {nombre}! 👋")

    st.subheader("🔥 Estadísticas principales")

    st.write(f"Tu mejor tiempo en una semana: **{mejor_tiempo} minutos** ({semana_mejor})")

    st.write(f"Tu promedio semanal: **{prom_general:.1f} minutos**")

    st.write(f"Tu desviación estándar: **{desviacion:.2f}**")

    st.write(f"Tu contribución al total: **{porcentaje_total:.2f}%**")

    st.write(f"Tu posición en el ranking general: **#{ranking_general}**")

    if ranking_mes2 < ranking_mes1:
        flecha = "⬆️"
    elif ranking_mes2 > ranking_mes1:
        flecha = "⬇️"
    else:
        flecha = "➡️"

    st.write(f"Ranking mes 1: **#{ranking_mes1}**")
    st.write(f"Ranking mes 2: **#{ranking_mes2}** {flecha}")

    if semanas_cero == 0:
        st.success("🔥 ¡Ejercitaste todas las semanas!")
    else:
        st.warning(f"Tuviste {semanas_cero} semanas en 0, ¡pero sigue adelante!")

    if semanas_num1:
        st.success(f"🏆 Fuiste MVP en las semanas {', '.join(map(str,semanas_num1))}")

    if desviacion < 100:
        st.success("😎 ¡Eres de los atletas más estables!")

    st.info(f"⚡ Tu mayor salto fue de {brinco_max} minutos ({semana_brinco})")

    st.info(f"🥇 Tu mejor semana del mes 1: {semana_mejor_m1} con {mejor_tiempo_m1} minutos")
    st.info(f"🥇 Tu mejor semana del mes 2: {semana_mejor_m2} con {mejor_tiempo_m2} minutos")
    
    # Gráfica individual
    st.subheader("📊 Minutos por semana")

    fig, ax = plt.subplots()

    minutos.plot(kind="bar", ax=ax)

    ax.set_ylabel("Minutos")

    ax.set_xlabel("Semana")

    st.pyplot(fig)

# =================================================
# GRÁFICAS GENERALES
# =================================================

  # Ranking minutos mes 2
    st.subheader("📊 Ranking de minutos Mes 2")
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

 # Ranking minutos totales
    st.subheader("📊 Ranking de minutos Total General")
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