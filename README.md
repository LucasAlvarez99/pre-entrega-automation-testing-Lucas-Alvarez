# pre-entrega-automation-testing-[Nombre-Apellido]

## Propósito
Automatizar flujos básicos en https://www.saucedemo.com usando Selenium WebDriver y Pytest,
cumpliendo con las consignas de la pre-entrega (login, ver catálogo y agregar producto al carrito).

## Estructura
- `tests/` -> tests de pytest
- `utils/` -> helpers (esperas y captura de pantalla)
- `conftest.py` -> fixture de WebDriver y hook para screenshots
- `reports/` -> reportes HTML
- `screenshots/` -> capturas automáticas al fallar

## Requisitos
- Python 3.8+ (probado con 3.13)
- Tener Brave o Chrome instalados. Para Brave, el script intenta detectar binario automáticamente.
- Git para versionado.

## Instalación
1. Crear y activar entorno virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
