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
            "inv",
            "trade_requests",
        ]
        self.data: dict = {
            "id": None,
            "balance": None,
            "xp": None,
            "level": None,
            "last_daily": None,
            "daily_streak": None,
            "cookies_sent": None,
            "cookies_got": None,
            "thefts_failed": None,
            "rpg_attack":None,
            "rpg_defense":None,
            "rpg_luck":None,
            "weapon":None,
            "armor":None,
            "inv":None,
            "trade_requests":None,
        }

    def getall(self) -> dict:
        return self.data

    def getprop(self, property: str):
        if property not in self.properties:
            print("CNDBUser :: NoSuchProperty Error -> {}".format(property))
            return None
        return self.data[property]

    def setall(self, data: dict) -> None:
        self.data = data

    def setprop(self, property: str, value: str) -> None:
        if property not in self.properties:
            print("CNDBUser :: NoSuchProperty Error -> {}".format(property))
            return
        self.data[property] = value

    def empty(self) -> bool:
        for key in self.data:
            if self.data[key] != None:
                return False
        return True
