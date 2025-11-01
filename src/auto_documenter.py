# src/auto_documenter.py
"""
Sistema de Documentación Automática Multi-Notebook
Uso: from src.auto_documenter import doc
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

class ProjectDocumenter:
    """Documentador centralizado para múltiples notebooks"""
    
    _instance = None  # Singleton pattern
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, project_name="PCOS-ML-Analysis", docs_dir="docs"):
        # Solo inicializar una vez
        if hasattr(self, '_initialized'):
            return
        
        self.project_name = project_name
        self.docs_dir = docs_dir
        self.doc_file = os.path.join(docs_dir, f"{project_name}_DOCUMENTATION.md")
        self.current_notebook = None
        self.session_start = datetime.now()
        
        # Crear carpeta docs si no existe
        os.makedirs(docs_dir, exist_ok=True)
        
        # Cargar o crear documentación
        if os.path.exists(self.doc_file):
            with open(self.doc_file, 'r', encoding='utf-8') as f:
                self.content = f.read()
        else:
            self.content = self._create_header()
            self._save_to_file()
        
        self._initialized = True
    
    def _create_header(self):
        """Crear encabezado del documento"""
        return f"""# 📊 Documentación Técnica: {self.project_name}

**Proyecto:** Análisis y Modelado ML para Síndrome de Ovario Poliquístico (SOP)  
**Dataset:** 541 pacientes, 42 variables  
**Objetivo:** Predicción de SOP, clustering de fenotipos, sistema de severidad  
**Fecha Inicio:** {self.session_start.strftime('%Y-%m-%d')}

---

## 📋 Índice de Notebooks

1. [Análisis Exploratorio](#notebook-1-análisis-exploratorio)
2. [Imputación de Valores](#notebook-2-imputación-de-valores)
3. [Limpieza de Outliers](#notebook-3-limpieza-de-outliers)
4. [Análisis Estadístico](#notebook-4-análisis-estadístico)
5. [Feature Engineering](#notebook-5-feature-engineering)
6. [Modelado ML](#notebook-6-modelado-ml)

---

"""
    
    def set_notebook(self, notebook_name, notebook_number):
        """
        Configurar notebook actual
        
        Args:
            notebook_name: Nombre descriptivo del notebook
            notebook_number: Número del notebook (01, 02, etc.)
        """
        self.current_notebook = notebook_name
        self.notebook_number = notebook_number
        self.notebook_steps = []
        
        # Añadir encabezado del notebook si no existe
        notebook_header = f"\n\n---\n\n# Notebook {notebook_number}: {notebook_name}\n\n"
        notebook_header += f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        if notebook_header not in self.content:
            self.content += notebook_header
            self._save_to_file()
        
        print(f"\n{'='*80}")
        print(f"📓 NOTEBOOK ACTIVO: {notebook_number} - {notebook_name}")
        print(f"📝 Documentación: {self.doc_file}")
        print(f"{'='*80}\n")
        
        return self
    
    def log_step(self, title, description=None, code=None, results=None, 
                 justification=None, decision=None, notes=None):
        """Registrar paso del análisis"""
        
        if not self.current_notebook:
            print("⚠️  Advertencia: Configura el notebook primero con doc.set_notebook()")
            return self
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Construir documentación
        step_doc = f"\n### {title}\n"
        step_doc += f"⏰ {timestamp}\n\n"
        
        if description:
            step_doc += f"**Descripción:**  \n{description}\n\n"
        
        if justification:
            step_doc += f"**🔬 Justificación:**  \n{justification}\n\n"
        
        if decision:
            step_doc += f"**✅ Decisión:**  \n{decision}\n\n"
        
        if code:
            # Limpiar código (quitar indentación extra)
            code = code.strip()
            step_doc += f"**💻 Código:**\n```python\n{code}\n```\n\n"
        
        if results:
            step_doc += f"**📊 Resultados:**  \n{results}\n\n"
        
        if notes:
            step_doc += f"**📌 Notas:**  \n{notes}\n\n"
        
        # Añadir al contenido
        self.content += step_doc
        self.notebook_steps.append(title)
        
        # Auto-guardar
        self._save_to_file()
        
        print(f"✅ Documentado: {title}")
        return self
    
    def _save_to_file(self):
        """Guardar a archivo"""
        with open(self.doc_file, 'w', encoding='utf-8') as f:
            f.write(self.content)
    
    def save(self):
        """Guardar explícitamente (para compatibilidad)"""
        self._save_to_file()
        print(f"💾 Documentación guardada: {self.doc_file}")
        return self
    
    def summary(self):
        """Resumen del notebook actual"""
        if not self.current_notebook:
            print("⚠️  No hay notebook activo")
            return self
        
        print(f"\n{'='*80}")
        print(f"📊 RESUMEN: {self.current_notebook}")
        print(f"{'='*80}")
        print(f"📝 Pasos documentados: {len(self.notebook_steps)}")
        if self.notebook_steps:
            for i, step in enumerate(self.notebook_steps, 1):
                print(f"   {i}. {step}")
        print(f"📁 Archivo: {self.doc_file}")
        print(f"{'='*80}\n")
        return self
    
    def quick(self, title, desc):
        """Atajo para logging rápido"""
        return self.log_step(title=title, description=desc)

# Crear instancia global (Singleton)
doc = ProjectDocumenter()