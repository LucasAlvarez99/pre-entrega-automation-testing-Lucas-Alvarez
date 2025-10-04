import pytest
from selenium.webdriver.common.by import By
from utils.helpers import esperar_elemento_visible, esperar_clickable, tomar_captura

URL = "https://www.saucedemo.com"
USER = "standard_user"
PASS = "secret_sauce"

def login(driver, username=USER, password=PASS):
    driver.get(URL)
    esperar_elemento_visible(driver, By.ID, "user-name").clear()
    driver.find_element(By.ID, "user-name").send_keys(username)
    esperar_elemento_visible(driver, By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    esperar_clickable(driver, By.ID, "login-button").click()

def test_login_redireccion_inventory(driver):
    """Automatización de Login y validación de redirección a /inventory.html y título."""
    login(driver)
    # validar que llegamos a inventory y el título sea "Products"
    titulo = esperar_elemento_visible(driver, By.CLASS_NAME, "title", timeout=10).text
    assert "Products" in titulo, f"Título esperado 'Products' pero se encontró '{titulo}'"
    assert "/inventory.html" in driver.current_url or "inventory" in driver.current_url

def test_catalogo_y_elementos_basicos(driver):
    """Verificar título, existencia de productos y listar nombre/precio del primero."""
    login(driver)
    titulo = esperar_elemento_visible(driver, By.CLASS_NAME, "title", timeout=10).text
    assert titulo == "Products"
    # comprobar que hay al menos un producto visible
    primer_nombre = esperar_elemento_visible(driver, By.CLASS_NAME, "inventory_item_name", timeout=10).text
    primer_precio = esperar_elemento_visible(driver, By.CLASS_NAME, "inventory_item_price", timeout=10).text
    assert primer_nombre != ""
    assert primer_precio.startswith("$")
    # verificar presencia de elementos importantes (menu de la izquierda/burger y filtros)
    assert driver.find_element(By.CLASS_NAME, "bm-burger-button").is_displayed()
    assert driver.find_element(By.CLASS_NAME, "product_sort_container").is_displayed()
    # imprimir en consola para evidencia
    print(f"Producto 1 -> {primer_nombre} - {primer_precio}")

def test_agregar_producto_y_verificar_carrito(driver):
    """Agregar el primer producto al carrito, verificar contador y ver en carrito."""
    login(driver)
    # agregar primer producto (botón 'Add to cart')
    boton_add = esperar_clickable(driver, By.CLASS_NAME, "btn_inventory", timeout=10)
    boton_add.click()

    # verificar contador del carrito
    cart_badge = esperar_elemento_visible(driver, By.CLASS_NAME, "shopping_cart_badge", timeout=5)
    assert cart_badge.text == "1", f"Contador del carrito esperado '1' pero fue '{cart_badge.text}'"

    # navegar al carrito y verificar item
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    item_name = esperar_elemento_visible(driver, By.CLASS_NAME, "inventory_item_name", timeout=10).text
    assert item_name != ""

# fallo provocado con intencion de mostrar que al fallar se va a tomar captura   
def test_login_invalido_muestra_error(driver, request):
    """Intentar login con credenciales incorrectas y validar mensaje de error."""
    # Setear nombre personalizado para la captura
    request.node.nombre_captura = "fallo_forzado"
    driver.get("https://www.saucedemo.com")
    driver.find_element(By.ID, "user-name").send_keys("usuario_invalido")
    driver.find_element(By.ID, "password").send_keys("clave_invalida")
    driver.find_element(By.ID, "login-button").click()
    error_msg = esperar_elemento_visible(driver, By.XPATH, "//h3[@data-test='error']", timeout=5).text
    assert "Epic sadface" in error_msg, f"El mensaje esperado no apareció. Se obtuvo: {error_msg}"
