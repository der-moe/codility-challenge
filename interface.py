import random
import PySimpleGUI as sg
import Score


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
    if score > 4:
        return "green"
    elif score > 3:
        return "yellow"
    elif score > 2:
        return "orange"
    else:
        return "red"


def call_api(room_val):
    global score, color
    room_val = room_val.upper()
    hints = Score.getIndividualScore(room_val)
    score = 5 - len(hints)
    if score < 0:
        score = 0
    color = get_color(score)
    window["room"].update("Score: %s" % score, background_color=color)
    window["hints-room"].update('\n'.join(hints))
    hints = Score.getTotalScore()
    score = 5 - len(hints)
    if score < 0:
        score = 0
    color = get_color(score)
    window["building"].update("Score: %s" % score, background_color=color)
    warn = []
    if len(hints) > 0:
        if not isinstance(hints[0], (int, float)):
            warn.append(hints[0])
        if isinstance(hints[-1], (int, float)):
            warn.append("Der Durchschnitt aller Büroräume ist unter %s" % hints[-1])
    window["hints-building"].update('\n'.join(warn))



sg.theme("DarkBlue")

layout = [[sg.Text("Choose a room:", size=(15, 1)),
           sg.InputText('A', key="room-val", tooltip="Type the key of a room (A-Z)", size=(15, 1)),
           sg.Button("Refresh", key="refresh")],
          [sg.Text("Your room score:", size=(15, 1)), sg.Text("", text_color="black", size=(20, 1), key="room")],
          [sg.Text("Hinweise:", size=(15, 1)), sg.Text("", size=(30, 5), key="hints-room")],
          [sg.Text("Building score:", size=(15, 1)), sg.Text("", size=(20, 1), text_color="black", key="building")],
          [sg.Text("Hinweise:", size=(15, 1)), sg.Text("", size=(30, 4), key="hints-building")]]

window = sg.Window(title="Smart Office Scanner", layout=layout)
# call_api()
while True:
    event, values = window.read(timeout=15000, timeout_key="auto-update")
    room_val = window["room-val"].get()
    # print(room_val)
    if check_char(room_val):
        if event == 'refresh':
            call_api(room_val)
        if event == 'auto-update':
            call_api(room_val)
    if window.was_closed():
        break

window.close()
