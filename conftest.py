import os
import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utils.helpers import tomar_captura

@pytest.fixture(scope="function")
def driver(request):
    options = Options()
    # options.binary_location = _find_brave_binary()
    chrome_driver_path = r"C:\Users\Lucas\Documents\pre-entrega-automation-testing-Lucas-Alvarez\drivers\chromedriver.exe"
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    request.node._driver = driver
    yield driver

    # Determinar el nombre del screenshot
    nombre_captura = getattr(request.node, "nombre_captura", None)
    if not nombre_captura:
        # Si no se setea desde el test, usar nombre del test y resultado
        nombre_captura = f"{request.node.name}_exitoso"
    path = tomar_captura(driver, nombre_captura)
    print(f"Screenshot guardado: {path}")

    driver.quit()