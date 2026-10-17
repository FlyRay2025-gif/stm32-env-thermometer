#ifndef __DS18B20_H
#define __DS18B20_H

#include "stm32f10x.h"

void DS18B20_Init(void);
void DS18B20_StartConv(void);
uint8_t DS18B20_ReadTemp(float *pTemp);

#endif
