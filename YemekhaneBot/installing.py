#selenium ile yemek listesini cekme
from selenium import webdriver
import time
driver=webdriver.Chrome()
url="http://uevi.mdr.firat.edu.tr/tr"
driver.get(url)
result=driver.find_elements_by_css_selector(".extra-inner .extra-content-inner .content-inner .contain .contain-text h5")
for element in result:
    file=open("yemek.txt","a",encoding="utf_8") 
    file.write(element.text+"\n")
    
driver.close()    
