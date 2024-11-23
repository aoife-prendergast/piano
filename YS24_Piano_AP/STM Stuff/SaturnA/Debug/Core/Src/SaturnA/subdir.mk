################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/SaturnA/SaturnA.c \
../Core/Src/SaturnA/SaturnA_Core.c \
../Core/Src/SaturnA/SaturnA_Device_ADC.c \
../Core/Src/SaturnA/SaturnA_Device_GPIO.c \
../Core/Src/SaturnA/SaturnA_Device_SPI.c 

OBJS += \
./Core/Src/SaturnA/SaturnA.o \
./Core/Src/SaturnA/SaturnA_Core.o \
./Core/Src/SaturnA/SaturnA_Device_ADC.o \
./Core/Src/SaturnA/SaturnA_Device_GPIO.o \
./Core/Src/SaturnA/SaturnA_Device_SPI.o 

C_DEPS += \
./Core/Src/SaturnA/SaturnA.d \
./Core/Src/SaturnA/SaturnA_Core.d \
./Core/Src/SaturnA/SaturnA_Device_ADC.d \
./Core/Src/SaturnA/SaturnA_Device_GPIO.d \
./Core/Src/SaturnA/SaturnA_Device_SPI.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/SaturnA/%.o Core/Src/SaturnA/%.su Core/Src/SaturnA/%.cyclo: ../Core/Src/SaturnA/%.c Core/Src/SaturnA/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32G431xx -c -I../Core/Inc -I../Drivers/STM32G4xx_HAL_Driver/Inc -I../Drivers/STM32G4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32G4xx/Include -I../Drivers/CMSIS/Include -Ofast -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src-2f-SaturnA

clean-Core-2f-Src-2f-SaturnA:
	-$(RM) ./Core/Src/SaturnA/SaturnA.cyclo ./Core/Src/SaturnA/SaturnA.d ./Core/Src/SaturnA/SaturnA.o ./Core/Src/SaturnA/SaturnA.su ./Core/Src/SaturnA/SaturnA_Core.cyclo ./Core/Src/SaturnA/SaturnA_Core.d ./Core/Src/SaturnA/SaturnA_Core.o ./Core/Src/SaturnA/SaturnA_Core.su ./Core/Src/SaturnA/SaturnA_Device_ADC.cyclo ./Core/Src/SaturnA/SaturnA_Device_ADC.d ./Core/Src/SaturnA/SaturnA_Device_ADC.o ./Core/Src/SaturnA/SaturnA_Device_ADC.su ./Core/Src/SaturnA/SaturnA_Device_GPIO.cyclo ./Core/Src/SaturnA/SaturnA_Device_GPIO.d ./Core/Src/SaturnA/SaturnA_Device_GPIO.o ./Core/Src/SaturnA/SaturnA_Device_GPIO.su ./Core/Src/SaturnA/SaturnA_Device_SPI.cyclo ./Core/Src/SaturnA/SaturnA_Device_SPI.d ./Core/Src/SaturnA/SaturnA_Device_SPI.o ./Core/Src/SaturnA/SaturnA_Device_SPI.su

.PHONY: clean-Core-2f-Src-2f-SaturnA

