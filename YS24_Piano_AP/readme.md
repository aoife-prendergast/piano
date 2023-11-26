# Piano 2.0 - BTYS 2024

### Working so far:
1. Sensor activation 
2. Note playing 

### Getting started:
1. Create Venv and install requirements
	Run the make.sh shell script by running "bash make.sh" in the terminal

#### To Run the program 
1. Launch terminal inside the led_control directory
2. Run 'sudo python3 main.py' 






***********************************************
1. Create Virtual Midi Port - sudo modprobe snd-virmidi midi-devs=1
2. Check that is there - aconnect -o
3. Connect the music player to the port 
4. Run the python script - plays a sound through the virtual cable
