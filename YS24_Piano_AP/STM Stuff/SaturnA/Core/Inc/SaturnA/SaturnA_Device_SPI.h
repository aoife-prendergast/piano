/*
 * SaturnA_Device_SPI.c
 *
 *  Created on: Sep 11, 2024
 *      Author: SMoore4
 */

#ifndef INC_SATURNA_SATURNA_DEVICE_SPI_H_
#define INC_SATURNA_SATURNA_DEVICE_SPI_H_

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#include "SCPI_Parser.h"
#include "Device_Driver_Template.h"
#include "Math_Utilities.h"

//#include "../../ADI Drivers/AD5676R/AD5676R.h"


#define SaturnA_SPI_PORTS_COUNT      3+1

//SPI Reg
#define Saturn_SPI_PORT_A       1
#define Saturn_SPI_PORT_B       2
#define Saturn_SPI_PORT_F       3

// Un-needed, taken from GPIO
#define Saturn_SPI_PIN_A0                  1000

#define Saturn_SPI_PIN_B0                  2000


#define Saturn_SPI_PIN_F0                  3000




//#define Saturn_DEFAULT_SPI_PORT_VALUE      0x00
//
//// Programmable SPI Ports not a feature for Saturn E...
//#define Saturn_DEFAULT_SPI_LEVEL_A         (float)3.3
//#define Saturn_DEFAULT_SPI_LEVEL_B         (float)3.3
//
//#define Saturn_MAP_DAC_SPI_A               AD5676R_DAC6
//#define Saturn_MAP_DAC_SPI_B               AD5676R_DAC7
//
//#define Saturn_LIMIT_VDDIO_A_MAX            (float)5.0
//#define Saturn_LIMIT_VDDIO_B_MAX            (float)5.0
//#define Saturn_LIMIT_VDDIO_A_MIN            (float)0.0
//#define Saturn_LIMIT_VDDIO_B_MIN            (float)0.0
//
//
//#define Saturn_VDDIO_A (uint16)91
//#define Saturn_VDDIO_B (uint16)92





//SPI FUNCTIONS
_Bool SPI_Execute();
_Bool SPI_InitializeAll();
//_Bool SPI_Initialize(int port);
_Bool SPI_DRST(int port);
_Bool SPI_SOUR_BYTE(int port, char * stringByte);
_Bool SPI_WRITE_BITS(int port, char * stringByte);
void DelayClockCycle(int numberOfcycles);
//0b76543210
//byte = 0bABCDEFGH
//location = 4
//length = 3
//0b765FGH10
//write entire control reg
uint8_t SPI_SOUR_BITS(int port, uint8_t byte, uint8_t location, uint8_t length);
uint8_t SPI_MEAS_BYTE(int port);
uint8_t SPI_SOUR_MODE(int port);
_Bool SPI_toString(char * stringByte);

#endif /* INC_SATURNA_SATURNA_DEVICE_SPI_H_ */
