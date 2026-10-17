#ifndef __ALARM_H
#define __ALARM_H

#include "stm32f10x.h"

#define ALARM_HYST   0.5f		/* 报警回差（℃） */

void Alarm_Init(void);
void Alarm_Update(float temp, float threshold);
uint8_t Alarm_IsOn(void);

#endif
