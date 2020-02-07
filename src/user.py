class CNDBUser:
    def __init__(self):
        self.properties: list = [
            "id",
            "balance",
            "xp",
            "level",
            "last_daily",
            "daily_streak",
            "cookies_sent",
            "cookies_got",
            "thefts_failed",
            "rpg_attack",
            "rpg_defense",
            "rpg_luck",
            "weapon",
            "armor",
            "ring",
            "neck",
            "accessory",
            "inv",
            "trade_requests",
            "origin",
            "evocation",
            "blessing",
            "materials",
        ]
        self.data: dict = {}
        for prop in self.properties: self.data[prop] = None

    def getall(self) -> dict:
        return self.data

    def getprop(self, prop: str):
        if prop not in self.properties:
            print("CNDBUser :: NoSuchProperty Error -> {}".format(prop))
            return None
        return self.data[prop]

    def setall(self, data: dict) -> None:
        self.data = data

    def setprop(self, prop: str, value: str) -> None:
        if prop not in self.properties:
            print("CNDBUser :: NoSuchProperty Error -> {}".format(prop))
            return
        self.data[prop] = value

    def empty(self) -> bool:
        for prop in self.data:
            if self.data[prop] != None:
                return False
        return True
