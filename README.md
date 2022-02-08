
# Smart_cities

## Contexte
Ce projet prend place alors qu'actuellement le marché de l'électricité en France est entièrement centralisé. Effectivement, que l'on vende ou que l'on achète, on doit passer par EDF. Nous avons vu dans un article qu'il existe la possibilité de passer à un marché pair à pair afin de permettre à tous les consommateurs de gagner de l'argent sur leurs échanges.
En effet, le prix de vente étant inférieur au prix d'achat pour la main grid, un marché de pair à pair permet de trouver un compromis direct entre l'acheteur et le vendeur plus avantageux aux deux. Le but de ce projet est donc de vérifier la validité de cette théorie en modélisant un cas pratique d'application.


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
Ces données se trouveront toutes dans le fichier 'main'. 

Le premier paramètre modifiable est dans la fonction 'pretraitement(tab, pourcentage)' : le pourcentage de valeurs nulles acceptées par ligne dans les données de consommation/production des résidences. Plus le pourcentage toléré est élevé, plus le temps d'expérimentation sera long (mais les erreurs dûes à des valeurs manquantes seront également élevées). Par défaut, cette valeur est mise à 50%, permettant d'expérimenter sur 14360 heures.

Les courbes renvoyées sont alors:
- La production d'électricité de chaque prosumer en fonction du temps.
- La consommation d'électricité de chaque prosumer en fonction du temps.
- La comparaison de coût entre la situation testée et la situation témoin pour la prosumer 5.
- La comparaison de coût entre la situation testée et la situation témoin pour la prosumer 7.
- L'impact du delta sur les gains du prosumer 5 dans la situation testée. 
- L'impact du delta sur les gains du prosumer 7 dans la situation testée.


## Limites

La simplicité du modèle: on considère le delta comme prédeterminé, car sa détermination prendrait énormément de temps, mais celle-ci permettrait également une meilleure modélisation des négociations.

On ne prend pas en compte la gestion des batteries et la rétention d'électricité, partant du principe que personne ne fait des réserves.

De plus, les prix de la production d'électricité n'est pas rentable en France aujourd'hui.

