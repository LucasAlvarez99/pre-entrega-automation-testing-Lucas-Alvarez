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
    driver.get(URL)
    driver.find_element(By.ID, "user-name").send_keys("usuario_invalido")
    driver.find_element(By.ID, "password").send_keys("clave_invalida")
    driver.find_element(By.ID, "login-button").click()
    error_msg = esperar_elemento_visible(driver, By.XPATH, "//h3[@data-test='error']", timeout=5).text
    assert "Epic sadface" in error_msg, f"El mensaje esperado no apareció. Se obtuvo: {error_msg}"
def test_login_sin_usuario(driver, request):
    """Intentar login sin ingresar usuario."""
    request.node.nombre_captura = "login_sin_usuario"
    driver.get(URL)
    driver.find_element(By.ID, "password").send_keys(PASS)
    driver.find_element(By.ID, "login-button").click()
    error_msg = esperar_elemento_visible(driver, By.XPATH, "//h3[@data-test='error']", timeout=5).text
    assert "Username is required" in error_msg

def test_login_sin_password(driver, request):
    """Intentar login sin ingresar contraseña."""
    request.node.nombre_captura = "login_sin_password"
    driver.get(URL)
    driver.find_element(By.ID, "user-name").send_keys(USER)
    driver.find_element(By.ID, "login-button").click()
    error_msg = esperar_elemento_visible(driver, By.XPATH, "//h3[@data-test='error']", timeout=5).text
    assert "Password is required" in error_msg

def test_login_usuario_bloqueado(driver, request):
    """Intentar login con usuario bloqueado."""
    request.node.nombre_captura = "login_usuario_bloqueado"
    driver.get(URL)
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys(PASS)
    driver.find_element(By.ID, "login-button").click()
    error_msg = esperar_elemento_visible(driver, By.XPATH, "//h3[@data-test='error']", timeout=5).text
    assert "locked out" in error_msg.lower()
    

def test_login_con_campos_vacios(driver, request):
    """Intentar login sin usuario ni contraseña."""
    request.node.nombre_captura = "login_campos_vacios"
    driver.get(URL)
    driver.find_element(By.ID, "login-button").click()
    error_msg = esperar_elemento_visible(driver, By.XPATH, "//h3[@data-test='error']", timeout=5).text
    assert "Username is required" in error_msg

def test_login_con_espacios(driver, request):
    """Intentar login con espacios en usuario y contraseña."""
    request.node.nombre_captura = "login_con_espacios"
    driver.get(URL)
    driver.find_element(By.ID, "user-name").send_keys("   ")
    driver.find_element(By.ID, "password").send_keys("   ")
    driver.find_element(By.ID, "login-button").click()
    error_msg = esperar_elemento_visible(driver, By.XPATH, "//h3[@data-test='error']", timeout=5).text
    assert "Username is required" in error_msg or "Epic sadface" in error_msg

def test_login_con_usuario_case_sensitive(driver, request):
    """Intentar login con usuario correcto pero en mayúsculas (case sensitive)."""
    request.node.nombre_captura = "login_usuario_case_sensitive"
    driver.get(URL)
    driver.find_element(By.ID, "user-name").send_keys(USER.upper())
    driver.find_element(By.ID, "password").send_keys(PASS)
    driver.find_element(By.ID, "login-button").click()
    error_msg = esperar_elemento_visible(driver, By.XPATH, "//h3[@data-test='error']", timeout=5).text
    assert "Epic sadface" in error_msg

def test_login_con_password_incorrecta(driver, request):
    """Intentar login con usuario correcto y password incorrecta."""
    request.node.nombre_captura = "login_password_incorrecta"
    driver.get(URL)
    driver.find_element(By.ID, "user-name").send_keys(USER)
    driver.find_element(By.ID, "password").send_keys("contraseña_incorrecta")
    driver.find_element(By.ID, "login-button").click()
    error_msg = esperar_elemento_visible(driver, By.XPATH, "//h3[@data-test='error']", timeout=5).text
    assert "Epic sadface" in error_msg

def test_login_con_usuario_inexistente(driver, request):
    """Intentar login con usuario que no existe."""
    request.node.nombre_captura = "login_usuario_inexistente"
    driver.get(URL)
    driver.find_element(By.ID, "user-name").send_keys("no_existo")
    driver.find_element(By.ID, "password").send_keys(PASS)
    driver.find_element(By.ID, "login-button").click()
    error_msg = esperar_elemento_visible(driver, By.XPATH, "//h3[@data-test='error']", timeout=5).text
    assert "Epic sadface" in error_msg
    
def test_agregar_y_remover_producto_carrito(driver, request):
    """Agregar y luego remover un producto del carrito, verificar que el carrito queda vacío."""
    request.node.nombre_captura = "carrito_remover_producto"
    login(driver)
    boton_add = esperar_clickable(driver, By.CLASS_NAME, "btn_inventory", timeout=10)
    boton_add.click()
    # Ir al carrito
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    # Remover producto
    boton_remove = esperar_clickable(driver, By.CLASS_NAME, "cart_button", timeout=5)
    boton_remove.click()
    # Verificar que el carrito está vacío (no hay items)
    items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(items) == 0, "El carrito debería estar vacío después de remover el producto"

def test_carrito_vacio_no_permite_checkout(driver, request):
    """Intentar ir a checkout con el carrito vacío y validar que no avanza."""
    request.node.nombre_captura = "carrito_checkout_vacio"
    login(driver)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    # Intentar hacer checkout sin productos
    checkout_btns = driver.find_elements(By.ID, "checkout")
    if checkout_btns:
        checkout_btns[0].click()
        # Debería mostrar algún mensaje o no avanzar
        assert driver.current_url.endswith("/cart.html"), "No debería avanzar a checkout con carrito vacío"
    else:
        # Si no hay botón, el comportamiento es correcto
        assert True

def test_catalogo_no_muestra_productos_inexistentes(driver, request):
    """Verificar que no existen productos con nombres inventados en el catálogo."""
    request.node.nombre_captura = "catalogo_producto_inexistente"
    login(driver)
    productos = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    nombres = [p.text for p in productos]
    assert "Producto Fantasma" not in nombres, "No debería existir un producto llamado 'Producto Fantasma'"

def test_no_se_puede_agregar_mismo_producto_dos_veces(driver, request):
    """Intentar agregar el mismo producto dos veces y verificar que solo aparece una vez en el carrito."""
    request.node.nombre_captura = "carrito_agregar_dos_veces"
    login(driver)
    boton_add = esperar_clickable(driver, By.CLASS_NAME, "btn_inventory", timeout=10)
    boton_add.click()
    # Intentar hacer click de nuevo (el botón debería cambiar a 'Remove' y no permitir agregar de nuevo)
    assert not boton_add.is_displayed() or boton_add.text != "Add to cart", "No debería poder agregar el mismo producto dos veces"
    # Ir al carrito y verificar solo un producto
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(items) == 1, "Solo debería haber un producto en el carrito"

def test_no_se_puede_remover_producto_inexistente(driver, request):
    """Intentar remover un producto que no está en el carrito (no debería haber botón 'Remove')."""
    request.node.nombre_captura = "carrito_remover_inexistente"
    login(driver)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    remove_btns = driver.find_elements(By.CLASS_NAME, "cart_button")
    assert len(remove_btns) == 0, "No debería haber botón 'Remove' si el carrito está vacío"