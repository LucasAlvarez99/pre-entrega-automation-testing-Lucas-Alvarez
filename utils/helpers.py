import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def esperar_elemento_visible(driver, by, locator, timeout=10):
    """Espera explícita hasta que un elemento sea visible"""
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, locator)))

def esperar_elemento_presente(driver, by, locator, timeout=10):
    """Espera explícita hasta que un elemento esté presente en el DOM."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, locator))
    )

def esperar_clickable(driver, by, locator, timeout=10):
    """Espera hasta que un elemento sea clickeable."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, locator))
    )

def tomar_captura(driver, nombre_archivo):
    """Toma captura de pantalla y guarda en carpeta screenshots con timestamp"""
    # Crear carpeta si no existe
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    # Agregar timestamp para nombres únicos
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    path = os.path.join("screenshots", f"{timestamp}-{nombre_archivo}.png")

    driver.save_screenshot(path)
    print(f"📸 Screenshot guardado en: {path}")
    return path
