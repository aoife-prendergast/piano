/*
 * Math_Utilities.c
 *
 *  Created on: Sep 9, 2024
 *      Author: SMoore4
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#include <stdio.h>
#include <math.h>
#include "Math_Utilities.h"

uint32_t floatToDigitalCode(float valueMin, float valueIn, float valueMax, uint32_t codeMax, uint32_t codeBits){
    float cm = 0.0;  // default to 0
    if(codeMax == 0){
        cm = (float)((2^codeBits)-1);  //doing it the hard, costly way
    }
    else{
        cm = (float)codeMax;  // the easy way
    }

    int32_t code = (int32_t)floor((valueIn-valueMin) / (valueMax-valueMin) * (cm));    // TODO check if this type cast is correct
    return (uint32_t)(code);
}

float digitalCodeToFloat(float valueMin, uint32_t codeIn, float valueMax, uint32_t codeMax, uint32_t codeBits){
    float cm = 0.0;  // default to 0
    if(codeMax == 0){
        cm = (float)(2^codeBits)-1;  //doing it the hard, costly way
    }
    else{
        cm = (float)codeMax;  // the easy way
    }

    float valueOut = (((float)(codeIn)/cm)*(valueMax-valueMin))+ valueMin;
    return valueOut;
}


// original: https://stackoverflow.com/questions/24420246/c-function-to-convert-float-to-byte-array
// the idea is that the float and byte array occupy the same memory location, therefore are equal
void floatToByteArray(uint8_t bytes_temp[4],float float_variable){
  union {
    float a;
    unsigned char bytes[4];
  } thing;
  thing.a = float_variable;
  memcpy(bytes_temp, thing.bytes, 4);
}
// super-hack alternative
//void float2Bytes(byte bytes_temp[4],float float_variable){
//  memcpy(bytes_temp, (unsigned char*) (&float_variable), 4);
//}

// this looks like it works with the floatToByteArray to read a float from EEPROM
float byteArrayToFloat(uint8_t bytes_temp[4]){
   union {
    float a;
    unsigned char bytes[4];
  } thing;
  memcpy(thing.bytes, bytes_temp, 4);

  return thing.a;
}



void int16ToByteArray(uint8_t bytes_temp[2],int16_t int_variable){
  union {
    int16_t a;
    unsigned char bytes[2];
  } thing;
  thing.a = int_variable;
  memcpy(bytes_temp, thing.bytes, 2);
}

int16_t byteArrayToInt16(uint8_t bytes_temp[2]){
   union {
    int16_t a;
    unsigned char bytes[2];
  } thing;
  memcpy(thing.bytes, bytes_temp, 2);

  return thing.a;
}
void int32ToByteArray(uint8_t bytes_temp[4],int32_t int_variable){
  union {
    int32_t a;
    unsigned char bytes[4];
  } thing;
  thing.a = int_variable;
  memcpy(bytes_temp, thing.bytes, 4);
}
int32_t byteArrayToInt32(uint8_t bytes_temp[4]){
   union {
    int32_t a;
    unsigned char bytes[4];
  } thing;
  memcpy(thing.bytes, bytes_temp, 4);

  return thing.a;
}

void uint16ToByteArray(uint8_t bytes_temp[2],uint16_t uint_variable){
  union {
    uint16_t a;
    unsigned char bytes[2];
  } thing;
  thing.a = uint_variable;
  memcpy(bytes_temp, thing.bytes, 2);
}
uint16_t byteArrayToUInt16(uint8_t bytes_temp[2]){
   union {
    uint16_t a;
    unsigned char bytes[2];
  } thing;
  memcpy(thing.bytes, bytes_temp, 2);

  return thing.a;
}
void uint32ToByteArray(uint8_t bytes_temp[4],uint32_t uint_variable){
  union {
    uint32_t a;
    unsigned char bytes[4];
  } thing;
  thing.a = uint_variable;
  memcpy(bytes_temp, thing.bytes, 4);
}
uint32_t byteArrayToUInt32(uint8_t bytes_temp[4]){
   union {
    uint32_t a;
    unsigned char bytes[4];
  } thing;
  memcpy(thing.bytes, bytes_temp, 4);

  return thing.a;
}




// TODO: test this - DS 2020-07-15
unsigned long hashString(unsigned char *str){
    unsigned long hash = 5381;
    int c = 0;

    while (c == *str++)
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

    return hash;
}


_Bool compareArray(uint8_t *buffer, uint8_t *buffercmp, int size){
    _Bool result = true;
    for(int i=0; i<size; i++){
        if(buffer[i] != buffercmp[i]){
            result = false;
            break;              // end loop if false found
        }
    }
    return result;
}

float convertADCreadToFloat(uint32_t data, float vref, int gain, _Bool polarity, uint32_t codeMax){
    float max;
    float min;
    float value;


    //check if bipolar to set min and max
    if(polarity == POLARITY_BIPOLAR){
        value = (((float)(data)/(float)(0x800000))-1)*(vref/gain);
    }
    else{
        min = 0.0;
        max = vref/gain;
        value = digitalCodeToFloat(min, data, max, codeMax, 0);
    }
    return value;
}
//requires lookup table with searchColumn ordered numerically increasing
//TODO find a way to get size of lookup table instead of passing it in
float useFloatLookUpTable(float lookUpTable[][2], float valueIN, int searchColumn, int returnColumn, int size, int seed){
    int rowIndex;
    for(rowIndex = 0; rowIndex < size; rowIndex++){
        if(valueIN < lookUpTable[rowIndex][searchColumn]){
            break;
        }
    }
    if( fabs(valueIN-lookUpTable[rowIndex-1][searchColumn]) < fabs(lookUpTable[rowIndex][searchColumn]-valueIN)){
        rowIndex = rowIndex-1;
    }
    if(rowIndex<0)rowIndex=0;
    return lookUpTable[rowIndex][returnColumn];
}

_Bool isDigitPolar(char ch){
    return ch == '-' || isdigit(ch);
}

float L11ToFloat(uint16_t valueIn){
    // extract exponent as MS 5 bits
    int8_t exponent = valueIn >> 11;
    // extract mantissa as LS 11 bits
    int16_t mantissa = valueIn & 0x7ff;
    // sign extend exponent from 5 to 8 bits
    if( exponent > 0x0F ) exponent |= 0xE0;
    // sign extend mantissa from 11 to 16 bits
    if( mantissa > 0x03FF ) mantissa |= 0xF800;
    // compute value as mantissa * 2^(exponent)
    return mantissa * pow(2,exponent);

}

uint16_t floatToL11(float valueIn){
    // set exponent to -16
    int exponent = -16;
    // extract mantissa from input value
    int mantissa = (int)(valueIn / pow(2.0, exponent));
    // Search for an exponent that produces
    // a valid 11-bit mantissa
    do{
        if((mantissa >= -1024) &&(mantissa <= +1023)){
           break; // stop if mantissa valid
        }
        exponent++;
        mantissa =(int)(valueIn / pow(2.0, exponent));
    } while (exponent < +15);
    // Format the exponent of the L11
    uint16_t uExponent = exponent << 11;
    // Format the mantissa of the L11
    uint16_t uMantissa = mantissa & 0x07FF;
    // Compute value as exponent | mantissa
    return uExponent | uMantissa;

}

// TODO
// Test that this has the correct Endian orientation
void uint8_tToCharArray(char * char_array, uint8_t uint8_t_variable){
    int bit = 0;
    int i = 7;

    for(i=7; i>=0; i--){
        bit = (uint8_t_variable>>i) & 0b1;
        char_array[i] = bit;
        // this may be backwards and it may actually need to be:
        // char_array[7-i] = bit;
    }
}

// return true if in1 == in2 for a given length
_Bool verifyUintEquality(uint32_t in1, uint32_t in2, int length){
    switch(length){
        case 1: return ((uint8_t)in1 == (uint8_t)in2) ;
        case 2: return ((uint16_t)in1 == (uint16_t)in2) ;
        case 3: return ((in1&0x00FFFFFF) == (in2&0x00FFFFFF)) ;     // mask off first byte
        case 4: return (in1 == in2) ;
        default: return false; // unnaceptable length
    }
}

uint32_t getUint32Mask(int length){
    switch(length){
        case 1:  return 0x000000FF;
        case 2:  return 0x0000FFFF;
        case 3:  return 0x00FFFFFF;
        case 4:  return 0xFFFFFFFF;
        default: return 0x00000000;
    }
}

int32_t int32Min(int32_t x, int32_t y){
    return (x>y) ? y : x;
}
int32_t int32Max(int32_t x, int32_t y){
    return (x>y) ? x : y;
}

float floatMin(float x, float y){
    return (x>y) ? y : x;
}
float floatMax(float x, float y){
    return (x>y) ? x : y;
}

float floatBound(float x, float min, float max){
    if(max >= min){
        return floatMin(max, floatMax(x, min));
    }
    else{
        return x;
    }
}


/* [] END OF FILE */
