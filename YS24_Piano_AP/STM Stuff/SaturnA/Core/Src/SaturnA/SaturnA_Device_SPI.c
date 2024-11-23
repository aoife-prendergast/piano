/*
 * SaturnA_Device_SPI.c
 *
 *  Created on: Sep 11, 2024
 *      Author: SMoore4
 */

#include <string.h>
#include <stdio.h>
#include <stdlib.h>


#include <SaturnA/SaturnA_Device_SPI.h>
#include <spi.h>

device_driver Dev_SPI_PORT[SaturnA_SPI_PORTS_COUNT];

uint8_t format_local_SPI[64];



//SPI FUNCTIONS
//
//
// return true if there's an error
_Bool SPI_Execute(){
    instruction.actionable = false; // do not repeat execution

    _Bool error = false;
//    uint8_t data = 0x00;

    if(instruction.readWriteMode == SERIAL_INSTRUCTION_MODE_READ){                                  // READ mode, use toString()
        error = SPI_toString(instruction.stringData);
    } // -- END -- READ mode

    else if(instruction.readWriteMode == SERIAL_INSTRUCTION_MODE_WRITE){
        if(strcmp(instruction.command, CMD_SOURCE) == 0){ // -- START -- SOURce commands
            if(strcmp(instruction.parameter, PARAM_LEVEL) == 0){ // -- START -- LEVEL
                error = true;
            } // -- END -- LEVEL
            if(strcmp(instruction.parameter, PARAM_BYTE) == 0){ // -- START -- BYTE
                error = SPI_SOUR_BYTE(instruction.channel, instruction.stringData); //write byte to port
            } // -- END -- BYTE
            else if(strcmp(instruction.parameter, PARAM_BITS) == 0){ // -- START -- BITS
                error = SPI_SOUR_BYTE(instruction.channel, instruction.stringData); //write byte to port
            } // -- END -- BITS
            else{ // unsuported SOURce paramater
                error = true;
            } // -- END -- unsuported SOURce paramater
        } // -- END -- SOURce commands

        else if(strcmp(instruction.command, CMD_OUTPUT_STATUS) == 0){ // -- START --

            Dev_SPI_PORT[instruction.channel].outputStateON = instruction.on_off_mode;  // set the mode state in memory
            /*
            if(instruction.on_off_mode == ON){
                SPI_SOUR_MODE(instruction.channel, Saturn_SPI_MODE_STRONG);
            }
            else{
                SPI_SOUR_MODE(instruction.channel, Saturn_SPI_MODE_HIZ);
            }
            */
        } //-- END -- OUTP commands

        else if(strcmp(instruction.command, CMD_WRITE) == 0){ // -- START -- WRITE commands
        	if(strcmp(instruction.parameter, PARAM_BITS) == 0){ // -- START -- BITS
				error = SPI_WRITE_BITS(instruction.channel, instruction.stringData); //write byte to port
			} // -- END -- BYTE


         } //-- END -- WRITE commands

        else if((strcmp(instruction.command, CMD_DRST)==0)){ //-- START -- DRST commands - Digital Reset
            SPI_DRST(instruction.channel);
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
_Bool SPI_InitializeAll(){
    // Setup SPI - Currently done in main.c

	// SPI_Core = SPI_HandleTypeDef *

    return false;
}

// Reset a Digital Port
//
//
// Return true if there's an error
_Bool SPI_DRST(int port){
    _Bool error = false;
    //SPI_SOUR_MODE(port, Saturn_SPI_MODE_HIZ);


    return error;
}


_Bool SPI_WRITE_BITS(int port, char * stringByte){
    _Bool error = false;

    HAL_SPI_TransmitReceive(&hspi2, stringByte, format_local_SPI,
                			sizeof(format_local_SPI), 1000);

    printlnToSerial(format_local_SPI);

    return error;
}


//write to a port with stringByte in either in hexidecimal or binary format_local_SPI
//examples:
// stringByte = "0x0F" or "0b11xx00x001"
//in binary format_local_SPI, "x" pins are left untouched (including their drive mode)
//in hexidecimal format_local_SPI, the entire port is written and set to strong drive
// return 0x
_Bool SPI_SOUR_BYTE(int port, char * stringByte){
    _Bool error = false;
    char bin[3] = "0b";
    char hex[3] = "0x";
//    uint8_t port_byte = 0xFF;
    char *ptr = NULL;

    //BINARY CASE
    if((ptr = strstr(stringByte, bin)) != NULL) {
        ptr +=2;        // move ptr to data start
        int i;
    } // END BINARY CASE

    //HEX CASE
    else if((ptr = strstr(stringByte, hex)) != NULL){   // this must be else if, because '0x' can appear in binary (ex. 0b0x0x0x0x)


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
uint8_t SPI_SOUR_BITS(int port, uint8_t byte, uint8_t location, uint8_t length){
    if((0<length) && (length<=8) && (0<=location) && (location<8)){ //check that length is from 1...8 and location is 0...7
        uint8_t portMask = ((0xFF<<(location +1)) | (0xFF>>(7-location +length))); //a byte with 1s in the bits to be preserved
        uint8_t byteMask = ~ portMask; //a byte with 0s in the port bits to be preserved
        byte = (byte<<(location+1-length)) & byteMask; //move byte to the correct location and put 0s in the port bits to be preserved

        uint8_t tempPort = 0;
        //get what's currently in the register
    }
}

// read the status register of a SPI port
// return the byte as uint8_t
uint8_t SPI_MEAS_BYTE(int port){
    uint8_t data = 0x00;

    switch(port){
        case Saturn_SPI_PORT_A:{
            //data = SPIA_Status_Read();
            Dev_SPI_PORT[port].measureByte = data;
            break;
        }
        case Saturn_SPI_PORT_B:{
            //data = SPIB_Status_Read();
            Dev_SPI_PORT[port].measureByte = data;
            break;
        }
        default:{
            break;
        }
    }
    return data;
}

//set the drive mode of all 8 bits in a SPI port
uint8_t SPI_SOUR_MODE(int port){
    uint8_t data = 0x00;



    Dev_SPI_PORT[port].mode = 0;   // not precisely true, but kinda close sometimes

    return data;
}



_Bool SPI_toString(char * stringByte){
    _Bool error = false;
    uint8_t data = 0x00;

    error = (instruction.readWriteMode != SERIAL_INSTRUCTION_MODE_READ) ? true : false;         // make sure this is READ mode

    if(!error){
        if(strcmp(instruction.command, CMD_SOURCE) == 0){        // -- START -- SOURce commands
            if(strcmp(instruction.parameter, PARAM_LEVEL) == 0){ // -- START -- LEVEL
            	int output = 1000;

            	//HAL_SPI_Transmit(&hspi2, stringByte, sizeof(stringByte), 1000);
            	//HAL_SPI_Receive(&hspi2, format_local_SPI, sizeof(format_local_SPI), 1000);


            	// May be needed if consecutive functions doesnt work
            	//HAL_Delay(1000)

            	HAL_SPI_TransmitReceive(&hspi2, stringByte, stringByte,
            			sizeof(stringByte), 1000);

            	//format_local_SPI =  stringByte;

            	//HAL_Delay(1000)

                //sprintf(format_local_SPI, "%d", output);
            } // -- END -- LEVEL
            else if((strcmp(instruction.parameter, PARAM_BYTE) == 0) || (strcmp(instruction.parameter, PARAM_BITS) == 0)){
            	error = true;
            }

            else{ // unsuported SOURce paramater
                error = true;
            }
        } // -- END -- SOURce commands

        // -- START -- MEASure commands
        else if((strcmp(instruction.command, CMD_MEASURE) == 0) &&
                    (strcmp(instruction.parameter, PARAM_BYTE) == 0)){
            data = SPI_MEAS_BYTE(instruction.channel);
            Dev_SPI_PORT[instruction.channel].measureByte = data;
            sprintf(format_local_SPI, "0x%02X", data);
        }  //-- END -- MEASure commands

        // -- START -- OUTP commands
        else if(strcmp(instruction.command, CMD_OUTPUT_STATUS) == 0){
            sprintf(format_local_SPI, "%d", Dev_SPI_PORT[instruction.channel].outputStateON);
            //sprintf(format_local_SPI, "%d", Dev_SPI_PORT[instruction.channel].outputStateON);
        } //-- END -- OUTP commands

        else{
            error = true; // no known case was executed
        }
    }

    if(!error){
        printlnToSerial(stringByte);
    }
    else{       // send a null, don't hang the COM port
        printlnToSerial("Error");
    }

    return error;
}


