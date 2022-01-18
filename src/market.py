class market:
    def __init__(self, liste_participants,delta_vendeur, heure,prix_achat_maingrid, prix_vente_maingrid, nombre_iteration):
        self.liste_participants = liste_participants
        self.heure = heure
        self.nombre_iteration = nombre_iteration
        self.dictionnaire_vente = {}
        self.total_vente = 0
        self.delta_vendeur = delta_vendeur
        self.main_grid_price = {'buyer': prix_achat_maingrid, 'seller': prix_vente_maingrid}

    def resolve(self):
        acheteurs = []
        vendeurs = []
        hors_marche = []

        for personne in self.liste_participants:
            if personne.balance < 0:
                acheteurs.append(personne)
            if personne.balance > 0:
                vendeurs.append(personne)
            if personne.balance == 0:
                hors_marche.append(personne)
        id_transaction = 0

        for numero_iteration in range(self.nombre_iteration):
            # Calcul du besoin total lors de l'itération
            besoin_total = 0
            for personne in acheteurs:
                besoin_total += personne.balance
            # Calcul du surplus total disponible
            surplus_total = 0
            for personne in vendeurs:
                surplus_total -= personne.balance
            surplus_total = abs(surplus_total)

            # On cherche à mettre en place des échanges
            for vendeur in vendeurs:
                for acheteur in acheteurs:
                    # Transaction entre le vendeur et l'acheteur
                    besoin_acheteur = acheteur.besoin
                    surplus_vendeur = vendeur.besoin
                    if besoin_acheteur < surplus_vendeur:
                        # L'acheteur achète tout ce qu'il veut
                        prix_acheteur = self.main_grid_price['buyer'] * (1-self.delta_vendeur)
                        transaction_amount = besoin_acheteur * prix_acheteur *(-1)
                        transaction = {'seller': vendeur.id, 'buyer':acheteur.id, 'amount':transaction_amount }
                        self.dictionnaire_vente[str(id_transaction)] = transaction
                        id_transaction += 1
                        # Mise a jour des besoins
                        # L'acheteur n'a plus de besoin et sort du marché
                        acheteur.besoin = 0
                        acheteurs.remove(acheteur)
                        hors_marche.append(acheteur)
                        # Les signes des besoins sont opposés
                        vendeur.besoin = surplus_vendeur + besoin_acheteur

                    if besoin_acheteur >= surplus_vendeur:
                        # Le vendeur vends tout son stock
                        prix_acheteur = self.main_grid_price['buyer'] * (1-self.delta_vendeur)
                        transaction_amount = surplus_vendeur * prix_acheteur
                        transaction = {'seller': vendeur.id, 'buyer': acheteur.id, 'amount': transaction_amount}
                        self.dictionnaire_vente[str(id_transaction)] = transaction
                        id_transaction += 1
                        # Mise a jour des besoins
                        vendeur.besoin = 0
                        vendeurs.remove(vendeur)
                        hors_marche.append(vendeur)
                        # Les signes des besoins sont opposés
                        acheteur.besoin = besoin_acheteur + surplus_vendeur

                        if besoin_acheteur == surplus_vendeur:
                            # On traite le cas d'égalité :
                            acheteurs.remove(acheteur)
                            hors_marche.append(acheteur)

        # Sortie de la boucle for, les personnes restantes n'ont pas trouvé d'accord et achetent/revende à la main_grid
        for acheteur in acheteurs:
            prix_achat = self.main_grid_price['buyer']
            transaction_amount = acheteur.besoin * prix_achat * (-1)
            transaction = {'seller': 'main_grid', 'buyer': acheteur.id, 'amount': transaction_amount}
            self.dictionnaire_vente[str(id_transaction)] = transaction
            id_transaction += 1
            acheteur.besoin = 0
            acheteurs.remove(acheteur)
            hors_marche.append(acheteur)

        for vendeur in vendeurs:
            prix_vendeur = self.main_grid_price['seller']
            transaction_amount = vendeur.besoin * prix_vendeur
            transaction = {'seller': vendeur.id, 'buyer': 'main_grid', 'amount': transaction_amount}
            self.dictionnaire_vente[str(id_transaction)] = transaction
            id_transaction += 1
            vendeur.besoin = 0
            vendeurs.remove(vendeur)
            hors_marche.append(vendeur)

    def getListeGain(self):
