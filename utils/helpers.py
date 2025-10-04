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
    """Guarda una captura en la carpeta 'screenshots' dentro del proyecto"""
    try:
        carpeta = "screenshots"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        path = os.path.join(carpeta, f"{timestamp}-{nombre_archivo}.png")
        resultado = driver.save_screenshot(path)
        if resultado:
            print(f"✅ Screenshot guardado correctamente: {path}")
            return path
        else:
            print(f"⚠️ Selenium no pudo guardar el screenshot (resultado=False)")
            return None
    except Exception as e:
        print(f"❌ Error al tomar captura: {e}")
        return None