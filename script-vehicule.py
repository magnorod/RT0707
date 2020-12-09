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

def gen_json_cam(stationId,stationType,vitesse,heading,latitude,longitude,timestamp):

    msg_cam = '{"stationId":'+str(stationId)+',"stationType":'+str(stationType)+',"timestamp":"'+timestamp+'","vitesse":'+str(vitesse)+',"heading":'+str(heading)+',"positionGPS":{"longitude":'+str(longitude)+',"latitude":'+str(latitude)+'}'+'}'
    return msg_cam

#endef

def gen_json_denm(stationId,stationType,cause,sub_cause,latitude,longitude,timestamp):

    msg_denm =  '{"stationId":'+str(stationId)+',"stationType":'+str(stationType)+',"timestamp":"'+timestamp+'","cause":'+str(cause)+',"sub-cause":'+str(sub_cause)+',"positionGPS":{"longitude":'+str(longitude)+',"latitude":'+str(latitude)+'}'+'}'
    return msg_denm

#endef


def gen_msg_cam(stationId,stationType,longitude,latitude,vitesse,ip_server_mqtt,timestamp):

    # génération heading
    heading = random.randint(-360,360)

   

    msg_cam = gen_json_cam(stationId,stationType,vitesse,heading,latitude,longitude,timestamp)


    # construction requête bash
    topic=""
    if stationId == 1:
        topic="auto"
    elif stationId == 2:
        topic="moto"
    else:
        topic="camion"

    cmd1="mosquitto_pub -h "+str(ip_server_mqtt)+" -q 1 "+"-u "+str(stationId)+" -t cam/"+str(topic)+" -m '"+str(msg_cam)+"'" 
    os.system(cmd1)
    print("\n")

    return msg_cam

#endef

def gen_msg_denm(stationId,stationType,longitude,latitude,vitesse,ip_server_mqtt,timestamp):

    # génération cause
    cause_tab=(3,4,5,6,7)

    # TOUTES CES VERIF DOIVENT ETRE EFFECTUEES PAR LA PASSEREL

   

   
    if stationType == 15 :
        cause=4
        print("accident ! ")


   

    """

    compteur exemple:
    
    cmpt=0
    si stationId=3 (camion) alors
        cmpt++
    
    Si cmpt ==5 Alors
        envoyer msd denm(accident)




    Véhicules:
    envoyer 3 msg denm avec vitesse <= 30 km avec cause 5 (embouteillage)


    Traitement sur la passerelle:
    si 3 vitesses de 3 véhicules <= 30 km  en moins de 2 min alors 
    
    
    Véhicules:
    envoyer 2 msg denm avec cause 3 

    Traitement sur la passerelle 
    accident si 2 véhicules remonte l'information "accident" en moins de 10 min

    

    Véhicules:
    envoyer 1 msg denm avec stationType = 15 et cause = 4

    Traitement sur la passerelle:
    si opérateur signale accident alors il y a bien un accident 

    """

    # accident si opérateur routier et vitesse <= 30
    elif stationType == 15 and vitesse <= 30:
        # embouteillage
        cause=5
        print("embouteillage ! ")
    else: 
        # génération aléatoire d'une cause
        choix_cause=random.randint(0,len(cause_tab)-1)
        cause=cause_tab[choix_cause]

    # si opérateur routier  





    # détection cause route glissante sur 5 min 



    # détection cause brouillard




    # génération sub-cause
    sub_cause=random.randint(1,10)

    msg_denm=gen_json_denm(stationId,stationType,cause,sub_cause,latitude,longitude,timestamp)

    # construction requête 
    topic=""
    if stationId == 1:
        topic="auto"
    elif stationId == 2:
        topic="moto"
    else:
        topic="camion"
    #endif

    cmd1="mosquitto_pub -h "+str(ip_server_mqtt)+" -q 1 "+"-u "+str(stationId)+" -t cam/"+str(topic)+" -m '"+str(msg_cam)+"'"

    return msg_denm
#endef 



if __name__ == '__main__' :
  
    stationId=gen_stationId()
    stationType_tab=(5,10,15)
    ip_server_mqtt="10.22.135.34"
    frequence_cam=0

    longitude_base= 4.0333
    latitude_base=49.25

    cmpt_tour_boucle=0

    variation_degre_1km_longitude= 0.01
    variation_degre_1km_latitude= 0.008

    while True :

        # génération stationType
        choix_stationType=random.randint(0,len(stationType_tab)-1)
        stationType=stationType_tab[choix_stationType]

        # génération vitesse

        if stationId == 2 :
            vitesse = random.randint(90,130)
        elif stationId == 3:
            vitesse = random.randint(0,90)
        else:
            vitesse = random.randint(0,130)
        #endif

        if vitesse < 90 :
            frequence_cam=1 # 1sec
        else:
            frequence_cam=0.100 #0,1
        #endif





        distance_parcourue=((vitesse/3.6)*frequence_cam)/1000

        # génération longitude 
        longitude=longitude_base+(distance_parcourue*variation_degre_1km_longitude)

        # génération latitude
        latitude=latitude_base+(distance_parcourue*variation_degre_1km_latitude)

         # génération du timestamp
        seconds=time.time()
        timestamp=str(time.ctime(seconds))

        # génération msg cam
        msg_cam = gen_msg_cam(stationId,stationType,longitude,latitude,vitesse,ip_server_mqtt,timestamp)

        # envoi d'un message denm à une fréquence de 1/10 de la fréquence d'envoi des msg CAM
        if cmpt_tour_boucle == 10:
            print("####DENM\n")
            msg_denm = gen_msg_denm(stationId,stationType,longitude,latitude,vitesse,ip_server_mqtt,timestamp)
            cmpt_tour_boucle=0
        #endif

        print("envoi à une fréquence de "+str(frequence_cam))
        print(msg_cam)
        cmpt_tour_boucle+=1
        time.sleep(frequence_cam)
    #end

   
    
    



    
