#include "stm32f10x.h"
#include <stdio.h>
#include "Delay.h"
#include "OLED.h"
#include "DS18B20.h"
#include "Key.h"
#include "Alarm.h"
#include "Uart.h"

/*=============================================================
 * 环境温度测量仪（基础版）
 * ------------------------------------------------------------
 * 功能：
 *   1. DS18B20 采集环境温度，5 点滑动平均滤波
 *   2. LM35 第二测温通道：输出经 R9 100Ω 直接接 PA4（ADC1_IN4），
 *      按 T = V / 0.01 反算（10 mV/℃），每次读取连采 16 次取平均
 *   3. OLED 显示两路温度 / 报警阈值 / 报警状态
 *   4. 温度超过阈值 -> 蜂鸣器 + LED 报警（带 0.5℃ 回差）
 *   5. 按键修改阈值：SET 进入设置模式，+ / - 调整
 *   6. 串口每秒输出一行数据（调试用）
 *
 * 硬件接线：
 *   DS18B20   DQ->PA1   VCC->3.3V  GND->GND
 *   LM35      OUT->R9 100Ω->PA4      VCC->5V  GND->GND（LM35 必须用 5V）
 *   C3        100nF 接在 PA4 与 GND 之间（抗混叠；不用运放，直接采样）
 *   OLED      SCL->PB6  SDA->PB7   VCC->3.3V  GND->GND
 *   蜂鸣器    PA6 -> 1k 电阻 -> S8050 基极（发射极接 GND）
 *   报警 LED  PA7 -> 1k 电阻 -> LED 正极，LED 负极接 GND
 *   按键      PB12 / PB13 / PB14 -> 按键 -> GND（内部上拉）
 *   心跳灯    PC13 板载 LED（无需接线）
 *   串口      PA9 / PA10（板载 CH340，USB 直接可用）
 *=============================================================*/

#define FILTER_N   5				/* 滑动平均窗口长度 */

static float   tempBuf[FILTER_N];	/* 采样缓冲（环形） */
static uint8_t bufIndex = 0;		/* 环形缓冲写指针 */
static float   tempFiltered = 0.0f;	/* DS18B20 滤波后的温度 */
static float   lm35Temp = 0.0f;		/* LM35 温度（直连 PA4，16 次平均） */
static float   threshold = 30.0f;	/* 报警阈值，默认 30.0℃ */
static uint8_t setMode = 0;			/* 0 = 运行模式   1 = 阈值设置模式 */

/**
  * @brief  滑动平均滤波：新采样值入缓冲，返回窗口内平均值
  */
static float Filter_Update(float newTemp)
{
	uint8_t i;
	float sum = 0.0f;

	tempBuf[bufIndex] = newTemp;
	bufIndex = (bufIndex + 1) % FILTER_N;

	for (i = 0; i < FILTER_N; i++)
	{
		sum += tempBuf[i];
	}

	return sum / FILTER_N;
}

/*---------------- LM35 采集（ADC1_IN4 / PA4，直接采样） ----------------
 * LM35 输出 10 mV/℃，经 R9 100Ω 直接接 PA4（PA4 节点带 C3 100nF 抗混叠）
 * 反推温度：T(℃) = V / 0.01（0℃ → 0.000V；25℃ → 0.250V；50℃ → 0.500V）
 * 每次读取连采 16 次取平均，抑制 ADC 噪声
 *------------------------------------------------------------------------*/

/**
  * @brief  LM35 通道初始化（PA4 模拟输入 + ADC1 校准）
  */
static void LM35_Init(void)
{
	GPIO_InitTypeDef GPIO_InitStructure;
	ADC_InitTypeDef ADC_InitStructure;

	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA | RCC_APB2Periph_ADC1, ENABLE);
	RCC_ADCCLKConfig(RCC_PCLK2_Div6);					/* ADC 时钟 = 72MHz/6 = 12MHz */

	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AIN;		/* PA4：模拟输入 */
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_4;
	GPIO_Init(GPIOA, &GPIO_InitStructure);

	ADC_InitStructure.ADC_Mode = ADC_Mode_Independent;
	ADC_InitStructure.ADC_ScanConvMode = DISABLE;
	ADC_InitStructure.ADC_ContinuousConvMode = DISABLE;
	ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None;
	ADC_InitStructure.ADC_DataAlign = ADC_DataAlign_Right;
	ADC_InitStructure.ADC_NbrOfChannel = 1;
	ADC_Init(ADC1, &ADC_InitStructure);

	ADC_Cmd(ADC1, ENABLE);

	ADC_ResetCalibration(ADC1);							/* 上电复位校准 */
	while (ADC_GetResetCalibrationStatus(ADC1));
	ADC_StartCalibration(ADC1);							/* 启动校准 */
	while (ADC_GetCalibrationStatus(ADC1));
}

/**
  * @brief  单次 ADC 采样（通道 4，长采样时间，适合高阻小信号）
  */
static uint16_t LM35_ReadRaw(void)
{
	ADC_RegularChannelConfig(ADC1, ADC_Channel_4, 1, ADC_SampleTime_239Cycles5);
	ADC_SoftwareStartConvCmd(ADC1, ENABLE);
	while (ADC_GetFlagStatus(ADC1, ADC_FLAG_EOC) == RESET);

	return ADC_GetConversionValue(ADC1);
}

/**
  * @brief  读取 LM35 温度（16 次采样平均）
  * @retval 温度值（℃，低于 0℃ 按 0 处理）
  */
static float LM35_GetTemp(void)
{
	uint8_t i;
	uint32_t sum = 0;
	float vin, t;

	for (i = 0; i < 16; i++)
	{
		sum += LM35_ReadRaw();
	}

	vin = (float)sum / 16.0f * 3.3f / 4095.0f;			/* LM35 输出电压(V) */
	t = vin / 0.010f;									/* 反推 LM35 温度(℃) */

	if (t < 0.0f)
	{
		t = 0.0f;
	}

	return t;
}

/**
  * @brief  OLED 显示刷新（两路温度 / 阈值 / 状态 / 提示）
  * @param  t DS18B20 滤波后的温度
  */
static void Display_Update(float t)
{
	int16_t t100 = (int16_t)(t * 100.0f + (t >= 0 ? 0.5f : -0.5f));	/* DS18B20×100 */
	int16_t l10  = (int16_t)(lm35Temp * 10.0f + 0.5f);					/* LM35×10 */
	int16_t th10 = (int16_t)(threshold * 10.0f + 0.5f);					/* 阈值×10 */

	if (t100 > 9999)			/* 防止超量程显示异常 */
	{
		t100 = 9999;
	}
	if (l10 > 999)
	{
		l10 = 999;
	}

	/* 第 1 行：DS18B20 温度 xx.xx C */
	OLED_ShowString(1, 1, "DS18B20:");
	if (t100 < 0)
	{
		OLED_ShowString(1, 9, "-");
		t100 = -t100;
	}
	else
	{
		OLED_ShowString(1, 9, " ");
	}
	OLED_ShowNum(1, 10, (uint32_t)(t100 / 100), 2);
	OLED_ShowString(1, 12, ".");
	OLED_ShowNum(1, 13, (uint32_t)(t100 % 100), 2);
	OLED_ShowString(1, 15, "C");

	/* 第 2 行：LM35 温度 xx.x C */
	OLED_ShowString(2, 1, "LM35:   ");
	OLED_ShowNum(2, 9, (uint32_t)(l10 / 10), 2);
	OLED_ShowString(2, 11, ".");
	OLED_ShowNum(2, 12, (uint32_t)(l10 % 10), 1);
	OLED_ShowString(2, 14, " C");

	/* 第 3 行：报警阈值 + 状态 */
	OLED_ShowString(3, 1, "TH:  ");
	OLED_ShowNum(3, 6, (uint32_t)(th10 / 10), 2);
	OLED_ShowString(3, 8, ".");
	OLED_ShowNum(3, 9, (uint32_t)(th10 % 10), 1);
	if (Alarm_IsOn())
	{
		OLED_ShowString(3, 11, "ALARM ");
	}
	else
	{
		OLED_ShowString(3, 11, "NORMAL");
	}

	/* 第 4 行：按键提示（固定长度字符串，避免残留字符） */
	if (setMode)
	{
		OLED_ShowString(4, 1, "SET TH: K2+ K3-");
	}
	else
	{
		OLED_ShowString(4, 1, "K1:SET K2:+ K3:-");
	}
}

int main(void)
{
	GPIO_InitTypeDef GPIO_InitStructure;
	uint8_t key;
	uint8_t i;
	float rawTemp = 0.0f;
	int16_t t100, th10, l10;
	uint16_t count = 0;

	/* ---- 各模块初始化 ---- */
	OLED_Init();
	DS18B20_Init();
	LM35_Init();
	Key_Init();
	Alarm_Init();
	Uart_Init();

	/* PC13 板载 LED：心跳指示（低电平点亮，初始熄灭） */
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_13;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOC, &GPIO_InitStructure);
	GPIO_SetBits(GPIOC, GPIO_Pin_13);

	/* ---- 上电自检：读一次 DS18B20 填充滤波缓冲 ---- */
	OLED_ShowString(1, 1, "ENV Thermometer ");
	OLED_ShowString(2, 1, "Self-checking...");
	DS18B20_StartConv();
	Delay_ms(760);
	if (DS18B20_ReadTemp(&rawTemp))
	{
		for (i = 0; i < FILTER_N; i++)
		{
			tempBuf[i] = rawTemp;		/* 用首次数值预填充，避免上电后均值偏小 */
		}
		tempFiltered = rawTemp;
		OLED_ShowString(3, 1, "DS18B20 OK      ");
	}
	else
	{
		OLED_ShowString(3, 1, "DS18B20 ERROR!  ");
	}

	/* ---- 上电自检：读一次 LM35 ---- */
	lm35Temp = LM35_GetTemp();
	l10 = (int16_t)(lm35Temp * 10.0f + 0.5f);
	OLED_ShowString(4, 1, "LM35:           ");
	OLED_ShowNum(4, 7, (uint32_t)(l10 / 10), 2);
	OLED_ShowString(4, 9, ".");
	OLED_ShowNum(4, 10, (uint32_t)(l10 % 10), 1);
	OLED_ShowString(4, 12, "C");
	Delay_ms(800);
	OLED_Clear();

	/* ---- 主循环 ---- */
	while (1)
	{
		/* 1. 启动一次 DS18B20 温度转换（12 位精度，最长 750ms） */
		DS18B20_StartConv();

		/* 2. 转换等待期间：扫描按键 */
		key = Key_GetNum();
		if (key == 1)						/* SET：进入/退出设置模式 */
		{
			setMode = !setMode;
		}
		else if (key == 2 && setMode == 1)	/* +：阈值 +0.5℃ */
		{
			threshold += 0.5f;
			if (threshold > 99.0f)
			{
				threshold = 99.0f;
			}
		}
		else if (key == 3 && setMode == 1)	/* -：阈值 -0.5℃ */
		{
			threshold -= 0.5f;
			if (threshold < 0.0f)
			{
				threshold = 0.0f;
			}
		}

		/* 3. 等待转换完成，读取 DS18B20 并滤波 */
		Delay_ms(760);
		if (DS18B20_ReadTemp(&rawTemp))
		{
			tempFiltered = Filter_Update(rawTemp);
		}
		else
		{
			printf("CRC error, sample dropped\r\n");	/* 校验失败，本次丢弃 */
		}

		/* 4. 读取 LM35（16 次 ADC 采样平均） */
		lm35Temp = LM35_GetTemp();

		/* 5. 报警判断（带 0.5℃ 回差，以 DS18B20 为准） */
		Alarm_Update(tempFiltered, threshold);

		/* 6. 显示刷新 */
		Display_Update(tempFiltered);

		/* 7. 串口输出一行（约 1 秒 1 行） */
		count++;
		t100 = (int16_t)(tempFiltered * 100.0f + 0.5f);
		l10  = (int16_t)(lm35Temp * 10.0f + 0.5f);
		th10 = (int16_t)(threshold * 10.0f + 0.5f);
		printf("%d,DS=%d.%02dC,LM=%d.%dC,TH=%d.%dC,%s\r\n",
			count, t100 / 100, t100 % 100,
			l10 / 10, l10 % 10, th10 / 10, th10 % 10,
			Alarm_IsOn() ? "ALARM" : "NORMAL");

		/* 8. 心跳指示：PC13 板载 LED 翻转 */
		GPIO_WriteBit(GPIOC, GPIO_Pin_13,
			(BitAction)(1 - GPIO_ReadOutputDataBit(GPIOC, GPIO_Pin_13)));
	}
}
