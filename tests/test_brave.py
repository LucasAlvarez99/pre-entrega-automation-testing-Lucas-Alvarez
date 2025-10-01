from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Ruta al ChromeDriver descargado
chrome_driver_path = "C:/Users/Lucas/Desktop/drivers/chromedriver.exe"  # Cambia según tu ubicación

# Ruta al ejecutable de Brave
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"  # Cambia según tu PC

# Configurar opciones
options = Options()
options.binary_location = brave_path

# Inicializar WebDriver
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

# Abrir página
driver.get("https://www.saucedemo.com")
print(driver.title)  # Debe mostrar "Swag Labs"
driver.quit()
