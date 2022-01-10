class ModalTitleType():
    @staticmethod
    def get_description(val):
        ret = ["購買土地",
               "付出金錢",
               "獲得獎勵",
               "暫停回合",
               "建造房屋",
               "",
               "",
               "",
               "錢不夠了",
               "公園"]
        return ret[val]