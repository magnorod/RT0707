## Debrief script (véhicule)

1) générer un message CAM sous forme json:

message CAM

{
    "stationId": random(1,2,3)
    "stationType": random(5,10,15)

    SI stationId != 3 ALORS
        "vitesse": random(0,130)
    Sinon
        "vitesse": random(0,90)
    "heading":random(-360,360)
    "positionGPS":[
      "longitude": random(0,100)   val réelle
      "latitude": random (0,100)   val réelle
    ]
}

2) génération du message DENM en fonction du message CAM

message DENM

{
    

    "stationId": messageCAM.stationId
    "stationType": messageCAM.station
    SI stationType == 15 && que messageCAM.vitesse == 0 Alors
        #accident
        cause=4

    SI stationType = 15 && vitesse <= 30
        #embouteillage
        cause=5

    "cause": random(3,4,5,6,7)
    "sub-cause": random(1-10)
    "positionGPS":[
    "longitude": messageCAM.longitude
    "latitude":  messageCAM.latitude
    ]
}

3) modification de la fréquence d'envoi

Si messageCAM.vitesse <= 90 Alors
    frequenceEnvoi= 1 (seconde)
Sinon
    frequenceEnvoi = 0.1













