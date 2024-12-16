from dataclasses import dataclass

from .actions import ActionsEnum


@dataclass
class VillageState:
    """
    Keep track of the state of the village.
    """

    #### Merry go round, aka carousel ####
    carousel_on: bool = False

    #### Ferris wheel ####
    ferris_wheel_on: bool = False

    #### Buzzers (xmas music) ####
    buzzers_1: bool = False
    buzzers_2: bool = False
    buzzers_3: bool = False

    #### LEDs ####
    leds_tree_on: bool = False
    leds_village_on: bool = False

    #### LCD messages ####
    lcd_1: bool = False
    lcd_2: bool = False
    lcd_cold: bool = False
    lcd_hot: bool = False


def update_state(action: ActionsEnum, state: VillageState) -> None:
    """
    Updates the state of the village, regarding the action to do.

    :param action: The action done, or to be done
    :param state: The village state that will be mutated
    :return: None. The state is mutated, nothing is returned.
    """

    # Carousel
    if action is ActionsEnum.CAROUSEL_ON:
        state.carousel_on = True
    elif action is ActionsEnum.CAROUSEL_OFF:
        state.carousel_on = False

    # Ferris wheel
    elif action is ActionsEnum.FERRIS_WHEEL_ON:
        state.carousel_on = True
    elif action is ActionsEnum.FERRIS_WHEEL_OFF:
        state.carousel_on = False

    # Buzzers
    elif action is ActionsEnum.BUZZERS_1:
        state.buzzers_1 = True
        state.buzzers_2 = False
        state.buzzers_3 = False
    elif action is ActionsEnum.BUZZERS_2:
        state.buzzers_1 = False
        state.buzzers_2 = True
        state.buzzers_3 = False
    elif action is ActionsEnum.BUZZERS_3:
        state.buzzers_1 = False
        state.buzzers_2 = False
        state.buzzers_3 = True
    elif action is ActionsEnum.BUZZERS_OFF:
        state.buzzers_1 = False
        state.buzzers_2 = False
        state.buzzers_3 = False

    # LEDs
    elif action is ActionsEnum.LEDS_TREE_ON:
        state.leds_tree_on = True
    elif action is ActionsEnum.LEDS_TREE_OFF:
        state.leds_tree_on = False
    elif action is ActionsEnum.LEDS_VILLAGE_ON:
        state.leds_village_on = True
    elif action is ActionsEnum.LEDS_VILLAGE_OFF:
        state.leds_village_on = False

    # LCD
    elif action is ActionsEnum.LCD_1:
        state.lcd_1 = True
        state.lcd_2 = False
        state.lcd_cold = False
        state.lcd_hot = False
    elif action is ActionsEnum.LCD_2:
        state.lcd_1 = False
        state.lcd_2 = True
        state.lcd_cold = False
        state.lcd_hot = False
    elif action is ActionsEnum.LCD_COLD:
        state.lcd_1 = False
        state.lcd_2 = False
        state.lcd_cold = True
        state.lcd_hot = False
    elif action is ActionsEnum.LCD_HOT:
        state.lcd_1 = False
        state.lcd_2 = False
        state.lcd_cold = False
        state.lcd_hot = True
    elif action is ActionsEnum.LCD_OFF:
        state.lcd_1 = False
        state.lcd_2 = False
        state.lcd_cold = False
        state.lcd_hot = False
