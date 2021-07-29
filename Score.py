import json

def getScore(id):
    data = __getData(id)
    room = __getRoom(data)
    sensors = room['sensors']
    print(room)
    print(sensors)

    warnings = []

    if sensors['lightOn'] and data['solarPowerOutput'] > 10:
        warnings = warnings.append("Das Licht ist angeschaltet, obwohl es Hell ist")
    if sensors['windowsOpen'] and sensors['airConditioningRunning'] :
        warnings.append("Das Fenster ist offen, obwohl die Klimaanlage angeschlatet ist")
    if sensors['windowsOpen'] and  sensors['heaterRunning']:
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


def __getRoom(data):
    for x in data['rooms']:
        if x['id'] == id:
            return x


def __getData(id):
    import urllib.request, json
    with urllib.request.urlopen("https://rvj6rnbpxj.execute-api.eu-central-1.amazonaws.com/prod/live-data") as url:
        data = json.loads(url.read().decode())
    return data
