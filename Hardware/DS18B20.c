#include "stm32f10x.h"
#include "DS18B20.h"
#include "Delay.h"

/*=============================================================
 * DS18B20 温度传感器驱动（单总线 1-Wire）
 * 接线：VCC->3.3V  GND->GND  DQ->PA1（模块自带 4.7k 上拉）
 * PA1 配置为开漏输出：写 1 = 释放总线，写 0 = 拉低总线
 * 注意：位级时序依赖微秒延时，期间不能被长中断打断
 *=============================================================*/

#define DQ_PORT   GPIOA
#define DQ_PIN    GPIO_Pin_1

#define DQ_Write(x)   GPIO_WriteBit(DQ_PORT, DQ_PIN, (BitAction)(x))
#define DQ_Read       GPIO_ReadInputDataBit(DQ_PORT, DQ_PIN)

/**
  * @brief  单总线复位，并检测存在脉冲
  * @retval 0：器件在线    1：无响应
  */
static uint8_t OW_Reset(void)
{
	uint8_t pres;

	DQ_Write(0);				/* 拉低约 500us */
	Delay_us(500);
	DQ_Write(1);				/* 释放总线 */
	Delay_us(70);
	pres = DQ_Read;				/* 若器件在线，此时总线被拉低（存在脉冲） */
	Delay_us(430);

	return pres;
}

/**
  * @brief  写一个位
  */
static void OW_WriteBit(uint8_t bit)
{
	DQ_Write(0);
	if (bit)
	{
		Delay_us(2);
		DQ_Write(1);
		Delay_us(60);			/* 写 1：短低电平 */
	}
	else
	{
		Delay_us(60);
		DQ_Write(1);
		Delay_us(2);			/* 写 0：长低电平 */
	}
}

/**
  * @brief  读一个位
  */
static uint8_t OW_ReadBit(void)
{
	uint8_t bit;

	DQ_Write(0);
	Delay_us(2);
	DQ_Write(1);
	Delay_us(10);				/* 在 15us 内采样 */
	bit = DQ_Read;
	Delay_us(50);

	return bit;
}

/**
  * @brief  写一个字节（低位先发）
  */
static void OW_WriteByte(uint8_t byte)
{
	uint8_t i;

	for (i = 0; i < 8; i++)
	{
		OW_WriteBit(byte & (0x01 << i));
	}
}

/**
  * @brief  读一个字节（低位先收）
  */
static uint8_t OW_ReadByte(void)
{
	uint8_t i;
	uint8_t byte = 0;

	for (i = 0; i < 8; i++)
	{
		byte |= (OW_ReadBit() << i);
	}

	return byte;
}

/**
  * @brief  CRC8 校验（多项式 X^8+X^5+X^4+1），用于校验暂存器数据
  */
static uint8_t CRC8(const uint8_t *data, uint8_t len)
{
	uint8_t i, j;
	uint8_t crc = 0;

	for (i = 0; i < len; i++)
	{
		crc ^= data[i];
		for (j = 0; j < 8; j++)
		{
			if (crc & 0x01)
			{
				crc = (crc >> 1) ^ 0x8C;
			}
			else
			{
				crc = crc >> 1;
			}
		}
	}

	return crc;
}

/**
  * @brief  DS18B20 初始化（PA1 开漏输出）
  */
void DS18B20_Init(void)
{
	GPIO_InitTypeDef GPIO_InitStructure;

	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_OD;
	GPIO_InitStructure.GPIO_Pin = DQ_PIN;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(DQ_PORT, &GPIO_InitStructure);

	DQ_Write(1);				/* 释放总线 */
}

/**
  * @brief  启动一次温度转换（12 位精度，最长需要 750ms）
  */
void DS18B20_StartConv(void)
{
	OW_Reset();
	OW_WriteByte(0xCC);			/* 跳过 ROM：总线上只有一只时可用 */
	OW_WriteByte(0x44);			/* 启动温度转换 */
}

/**
  * @brief  读取温度
  * @param  pTemp 读出的温度值（单位：℃）
  * @retval 1：成功（CRC 校验通过）  0：失败
  */
uint8_t DS18B20_ReadTemp(float *pTemp)
{
	uint8_t buf[9];
	uint8_t i;
	int16_t raw;

	OW_Reset();
	OW_WriteByte(0xCC);
	OW_WriteByte(0xBE);			/* 读暂存器（9 字节） */

	for (i = 0; i < 9; i++)
	{
		buf[i] = OW_ReadByte();
	}

	if (CRC8(buf, 8) != buf[8])
	{
		return 0;				/* CRC 校验失败，数据丢弃 */
	}

	raw = (int16_t)((buf[1] << 8) | buf[0]);
	*pTemp = raw * 0.0625f;		/* 最低有效位 = 0.0625℃ */

	return 1;
}
