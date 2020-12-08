## Debrief script (passerelle)

durée accident = 10 min



1) lire message des différents topics

compteur: 

nb_voiture_arret
nb_voiture_embouteillage

while true:


lire (vehicule.flux)

# Gestion accident
# Précision; Si deux véhicules sont à la suite = 0 
# dans un interval de 10 min/600 s


Si vehicule.vitesse == 0 Alors
    nb_voiture_arret ++

    SI nb_voiture_arret == 2 ALors
       envoyer(evenement_accident)

FinSi


# Gestion embouteillage 
# Précision Si 3 véhicules sont à la suite <=30 
# dans un interval de 2 min/120 s
SI vehicule.vitesse <= 30 Alors
    nb_voiture_embouteillage ++

    Si nb_voiture_embouteillage == 3 Alors
        envoyer(evenement_embouteillage)
FinSi





Un accident si l’événement est remonté par au moins 5 véhicules ;

Un embouteillage si elle prend connaissance que plusieurs véhicules roulent en dessous de la
vitesse autorisée (ici 90km/h).