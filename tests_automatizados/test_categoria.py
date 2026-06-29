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

def test_crear_categoria(driver):
    # Login
    driver.get("http://127.0.0.1:8000/login/")
    driver.find_element(By.NAME, "username").send_keys("caro")
    driver.find_element(By.NAME, "password").send_keys("12345")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Menú Gestión ABM
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Gestión ABM')]"))
    ).click()

    # Botón Ver (detalle reclamo)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.ver"))
    ).click()

    # Enlace Gestionar Categorías (rosa)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn-rosa"))
    ).click()

    # Esperar directamente el input de nueva categoría
    input_nombre = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, "nombre"))
    )
    input_nombre.clear()
    input_nombre.send_keys("QA2")

    # Guardar la nueva categoría
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    ).click()

    # Validar que aparece en el listado
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "QA2")
    )
    assert "QA2" in driver.page_source

    # Guardar evidencia
    driver.save_screenshot(os.path.join(EVIDENCIA_DIR, "categoria_QA2.png"))
