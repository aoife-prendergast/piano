/*
 * SaturnA_Device_GPIO.c
 *
 *  Created on: Sep 11, 2024
 *      Author: SMoore4
 */

#include <string.h>
#include <stdio.h>
#include <stdlib.h>


#include <SaturnA/SaturnA_Device_GPIO.h>

device_driver Dev_GPIO_PORT[SaturnA_GPIO_PORTS_COUNT];

uint8_t format_local_GPIO[64];

int high1 = 0;
int low1 = 0;
int high2 = 0;
int low2 = 0;


//GPIO FUNCTIONS
//
//
// return true if there's an error
_Bool GPIO_Execute(){
    instruction.actionable = false; // do not repeat execution

    _Bool error = false;
//    uint8_t data = 0x00;

    if(instruction.readWriteMode == SERIAL_INSTRUCTION_MODE_READ){                                  // READ mode, use toString()
        error = GPIO_toString();
    } // -- END -- READ mode

    else if(instruction.readWriteMode == SERIAL_INSTRUCTION_MODE_WRITE){
        if(strcmp(instruction.command, CMD_SOURCE) == 0){ // -- START -- SOURce commands
            if(strcmp(instruction.parameter, PARAM_LEVEL) == 0){ // -- START -- LEVEL
                error = GPIO_SOUR_LEVEL(instruction.channel, instruction.int32Data);                    // set LEVEL
            } // -- END -- LEVEL
            if(strcmp(instruction.parameter, PARAM_BYTE) == 0){ // -- START -- BYTE
                error = GPIO_SOUR_BYTE(instruction.channel, instruction.stringData); //write byte to port
            } // -- END -- BYTE
            else if(strcmp(instruction.parameter, PARAM_BITS) == 0){ // -- START -- BITS
                error = GPIO_SOUR_BYTE(instruction.channel, instruction.stringData); //write byte to port
            } // -- END -- BITS
            else{ // unsuported SOURce paramater
                error = true;
            } // -- END -- unsuported SOURce paramater
        } // -- END -- SOURce commands

        else if(strcmp(instruction.command, CMD_OUTPUT_STATUS) == 0){ // -- START --

            Dev_GPIO_PORT[instruction.channel].outputStateON = instruction.on_off_mode;  // set the mode state in memory
            /*
            if(instruction.on_off_mode == ON){
                GPIO_SOUR_MODE(instruction.channel, Saturn_GPIO_MODE_STRONG);
            }
            else{
                GPIO_SOUR_MODE(instruction.channel, Saturn_GPIO_MODE_HIZ);
            }
            */
        } //-- END -- OUTP commands

        else if(strcmp(instruction.command, CMD_WRITE) == 0){ // -- START -- WRITE commands
        	if(strcmp(instruction.parameter, PARAM_BITS) == 0){ // -- START -- BITS
				error = GPIO_WRITE_BITS(instruction.channel, instruction.stringData); //write byte to port
			} // -- END -- BYTE


         } //-- END -- WRITE commands

        else if((strcmp(instruction.command, CMD_DRST)==0)){ //-- START -- DRST commands - Digital Reset
            GPIO_DRST(instruction.channel);
        }  //-- END -- DRST commands

        else{ // no known command was requested
            error = true;
        }
    } // -- END -- WRITE mode

    else{ // neither READ nor WRITE mode
        error = true;
    } // -- END -- neither READ nor WRITE mode

    return error;
}


// return true if error
_Bool GPIO_InitializeAll(){
    // Setup GPIO - Currently done in main.c



    return false;
}

// Reset a Digital Port
//
//
// Return true if there's an error
_Bool GPIO_DRST(int port){
    _Bool error = false;
    //GPIO_SOUR_MODE(port, Saturn_GPIO_MODE_HIZ);

    switch(port){
        case Saturn_GPIO_PORT_A:{
            //GPIOA_MUX_Write(0); // set GPIOA to GPIO mode
            //GPIOA_CR_Write(0xFF);
//            GPIOA_CR_AUX_Write(0x00);

            //GPIOA_MUX_Write(0b0);
            //error = GPIO_SOUR_LEVEL(port, Saturn_DEFAULT_GPIO_LEVEL_A);

            break;
        }
        case Saturn_GPIO_PORT_B:{
            //GPIOB_CR_Write(0x00);
            //error = GPIO_SOUR_LEVEL(port, Saturn_DEFAULT_GPIO_LEVEL_B);

            break;
        }
        default:{
            error = true;
            break;
        }
    }

    return error;
}


_Bool GPIO_WRITE_BITS(int port, char * stringByte){
    _Bool error = false;
    char bin[3] = "0b";
    char hex[3] = "0x";
//    uint8_t port_byte = 0xFF;
    char *ptr = NULL;

    char buffer [64];

    //BINARY CASE
    if((ptr = strstr(stringByte, bin)) != NULL) {
        memmove(buffer, stringByte+2, strlen(stringByte));
    } // END BINARY CASE

    //HEX CASE
    else if((ptr = strstr(stringByte, hex)) != NULL){   // this must be else if, because '0x' can appear in binary (ex. 0b0x0x0x0x)
        uint64_t byte = strtol(stringByte, NULL, 0); //extract data from hex format_local_GPIO
        itoa (byte,buffer,2);
    } // END HEX CASE


	uint32_t packetLen = strlen(buffer);

	switch(port){
		case Saturn_GPIO_PIN_A6:{
			for (int i = 0; i<packetLen; i++){
				if ((int)(buffer[i]) == 49){
					WriteBitPri(high1, low1);
				} else if ((int)(buffer[i]) == 48) {
					WriteBitPri(high2, low2);
				} else {
					error = true;
				}
			}

			break;
		}
		case Saturn_GPIO_PIN_B6:{
			for (int i = 0; i<packetLen; i++){
				if ((int)(buffer[i]) == 49){
					WriteBitSec(high1, low1);
				} else if ((int)(buffer[i]) == 48) {
					WriteBitSec(high2, low2);
				} else {
					error = true;
				}
			}

			break;
		}
		default:{
			error = true;
			break;
		}
	}

    return error;
}

// Specifically used for quickly toggling Pins for Jupiter 2 GPIO
void WriteBitPri(int high, int low) {


// High = 558nS, Low = 898
//	for (uint8_t i=0; i<high; i++) {
//		GPIOA->BSRR |= (1<<6); // Set the Pin PA6
//	}
//	for (uint8_t i=0; i<low; i++) {
//		GPIOA->BSRR |= (1<<6) <<16;  // Clear the Pin PA6
//	}


 //High = 336nS, Low = 630
	GPIOA->BSRR |= (1<<6); // Set the Pin PA6
	DelayClockCycle(high);
	GPIOA->BSRR |= (1<<6) <<16;  // Clear the Pin PA6
	DelayClockCycle(low);
}

void WriteBitSec(int high, int low) {
	GPIOB->BSRR |= (1<<6); // Set the Pin PF0
	DelayClockCycle(high);
	GPIOB->BSRR |= (1<<6) <<16;  // Clear the Pin PF0
	DelayClockCycle(low);
}

void DelayClockCycle(int numberOfcycles){
	int i;
	for (i=0; i<numberOfcycles; i++) {
		asm("NOP");
	}
}

//write to a port with stringByte in either in hexidecimal or binary format_local_GPIO
//examples:
// stringByte = "0x0F" or "0b11xx00x001"
//in binary format_local_GPIO, "x" pins are left untouched (including their drive mode)
//in hexidecimal format_local_GPIO, the entire port is written and set to strong drive
// return 0x
_Bool GPIO_SOUR_BYTE(int port, char * stringByte){
    _Bool error = false;
    char bin[3] = "0b";
    char hex[3] = "0x";
//    uint8_t port_byte = 0xFF;
    char *ptr = NULL;

    //BINARY CASE
    if((ptr = strstr(stringByte, bin)) != NULL) {
        ptr +=2;        // move ptr to data start
        int i;

        switch(port){
            case Saturn_GPIO_PORT_A:{
                for(i=0; i<8; i++){
                    switch(ptr[i]){
                        case '0':{
                            if(i<3){
                                //GPIOA_MUX_Write(0); // set GPIOA to GPIO mode
                            }
                            //GPIOA_CR_Write(GPIOA_CR_Read() & ~(0b1 << (7-i))); //set bit to 0 if 0
//                            GPIOA_CR_AUX_Write(GPIOA_CR_AUX_Read() & ~(0b1 << (7-i))); //set bit to 0 if 0
                            //setSaturnGPIOBitMode(Saturn_GPIO_PIN_A7-i, Saturn_GPIO_MODE_STRONG); //set drive mode
                            break;
                        }
                        case '1':{
                            if(i<3){
                                //GPIOA_MUX_Write(0); // set GPIOA to GPIO mode
                            }
                            //GPIOA_CR_Write(GPIOA_CR_Read() | (0b1 << (7-i)));//set bit to 1 if 1
//                            GPIOA_CR_AUX_Write(GPIOA_CR_AUX_Read() | (0b1 << (7-i)));//set bit to 1 if 1
                            //setSaturnGPIOBitMode(Saturn_GPIO_PIN_A7-i, Saturn_GPIO_MODE_STRONG); //set drive mode
                            break;
                        }
                        default:{
                            //if not a 0 or 1, do nothing
                            break;
                        }
                    }
                }
                break;
            }
            case Saturn_GPIO_PORT_B:{
                for(i=0; i<8; i++){
                    switch(ptr[i]){
                        case '0':{
                            //GPIOB_CR_Write(GPIOB_CR_Read() & ~(0b1 << (7-i))); //set bit to 0 if 0
                            setSaturnGPIOBitMode(Saturn_GPIO_PIN_B7-i); //set drive mode
                            break;
                        }
                        case '1':{
                            //GPIOB_CR_Write(GPIOB_CR_Read() | (0b1 << (7-i)));//set bit to 1 if 1
                            setSaturnGPIOBitMode(Saturn_GPIO_PIN_B7-i); //set drive mode
                            break;
                        }
                        default:{
                            //if not a 0 or 1, do nothing
                            break;
                        }
                    }
                }
                break;
            }

            default:{
                error = true;
                break;
            }
        }
    } // END BINARY CASE

    //HEX CASE
    else if((ptr = strstr(stringByte, hex)) != NULL){   // this must be else if, because '0x' can appear in binary (ex. 0b0x0x0x0x)
        uint8_t byte = strtol(stringByte, NULL, 0); //extract data from hex format_local_GPIO

        switch(port){
            case Saturn_GPIO_PORT_A:{
                //GPIOA_MUX_Write(0); // set GPIOA to GPIO mode
                //GPIOA_CR_Write(byte);
//                GPIOA_CR_AUX_Write(byte);
                //GPIO_SOUR_MODE(Saturn_GPIO_PORT_A);
                break;
            }
            case Saturn_GPIO_PORT_B:{
                //GPIOB_CR_Write(byte);
                //GPIO_SOUR_MODE(Saturn_GPIO_PORT_B);
                break;
            }
            default:{
                error = true;
                break;
            }
        }

    } // END HEX CASE

    // error case
    else{
        error = true;
    }

    return error;
}

//write byte of length into the location of the given port, example bellow
//port original state = 0b76543210
//byte passed in =  0bABCDEFGH
//location = 4
//length = 3
//resulting byte = 0b765FGH10
uint8_t GPIO_SOUR_BITS(int port, uint8_t byte, uint8_t location, uint8_t length){
    if((0<length) && (length<=8) && (0<=location) && (location<8)){ //check that length is from 1...8 and location is 0...7
        uint8_t portMask = ((0xFF<<(location +1)) | (0xFF>>(7-location +length))); //a byte with 1s in the bits to be preserved
        uint8_t byteMask = ~ portMask; //a byte with 0s in the port bits to be preserved
        byte = (byte<<(location+1-length)) & byteMask; //move byte to the correct location and put 0s in the port bits to be preserved

        uint8_t tempPort = 0;
        //get what's currently in the register
        switch(port){
            case Saturn_GPIO_PORT_A:{
                if(location < 3){
                    GPIOA_MUX_Write(0); // set GPIOA to GPIO mode
                }
                //GPIO_SOUR_MODE(Saturn_GPIO_PORT_A, Saturn_GPIO_MODE_STRONG);
                tempPort = GPIOA_CR_Read();
                tempPort = tempPort & portMask; //put 0s where byte will be
                tempPort = tempPort | byte; //or the masked port and masked byte
                GPIOA_CR_Write(tempPort); //write to port
                break;
            }
            case Saturn_GPIO_PORT_B:{
                GPIO_SOUR_MODE(Saturn_GPIO_PORT_B);
                tempPort = GPIOB_CR_Read();
                tempPort = tempPort & portMask;
                tempPort = tempPort | byte;
                GPIOB_CR_Write(tempPort);
                break;
            }
            default:{
                break;
            }
        }
        return tempPort;
    }
    //invalid length or location, just return what's in the port without change
    else{
        switch(port){
            case Saturn_GPIO_PORT_A:{
                return GPIOA_CR_Read();
                break;
            }
            case Saturn_GPIO_PORT_B:{
                return GPIOB_CR_Read();
                break;
            }
            default:{

            }
        }
        return 0;
    }
}

// read the status register of a GPIO port
// return the byte as uint8_t
uint8_t GPIO_MEAS_BYTE(int port){
    uint8_t data = 0x00;

    switch(port){
        case Saturn_GPIO_PORT_A:{
            //data = GPIOA_Status_Read();
            Dev_GPIO_PORT[port].measureByte = data;
            break;
        }
        case Saturn_GPIO_PORT_B:{
            //data = GPIOB_Status_Read();
            Dev_GPIO_PORT[port].measureByte = data;
            break;
        }
        default:{
            break;
        }
    }
    return data;
}

//set the drive mode of all 8 bits in a GPIO port
uint8_t GPIO_SOUR_MODE(int port){
    uint8_t data = 0x00;

    if(port == Saturn_GPIO_PORT_A){
        /*
        GPIOA_0_SetDriveMode(mode);
        GPIOA_1_SetDriveMode(mode);
        GPIOA_2_SetDriveMode(mode);
        GPIOA_3_SetDriveMode(mode);
        GPIOA_4_SetDriveMode(mode);
        GPIOA_5_SetDriveMode(mode);
        GPIOA_6_SetDriveMode(mode);
        GPIOA_7_SetDriveMode(mode);
        */
        //data = GPIOA_Status_Read();
    }
    else if(port == Saturn_GPIO_PORT_B){
        /*
        GPIOB_0_SetDriveMode(mode);
        GPIOB_1_SetDriveMode(mode);
        GPIOB_2_SetDriveMode(mode);
        GPIOB_3_SetDriveMode(mode);
        GPIOB_4_SetDriveMode(mode);
        GPIOB_5_SetDriveMode(mode);
        GPIOB_6_SetDriveMode(mode);
        GPIOB_7_SetDriveMode(mode);
        */
        //data = GPIOB_Status_Read();
    }
    else if((port >= Saturn_GPIO_PIN_A0) && (port <= Saturn_GPIO_PIN_A7)){
        setSaturnGPIOBitMode((uint16_t)port);
        data = GPIOA_Status_Read();
    }
    else if((port >= Saturn_GPIO_PIN_B0) && (port <= Saturn_GPIO_PIN_B7)){
        setSaturnGPIOBitMode((uint16_t)port);
        data = GPIOB_Status_Read();
    }
    else{
        // error case
        data = 0;
    }

    Dev_GPIO_PORT[port].mode = 0;   // not precisely true, but kinda close sometimes

    return data;
}

//set the drive mode of a single GPIO pin
void setSaturnGPIOBitMode(uint16_t pin){
    switch(pin){

        default:{
        }
    }
}


_Bool GPIO_SOUR_LEVEL(int port, int level){
    _Bool error = false;

    switch(port){
        case 0:{
        	high1 = level;
        	break;
        }
        case 1:{
        	low1 = level;
        	break;
        }
        case 2:{
			high2 = level;
			break;
		}
		case 3:{
			low2 = level;
			break;
		}
        default:{ // do nothing
            error = true;
            break;
        }
    }

    return error;
}


_Bool GPIO_toString(){
    _Bool error = false;
    uint8_t data = 0x00;

    error = (instruction.readWriteMode != SERIAL_INSTRUCTION_MODE_READ) ? true : false;         // make sure this is READ mode

    if(!error){
        if(strcmp(instruction.command, CMD_SOURCE) == 0){        // -- START -- SOURce commands
            if(strcmp(instruction.parameter, PARAM_LEVEL) == 0){ // -- START -- LEVEL
            	int output = 1000;
            	switch(instruction.channel){        // standard GPIOA and GPIOB
					case Saturn_GPIO_PORT_A:{
						if ((GPIOA->IDR & GPIO_PIN_5) != 0x00U)
						{
							output = 1;
						}
						else
						{
							output = 0;
						}
						break;
					}
					case Saturn_GPIO_PORT_B:{
						error = true;
						break;
					}
					case Saturn_GPIO_PORT_F:{
						if ((GPIOF->IDR & GPIO_PIN_0) != 0x00U)
						{
							output = 1;
						}
						else
						{
							output = 0;
						}
						break;
					}
					default:{                       // error out otherwise
						error = true;
						break;
					}
				}
                sprintf(format_local_GPIO, "%d", output);
            } // -- END -- LEVEL
            else if((strcmp(instruction.parameter, PARAM_BYTE) == 0) || (strcmp(instruction.parameter, PARAM_BITS) == 0)){
                // get the data
                if(instruction.channel == Saturn_GPIO_PORT_A){
                	data = 32;
//                    }
                }
                // get the data
                else if(instruction.channel == Saturn_GPIO_PORT_B){
                        //data = GPIOB_Status_Read();
                }
                else{
                    error = true;
                }

                sprintf(format_local_GPIO, "It worked! 0x%02X", data);
            }

            else{ // unsuported SOURce paramater
                error = true;
            }
        } // -- END -- SOURce commands

        // -- START -- MEASure commands
        else if((strcmp(instruction.command, CMD_MEASURE) == 0) &&
                    (strcmp(instruction.parameter, PARAM_BYTE) == 0)){
            data = GPIO_MEAS_BYTE(instruction.channel);
            Dev_GPIO_PORT[instruction.channel].measureByte = data;
            sprintf(format_local_GPIO, "0x%02X", data);
        }  //-- END -- MEASure commands

        // -- START -- OUTP commands
        else if(strcmp(instruction.command, CMD_OUTPUT_STATUS) == 0){
            sprintf(format_local_GPIO, "%d", Dev_GPIO_PORT[instruction.channel].outputStateON);
            //sprintf(format_local_GPIO, "%d", Dev_GPIO_PORT[instruction.channel].outputStateON);
        } //-- END -- OUTP commands

        else{
            error = true; // no known case was executed
        }
    }

    if(!error){
        printlnToSerial(format_local_GPIO);
    }
    else{       // send a null, don't hang the COM port
        printlnToSerial("Error");
    }

    return error;
}


