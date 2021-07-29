import random
import PySimpleGUI as sg


def check_char(c):
    c = str(c)
    if len(c) > 1:
        window["room"].update("Input has to be only one char")
        return False
    if not c.isalpha():
        window["room"].update("Input has to be alphabetical")
        return False
    return True


def get_color(score):
    if score > 80:
        return "green"
    elif score > 50:
        return "yellow"
    elif score > 20:
        return "orange"
    else:
        return "red"


sg.theme("DarkBlue")

layout = [[sg.Text("Choose a room:", size=(15, 1)),
           sg.InputText('A', key="room-val", tooltip="Type the key of a room (A-Z)", size=(15, 1)),
           sg.Button("Refresh", key="refresh")],
          [sg.Text("Your room score:", size=(15, 1)), sg.Text("Good 🙂", background_color="green", text_color="black", size=(20, 1), key="room")],
          [sg.Text("Building score:", size=(15, 1)), sg.Text("Bad 😐", size=(20, 1), key="building")]]

window = sg.Window(title="Smart Office Scanner", layout=layout)

while True:
    event, values = window.read(timeout=15000, timeout_key="auto-update")
    room_val = window["room-val"].get()
    print(room_val)
    if check_char(room_val):
        if event == 'refresh':
            # ------ call api
            score = random.randint(0, 100)
            color = get_color(score)
            window["room"].update("Score: %s" % score, background_color=color)
        if event == 'auto-update':
            # ------ call api
            score = random.randint(0, 100)
            color = get_color(score)
            window["room"].update("Medium 😟")
    if window.was_closed():
        break

window.close()
