import os
import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.helpers import tomar_captura, ensure_dir

# Rutas comunes para Brave (si querés forzar otro binario, cambia BRAVE_PATH env var)
BRAVE_COMMON_PATHS = [
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
]

def _find_brave_binary():
    # 1) chequear variable de entorno BRAVE_BIN
    env_path = os.environ.get("BRAVE_BIN")
    if env_path and os.path.exists(env_path):
        return env_path
    # 2) chequear rutas comunes
    for p in BRAVE_COMMON_PATHS:
        if os.path.exists(p):
            return p
    # 3) intentar which
    path = shutil.which("brave-browser") or shutil.which("brave")
    if path:
        return path
    return None

@pytest.fixture(scope="function")
def driver(request):
    options = Options()
    options.binary_location = _find_brave_binary()

    # 👇 Ruta local de tu chromedriver 140
    chrome_driver_path = r"C:\Users\Lucas\Documents\pre-entrega-automation-testing-Lucas-Alvarez\drivers\chromedriver.exe"
    service = Service(chrome_driver_path)

    driver = webdriver.Chrome(service=service, options=options)
    request.node._driver = driver
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    driver = getattr(item, "_driver", None)

    if rep.when == "call" and driver:
        nombre = f"{rep.nodeid.replace('::', '_')}_{rep.outcome}"
        try:
            path = tomar_captura(driver, nombre)
            print(f"Screenshot guardado: {path}")
        except Exception as e:
            print(f"No se pudo guardar screenshot: {e}")