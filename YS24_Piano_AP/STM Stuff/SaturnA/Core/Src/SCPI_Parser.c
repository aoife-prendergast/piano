/*
 * SCPI_Parser.c
 *
 *  Created on: Sep 5, 2024
 *      Author: SMoore4
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <SaturnA/SaturnA_Core.h>
#include "Math_Utilities.h"

#include "SCPI_Parser.h"

//*******************************************************************************

char format_Parser[64];
UART_HandleTypeDef huart;

//*******************************************************************************



HAL_StatusTypeDef Saturn_UART_Receive(UART_HandleTypeDef *huart, uint8_t *pData, uint8_t *Size, uint32_t Timeout)
{
  uint8_t  *pdata8bits;
  uint16_t uhMask;
  uint32_t tickstart;
  uint8_t max_buffer = *Size;

  /* Check that a Rx process is not already ongoing */
  if (huart->RxState == HAL_UART_STATE_READY)
  {
    if ((pData == NULL) || (*Size == 0U))
    {
      return  HAL_ERROR;
    }

    huart->ErrorCode = HAL_UART_ERROR_NONE;
    huart->RxState = HAL_UART_STATE_BUSY_RX;
    huart->ReceptionType = HAL_UART_RECEPTION_STANDARD;

    /* Init tickstart for timeout management */
    tickstart = HAL_GetTick();

    huart->RxXferSize  = *Size;
    huart->RxXferCount = *Size;

    /* Computation of UART mask to apply to RDR register */
    UART_MASK_COMPUTATION(huart);
    uhMask = huart->Mask;

    pdata8bits  = pData;

    /* as long as data have to be received */
    while (huart->RxXferCount > 0U)
    {
      if (UART_WaitOnFlagUntilTimeout(huart, UART_FLAG_RXNE, RESET, tickstart, Timeout) != HAL_OK)
      {
        huart->RxState = HAL_UART_STATE_READY;

        return HAL_TIMEOUT;
      }
      *pdata8bits = (uint8_t)(huart->Instance->RDR & (uint8_t)uhMask);

      huart->RxXferCount--;

      if (*pdata8bits == 10)
      {
    	  break;
      }

      pdata8bits++;
    }

    *Size = max_buffer - huart->RxXferCount;

    /* At end of Rx process, restore huart->RxState to Ready */
    huart->RxState = HAL_UART_STATE_READY;

    return HAL_OK;
  }
  else
  {
    return HAL_BUSY;
  }
}


extern serial_instruction instruction = {
    SERIAL_HARDWARE_USB,

    false
};                  // define a global instruction instance for universal use

void SCPI_Initialize(UART_HandleTypeDef *huart_parse)
{
	huart = *huart_parse;
}

void printlnToSerial(uint8_t * outText)
{
	uint32_t packetLen = strlen(outText);
	HAL_UART_Transmit(&huart, outText, packetLen, 1000);
}

// extracts SN string from *SN command
_Bool findSerialNumber(char * SN_out, char * buffer){
    char *start = strstr(buffer, PARAM_SN);

    if(start != NULL){  // found it
        int snStart = strstr(buffer, PARAM_SN) - buffer + 4; // remove <*SN >
          strcpy(SN_out, buffer + snStart);                    // return the end of the string
        //SN_out = strndup(buffer+snStart, 15);  // return the end of the string with a max of 15 bytes plus 1 forced null
        return 1;
    }
    else{  // not found
        strcpy(SN_out, "");  // return null string
        return false;
    }
}


// reads the ADDRess as int
// return -9999 if no ADDRESS found
int findAddress(char * buffer){
    int address = SERIAL_INSTRUCTION_DEFAULT_ADDRESS;

    char *addrRef = strstr(buffer,"ADDR:");
    if(addrRef != NULL){
        int addrOffset = addrRef - buffer + 5;

        address = (int)strtol(buffer + addrOffset, NULL, 10);                // return string as a DEC
    }

    else{
        addrRef = strstr(buffer,"*SETADDR ");
         if((addrRef != NULL)){
            int addrOffset = addrRef - buffer + 9;

            address = (int)strtol(buffer + addrOffset, NULL, 10);                // return string as a DEC
        }
    }

    return address;
}


//*******************************************************************************

// returns string found between two spaces. ie: ' stringdata '
_Bool findStringData(char * stringData, char * buffer){
    char* startPtr = strchr(buffer, ' '); // first ' '

    if(startPtr!=NULL){
        char* endPtr = strrchr(buffer, ' '); // last ' '

        if(startPtr == endPtr){  // there is only one space
            strcpy(stringData, startPtr+1);  // delete the space, return the rest
        }
        else{  // there are at least 2 spaces
            int start = startPtr - buffer + 1;
            int stop = endPtr - buffer;

            char temp[32]; // temporary string
            memset(temp, 0, sizeof(temp)); // very neccessary...
            int k = 0; // iterators
            int j = 0;
            for(j = start; j<stop; k++, j++){ // build string
                temp[k] = buffer[j];
            }
            strcpy(stringData, temp); // output the new string - can be replaced with strncpy
        }

        return true;

    }
    else{
        return false;
    }
}

int32_t findDataDigitIndex(char * startingString, char * buffer){
    char *ptr = strstr(buffer, startingString);

    if(ptr != NULL){
        _Bool foundDigit = false;
        int32_t k = 0;
        for(k = ptr-buffer+strlen(startingString); k<strlen(buffer); k++){  // look for a digit after the start
            if(isDigitPolar(buffer[k])){
                foundDigit = true;
                break;
            }
            else if((buffer[k] != ' ') && (buffer[k] != ':')){  // ran into more writing, bad format_Parser
                foundDigit = false;
                break;
            }
        }

        if(foundDigit){
            return k;// return index
        }
        else{
            return -1;
        }
    }
    else{
        return -1;
    }
}


// reads in the first float after the first space character in a string
// in the abbreviated SCPI format_Parser we are using, there will only ever be 1 float max in a command
float findFloatData(char * buffer){
    int32_t k = findDataDigitIndex(" ", buffer);

    if(k != -1){
        return atof(buffer + k);  // read the float value offset by the white space from buffer start
    }
    else{// incorrect format_Parser
        return SERIAL_INSTRUCTION_DEFAULT_DATA_FLOAT;
    }
}

// reads in the first int32_t after the first space character in a string
// in the abbreviated SCPI format_Parser we are using, there will only ever be 1 int32_t max in a command
int32_t findInt32Data(char * buffer){
 //   int32_t k = findDataDigitIndex(" ", buffer);

    char *ptr = strstr(buffer, " "); //check if '0x' is found

 //   if(k != -1){
    if(ptr != NULL){
//        return strtol(buffer + k, NULL, 10);// return string as a DEC
        return strtol(ptr, NULL, 10);// return string as a DEC
    }
    else{// incorrect format_Parser
        return SERIAL_INSTRUCTION_DEFAULT_DATA_LINT;
    }
}

// reads in the first uint32_t after the first space character in a string, in '0x<XXXXXXXX>' format_Parser
// in the abbreviated SCPI format_Parser we are using, there will only ever be 1 uint32_t max in a command
uint32_t findUint32Data(char * buffer){

    char *ptr = strstr(buffer, "0x"); //check if '0x' is found

    if(ptr != NULL){
        return strtol(ptr, NULL, 0);// return as uint32_t
    }
    else{// incorrect format_Parser
        return SERIAL_INSTRUCTION_DEFAULT_DATA_UINT;
    }
}

// reads in the first uint32_t after the first space character in a string, in '0x<XXXXXXXX>' format_Parser
// in the abbreviated SCPI format_Parser we are using, there will only ever be 1 uint32_t max in a command
uint64_t findUint64Data(char * buffer){

    char *ptr = strstr(buffer, "0LL"); //check if '0x' is found

    if(ptr != NULL){
        return strtoll(ptr + 3, NULL, 16);// return as uint64
    }
    else{// incorrect format_Parser
        return SERIAL_INSTRUCTION_DEFAULT_DATA_UINT;
    }
}


//*******************************************************************************

// reads the chanel number nnn from a string of the format_Parser: "stuff (@nnn) potentially more stuff"
int findChannel(char * buffer){
    int32_t k = findDataDigitIndex("(@", buffer);

    if(k != -1){
        return strtol(buffer + k, NULL, 10);// return string as a DEC
    }
    else{// incorrect format_Parser
        return SERIAL_INSTRUCTION_DEFAULT_CHANNEL;
    }
}

// get read/write mode
uint8_t findReadWriteMode(char * buffer){
    if(strchr(buffer, '?') != NULL){    // '?' indicates read mode
        return SERIAL_INSTRUCTION_MODE_READ;
    }
    else{                               // all else assumed write mode
        return SERIAL_INSTRUCTION_MODE_WRITE;
    }
}

// get ON/OFF mode
int findOnOffMode(char * buffer){
    if(strstr(buffer, "ON") != NULL){
        return 1;
    }
    else if(strstr(buffer, "OFF") != NULL){
        return 0;
    }
    else{
        return -1;
    }
}



// set a serial_instruction to default values
void serial_instruction_initialize(serial_instruction *serialInstructionIN){
    serialInstructionIN->actionable = false;
    serialInstructionIN->slot = SERIAL_INSTRUCTION_DEFAULT_SLOT;
    serialInstructionIN->address = SERIAL_INSTRUCTION_DEFAULT_ADDRESS;
    serialInstructionIN->readWriteMode = SERIAL_INSTRUCTION_DEFAULT_RW_MODE;
    strcpy(serialInstructionIN->resource, SERIAL_INSTRUCTION_DEFAULT_DATA_STRING);
    strcpy(serialInstructionIN->command, SERIAL_INSTRUCTION_DEFAULT_DATA_STRING);
    strcpy(serialInstructionIN->parameter, SERIAL_INSTRUCTION_DEFAULT_DATA_STRING);
    serialInstructionIN->channel = SERIAL_INSTRUCTION_DEFAULT_CHANNEL;
    serialInstructionIN->on_off_mode = -1;
    memset(serialInstructionIN->stringData, 0, 16); // put in 16 x 0 bytes
    serialInstructionIN->int32Data = SERIAL_INSTRUCTION_DEFAULT_DATA_LINT;
    serialInstructionIN->floatData = SERIAL_INSTRUCTION_DEFAULT_DATA_FLOAT;
    serialInstructionIN->uint32Data = SERIAL_INSTRUCTION_DEFAULT_DATA_UINT;
    serialInstructionIN->uint64Data = SERIAL_INSTRUCTION_DEFAULT_DATA_UINT;
}

// take in a string and parse into a serial_instruction
serial_instruction parseSerialInstruction(char *buffer){
    //init all values of instr
    serial_instruction instr;
    serial_instruction_initialize(&instr);

    instr.serialHardware = instruction.serialHardware;
    //instr.slot = findSlot(buffer);          // get the slot
    instr.address = findAddress(buffer);    // get the address
    instr.readWriteMode = findReadWriteMode(buffer);    // get read write mode

    // -- START -- look for actionable commands
    int k = 0;

    // -- START -- look for SCPI headers
    for(k=0; k<SCPI_COUNT; k++){
        if(strstr(buffer, scpiDefArray[k]) != NULL){            // found an SCPI header
            strcpy(instr.resource, RESOURCE_SCPI);              // set resource = SCPI
            strcpy(instr.command, scpiDefArray[k]);             // set command
            if(strstr(buffer, SCPI_ADDRESS_AUTOSET) != NULL){ //if ASET, need more info
                instr.channel = findChannel(buffer); //need channel
                instr.int32Data = findInt32Data(buffer); //need resistance (getting as int and float)
                instr.floatData = findFloatData(buffer); //need resistance
            }

            instr.actionable = true;                            // set to actionable true
            break;
        }
    }
    // -- END -- look for SCPI headers

    // -- START -- look for SCPI META headers
    for(k=0; k<PARAM_MISC_COUNT; k++){
        if(strstr(buffer, parameterSpecialDefArray[k]) != NULL){    // found a special parameter
            strcpy(instr.resource, RESOURCE_SCPI);                  // set resource = SCPI
            strcpy(instr.command, CMD_ROM);                         // set command = ROM
            strcpy(instr.parameter, parameterSpecialDefArray[k]);   // set parameter

            if(instr.readWriteMode == SERIAL_INSTRUCTION_MODE_WRITE){
                // this is a write instruction, we need to extract the data
                if(strstr(buffer, PARAM_SN) != NULL){
                    // serial number
                    findSerialNumber(instr.stringData, buffer);
                }
                else if(strstr(buffer, PARAM_SCRATCHPAD) != NULL){
                    // scratchpad needs string data and CH#
                    findStringData(instr.stringData, buffer);
                    instr.channel = findChannel(buffer);
                }
                else{
                    // SLTS and ADDR need int32_t data
                    instr.int32Data = findInt32Data(buffer);
                }
            }
            else{// this is a read instruction
                if(strstr(buffer, PARAM_SCRATCHPAD) != NULL){
                    // the scratch read needs a channel
                    instr.channel = findChannel(buffer);
                }
                else{
                    // do nothing
                }
            }

            instr.actionable = true;                            // set to actionable true
            break;
        }
    }
    // -- END -- look for SCPI META headers

    // START look for regular commands
    if(instr.actionable != true){  // did not find SCPI header, or special parameter, look for other things
        // get onoff state, data, and channel
        instr.on_off_mode = findOnOffMode(buffer);

        findStringData(instr.stringData, buffer);
        instr.int32Data = findInt32Data(buffer);
        instr.floatData = findFloatData(buffer);
        instr.uint32Data = findUint32Data(buffer);
        instr.uint64Data = findUint64Data(buffer);

        if(instr.uint32Data == 0xA1) {
            instr.uint32Data = 0xA1;
        }

        instr.channel = findChannel(buffer);

        for(k=0; k<RESOURCE_COUNT; k++){
            if(strstr(buffer, resourceDefArray[k]) != NULL){ // test this working
                strcpy(instr.resource, resourceDefArray[k]);
                instr.actionable = true;
                break;
            }
        }

        for(k=0; k<CMD_COUNT; k++){
            if(strstr(buffer, commandDefArray[k]) != NULL){
                strcpy(instr.command, commandDefArray[k]);
                instr.actionable = true;
                break;
            }
        }

        for(k=0; k<PARAM_COUNT; k++){
            if(strstr(buffer, parameterDefArray[k]) != NULL){
                strcpy(instr.parameter, parameterDefArray[k]);
                instr.actionable = true;
                break;
            }
        }
    }
    // -- END -- look for regular commands

    return instr;
}

// generate an ECHO of the input serial instruction that would have generated this data
void serial_instruction_toString(serial_instruction printThis){
//    _Bool actionable;
//	  uint16 slot;
//    uint32_t address;
//    uint8_t readWriteMode;
//    char resource[10];
//    char command[10];
//    char parameter[10];
//    int channel;
//    uint8_t data[16];

    char outputString[64] = "";
    //char format_Parser[64];  // used for string manipulations

    char stringSlot[10] = "";
    char stringAddress[10] = "";
    char stringRWmode[1] = "?";
    char stringResource[10] = "";
    char stringCommand[10] = "";
    char stringParameter[10] = "";
    char stringChannel[10] = "";
    //char stringDigitalData[16] = "";
    //char stringIntData[16] = "";
    //char stringFloatData[16] = "";
    char stringData[16] = "";


    if(printThis.actionable){
        if(strcmp(printThis.resource, RESOURCE_SCPI) == 0){  // SCPI META *type commands
            /*
            // TODO: fix this


            if(strcmp(printThis.command, CMD_SCPI_IDN) == 0){
                strcat(outputString, stringSlot);       // append SLOT
                strcat(outputString, stringAddress);    // append ADDRess
                strcat(outputString, SCPI_IDN);         // append *IDN?
            }
            else if(strcmp(printThis.command, CMD_SCPI_RST) == 0){
                strcat(outputString, stringSlot);       // append SLOT
                strcat(outputString, stringAddress);    // append ADDRess
                strcat(outputString, SCPI_RST);         // append RST
            }
            else if(strcmp(printThis.command, CMD_SCPI_SET_SN) == 0){
                strcat(outputString, stringSlot);       // append SLOT
                strcat(outputString, stringAddress);    // append ADDRess
                strcat(outputString, SCPI_SET_SN);      // append *SETSN?
            }
            else if(strcmp(printThis.command, CMD_SCPI_N) == 0){
                strcat(outputString, stringSlot);                               // append SLOT
                strcat(outputString, stringAddress);                            // append ADDRess

                if(printThis.readWriteMode == SERIAL_INSTRUCTION_MODE_READ){                    // READ mode
                    sprintf(stringCommand,"N%.1d?",printThis.channel);
                    strcat(outputString, stringCommand);                        // append CoMandD
                }
                else{
                    sprintf(stringCommand,"*SETN%.1d ",printThis.channel);          // WRITE mode
                    strcat(outputString, stringCommand);                        // append CoMandD
                    strcat(outputString, printThis.stringData);                 // append the string
                }
            }
            else if(strcmp(printThis.command, CMD_SCPI_SLOT) == 0){
                if(printThis.readWriteMode == SERIAL_INSTRUCTION_MODE_READ){                    // READ mode
                    strcat(outputString, "SLOT?");                        // append CoMandD
                }
                else{
                    // do nothing, only SLOT? is an SCPI command
                }
            }
            else if(strcmp(printThis.command, CMD_SCPI_SLOTS) == 0){
                if(printThis.readWriteMode == SERIAL_INSTRUCTION_MODE_READ){                    // READ mode
                    strcat(outputString, "SLTS?");                        // append CoMandD
                }
                else{
                    sprintf(stringCommand,"*SETSLTS:%d ",printThis.intData);          // WRITE mode
                    strcat(outputString, stringCommand);                        // append CoMandD
                    strcat(outputString, printThis.stringData);                 // append the string
                }
            }
            else if(strcmp(printThis.command, CMD_SCPI_ADDR) == 0){
                if(printThis.readWriteMode == SERIAL_INSTRUCTION_MODE_READ){                    // READ mode
                    strcat(outputString, "ADDR?");                        // append CoMandD
                }
                else{
                    sprintf(stringCommand,"*SETADDR:%ld ",printThis.int32_tData);          // WRITE mode
                    strcat(outputString, stringCommand);                        // append CoMandD
                    strcat(outputString, printThis.stringData);                 // append the string
                }
            } */
        }
        else{
            if(printThis.slot != SERIAL_INSTRUCTION_DEFAULT_SLOT){
                sprintf(stringSlot,"SLOT:%d:",printThis.slot);
                strcat(outputString, stringSlot);  // append SLOT
            }
            if(printThis.address != SERIAL_INSTRUCTION_DEFAULT_ADDRESS){
                sprintf(stringAddress,"ADDR:%d:",printThis.address);
                strcat(outputString, stringAddress); // append ADDRess
            }

            if(printThis.readWriteMode == SERIAL_INSTRUCTION_MODE_READ){  // read mode
                if(strcmp(printThis.command,CMD_OUTPUT_STATUS) == 0){ // OUTP command
                    sprintf(format_Parser,"%s:OUTP? (@%d)",printThis.resource, printThis.channel);
                }
                else if((strcmp(printThis.command,CMD_CALIBRATE_OFFSET) == 0) ||
                            (strcmp(printThis.command,CMD_CALIBRATE_GAIN) == 0)){ // CALibrate command
                    sprintf(format_Parser,"%s:%s:%s? (@%d)",printThis.resource, printThis.command, printThis.parameter, printThis.channel);
                }
                else{ // other commands are simpler
                    sprintf(format_Parser,"%s:%s? (@%d)", printThis.resource, printThis.parameter, printThis.channel);
                }
                strcat(outputString, format_Parser); // append format_Parserted string
            }
            else{  // WRITE mode
                if(strcmp(printThis.command,CMD_OUTPUT_STATUS) == 0){ // OUTP command
                    _Bool outputONOFF = (printThis.floatData == 0) ? false : true;
                    sprintf(format_Parser,"%s:OUTP %d (@%d)",printThis.resource, outputONOFF, printThis.channel);
                }
                else if((strcmp(printThis.command,CMD_CALIBRATE_OFFSET) == 0) ||
                            (strcmp(printThis.command,CMD_CALIBRATE_GAIN) == 0)){ // CALibrate command
                    sprintf(format_Parser,"%s:%s:%s %f (@%d)",printThis.resource, printThis.command, printThis.parameter, printThis.floatData, printThis.channel);
                }
                else{ // other commands are simpler
                    sprintf(format_Parser,"%s:%s %f (@%d)", printThis.resource, printThis.parameter, printThis.floatData, printThis.channel);
                }
                strcat(outputString, format_Parser); // append formatted string
            }
        }
        printlnToSerial(outputString);  // print out the final reconstructed string command
    }
    else{
        printlnToSerial("Error: unactionable serial instruction");
    }
}
