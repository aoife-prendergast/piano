/*
 * SCPI_Parser.h
 *
 *  Created on: Sep 5, 2024
 *      Author: SMoore4
 */

#ifndef INC_SCPI_PARSER_H_
#define INC_SCPI_PARSER_H_

#include <stdio.h>
#include <stm32g4xx.h>

// -- BEGIN -- SCPI Definitions
#define SCPI_LENGTH                   16

// START standard SCPI commands           (2)
#define SCPI_IDN                    "*IDN?"         // 1. standard IDN query
#define SCPI_RST                    "*RST" 			// 2. standard RST command
//--------------------------------------------------
#define STANDARD_SCPI_COUNT				2

// START custom SCPI commands
#define SCPI_RESET_ADDRESS          "*ARST"         // 1. set ADDR=-9999
#define SCPI_RESET_CALIBRATION      "*CRST"         // 2. reset all calibration data
#define SCPI_ADDRESS_AUTOSET        "*ASET"         //3. autoset address based on site ID resistor
//--------------------------------------------------
#define CUSTOM_SCPI_COUNT					3

//--------------------------------------------------
#define SCPI_COUNT							STANDARD_SCPI_COUNT + CUSTOM_SCPI_COUNT

static const char scpiDefArray[SCPI_COUNT][SCPI_LENGTH] = {
        SCPI_IDN,
        SCPI_RST,
        SCPI_RESET_ADDRESS,
        SCPI_RESET_CALIBRATION,
        SCPI_ADDRESS_AUTOSET
    };
// -- END -- SCPI Definitions


// Copied from COM_PSoC6
#define SERIAL_HARDWARE_NA      0b00
#define SERIAL_HARDWARE_USB     0b001
#define SERIAL_HARDWARE_RS485   0b010


// Write/Read mode
#define SERIAL_INSTRUCTION_MODE_READ    0b01        //
#define SERIAL_INSTRUCTION_MODE_WRITE   0b10        //


// -- BEGIN -- RESOURCE Definitions
#define RESOURCE_LENGTH               10

#define RESOURCE_SCPI               "SCPI"			// 1.
#define RESOURCE_VSUPPLY            "VSUPPLY" 		// 2. normal power supply
#define RESOURCE_ISUPPLY            "ISUPPLY" 		// 3. current source
#define RESOURCE_TSUPPLY            "TSUPPLY" 		// 4. temperature controller
#define RESOURCE_FSUPPLY            "FSUPPLY" 		// 5. frequency generator
#define RESOURCE_ADC                "ADC"			// 6.
#define RESOURCE_PWM                "PWM"			// 7.
#define RESOURCE_SPI                "SPI"			// 8.
#define RESOURCE_UART               "UART"			// 9.
#define RESOURCE_DUT_SITE           "DUT"			// 10.
#define RESOURCE_VDAC               "VDAC"			// 11.
#define RESOURCE_IDAC               "IDAC"			// 12.
#define RESOURCE_MEMORY             "MEM"			// 13.
#define RESOURCE_GPIO               "GPIO"			// 14.
#define RESOURCE_SPI                "SPI"			// 15. SPI interfacing
#define RESOURCE_I2C                "I2C"			// 16. I2C interfacing
#define RESOURCE_LED                "LED"			// 17.
#define RESOURCE_UNKNOWN            "RSC_UNK"		// 18.
#define RESOURCE_ARBITRARY          "ARB"			// 19.
#define RESOURCE_BRIDGE             "BRIDGE"		// 20.
#define RESOURCE_I2C                "I2C"			// 21.
#define RESOURCE_JTAG               "JTAG"			// 22.
#define RESOURCE_CAN                "CAN"			// 23.
#define RESOURCE_SYSTEM             "SYST"			// 24.
#define RESOURCE_MSUPPLY            "MOTOR" 		// 25. MOTOR CONTROL
//--------------------------------------------------
#define RESOURCE_COUNT							23

static const char resourceDefArray[RESOURCE_COUNT][RESOURCE_LENGTH] = {
        RESOURCE_SCPI,
        RESOURCE_VSUPPLY,
        RESOURCE_ISUPPLY,
        RESOURCE_TSUPPLY,
        RESOURCE_FSUPPLY,
        RESOURCE_ADC,
        RESOURCE_PWM,
        RESOURCE_SPI,
        RESOURCE_UART,
        RESOURCE_DUT_SITE,
        RESOURCE_VDAC,
        RESOURCE_IDAC,
        RESOURCE_MEMORY,
        RESOURCE_GPIO,
        RESOURCE_LED,
        RESOURCE_UNKNOWN,
        RESOURCE_ARBITRARY,
        RESOURCE_BRIDGE,
        RESOURCE_I2C,
        RESOURCE_JTAG,
        RESOURCE_CAN,
        RESOURCE_SYSTEM,
        RESOURCE_MSUPPLY
    };
// -- END -- RESOURCE Definitions

// -- BEGIN -- COMMAND Definiitons
#define CMD_LENGTH                    10

// START analog commands                  (6)
#define CMD_SOURCE                  "SOUR"		// 1. SOURce
#define CMD_MEASURE                 "MEAS"		// 2. MEASure

#define CMD_OUTPUT_STATUS           "OUTP"    	// 3. OUTPut

#define CMD_CALIBRATE_OFFSET        "CALOFST"	// 4.
#define CMD_CALIBRATE_GAIN          "CALGAIN"	// 5.
#define CMD_CALIBRATE               "CALIBRATE"	// 6.
#define CMD_STEP                    "STEP"	    // 7
#define CMD_ANGLE                   "ANGLE"     // 8
//--------------------------------------------------
#define CMD_ANALOG_COUNT					8

// START digital and all purpose commands (9)
#define CMD_INITIALIZE              "INIT"		// 1.
#define CMD_ENABLE                  "ENABLE"	// 2.
#define CMD_WRITE_VERIFIED          "VWRITE"	// 3.
#define CMD_COMMUNICATION           "COMM"		// 4.
#define CMD_DRST                    "DRST" 		// 5. digital pin reset
#define CMD_CRST                    "CRST" 		// 6. calibration reset
#define CMD_COMM                    "COMM"		// 7.
#define CMD_WRITE                   "WRITE"		// 8.
#define CMD_ROM                     "ROM"		// 9.
#define CMD_ERROR                   "ERROR"     // 10.
#define CMD_FAULT                   "FAULT"     // 11.

//--------------------------------------------------
#define CMD_DIGITAL_COUNT					11

//--------------------------------------------------
#define CMD_COUNT						CMD_ANALOG_COUNT + CMD_DIGITAL_COUNT


static const char commandDefArray[CMD_COUNT][CMD_LENGTH] = {
        CMD_OUTPUT_STATUS,

        CMD_SOURCE,
        CMD_MEASURE,

        CMD_CALIBRATE_OFFSET,
        CMD_CALIBRATE_GAIN,
        CMD_CALIBRATE,

        CMD_INITIALIZE,
        CMD_ENABLE,
        CMD_WRITE_VERIFIED,
        CMD_COMMUNICATION,
        CMD_DRST,
        CMD_CRST,
        CMD_COMM,
        CMD_WRITE,

        CMD_ROM,

        CMD_ERROR,
        CMD_FAULT,

        CMD_STEP,
        CMD_ANGLE
    };
// -- END -- COMMAND Definitions



// -- BEGIN -- Command Parameters Definitions
#define PARAM_LENGTH                  10

// START misc parameters
#define PARAM_SN                        "*SN"		// 1.
#define PARAM_SCRATCHPAD                "*SCRATCH"	// 2.
#define PARAM_SLOTS                     "*SLTS"		// 3.
#define PARAM_ADDRESS                   "*ADDR"		// 4.

//--------------------------------------------------
#define PARAM_MISC_COUNT							4

static const char parameterSpecialDefArray[PARAM_MISC_COUNT][PARAM_LENGTH] = {
        PARAM_SN,
        PARAM_SCRATCHPAD,
        PARAM_SLOTS,
        PARAM_ADDRESS
    };

// START analog parameters
#define PARAM_VOLTAGE                   "VOLT"		// 1.
#define PARAM_CURRENT                   "CURR"		// 2.
#define PARAM_TEMPERATURE               "TEMP"		// 3.
#define PARAM_HTPWM                     "HTPWM"		// 4.
#define PARAM_VMIN                      "VMIN"		// 5.
#define PARAM_VMAX                      "VMAX"		// 6.
#define PARAM_IMIN                      "IMIN"		// 7.
#define PARAM_IMAX                      "IMAX"		// 8.
#define PARAM_TMIN                      "TMIN"		// 9.
#define PARAM_TMAX                      "TMAX"		// 10.
#define PARAM_POWER                     "POW"		// 11.
#define PARAM_PVI                       "PVI"		// 12.
//--------------------------------------------------
#define PARAM_ANALOG_COUNT							12

// START digital parameters
#define PARAM_LEVEL                     "LEVEL"		// 1.
#define PARAM_BYTE                      "BYTE"		// 2.
#define PARAM_BITS                      "BITS"		// 3.
#define PARAM_FREQUENCY                 "FREQ"		// 4.
#define PARAM_DUTY_CYCLE                "DUTY"		// 5.
#define PARAM_LANGUAGE                  "LANG"		// 6.
#define PARAM_BAUD                      "BAUD"		// 7.
#define PARAM_CRC                       "CRC"		// 8.
#define PARAM_MODE                      "MODE"		// 9.
#define PARAM_FILE                      "FILE"		// 10.
#define PARAM_STEP                      "STEP"		// 11.
#define PARAM_PULSE                     "PULSE"		// 12.
//--------------------------------------------------
#define PARAM_DIGITAL_COUNT							12
//--------------------------------------------------
#define PARAM_COUNT						PARAM_ANALOG_COUNT + PARAM_DIGITAL_COUNT



static const char parameterDefArray[PARAM_COUNT][PARAM_LENGTH] = {
        PARAM_VOLTAGE,
        PARAM_CURRENT,
        PARAM_TEMPERATURE,
        PARAM_HTPWM,
        PARAM_VMIN,
        PARAM_VMAX,
        PARAM_IMIN,
        PARAM_IMAX,
        PARAM_TMIN,
        PARAM_TMAX,
        PARAM_POWER,
        PARAM_LEVEL,
        PARAM_BYTE,
        PARAM_BITS,
        PARAM_FREQUENCY,
        PARAM_DUTY_CYCLE,
        PARAM_LANGUAGE,
        PARAM_BAUD,
        PARAM_CRC,
        PARAM_MODE,
        PARAM_PVI,
        PARAM_FILE,
        PARAM_STEP,
        PARAM_PULSE
    };
// -- END -- Command Parameters Definitions

/*
// NOT USED! COMMENTED OUT ON PURPOSE - DS - 2020-07-28
// -- START -- composite SCPI definitions, for easy SWITCH
#define COMPOSITE_SCPI_OUTPUT_STATUS_READ 0
#define COMPOSITE_SCPI_OUTPUT_STATUS_WRITE 1

#define COMPOSITE_SCPI_SOURCE_VOLTAGE_READ 2
#define COMPOSITE_SCPI_SOURCE_VOLTAGE_WRITE 3
#define COMPOSITE_SCPI_SOURCE_CURRENT_READ 4
#define COMPOSITE_SCPI_SOURCE_CURRENT_WRITE 5
#define COMPOSITE_SCPI_SOURCE_POWER_READ 6
#define COMPOSITE_SCPI_SOURCE_POWER_WRITE 7

#define COMPOSITE_SCPI_MEASURE_VOLTAGE_READ 8
#define COMPOSITE_SCPI_MEASURE_CURRENT_READ 9
#define COMPOSITE_SCPI_MEASURE_POWER_READ 10

#define COMPOSITE_SCPI_CALIBRATE_OFFSET_VOLTAGE_READ 11
#define COMPOSITE_SCPI_CALIBRATE_OFFSET_VOLTAGE_WRITE 12
#define COMPOSITE_SCPI_CALIBRATE_OFFSET_CURRENT_READ 13
#define COMPOSITE_SCPI_CALIBRATE_OFFSET_CURRENT_WRITE 14
#define COMPOSITE_SCPI_CALIBRATE_OFFSET_POWER_READ 15
#define COMPOSITE_SCPI_CALIBRATE_OFFSET_POWER_WRITE 16
// -- END -- composite SCPI definitions
*/

// serial_instruction default defines
#define SERIAL_INSTRUCTION_DEFAULT_SLOT         0
#define SERIAL_INSTRUCTION_DEFAULT_ADDRESS      100
#define SERIAL_INSTRUCTION_UNIVERSAL_ADDRESS    777
#define SERIAL_INSTRUCTION_DEFAULT_RESISTOR     100000000.0     // 100Mohm
#define SERIAL_INSTRUCTION_DEFAULT_RW_MODE      SERIAL_INSTRUCTION_MODE_READ
#define SERIAL_INSTRUCTION_DEFAULT_CHANNEL      -9999
#define SERIAL_INSTRUCTION_DEFAULT_DATA_LINT    -99999
#define SERIAL_INSTRUCTION_DEFAULT_DATA_FLOAT   -99999.0
#define SERIAL_INSTRUCTION_DEFAULT_DATA_STRING  ""
#define SERIAL_INSTRUCTION_DEFAULT_DATA_UINT    99999
#define SERIAL_INSTRUCTION_UNIVERSAL_BP_SLOT    7

typedef struct serial_instruction serial_instruction;
struct serial_instruction {
    uint8_t serialHardware;

    _Bool actionable;
	int16_t slot;
    int16_t address;
    uint8_t readWriteMode;
    char resource[10];
    char command[10];
    char parameter[10];
    int16_t channel;
    int16_t on_off_mode;
    char stringData[32];
    int32_t int32Data;
    float floatData;
    uint32_t uint32Data;
    uint64_t uint64Data;
};
extern serial_instruction instruction;   // declare a global instruction instance for universal use

typedef struct idn_info idn_info;
struct idn_info{
    char manufacturer[15];
    char model[15];
    char serialNumber[16];
    char firmwareVersion[15];

    int32_t address;
    int32_t slot;
    int32_t serialBaud;
    int32_t resistor;
};
extern idn_info idnInfo;                // declare a global idnInfo for universal use

typedef struct csv_data csv_data;
struct csv_data{
	int32_t data_1;
	int32_t data_2;
	int32_t data_3;
};

//*******************************************************************************
	HAL_StatusTypeDef Saturn_UART_Receive(UART_HandleTypeDef *huart, uint8_t *pData, uint8_t *Size, uint32_t Timeout);
	void SCPI_Initialize(UART_HandleTypeDef *huart_parse);
	void printlnToSerial(uint8_t * outText);
    _Bool findSerialNumber(char * SN_out, char * buffer);
    int findSlot(char * buffer);
    int findAddress(char * buffer);
//*******************************************************************************
    _Bool findStringData(char * stringData, char * buffer);
    int32_t findDataDigitIndex(char * startingString, char * buffer);
    int32_t findInt32Data(char * buffer);
    uint32_t findUint32Data(char * buffer);
    uint64_t findUint64Data(char * buffer);
    float findFloatData(char * buffer);
//*******************************************************************************
    int findChannel(char * buffer);
    uint8_t findReadWriteMode(char * buffer);
    int findOnOffMode(char * buffer);
//*******************************************************************************
    void testFindUtilities();
    void serial_instruction_initialize(serial_instruction *serialInstructionIN);
    serial_instruction parseSerialInstruction(char *buffer);
    void serial_instruction_toString(serial_instruction printThis);
    void serial_instruction_printState(serial_instruction serialInstructionIN);
    void serial_instruction_debugMain();
    void serial_instruction_debugParrot(char * buffer);
//*******************************************************************************


#endif /* INC_SCPI_PARSER_H_ */
