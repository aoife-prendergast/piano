/*
 * SaturnA_Device_ADC.h
 *
 *  Created on: Nov 18, 2024
 *      Author: SMoore4
 */

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#ifndef INC_SATURNA_SATURNA_DEVICE_ADC_H_
#define INC_SATURNA_SATURNA_DEVICE_ADC_H_

#define SATURNA_ADCS_COUNT            1+1

// Register Mapping
// General
#define STATUS		0x00
#define ADCMODE		0x01
#define IFMODE		0x02
#define REGCHECK	0x03
#define DATA		0x04
#define GPIOCON		0x06
#define ID			0x07

// Channels
#define CH0			0x10
#define CH1			0x11
#define CH2			0x12
#define CH3			0x13
#define CH4			0x14
#define CH5			0x15
#define CH6			0x16
#define CH7			0x17
#define CH8			0x18
#define CH9			0x19
#define CH10		0x1A
#define CH11		0x1B
#define CH12		0x1C
#define CH13		0x1D
#define CH14		0x1E
#define CH15		0x1F

// Setup
#define SETUPCON0	0x20
#define SETUPCON1	0x21
#define SETUPCON2	0x22
#define SETUPCON3	0x23
#define SETUPCON4	0x24
#define SETUPCON5	0x25
#define SETUPCON6	0x26
#define SETUPCON7	0x27

// Filters
#define FILT_CON0	0x28
#define FILT_CON1	0x28
#define FILT_CON2	0x2A
#define FILT_CON3	0x2B
#define FILT_CON4	0x2C
#define	FILT_CON5	0x2D
#define FILT_CON6	0x2E
#define FILT_CON7	0x2F

// Offset Register
#define OFFSET0		0x30
#define OFFSET1		0x31
#define OFFSET2		0x32
#define OFFSET3		0x33
#define OFFSET4		0x34
#define OFFSET5		0x35
#define OFFSET6		0x36
#define OFFSET7		0x37

// GAIN Register
#define GAIN0		0x38
#define GAIN1		0x39
#define GAIN2		0x3A
#define GAIN3		0x3B
#define GAIN4		0x3C
#define GAIN5		0x3D
#define GAIN6		0x3E
#define GAIN7		0x3F

typedef struct adc_cal adc_cal;
struct adc_cal {
    float cal_voltage_ch0;
    float cal_voltage_ch1;
    float cal_voltage_ch2;
    float cal_voltage_ch3;
    float cal_voltage_ch4;
    float cal_voltage_ch5;
    float cal_voltage_ch6;
    float cal_voltage_ch7;
    float cal_voltage_ch8;
    float cal_voltage_ch9;
    float cal_voltage_ch10;
    float cal_voltage_ch11;
    float cal_voltage_ch12;
    float cal_voltage_ch13;
    float cal_voltage_ch14;
    float cal_voltage_ch15;
};

//ADC FUNCTIONS
/**
 * @brief Executes the current ADC SCPI command
 * @note Handles its own error codes
 * @returns True if there was an error.
 */
_Bool ADC_Execute();
/**
 * @brief Initializes the ADCs
 * @note Handles its own error codes.
 * @returns True if there was an error.
 */
_Bool ADC_InitializeAll();
/**
 * @brief Writes to the ADC using SPI
 * @does not return anything
 */
void ADC_write(uint8_t adc_reg, uint8_t byte1, uint8_t byte2);
/**
 * @brief Reads the ADC ID from the ADC using SPI
 * @returns a float of the ADC voltage
 */
void ADC_read_id();
/**
 * @brief Reads from the ADC using SPI
 * @returns a float of the ADC voltage
 */
void ADC_read(uint8_t reg, uint8_t *output);
/**
 * @brief toggles GPIO3
 * @returns a float of the ADC voltage
 */
void ADC_GPIO3_Toggle();
/**
 * @brief turn on GPIO3
 * @returns a float of the ADC voltage
 */
void ADC_GPIO3_On();
/**
 * @brief toggles GPIO3
 * @does not return anything
 */
void ADC_GPIO3_Off();
/**
 * @brief for testing the ADC readback
 * @returns a float of the ADC voltage
 */
void ADC_read_test(uint8_t reg, uint8_t *output);
/**
 * @brief for testing the ADC readback
 * @returns a float of the ADC voltage
 */
float ADC_decode(uint32_t data_in);
/**
 * @brief sends the data of all channels back to the host device
 * @does not return anything
 */
void ADC_All_Channels();
/**
 * @brief calibrates the ADC in accordance with each sensor
 * @does not return anything
 */
void ADC_Calibrate();

#endif
