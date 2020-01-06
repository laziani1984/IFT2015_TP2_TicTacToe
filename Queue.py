

# Classe initiale pour un Queue.
class Queue:

    # constructeur
    def __init__(self):
        self._A = []

    # retourne le nombre d'éléments
    def __len__(self):
        return len(self._A)

    # produit une chaîne de caractères:
    # les éléments entre crochets
    # séparés par des virgules
    # taille et capacité de la structure de données
    # indiquées lorsque pertinent
    def __str__(self):
        return str(self._A)

    # indique s'il y a des éléments
    # dans la Queue
    def is_empty(self):
        return self._A == []

    # ajoute un élément à la fin de la Queue
    def enqueue(self, element):
        self._A.insert(0, element)

    # retire le prochain élément de la Queue
    def dequeue(self):
        return self._A.pop()

    # Enlève le dernier élément de la Queue.
    def remove_last(self):
        self._A.remove(self._A[0])

    # retourne le premier élément
    # en Queue sans le retirer.
    def first(self):
        return self._A[0]

    def get_element(self, elem):
        return self._A[elem]