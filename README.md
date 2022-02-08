# Smart_cities

## Contexte

## Organisation du projet
### Dossier src 
Le projet est lancé avec le fichier 'main', où sont trouvés tous les paramètres modifiables pour visualiser des courbes différentes en fonction des contextes.

Le fichier 'pretraitement' contient l'ensemble des fonctions permettant de passer d'un fichier .csv à des données utilisables dans le projet.

Le fichier 'prosumers' définie la classe des prosumers (résidences consommant et produisant de l'électricité), et permet le calcul de la situation témoin, à savoir lorsque les prosumers ne peuvent échanger qu'avec la maingrid.

Le fichier 'market' définie la classe market (marché où les prosumers peuvent négocier les prix d'échange d'électricité), et permet le calcul de la situation testée, à savoir lorsque les prosumers peuvent échanger entre eux en plus de pouvoir échanger avec la maingrid, avec choix de paramètres ayant un impact sur le test.

Le fichier 'graph' renferme l'ensemble des fonctions de visualisation de différentes données: celles de la situation de départ, et la comparaison des résultats de la situation témoin avec ceux de la situation testée.

On trouve aussi plusieurs fichiers de test, qui ont été utilisés pour vérifier le bon fonctionnement des fonctions.

### Dossier data/household_data
On y trouve plusieurs ensembles de données qui ont été utilisées au cours du projet, notamment pour tester le prétraitement et son bon fonctionnement.  Copie.csv et household_data_60min_singleindex.csv sont ceux que l'on utilise pour les tests de situations.

## Données à manipuler

