# 📊 Documentación - Notebook 01: Análisis Exploratorio

**Fecha:** 30 de octubre, 2025  
**Autor:** Análisis de datos PCOS  
**Dataset:** PCOS_data_1.xlsx

---

## 🎯 Objetivo del Notebook

Realizar análisis exploratorio de datos (EDA) del dataset de SOP y limpiar outliers críticos que representan errores de captura.

---

## 📥 Datos de Entrada

- **Archivo:** `PCOS_data_1.xlsx`
- **Tamaño:** 541 pacientes × 42 variables
- **Variable objetivo:** PCOS (Y/N)
  - No-SOP: 364 pacientes (67.3%)
  - SOP: 177 pacientes (32.7%)

---

## 🔬 Análisis Realizados

### 1. **Análisis de Valores Nulos**
- **Resultado:** 44 valores nulos encontrados (0.19% del total)
- **Variables afectadas:**
  - Fast food (Y/N): 15 nulos
  - Marr.Status (Yrs): 10 nulos
  - Pregnant(Y/N): 9 nulos
  - No. of aborptions: 1 nulo
  - AMH(ng/mL): 9 nulos

### 2. **Análisis de Distribuciones**
- Se generaron histogramas para todas las variables numéricas
- Se identificó que la mayoría de variables NO siguen distribución normal
- Variables clave analizadas: FSH, LH, TSH, AMH, BMI, etc.

### 3. **Detección de Outliers (Método IQR)**
- **Método:** Rango Intercuartílico (IQR = Q3 - Q1)
- **Criterio:** Valores fuera de [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
- **Resultado:**
  - 180 outliers extremos detectados
  - 150 filas afectadas (27.7% del dataset)

### 4. **Ranking de Variables con Más Outliers**

| Variable | # Outliers | Valor Máximo | Comentario |
|----------|-----------|--------------|------------|
| beta-HCG II (mIU/mL) | 25 | 6.00 | Extremos moderados |
| FSH/LH | 22 | 47.69 | Ratio muy alto |
| beta-HCG I (mIU/mL) | 21 | 9.00 | Múltiples extremos |
| PRL(ng/mL) | 20 | 45.14 | Outliers moderados |
| FSH(mIU/mL) | 19 | **5052.00** | ⚠️ ERROR CRÍTICO |
| LH(mIU/mL) | 16 | **2018.00** | ⚠️ ERROR CRÍTICO |
| TSH (mIU/L) | 16 | **65.00** | ⚠️ ERROR CRÍTICO |

---

## 🚨 Outliers Críticos Identificados

### Valores IMPOSIBLES (errores de captura):

1. **Fila 331** → FSH = 5052 mIU/mL
   - Valor normal: 3-10 mIU/mL
   - Este valor es **500x** el valor máximo normal
   - **Conclusión:** Error de captura de datos

2. **Fila 457** → LH = 2018 mIU/mL
   - Valor normal: 2-15 mIU/mL
   - Este valor es **200x** el valor máximo normal
   - **Conclusión:** Error de captura de datos

3. **Fila 39** → TSH = 65 mIU/L
   - Valor normal: 0.5-5 mIU/L
   - Este valor es **13x** el valor máximo normal
   - **Conclusión:** Posible error de captura

---

## 🔄 Estrategia de Limpieza Aplicada

### **ENFOQUE HÍBRIDO (3 pasos):**

#### **Paso 1: Eliminación de Outliers Críticos** ✅
- **Criterio:** Eliminar valores imposibles
  - FSH > 1000 mIU/mL
  - LH > 1000 mIU/mL
  - TSH > 50 mIU/L
- **Filas eliminadas:** 3 (0.6% del dataset)
- **Justificación:** Son errores evidentes de captura, no valores biológicos válidos

#### **Paso 2: Winsorización de Outliers Extremos** ⏳ (Notebook 02)
- **Método:** Reemplazar valores extremos con percentil 99
- **Variables a winsorizar:** FSH, LH, TSH, AMH, FSH/LH ratio
- **Justificación:** Conserva información clínica válida pero reduce distorsión en modelos

#### **Paso 3: Mantener Outliers Moderados** ✅
- Los outliers restantes representan casos clínicos reales
- Ejemplo: AMH alto en SOP severo es información diagnóstica valiosa
- **No se eliminan**

---

## 💾 Archivos Generados

### Datos Limpios:
- **`PCOS_data_clean.csv`** → 538 filas (eliminados 3 outliers críticos)

### Visualizaciones:
- **`outliers_boxplots.png`** → Boxplots comparativos SOP vs No-SOP

### Reportes:
- **`outliers_extremos_detalle.csv`** → Lista completa de los 180 outliers detectados

---

## 📈 Estadísticas Finales

| Métrica | Valor |
|---------|-------|
| **Pacientes originales** | 541 |
| **Outliers extremos detectados** | 180 |
| **Filas con outliers** | 150 (27.7%) |
| **Outliers críticos eliminados** | 3 |
| **Dataset final** | 538 filas |
| **Pérdida de datos** | 0.6% |

---

## 🎯 Próximos Pasos (Notebook 02)

1. **Imputación de valores nulos**
   - Fast food, Marr.Status, Pregnant, AMH
   - Métodos: Mediana/Moda según variable

2. **Winsorización de outliers extremos restantes**
   - FSH, LH, TSH, AMH, FSH/LH
   - Límites: Percentil 1 y 99

3. **Validación de normalidad**
   - Tests de Shapiro-Wilk
   - Decisión sobre transformaciones

---

## 💡 Decisiones Clave Tomadas

### ¿Por qué solo eliminar 3 outliers?
- La mayoría de outliers son **casos clínicos reales** (SOP severo)
- Solo eliminamos valores **biológicamente imposibles**
- Preservamos información diagnóstica valiosa

### ¿Por qué winsorizar en lugar de eliminar?
- **Conserva el tamaño del dataset** (importante con solo 541 pacientes)
- **Reduce distorsión** en estadísticas y modelos ML
- **Mantiene la estructura** de los datos

### ¿Cómo se identificaron los outliers críticos?
- **Conocimiento clínico:** Rangos normales de hormonas
- **Consulta con experto:** Mtro. Carlos Fregoso (biomédico)
- **Literatura médica:** Guías ESHRE 2023 para SOP

---

## 📚 Referencias

- **Guías ESHRE 2023** para diagnóstico de SOP
- **Método IQR** (Tukey, 1977) para detección de outliers
- **Winsorización** para tratamiento de outliers en datasets pequeños

---

## ✅ Checklist de Calidad

- [x] Dataset cargado correctamente (541 filas)
- [x] Análisis de valores nulos completado
- [x] Distribuciones visualizadas
- [x] Outliers detectados sistemáticamente (IQR)
- [x] Outliers críticos identificados (3 casos)
- [x] Limpieza de datos ejecutada
- [x] Dataset limpio guardado (538 filas)
- [x] Visualizaciones generadas
- [x] Archivos documentados

---

**Notebook completado con éxito** ✅
