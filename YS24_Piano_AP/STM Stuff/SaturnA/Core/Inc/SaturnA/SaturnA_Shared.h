/*
* @file VulcanE_Shared.h
* @brief Contains the important bits of shared code between both cores, primarily defines and utilities
*
* @version 1.0.0

* @author Timothy Volpe
* @copyright Analog Devices Inc. 2022
*
*/

#ifndef TRUE
    /** @brief The value of TRUE is the integer 0. */
    #define TRUE 1
//#elif
//    #warning TRUE was already defined, best to make sure that is is defined was what we expect (1)!
#endif
#ifndef FALSE
    /** @brief The value of FALSE is the integer 0. */
    #define FALSE 0
//#elif
//    #warning FALSE was already defined, best to make sure that is is defined was what we expect (0)!
#endif

#ifndef NULL
    /** @brief NULL is 0, or null pointer. Should only be used in the context of pointers to avoid confusion. */
    #define NULL 0
#endif

#ifndef COMPLETE
    /** @brief Used for functions that return 0 integer on success or error code on failure. */
    #define COMPLETE 0
#endif

/** @brief Because functions return FALSE on success (no error), this is defined this way. */
#define VNO_ERROR FALSE

/** @brief Vulcan error, TRUE means an error occured. Not defined as just "ERROR" because thats probably already used. */
#define VERROR TRUE

//////////////////////
// Program Metadata //
//////////////////////

/** @brief Manufacturer, should always be ADI? */
#define VULCAN_MANUFACTURER    "ADI"
/** @brief Hardware model intended for this firmware to run on. */
#define VULCAN_MODEL           "VULCANE"
/**
 * @brief Default serial number string... not sure if this is actually used.
 * @deprecated The previous versions of firmware return an empty string if serial number is not defined,
 * so it seems as if this is not used.
*/
#define VULCAN_DEFAULT_SN      "DEFAULT_SN"
/** @brief The firmware version string. Should always follow the format of '[Firmware Name] [Version String]' */
#define VULCAN_FIRMWARE        "VulcanE v1.0.0"

////////////////
// Semaphores //
////////////////

/** @brief Semaphores 0-15 are reserved, so start at 16. */
#define SEMAPHORE_BASE      16
/** @brief Semaphore for core initialization sync (first stage). */
#define SEMAPHORE_INIT1      SEMAPHORE_BASE+0
/** @brief Semaphore for core initialization sync (second stage). */
#define SEMAPHORE_INIT2      SEMAPHORE_BASE+1
/** @brief Semaphore for hard fault, so that LED blinks only come from one core. */
#define SEMAPHORE_HARD_FAULT SEMAPHORE_BASE+2
