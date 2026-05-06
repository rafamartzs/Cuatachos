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

    st.header(f"🔥 Lo que pasó en la {ultima_semana}:")

    atletas_moviendose = (df[ultima_semana] > 0).sum()

    minutos_totales = df[ultima_semana].sum()

    promedio = minutos_totales / atletas_moviendose if atletas_moviendose > 0 else 0

    despertaron = df[(df[semana_previa] == 0) & (df[ultima_semana] > 0)]["Nombre"].tolist()
    
    durmieron = df[(df[semana_previa] > 0) & (df[ultima_semana] == 0)]["Nombre"].tolist()

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
        st.markdown(f"**{', '.join(despertaron)}**")

    if durmieron:
        st.write("😴 Se durmieron:")
        st.markdown(f"**{', '.join(durmieron)}**")

    st.write(f"⚡ Mayor activación: **{atleta_activacion}** (+{diff.max()} min)")
    st.write(f"😴 Mayor relajación: **{atleta_relajado}** ({diff.min()} min)")

    st.subheader("🥇 Top 3 de la semana:")

    top3_semana = df.sort_values(ultima_semana, ascending=False).head(3)

    for _, row in top3_semana.iterrows():
        st.write(f"**{row['Nombre']} — {row[ultima_semana]} min**")

# -----------------------------------
# Tendencia positiva
# -----------------------------------

    def tendencia_positiva_hasta_final(serie):
    # Convertir a numérico y conservar los 0 como cortadores de tendencia
        serie = pd.to_numeric(serie, errors="coerce").fillna(0)

        count = 0

        for i in range(1, len(serie)):
            if serie.iloc[i] > serie.iloc[i - 1] and serie.iloc[i] != 0:
                count += 1
            else:
                count = 0

    # Solo cuenta si la tendencia positiva llega hasta la última semana
        if len(serie) >= 2 and serie.iloc[-1] > serie.iloc[-2] and serie.iloc[-1] != 0:
            return count + 1
        else:
            return 0

# Calcular tendencias
    tendencias_final = df[semanas].apply(tendencia_positiva_hasta_final, axis=1)

    max_tendencia = tendencias_final.max()

    if max_tendencia > 0:
        ganadores = df.loc[tendencias_final == max_tendencia, "Nombre"].tolist()
    
        nombres = ", ".join(ganadores)
    
        st.subheader("Tendencias:")
    
        if len(ganadores) == 1:
            st.write(f"🏅 Golden Trend Athlete: **{nombres}** ({max_tendencia} semanas con tendencia positiva)")
        else:
            st.write(f"🏅 Golden Trend Athletes: **{nombres}** ({max_tendencia} semanas con tendencia positiva)")
    # -----------------------------------
    # RÉCORDS HISTÓRICOS
    # -----------------------------------

    st.header("🏛️ Récords del reto:")

    records = []

    for _, row in df.iterrows():
        for semana in semanas:
            records.append((row["Nombre"], semana, row[semana]))

    records_df = pd.DataFrame(records, columns=["Nombre", "Semana", "Minutos"])

    top3 = records_df.sort_values("Minutos", ascending=False).head(3)

    st.subheader("🥇 Mejores tiempos históricos:")

    for _, r in top3.iterrows():
        st.success(f"{r['Nombre']} — {r['Semana']} — {r['Minutos']} min")

    totales_semana = df[semanas].sum()

    semana_record = totales_semana.idxmax()
    st.subheader("⚡Atletas que han logrado 1000 minutos más rápido:")
    st.success("Ed Guillén (Semanas 1 y 2)")
    st.success("Miriam Sarreón (Semanas 1 y 2)")
    st.success("Gaby Rodríguez (Semanas 1 y 2)")
    st.success("Roma Velázquez (Semanas 1 y 2)")
    st.success("Luis Sarreón (Semanas 1 y 2)")


    # Estabilidad

    # Contar semanas en 0
    semanas_cero = (df[semanas] == 0).sum(axis=1)

# Filtrar atletas con menos de 2 semanas en 0
    df_filtrado = df[semanas_cero < 2].copy()

# Calcular desviación estándar ignorando ceros
    df_std = df_filtrado[semanas].replace(0, np.nan).std(axis=1)

    idx_estable = df_std.idxmin()
    idx_variable = df_std.idxmax()

    atleta_estable = df_filtrado.loc[idx_estable, "Nombre"]
    atleta_variable = df_filtrado.loc[idx_variable, "Nombre"]
    st.subheader("🎯 Atleta más estable:")
    st.success(f"**{atleta_estable}** (σ = {df_std.min():.2f})")
    st.subheader("🌪 Atleta más variable:")
    st.success(f"**{atleta_variable}** (σ = {df_std.max():.2f})")

    podios = (df[rank_semanas] == 1).sum(axis=1)

    max_podios = podios.max()

    ganadores = df.loc[podios == max_podios, "Nombre"].tolist()

    nombres = ", ".join(ganadores)

    if len(ganadores) == 1:
        st.subheader("👑 Monarca del podio:")
        st.success(f"**{nombres}** ({max_podios} semanas #1)")
    else:
        st.subheader("👑 Monarcas del podio:")
        st.success(f"**{nombres}** ({max_podios} semanas #1)")
    # Consistencia perfecta

    consistentes = df[(df[semanas] == 0).sum(axis=1) == 0]["Nombre"]

    if len(consistentes) > 0:
        st.subheader("💎 Consistencia perfecta:")
        st.success(", ".join(consistentes))

    # Activación histórica

    diffs = df[semanas].diff(axis=1)

    mayor_activacion = diffs.max().max()
    idx = diffs.stack().idxmax()

    atleta = df.loc[idx[0], "Nombre"]
    semana = idx[1]
    st.subheader("⚡ Mayor activación histórica:")
    st.success(f"**{atleta}** (+{mayor_activacion} min en {semana})")

    mayor_bajon = diffs.min().min()
    idx = diffs.stack().idxmin()

    atleta = df.loc[idx[0], "Nombre"]
    semana = idx[1]
    st.subheader("📉 Mayor bajón histórico:")
    st.success(f"**{atleta}** ({mayor_bajon} min en {semana})")

    st.write(f"📈 Semana con más minutos: **{semana_record}** ({totales_semana.max()} min)")
# MVPs semanales

    st.subheader("🥇 MVPs semanales:")

    for semana in semanas:
 
        idx = df[semana].idxmax()

        atleta = df.loc[idx, "Nombre"]

        minutos = df.loc[idx, semana]

        st.success(f"{semana} — {atleta} ({minutos} min)")

    st.subheader("Minutos por género:")

    df_genero = df.groupby("Sexo")[semanas].sum().sum(axis=1)

    st.bar_chart(df_genero)

    st.subheader("Promedio por edades")

    df_edades = df.groupby("Edades")["Total"].mean().sort_values(ascending=False)

    st.bar_chart(df_edades)

    st.subheader("Promedio por regiones:")

    df_regiones = df.groupby("Regiones")["Total"].mean().sort_values(ascending=False)

    st.bar_chart(df_regiones)

# =====================================================
# PANEL INDIVIDUAL
# =====================================================

if nombre and nombre != "🏆 Salón de la Fama":

    row = df[df["Nombre"] == nombre].iloc[0]

    minutos = row[semanas]

    st.title(f"📊 Cifras de {nombre}")

    mejor = minutos.max()
    semana_mejor = minutos.idxmax()

    promedio = minutos.mean()

    std = minutos.replace(0, np.nan).std()
    
    contribucion = minutos.sum() / total_minutos_global * 100

    ranking_general = row["Ranking general"]

    
    st.header("Estadísticas principales")

    st.write(f"🔥 Mejor semana: **{mejor} min ({semana_mejor})**")
    st.write(f"📊 Promedio semanal: **{promedio:.1f} min**")
    st.write(f"🎯 Desviación estándar: **{std:.2f}**")
    # Mostrar mensaje si es menor a 100
    if std < 100:
        st.success("¡Felicidades! Eres de los atletas más estables")
    st.write(f"🌎 Contribución al total: **{contribucion:.2f}%**")
    st.write(f"🏆 Ranking general: **#{ranking_general}**")

    

    # Saltos personales

    diffs = minutos.diff()

    salto = diffs.max()
    semana_salto = diffs.idxmax()

    bajon = diffs.min()
    semana_bajon = diffs.idxmin()

    st.write(f"⚡ Mayor salto de activación: **{salto} min ({semana_salto})**")
    st.write(f"📉 Mayor bajón: **{bajon} min ({semana_bajon})**")

    # -----------------------------------
    # PROGRESO A 1000 MIN (MES 1)
    # -----------------------------------

    meta = 1000

    minutos_actuales = row[semanas[-2:]].sum()

    faltante = meta - minutos_actuales

    if faltante > 0:
       st.write(f"🎯 Te faltan **{faltante:.0f} min** para llegar a 1000")
    else:
        st.success(f"🏆 ¡Lograste superar los 1000 minutos del mes 1! (+{abs(faltante):.0f})")

    # -----------------------------------
    # TROFEOS
    # -----------------------------------
    
    st.header("🏅 Trofeos")
    # Posición general (siempre aparece)
    st.info(f"🎖 Posición general actual: **#{ranking_general}**")
    mejor_global = df[semanas].max().max()

    mejor_mes1 = df[semanas[:4]].max().max()

    if row[semanas[:4]].max() == mejor_mes1:
        semana = row[semanas[:4]].idxmax()
        st.success(f"🥇 Mejor tiempo Mes 1 ({row[semana]} min en {semana})")

    mejor_mes2 = df[semanas[4:8]].max().max()

    if row[semanas[4:8]].max() == mejor_mes2:
        semana = row[semanas[4:8]].idxmax()
        st.success(f"🥇 Mejor tiempo Mes 2 ({row[semana]} min en {semana})")

    mejor_mes3 = df[semanas[9:12]].max().max()

    if row[semanas[9:12]].max() == mejor_mes3:
        semana = row[semanas[9:12]].idxmax()
        st.success(f"🥇 Mejor tiempo Mes 3 ({row[semana]} min en {semana})")

    # Rey/Reina del podio (con empates)

    podios = (df[rank_semanas] == 1).sum(axis=1)

    max_podios = podios.max()

    ganadores_podio = df.loc[podios == max_podios, "Nombre"].tolist()

    if nombre in ganadores_podio:
        st.success(f"👑 Monarca del podio ({max_podios} semanas #1)")

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

    # Estabilidad (solo atletas con menos de 2 semanas en 0)

    semanas_cero = (df[semanas] == 0).sum(axis=1)

    df_filtrado = df[semanas_cero < 2].copy()

    if not df_filtrado.empty:
        df_std = df_filtrado[semanas].replace(0, np.nan).std(axis=1)

        idx_estable = df_std.idxmin()

        if nombre == df_filtrado.loc[idx_estable, "Nombre"]:
            st.success(f"🎯 Atleta más estable del reto (σ = {df_std.min():.2f})")

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

 # Ranking minutos mes 1

    st.subheader("📊 Ranking de minutos Mes 1")

    semanas_mes1 = semanas[-4:]

    df_mes1 = df[["Nombre"] + semanas_mes1].copy()

    df_mes1["Total Mes1"] = df_mes1[semanas_mes1].sum(axis=1)

    df_mes1_sorted = df_mes1.sort_values("Total Mes1", ascending=False)

    colors = ["#ff69b4" if n == nombre else "#1f77b4" for n in df_mes1_sorted["Nombre"]]

    fig2, ax2 = plt.subplots(figsize=(10,5))

    ax2.bar(df_mes3_sorted["Nombre"], df_mes1_sorted["Total Mes1"], color=colors)
    
    ax2.axhline(y=1000, color='red', linestyle='--', linewidth=2, label='Objetivo 1000 min')
    ax2.legend()

    ax2.set_ylabel("Minutos Mes 1")

    ax2.set_xlabel("Atletas")

    ax2.set_title("Ranking de minutos Mes 1")

    plt.xticks(rotation=45, ha="right")

    st.pyplot(fig2)


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

