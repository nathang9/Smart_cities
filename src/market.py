class market:
    def __init__(self, liste_participants, heure, nombre_iteration):
        self.liste_participants = liste_participants
        self.heure = heure
        self.nombre_iteration = nombre_iteration
        self.dictionnaire_vente = {}

    def resolve(self):
        acheteurs = []
        vendeurs = []
        hors_marche = []

        for personne in self.liste_participants:
            if personne.balance > 0:
                acheteurs.append(personne)
            if personne.balance < 0:
                vendeurs.append(personne)
            if personne.balance == 0:
                hors_marche.append(personne)
        while self.nombre_iteration  > 0:
            # Calcul du besoin total lors de l'itération
            besoin_total = 0
            for personne in acheteurs:
                besoin_total += personne.balance
            # Calcul du surplus total disponible
            surplus_total = 0
            for personne in vendeurs:
                surplus_total -= personne.balance
            surplus_total = abs(surplus_total)
            # Calcul des delta de l'itération k
            for personne in acheteurs:
                personne.compute_delta(besoin_total,surplus_total, self.nombre_iteration)
            for personne in vendeurs:
                personne.compute_delta(besoin_total,surplus_total, self.nombre_iteration)

            # On cherche à mettre en place des
            for vendeur in vendeurs:
                for acheteur in acheteurs:
                    pass

            self.nombre_iteration -=1