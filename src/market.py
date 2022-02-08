class market:
    def __init__(self, liste_participants,delta_vendeur,prix_achat_maingrid, prix_vente_maingrid):
        self.liste_participants = liste_participants
        self.dictionnaire_vente = {}
        self.total_vente = 0
        self.delta_vendeur = delta_vendeur
        self.main_grid_price = {'buyer': prix_achat_maingrid, 'seller': prix_vente_maingrid}

        self.dictionnaire_proportion_acheteurs = {}
        self.dictionnaire_proportion_vendeurs = {}
        self.dictionnaire_already_hors_market = {}

    def resolve(self):
        acheteurs = []
        vendeurs = []
        hors_marche = []

        for personne in self.liste_participants:
            if personne.balance < 0:
                acheteurs.append(personne)
                self.dictionnaire_proportion_acheteurs[str(personne.id)] = (-1)*personne.balance
            if personne.balance > 0:
                vendeurs.append(personne)
                self.dictionnaire_proportion_vendeurs[str(personne.id)] = personne.balance
            if personne.balance == 0:
                hors_marche.append(personne)
                self.dictionnaire_already_hors_market[str(personne.id)] = personne.balance
        id_transaction = 0


        # On cherche à mettre en place des échanges
        for vendeur in vendeurs:
            for acheteur in acheteurs:
                # Transaction entre le vendeur et l'acheteur
                besoin_acheteur = acheteur.balance
                surplus_vendeur = vendeur.balance
                if besoin_acheteur < surplus_vendeur:
                    # L'acheteur achète tout ce qu'il veut
                    prix_acheteur = self.main_grid_price['buyer'] - (self.main_grid_price['buyer']-self.main_grid_price['seller']) * (1-self.delta_vendeur)
                    transaction_amount = besoin_acheteur * prix_acheteur *(-1)
                    transaction = {'seller': vendeur.id, 'buyer':acheteur.id, 'amount':transaction_amount }
                    self.dictionnaire_vente[str(id_transaction)] = transaction
                    id_transaction += 1
                    # Mise a jour des besoins
                    # L'acheteur n'a plus de besoin et sort du marché
                    acheteur.balance= 0
                    acheteurs.remove(acheteur)
                    hors_marche.append(acheteur)
                    # Les signes des besoins sont opposés
                    vendeur.balance = surplus_vendeur + besoin_acheteur

                if besoin_acheteur >= surplus_vendeur:
                    # Le vendeur vends tout son stock
                    prix_acheteur = self.main_grid_price['buyer'] - (self.main_grid_price['buyer']-self.main_grid_price['seller']) * (1-self.delta_vendeur)
                    transaction_amount = surplus_vendeur * prix_acheteur
                    transaction = {'seller': vendeur.id, 'buyer': acheteur.id, 'amount': transaction_amount}
                    self.dictionnaire_vente[str(id_transaction)] = transaction
                    id_transaction += 1
                    # Mise a jour des besoins
                    vendeur.balance = 0
                    vendeurs.remove(vendeur)
                    hors_marche.append(vendeur)
                    # Les signes des besoins sont opposés
                    acheteur.balance = besoin_acheteur + surplus_vendeur

                    if besoin_acheteur == surplus_vendeur:
                        # On traite le cas d'égalité :
                        acheteurs.remove(acheteur)
                        hors_marche.append(acheteur)

        # Sortie de la boucle for, les personnes restantes n'ont pas trouvé d'accord et achetent/revende à la main_grid
        for acheteur in acheteurs:
            prix_achat = self.main_grid_price['buyer']
            transaction_amount = acheteur.balance * prix_achat * (-1)
            transaction = {'seller': 'main_grid', 'buyer': acheteur.id, 'amount': transaction_amount}
            self.dictionnaire_vente[str(id_transaction)] = transaction
            id_transaction += 1
            acheteur.balance = 0
            acheteurs.remove(acheteur)
            hors_marche.append(acheteur)

        for vendeur in vendeurs:
            prix_vendeur = self.main_grid_price['seller']
            transaction_amount = vendeur.balance * prix_vendeur
            transaction = {'seller': vendeur.id, 'buyer': 'main_grid', 'amount': transaction_amount}
            self.dictionnaire_vente[str(id_transaction)] = transaction
            id_transaction += 1
            vendeur.balance = 0
            vendeurs.remove(vendeur)
            hors_marche.append(vendeur)

    def getDictionnaireGain(self):
        total_vendu = 0.0
        total_achete = 0.0
        # On va avoir besoin du gain total du marché par rapport à maingrid
        for transaction_id in self.dictionnaire_vente.keys():
            transaction = self.dictionnaire_vente[transaction_id]
            if transaction['seller'] == 'main_grid' or transaction['buyer']=='main_grid':
                # Cas d'une vente ou d'un achat vers main_grid
                if transaction['seller'] == 'main_grid':
                    total_achete += transaction['amount']
                if transaction['buyer'] == 'main_grid':
                    total_vendu += transaction['amount']
            else:
                # Cas d'une vente directe entre particulier
                # On incremente le total vendu hors main_grid
                total_vendu += transaction['amount']
                total_achete += transaction['amount']

        dictionnaire_gain = {}

        # On calcule le besoin total
        total_besoin = 0.0
        for id_acheteur in self.dictionnaire_proportion_acheteurs:
            total_besoin += self.dictionnaire_proportion_acheteurs[id_acheteur]

        total_surplus = 0.0
        for id_vendeur in self.dictionnaire_proportion_vendeurs:
            total_surplus += self.dictionnaire_proportion_vendeurs[id_vendeur]

        # On commence par les acheteurs
        for id_acheteur in self.dictionnaire_proportion_acheteurs:
            dictionnaire_gain[id_acheteur] = self.dictionnaire_proportion_acheteurs[id_acheteur]/total_besoin * total_achete
        for id_vendeur in self.dictionnaire_proportion_vendeurs:
            dictionnaire_gain[id_vendeur] = self.dictionnaire_proportion_vendeurs[id_vendeur]/total_surplus * total_vendu
        for id_hors_market in self.dictionnaire_already_hors_market:
            # Normalement c'est 0 donc ca devrait pas poser de problème
            dictionnaire_gain[id_hors_market] = self.dictionnaire_already_hors_market[id_hors_market]
        return dictionnaire_gain

