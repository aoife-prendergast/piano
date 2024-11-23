/*
 * SaturnA.h
 *
 *  Created on: Sep 9, 2024
 *      Author: SMoore4
 */

#ifndef INC_SATURNA_SATURNA_H_
#define INC_SATURNA_SATURNA_H_

// -- START -- Device Driver Includes - Sean Future Work

//#include "SaturnA_Device_ADC.h"
//#include "SaturnA_Device_GPIO.h"
//#include "SaturnA_Device_TSUPPLY.h"
//#include "SaturnA_Device_ISUPPLY.h"
//#include "SaturnA_Device_ADC.h"
//#include "SaturnA_Device_VSUPPLY.h"
//#include "SaturnA_Device_OVERLOADS.h"
//#include "SaturnA_Device_MSUPPLY.h"

// -- END -- Device Driver Includes

#include "SCPI_Parser.h"
#include "Device_Driver_Template.h"
#include "Math_Utilities.h"

////#include "../../ADI Drivers/AD5621/AD5621.h"                  // 1 CH DAC only used for tokelau-type BIBs
//#include "../../ADI Drivers/AD5676R/AD5676R.h"                  // 8 CH DAC used on Saturn cards
////#include "../../ADI Drivers/AD5302_12_22/AD5302_12_22.h"
//#include "../../../PSoC Drivers/PSoC6/AD7124/AD7124.h"
//#include "../../ADI Drivers/AD7124_8/AD7124_8_PSoC6.h"
//#include "../../ADI Drivers/AD7124_8/AD7124_8_regs.h"
////#include "../../ADI Drivers/AD7124/AD7124.h"
////#include "../../ADI Drivers/ADGxxxx/ADGxxxx.h"
//#include "../../ADI Drivers/LTC2662/LTC2662PSoC6.h"
////#include "../../ADI Drivers/LTM4676A/LTM4676A.h"

#define Saturn_MANUFACTURER    "ADI"
#define Saturn_MODEL           "Saturn_A"
#define Saturn_DEFAULT_SN      "DEFAULT_SN"
#define Saturn_FIRMWARE        "SaturnA v1"

//#define DAC_STEP_FB_CODE_ON    0x3EB8 // generates 1.225V with a 16 bit 5V DAC
//#define DAC_STEP_FB_CODE_OFF   0x0000 // generates 0V with a 16 bit 5V DAC
//#define I2      AD5676R_DAC5

//Saturn RTD parameters - Sean Future Work
//#define Saturn_RTD_IDAC_CHANNEL     SaturnA_MAP_IDAC0
//#define Saturn_RTD_ADC_CHANNEL      SaturnXADC_DIFF_CH1
//#define Saturn_RTD_TOLERANCE        (float)0.01

// START FAULT DEFINITIONS    - Sean Future Work
//#define Saturn_ERROR_TSUPPLY    0b00000001
//#define Saturn_ERROR_VSUPPLY    0b00000010
//#define Saturn_ERROR_ISUPPLY    0b00000100
//#define Saturn_ERROR_ADC        0b00001000
//#define Saturn_ERROR_MEMORY     0b00010000
//#define Saturn_ERROR_PERIPHERAL 0b00100000
//#define Saturn_ERROR_SYSTEM     0b01000000
//#define Saturn_ERROR_ENABLE     0b10000000
//
//#define Saturn_WARNING_TSUPPLY    0b00000001
//#define Saturn_WARNING_VSUPPLY    0b00000010
//#define Saturn_WARNING_ISUPPLY    0b00000100
//#define Saturn_WARNING_ADC        0b00001000
//#define Saturn_WARNING_MEMORY     0b00010000
//#define Saturn_WARNING_PERIPHERAL 0b00100000
//#define Saturn_WARNING_SYSTEM     0b01000000
//#define Saturn_WARNING_ENABLE     0b10000000

// END FAULT DEFINITIONS

/**
* @brief Saturn Device Initialisation
*/
void initializeSaturn();

/**
* @brief Initializes the shared driver libraries
*/
void initializeDrivers();

/**
* @brief Something here...
*/
_Bool SaturnParseAndExecuteSCPI(char * buffer);

/**
* @brief Saturn Device Initialisation
* @details DUT Driver Card Saturn only processes the instruciton by this particular Saturn based on the set Address
* @param[in] idnInfo            Identifying details of this Saturn
* @param[in] newInstruction     Parsed Serial Instruction Information
* @rturns True if instruction deserves action by this Saturn, false otherwise
*/
_Bool SaturnTestValidSCPI(idn_info idnInfo, serial_instruction newInstruction);

#endif /* INC_SATURNA_SATURNA_H_ */
