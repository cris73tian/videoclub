# TP Programación Avanzada - Grupo 9 🎬
## Sistema Integrador de Alquiler de Videojuegos y Películas

Este proyecto implementa un sistema digital completo para la gestión y administración de un videoclub, aplicando los conceptos fundamentales de la Programación Orientada a Objetos (POO).

### 🚀 Información del Proyecto
* **Modalidad Elegida:** Opción C - Aplicación web con interfaz gráfica (Flask)
* **Link de la Web Activa:** https://videoclub-vrke.onrender.com

### 👥 Integrantes:
* **Cristian Alias. -**
* **D.N.I.:** 31061946. -

### 🛠️ Tecnologías Utilizadas
* **Backend:** Python 3 + Framework Flask
* **Frontend:** HTML5 / CSS3 / Bootstrap (Interfaz Gráfica)
* **Persistencia:** Archivos JSON para almacenamiento de estados

### 💡 Lógica de Negocio e Implementación (POO)
El sistema cumple con el modelado y encapsulamiento de datos estructurado en clases:
* **Clase ProductoAlquiler:** Administra los atributos individuales de cada título (ID autoincremental, título, tipo, plataforma, género, precio por día y estado de disponibilidad).
* **Clase Catalogo:** Gestor principal que contiene las listas de objetos y encapsula los métodos de negocio del sistema (altas, bajas, cambios de estado para alquiler/devolución y cálculo de ingresos estimados).

### 📐 Requerimientos Mínimos Cumplidos
1. **ABM Completo:** Interfaz visual con tablas y formularios interactivos para administrar el catálogo.
2. **Cambios de Estado:** Lógica de negocio robusta que valida flujos de alquiler y devoluciones.
3. **Persistencia de Datos:** Mini persistencia implementada para mantener el estado del videoclub.
4. **Despliegue Exitoso:** Proyecto subido y hosteado en la nube de forma pública a través de Render.
