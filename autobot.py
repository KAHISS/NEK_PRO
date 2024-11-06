import pyautogui
from keyboard import write
from time import sleep
from datetime import datetime
import locale
from largeVariables import messageForCharge
from databaseConnection import DataBase


class SendMessage:
    def __init__(self):
        pyautogui.PAUSE = 2
        pyautogui.FAILSAFE = True

    @staticmethod
    def open_whatsapp():
        pyautogui.hotkey('win', 's')
        pyautogui.write('whatsapp')
        pyautogui.press('enter')
        pyautogui.hotkey('win', 'up')

    @staticmethod
    def pause(file):
        while True:
            abriu = pyautogui.locateCenterOnScreen(file)
            if abriu:
                break
            else:
                continue

    @staticmethod
    def pick_saluation():
        salutation = ''
        if float(datetime.now().strftime('%H.%M')) < 12.00:
            salutation = 'Bom dia'
        elif 12.00 <= float(datetime.now().strftime('%H:%M').replace(':', '.')) < 18.00:
            salutation = 'Boa tarde'
        else:
            salutation = 'Boa noite'
        return salutation

    def whatsapp(self, contacts):
        locale.setlocale(locale.LC_TIME, 'pt_BR')
        for contact in contacts:
            # entering in chat of contact =========================
            pyautogui.click(x=25, y=119, duration=1)
            pyautogui.hotkey('ctrl', 'f')
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            # vaditing phone for send message =========================
            birthday = datetime.strptime(contact[4], '%d/%m/%Y')
            age = datetime.now().year - birthday.year
            receiver = ''
            if age <= 13:
                write(contact[8].replace('9', '', 1))
                receiver = contact[5]
            else:
                write(contact[7].replace('9', '', 1))
                receiver = contact[1]
            sleep(1.5)

            # send message ================================
            pyautogui.click(x=289, y=191, duration=1)
            pyautogui.click(x=724, y=720, duration=1)
            sleep(1.5)
            # pick plan value =============================
            price = DataBase('resources/Informações.db').searchDatabase(f'SELECT valor FROM Planos WHERE plano = "{contact[15]}"')[0][0]
            # writing menssage and sending
            linesMessage = messageForCharge.format(self.pick_saluation(), receiver, datetime.now().strftime('%m/%Y'), contact[15], price).split('\n')
            pyautogui.PAUSE = 0.4
            for line in linesMessage:
                write(line)
                pyautogui.hotkey('shift', 'enter')
            pyautogui.PAUSE = 2
            pyautogui.press('return')
            pyautogui.press('esc')
            sleep(1)
