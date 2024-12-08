# Connect the ferris wheel to Arduino MKR WAN 1310

## Overview
The Ferris wheel uses the servo motor to make it spin. In the script, the Ferris wheel will spin 180 degrees, then spin back another 180 degrees.

## Detailed Wiring Diagrams

### Wiring for the servo motor to MKR WAN 1310:

| **Servo motor Pin** | **Uno Pin** |
|---------------------|-------------|
| Brown               | GND         |
| Red                 | VCC         |
| Orange              | ~2          |


## Attention
This servo motor may not work properly when the MKR WAN 1310 is also connected to other components to perform other actions. In any case, it works fine when the MKR WAN 1310 connects only to the Ferris wheel.