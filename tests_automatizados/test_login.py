import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login_caro(driver):
    # Ir a la página de login
    driver.get("http://127.0.0.1:8000/login/")

    # Completar credenciales
    driver.find_element(By.NAME, "username").send_keys("caro")
    driver.find_element(By.NAME, "password").send_keys("12345")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Esperar que aparezca el menú administrativo
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "bienvenida"), "Bienvenido")
    )

    # Validar que los botones del menú estén presentes
    assert "Alta usuarios" in driver.page_source
    assert "Gestión ABM" in driver.page_source
    assert "Reportes y estadísticas" in driver.page_source
