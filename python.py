# print("Hello World")
numero1 = 5
numero2 = 10
print(numero1+numero2)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service  
from webdriver_manager.chrome import ChromeDriverManager
import time

email = "email"
senha = "senha"
# print("Importação deu bom!")

pesquisa = input("Insira um Tema: ") #input para pegar oq o usuari deseja

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # para o google abrir

driver.get("https://accounts.google.com") # navegar link desejado
time.sleep(5) # tempo de exibição

# inserindo email  
email_input = driver.find_element(By.ID, "identifierId")
email_input.send_keys(email)
email_input.send_keys(Keys.RETURN)
time.sleep(5)
# inserindo senha
senha_input = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
senha_input.send_keys(senha)
senha_input.send_keys(Keys.RETURN)
time.sleep(8)

driver.get("https://www.youtube.com")
time.sleep(2)
# encontrando a barra de pesquisa de youtube
barra_de_pesquisa = driver.find_element(By.NAME, "search_query")
# limpando a barra de pesquisa
barra_de_pesquisa.clear()
barra_de_pesquisa.send_keys(pesquisa)
barra_de_pesquisa.send_keys(Keys.RETURN)
time.sleep(30)

# importando as libs / pip install opencv-python pyautogui
import cv2
import mediapipe as mp
import pyautogui
import math

# iniciando processamento das maos
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# definido parametros de detecção de mao

hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# iniciando a captura de video

cap = cv2.VideoCapture(0)

# informando o tamanho da minha tela

screen_width, screen_height = pyautogui.size()

# funcao para calcular a menor distancia entra dois pontos

def calculate_distance(p1, p2):
    return math.sqrt((p1.x - p2.x)*2 + (p1.y -p2.y)2 + (p1.z - p2.z)*2)

#loop para processar as mãos 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # convertendo a imagem pra rbg

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processando a imagem para deteção

    result = hands.process(frame_rgb)

    # obtendo as dimensões da captura (frame)

    frame_height, frame_width, _ = frame.shape

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # extrair pontos da maos 
            index_finger_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            #calcular a distancia entre o mata-piolho e o fura-bolo
            distance = calculate_distance(index_finger_tip, thumb_tip)

            # mover cursor do mouse
            x = int(index_finger_tip.x * frame_width)
            y = int(thumb_tip.y * frame_height)

            # invertendo o eixo x e ajustando o eixo y
            screen_x = screen_width - (screen_width / frame_width * x)
            screen_y = screen_height / frame_height *y

            pyautogui.moveTo(screen_x, screen_y)

            # se os pontos dos dedos estao proximos o suficiente pra clicar
            if distance < 0.05:
                pyautogui.click()
            
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # MOSTRAR TELINHA SEM ESPELHAR
    cv2.imshow("pegou a mão", frame)

# soltando a bagaça toda
cap.release()
cv2.destroyAllWindows()