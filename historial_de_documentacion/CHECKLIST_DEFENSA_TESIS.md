# ✅ CHECKLIST DEFENSA DE TESIS - PROYECTO SOP

---

## 📋 SLIDES ESENCIALES (8-10 diapositivas)

### 1. INTRODUCCIÓN
- ☐ Problema: SOP afecta 5-10% mujeres edad reproductiva
- ☐ Objetivo: Predecir SOP con ML usando 42 variables clínicas/hormonales

### 2. METODOLOGÍA
- ☐ Dataset: 538 pacientes (362 SOP, 176 No-SOP)
- ☐ Preprocesamiento: VIF + RFE (42 → 30 variables)
- ☐ Modelos: Random Forest, XGBoost, Logistic Regression, KNN
- ☐ Validación: Repeated 5-Fold CV × 3

### 3. RESULTADOS - MODELO GANADOR
**Random Forest (30 features)**
- ☐ F1-Score: 92.8% ± 2.5%
- ☐ Sensibilidad: 85.7%
- ☐ Especificidad: 95.9%
- ☐ LR+: 20.86 (diagnóstico definitivo)

### 4. VARIABLES MÁS IMPORTANTES (SHAP)
- ☐ Top 3: Num Folículos, Aumento Peso, Crecimiento Vello
- ☐ Coherencia con criterios Rotterdam ✅

### 5. VALIDACIÓN CLÍNICA
- ☐ Confusion Matrix (TP=30, TN=70, FP=3, FN=5)
- ☐ Gráfico SHAP beeswarm
- ☐ Curva ROC (AUC = 98.2%)

### 6. CONCLUSIONES
- ☐ Modelo robusto y clínicamente útil
- ☐ Reduce necesidad de pruebas invasivas
- ☐ Potencial para screening primario

---

## 💬 PREGUNTAS FRECUENTES DEL COMITÉ

### **¿Por qué Random Forest y no Regresión Logística?**
> "RF tiene mejor F1 (92.8% vs 90.7%) y captura interacciones no lineales. Logistic es más simple pero menos preciso en este dataset."

### **¿Cómo validaste el modelo?**
> "Validación cruzada repetida 5×3 (15 evaluaciones). F1 estable: 92.8% ± 2.5%. Demuestra robustez."

### **¿El modelo es interpretable?**
> "Sí. SHAP identifica top variables: Num Folículos (SHAP=1.73) coincide con criterio Rotterdam #1. Clínicamente coherente."

### **¿Por qué 30 features y no 42?**
> "RFE optimization. 30 features mantienen performance (F1=87%) con menos complejidad. Reducción sin pérdida."

### **¿Qué es LR+ = 20.86?**
> "Likelihood Ratio positivo. Si test positivo, probabilidad post-test sube a 95%. LR+ > 10 es diagnóstico definitivo."

### **¿Dataset balanceado?**
> "No (362 SOP vs 176 No-SOP). Usé SMOTE en train. Test mantiene proporción real para evaluar performance realista."

### **Limitaciones del estudio:**
> "1. Dataset moderado (n=538), 2. Validación externa pendiente, 3. Factores genéticos no incluidos."

---

## 📊 GRÁFICOS CLAVE PARA PROYECTAR

1. **SHAP Beeswarm (XGBoost)** - Muestra top 15 variables + dirección impacto
2. **Confusion Matrix** - Visual de TN/FP/FN/TP
3. **Validación Cruzada (barras con IC)** - Muestra robustez
4. **Comparación Modelos** - Tabla RF vs XGBoost vs LR vs KNN

---

## 🎯 MENSAJES CLAVE (30 segundos)

**Elevator Pitch:**
> "Desarrollé un modelo Random Forest para predecir SOP con 92.8% F1-Score usando 30 variables clínicas. El modelo identifica correctamente 86% de casos SOP con solo 4% falsos positivos. Validación rigurosa (5×3 CV) demuestra robustez. Las variables más importantes coinciden con criterios de Rotterdam, confirmando coherencia clínica."

---

## ✅ VERIFICACIÓN PRE-DEFENSA

- ☐ Domino interpretación de métricas (Sens/Spec/PPV/NPV/LR+)
- ☐ Puedo explicar SHAP en 1 minuto
- ☐ Sé justificar por qué RF ganó
- ☐ Conozco limitaciones del estudio
- ☐ Tengo backup de validación externa (futuro trabajo)
- ☐ Puedo explicar VIF y RFE en lenguaje simple

---

**Tiempo estimado defensa:** 15-20 min + 10 min preguntas  
**Confianza:** ALTA ✅ (proyecto robusto, bien validado)
