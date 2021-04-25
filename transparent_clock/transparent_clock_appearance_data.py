# dictionary entries names
TC_APPEARANCE_FIELDS___NAME = "name"
TC_APPEARANCE_FIELDS___FONT_FAMILY = "font_family"
TC_APPEARANCE_FIELDS___FONT_SIZE = "font_size"
TC_APPEARANCE_FIELDS___FONT_COLOR = "font_color"
TC_APPEARANCE_FIELDS___FONT_ALPHAF = "font_alphaF"
TC_APPEARANCE_FIELDS___X_POS = "x_pos"
TC_APPEARANCE_FIELDS___Y_POS = "y_pos"


class TransparentClockAppearanceData:
    def __init__(self, name: str, font_family: str, font_size: int, font_color: str, font_alphaF: float, x_pos: int, y_pos: int):
        self.__name = name
        self.__font_family = font_family
        self.__font_size = font_size
        self.__font_color = font_color
        self.__font_alphaF = font_alphaF
        self.__x_pos = x_pos
        self.__y_pos = y_pos

    def update_with(self, other_appearance):
        self.__name = other_appearance.name
        self.__font_family = other_appearance.font_family
        self.__font_size = other_appearance.font_size
        self.__font_color = other_appearance.font_color
        self.__font_alphaF = other_appearance.font_alphaF
        self.__x_pos = other_appearance.x_pos
        self.__y_pos = other_appearance.y_pos

    def to_dict(self) -> dict:
        appearance_dict = {}
        appearance_dict[TC_APPEARANCE_FIELDS___NAME] = self.__name
        appearance_dict[TC_APPEARANCE_FIELDS___FONT_FAMILY] = self.__font_family
        appearance_dict[TC_APPEARANCE_FIELDS___FONT_SIZE] = self.__font_size
        appearance_dict[TC_APPEARANCE_FIELDS___FONT_COLOR] = self.__font_color
        appearance_dict[TC_APPEARANCE_FIELDS___FONT_ALPHAF] = self.__font_alphaF
        appearance_dict[TC_APPEARANCE_FIELDS___X_POS] = self.__x_pos
        appearance_dict[TC_APPEARANCE_FIELDS___Y_POS] = self.__y_pos
        return appearance_dict

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name: str):
        self.__name = new_name

    @property
    def font_family(self) -> str:
        return self.__font_family

    @font_family.setter
    def font_family(self, new_font_name: str):
        self.__font_family = new_font_name

    @property
    def font_size(self) -> int:
        return self.__font_size

    @font_size.setter
    def font_size(self, new_font_size):
        self.__font_size = new_font_size

    @property
    def font_color(self) -> str:
        return self.__font_color

    @font_color.setter
    def font_color(self, new_font_color: str):
        self.__font_color = new_font_color

    @property
    def font_alphaF(self) -> float:
        return self.__font_alphaF

    @font_alphaF.setter
    def font_alphaF(self, new_font_alphaF: float):
        self.__font_alphaF = new_font_alphaF

    @property
    def x_pos(self) -> int:
        return self.__x_pos

    @x_pos.setter
    def x_pos(self, new_x_pos):
        self.__x_pos = new_x_pos

    @property
    def y_pos(self) -> int:
        return self.__y_pos

    @y_pos.setter
    def y_pos(self, new_y_pos):
        self.__y_pos = new_y_pos

    def __str__(self):
        obj_str = "Name = {}\n".format(self.__name)
        obj_str += "Font: Name = {} Size = {} Color = {} AlphaF = {}\n".format(self.__font_family, self.__font_size, self.__font_color, self.__font_alphaF)
        obj_str += "Position = ({}, {})\n".format(self.__x_pos, self.__y_pos)
        return obj_str
