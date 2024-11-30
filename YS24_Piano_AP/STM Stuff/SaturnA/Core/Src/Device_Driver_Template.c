/*
 * Device_Driver_Template.c
 *
 *  Created on: Sep 9, 2024
 *      Author: SMoore4
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#if defined (__GNUC__)
    /* Add an explicit reference to the floating point printf library */
    /* to allow the usage of floating point conversion specifiers. */
    /* This is not linked in by default with the newlib-nano library. */
    asm (".global _printf_float");
#endif

#include "Device_Driver_Template.h"



//*******************************************************************************

void device_driver_initialize(device_driver * deviceIN){
//    deviceIN = &device_driver_default;

    deviceIN->status = device_driver_default.status;
    deviceIN->actionable = device_driver_default.actionable;
    deviceIN->outputStateON = device_driver_default.outputStateON;
    deviceIN->mode = device_driver_default.mode;

    deviceIN->sourcePowerMin = device_driver_default.sourcePowerMin;
    deviceIN->sourceVoltMin = device_driver_default.sourceVoltMin;
    deviceIN->sourceCurrentMin = device_driver_default.sourceCurrentMin;
    deviceIN->sourceTemperatureMin = device_driver_default.sourceTemperatureMin;

    deviceIN->sourcePower = device_driver_default.sourcePower;
    deviceIN->sourceVolt = device_driver_default.sourceVolt;
    deviceIN->sourceCurrent = device_driver_default.sourceCurrent;
    deviceIN->sourceTemperature = device_driver_default.sourceTemperature;

    deviceIN->sourcePowerMax = device_driver_default.sourcePowerMax;
    deviceIN->sourceVoltMax = device_driver_default.sourceVoltMax;
    deviceIN->sourceCurrentMax = device_driver_default.sourceCurrentMax;
    deviceIN->sourceTemperatureMax = device_driver_default.sourceTemperatureMax;

    deviceIN->calOffsetPower = device_driver_default.calOffsetPower;
    deviceIN->calOffsetVolt = device_driver_default.calOffsetVolt;
    deviceIN->calOffsetCurrent = device_driver_default.calOffsetCurrent;
    deviceIN->calOffsetTemperature = device_driver_default.calOffsetTemperature;

    deviceIN->calGainPower = device_driver_default.calGainPower;
    deviceIN->calGainVolt = device_driver_default.calGainVolt;
    deviceIN->calGainCurrent = device_driver_default.calGainCurrent;
    deviceIN->calGainTemperature = device_driver_default.calGainTemperature;

    deviceIN->tolerancePower = device_driver_default.calGainPower;
    deviceIN->toleranceVolt = device_driver_default.calGainVolt;
    deviceIN->toleranceCurrent = device_driver_default.calGainCurrent;
    deviceIN->toleranceTemperature = device_driver_default.calGainTemperature;

    deviceIN->measurePower = device_driver_default.measurePower;
    deviceIN->measureVolt = device_driver_default.measureVolt;
    deviceIN->measureCurrent = device_driver_default.measureCurrent;
    deviceIN->measureTemperature = device_driver_default.measureTemperature;

    //deviceIN->temp_prev_i = device_driver_default.temp_prev_i;
    //deviceIN->temp_prev_d = device_driver_default.temp_prev_d;

    deviceIN->measureByte = device_driver_default.measureByte;
    deviceIN->byteCount = device_driver_default.byteCount;
    deviceIN->bitCount = device_driver_default.bitCount;
    deviceIN->sourceByte = device_driver_default.sourceByte;

    deviceIN->switchingFrequency = device_driver_default.switchingFrequency;
    deviceIN->dutyCycle = device_driver_default.dutyCycle;
    deviceIN->sourceFrequency = device_driver_default.sourceFrequency;

    deviceIN->step_count = device_driver_default.step_count;
    deviceIN->position = device_driver_default.position;

}


/* [] END OF FILE */

