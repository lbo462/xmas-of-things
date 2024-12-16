from dataclasses import dataclass


@dataclass
class VillageState:
    """
    Keep track of the state of the village.
    """

    #### mary_go_on ####
    mary_go_on_on :bool = False
    #### ferris_wheel ####
    ferris_wheel_on :bool = False
    #### buzzers ####
    buzzers_1 :bool = False
    buzzers_2 :bool = False
    buzzers_3 :bool = False
    #### leds ####
    leds_tree_on :bool = False
    leds_village_on :bool = False
    #### lcd ####
    lcd_1 :bool = False
    lcd_2 :bool = False