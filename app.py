import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Cuatachos Wrapped", layout="wide")

# -----------------------------------
# Cargar datos
# -----------------------------------

df = pd.read_excel("reto_cuatachos.xlsx")

semanas = [c for c in df.columns if "Semana" in c]
rank_semanas = [c for c in df.columns if "Ranking " in c and "Mens" not in c and "general" not in c]

ultima_semana = semanas[-1]
semana_previa = semanas[-2]

num_semana_actual = int(ultima_semana.split()[1])

total_minutos_global = df[semanas].sum().sum()

# -----------------------------------
# SELECTOR
# -----------------------------------

opciones = ["🏆 Salón de la Fama"] + df["Nombre"].tolist()

nombre = st.selectbox("Selecciona tu nombre", opciones, index=None)

# =====================================================
# SALÓN DE LA FAMA
# =====================================================

if nombre == "🏆 Salón de la Fama":

    st.title("🏆 Salón de la Fama del Reto")

    # -----------------------------------
    # SEMANA RECIENTE
    # -----------------------------------

    st.header(f"🔥 Lo que pasó en la {ultima_semana}")

    atletas_moviendose = (df[ultima_semana] > 0).sum()

    minutos_totales = df[ultima_semana].sum()

    promedio = minutos_totales / atletas_moviendose if atletas_moviendose > 0 else 0

    despertaron = df[(df[semana_previa] == 0) & (df[ultima_semana] > 0)]["Nombre"].tolist()

    diff = df[ultima_semana] - df[semana_previa]

    idx_activacion = diff.idxmax()
    idx_relajaron = diff.idxmin()

    atleta_activacion = df.loc[idx_activacion, "Nombre"]
    atleta_relajado = df.loc[idx_relajaron, "Nombre"]

    st.write(f"👟 Atletas moviéndose: **{atletas_moviendose}**")

    st.write(f"⏱ Minutos totales: **{minutos_totales}**")

    st.write(f"📊 Promedio entre atletas activos: **{promedio:.1f}**")

    if despertaron:
        st.write("🌅 Despertaron:")
        st.write(", ".join(despertaron))

    st.write(f"⚡ Mayor activación: **{atleta_activacion}** (+{diff.max()} min)")

    st.write(f"😴 Mayor relajación: **{atleta_relajado}** ({diff.min()} min)")

    st.subheader("🥇 Top 3 de la semana")

    top3_semana = df.sort_values(ultima_semana, ascending=False).head(3)

    for i, row in top3_semana.iterrows():
        st.write(f"{row['Nombre']} — {row[ultima_semana]} min")

    # -----------------------------------
    # RECORDS HISTORICOS
    # -----------------------------------

    st.header("🏛️ Récords del reto")

    # TOP 3 mejores semanas

    records = []

    for _, row in df.iterrows():
        for semana in semanas:
            records.append((row["Nombre"], semana, row[semana]))

    records_df = pd.DataFrame(records, columns=["Nombre", "Semana", "Minutos"])

    top3 = records_df.sort_values("Minutos", ascending=False).head(3)

    st.subheader("🥇 Mejores semanas históricas")

    for i, r in top3.iterrows():
        st.write(f"{r['Nombre']} — {r['Semana']} — {r['Minutos']} min")

    # Semana con más minutos

    totales_semana = df[semanas].sum()

    semana_record = totales_semana.idxmax()

    st.write(f"📈 Semana con más minutos: **{semana_record}** ({totales_semana.max()} min)")

    # Estabilidad (ignorando ceros)

    df_std = df[semanas].replace(0, np.nan).std(axis=1)

    atleta_estable = df.loc[df_std.idxmin(), "Nombre"]

    atleta_variable = df.loc[df_std.idxmax(), "Nombre"]

    st.write(f"🎯 Atleta más estable: **{atleta_estable}**")

    st.write(f"🌪 Atleta más variable: **{atleta_variable}**")

    # Rey del podio

    podios = (df[rank_semanas] == 1).sum(axis=1)

    atleta_podio = df.loc[podios.idxmax(), "Nombre"]

    st.write(f"👑 Rey/Reina del podio: **{atleta_podio}** ({podios.max()} semanas #1)")

    # Consistencia perfecta

    consistentes = df[(df[semanas] == 0).sum(axis=1) == 0]["Nombre"]

    if len(consistentes) > 0:
        st.write("💎 Consistencia perfecta:")
        st.write(", ".join(consistentes))

    # Mayor activación histórica

    diffs = df[semanas].diff(axis=1)

    mayor_activacion = diffs.max().max()

    idx = diffs.stack().idxmax()

    atleta = df.loc[idx[0], "Nombre"]

    st.write(f"⚡ Mayor activación histórica: **{atleta}** (+{mayor_activacion} min)")

    # Mayor bajón

    mayor_bajon = diffs.min().min()

    idx = diffs.stack().idxmin()

    atleta = df.loc[idx[0], "Nombre"]

    st.write(f"📉 Mayor bajón histórico: **{atleta}** ({mayor_bajon} min)")

    # MVPs semanales

    st.subheader("🥇 MVPs semanales")

    for semana in semanas:

        idx = df[semana].idxmax()

        atleta = df.loc[idx, "Nombre"]

        st.write(f"{semana} — {atleta}")

# =====================================================
# PANEL INDIVIDUAL
# =====================================================

if nombre and nombre != "🏆 Salón de la Fama":

    row = df[df["Nombre"] == nombre].iloc[0]

    minutos = row[semanas]

    st.title(f"📊 Estadísticas de {nombre}")

    mejor = minutos.max()
    semana_mejor = minutos.idxmax()

    promedio = minutos.mean()

    std = minutos.std()

    contribucion = minutos.sum() / total_minutos_global * 100

    ranking_general = row["Ranking general"]

    ranking_m1 = row["Ranking Mens. 1"]

    ranking_m2 = row["Ranking Mens. 2"]

    st.header("📊 Estadísticas principales")

    st.write(f"🔥 Mejor semana: **{mejor} min ({semana_mejor})**")

    st.write(f"📊 Promedio semanal: **{promedio:.1f} min**")

    st.write(f"🎯 Desviación estándar: **{std:.2f}**")

    st.write(f"🌎 Contribución al total: **{contribucion:.2f}%**")

    st.write(f"🏆 Ranking general: **#{ranking_general}**")

    if ranking_m2 < ranking_m1:
        flecha = "⬆️"
    elif ranking_m2 > ranking_m1:
        flecha = "⬇️"
    else:
        flecha = "➡️"

    st.write(f"Mes 1: **#{ranking_m1}**")

    st.write(f"Mes 2: **#{ranking_m2}** {flecha}")

    # TROFEOS

    st.header("🏅 Trofeos")

    if mejor == df[semanas].max().max():
        st.success("🏆 Récord histórico del reto")

    semanas_mvp = []

    for i, semana in enumerate(semanas):
        if row[semana] == df[semana].max():
            semanas_mvp.append(i + 1)

    if semanas_mvp:
        st.success(f"🥇 MVP en semanas {', '.join(map(str,semanas_mvp))}")

    diffs = minutos.diff()

    salto = diffs.max()

    bajon = diffs.min()

    st.write(f"⚡ Mayor salto de activación: **{salto} min**")

    st.write(f"📉 Mayor bajón: **{bajon} min**")

    if (minutos == 0).sum() == 0:
        st.success("💎 Consistencia perfecta")

    # GRAFICA

    st.header("📈 Progreso semanal")

    fig, ax = plt.subplots()

    minutos.plot(kind="line", marker="o", ax=ax)

    ax.set_ylabel("Minutos")

    ax.set_xlabel("Semana")

    st.pyplot(fig)