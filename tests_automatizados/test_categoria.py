import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_crear_categoria(driver):
    driver.get("http://localhost:8000/login/")

    # Login
    usuario_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    usuario_input.send_keys("caro")
    password_input.send_keys("12345")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-acceder"))
    ).click()

    # Menú admin → Gestión ABM
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Gestión ABM')]"))
    ).click()

    # Panel de control → botón azul Ver
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Ver')]"))
    ).click()

    # Página detalle → botón rosa Gestionar Categorías
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-rosa"))
    ).click()

    # 🔎 Depuración: guardar screenshot y URL después del click
    os.makedirs("QA_Evidencias", exist_ok=True)
    driver.save_screenshot("QA_Evidencias/debug_after_btn_rosa.png")
    print("URL actual:", driver.current_url)

    # Esperar directamente el campo de nueva categoría
    campo_nombre = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "nombre"))
    )
    campo_nombre.send_keys("Soporte QA")

    # Guardar categoría
    driver.find_element(By.XPATH, "//button[contains(.,'Guardar')]").click()

    # Validar que aparece en la tabla
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "table"), "Soporte QA")
    )

    # Evidencia final
    driver.save_screenshot("QA_Evidencias/CP-ABM-001_categoria.png")
    assert "Soporte QA" in driver.page_source
