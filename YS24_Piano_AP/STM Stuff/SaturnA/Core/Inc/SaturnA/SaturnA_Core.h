/*
 * STM32_Core.h
 *
 *  Created on: Sep 5, 2024
 *      Author: SMoore4
 */

#ifndef SRC_STM32_CORE_H_
#define SRC_STM32_CORE_H_

#include <stm32g4xx.h>

#define RD_BUFFER_LEN           (64u)
#define WR_BUFFER_LEN           (64u)


/**
 * @brief Initialize resources used by Core 1, this is called after Core 0 is already fully initialized.
 * @details If an error occurred, the application will halt with a fault.
 * @returns False if operations completed successfully, or True if there was an error.
 */
_Bool Core1_Initialize(UART_HandleTypeDef *huart_parse);

/**
 * @brief Application loop on core 1
 * @details This is the application loop on core 0 which runs continuously if both cores initialized successfully.
 * Core 1 main purpose is to loop and check for any recieved commands through USBUART or RS485 connections...
 * @warning Returning True from this function will cause a hard fault, which is only recoverable by resetting the PSoC. Use sparingly!
 * @returns True if there was an error that caused the loop to break, otherwise return False
 */
_Bool Core1_Loop();


#endif /* SRC_STM32_CORE_H_ */
