/*
 * Math_Utilities.h
 *
 *  Created on: Sep 9, 2024
 *      Author: SMoore4
 */

#ifndef INC_MATH_UTILITIES_H_
#define INC_MATH_UTILITIES_H_

//#define SPI_MODE_0      0b00

//digital to analog code conversion constants
#define CODE_MAX_8_BIT      0xFF
#define CODE_MAX_12_BIT     0xFFF
#define CODE_MAX_16_BIT     0xFFFF
#define CODE_MAX_24_BIT     0xFFFFFF

//Polarity Defines
#define POLARITY_UNIPOLAR            0b0
#define POLARITY_BIPOLAR             0b1

/***************************************
*        Function Prototypes
***************************************/

uint32_t floatToDigitalCode(float valueMin, float valueIn, float valueMax, uint32_t codeMax, uint32_t codeBits);
float digitalCodeToFloat(float valueMin, uint32_t codeIn, float valueMax, uint32_t codeMax, uint32_t codeBits);

float convertADCreadToFloat(uint32_t data, float vref, int gain, _Bool polarity, uint32_t codeMax);

float useFloatLookUpTable(float lookUpTable[][2], float valueIN, int searchColumn, int returnColumn, int size, int seed);

void floatToByteArray(uint8_t bytes_temp[4],float float_variable);
float byteArrayToFloat(uint8_t bytes_temp[4]);

void int16ToByteArray(uint8_t bytes_temp[2],int16_t int_variable);
int16_t byteArrayToInt16(uint8_t bytes_temp[2]);
void int32ToByteArray(uint8_t bytes_temp[4],int32_t int_variable);
int32_t byteArrayToInt32(uint8_t bytes_temp[4]);

void uint16ToByteArray(uint8_t bytes_temp[2],uint16_t uint_variable);
uint16_t byteArrayToUInt16(uint8_t bytes_temp[2]);
void uint32_tToByteArray(uint8_t bytes_temp[4],uint32_t uint_variable);
uint32_t byteArrayTouint32_t(uint8_t bytes_temp[4]);


unsigned long hashString(unsigned char *str);

_Bool compareArray(uint8_t *buffer, uint8_t *buffercmp, int size);

_Bool isDigitPolar(char ch);


//Lienar_5s_11s conversions

float L11ToFloat(uint16_t valueIn);

uint16_t floatToL11(float valueIn);

void uint8_tToCharArray(char * char_array, uint8_t uint8_t_variable);

_Bool verifyUintEquality(uint32_t in1, uint32_t in2, int length);
uint32_t getuint32_tMask(int length);

int32_t int32Min(int32_t x, int32_t y);
int32_t int32Max(int32_t x, int32_t y);

float floatMin(float x, float y);
float floatMax(float x, float y);
float floatBound(float x, float min, float max);

// Added by Sean Moore


#endif /* INC_MATH_UTILITIES_H_ */
