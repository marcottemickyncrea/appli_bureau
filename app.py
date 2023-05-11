from tkinter import *
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link = 'https://www.worldometers.info/'

options = Options()
options.add_argument('--headless=chrome')
options.add_argument('--desable-web-security')

def get_population_count(wait,link):   
    driver.get(link)
    data = {}
    while True:
        data['population_mondiale'] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"span[rel='current_population']"))).text
        if "retrieving data" not in data['population_mondiale']:
            break
    while True:
        data['nb_naissance'] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"span[rel='births_today']"))).text
        if "retrieving data" not in data['nb_naissance']:
            break
    while True:
        data['nb_deces'] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"span[rel='dth1s_today']"))).text
        if "retrieving data" not in data['nb_deces']:
            break
    while True:
        data['difference'] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"span[rel='absolute_growth']"))).text
        if "retrieving data" not in data['difference']:
            break
    return data


with webdriver.Chrome(chrome_options=options) as driver:
    wait = WebDriverWait(driver,10)
    data = get_population_count(wait,link)

root = Tk()
root.geometry("530x750")
bg = PhotoImage(file = "Image_brief.png")
bg = bg.subsample(3)

canvas1 = Canvas(root, width=500, height=800)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")

populations= int(data['population_mondiale'].replace(',', ''))
nb_naissance = int(data['nb_naissance'].replace(',',''))
nb_deces = int(data['nb_deces'].replace(',',''))
incrementation_jour = int(data['difference'].replace(',',''))

populations_label= canvas1.create_text(200, 50, text="Population mondiale: {}".format(populations), font=("Helvetica", 15, "bold"), fill='white')  
nb_naissance_label = canvas1.create_text(280, 100, text="Nombre de naissance: {}".format(nb_naissance), font=("Helvetica", 15, "bold"), fill='white')  
nb_deces_label = canvas1.create_text(320, 150, text="Nombre de décès: {}".format(nb_deces), font=("Helvetica", 15, "bold"), fill='white')  
incrementation_jour_label = canvas1.create_text(360, 200, text="+ {} terrien aujourd'hui".format(incrementation_jour), font=("Helvetica", 15, "bold"), fill='white') 

def update_data():
    global populations  
    global incrementation_jour
    global nb_naissance
    global nb_deces
    nb_naissance_seconde = random.randint(1, 3)
    nb_naissance += nb_naissance_seconde
    nb_deces_seconde = random.randint(0, 2)
    nb_deces += nb_deces_seconde
    reste_seconde = (nb_naissance_seconde - nb_deces_seconde)
    incrementation_jour += reste_seconde
    populations += reste_seconde
    canvas1.itemconfigure(populations_label, text="Population mondiale: {}".format(populations))
    canvas1.itemconfigure(nb_naissance_label, text="Nombre de naissance: {}".format(nb_naissance))
    canvas1.itemconfigure(nb_deces_label, text="Nombre de décès: {}".format(nb_deces))
    canvas1.itemconfigure(incrementation_jour_label, text="+ {} terrien aujourd'hui".format(incrementation_jour))
    root.after(1000, update_data)

canvas1.create_rectangle(150, 300, 470, 590, outline="white", width=8)
canvas1.create_text(310, 450, text="What's\nup today,\nWorld ?", font=("Helvetica", 50, "bold"), fill='white')

update_data()

root.mainloop()
