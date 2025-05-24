# NewtonLab Proyecto de análisis numérico

## Estudiantes
- Santiago Acevedo Urrego
- Miguel Ángel Cano Salinas
- Daniel Correa Botero

## Descripción de la aplicación
Los métodos que nuestra aplicación resuelve son:
- Método de Bisección
- Método de Regla Falsa
- Método de Punto Fijo
- Método de Newton-Raphson
- Método de la Secante
- Método de Raíces Múltiples #1
- Método de Raíces Múltiples #2
- Método de Jacobi
- Método de Gauss-Seidel
- Método SOR (Sobre-relajación Sucesiva)
- Método de Vandermonde
- Método de Interpolación de Newton
- Método de Lagrange
- Métodos de Spline Lineal, Cuadrático y Cúbico

## Requisitos previos
- Python 3.x instalado.
- `pip` instalado.
- Virtualenv (opcional pero recomendado).

## Pasos para configurar el proyecto

1. **Crear un entorno virtual (opcional pero recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Crear variables de entorno**
   - Copiar el archivo `.env.example` a `.env`:
     ```bash
     cp .env.example .env
     ```
   - Modificar el archivo `.env` con las configuraciones apropiadas según sea necesario.

4. **Ejecutar el servidor**
   ```bash
   python manage.py runserver
   ```

5. **Acceder a la aplicación**
   - Abrir el navegador y visitar: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).