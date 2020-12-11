
 
#################### évènements à remonter à la passerelle

## tout évènement provenant d'un opérateur routier 
if stationType == 15:   
    remonter info à passerelle
#endif

# prise en compte des accidents
cmpt_signalement_accident=0
latitude_accident=0
longitude_accident=0
tab_timestamp_accident=[]


##  vérifie si 2 véhicules standard ont signalé un accident durant les 10 dernières minutes
elif stationType != 15 and cause == 4:

    # ajout du timestamp du véhicule 
    tab_timestamp_accident.append(timestamp)

    # ajout de la position de l'accident signalé 
    if cmpt_signalement_accident == 0:
        latitude_accident=latitude
        longitude_accident=longitude
    #endif

    
    

    difference_timestamp=(nouveau_timestamp) -(tab_timestamp_accident[0])

    if (difference_timestamp  <! 600 ) # < à 10 minutes

        #prise en compte du signalement
        cmpt_signalement_accident+=1
        tab_timestamp_accident.append(timestamp)


    # il ya bien un accident 
    if cmpt_signalement_accident == 2:
        cmpt_signalement_accident=0
        
        
        tab_timestamp_accident.pop(0)
        tab_timestamp_accident.pop(1)

        envoyer msg au centralisateur
    #endif

#endif

# prise en compte des embouteillages
cmpt_signalement_embouteillage=0
latitude_embouteillage=0
longitude_embouteillage=0
tab_timestamp_embouteillage=[]


elif stationType != 15 and cause == 5:

    # ajout du timestamp du véhicule 
    tab_timestamp_embouteillage.append(timestamp)









    

    