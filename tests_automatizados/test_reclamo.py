import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Carpeta fija para guardar evidencias
EVIDENCIA_DIR = r"C:\Users\anaca\OneDrive\Desktop\sistemaReclamos\QA_Evidencias"
os.makedirs(EVIDENCIA_DIR, exist_ok=True)

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_alta_reclamo(driver):
    # Usar la ruta correcta
    driver.get("http://127.0.0.1:8000/registrar/")

    # Completar los campos con esperas explícitas
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "nombre"))).send_keys("Ana Ortiz")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "correo"))).send_keys("ana@example.com")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "telefono"))).send_keys("2211234567")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "categoria"))).send_keys("Atención al Cliente")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "descripcion"))).send_keys("El servicio no funciona correctamente.")

    # Enviar formulario
    driver.find_element(By.CSS_SELECTOR, "button.boton").click()

    # Esperar confirmación
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tarjeta")))

    # Validar confirmación
    assert "N° de Reclamo" in driver.page_source
    assert "Descargar PDF" in driver.page_source
    assert "Nuevo Reclamo" in driver.page_source
    assert "Mis Consultas" in driver.page_source

    # Guardar captura
    driver.save_screenshot(os.path.join(EVIDENCIA_DIR, "reclamo_confirmacion.png"))
