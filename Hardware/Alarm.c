#include "stm32f10x.h"
#include "Alarm.h"

/*=============================================================
 * 报警模块
 * 蜂鸣器：PA6 = TIM3_CH1，输出 2kHz PWM，经 S8050 三极管驱动
 *         无源蜂鸣器需要方波驱动，频率可用软件调整
 * 报警灯：PA7 推挽输出，高电平点亮
 * 消音方式：比较值写 0（输出恒为低电平），不反复开关定时器
 *=============================================================*/

static uint8_t alarmOn = 0;

/**
  * @brief  报警模块初始化（蜂鸣器 PWM + 报警 LED）
  */
void Alarm_Init(void)
{
	GPIO_InitTypeDef GPIO_InitStructure;
	TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
	TIM_OCInitTypeDef TIM_OCInitStructure;

	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE);

	/* PA6：复用推挽输出（TIM3_CH1） */
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);

	/* PA7：报警 LED */
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_7;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	GPIO_ResetBits(GPIOA, GPIO_Pin_7);

	/* TIM3 时基：72MHz / 36 / 1000 = 2kHz */
	TIM_TimeBaseStructure.TIM_Prescaler = 36 - 1;
	TIM_TimeBaseStructure.TIM_Period = 1000 - 1;
	TIM_TimeBaseStructure.TIM_ClockDivision = TIM_CKD_DIV1;
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;
	TIM_TimeBaseInit(TIM3, &TIM_TimeBaseStructure);

	/* PWM 输出通道 1 */
	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;
	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable;
	TIM_OCInitStructure.TIM_Pulse = 0;					/* 初始静音 */
	TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High;
	TIM_OCInitStructure.TIM_OCIdleState = TIM_OCIdleState_Reset;
	TIM_OCInitStructure.TIM_OCNIdleState = TIM_OCNIdleState_Reset;
	TIM_OC1Init(TIM3, &TIM_OCInitStructure);
	TIM_OC1PreloadConfig(TIM3, TIM_OCPreload_Enable);

	TIM_Cmd(TIM3, ENABLE);
}

/**
  * @brief  报警判断与输出（带 0.5℃ 回差，防止阈值边界反复抖动）
  * @param  temp      当前温度
  * @param  threshold 报警阈值
  */
void Alarm_Update(float temp, float threshold)
{
	if (alarmOn)
	{
		if (temp < threshold - ALARM_HYST)	/* 已报警：低于（阈值-回差）才解除 */
		{
			alarmOn = 0;
		}
	}
	else
	{
		if (temp > threshold)				/* 未报警：超过阈值才触发 */
		{
			alarmOn = 1;
		}
	}

	if (alarmOn)
	{
		TIM_SetCompare1(TIM3, 500);			/* 50% 占空比，蜂鸣器响 */
		GPIO_SetBits(GPIOA, GPIO_Pin_7);	/* 报警灯亮 */
	}
	else
	{
		TIM_SetCompare1(TIM3, 0);			/* 静音 */
		GPIO_ResetBits(GPIOA, GPIO_Pin_7);	/* 报警灯灭 */
	}
}

/**
  * @brief  查询当前是否处于报警状态
  * @retval 0：正常   1：报警中
  */
uint8_t Alarm_IsOn(void)
{
	return alarmOn;
}
