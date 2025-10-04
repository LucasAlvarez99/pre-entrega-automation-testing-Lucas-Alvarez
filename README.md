# pre-entrega-automation-testing-Lucas-Alvarez

## Propósito

Automatizar flujos básicos y negativos en [SauceDemo](https://www.saucedemo.com) usando Selenium WebDriver y Pytest, cumpliendo con las consignas de la pre-entrega: login, ver catálogo, agregar y quitar productos del carrito, y validaciones de errores.

---

## Estructura del Proyecto

- `tests/`  
  Tests automatizados con Pytest.
- `utils/`  
  Helpers reutilizables (esperas explícitas y capturas de pantalla).
- `conftest.py`  
  Fixture de WebDriver y lógica para capturas automáticas.
- `reports/`  
  Reportes HTML generados por pytest.
- `screenshots/`  
  Capturas automáticas de pantalla por cada test.
- `drivers/`  
  (Opcional) Ubicación sugerida para tu chromedriver.exe.

---

## Requisitos

- Python 3.8 o superior (probado con 3.13)
- Google Chrome instalado (o Brave, si ajustas el binario)
- ChromeDriver compatible con tu versión de navegador
- Git (opcional, para versionado)
- Recomendado: entorno virtual

---

## Instalación

1. **Clona el repositorio y entra a la carpeta:**
    ```sh
    git clone https://github.com/LucasAlvarez99/pre-entrega-automation-testing-Lucas-Alvarez
    cd pre-entrega-automation-testing-Lucas-Alvarez
    ```

2. **Crea y activa un entorno virtual:**
    ```sh
    python -m venv venv
    venv\Scripts\activate  # En Windows
    # source venv/bin/activate  # En Linux/macOS
    ```

3. **Instala las dependencias:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Descarga ChromeDriver**  
   Descarga la versión de ChromeDriver que coincida con tu navegador desde  
   https://chromedriver.chromium.org/downloads  (dejo el driver version 140)
   y colócala en la carpeta `drivers/` (o ajusta la ruta en `conftest.py`).

---

## Ejecución de los tests

1. **Corre todos los tests:**
    ```sh
    pytest
    ```

2. **Genera un reporte HTML:**
    ```sh
    pytest --html=reports/reporte.html
    ```

3. **Capturas automáticas:**  
   Cada test genera una captura de pantalla al finalizar, guardada en la carpeta `screenshots/` con nombre descriptivo (por ejemplo, `20251004-182744-carrito_agregar_dos_veces.png`).

---

## ¿Qué cubre la automatización?

- Login exitoso y fallido (campos vacíos, usuario bloqueado, credenciales incorrectas, etc.)
- Validación de elementos del catálogo y productos
- Agregar y quitar productos del carrito
- Validaciones negativas de carrito y catálogo (checkout vacío, productos inexistentes, etc.)
- Capturas automáticas de pantalla para cada test

---

## Personalización

- Puedes ajustar el navegador a Brave descomentando la línea correspondiente en `conftest.py`.
- Puedes agregar más tests en la carpeta `tests/` siguiendo el patrón actual.

---

## Notas

- Si algún test falla, revisa la carpeta `screenshots/` para ver la evidencia visual.
- Si necesitas cambiar la ruta de ChromeDriver, edita la variable `chrome_driver_path` en `conftest.py`.
- El proyecto está listo para ampliarse con más casos de prueba según lo requieras.

---

**Autor:** Lucas Alvarez  
**Pre-entrega: Automatización de Testing - Coderhouse**
