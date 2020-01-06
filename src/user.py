class CNDBUser:
    def __init__ (self):
        self.properties: list = [
            "id",
            "balance",
            "xp",
            "last_daily",
            "daily_streak",
            "cookies_sent",
            "cookies_got",
            "thefts_failed",
        ]
        self.data: dict = {
            "id":None,
            "balance":None,
            "xp":None,
            "last_daily":None,
            "daily_streak":None,
            "cookies_sent":None,
            "cookies_got":None,
            "thefts_failed":None,
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