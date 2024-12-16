from dataclasses import dataclass


@dataclass
class VillageState:
    """
    Keep track of the state of the village.
    """

    ### LEDs

    tree_led_on: bool = False
    tree_star_on: bool = False
    village_leds_on: bool = False
    santa_track_on: bool = True


    ### Snow spray

    snow_spray: bool = False

    ### Songs

    music_off: bool = False
    music_1_on: bool = False
    music_2_on: bool = False
    music_3_on: bool = True

    ### Messages

    no_message_displayed: bool = False
    message_1_displayed: bool = False
    message_2_displayed: bool = False

    ### Ferris wheel

    wheel_turning: bool = True
