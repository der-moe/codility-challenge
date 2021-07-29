import datetime
import time
import PySimpleGUI as sg

layout = [[sg.Text("Choose a room"), sg.InputText('A', key="room-val")],
          [sg.Text("Room Score:"), sg.Text("🙂", key="room")],
          [sg.Text("Building Score"), sg.Text("😐", key="building")]]

window = sg.Window(title="Smart Office Scanner", layout=layout, margins=(100, 50))

timer = datetime.datetime.now()

window.read()

while True:
    # time.sleep(15)
    event, values = window.read()
    # ------ call api

    window["room"].update("😟")

window.close()
