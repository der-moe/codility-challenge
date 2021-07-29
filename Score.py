import json


def getScore(id):
    data = __getData(id)
    room = __getRoom(data)
    sensors = room['sensors']
    print(room)
    print(sensors)

    score = 6

    if sensors['lightOn']:
        score = score - 1
    if sensors['windowsOpen'] and (sensors['airConditioningRunning'] or sensors['heaterRunning']):
        score = score - 1
    if sensors['airConditioningRunning'] and sensors['heaterRunning']:
        score = score - 1
    if sensors['rollerBlindsClosed'] == False and sensors['airConditioningRunning']:
        score = score - 1

    return score


def __getRoom(data):
    for x in data['rooms']:
        if x['id'] == id:
            return x


def __getData(id):
    import urllib.request, json
    with urllib.request.urlopen("https://rvj6rnbpxj.execute-api.eu-central-1.amazonaws.com/prod/live-data") as url:
        data = json.loads(url.read().decode())
    return data
