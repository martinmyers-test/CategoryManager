from typing import List, Dict


def read_token() -> int:
    return PseudoDatabase.token


class PseudoDatabase:
    class DatabaseLockedForWrite(Exception):
        pass

    class ItemInCategory(Exception):
        pass

    class UnknownCategory(Exception):
        pass

    class ItemNotFound(Exception):
        pass

    class IncorrectPassword(Exception):
        pass

    class Item:
        def __init__(self, label: str):
            self.label = label

    database = {}
    locked = False
    token = 1

    def __init__(self, load_from_store: bool = False):
        if load_from_store:
            self._load()

    def _contains(self, category: str, label: str) -> bool:
        for item in self.database[category]:
            if item.label == label:
                return True
        return False

    def _lock(self):
        if PseudoDatabase.locked:
            raise self.DatabaseLockedForWrite
        else:
            PseudoDatabase.locked = True

    def _load(self):
        # would take the data from persistent storage and load it into "database" class variable
        pass

    def _commit(self):
        # would update persistent data with transaction and then perform the following
        PseudoDatabase.locked = False
        PseudoDatabase.token += 1

    def create(self, category: str, item: Item):
        self._lock()
        if category in PseudoDatabase.database.keys():
            if self._contains(category, item.label):
                PseudoDatabase.locked = False
                raise self.ItemInCategory
        else:
            PseudoDatabase.database[category] = []
        PseudoDatabase.database[category].append(item)
        self._commit()

    def read(self, category: str, label: str) -> Item:
        try:
            for item in PseudoDatabase.database[category]:
                if item.label == label:
                    return item
            raise self.ItemNotFound
        except KeyError:
            raise self.UnknownCategory

    def read_category(self, category: str) -> List[Item]:
        try:
            return PseudoDatabase.database[category]
        except KeyError:
            raise self.UnknownCategory

    def read_all(self) -> Dict[str, List[Item]]:
        return PseudoDatabase.database

    def add(self, category: str, item: Item):
        self._lock()
        if category not in PseudoDatabase.database.keys():
            PseudoDatabase.database[category] = []
        else:
            if self._contains(category, item.label):
                PseudoDatabase.locked = False
                raise self.ItemInCategory
        PseudoDatabase.database[category].append(item)
        self._commit()

    def delete(self, category: str, label: str):
        try:
            self._lock()
            for item in PseudoDatabase.database[category]:
                if item.label == label:
                    PseudoDatabase.database[category].remove(item)
                    if not PseudoDatabase.database[category]:
                        del PseudoDatabase.database[category]
                    self._commit()
                    return
            PseudoDatabase.locked = False
            raise self.ItemNotFound
        except KeyError:
            PseudoDatabase.locked = False
            raise self.UnknownCategory

    def reset(self, password: str):
        if password == "admin":
            self._lock()
            PseudoDatabase.database = {}
            PseudoDatabase.locked = False
            PseudoDatabase.token = 0
            self._commit()
        else:
            raise self.IncorrectPassword
