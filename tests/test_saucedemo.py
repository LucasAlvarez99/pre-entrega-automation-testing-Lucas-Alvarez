import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.helpers import esperar_elemento, tomar_captura

URL = "https://www.saucedemo.com"
USUARIO = "standard_user"
PASSWORD = "secret_sauce"

@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Asegurarse de tener chromedriver en PATH
    driver.maximize_window()
    yield driver
    driver.quit()

def test_login(driver):
    driver.get(URL)
    try:
        # Login
        esperar_elemento(driver, By.ID, "user-name").send_keys(USUARIO)
        esperar_elemento(driver, By.ID, "password").send_keys(PASSWORD)
        esperar_elemento(driver, By.ID, "login-button").click()

        # Validar redirección
        titulo = esperar_elemento(driver, By.CLASS_NAME, "title").text
        assert titulo == "Products", "Login fallido o página de inventario incorrecta"

    except Exception as e:
        tomar_captura(driver, "login_error")
        raise e

def test_navegacion_catalogo(driver):
    driver.get(URL)
    # Login previo
    esperar_elemento(driver, By.ID, "user-name").send_keys(USUARIO)
    esperar_elemento(driver, By.ID, "password").send_keys(PASSWORD)
    esperar_elemento(driver, By.ID, "login-button").click()

    try:
        # Validar título
        titulo = esperar_elemento(driver, By.CLASS_NAME, "title").text
        assert titulo == "Products"

        # Validar presencia de productos
        primer_producto = esperar_elemento(driver, By.CLASS_NAME, "inventory_item_name")
        precio_producto = esperar_elemento(driver, By.CLASS_NAME, "inventory_item_price")
        print(f"Primer producto: {primer_producto.text} - Precio: {precio_producto.text}")

        # Validar elementos importantes (ej. menú de filtros)
        menu = esperar_elemento(driver, By.CLASS_NAME, "bm-burger-button")
        assert menu.is_displayed()

    except Exception as e:
        tomar_captura(driver, "catalogo_error")
        raise e

def test_carrito(driver):
    driver.get(URL)
    # Login previo
    esperar_elemento(driver, By.ID, "user-name").send_keys(USUARIO)
    esperar_elemento(driver, By.ID, "password").send_keys(PASSWORD)
    esperar_elemento(driver, By.ID, "login-button").click()

    try:
        # Añadir primer producto al carrito
        boton_add = esperar_elemento(driver, By.CLASS_NAME, "btn_inventory")
        boton_add.click()

        # Verificar contador del carrito
        contador = esperar_elemento(driver, By.CLASS_NAME, "shopping_cart_badge")
        assert contador.text == "1"

        # Navegar al carrito
        esperar_elemento(driver, By.CLASS_NAME, "shopping_cart_link").click()
        producto_carrito = esperar_elemento(driver, By.CLASS_NAME, "inventory_item_name")
        assert producto_carrito.is_displayed()

    except Exception as e:
        tomar_captura(driver, "carrito_error")
        raise e
