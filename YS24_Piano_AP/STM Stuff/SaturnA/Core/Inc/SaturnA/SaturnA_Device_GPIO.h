/*
 * SaturnA_Device_GPIO.h
 *
 *  Created on: Sep 11, 2024
 *      Author: SMoore4
 */

#ifndef INC_SATURNA_SATURNA_DEVICE_GPIO_H_
#define INC_SATURNA_SATURNA_DEVICE_GPIO_H_

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#include "SCPI_Parser.h"
#include "Device_Driver_Template.h"
#include "Math_Utilities.h"

//#include "../../ADI Drivers/AD5676R/AD5676R.h"


#define SaturnA_GPIO_PORTS_COUNT      3+1

//GPIO Reg
#define Saturn_GPIO_PORT_A       1
#define Saturn_GPIO_PORT_B       2
#define Saturn_GPIO_PORT_F       3


#define Saturn_GPIO_PIN_A0                  1000
#define Saturn_GPIO_PIN_A1                  1001
#define Saturn_GPIO_PIN_A2                  1002
#define Saturn_GPIO_PIN_A3                  1003
#define Saturn_GPIO_PIN_A4                  1004
#define Saturn_GPIO_PIN_A5                  1005
#define Saturn_GPIO_PIN_A6                  1006
#define Saturn_GPIO_PIN_A7                  1007
#define Saturn_GPIO_PIN_A9                  1009
#define Saturn_GPIO_PIN_A10                 1010
#define Saturn_GPIO_PIN_A11                 1011
#define Saturn_GPIO_PIN_A12                 1012
#define Saturn_GPIO_PIN_A15                 1015

#define Saturn_GPIO_PIN_B0                  2000
#define Saturn_GPIO_PIN_B3                  2003
#define Saturn_GPIO_PIN_B4                  2004
#define Saturn_GPIO_PIN_B5                  2005
#define Saturn_GPIO_PIN_B6                  2006
#define Saturn_GPIO_PIN_B7                  2007
#define Saturn_GPIO_PIN_B8                  2008

#define Saturn_GPIO_PIN_F0                  3000
#define Saturn_GPIO_PIN_F1                  3001


// Saturn code - may be dependent to fnction
//    // Modified for PSoC6 - AP...
//    typedef enum pin_mode{
//        DM_ALG_HIZ      = (CY_GPIO_DM_ANALOG),
//        DM_DIG_HIZ      = (CY_GPIO_DM_HIGHZ),
//        DM_RES_UP       = (CY_GPIO_DM_PULLUP),
//        DM_RES_DWN      = (CY_GPIO_DM_PULLDOWN),
//        DM_OD_LO        = (CY_GPIO_DM_OD_DRIVESLOW),
//        DM_OD_HI        = (CY_GPIO_DM_OD_DRIVESHIGH),
//        DM_STRONG       = (CY_GPIO_DM_STRONG),
//        DM_RES_UPDWN    = (CY_GPIO_DM_PULLUP_DOWN)
//    } pin_mode;


//#define Saturn_DEFAULT_GPIO_PORT_VALUE      0x00
//
//// Programmable GPIO Ports not a feature for Saturn E...
//#define Saturn_DEFAULT_GPIO_LEVEL_A         (float)3.3
//#define Saturn_DEFAULT_GPIO_LEVEL_B         (float)3.3
//
//#define Saturn_MAP_DAC_GPIO_A               AD5676R_DAC6
//#define Saturn_MAP_DAC_GPIO_B               AD5676R_DAC7
//
//#define Saturn_LIMIT_VDDIO_A_MAX            (float)5.0
//#define Saturn_LIMIT_VDDIO_B_MAX            (float)5.0
//#define Saturn_LIMIT_VDDIO_A_MIN            (float)0.0
//#define Saturn_LIMIT_VDDIO_B_MIN            (float)0.0
//
//
//#define Saturn_VDDIO_A (uint16)91
//#define Saturn_VDDIO_B (uint16)92





//GPIO FUNCTIONS
_Bool GPIO_Execute();
_Bool GPIO_InitializeAll();
//_Bool GPIO_Initialize(int port);
_Bool GPIO_DRST(int port);
_Bool GPIO_SOUR_BYTE(int port, char * stringByte);
_Bool GPIO_WRITE_BITS(int port, char * stringByte);
void WriteBitPri(int high, int low);
void WriteBitSec(int high, int low);
void DelayClockCycle(int numberOfcycles);
//0b76543210
//byte = 0bABCDEFGH
//location = 4
//length = 3
//0b765FGH10
//write entire control reg
uint8_t GPIO_SOUR_BITS(int port, uint8_t byte, uint8_t location, uint8_t length);
uint8_t GPIO_MEAS_BYTE(int port);
uint8_t GPIO_SOUR_MODE(int port);
void setSaturnGPIOBitMode(uint16_t pin);
_Bool GPIO_SOUR_LEVEL(int pot, int level);
_Bool GPIO_toString();

#endif /* INC_SATURNA_SATURNA_DEVICE_GPIO_H_ */
