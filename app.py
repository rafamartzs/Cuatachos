import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Cuatachos Wrapped", layout="wide")

# -----------------------------------
# FUNCIONES
# -----------------------------------

def tendencia_positiva(serie):

    diffs = serie.diff()

    count = 0
    best = 0

    for d in diffs[1:]:

        if d > 0:
            count += 1
            best = max(best, count)
        else:
            count = 0

    return best

# -----------------------------------
# CARGAR DATOS
# -----------------------------------

df = pd.read_excel("reto_cuatachos.xlsx")

semanas = [c for c in df.columns if "Semana" in c]
rank_semanas = [c for c in df.columns if "Ranking " in c and "Mens" not in c and "general" not in c]

ultima_semana = semanas[-1]
semana_previa = semanas[-2]

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

    for _, row in top3_semana.iterrows():
        st.write(f"{row['Nombre']} — {row[ultima_semana]} min")

    # -----------------------------------
    # RÉCORDS HISTÓRICOS
    # -----------------------------------

    st.header("🏛️ Récords del reto")

    records = []

    for _, row in df.iterrows():
        for semana in semanas:
            records.append((row["Nombre"], semana, row[semana]))

    records_df = pd.DataFrame(records, columns=["Nombre", "Semana", "Minutos"])

    top3 = records_df.sort_values("Minutos", ascending=False).head(3)

    st.subheader("🥇 Mejores semanas históricas")

    for _, r in top3.iterrows():
        st.write(f"{r['Nombre']} — {r['Semana']} — {r['Minutos']} min")

    totales_semana = df[semanas].sum()

    semana_record = totales_semana.idxmax()

    st.write(f"📈 Semana con más minutos: **{semana_record}** ({totales_semana.max()} min)")

    # Estabilidad

    df_std = df[semanas].replace(0, np.nan).std(axis=1)

    idx_estable = df_std.idxmin()
    idx_variable = df_std.idxmax()

    atleta_estable = df.loc[idx_estable, "Nombre"]
    atleta_variable = df.loc[idx_variable, "Nombre"]

    st.write(f"🎯 Atleta más estable: **{atleta_estable}** (σ = {df_std.min():.2f})")
    st.write(f"🌪 Atleta más variable: **{atleta_variable}** (σ = {df_std.max():.2f})")

    # Rey del podio

    podios = (df[rank_semanas] == 1).sum(axis=1)

    atleta_podio = df.loc[podios.idxmax(), "Nombre"]

    st.write(f"👑 Rey/Reina del podio: **{atleta_podio}** ({podios.max()} semanas #1)")

    # Consistencia perfecta

    consistentes = df[(df[semanas] == 0).sum(axis=1) == 0]["Nombre"]

    if len(consistentes) > 0:
        st.write("💎 Consistencia perfecta:")
        st.write(", ".join(consistentes))

    # Activación histórica

    diffs = df[semanas].diff(axis=1)

    mayor_activacion = diffs.max().max()
    idx = diffs.stack().idxmax()

    atleta = df.loc[idx[0], "Nombre"]
    semana = idx[1]

    st.write(f"⚡ Mayor activación histórica: **{atleta}** (+{mayor_activacion} min en {semana})")

    mayor_bajon = diffs.min().min()
    idx = diffs.stack().idxmin()

    atleta = df.loc[idx[0], "Nombre"]
    semana = idx[1]

    st.write(f"📉 Mayor bajón histórico: **{atleta}** ({mayor_bajon} min en {semana})")
# MVPs semanales

    st.subheader("🥇 MVPs semanales")

    for semana in semanas:
 
        idx = df[semana].idxmax()

        atleta = df.loc[idx, "Nombre"]

        minutos = df.loc[idx, semana]

        st.write(f"{semana} — {atleta} ({minutos} min)")

    st.subheader("👥 Análisis por género")

    df_genero = df.groupby("Sexo")[semanas].sum().sum(axis=1)

    st.bar_chart(df_genero)

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

    std = minutos.replace(0, np.nan).std()
    
    contribucion = minutos.sum() / total_minutos_global * 100

    ranking_general = row["Ranking general"]

    ranking_m1 = row["Ranking Mens. 1"]
    ranking_m2 = row["Ranking Mens. 2"]

    st.header("📊 Estadísticas principales")

    st.write(f"🔥 Mejor semana: **{mejor} min ({semana_mejor})**")
    st.write(f"📊 Promedio semanal: **{promedio:.1f} min**")
    st.write(f"🎯 Desviación estándar: **{std:.2f}**")
    # Mostrar mensaje si es menor a 100
    if std < 100:
        st.success("¡Felicidades! Eres de los atletas más estables")
    st.write(f"🌎 Contribución al total: **{contribucion:.2f}%**")
    st.write(f"🏆 Ranking general: **#{ranking_general}**")

    # Cambio de ranking

    if ranking_m2 < ranking_m1:
        flecha = "⬆️"
    elif ranking_m2 > ranking_m1:
        flecha = "⬇️"
    else:
        flecha = "➡️"

    st.write(f"Mes 1: **#{ranking_m1}**")
    st.write(f"Mes 2: **#{ranking_m2}** {flecha}")

    # Saltos personales

    diffs = minutos.diff()

    salto = diffs.max()
    semana_salto = diffs.idxmax()

    bajon = diffs.min()
    semana_bajon = diffs.idxmin()

    st.write(f"⚡ Mayor salto de activación: **{salto} min ({semana_salto})**")
    st.write(f"📉 Mayor bajón: **{bajon} min ({semana_bajon})**")

    # -----------------------------------
    # PROGRESO A 1000 MIN (MES 3)
    # -----------------------------------

    meta = 1000

    minutos_actuales = row[ultima_semana]

    faltante = meta - minutos_actuales

    if faltante > 0:
       st.write(f"🎯 Te faltan **{faltante:.0f} min** para llegar a 1000")
    else:
        st.success(f"🏆 ¡Ya superaste los 1000 min! (+{abs(faltante):.0f})")

# -----------------------------------
# PREDICCIÓN FUTURA (REGRESIÓN)
# -----------------------------------

    st.subheader("🔮 Predicción semanas 10–12 (regresión)")

# Tomar últimas 4 semanas
    ultimas_4 = minutos[-4:]

# Convertir semanas a números (ej: "Semana 6" → 6)
    x = [int(s.split()[1]) for s in ultimas_4.index]
    y = ultimas_4.values

# Ajustar regresión lineal
    coef = np.polyfit(x, y, 1)  # grado 1 = línea
    m, b = coef

# Semanas futuras
    semanas_futuras = [x[-1] + 1, x[-1] + 2, x[-1] + 3]

    predicciones = {}

    for s in semanas_futuras:
        pred = m * s + b
        pred = max(pred, 0)  # evitar negativos
        predicciones[f"Semana {s}"] = pred

# Mostrar predicciones
    for semana, valor in predicciones.items():
       st.write(f"{semana}: **{valor:.1f} min**")

# Total proyectado
    total_estimado = minutos.sum() + sum(predicciones.values())

    st.write(f"🏁 Total proyectado: **{total_estimado:.0f} min**")

    # -----------------------------------
    # TROFEOS
    # -----------------------------------
    
    st.header("🏅 Trofeos")
    # Posición general (siempre aparece)
    st.info(f"🎖 Posición general actual: **#{ranking_general}**")
    mejor_global = df[semanas].max().max()

    if mejor == mejor_global:
        st.success(f"🏆 Mejor tiempo histórico ({mejor} min en {semana_mejor})")

    mejor_mes1 = df[semanas[:4]].max().max()

    if row[semanas[:4]].max() == mejor_mes1:
        semana = row[semanas[:4]].idxmax()
        st.success(f"🥇 Mejor tiempo Mes 1 ({row[semana]} min en {semana})")

    mejor_mes2 = df[semanas[4:8]].max().max()

    if row[semanas[4:8]].max() == mejor_mes2:
        semana = row[semanas[4:8]].idxmax()
        st.success(f"🥇 Mejor tiempo Mes 2 ({row[semana]} min en {semana})")

    # Rey del podio

    podios = (df[rank_semanas] == 1).sum(axis=1)

    if nombre == df.loc[podios.idxmax(), "Nombre"]:
        st.success(f"👑 Rey/Reina del podio ({podios.max()} semanas #1)")

    # Tendencia positiva

    tendencias = df[semanas].apply(tendencia_positiva, axis=1)

    idx = tendencias.idxmax()

    if nombre == df.loc[idx, "Nombre"]:
        st.success(f"📈 Mayor tendencia positiva ({tendencias.max()} semanas seguidas subiendo)")
    # Mayor salto de activación histórico

    diffs_global = df[semanas].diff(axis=1)

    mayor_salto = diffs_global.max().max()

    idx = diffs_global.stack().idxmax()

    atleta_salto = df.loc[idx[0], "Nombre"]

    semana_salto = idx[1]

    if nombre == atleta_salto:
        st.success(f"⚡ Mayor salto de activación histórico (+{mayor_salto} min en {semana_salto})")

    # Estabilidad

    df_std = df[semanas].replace(0, np.nan).std(axis=1)

    if nombre == df.loc[df_std.idxmin(), "Nombre"]:
        st.success("🎯 Atleta más estable del reto")

    # Consistencia perfecta

    if (minutos == 0).sum() == 0:
        st.success("💎 Consistencia perfecta")
    
# MVPs semanales del atleta

    for semana in semanas:

        if row[semana] == df[semana].max():

            st.success(f"🥇 MVP en {semana} ({row[semana]} min)")

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

 # Ranking minutos mes 3

    st.subheader("📊 Ranking de minutos Mes 3")

    ultima_semana = semanas[-2]

    df_mes3 = df[["Nombre", ultima_semana]].copy()

    df_mes3["Total Mes3"] = df_mes3[ultima_semana]

    df_mes3_sorted = df_mes3.sort_values("Total Mes3", ascending=False)

    colors = ["#ff69b4" if n == nombre else "#1f77b4" for n in df_mes3_sorted["Nombre"]]

    fig2, ax2 = plt.subplots(figsize=(10,5))

    ax2.bar(df_mes3_sorted["Nombre"], df_mes3_sorted["Total Mes3"], color=colors)

    ax2.set_ylabel("Minutos Mes 3")

    ax2.set_xlabel("Atletas")

    ax2.set_title("Ranking de minutos Mes 3")

    plt.xticks(rotation=45, ha="right")

    st.pyplot(fig2)

# -----------------------------------
# HISTOGRAMA DE MINUTOS
# -----------------------------------

    st.subheader("📊 Distribución de minutos")

    fig_hist, ax_hist = plt.subplots()

    valores = minutos.replace(0, np.nan).dropna()

    ax_hist.hist(valores)

    ax_hist.set_xlabel("Minutos")
    ax_hist.set_ylabel("Frecuencia")
    ax_hist.set_title("Distribución de minutos por semana")

    st.pyplot(fig_hist)

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

 # =================================================
 # GRÁFICA DE EVOLUCIÓN DEL RANKING SEMANAL
 # =================================================

    st.subheader("📈 Evolución del ranking semanal")

    # Construimos un DataFrame con las posiciones semanales
    df_ranking = df[["Nombre"] + rank_semanas].copy()

    # Invertimos el ranking para que #1 quede arriba en la gráfica
    for col in rank_semanas:
        df_ranking[col] = df_ranking[col]  # los rankings ya son numéricos, #1 es el mejor

    fig4, ax4 = plt.subplots(figsize=(12,6))

    for i, row in df_ranking.iterrows():
        if row["Nombre"] == nombre:
            ax4.plot(rank_semanas, row[rank_semanas], marker='o', linewidth=3, color="#ff69b4",      label=row["Nombre"])
        else:
            ax4.plot(rank_semanas, row[rank_semanas], marker='o', linewidth=1.5, alpha=0.5, color="#1f77b4")

    ax4.invert_yaxis()  # #1 arriba
    ax4.set_xlabel("Semanas")
    ax4.set_ylabel("Ranking")
    ax4.set_title("Evolución del ranking semanal de atletas")
    ax4.legend(loc="upper right", fontsize=10)
    plt.xticks(rotation=45)
    st.pyplot(fig4)

# =================================================
# EVOLUCIÓN DEL RANKING GENERAL (ACUMULADO)
# =================================================

    st.subheader("🏁 Evolución del ranking general (acumulado)")

# Construir acumulados semana a semana
    df_acum = df[["Nombre"] + semanas].copy()

    for i, semana in enumerate(semanas):
        if i == 0:
            df_acum[semana] = df[semana]
        else:
            df_acum[semana] = df_acum[semanas[:i+1]].sum(axis=1)

# Calcular ranking por semana
    ranking_acum = pd.DataFrame()
    ranking_acum["Nombre"] = df["Nombre"]

    for semana in semanas:
        ranking_acum[semana] = df_acum[semana].rank(ascending=False, method="min")

# Plot
    fig_rank, ax_rank = plt.subplots(figsize=(12,6))

    for i, row in ranking_acum.iterrows():
        if row["Nombre"] == nombre:
            ax_rank.plot(semanas, row[semanas], marker='o', linewidth=3)
        else:
            ax_rank.plot(semanas, row[semanas], marker='o', linewidth=1, alpha=0.4)

    ax_rank.invert_yaxis()
    ax_rank.set_xlabel("Semanas")
    ax_rank.set_ylabel("Ranking acumulado")
    ax_rank.set_title("Carrera por el ranking general")

    plt.xticks(rotation=45)
    st.pyplot(fig_rank)