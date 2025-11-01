# 📊 Documentación Completa - Preprocesamiento de Datos PCOS

**Proyecto:** Análisis y Predicción de Síndrome de Ovario Poliquístico (SOP)  
**Dataset:** PCOS_data_1.xlsx  
**Fecha:** 30-31 de octubre, 2025

---

## 📋 RESUMEN EJECUTIVO

| Métrica | Valor |
|---------|-------|
| **Pacientes originales** | 541 |
| **Outliers críticos eliminados** | 3 (0.6%) |
| **Valores nulos imputados** | 3 (0.6%) |
| **Dataset final limpio** | 538 pacientes |
| **Pérdida total de datos** | 0.6% |

---

## 🔄 PIPELINE DE PREPROCESAMIENTO COMPLETADO

```
PASO 1: Análisis Exploratorio ✅
├─ Carga de datos: 541 filas × 42 columnas
├─ Detección de nulos: 3 valores (0.55%)
├─ Detección de outliers: 180 extremos en 150 filas
└─ Identificación de errores críticos: 3 filas

PASO 2: Limpieza de Outliers Críticos ✅
├─ Eliminadas: 3 filas con errores de captura
└─ Resultado: 538 filas

PASO 3: Imputación de Valores Nulos ✅
├─ Imputados: 3 valores
└─ Resultado: 538 filas sin nulos

PASO 4: Winsorización ⏳ PENDIENTE
PASO 5: Análisis Estadístico ⏳ PENDIENTE
```

---

# 📊 PASO 1: ANÁLISIS EXPLORATORIO DE DATOS

## 🎯 Objetivo
Identificar problemas de calidad en el dataset: valores nulos, outliers, errores de captura.

## 📥 Dataset Original

**Archivo:** `PCOS_data_1.xlsx`

| Característica | Valor |
|----------------|-------|
| **Filas** | 541 pacientes |
| **Columnas** | 42 variables |
| **Variable objetivo** | PCOS (Y/N) |
| **Distribución** | No-SOP: 364 (67.3%) / SOP: 177 (32.7%) |
| **Desbalance** | Ratio 1:2.06 (moderado) |

## 🔍 Análisis de Valores Nulos

**Total detectado:** 3 valores nulos (0.55% del dataset)

| Variable | Nulos | % del Total |
|----------|-------|-------------|
| Marraige Status (Yrs) | 1 | 0.19% |
| AMH(ng/mL) | 1 | 0.19% |
| Fast food (Y/N) | 1 | 0.19% |

**Conclusión:** Impacto mínimo, dataset de alta calidad.

## 📊 Detección de Outliers

### Método Utilizado: IQR (Rango Intercuartílico)
- **Criterio:** Valores fuera de [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
- **Resultado:** 180 outliers extremos en 150 filas (27.7%)

### Ranking de Variables con Más Outliers

| Variable | # Outliers | Valor Máximo | Tipo |
|----------|-----------|--------------|------|
| beta-HCG II (mIU/mL) | 25 | 6.00 | Moderado |
| FSH/LH | 22 | 47.69 | Moderado |
| beta-HCG I (mIU/mL) | 21 | 9.00 | Moderado |
| PRL(ng/mL) | 20 | 45.14 | Moderado |
| **FSH(mIU/mL)** | 19 | **5052.00** | 🚨 CRÍTICO |
| **LH(mIU/mL)** | 16 | **2018.00** | 🚨 CRÍTICO |
| **TSH (mIU/L)** | 16 | **65.00** | 🚨 CRÍTICO |

---

# 🚨 PASO 2: ELIMINACIÓN DE OUTLIERS CRÍTICOS

## ⚠️ Valores Biológicamente Imposibles Detectados

### 1. Fila 331 (Excel: 332)
```
FSH = 5052 mIU/mL
├─ Rango normal: 3-10 mIU/mL
├─ Desviación: 500x el máximo normal
└─ Diagnóstico: Error de captura de datos
```

### 2. Fila 457 (Excel: 458)
```
LH = 2018 mIU/mL
├─ Rango normal: 2-15 mIU/mL
├─ Desviación: 200x el máximo normal
└─ Diagnóstico: Error de captura de datos
```

### 3. Fila 39 (Excel: 40)
```
TSH = 65 mIU/L
├─ Rango normal: 0.5-5 mIU/L
├─ Desviación: 13x el máximo normal
└─ Diagnóstico: Posible error de captura
```

## 🔧 Acción Tomada

```python
# Criterios de eliminación
- FSH > 1000 mIU/mL → ELIMINAR
- LH > 1000 mIU/mL → ELIMINAR
- TSH > 50 mIU/L → ELIMINAR

# Resultado
Filas eliminadas: 3
Filas restantes: 538
Pérdida de datos: 0.6%
```

## 📝 Justificación

**¿Por qué eliminar solo estos 3 outliers?**

1. **Valores biológicamente imposibles** → No son casos clínicos reales
2. **Magnitud extrema** → 100-500x por encima del rango normal
3. **Consenso médico** → Confirmado por experto biomédico (Mtro. Carlos Fregoso)
4. **Preservación de datos** → Los demás outliers representan casos clínicos válidos (SOP severo, resistencia insulínica, etc.)

## 💾 Archivo Generado

**`PCOS_data_clean.csv`**
- 538 filas × 42 columnas
- Sin outliers críticos
- Con 3 valores nulos pendientes

---

# 🔧 PASO 3: IMPUTACIÓN DE VALORES NULOS

## 🎯 Estrategia de Imputación

**Método:** Mediana estratificada por grupo PCOS

**Justificación:**
- Solo 3 valores nulos (0.56% del dataset) → Impacto mínimo
- Mediana por grupo preserva diferencias entre SOP vs No-SOP
- Mediana es robusta a outliers restantes

## 📊 Imputaciones Realizadas

### 1. Marraige Status (Yrs)
```
Variable numérica continua
├─ Nulos: 1
├─ Mediana No-SOP: 7.00 años
├─ Mediana SOP: 6.00 años
└─ Valor imputado: Según grupo PCOS del paciente
```

### 2. AMH(ng/mL)
```
Variable numérica continua (biomarcador clave)
├─ Nulos: 1
├─ Mediana No-SOP: 3.20 ng/mL
├─ Mediana SOP: 5.83 ng/mL
└─ Valor imputado: Según grupo PCOS del paciente

Nota: AMH elevado es característica distintiva del SOP
```

### 3. Fast food (Y/N)
```
Variable binaria (0=No, 1=Sí)
├─ Nulos: 1
├─ Mediana No-SOP: 0.00 (No consume)
├─ Mediana SOP: 1.00 (Sí consume)
└─ Valor imputado: Según grupo PCOS del paciente

Nota: Consumo de comida rápida correlaciona con SOP
```

## ✅ Resultado

```
Valores nulos antes: 3
Valores nulos después: 0
Método: Mediana estratificada por grupo PCOS
```

## 💾 Archivo Generado

**`PCOS_data_imputed.csv`**
- 538 filas × 42 columnas
- Sin outliers críticos
- Sin valores nulos
- Listo para winsorización

---

# 📈 ESTADÍSTICAS FINALES DEL PREPROCESAMIENTO

## Comparativa: Original → Limpio

| Métrica | Original | Limpio | Cambio |
|---------|----------|--------|--------|
| **Filas** | 541 | 538 | -3 (-0.6%) |
| **Columnas** | 42 | 42 | 0 |
| **Valores nulos** | 3 | 0 | -3 (-100%) |
| **Outliers críticos** | 3 | 0 | -3 (-100%) |
| **Outliers moderados** | 177 | 177 | 0 (preservados) |
| **No-SOP** | 364 | 362 | -2 |
| **SOP** | 177 | 176 | -1 |
| **Ratio desbalance** | 1:2.06 | 1:2.06 | Sin cambio |

## ✅ Calidad del Dataset Limpio

```
✅ Sin errores de captura
✅ Sin valores nulos
✅ Sin outliers biológicamente imposibles
✅ Outliers clínicos válidos preservados
✅ Distribución de clases intacta
✅ 99.4% de los datos originales preservados
```

---

# 🎯 PRÓXIMOS PASOS

## PASO 4: Winsorización (Pendiente)

**Objetivo:** Reducir impacto de outliers extremos sin eliminar datos

**Variables a winsorizar:**
- FSH(mIU/mL)
- LH(mIU/mL)
- TSH (mIU/L)
- AMH(ng/mL)
- FSH/LH ratio
- PRL(ng/mL)

**Método:** Reemplazo con percentil 99

**Justificación:**
- Conserva 100% de los datos
- Reduce distorsión en estadísticas
- Percentil 99 es conservador
- No elimina información clínica valiosa

## PASO 5: Análisis Estadístico (Pendiente)

1. Estadística descriptiva por grupo
2. Pruebas de normalidad (Shapiro-Wilk)
3. Pruebas de hipótesis (t-test / Mann-Whitney)
4. Análisis de correlaciones
5. Multicolinealidad (VIF)

## PASO 6: Feature Engineering (Pendiente)

1. Creación de ratios hormonales adicionales
2. Categorización de variables continuas
3. Interacciones entre variables
4. Selección de features (RFE, importancia)

## PASO 7: Preparación para Modelado (Pendiente)

1. Encoding de variables categóricas
2. Normalización/Estandarización
3. Train/Test split (80/20)
4. SMOTE en train set (solo al final)

---

# 📁 ARCHIVOS GENERADOS

```
data/
├─ raw/
│  └─ PCOS_data_1.xlsx          [ORIGINAL - 541 filas]
│
├─ interim/
│  └─ PCOS_data_clean.csv       [Sin outliers críticos - 538 filas]
│
└─ processed/
   └─ PCOS_data_imputed.csv     [Sin nulos - 538 filas]

visualizations/
└─ outliers_boxplots.png        [Boxplots comparativos SOP vs No-SOP]

reports/
└─ outliers_extremos_detalle.csv [Lista de 180 outliers detectados]
```

---

# 💡 DECISIONES CLAVE Y JUSTIFICACIONES

## ¿Por qué eliminar solo 3 outliers de 180 detectados?

**Respuesta:** Porque 177 outliers son casos clínicos reales:

| Tipo de Outlier | Cantidad | Decisión | Justificación |
|-----------------|----------|----------|---------------|
| **Críticos** | 3 | ❌ ELIMINAR | Errores de captura (FSH=5052, LH=2018, TSH=65) |
| **Extremos** | ~20 | 🔄 WINSORIZAR | Valores altos pero posibles (percentil 99) |
| **Moderados** | ~157 | ✅ MANTENER | Casos clínicos válidos (SOP severo, resistencia insulínica) |

## ¿Por qué imputar con mediana y no con media?

**Respuesta:** Robustez a outliers

```
Media: Sensible a outliers restantes
Mediana: Resistente a outliers, más representativa
```

## ¿Por qué imputar por grupo PCOS?

**Respuesta:** Preservar diferencias clínicas

```
Ejemplo AMH:
- No-SOP: Mediana 3.20 ng/mL (normal)
- SOP: Mediana 5.83 ng/mL (elevado)

Si usáramos mediana global, perderíamos esta diferencia diagnóstica.
```

---

# 📚 REFERENCIAS CLÍNICAS

## Rangos Normales de Biomarcadores

| Biomarcador | Rango Normal | Unidad | Fuente |
|-------------|--------------|--------|--------|
| FSH | 3-10 | mIU/mL | ESHRE 2023 |
| LH | 2-15 | mIU/mL | ESHRE 2023 |
| TSH | 0.5-5 | mIU/L | ATA 2023 |
| AMH | 1.0-5.0 | ng/mL | ASRM 2023 |

## Guías Utilizadas

- **ESHRE 2023** - Guías internacionales para diagnóstico de SOP
- **ATA 2023** - American Thyroid Association guidelines
- **ASRM 2023** - American Society for Reproductive Medicine

## Consultas con Expertos

- **Mtro. Carlos Fregoso** - Químico Farmacobiólogo
  - Validación de rangos biológicos
  - Confirmación de outliers críticos
  - Asesoría en interpretación clínica

---

# ✅ CHECKLIST DE VALIDACIÓN

## Análisis Exploratorio
- [x] Dataset cargado correctamente (541 → 538 filas)
- [x] Tipos de datos verificados (42 variables)
- [x] Valores nulos identificados (3)
- [x] Distribuciones visualizadas
- [x] Outliers detectados sistemáticamente (IQR)
- [x] Outliers críticos identificados (3)

## Limpieza de Datos
- [x] Outliers críticos eliminados (3 filas)
- [x] Valores nulos imputados (3 valores)
- [x] Dataset limpio guardado
- [x] Sin pérdida significativa de datos (<1%)
- [x] Distribución de clases preservada

## Documentación
- [x] Archivos CSV generados
- [x] Visualizaciones guardadas
- [x] Decisiones justificadas
- [x] Código reproducible
- [x] Documentación completa

---

**Estado del proyecto:** PASO 3/7 COMPLETADO ✅

**Próximo paso:** Winsorización de outliers moderados

**Última actualización:** 31 de octubre, 2025
