/*
 * SaturnA.c
 *
 *  Created on: Sep 9, 2024
 *      Author: SMoore4
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>


#include <SaturnA/SaturnA.h>
//#include "SCPI_Parser.h"

// initialize SaturnA IDN
idn_info idnInfo;
char format[64];
//char format_usb[64];

void initializeSaturn(){

    // Initialise idnInfo
    memcpy(idnInfo.manufacturer, Saturn_MANUFACTURER, strlen(Saturn_MANUFACTURER));
    memcpy(idnInfo.model, Saturn_MODEL, strlen(Saturn_MODEL));
    memcpy(idnInfo.serialNumber, Saturn_DEFAULT_SN, strlen(Saturn_DEFAULT_SN));
    //memcpy(idnInfo.serialNumber, "P47959071E", strlen(Saturn_DEFAULT_SN));
    memcpy(idnInfo.firmwareVersion, Saturn_FIRMWARE, strlen(Saturn_FIRMWARE));
    idnInfo.slot = SERIAL_INSTRUCTION_DEFAULT_SLOT;
    idnInfo.serialBaud = 1152000;
    idnInfo.address = SERIAL_INSTRUCTION_DEFAULT_ADDRESS;
    //idnInfo.address = 3;
    idnInfo.resistor = SERIAL_INSTRUCTION_DEFAULT_RESISTOR;


// To retrieve idnInfo data from memory - Seans future work
//    // -- START Prelim stuff
//    if(strcmp(idnInfo.serialNumber, Saturn_DEFAULT_SN) == 0)
//    {
//        // load SN to local memory if needed
//        //printlnToSerial("needed local SN");
//        getMemBytesArray(idnInfo.serialNumber, SERIAL_NUMBER_ADDRESS, 16);
//        // grab eeprom SN
//    }
//
//    if(idnInfo.address == SERIAL_INSTRUCTION_DEFAULT_ADDRESS)
//    {
//        // load ADDRess to local memory if needed
//        //printlnToSerial("needed local ADDR");
//        idnInfo.address = getMemInt32(ADDR_ADDRESS);
//    }
//
//    if(idnInfo.slot == SERIAL_INSTRUCTION_DEFAULT_SLOT)
//    {
//        // load SLOT to local memory if needed
//        //printlnToSerial("needed local SLOT");
//        idnInfo.slot = getMemInt32(SLOT_NUMBER_ADDRESS);
//    }
}

void initializeDrivers()
{
//    initializeAD5676R();
//
//    ad7124_wrappers_metadata adc_wrappers_data;
//
//    // AD7124-8 Driver
//    adc_wrappers_data.spimId = SPIM_ID_ADC;
//    memset(&adc_wrappers_data.adc_csIDs[0], 0, AD7124_MAX_ADCS);
//    adc_wrappers_data.adc_csIDs[0] = SPI_CS_ID_ADC1;
//    adc_wrappers_data.timeoutOFThreshold = 1;
//    adc_wrappers_data.SPIM_StartTransaction = SaturnA_SPIM_StartTransaction;
//    adc_wrappers_data.SPIM_StopTransaction = SaturnA_SPIM_StopTransaction;
//    adc_wrappers_data.SPIM_do = SaturnA_SPIM_do;
//
//    adc_wrappers_data.SPIM_do_write = SaturnA_SPIM_do_write;
//    adc_wrappers_data.SPIM_do_read = SaturnA_SPIM_do_read;
//
//    adc_wrappers_data.TOTimer_Reset = SaturnA_ResetTimeoutTimer;
//    adc_wrappers_data.TOTimer_ReadCounter = Timeout_Timer_ReadCounter;
//    adc_wrappers_data.TOTimer_ReadPeriod = Timeout_Timer_ReadPeriod;
//    adc_wrappers_data.DelayMS = CyDelayUs;
//    //adc_wrappers_data.WaitForBuffers = SaturnA_SPIM_waitForBuffers;
//    AD7124_init(adc_wrappers_data);

}

_Bool SaturnParseAndExecuteSCPI(char * buffer){
    _Bool error = false;
    instruction = parseSerialInstruction(buffer);

    //   serial_instruction instr = parseSerialInstruction(buffer);

    // -- START Prelim stuff

    // To retrieve idnInfo data from memory - Seans future work
//    if(strcmp(idnInfo.serialNumber, Saturn_DEFAULT_SN) == 0){               // load SN to local memory if needed
//        getMemBytesArray(idnInfo.serialNumber, SERIAL_NUMBER_ADDRESS, 16);  // grab eeprom SN
//    }
//
//    if(idnInfo.address == SERIAL_INSTRUCTION_DEFAULT_ADDRESS){              // load ADDRess to local memory if needed
//        idnInfo.address = getMemInt32(ADDR_ADDRESS);
//    }
//    // -- END Prelim stuff

    _Bool doWork = SaturnTestValidSCPI(idnInfo, instruction);
    if(!doWork)
        error = true;
    // -- START -- take care of actual commands
    // test that this is an actionable instruction addresses properly

    int k = 0;  // for loop indexer

    // -- START -- look for SCPI headers
    k = 0;                      // reset k index

    instruction.actionable = true;    // reset actionable

    while(doWork && k<SCPI_COUNT){

        if(strcmp(instruction.command, scpiDefArray[k]) == 0){                          // found an SCPI header

            if(strcmp(instruction.command, SCPI_IDN) == 0) {
                sprintf(format, "%s,%s,%s,%s", idnInfo.manufacturer,
                                                     idnInfo.model,
                                                     idnInfo.serialNumber,
                                                     idnInfo.firmwareVersion);
                printlnToSerial(format);

                instruction.actionable = false;
            }
            else if(strcmp(instruction.command, SCPI_RESET_ADDRESS) == 0) {
                // reset address to default
                // printlnToSerial("resetting address to -9999");                       // for debug, comment out for real use
                idnInfo.address = SERIAL_INSTRUCTION_DEFAULT_ADDRESS;                   // reset local
                // setMemInt32(SERIAL_INSTRUCTION_DEFAULT_ADDRESS, ADDR_ADDRESS);          // reset EEPROM - Seans Future Work
                instruction.actionable = false;
            }
            /* Commenting out for now - AP
            else if(strcmp(instruction.command, SCPI_RESET_CALIBRATION) == 0) {
                // reset address to default
                // printlnToSerial("resetting calibration to default", instruction.serialHardware); // for debug, comment out for real use
                for(int i=1; i <= SaturnX_VSUPPLIES_COUNT; i++){
                    VSUPPLY_CRST(i);
                }
                for(int i=1; i <= SaturnA_TSUPPLIES_COUNT; i++){
                    resetTCalData(i);
                }
                instruction.actionable = false;
            }
            */
            else if(strcmp(instruction.command, SCPI_RST) == 0) {
                // printlnToSerial("found *RST"); // for debug, comment out for real use
                // DO NOTHING NOW
                // TODO: do something eventually - DS 2020-07-21
                instruction.actionable = false;
            }
            else{
                instruction.actionable = true;                                          // didn't find any actions here, still actionable
            }

        }
        doWork = SaturnTestValidSCPI(idnInfo, instruction);
        k++;
    }
    // -- END -- look for SCPI headers

    // -- START -- look for SCPI META headers
    k = 0;
    while(doWork && k<PARAM_MISC_COUNT) {
        //printlnToSerial("found special Parameter");                                   // for debug, comment out for real use
        if(strcmp(instruction.parameter, PARAM_SN) == 0){                               // Serial Number
            if(instruction.readWriteMode == SERIAL_INSTRUCTION_MODE_WRITE){             // write SN
                strcpy(idnInfo.serialNumber, instruction.stringData);                   // write locally
                // write to EEPROM - Sean Future Work
            }
            else{ // output SN
                strcpy(format, idnInfo.serialNumber);
                printlnToSerial(format);
            }
            instruction.actionable = false;
        }
        else if(strcmp(instruction.parameter, PARAM_ADDRESS) == 0){                 // ADDRess
            if(instruction.readWriteMode == SERIAL_INSTRUCTION_MODE_WRITE){         // write ADDRess
                idnInfo.address = instruction.int32Data;                            // write locally
                //setMemInt32(instruction.int32Data, ADDR_ADDRESS);                   // write to EEPROM - Seans Future Work
            }
            else{                                                                   // output ADDRess
                //idnInfo.address = getMemInt32(ADDR_ADDRESS); - Seans Future Work
                sprintf(format, "%ld", idnInfo.address);
                printlnToSerial(format);
            }
            instruction.actionable = false;
        }
        doWork = SaturnTestValidSCPI(idnInfo, instruction);
        k++;
    }
    // -- END -- look for SCPI META headers

    // START look for regular commands
    k = 0;
    while(doWork && k<RESOURCE_COUNT){

        if(strcmp(instruction.resource, RESOURCE_TSUPPLY) == 0){  // temperature power supply
            //TSUPPLY_Execute();
        }
        else if(strcmp(instruction.resource, RESOURCE_VSUPPLY) == 0){
            //VSUPPLY_Execute();
        }
        else if(strcmp(instruction.resource, RESOURCE_ISUPPLY) == 0){
            //ISUPPLY_Execute();
        }
        else if(strcmp(instruction.resource, RESOURCE_ADC) == 0){
            ADC_Execute();
        }
        else if(strcmp(instruction.resource, RESOURCE_GPIO) == 0){
            GPIO_Execute();
        }
        else if(strcmp(instruction.resource, RESOURCE_SPI) == 0){
        	SPI_Execute();
		}
        else if(strcmp(instruction.resource, RESOURCE_MSUPPLY) == 0){
            //MSUPPLY_Execute();
        }

        doWork = SaturnTestValidSCPI(idnInfo, instruction);
        k++;
    }  // -- END -- look for regular commands

    return error;
}

_Bool SaturnTestValidSCPI(idn_info idnInfo, serial_instruction newInstruction){

    return (newInstruction.actionable &&
            (   (idnInfo.address == newInstruction.address) ||
                (SERIAL_INSTRUCTION_UNIVERSAL_ADDRESS == newInstruction.address) ||
                (strcmp(newInstruction.command, SCPI_RESET_ADDRESS) == 0)));
}

/* [] END OF FILE */
