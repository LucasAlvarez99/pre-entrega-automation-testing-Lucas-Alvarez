from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def esperar_elemento(driver, by, locator, timeout=10):
    """Espera explícita hasta que un elemento sea visible"""
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, locator)))

def tomar_captura(driver, nombre_archivo):
    """Toma captura de pantalla y guarda en carpeta screenshots"""
    driver.save_screenshot(f"screenshots/{nombre_archivo}.png")
