#!/usr/bin/python3

import random
import time
import os
import subprocess



# initialisation graine random
random.seed()

def gen_stationId():

     # récupération hostname (auto,moto,camion)
    hostname = subprocess.check_output(['hostname'])
    hostname=hostname.decode()
    hostname=str(hostname)

    # corrélation entre le hostname et le stationId
    if "auto" in hostname :
        stationId=1
    elif "moto" in hostname :
        stationId=2
    else: 
        # camion
        stationId=3
    #endif

    return stationId
#endef

def gen_json_cam(stationId,stationType,vitesse,heading,latitude,longitude):

    msg_cam = '{"stationId":'+str(stationId)+',"stationType":'+str(stationType)+',"vitesse":'+str(vitesse)+',"heading":'+str(heading)+',"positionGPS":{"longitude":'+str(longitude)+',"latitude":'+str(latitude)+'}'+'}'
    return msg_cam

#endef

def gen_json_denm(stationId,stationType,cause,sub_cause,latitude,longitude):

    msg_denm =  '{"stationId":'+str(stationId)+',"stationType":'+str(stationType)+',"cause":'+str(cause)+',"sub-cause":'+str(sub_cause)+',"positionGPS":{"longitude":'+str(longitude)+',"latitude":'+str(latitude)+'}'+'}'
    return msg_denm

#endef


def gen_msg_cam(stationId,stationType,longitude,latitude,vitesse,ip_server_mqtt):

    # génération heading
    heading = random.randint(-360,360)

    msg_cam = gen_json_cam(stationId,stationType,vitesse,heading,latitude,longitude)


    # construction requête bash

    cmd1="mosquitto_pub -h "+str(ip_server_mqtt)+" -q 1 "+"-u "+str(stationId)+" -t topic/"+str(stationId)+"/cam "+" -m '"+str(msg_cam)+"'" 

    #10.22.135.64 -q 1 -u auto -t topic/auto/cam -m '{"stationId": 1,"stationType":[5,10,15],"vitesse":100.00,"heading": "test ","positionGPS": "48.8566969,2.3514616"}'


    os.system(cmd1)
    print("\n")

    return msg_cam

#endef

def gen_msg_denm(stationId,stationType,longitude,latitude,vitesse,ip_server_mqtt):

    # génération cause
    cause_tab=(3,4,5,6,7)

    # accident si opérateur routier et vitesse 0
    if stationType == 15 and vitesse == 0 :
        cause=4
        print("accident ! ")

    # accident si opérateur routier et vitesse <= 30
    elif stationType == 15 and vitesse <= 30:
        # embouteillage
        cause=5
        print("embouteillage ! ")
    else: 
        # génération aléatoire d'une cause
        choix_cause=random.randint(0,len(cause_tab)-1)
        cause=cause_tab[choix_cause]

    # génération sub-cause
    sub_cause=random.randint(1,10)

    msg_denm=gen_json_denm(stationId,stationType,cause,sub_cause,latitude,longitude)

    return msg_denm
#endef 



if __name__ == '__main__' :


   
    stationId=gen_stationId()
    stationType_tab=(5,10,15)
    ip_server_mqtt="10.22.135.34"
    frequence=0

    while True :

        # génération stationType
        choix_stationType=random.randint(0,len(stationType_tab)-1)
        stationType=stationType_tab[choix_stationType]

        # génération longitude
        longitude=random.uniform(0,100)

        # génération latitude
        latitude=random.uniform(0,100)

        # génération vitesse

        if stationId == 2 :
            vitesse = random.randint(90,130)
        elif stationId == 3:
            vitesse = random.randint(0,90)
        else:
            vitesse = random.randint(0,130)
        #endif

        if vitesse < 90 :
            frequence=1
        else:
            frequence=0.100
        #endif

        # génération msg cam
        msg_cam = gen_msg_cam(stationId,stationType,longitude,latitude,vitesse,ip_server_mqtt)
        msg_denm = gen_msg_denm(stationId,stationType,longitude,latitude,vitesse,ip_server_mqtt)
    
        print("envoi à une fréquence de "+str(frequence))
        print(msg_cam)
        time.sleep(frequence)
    #end

   
    
    



    
