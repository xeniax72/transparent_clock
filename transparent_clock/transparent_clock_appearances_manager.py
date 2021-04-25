# TODO: 1 - gestione delle eccezioni riguardanti il file json... file che non si trova... file in formato errato... ecc.


import json

from transparent_clock_appearance_data import *


# globals constants
TC_APPEARANCES_MANAGER___DICT_NAME = "transparent_clock_appearances"


class TransparentClockAppearancesManager:
    def __init__(self, appearances_file_path_name: str):
        self.__appearances_file_path_name = appearances_file_path_name
        self.__appearances_list = []
        self.load_appearances()

    def load_appearances(self) -> None:
        with open(self.__appearances_file_path_name) as json_file:
            appearances_dict = json.load(json_file)

        for appearance in appearances_dict[TC_APPEARANCES_MANAGER___DICT_NAME]:
            self.__appearances_list.append(TransparentClockAppearanceData(
                appearance[TC_APPEARANCE_FIELDS___NAME], appearance[TC_APPEARANCE_FIELDS___FONT_FAMILY],
                appearance[TC_APPEARANCE_FIELDS___FONT_SIZE], appearance[TC_APPEARANCE_FIELDS___FONT_COLOR],
                appearance[TC_APPEARANCE_FIELDS___FONT_ALPHAF],
                appearance[TC_APPEARANCE_FIELDS___X_POS], appearance[TC_APPEARANCE_FIELDS___Y_POS]
            ))

    def save_appearances(self) -> None:
        appearances_dict = {}
        appearances_dict[TC_APPEARANCES_MANAGER___DICT_NAME] = []
        for appearance in self.__appearances_list:
            appearances_dict[TC_APPEARANCES_MANAGER___DICT_NAME].append(appearance.to_dict())

        with open(self.__appearances_file_path_name, "w") as out_file:
            json.dump(appearances_dict, out_file)

    def add_appearance(self, new_conf: TransparentClockAppearanceData) -> None:
        self.__appearances_list.append(new_conf)

    def get_appearance(self, conf_name) -> TransparentClockAppearanceData:
        for conf in self.__appearances_list:
            if conf.name == conf_name:
                returned_conf = TransparentClockAppearanceData(conf.name, conf.font_family, conf.font_size, conf.font_color,
                                                               conf.font_alphaF, conf.x_pos, conf.y_pos)
                return returned_conf
        return None

    def get_appearances_names(self) -> list:
        names_list = []
        for conf in self.__appearances_list:
            names_list.append(conf.name)
        return names_list

    def update_appearance(self, new_conf: TransparentClockAppearanceData) -> None:
        for conf in self.__appearances_list:
            if conf.name == new_conf.name:
                self.__appearances_list.remove(conf)
                self.__appearances_list.append(new_conf)
                break


if __name__ == '__main__':
    conf_manager = TransparentClockAppearancesManager("../datas/transparent_clock_appearances.json")
    conf_manager.load_appearances()

    print(conf_manager.get_appearance("PyCharm"))
    conf_manager.add_appearance(TransparentClockAppearanceData("Test", "Colibri", 32, "#ff00ee", 0.32, 234, 456))
    print(conf_manager.get_appearance("Test"))
