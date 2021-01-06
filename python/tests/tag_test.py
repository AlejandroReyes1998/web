from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',options=options)

driver.get('http://localhost:5000/login')
driver.implicitly_wait(30)
driver.find_element_by_id('nombreUsuario').send_keys('extra')
driver.find_element_by_id('passwor_d').send_keys('innings')

driver.find_element_by_id('login-submit').click()
driver.implicitly_wait(30)
# create a new note

# set the tag info

criterio = 'minatozaki sana'
sugerencias = 'myoui mina'
motivo = 'hirai momo'

driver.get('http://localhost:5000/medico/altanota/2/')
driver.implicitly_wait(60)
# datos de nota médica
driver.find_element_by_id('resumenInterrogatorio').send_keys('guillotine')
driver.find_element_by_id('planotratamiento').send_keys('all caps')
driver.find_element_by_id('pronostico').send_keys('the best thing i ever did')
driver.find_element_by_id('exploracion').send_keys('through the wire')
driver.find_element_by_id('resultado').send_keys('el scorcho')
driver.find_element_by_id('diagnostico').send_keys('porcelina of the vast oceans')
driver.find_element_by_id('edomental').send_keys('medellia of the gray skies')
# signos vitales
driver.find_element_by_id('peso').send_keys('1979')
driver.find_element_by_id('talla').send_keys('77')
driver.find_element_by_id('tension').send_keys('808')
driver.find_element_by_id('frecuenciaCardiaca').send_keys('1337')
driver.find_element_by_id('frecuenciaRespiratoria').send_keys('88')
driver.find_element_by_id('temperatura').send_keys('44')
# información de etiqueta
driver.find_element_by_id('criteriodiagnostico').send_keys(criterio)
driver.find_element_by_id('sugerenciasdiagnosticas').send_keys(sugerencias)
driver.find_element_by_id('motivoconsulta').send_keys(motivo)
driver.implicitly_wait(120)
#read the tag

driver.get('http://localhost:5000/medico/selectkey/2')
driver.implicitly_wait(30)
# select martinez_islas private key
driver.find_element_by_id('key-upload').send_keys('/home/pi/web/python/martinez_islas_mauricio_private.pem')
driver.find_element_by_id('selectkey-submit').click()

# check if next url is correct
if (driver.current_url == 'http://localhost:5000/medico/selectkey/2/'):
	driver.implicitly_wait(40)
	rcriterio = driver.find_element_by_id('criterio').get_attribute('innerHTML')
	rsugerencias = driver.find_element_by_id('sugerencias').get_attribute('innerHTML')
	rmotivo = driver.find_element_by_id('motivo').get_attribute('innerHTML')

	if rcriterio == criterio and rsugerencias == sugerencias and rmotivo == motivo:
		print('TEST SUCCESSFUL')
	# check if results are correct
