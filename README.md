# Steam Engine Simulator Cheat

This is a fun tool designed to enhance your experience in the steam game [Steam Engine Simulator](https://store.steampowered.com/app/2381620/Steam_Engine_Simulator/). It allows you to control the water, heat, brakes, and water quantity parameters directly, allowing you to go up to 4e6 the standard heat controls.

This tool is written in Python, and utilizes the `pymem` and `keyboard` libraries to modify the game's process memory.


### Usage

Download the .exe from the Releases tab, and launch it.

In game, you can control the parameters using the following keys:

- 'W' key: Increase heat control and water quantity exponentially
- 'S' key: Activate brakes and set heat and water control to 0.
- 'G' key: Hold water quantity (experimental)
- 'Shift' key: Use in combination with 'W' or 'S' for faster heat control increment.
- 'Ctrl' key: Use in combination with 'W' or 'S' for slower heat control increment.
