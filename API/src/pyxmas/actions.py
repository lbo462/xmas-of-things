from enum import IntEnum


class ActionsEnum(IntEnum):
    """
    Defines every possible actions in the village.
    The enum value correspond to the value read by the CTH to activate its things.
    """

    #### MERRY GO ROUND ####
    CAROUSEL_ON = 0
    CAROUSEL_OFF = 1

    #### FERRIS WHEEL ####
    FERRIS_WHEEL_ON = 10
    FERRIS_WHEEL_OFF = 11

    #### BUZZERS ####
    BUZZERS_1 = 20
    BUZZERS_2 = 21
    BUZZERS_3 = 22
    BUZZERS_OFF = 23

    #### LEDS ####
    LEDS_TREE_ON = 30
    LEDS_TREE_OFF = 31
    LEDS_VILLAGE_ON = 32
    LEDS_VILLAGE_OFF = 33

    #### LCD ####
    LCD_1 = 40
    LCD_2 = 41
    LCD_OFF = 42
    LCD_COLD = 43
    LCD_HOT = 44
