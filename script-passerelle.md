## Debrief script (passerelle)

durée accident = 10 min



1) lire message des différents topics

compteur: 

nb_voiture_arret
nb_voiture_embouteillage
nb_voiture_brouillard
nb_voiture_travaux
nb_voiture_route_glissante

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


# Gestion brouillard

Si vehicule.cause = 7 Alors
    nb_voiture_brouillard ++ 
    afficher (brouillard en cours)

# Gestion travaux

Si vehicule.cause = 3 Alors
    nb_voiture_travaux ++ 
    afficher (travaux en cours)

# Gestion travaux

Si vehicule.cause = 6 Alors
    nb_voiture_route_glissante ++ 
    afficher (route glissante  en cours)





Un accident si l’événement est remonté par au moins 5 véhicules ;

Un embouteillage si elle prend connaissance que plusieurs véhicules roulent en dessous de la
vitesse autorisée (ici 90km/h).