import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Ventas Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar session state para cross-filtering
if 'filtro_producto' not in st.session_state:
    st.session_state.filtro_producto = None
if 'filtro_region' not in st.session_state:
    st.session_state.filtro_region = None
if 'nivel_detalle' not in st.session_state:
    st.session_state.nivel_detalle = 'mes'
if 'mes_seleccionado' not in st.session_state:
    st.session_state.mes_seleccionado = None

# Título principal
st.title("📊 Dashboard Interactivo PRO con IA")
st.markdown("**🎯 Click en los gráficos para filtrar | 🔍 Drill-down disponible | ⏯️ Modo animación activo**")
st.markdown("---")

# Función para generar datos inventados
@st.cache_data
def generar_datos():
    np.random.seed(42)
    
    # Generar fechas
    fechas = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    
    # Productos
    productos = ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Audífonos', 'Webcam']
    
    # Regiones
    regiones = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
    
    # Generar datos aleatorios
    datos = []
    for fecha in fechas:
        for _ in range(np.random.randint(5, 15)):
            producto = np.random.choice(productos)
            region = np.random.choice(regiones)
            
            # Precios base por producto
            precios_base = {
                'Laptop': 800,
                'Monitor': 300,
                'Teclado': 50,
                'Mouse': 25,
                'Audífonos': 60,
                'Webcam': 80
            }
            
            precio = precios_base[producto] * np.random.uniform(0.8, 1.2)
            cantidad = np.random.randint(1, 10)
            venta_total = precio * cantidad
            
            datos.append({
                'Fecha': fecha,
                'Producto': producto,
                'Region': region,
                'Cantidad': cantidad,
                'Precio_Unitario': round(precio, 2),
                'Venta_Total': round(venta_total, 2)
            })
    
    df = pd.DataFrame(datos)
    df['Mes'] = df['Fecha'].dt.to_period('M').astype(str)
    df['Semana'] = df['Fecha'].dt.to_period('W').astype(str)
    df['Año'] = df['Fecha'].dt.year
    df['Dia_Semana'] = df['Fecha'].dt.day_name()
    
    return df

# Función para predicciones
def predecir_ventas(df, meses_futuro=3):
    # Agrupar por mes
    ventas_mensuales = df.groupby('Mes')['Venta_Total'].sum().reset_index()
    ventas_mensuales['Fecha'] = pd.to_datetime(ventas_mensuales['Mes'])
    ventas_mensuales = ventas_mensuales.sort_values('Fecha')
    
    # Preparar datos para regresión
    ventas_mensuales['dias_desde_inicio'] = (ventas_mensuales['Fecha'] - ventas_mensuales['Fecha'].min()).dt.days
    
    X = ventas_mensuales['dias_desde_inicio'].values.reshape(-1, 1)
    y = ventas_mensuales['Venta_Total'].values
    
    # Modelo de regresión lineal
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    # Generar predicciones
    ultima_fecha = ventas_mensuales['Fecha'].max()
    fechas_futuras = pd.date_range(start=ultima_fecha + timedelta(days=30), periods=meses_futuro, freq='ME')
    
    predicciones = []
    for fecha in fechas_futuras:
        dias = (fecha - ventas_mensuales['Fecha'].min()).days
        pred = modelo.predict([[dias]])[0]
        predicciones.append({
            'Fecha': fecha,
            'Mes': fecha.strftime('%Y-%m'),
            'Venta_Predicha': max(0, pred),
            'Tipo': 'Predicción'
        })
    
    # Agregar datos históricos
    historico = ventas_mensuales[['Fecha', 'Mes', 'Venta_Total']].copy()
    historico['Tipo'] = 'Histórico'
    historico.rename(columns={'Venta_Total': 'Venta_Predicha'}, inplace=True)
    
    # Combinar
    resultado = pd.concat([historico, pd.DataFrame(predicciones)], ignore_index=True)
    
    return resultado, modelo.coef_[0], modelo.intercept_

# Cargar datos
df = generar_datos()

# SIDEBAR - Filtros y controles
st.sidebar.header("🎛️ Centro de Control")

# Modo de visualización
modo = st.sidebar.radio(
    "🔍 Modo de Análisis",
    ["📊 Dashboard Completo", "⏯️ Animación Temporal", "🔬 Drill-Down"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.header("🔍 Filtros Tradicionales")

# Filtro de fecha
fecha_min = df['Fecha'].min()
fecha_max = df['Fecha'].max()
fecha_inicio, fecha_fin = st.sidebar.date_input(
    "Rango de fechas",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)

# Filtro de región
regiones_disponibles = df['Region'].unique()
regiones_seleccionadas = st.sidebar.multiselect(
    "Regiones",
    options=regiones_disponibles,
    default=regiones_disponibles
)

# Filtro de producto
productos_disponibles = df['Producto'].unique()
productos_seleccionados = st.sidebar.multiselect(
    "Productos",
    options=productos_disponibles,
    default=productos_disponibles
)

st.sidebar.markdown("---")
st.sidebar.header("🎯 Filtros Dinámicos (Cross-Filter)")

# Mostrar filtros activos
if st.session_state.filtro_producto:
    st.sidebar.info(f"🔹 Producto: **{st.session_state.filtro_producto}**")
    if st.sidebar.button("❌ Limpiar filtro producto"):
        st.session_state.filtro_producto = None
        st.rerun()

if st.session_state.filtro_region:
    st.sidebar.info(f"🔹 Región: **{st.session_state.filtro_region}**")
    if st.sidebar.button("❌ Limpiar filtro región"):
        st.session_state.filtro_region = None
        st.rerun()

if st.session_state.filtro_producto or st.session_state.filtro_region:
    if st.sidebar.button("🔄 Limpiar TODOS los filtros dinámicos"):
        st.session_state.filtro_producto = None
        st.session_state.filtro_region = None
        st.session_state.mes_seleccionado = None
        st.rerun()

# Configuración de predicción
st.sidebar.markdown("---")
st.sidebar.header("🔮 Predicciones")
meses_prediccion = st.sidebar.slider(
    "Meses a predecir",
    min_value=1,
    max_value=6,
    value=3
)

# Aplicar filtros tradicionales
df_filtrado = df[
    (df['Fecha'] >= pd.to_datetime(fecha_inicio)) &
    (df['Fecha'] <= pd.to_datetime(fecha_fin)) &
    (df['Region'].isin(regiones_seleccionadas)) &
    (df['Producto'].isin(productos_seleccionados))
]

# Aplicar filtros dinámicos (cross-filtering)
if st.session_state.filtro_producto:
    df_filtrado = df_filtrado[df_filtrado['Producto'] == st.session_state.filtro_producto]

if st.session_state.filtro_region:
    df_filtrado = df_filtrado[df_filtrado['Region'] == st.session_state.filtro_region]

if st.session_state.mes_seleccionado:
    df_filtrado = df_filtrado[df_filtrado['Mes'] == st.session_state.mes_seleccionado]

# ============ MODO ANIMACIÓN TEMPORAL ============
if modo == "⏯️ Animación Temporal":
    st.header("⏯️ Animación Temporal de Ventas")
    
    # Preparar datos para animación
    df_animacion = df_filtrado.groupby(['Mes', 'Producto'])['Venta_Total'].sum().reset_index()
    df_animacion['Fecha'] = pd.to_datetime(df_animacion['Mes'])
    df_animacion = df_animacion.sort_values('Fecha')
    
    # Gráfico animado
    fig_animado = px.bar(
        df_animacion,
        x='Producto',
        y='Venta_Total',
        color='Producto',
        animation_frame='Mes',
        title="📈 Evolución de Ventas por Producto (Animado)",
        range_y=[0, df_animacion['Venta_Total'].max() * 1.1]
    )
    
    fig_animado.update_layout(
        height=600,
        showlegend=True,
        xaxis_title="Producto",
        yaxis_title="Ventas ($)"
    )
    
    st.plotly_chart(fig_animado, use_container_width=True)
    
    # Gráfico de evolución animado por región
    df_animacion_region = df_filtrado.groupby(['Mes', 'Region'])['Venta_Total'].sum().reset_index()
    df_animacion_region['Fecha'] = pd.to_datetime(df_animacion_region['Mes'])
    
    fig_animado_region = px.line(
        df_animacion_region,
        x='Fecha',
        y='Venta_Total',
        color='Region',
        animation_frame='Mes',
        title="🗺️ Evolución de Ventas por Región",
        markers=True
    )
    
    fig_animado_region.update_layout(height=500)
    st.plotly_chart(fig_animado_region, use_container_width=True)

# ============ MODO DRILL-DOWN ============
elif modo == "🔬 Drill-Down":
    st.header("🔬 Análisis Drill-Down")
    
    # Selector de nivel
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        nivel_actual = st.selectbox(
            "📊 Nivel de Detalle",
            ["Mes", "Semana", "Día"],
            index=["Mes", "Semana", "Día"].index(st.session_state.nivel_detalle.capitalize())
        )
        st.session_state.nivel_detalle = nivel_actual.lower()
    
    with col2:
        if st.button("🔄 Resetear Drill-Down"):
            st.session_state.nivel_detalle = 'mes'
            st.session_state.mes_seleccionado = None
            st.rerun()
    
    # Agrupar según nivel
    if st.session_state.nivel_detalle == 'mes':
        df_drill = df_filtrado.groupby('Mes')['Venta_Total'].sum().reset_index()
        df_drill['Periodo'] = df_drill['Mes']
    elif st.session_state.nivel_detalle == 'semana':
        df_drill = df_filtrado.groupby('Semana')['Venta_Total'].sum().reset_index()
        df_drill['Periodo'] = df_drill['Semana']
    else:
        df_drill = df_filtrado.groupby('Fecha')['Venta_Total'].sum().reset_index()
        df_drill['Periodo'] = df_drill['Fecha'].astype(str)
    
    # Gráfico drill-down
    fig_drill = px.bar(
        df_drill,
        x='Periodo',
        y='Venta_Total',
        title=f"📊 Ventas por {nivel_actual}",
        color='Venta_Total',
        color_continuous_scale='Viridis'
    )
    
    fig_drill.update_layout(
        height=500,
        xaxis_title=nivel_actual,
        yaxis_title="Ventas ($)"
    )
    
    st.plotly_chart(fig_drill, use_container_width=True)
    
    # Selector de período para drill-down
    if st.session_state.nivel_detalle == 'mes':
        st.subheader("🔽 Selecciona un mes para ver detalle semanal")
        mes_opciones = df_drill['Mes'].tolist()
        mes_sel = st.selectbox("Mes:", mes_opciones)
        
        if st.button("⬇️ Drill-Down a Semanas"):
            st.session_state.nivel_detalle = 'semana'
            st.session_state.mes_seleccionado = mes_sel
            st.rerun()
    
    # Mostrar detalle del período seleccionado
    st.subheader(f"📋 Top 10 Transacciones del Período")
    df_detalle = df_filtrado.nlargest(10, 'Venta_Total')[['Fecha', 'Producto', 'Region', 'Venta_Total']]
    st.dataframe(df_detalle, use_container_width=True, hide_index=True)

# ============ MODO DASHBOARD COMPLETO ============
else:
    # MÉTRICAS PRINCIPALES
    st.header("📈 Métricas Clave")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ventas_totales = df_filtrado['Venta_Total'].sum()
        st.metric(
            label="Ventas Totales",
            value=f"${ventas_totales:,.0f}",
            delta="↑ 12.5%"
        )
    
    with col2:
        num_transacciones = len(df_filtrado)
        st.metric(
            label="Transacciones",
            value=f"{num_transacciones:,}",
            delta="↑ 8.2%"
        )
    
    with col3:
        ticket_promedio = df_filtrado['Venta_Total'].mean()
        st.metric(
            label="Ticket Promedio",
            value=f"${ticket_promedio:.2f}",
            delta="↑ 3.7%"
        )
    
    with col4:
        productos_vendidos = df_filtrado['Cantidad'].sum()
        st.metric(
            label="Productos Vendidos",
            value=f"{productos_vendidos:,}",
            delta="↑ 15.3%"
        )
    
    st.markdown("---")
    
    # SECCIÓN DE PREDICCIONES
    st.header("🔮 Predicción de Ventas con IA")
    
    # Generar predicciones
    df_prediccion, tendencia, intercepto = predecir_ventas(df_filtrado, meses_prediccion)
    
    # Calcular ventas predichas totales
    ventas_predichas = df_prediccion[df_prediccion['Tipo'] == 'Predicción']['Venta_Predicha'].sum()
    
    # Métricas de predicción
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label=f"Ventas Proyectadas ({meses_prediccion} meses)",
            value=f"${ventas_predichas:,.0f}",
            delta=f"Tendencia: {'↑' if tendencia > 0 else '↓'}"
        )
    
    with col2:
        promedio_mensual = df_prediccion[df_prediccion['Tipo'] == 'Predicción']['Venta_Predicha'].mean()
        st.metric(
            label="Promedio Mensual Proyectado",
            value=f"${promedio_mensual:,.0f}"
        )
    
    with col3:
        tasa_crecimiento = (tendencia / df_filtrado.groupby('Mes')['Venta_Total'].sum().mean()) * 100
        st.metric(
            label="Tasa de Crecimiento",
            value=f"{tasa_crecimiento:.2f}%"
        )
    
    # Gráfico de predicción con tendencia
    st.subheader("📊 Histórico vs Predicción")
    
    fig_pred = go.Figure()
    
    # Datos históricos
    df_historico = df_prediccion[df_prediccion['Tipo'] == 'Histórico']
    fig_pred.add_trace(go.Scatter(
        x=df_historico['Fecha'],
        y=df_historico['Venta_Predicha'],
        mode='lines+markers',
        name='Ventas Históricas',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6)
    ))
    
    # Predicciones
    df_futuro = df_prediccion[df_prediccion['Tipo'] == 'Predicción']
    fig_pred.add_trace(go.Scatter(
        x=df_futuro['Fecha'],
        y=df_futuro['Venta_Predicha'],
        mode='lines+markers',
        name='Predicción',
        line=dict(color='#ff7f0e', width=2, dash='dash'),
        marker=dict(size=8, symbol='star')
    ))
    
    # Línea de tendencia
    fig_pred.add_trace(go.Scatter(
        x=df_prediccion['Fecha'],
        y=tendencia * (df_prediccion['Fecha'] - df_prediccion['Fecha'].min()).dt.days + intercepto,
        mode='lines',
        name='Tendencia Lineal',
        line=dict(color='red', width=1, dash='dot')
    ))
    
    fig_pred.update_layout(
        title="Proyección de Ventas con Tendencia",
        xaxis_title="Fecha",
        yaxis_title="Ventas ($)",
        hovermode='x unified',
        legend=dict(x=0.01, y=0.99),
        height=500
    )
    
    st.plotly_chart(fig_pred, use_container_width=True)
    
    # Tabla de predicciones
    with st.expander("📅 Ver Detalle de Predicciones"):
        tabla_predicciones = df_futuro[['Mes', 'Venta_Predicha']].copy()
        tabla_predicciones['Venta_Predicha'] = tabla_predicciones['Venta_Predicha'].apply(lambda x: f"${x:,.2f}")
        tabla_predicciones.columns = ['Mes', 'Venta Proyectada']
        st.dataframe(tabla_predicciones, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # GRÁFICOS INTERACTIVOS CON CROSS-FILTERING
    st.header("📊 Análisis Interactivo (Click para Filtrar)")
    
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.subheader("🎯 Ventas por Producto (Click para filtrar)")
        ventas_producto = df_filtrado.groupby('Producto')['Venta_Total'].sum().reset_index()
        ventas_producto = ventas_producto.sort_values('Venta_Total', ascending=False)
        
        fig2 = px.bar(
            ventas_producto,
            x='Producto',
            y='Venta_Total',
            color='Venta_Total',
            title="Ventas Totales por Producto",
            color_continuous_scale='Blues',
            hover_data={'Venta_Total': ':,.0f'}
        )
        fig2.update_layout(
            xaxis_title="Producto",
            yaxis_title="Ventas ($)",
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True, key="productos")
        
        # Selector de producto para cross-filter
        producto_click = st.selectbox(
            "🔍 Filtrar por producto:",
            ["Todos"] + ventas_producto['Producto'].tolist(),
            key="select_producto"
        )
        
        if producto_click != "Todos":
            if st.button("✅ Aplicar filtro producto"):
                st.session_state.filtro_producto = producto_click
                st.rerun()
    
    with row1_col2:
        st.subheader("🗺️ Ventas por Región (Click para filtrar)")
        ventas_region = df_filtrado.groupby('Region')['Venta_Total'].sum().reset_index()
        
        fig3 = px.pie(
            ventas_region,
            values='Venta_Total',
            names='Region',
            title="Distribución de Ventas por Región",
            hole=0.4
        )
        st.plotly_chart(fig3, use_container_width=True, key="regiones")
        
        # Selector de región para cross-filter
        region_click = st.selectbox(
            "🔍 Filtrar por región:",
            ["Todas"] + ventas_region['Region'].tolist(),
            key="select_region"
        )
        
        if region_click != "Todas":
            if st.button("✅ Aplicar filtro región"):
                st.session_state.filtro_region = region_click
                st.rerun()
    
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        st.subheader("💰 Evolución Mensual")
        ventas_mes = df_filtrado.groupby('Mes')['Venta_Total'].sum().reset_index()
        fig1 = px.line(
            ventas_mes,
            x='Mes',
            y='Venta_Total',
            markers=True,
            title="Evolución de Ventas Mensuales"
        )
        fig1.update_layout(
            xaxis_title="Mes",
            yaxis_title="Ventas ($)",
            hovermode='x unified'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with row2_col2:
        st.subheader("📦 Cantidad Vendida")
        cantidad_producto = df_filtrado.groupby('Producto')['Cantidad'].sum().reset_index()
        cantidad_producto = cantidad_producto.sort_values('Cantidad', ascending=True)
        fig4 = px.bar(
            cantidad_producto,
            x='Cantidad',
            y='Producto',
            orientation='h',
            title="Unidades Vendidas por Producto",
            color='Cantidad',
            color_continuous_scale='Viridis'
        )
        fig4.update_layout(
            xaxis_title="Unidades",
            yaxis_title="Producto"
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # HEATMAP
    st.subheader("🔥 Mapa de Calor: Ventas por Región y Producto")
    heatmap_data = df_filtrado.pivot_table(
        values='Venta_Total',
        index='Producto',
        columns='Region',
        aggfunc='sum',
        fill_value=0
    )
    
    fig5 = px.imshow(
        heatmap_data,
        labels=dict(x="Región", y="Producto", color="Ventas ($)"),
        title="Intensidad de Ventas",
        color_continuous_scale='RdYlGn',
        aspect="auto"
    )
    st.plotly_chart(fig5, use_container_width=True)
    
    # Análisis de día de la semana
    st.subheader("📅 Ventas por Día de la Semana")
    ventas_dia = df_filtrado.groupby('Dia_Semana')['Venta_Total'].sum().reset_index()
    orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ventas_dia['Dia_Semana'] = pd.Categorical(ventas_dia['Dia_Semana'], categories=orden_dias, ordered=True)
    ventas_dia = ventas_dia.sort_values('Dia_Semana')
    
    fig_dias = px.bar(
        ventas_dia,
        x='Dia_Semana',
        y='Venta_Total',
        title="Patrón de Ventas Semanal",
        color='Venta_Total',
        color_continuous_scale='Sunset'
    )
    st.plotly_chart(fig_dias, use_container_width=True)
    
    # TABLA DE DATOS
    st.markdown("---")
    st.subheader("📋 Explorador de Datos")
    
    # Opciones de visualización
    col1, col2 = st.columns([3, 1])
    
    with col1:
        num_registros = st.slider("Número de registros a mostrar:", 10, 100, 50)
    
    with col2:
        ordenar_por = st.selectbox("Ordenar por:", ['Fecha', 'Venta_Total', 'Producto'])
    
    df_display = df_filtrado.sort_values(ordenar_por, ascending=False).head(num_registros)
    st.dataframe(
        df_display,
        use_container_width=True,
        height=400
    )
    
    # ESTADÍSTICAS ADICIONALES
    st.markdown("---")
    st.subheader("📊 Estadísticas y Rankings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**🏆 Top 3 Productos**")
        top_productos = df_filtrado.groupby('Producto')['Venta_Total'].sum().nlargest(3)
        for i, (producto, venta) in enumerate(top_productos.items(), 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            st.write(f"{emoji} {producto}: ${venta:,.0f}")
    
    with col2:
        st.write("**🗺️ Top 3 Regiones**")
        top_regiones = df_filtrado.groupby('Region')['Venta_Total'].sum().nlargest(3)
        for i, (region, venta) in enumerate(top_regiones.items(), 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            st.write(f"{emoji} {region}: ${venta:,.0f}")
    
    with col3:
        st.write("**📈 Estadísticas**")
        st.write(f"• Media: ${df_filtrado['Venta_Total'].mean():.2f}")
        st.write(f"• Mediana: ${df_filtrado['Venta_Total'].median():.2f}")
        st.write(f"• Desv. Est: ${df_filtrado['Venta_Total'].std():.2f}")

# Footer
st.markdown("---")
st.markdown("*🚀 Dashboard Pro creado con Streamlit, Plotly y Machine Learning | Interactividad Total*")