from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from datetime import date, datetime, timedelta
import sqlite3

# Create a new instance of the Firefox driver
conn = sqlite3.connect("publicidad.db")
c = conn.cursor()

driver = webdriver.Firefox()

# go to the google home page
driver.get("http://www.google.com")

# the page is ajaxy so the title is originally this:
print (driver.title)

# find the element that's name attribute is q (the google search box)
inputElement = driver.find_element_by_name("q")


# type in the search
inputElement.send_keys("tv led oferta")

# submit the form (although google automatically searches now without submitting)
inputElement.submit()

try:
    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
    WebDriverWait(driver, 10).until(EC.title_contains("tv led oferta"))

    heading1 = driver.find_elements_by_class_name('ads-ad')
    texto_interno = [head.text for head in heading1]
    ads =[]
    ads2 =[]
    str = ""
    for i in range(0,len(texto_interno)):
        for t in range(0,len(texto_interno[i])):
            print (i, " ", t, " ", texto_interno[i][t])
            if not(texto_interno[i][t] == "\n"):
                str = str+texto_interno[i][t]
            else:
                if str:
                    ads2.append(str)
                str=""
        ads.append(ads2)
        ads2=[]


    tiempo = datetime.now()
    contador = 1

    for text in ads:
        linea1=""
        url=""
        linea2=""
        for i in range(0,len(text)):
            if i == 0:
                linea1 = text[0]
            if i == 1:
                url = text[1]
            if i == 2:
                linea3 = text[2]

        c.execute("INSERT INTO publi VALUES (?, ?, ?, ?)", (tiempo.strftime("%d/%m/%Y %H:%M:%S"), linea1,url,linea3))
        print(text)

    conn.commit()

finally:
    driver.quit()