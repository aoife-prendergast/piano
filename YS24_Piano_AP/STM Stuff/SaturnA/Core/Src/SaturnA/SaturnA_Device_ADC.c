/*
 * SaturnA_Device_GPIO.c
 *
 *  Created on: November 18th, 2024
 *      Author: SMoore4
 */

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


#include <SaturnA/SaturnA_Device_ADC.h>
#include <SaturnA/SaturnA_Device_SPI.h>
#include <spi.h>

device_driver Dev_ADC[SATURNA_ADCS_COUNT];

float adc_cal_levels[] = {1.0, 1.0, 1.0, 1.0,		// CH0-3
							1.0, 1.0, 1.0, 1.0,		// CH4-7
							1.0, 1.0, 1.0, 1.0,		// CH8-11
							1.0, 1.0, 1.0, 1.0,};	// CH12-15

uint8_t format_adc[64];


_Bool ADC_Execute(){
    instruction.actionable = false; // do not repeat execution

    _Bool error = false;  // preload to false, will be set true if there is an error coming up


    // Test ADC Rread
    if(instruction.readWriteMode == SERIAL_INSTRUCTION_MODE_READ){                                  // READ mode, use toString()
    	uint8_t output[] = {0x00, 0x00, 0x00, 0x00};
    	ADC_read_id(output);
	} // -- END -- READ mode
    // -- START -- MEASure commands
    //VOLT
    else if((strcmp(instruction.command, CMD_MEASURE) == 0) && (strcmp(instruction.parameter, PARAM_VOLTAGE) == 0))
//        error = ADC_InitializeAll();
    	ADC_All_Channels();
    else if((strcmp(instruction.command, CMD_MEASURE) == 0) && (strcmp(instruction.parameter, PARAM_BYTE) == 0)){
    	uint8_t output[] = {0x00, 0x00, 0x00, 0x00};
    	ADC_read_test((instruction.int32Data & 0xF), output);
    }
    else if((strcmp(instruction.command, CMD_MEASURE) == 0) && (strcmp(instruction.parameter, PARAM_LEVEL) == 0))
    	if (instruction.channel == 1){
    		ADC_GPIO3_On();
    	} else {
    		ADC_GPIO3_Off();
    	}
    else if((strcmp(instruction.command, CMD_MEASURE) == 0) && (strcmp(instruction.parameter, PARAM_BITS) == 0)){
    	error = ADC_InitializeAll();
    } else {
        //ErrorHandler_PushCode(ERROR_UNKNOWN_COMMAND);
        error = true; // no known case was executed
    }

    return error;
}


// Initialises ADC - Can confirm if the registers are set by reading them back
_Bool ADC_InitializeAll()
{
    _Bool error = false;
    uint32_t data_in = 0x00;

    /*
     * ADC Configuration
     * See Datasheet for information on setup configurations
     * */
    // SPI Write: 0x8600 // Sets to continuous conversion mode with a 1ms delay after channel switch
	ADC_write(ADCMODE, 0x86, 0x00);

    // Interface Mode
    // SPI Write 0x1040 // Enables ALT_SYNC and DATA_STAT
	ADC_write(IFMODE, 0x10, 0x40);

    // GPIO Config
    // SPI Write 0x2880 // Enables GPO2/3, SYNC_EN, and sets GPIO1 high.
	ADC_write(GPIOCON, 0x28, 0x00);

    // Setup Con 0
    // SPI Write 0x0C00 // This config is for Unipolar mode, enables the +/- Refbuf
	ADC_write(SETUPCON0, 0x0C, 0x00);

    // Initialize Channels
    // SPI Write 0x8010 // Enables this channel, select setup 0, and pairs the channel0 to GND
	ADC_write(CH0, 0x80, 0x10);
    // SPI Write 0x8030 // Enables this channel, select setup 0, and pairs the channel1 to GND
	ADC_write(CH1, 0x80, 0x30);
    // SPI Write 0x8050 // Enables this channel, select setup 0, and pairs the channel2 to GND
	ADC_write(CH2, 0x80, 0x50);
    // SPI Write 0x8070 // Enables this channel, select setup 0, and pairs the channel3 to GND
	ADC_write(CH3, 0x80, 0x70);
    // SPI Write 0x8090 // Enables this channel, select setup 0, and pairs the channel4 to GND
	ADC_write(CH4, 0x80, 0x90);
    // SPI Write 0x80B0 // Enables this channel, select setup 0, and pairs the channel5 to GND
	ADC_write(CH5, 0x80, 0xB0);
    // SPI Write 0x80D0 // Enables this channel, select setup 0, and pairs the channel6 to GND
	ADC_write(CH6, 0x80, 0xD0);
    // SPI Write 0x80F0 // Enables this channel, select setup 0, and pairs the channel7 to GND
	ADC_write(CH7, 0x80, 0xF0);
    // SPI Write 0x8110 // Enables this channel, select setup 0, and pairs the channel8 to GND
	ADC_write(CH8, 0x81, 0x10);
    // SPI Write 0x8130 // Enables this channel, select setup 0, and pairs the channel9 to GND
	ADC_write(CH9, 0x81, 0x30);
    // SPI Write 0x8150 // Enables this channel, select setup 0, and pairs the channel10 to GND
	ADC_write(CH10, 0x81, 0x50);
    // SPI Write 0x8170 // Enables this channel, select setup 0, and pairs the channel11 to GND
	ADC_write(CH11, 0x81, 0x70);
    // SPI Write 0x8190 // Enables this channel, select setup 0, and pairs the channel12 to GND
	ADC_write(CH12, 0x81, 0x90);
    // SPI Write 0x81B0 // Enables this channel, select setup 0, and pairs the channel13 to GND
	ADC_write(CH13, 0x81, 0xB0);
    // SPI Write 0x81D0 // Enables this channel, select setup 0, and pairs the channel14 to GND
	ADC_write(CH14, 0x81, 0xD0);
    // SPI Write 0x81F0 // Enables this channel, select setup 0, and pairs the channel15 to GND
	ADC_write(CH15, 0x81, 0xF0);


	// Calibrate ADC Channels
	//ADC_Calibrate(); // Commented out while debugging


	// Print out to confirm Function completed
	sprintf(format_adc, "ADC Initialised");
	printlnToSerial(format_adc);

    return false; // Does nothing
}


// Writes to the ADC for a given Register, 16bit command given in two bytes
void ADC_write(uint8_t adc_reg, uint8_t byte1, uint8_t byte2)
{
	uint8_t command[] = {adc_reg, byte1, byte2}; 					// Puts the bytes in an arry to send
	HAL_SPI_Transmit(&hspi2, &command, sizeof(command), 1000);		// Transmit the command
	HAL_Delay(20); // 20ms delay (can be shortened?)
}


// Reads the ADC using the given reg, an pointer output array is parsed in to return the output
void ADC_read(uint8_t reg, uint8_t *output)
{
	uint8_t address = 64 + reg;									// 64 is used to set a write command, then add the register to read
	uint8_t command[] = {address};								// Puts the command into an array for sending
	HAL_SPI_Transmit(&hspi2, &command, sizeof(command), 1000);	// Transmit the command
	HAL_SPI_Receive(&hspi2, &output, sizeof(output), 1000);		// Receive the data from the ADC and store in the output array


	// For DEBUG
	//	sprintf(format_adc, "ADC ID: %d", output[0]);
	//printlnToSerial(format_adc);
}

// Same as the read command, used to read just the ADC ID and return it over uart
void ADC_read_id(uint8_t *output)
{
	uint8_t address = 64 + ID;
	uint8_t command[] = {address};
	uint8_t receive[] = {0x00, 0x00, 0x00, 0x00};
	HAL_SPI_Transmit(&hspi2, &command, sizeof(command), 1000);
	HAL_SPI_Receive(&hspi2, &receive, sizeof(receive), 1000);


	sprintf(format_adc, "ADC ID: %x %x %x %x", receive[0], receive[1], receive[2], receive[3]);
	printlnToSerial(format_adc);
}

// Same as the ADC_Read function, I was just using for debug but both should work the same
void ADC_read_test(uint8_t reg, uint8_t *output)
{
	uint8_t address = 64 + reg;
	uint8_t command[] = {address};
	uint8_t receive[] = {0x00, 0x00, 0x00, 0x00};
	HAL_SPI_Transmit(&hspi2, &command, sizeof(command), 1000);
	HAL_SPI_Receive(&hspi2, &receive, sizeof(receive), 1000);

	sprintf(format_adc, "Readback: %x %x %x %x", receive[0], receive[1], receive[2], receive[3]);
	printlnToSerial(format_adc);
}

// Should toggle the GPIO3 pin, just turns on right now
void ADC_GPIO3_Toggle()
{
	ADC_write(GPIOCON, 0x28, 0x80); // Just turns on now
}

// Turns on the GPIO3 Pin
void ADC_GPIO3_On()
{
	ADC_write(GPIOCON, 0x28, 0x80); // Turn on GPIO3
}

// Turns off the GPIO3 Pin
void ADC_GPIO3_Off()
{
	ADC_write(GPIOCON, 0x08, 0x80); // Turn on GPIO3
}

// Decodes the ADC code to voltage
float ADC_decode(uint32_t data_in)
{
	uint8_t vref = 5; // This could be put to a definiton later, or read from the adc possibly.
				 // Our Ref+ is 5V and Ref- is 0. We are using external reference

	uint32_t max_code = 0x00FFFFFF; // This is 2^N where N is the number of bits the ADC is set to
									// In this case it is 24 bits

	// Read adc instead of dummy code
	uint32_t code = data_in & max_code; // the & cuts the code to the max value (may be uncessecary)

	float voltage = (code*vref)/(max_code*0.1);

	return voltage;
}

// Sends a string of all the ADC channels if they are pressed or not over UART. Worked when using test codes,
// To be tested when ADC is reading correctly
void ADC_All_Channels()
{
	float channel_voltages[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint8_t data_received[] = {0x00, 0x00, 0x00, 0x00};

	for (int i = 0; i < 16; i++) {
		ADC_GPIO3_Off();
		ADC_GPIO3_On();
		ADC_GPIO3_Off();
		HAL_Delay(5);
		ADC_read(DATA, data_received);
		uint32_t code = (data_received[0]<<16)| (data_received[1]<<8) | data_received[2];
		uint8_t channel = data_received[3] & 0x0F;
		float voltage_in = ADC_decode(code);
		channel_voltages[channel] = voltage_in;
	}

	// For debugging
	// sprintf(format_adc, "%f", outputs[2]);

	uint8_t key_presses[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

	for (int i = 0; i < 16; i++) {
		if (channel_voltages[i] > adc_cal_levels[i] + 1){
			key_presses[i] = 1;
		} else {
			key_presses[i] = 0;
		}

	}

	sprintf(format_adc, "%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d", key_presses[0],
			key_presses[1], key_presses[2], key_presses[3], key_presses[4], key_presses[5], key_presses[6],
			key_presses[7], key_presses[8], key_presses[9], key_presses[10], key_presses[11], key_presses[12],
			key_presses[13], key_presses[14], key_presses[15]);

	printlnToSerial(format_adc);
}

// Calibrates teh ADC by reading all the channels and setting their current voltage in the cal_levels array.
void ADC_Callibrate()
{
	uint8_t data_received[] = {0x00, 0x00, 0x00, 0x00};
	for (int i = 0; i < 16; i++) {
		ADC_read_test(DATA, data_received);
		uint32_t code = (data_received[0]<<16)| (data_received[1]<<8) | data_received[2];
		uint8_t channel = data_received[3] & 0x0F;
		float voltage_in = ADC_decode(code);
		adc_cal_levels[channel] = voltage_in;
	}
}
