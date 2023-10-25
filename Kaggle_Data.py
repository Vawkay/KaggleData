import os
import zipfile
import glob
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def setup():
    print("> Iniciando navegador")
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option('prefs', {'download.default_directory': os.getcwd()})
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# ‘Login’ e senha a serem utilizados no site
login = 'e-mail@email.com'
senha = 'senha@2023'

# Configurando WebDriver
driver = setup()
wait = WebDriverWait(driver, 20)

# Entrando no site, clicando em download e escolhendo login por e-mail
driver.get("https://www.kaggle.com/austinreese/craigslist-carstrucks-data")
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/datasets/austinreese/craigslist-carstrucks-data'
                                                        '/download?datasetVersionNumber=10"]'))).click()

wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="/account/login?phase=emailSignIn"]'))).click()


wait.until(EC.element_to_be_clickable((By.NAME, "email"))).send_keys(login)
wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(senha)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()

# Clicando novamente em download
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/datasets/austinreese/craigslist-carstrucks-data'
                                                        '/download?datasetVersionNumber=10"]'))).click()

# Pesquisando por arquivo na pasta durante 10 segundos
found_file = False
start_time = time.time()
while not found_file and time.time() - start_time < 30:
    file_list = glob.glob("*.zip")
    if len(file_list) > 0:
        found_file = True
    time.sleep(1)
if not found_file:
    raise Exception("Arquivo zip não encontrado após 30 segundos")

# Extraindo o arquivo zip na mesma pasta do script
with zipfile.ZipFile(glob.glob("*.zip")[0], 'r') as my_zip:
    my_zip.extractall('.')

# Encerrando webdriver
driver.close()

# Carregando o CSV para o Pandas
df = pd.read_csv(glob.glob("*.csv")[0])

