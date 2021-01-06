from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome
import time
import random
import string


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    #print("Random string of length", length, "is:", result_str)
    return result_str


options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Firefox()

driver.get('http:/127.0.0.1:5000/login')
time.sleep(5)
#login1
driver.find_element_by_id('nombreUsuario').send_keys(get_random_string(8))
driver.find_element_by_id('passwor_d').send_keys(get_random_string(8))

#driver.find_element_by_id('login-submit').click()
#time.sleep(5)
#login2

# time.sleep(1)
# driver.find_element_by_id('nombreUsuario').send_keys("CesarUrico")
# driver.find_element_by_id('passwor_d').send_keys(get_random_string(8))

# driver.find_element_by_id('login-submit').click()
# time.sleep(5)
#login3
# time.sleep(1)
# driver.find_element_by_id('nombreUsuario').send_keys("CesarUrico")
# driver.find_element_by_id('passwor_d').send_keys("cesarurieladmin123")

# driver.find_element_by_id('login-submit').click()
# time.sleep(5)
# create a new note

    
#driver.close()