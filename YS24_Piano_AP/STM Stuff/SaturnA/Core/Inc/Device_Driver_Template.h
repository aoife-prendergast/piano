/*
 * Device_Driver_Template.h
 *
 *  Created on: Sep 9, 2024
 *      Author: SMoore4
 */

#ifndef INC_DEVICE_DRIVER_TEMPLATE_H_
#define INC_DEVICE_DRIVER_TEMPLATE_H_

#include <stdio.h>


//Device Ennumeration
//add 1 to physical number of supplies in order to 1-index, not 0-index
#define ADATE324_VSUPPLIES          3+1
#define ADATE324_ISUPPLIES          0+1
#define ADATE324_TSUPPLIES          1+1
#define ADATE324_ADCS               1+1
#define ADATE324_LEDS               1+1
#define ADATE324_ARBITRARIES        0+1
#define ADATE324_GPIO_PORTS         1+1
#define ADATE324_MEMORY_DEVS        1+1
#define ADATE324_JTAG_DEVS          0+1
#define ADATE324_SPI_DEVS           1+1

#define DEVICE_STATUS_NA            (int)-1
#define DEVICE_STATUS_BAD           (int)0
#define DEVICE_STATUS_GOOD          (int)1

// -- BEGIN -- device_driver typedef
typedef struct device_error device_error;
struct device_error {
    _Bool error;
    uint16_t errorCode;
};

// -- BEGIN -- device_driver typedef
typedef struct device_driver device_driver;
struct device_driver {
    int status;
    _Bool actionable;
    _Bool outputStateON;
    uint8_t mode;

    float sourcePowerMin;
    float sourceVoltMin;
    float sourceCurrentMin;
    float sourceTemperatureMin;

    float sourcePower;
    float sourceVolt;
    float sourceCurrent;
    float sourceTemperature;

    float sourcePowerMax;
    float sourceVoltMax;
    float sourceCurrentMax;
    float sourceTemperatureMax;

    float calOffsetPower;
    float calOffsetVolt;
    float calOffsetCurrent;
    float calOffsetTemperature;

    float calGainPower;
    float calGainVolt;
    float calGainCurrent;
    float calGainTemperature;

    float tolerancePower;
    float toleranceVolt;
    float toleranceCurrent;
    float toleranceTemperature;

    float measurePower;
    float measureVolt;
    float measureCurrent;
    float measureTemperature;
    float measureFrequency;

    // new stuff after this
    //float temp_prev_i;
    //float temp_prev_d;

    uint8_t measureByte;
    int byteCount;
    int bitCount;
    uint8_t sourceByte;
    uint8_t sourceBytes[8];

    float switchingFrequency;
    float dutyCycle;
    float sourceFrequency;

    int step_count;
    float position;
};
// -- END -- device_driver typedef

// -- BEGIN -- site_driver typedef
typedef struct site_driver site_driver;
struct site_driver {
    device_driver Dev_VSUPPLY[ADATE324_VSUPPLIES];
    device_driver Dev_ISUPPLY[ADATE324_ISUPPLIES];
    device_driver Dev_TSUPPLY[ADATE324_TSUPPLIES];
    device_driver Dev_MSUPPLY[2];
    device_driver Dev_ADC[ADATE324_ADCS];
    device_driver Dev_LED[ADATE324_LEDS];
    device_driver Dev_ARBITRARY[ADATE324_ARBITRARIES];
    device_driver Dev_GPIO_PORT[ADATE324_GPIO_PORTS];
    device_driver Dev_MEMORY[ADATE324_MEMORY_DEVS];
    device_driver Dev_JTAG[ADATE324_JTAG_DEVS];
    device_driver Dev_SPI[ADATE324_SPI_DEVS];
};

// -- END -- device_driver typedef

// totally disabled, all gain offsets at 1.0, everything else at 0.0
static const device_driver device_driver_default = {
    DEVICE_STATUS_NA,
    false,
    false,
    0,

    0.0,0.0,0.0,0.0,
    0.0,0.0,0.0,0.0,
    0.0,0.0,0.0,0.0,

    0.0,0.0,0.0,0.0,
    1.0,1.0,1.0,1.0,1.0,
    0.0,0.0,0.0,0.0,

    0.0,0.0,0.0,0.0,

    //0.0,0.0,

    0x00, 0, 0, 0x00,0x00,
    0.0,0.0,0.0,
    0, 0.0

};


//*******************************************************************************

void device_driver_initialize(device_driver * deviceIN);

#endif /* INC_DEVICE_DRIVER_TEMPLATE_H_ */
