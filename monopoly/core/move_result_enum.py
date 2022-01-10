class MoveResultType(object):
    BUY_LAND_OPTION = 0
    PAYMENT = 1
    REWARD = 2
    STOP_ROUND = 3
    CONSTRUCTION_OPTION = 4
    NOTHING = 5
    USER_DEFINE = 6
    CHANCE_CARD = 7
    IS_NOT_AFFORDABLE = 8
    PARK = 9

    @staticmethod
    def get_description(val):
        ret = ["正在選擇要不要購買",
               "",
               "",
               "進監獄了",
               "正在選擇要不要建造房屋 ",
               "",
               "",
               "",
               "買不起這塊地了",
               "在公園休息"]
        return ret[val]
