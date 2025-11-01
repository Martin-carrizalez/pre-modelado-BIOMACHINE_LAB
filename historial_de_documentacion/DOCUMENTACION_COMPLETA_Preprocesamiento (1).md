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
| **Variables winsorizadas** | 4 |
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

PASO 4: Winsorización ✅
├─ Variables winsorizadas: 4
├─ Reducción de valores extremos: -83.5% promedio
└─ Resultado: 538 filas sin valores absurdos

PASO 5: Análisis Estadístico ⏳ SIGUIENTE
PASO 6: Feature Engineering ⏳ PENDIENTE
PASO 7: Preparación para Modelado ⏳ PENDIENTE
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

# 🔄 PASO 4: WINSORIZACIÓN DE OUTLIERS MODERADOS

## 🎯 Objetivo

Reducir el impacto de valores extremos en modelos de ML sin eliminar datos valiosos.

## 📊 Identificación de Variables para Winsorizar

**Criterio:** Variables con >5% de outliers detectados (método IQR)

### Análisis Completo de Outliers

| Variable | # Outliers | % Outliers | Max Actual | P99 | Acción |
|----------|-----------|------------|------------|-----|--------|
| II beta-HCG(mIU/mL) | 79 | 14.7% | 25,000.00 | 3,692.20 | ✅ WINSORIZAR |
| AMH(ng/mL) | 52 | 9.7% | 66.00 | 24.77 | ✅ WINSORIZAR |
| FSH/LH | 47 | 8.7% | 327.00 | 29.40 | ✅ WINSORIZAR |
| Vit D3 (ng/mL) | 31 | 5.8% | 6,014.66 | 73.03 | ✅ WINSORIZAR |
| TSH (mIU/L) | 26 | 4.8% | 25.91 | 16.26 | ⏸️ Mantener |
| LH(mIU/mL) | 23 | 4.3% | 14.69 | 10.31 | ⏸️ Mantener |
| PRL(ng/mL) | 21 | 3.9% | 128.24 | 95.02 | ⏸️ Mantener |
| Weight (Kg) | 18 | 3.3% | 108.00 | 89.00 | ⏸️ Mantener |

**Resultado:** 4 variables seleccionadas para winsorización

## 🔧 Aplicación de Winsorización

**Método:** Winsorización bilateral con límites 1% y 99%

### Transformaciones Realizadas

#### 1. II beta-HCG(mIU/mL)
```
Antes:  Max = 25,000.00 mIU/mL
Después: Max = 3,893.06 mIU/mL
Reducción: -84.4%

Interpretación clínica:
- Valor original biológicamente inverosímil
- P99 más consistente con casos de embarazo ectópico
- Preserva información clínica relevante
```

#### 2. AMH(ng/mL)
```
Antes:  Max = 66.00 ng/mL
Después: Max = 26.40 ng/mL
Reducción: -60.0%

Interpretación clínica:
- AMH extremadamente elevado en casos de SOP severo
- P99 representa casos clínicos reales pero graves
- Valor 66 probablemente error de medición
```

#### 3. FSH/LH
```
Antes:  Max = 327.00
Después: Max = 29.73
Reducción: -90.9%

Interpretación clínica:
- Ratio normal: 1-2 (SOP invierte a 2-3)
- Ratio 327 matemáticamente imposible
- P99 representa casos extremos pero válidos
```

#### 4. Vit D3 (ng/mL)
```
Antes:  Max = 6,014.66 ng/mL
Después: Max = 74.50 ng/mL
Reducción: -98.8%

Interpretación clínica:
- Rango normal: 20-50 ng/mL
- Valor 6,014 claramente erróneo
- P99 representa suplementación agresiva
```

## 📊 Resultados de la Winsorización

### Impacto Global

| Métrica | Valor |
|---------|-------|
| **Variables winsorizadas** | 4 |
| **Filas afectadas** | 209 (38.8%) |
| **Reducción promedio de máximos** | -83.5% |
| **Datos preservados** | 538 filas (100%) |

### Cambios en Estadísticas Descriptivas

| Variable | Mean Antes | Mean Después | Cambio |
|----------|-----------|--------------|--------|
| II beta-HCG | 142.45 | 134.82 | -5.4% |
| AMH | 5.89 | 5.67 | -3.7% |
| FSH/LH | 2.87 | 2.45 | -14.6% |
| Vit D3 | 39.82 | 31.24 | -21.6% |

## 🤔 ¿Por qué los Outliers IQR Solo Bajaron 0.5%?

**Pregunta válida:** Si winsorizamos exitosamente, ¿por qué los outliers según IQR solo bajaron de 209 a 208?

### Explicación

El método IQR detecta outliers de forma **relativa**, no absoluta:

```python
# Ejemplo con AMH
Antes de winsorizar:
├─ Datos: [1, 2, 3, ..., 20, 25, 30, 66]
├─ Q1 = 2.5, Q3 = 15, IQR = 12.5
├─ Límite superior = 15 + 1.5×12.5 = 33.75
└─ Outliers: 66 (muy extremo)

Después de winsorizar:
├─ Datos: [1, 2, 3, ..., 20, 25, 26.4, 26.4]  ← 66 → 26.4
├─ Q1 = 2.6, Q3 = 16, IQR = 13.4
├─ Límite superior = 16 + 1.5×13.4 = 36.1
└─ Outliers: Ninguno en este rango
PERO si la distribución sigue sesgada, puede seguir habiendo outliers
```

**Lo importante:**
- ✅ Los valores **extremos absurdos** fueron eliminados (66→26.4)
- ✅ El **impacto en modelos ML** se redujo drásticamente
- ⚠️ Algunos valores pueden seguir siendo "outliers" según IQR, pero ya no son problemáticos

## 📈 Impacto Esperado en Modelos ML

### Antes de Winsorización
```python
Problema: Valores extremos dominan el aprendizaje
├─ beta-HCG = 25,000 → Modelo aprende patrones erróneos
├─ FSH/LH = 327 → Distorsiona decisiones del árbol
└─ Vit D3 = 6,014 → Sesga predicciones
```

### Después de Winsorización
```python
Solución: Valores representativos de casos reales
├─ beta-HCG = 3,893 → Modelo aprende casos graves válidos
├─ FSH/LH = 29.7 → Decisiones más robustas
└─ Vit D3 = 74.5 → Predicciones más confiables
```

## 💾 Archivos Generados

### Dataset Final
**`PCOS_data_winsorized.csv`**
- 538 filas × 42 columnas
- Sin outliers críticos
- Sin valores nulos
- Sin valores extremos absurdos
- **Listo para análisis estadístico**

### Log Detallado
**`winsorization_log.csv`**
- Estadísticas antes/después por variable
- Mean, Std, Max, Min
- Conteo de outliers IQR
- Porcentaje de reducción

### Visualización
**`winsorization_impact.png`**
- Boxplots comparativos antes/después
- Top 6 variables más afectadas
- Outliers marcados en rojo

## 📝 Justificación de la Estrategia

### ¿Por qué no eliminar outliers en lugar de winsorizar?

| Criterio | Eliminar | Winsorizar |
|----------|----------|------------|
| **Pérdida de datos** | 38.8% (209 filas) | 0% |
| **Tamaño final** | 329 filas | 538 filas |
| **Poder estadístico** | ⚠️ Bajo | ✅ Alto |
| **Información clínica** | ❌ Perdida | ✅ Preservada |
| **Validez del modelo** | ⚠️ Riesgo de overfitting | ✅ Más robusto |

### ¿Por qué percentil 99 y no 95?

```
P95: Más agresivo, elimina 5% superior
├─ Pro: Reduce más la varianza
└─ Contra: Puede eliminar casos clínicos válidos graves

P99: Más conservador, elimina 1% superior
├─ Pro: Preserva casos graves pero reales
└─ Contra: Mantiene más variabilidad

Decisión: P99 (conservador)
Justificación: Con solo 538 pacientes, cada caso cuenta
```

---

# 📈 ESTADÍSTICAS FINALES DEL PREPROCESAMIENTO

## Comparativa: Original → Limpio

| Métrica | Original | Limpio | Cambio |
|---------|----------|--------|--------|
| **Filas** | 541 | 538 | -3 (-0.6%) |
| **Columnas** | 42 | 42 | 0 |
| **Valores nulos** | 3 | 0 | -3 (-100%) |
| **Outliers críticos** | 3 | 0 | -3 (-100%) |
| **Valores extremos absurdos** | 4 | 0 | -4 (-100%) |
| **Outliers moderados preservados** | ~173 | ~173 | 0 |
| **No-SOP** | 364 | 362 | -2 |
| **SOP** | 177 | 176 | -1 |
| **Ratio desbalance** | 1:2.06 | 1:2.06 | Sin cambio |

## ✅ Calidad del Dataset Limpio

```
✅ Sin errores de captura
✅ Sin valores nulos
✅ Sin outliers biológicamente imposibles
✅ Sin valores extremos absurdos (winsorización aplicada)
✅ Outliers clínicos válidos preservados
✅ Distribución de clases intacta
✅ 99.4% de los datos originales preservados
✅ Estadísticas robustas (reducción -83.5% en valores extremos)
```

---

# 🎯 PRÓXIMOS PASOS

## PASO 4: Winsorización ✅ COMPLETADO

**Objetivo:** Reducir impacto de outliers extremos sin eliminar datos

**Método:** Reemplazo con percentil 1 y 99 (límites bilateral)

**Criterio de selección:** Variables con >5% de outliers detectados (método IQR)

### Variables Winsorizadas

| Variable | Outliers (%) | Max Antes | Max Después | Reducción |
|----------|--------------|-----------|-------------|-----------|
| **II beta-HCG(mIU/mL)** | 14.7% | 25,000.00 | 3,893.06 | -84.4% |
| **AMH(ng/mL)** | 9.7% | 66.00 | 26.40 | -60.0% |
| **FSH/LH** | 8.7% | 327.00 | 29.73 | -90.9% |
| **Vit D3 (ng/mL)** | 5.8% | 6,014.66 | 74.50 | -98.8% |

### Resultados

```
Variables winsorizadas: 4
Valores extremos eliminados: 100%
Datos preservados: 538 filas (100%)
Reducción promedio de máximos: -83.5%
```

### ¿Por qué la reducción de outliers IQR fue mínima (0.5%)?

**Respuesta:** El método IQR detecta outliers de forma relativa, no absoluta.

```
Ejemplo con AMH:
├─ Antes: Max = 66.00 ng/mL (valor extremo absurdo)
├─ Después: Max = 26.40 ng/mL (P99)
├─ IQR recalculado: 26.40 SIGUE siendo outlier según IQR
└─ PERO: Impacto en modelos ML es mucho menor (66→26.4)
```

**Lo importante:** Los valores extremos fueron reducidos dramáticamente (-84% promedio), aunque técnicamente sigan siendo "outliers" según el criterio IQR. La winsorización cumplió su objetivo: reducir distorsión sin eliminar datos.

### Justificación

- ✅ Conserva 100% de los datos (538 filas)
- ✅ Reduce distorsión en estadísticas y modelos ML
- ✅ Percentil 99 es conservador (mantiene 98% de distribución original)
- ✅ Valores extremos reducidos en promedio 83.5%
- ✅ No elimina información clínica valiosa

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
│  ├─ PCOS_data_clean.csv       [Sin outliers críticos - 538 filas]
│  └─ PCOS_data_imputed.csv     [Sin nulos - 538 filas]
│
└─ processed/
   └─ PCOS_data_winsorized.csv  [Dataset final limpio - 538 filas]

visualizations/
├─ outliers_boxplots.png        [Boxplots comparativos SOP vs No-SOP]
└─ winsorization_impact.png     [Antes/después de winsorización]

reports/
├─ outliers_extremos_detalle.csv [Lista de 180 outliers detectados]
└─ winsorization_log.csv         [Log detallado de cambios por variable]
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
- [x] Outliers extremos winsorizados (4 variables)
- [x] Dataset limpio guardado
- [x] Sin pérdida significativa de datos (<1%)
- [x] Distribución de clases preservada

## Documentación
- [x] Archivos CSV generados
- [x] Visualizaciones guardadas
- [x] Decisiones justificadas
- [x] Código reproducible
- [x] Documentación completa
- [x] Logs detallados de transformaciones

---

**Estado del proyecto:** PASO 4/7 COMPLETADO ✅

**Próximo paso:** Análisis estadístico completo (normalidad, pruebas de hipótesis, correlaciones)

**Última actualización:** 31 de octubre, 2025
