#include "stm32f10x.h"
#include "Key.h"
#include "Delay.h"

/*=============================================================
 * 按键驱动（轮询方式）
 * PB12 = KEY_SET   PB13 = KEY_+   PB14 = KEY_-
 * 按键另一端接 GND，引脚内部上拉：未按下读 1，按下读 0
 * 消抖：检测到按下后延时 20ms 复检，等待松手再返回键码
 *=============================================================*/

#define KEY_SET   GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_12)
#define KEY_UP    GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_13)
#define KEY_DOWN  GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_14)

/**
  * @brief  按键初始化（上拉输入）
  */
void Key_Init(void)
{
	GPIO_InitTypeDef GPIO_InitStructure;

	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);

	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_12 | GPIO_Pin_13 | GPIO_Pin_14;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure);
}

/**
  * @brief  获取键码（含消抖）
  * @retval 0 = 无按键   1 = SET   2 = +   3 = -
  */
uint8_t Key_GetNum(void)
{
	uint8_t num = 0;

	if (KEY_SET == 0)
	{
		Delay_ms(20);
		if (KEY_SET == 0)
		{
			num = 1;
			while (KEY_SET == 0);	/* 等待松手，一次按下只产生一个键码 */
		}
	}
	else if (KEY_UP == 0)
	{
		Delay_ms(20);
		if (KEY_UP == 0)
		{
			num = 2;
			while (KEY_UP == 0);
		}
	}
	else if (KEY_DOWN == 0)
	{
		Delay_ms(20);
		if (KEY_DOWN == 0)
		{
			num = 3;
			while (KEY_DOWN == 0);
		}
	}

	return num;
}
