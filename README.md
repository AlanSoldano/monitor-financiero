# Monitor Financiero Personal

---

## Descripción

Aplicación desarrollada en Python utilizando Streamlit para el análisis y visualización automática de gastos mensuales a partir de archivos Excel.

El proyecto permite procesar datos financieros, generar resúmenes mensuales y visualizar información por categorías y evolución temporal de manera estructurada.

---

## Funcionalidades

- Carga de archivo Excel con movimientos financieros  
- Limpieza y transformación de datos  
- Resumen mensual de ingresos y gastos  
- Análisis por categorías  
- Evolución temporal de gastos  
- Sistema básico de alertas  
- Exportación de reportes  

---

## Tecnologías utilizadas

- Python  
- Streamlit  
- Pandas  
- Matplotlib  
- OpenPyXL  

---

## Estructura del proyecto

monitor-financiero/
│
├── app.py  
├── loaders/  
├── processing/  
├── visualization/  
├── exports/  
├── config.py  
├── requirements.txt  
└── README.md  

El proyecto está organizado de forma modular para separar responsabilidades:

- loaders/ → carga de datos  
- processing/ → lógica de análisis  
- visualization/ → generación de gráficos  
- exports/ → generación de reportes  

---

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```git clone https://github.com/AlanSoldano/monitor-financiero.git```
```cd monitor-financiero```

### 2. Crear entorno virtual

```python -m venv venv```

Activar entorno visual:
```venv\Scripts\activate```

### 3. Instalar dependencias
```pip install -r requirements.txt```

### 4. Ejecutar la aplicación

```streamlit run app.py```

---

### Objetivo del proyecto:

Este proyecto fue desarrollado para fortalecer habilidades en:
Manipulación y análisis de datos con Pandas
Organización modular de proyectos en Python
Visualización de datos
Desarrollo de aplicaciones interactivas

---

### Posibles mejoras futuras:

Soporte para múltiples archivos
Persistencia en base de datos
Métricas comparativas avanzadas
Optimización del sistema de alertas
