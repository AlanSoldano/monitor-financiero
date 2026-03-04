import streamlit as st
import pandas as pd
import os
import locale
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

from loaders.excel_loader import ExcelLoader
from processing.analyzer import Analyzer
from alerts.alerts_engine import AlertsEngine
from visualization.charts import pie_categories, line_evolution
from exports.report_generator import ReportGenerator
from config import DEFAULT_EXCEL_FILE

st.set_page_config(layout="wide")
st.title("Monitor Financiero Personal")

# ---------------------------------------------------
# Crear archivo base
# ---------------------------------------------------

if not os.path.exists(DEFAULT_EXCEL_FILE):
    df_base = pd.DataFrame(columns=["Fecha", "Tipo", "Categoria", "Monto", "Descripcion"])
    df_config = pd.DataFrame({"Clave": ["ingreso_mensual"], "Valor": [0]})

    with pd.ExcelWriter(DEFAULT_EXCEL_FILE) as writer:
        df_base.to_excel(writer, sheet_name="movimientos", index=False)
        df_config.to_excel(writer, sheet_name="configuracion", index=False)

# ---------------------------------------------------
# Tabs
# ---------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "Registrar Movimiento", "Configuración", "Ver meses anteriores", "Ver tablas"])

# ===================================================
# DASHBOARD
# ===================================================

with tab1:

    file_path = DEFAULT_EXCEL_FILE

    loader = ExcelLoader(file_path)
    df_mov, df_config = loader.load()

    df = df_mov.copy()

    # Leer ingreso
    ingreso_configurado = 0

    try:
        ingreso_configurado = float(
            df_config[df_config["Clave"] == "ingreso_mensual"]["Valor"].values[0]
        )
    except:
        ingreso_configurado = 0

    analyzer = Analyzer(df, ingreso_configurado)
    metrics = analyzer.compute_metrics()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Ingresos", f"${metrics['ingresos']:.2f}")
    col2.metric("Gastos", f"${metrics['gastos']:.2f}")
    col3.metric("Balance", f"${metrics['balance']:.2f}")
    col4.metric("Promedio Diario", f"${metrics['promedio_diario']:.2f}")

    st.divider()

    st.subheader("Presupuesto mensual")

    col5, col6, col7 = st.columns(3)

    col5.metric("Ingreso Configurado", f"${metrics['ingreso_configurado']:.2f}")
    col6.metric("Disponible Restante", f"${metrics['disponible']:.2f}")
    col7.metric("Gastado %", f"{metrics['porcentaje_gastado']:.2f}%")

# Barra visual de progreso
    if metrics["ingreso_configurado"] > 0:
        progreso = min(metrics["porcentaje_gastado"] / 100, 1.0)
        st.progress(progreso)

    st.plotly_chart(pie_categories(analyzer.gasto_por_categoria()))
    st.plotly_chart(line_evolution(analyzer.evolucion_mensual()))

    alerts = AlertsEngine(df).generate_alerts()

    st.subheader("Alertas")
    for alert in alerts:
        st.warning(alert)

    if st.button("Generar Reporte"):
        ReportGenerator("Reporte_Mensual.xlsx").generate(
            metrics,
            analyzer.gasto_por_categoria(),
            alerts,
        )
        st.success("Reporte generado correctamente")

# ===================================================
# REGISTRAR MOVIMIENTO
# ===================================================

with tab2:

    st.subheader("Registrar nuevo movimiento")

    with st.form("form_movimiento"):
        fecha = st.date_input("Fecha")
        tipo = st.selectbox("Tipo", ["Gasto", "Ingreso"])
        categoria = st.text_input("Categoría")
        monto = st.number_input("Monto", min_value=0.0, step=100.0)
        descripcion = st.text_input("Descripción")

        submitted = st.form_submit_button("Guardar")

        if submitted:

            nuevo = {
                "Fecha": fecha,
                "Tipo": tipo,
                "Categoria": categoria,
                "Monto": monto,
                "Descripcion": descripcion
            }

            df_nuevo = pd.DataFrame([nuevo])

            try:
                df_existente = pd.read_excel(DEFAULT_EXCEL_FILE, sheet_name="movimientos")
                df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
            except:
                df_final = df_nuevo

            with pd.ExcelWriter(
            DEFAULT_EXCEL_FILE,
            mode="a",
            if_sheet_exists="replace",
            engine="openpyxl"
             ) as writer:
                df_final.to_excel(writer, sheet_name="movimientos", index=False)

            st.success("Movimiento guardado correctamente")
            st.rerun()

# ===================================================
# CONFIGURACION
# ===================================================

with tab3:

    st.subheader("Configuración financiera")

    df_config = pd.read_excel(DEFAULT_EXCEL_FILE, sheet_name="configuracion")

    ingreso_actual = float(
        df_config[df_config["Clave"] == "ingreso_mensual"]["Valor"].values[0]
    )

    nuevo_ingreso = st.number_input(
        "Ingreso mensual",
        value=ingreso_actual,
        step=1000.0
    )

    if st.button("Guardar configuración"):

        df_config.loc[
            df_config["Clave"] == "ingreso_mensual",
            "Valor"
        ] = nuevo_ingreso

        with pd.ExcelWriter(
        DEFAULT_EXCEL_FILE,
        mode="a",
        if_sheet_exists="replace",
        engine="openpyxl"
        ) as writer:
            df_config.to_excel(writer, sheet_name="configuracion", index=False)

        st.success("Ingreso mensual actualizado")
        st.rerun()

# ===================================================
# RESUMEN MENSUAL
# ===================================================
with tab4:
    st.subheader("Resumen mensual")

    # Fecha → datetime
    df_mov["Fecha"] = pd.to_datetime(df_mov["Fecha"], errors="coerce")

    # Periodos mensuales
    meses_disponibles = df_mov["Fecha"].dt.to_period("M").dropna().unique()

    # Ordenamiento de manera descendente
    meses_disponibles = sorted(meses_disponibles, reverse=True)

    if len(meses_disponibles) == 0:
        st.info("No hay movimientos registrados.")
    else:
        # Expander por cada mes
        for mes in meses_disponibles:
            df_mes = df_mov[df_mov["Fecha"].dt.to_period("M") == mes]

            if df_mes.empty:
                continue

            # Period a Timestamp y nombre de mes en español
            fecha_mes = mes.to_timestamp()
            mes_nombre = fecha_mes.strftime("%B %Y").capitalize()

            with st.expander(f"📅 {mes_nombre}", expanded=False):
                analyzer_mes = Analyzer(df_mes)
                metrics_mes = analyzer_mes.compute_metrics()

                # Metricas en columnas
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Ingresos", f"${metrics_mes['ingresos']:.2f}")
                col2.metric("Gastos", f"${metrics_mes['gastos']:.2f}")
                col3.metric("Balance", f"${metrics_mes['balance']:.2f}")
                col4.metric("Promedio Diario", f"${metrics_mes['promedio_diario']:.2f}")

                # Graficos
                st.plotly_chart(
                    pie_categories(analyzer_mes.gasto_por_categoria()),
                    key=f"pie_{mes}"
                )
                st.plotly_chart(
                    line_evolution(analyzer_mes.evolucion_mensual()),
                    key=f"line_{mes}"
                )

# ===================================================
# VER TABLAS
# ===================================================
with tab5:
    st.subheader("Tablas de Movimientos y Configuración")
    st.write("Movimientos:")
    st.dataframe(df_mov)
    st.write("Configuración:")
    st.dataframe(df_config)