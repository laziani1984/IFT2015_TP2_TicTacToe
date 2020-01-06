

# Classe initiale pour une pile.
class Stack:

    def __init__(self):
        self.__list = []

    def push(self, obj):
        self.__list.append(obj)

    def pop(self):
        return self.__list.pop()

    def is_empty(self):
        return len(self.__list) == 0

    def length(self):
        return len(self.__list)

    # Affiche le contenu de la pile.
    def get_data(self):
        return self.__list

    def top(self):
        return self.__list[len(self.__list)-1]
