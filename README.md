# RECETARIO
API para Recetario Inteligente con planificador semanal y lista de compras. Stack: FastAPI, SQLAlchemy (Async), Pandas, Matplotlib y React.

# Recetario Inteligente (API)

Este repositorio contiene el backend de un **Recetario Inteligente**, una aplicación full-stack diseñada para la gestión de recetas, planificación de comidas y visualización de datos.

El proyecto va más allá de un simple CRUD, ya que sus características principales incluyen un **planificador semanal** que calcula una **lista de compras** (usando Pandas) y un módulo de **estadísticas** que genera gráficos (usando Matplotlib).

## 🚀 Características Principales

* **Autenticación de Usuarios:** Sistema de registro y login con tokens JWT.
* **Gestión de Recetas (CRUD):** Creación, lectura, actualización y eliminación de recetas (protegido por usuario).
* **Gestión de Ingredientes:** CRUD para los ingredientes base.
* **Planificador Semanal:** Permite a los usuarios asignar recetas a un día específico y tipo de comida.
* **Lista de Compras Inteligente:** Un endpoint que analiza el plan semanal del usuario (usando **Pandas**), agrupa los ingredientes y devuelve una lista de compras consolidada.
* **Visualización de Estadísticas:** Endpoints que analizan datos (ej. ingredientes más populares) y generan visualizaciones de datos directamente desde el backend usando **Matplotlib**.

## 🛠️ Stack Tecnológico (Backend)

* **Framework:** **FastAPI** (para endpoints asíncronos y síncronos).
* **Base de Datos:** **MySQL** (conectado vía **SQLAlchemy**).
* **Programación Asíncrona:** Uso de `AsyncSession` y `aiomysql` para operaciones de alto rendimiento.
* **Procesamiento de Datos:** **Pandas** para el análisis de la lista de compras.
* **Visualización de Datos:** **Matplotlib** para la generación de gráficos de estadísticas.
* **Validación de Datos:** **Pydantic** para los esquemas de entrada y salida.
