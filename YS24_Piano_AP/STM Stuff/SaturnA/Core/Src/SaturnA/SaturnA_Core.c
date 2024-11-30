/*
 * SCPI_Parser.c
 *
 *  Created on: Sep 5, 2024
 *      Author: SMoore4
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <SaturnA/SaturnA.h>
#include <SaturnA/SaturnA_Core.h>
#include <SaturnA/SaturnA_Shared.h>

#include "SCPI_Parser.h"

#include <spi.h>


/***************************************************************************/
// Variables 
/***************************************************************************/
UART_HandleTypeDef huart_core;

uint8_t format_local[64];
//uint8 format_usb[64];

uint8_t rawBuffer[RD_BUFFER_LEN];
uint8_t rdBuffer[RD_BUFFER_LEN];
uint8_t rdBuffer2[RD_BUFFER_LEN];

// not sure if these belong here 
_Bool validData = FALSE;
_Bool error = FALSE;

// For testing
#define rx_buff_size_set 64
uint8_t rx_size_max = 64;
uint8_t *rx_size = &rx_size_max;; // Works - uint8_t *rx_size = &rx_size_max;
uint8_t tx_buff[13]= "Hi everyone\n\r";
uint8_t newline[2]= "\n\r";


uint8_t rx_buff[rx_buff_size_set];

uint8_t send_chars[5];


/***************************************************************************/

/***************************************************************************/

_Bool Core1_Initialize(UART_HandleTypeDef *huart_parse)
{
    //initializeDrivers();
    
    // ******************* COMS **********************/
    /* Start the USB UART peripheral */
	huart_core = *huart_parse;
	SCPI_Initialize(&huart_core);
	initializeSaturn();
    
    // SPI Init
	// Done in Main by default - Not done yet
    

    // ***************** STM32 - Future work *********************/
    
//    ISUPPLY_InitializeAll();
//    VSUPPLY_InitializeAll();
//    MSUPPLY_Initialize();

//    initializeVulcan();
//    initializeDrivers();
//    ADC_InitializeAll();

//    TSUPPLY_InitializeAll();
    
    return SUCCESS;
}

_Bool Core1_Loop()
{
    error = FALSE;
    validData = FALSE;
    _Bool noRespond = FALSE;

    *rx_size = 64;

    memset(rx_buff, 0, sizeof(rx_buff)); // clear buffers


    //memset(rawBuffer, 0, RD_BUFFER_LEN); // clear buffers
    //memset(rdBuffer, 0, RD_BUFFER_LEN);
    //memset(format_local, 0, RD_BUFFER_LEN);
    //memset(format_usb, 0, RD_BUFFER_LEN);
    
            // Commenting out for now :) - AP 
            /*
            // Host can send double SET_INTERFACE request.
            // Initialize IN endpoints when device is configured.
            if ((0u != USBUART_IsConfigurationChanged()) && (0u != USBUART_GetConfiguration())){
                    USBUART_CDC_Init();  // Enumeration is done, enable OUT endpoint to receive data from host.
            }          
            if((UART_RS485RX_GetRxBufferSize()!= 0u) ||
            ((0u != USBUART_GetConfiguration()) && (0u != USBUART_DataIsReady())) ){
            */
    
    // Test for serial loopback on STM32-G4
    if(Saturn_UART_Receive(&huart_core, rx_buff, rx_size, 1000)==HAL_OK) //if transfer is successful
	{
	  //HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_7);
    	if(!error) {
			strlcpy(rdBuffer, rx_buff, RD_BUFFER_LEN);        // sanitize RAW buffer to just 64 bytes to prevent buffer overflows

			// Normal Flow for SCPI Parser
			error = SaturnParseAndExecuteSCPI(rdBuffer);        // parse the serial data

			// Testing of SPI - Comment out SCPI Parser above
//			uint8_t byte1 = 0x10;
//			uint8_t byte2 = 0x86;
//			uint8_t byte3 = 0x00;
//			HAL_SPI_Transmit(&hspi2, byte1, sizeof(byte1), 1000);
//			HAL_SPI_Transmit(&hspi2, byte2, sizeof(byte2), 1000);
//			HAL_SPI_Transmit(&hspi2, byte3, sizeof(byte3), 1000);
////			HAL_SPI_TransmitReceive(&hspi2, rdBuffer, rdBuffer2,
////			            			strlen(rdBuffer), 1000);
//			HAL_UART_Transmit(&huart_core, rdBuffer, strlen(rdBuffer), 1000);

			// Send an acknowledge packet for write commands
			if( !error)
			{
				// Free for use if debugging needed
			}
		}

	  //HAL_UART_Transmit(&huart_core, rx_buff, *rx_size, 1000);

	}

    // Vulcan original Code
//    if(HAL_UART_Receive(&huart_core, RD_BUFFER_LEN, sizeof(RD_BUFFER_LEN), 1000)==HAL_OK)
//    {
//
//    	//Vulcan Code
////        // If its USB Serial Data -> Get the data...
////        if(Cy_USB_Dev_CDC_IsDataReady(USBUART_COM_PORT, &USBUART_cdcContext) != 0u)
////        {
////            instruction.serialHardware = SERIAL_HARDWARE_USB;
////            Cy_USB_Dev_CDC_GetAll(USBUART_COM_PORT, rawBuffer, USBUART_BUFFER_SIZE, &USBUART_cdcContext);
////            validData = TRUE;
////
////        }
////        else {
////            // never gets here
////        }
//
//
//        if(!error) {
//            strlcpy(rdBuffer, rawBuffer, RD_BUFFER_LEN);        // sanitize RAW buffer to just 64 bytes to prevent buffer overflows
//            error = SaturnParseAndExecuteSCPI(rdBuffer);        // parse the serial data
//
//            // Send an acknowledge packet for write commands
//            if( !error)
//            {
//            	// Free for use if debugging needed
//            }
//        }
//    }
    
    return SUCCESS;
}
