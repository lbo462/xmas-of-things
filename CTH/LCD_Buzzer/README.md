# Play songs using buzzer and display messages using LCD module on Arduino MKR WAN 1310 and Arduino UNO R3

## Connect the buzzers to Arduino MKR WAN 1310 to play songs

### Overview
Unlike Teensyduino, Arduino MKR WAN 1310 does not have an SD card slot. Thus, we cannot play the songs directly from the SD card. We are playing the melody of the songs using the notes with different frequencies and durations.

### Detailed Wiring Diagrams

#### Wiring for the buzzers to MKR WAN 1310:

| **Buzzers** | **MKR WAN 1310 Pin** |
|-------------|----------------------|
|Red          |GND                   |
|Blac         |8                     |

- If there's no more GND in the MKR WAN 1310, we can connect to the GND of the Arduino UNO R3

## Connect Arduino MKR WAN 1310 to Arduino UNO R3 for LCD display

### Overview
The LCD module is not compatible with the Arduino MKR WAN 1310 but works with the Arduino UNO. Since the Arduino UNO cannot directly receive messages from the TTN, the Arduino MKR WAN will act as a middleman. The Arduino MKR WAN will send messages through Serial1 (UART connection, Tx/Rx), and the Arduino UNO will display the messages on the LCD.

### Detailed Wiring Diagrams for Serial Communication Code

#### Wiring for the LCD Module to Arduino Uno:

| **LCD Pin** | **Uno Pin** |
|-------------|-------------|
| GND         | GND         |
| VCC         | 5V          |
| SDA         | A4          |
| SCL         | A5          |

#### Wiring for Communication Between MKR WAN 1310 and Uno:

| **MKR WAN 1310 Pin** | **Uno Pin** |
|----------------------|-------------|
| 13->RX               | TX->1       |
| 14<-TX               | RX<-0       |
| GND                  | GND         |


### Attention
The ```uno_script.ino``` and ```mkr_script.ino``` should be uploaded without the Tx/Rx connection. Once the upload process is complete, the connection can be made.
  
