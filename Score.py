import json


def getIndividualScore(id, data = None):
    if data is None:
        data = __getData()
    room = __getRoom(data, id)
    sensors = room['sensors']
    print(room)
    print(sensors)

    warnings = []

    if sensors['lightOn'] and data['solarPowerOutput'] > 10:
        warnings = warnings.append("Das Licht ist angeschaltet, obwohl es Hell ist")
    if sensors['windowsOpen'] and sensors['airConditioningRunning']:
        warnings.append("Das Fenster ist offen, obwohl die Klimaanlage angeschlatet ist")
    if sensors['windowsOpen'] and sensors['heaterRunning']:
        warnings.append("Das Fenster ist offen, obwohl die Heizung angeschlatet ist")
    if sensors['airConditioningRunning'] and sensors['heaterRunning']:
        warnings.append("Sowohl Heizung, als auch Klimaanlage sind eingeschaltet")
    if sensors['rollerBlindsClosed'] == False and sensors['airConditioningRunning']:
        warnings.append("Die Klimaanlage ist an, obwohl die Rollläden oben sind")
    if sensors['airConditioningRunning'] and room['temperature'] < 22:
        warnings.append("Die Klimaanlage ist an, es bereits kälter als 22 Grad ist")
    if not sensors['airConditioningRunning'] and room['temperature'] < 22:
        if sensors['airConditioningRunning'] and room['temperature'] > data['building']['outdoorTemperature']:
            warnings.append("Die Klimaanlage ist an, obwohl es draußen kühler als drinnen ist")
    if sensors['airConditioningRunning'] and room['temperature'] > 24:
        warnings.append("Die Klimaanlage ist an, es bereits kälter als 24 Grad ist")
    if not sensors['airConditioningRunning'] and room['temperature'] < 24:
        if sensors['airConditioningRunning'] and room['temperature'] > data['building']['outdoorTemperature']:
            warnings.append("Die Klimaanlage ist an, obwohl es draußen kühler als drinnen ist")
    return warnings


def __getRoom(data, id):
    for x in data['rooms']:
        if x['id'] == id:
            return x


def __getData():
    import urllib.request, json
    with urllib.request.urlopen("https://rvj6rnbpxj.execute-api.eu-central-1.amazonaws.com/prod/live-data") as url:
        data = json.loads(url.read().decode())
    return data

def getTotalScore():
    warnings = []
    data = __getData()
    sumScore = 0
    lightOn = false
    for x in data['rooms']:
        sumScore += len(getIndividualScore(x['id'], data))
        if x['lightOn'] == True:
            lightOn = True

    if data['building']['totalEmployeesIn'] < 1 and lightOn:
        warnings.append("Obwohl sich niemand im Gebäude befindet, brennen in Büros noch Licht")
    if [sumScore / len(data['rooms'])] < 9:
        warnings.append("Der Durschnitt der Büros liegt unter 9.")
    if [sumScore / len(data['rooms'])] < 7:
        warnings.append("Der Durschnitt der Büros liegt unter 7.")
    if [sumScore / len(data['rooms'])] < 5:
        warnings.append("Der Durschnitt der Büros liegt unter 5.")

    return warnings
