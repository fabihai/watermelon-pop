# Watermelon Pop
## External Links
Here you can find a link to the [blog post](https://fabihai.github.io/).
## Inspiration
I wanted to make a simple game where the user has to go around obstacles to reach a goal. Here the goal is to achieve as high of a goal as possible. Watermelon are one of my favorite fruits for many reasons so I thought it would be fun to create a game where instead of a person spitting watermelon seeds, it would be the watermelon itself shooting seeds to pop balloons, hence the name "Watermelon Pop".

## Materials
This was made on an ESP32. Additional materials include a potentiometer, two buttons, a breadboard, and 7 female-to-male connectors. (Note: if you choose not to use a breadboard, you will just need 7 female-to-female connectors.)

## Setup
### Hardware
For the buttons, one side of each button should be connected to the pin indicated in the Arduino file. The other side of each button should be connected to a `GROUND` pin on the ESP32. `ANALOG_PIN` indicates what the middle pin of the potentiometer should be connected to. The other pins should be connected to `GROUND` and `VCC`, as is indicated in the potentiometer link. Detailed tutorials for how to connect these can be found <a href="https://esp32io.com/tutorials/esp32-button">here</a> (button) and <a href="https://esp32io.com/tutorials/esp32-potentiometer">here</a> (potentiometer).

### Arduino
On Arduino, the baud rate should be 115200. The pins that the buttons and potentiometer are supposed to be connected to are defined at the top of the Arduino file. Change these numbers if you connect your materials to different pins.
### Python
I used PyGame to implement the visual game feature. Use `pip install pygame` in the terminal to make sure you have it installed. The port is preset at the top of the python file. If the ESP32 is connected to a different port, change it accordingly.

### **** Important ****
After the Arduino code is uploaded to the ESP32, you must close the Arduino IDE before running the Python code. Otherwise, the Python code will throw an error.

## Technical Aspect

For the hardware, two buttons and a potentiometer were used, which control whether the game can be reset, the seed attacks, and moving the watermelon up and down the screen.

I used PyGame to run the visual game part of this project. I used Serial to handle communication between Arduino and the laptop. The images on the screen are all sprites that are created automatically as the game continues (the Watermelon and the Balloons), or as a result of user actions (the Seeds). Sprite functions are handled in their respective classes: Player(), Balloon(), Seed(), and Score().

## Gameplay
The game itself is pretty straightforward. The user uses the potentiometer to move up and down the screen. One button handles resetting the game and another fires seeds at the balloons. For each balloon that the player pops with the seeds, the user gains 10 points. If the watermelon collides with a balloon, the player loses 10 points. Certain balloons are randomly generated to be worth +30 or -30 points. If a seed hits any of these balloons, they will gain or lose 30 points accordingly instead of the usual 10 points. Pressing the reset button will reset the score, and delete all sprites from the screen except for the watermelon.

## Enclosure
I wanted to make this seem like an arcade game so I opted for a shape that looks like a mini arcade machine. In arcades, the machines are usually very colorful and are covered with symbols from the game, which I wanted to reflect in this game. So I filled the space with as many many watermelon colors and symbols in the game that I could.
