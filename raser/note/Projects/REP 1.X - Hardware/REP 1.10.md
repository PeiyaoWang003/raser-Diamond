---
REP: 1.1
Title: R1 fabrication
Author: 何野
Status: Active
Type: Hardware
Created: 2023-11-07
Updated: 2023-11-07
---
# R1 fabrication
- 硬件
	-  [ ] 根据需求，确认使用的器件清单（BOM）
	-  [ ] 画出要实现需求的功能所需要的电路的原理图
- 软件
	-  [ ] 输入电路（模拟部分）信号仿真
	-  [ ] ADC及FPGA（数字部分）仿真
### DRS4读出板--R1 设计图
![R1.png](https://raser-1314796952.cos.ap-beijing.myqcloud.com/media/20231107163911.png)

### 输入电路
![input_cir.png](https://raser-1314796952.cos.ap-beijing.myqcloud.com/media/20231107164738.png)

假设信号由UCSC产生，模拟Sr90 $\beta$源产生的信号，经过输入电路和DRS4芯片后，产生的模拟信号为
![analog_out.png](https://raser-1314796952.cos.ap-beijing.myqcloud.com/media/20231107164850.png)
模拟功能在raser elec drs4_get_analog完成

### ADC及FPGA仿真
输入电路部分已经获得了ADC输入的模拟信号，需要在ADC仿真中实现模拟信号转换为数字信号，然后由FPGA进行处理

### BOM
| 型号                   | 类型       | 数量 | 单价/RMB | 总价/RMB | 购买地址                                                                                           |
|----------------------|----------|----|--------|--------|------------------------------------------------------------------------------------------------|
| 24LC128_SN           | EEPROM   | 1  | 6.47   | 6.47   | 24LC128-I/SN Microchip Technology | 集成电路（IC） | DigiKey                                         |
| A25L016M             | 闪存芯片     | 1  | 4.656  | 4.656  | A25L016M-F | AMIC Technology 16Mbit 闪存芯片, SPI接口, SOP-8, 5.23 x 5.28 x 1.8mm | RS (rsonline.cn) |
| AD8061ART            | 放大器      | 1  | 10     | 10     | AD8061 数据手册和产品信息 | 亚德诺（ADI）半导体 (analog.com)                                                    |
| AD8065ART            | 放大器      | 3  | 24     | 72     | AD8065 数据手册和产品信息 | 亚德诺（ADI）半导体 (analog.com)                                                    |
| AD9245               | ADC      | 1  | 599.8  | 599.8  | AD9245BCPZ-80 Analog Devices Inc. | 集成电路（IC） | DigiKey                                         |
| ADCMP601             | 高速比较器    | 4  | 54     | 216    | ADCMP601BKSZ-R2 Analog Devices Inc. | 集成电路（IC） | DigiKey                                       |
| PE4251               | 射频开关     | 4  | 11.79  | 47.16  | PE4251MLI-Z pSemi | 射频和无线 | DigiKey                                                            |
| ADR03                | 基准电压源    | 1  | 13     | 13     | ADR03 数据手册和产品信息 | 亚德诺（ADI）半导体 (analog.com)                                                     |
| ASEMP-3.2X2.5        | 振荡器      | 2  | 30.87  | 61.74  | ASEMPC-100.000MHZ-LR-T - Abracon - MEMS Oscillator, Clock, Pure Silicon™ (element14.com)       |
| BAV99                | 二极管      | 4  | 1.83   | 7.32   | BAV99 SMC Diode Solutions | 分立半导体产品 | DigiKey                                                  |
| CY7C68013-56         | 微控制器     | 1  | 126.9  | 126.9  | CY7C68013A-56PVXC Infineon Technologies | 集成电路（IC） | DigiKey                                   |
| DRS4_76              | DRS4芯片   | 1  |        |        | DRS4 SHOP | Radec                                                                              |
| LED_PLCC-4           | LED      | 3  | 5.45   | 16.35  | ASMB-MTB1-0B3A2 Broadcom / Avago | Mouser                                                      |
| LMZ10503             | 直流转换器    | 1  | 138.44 | 138.44 | LMZ10503EXTTZE/NOPB Texas Instruments | 板安装电源 | DigiKey                                        |
| LP2985               | 降稳压器     | 2  | 0.26   | 0.52   | LP2985 数据表、产品信息和支持 | 德州仪器 TI.com.cn                                                            |
| LTC2600              | DAC      | 1  | 267.75 | 267.75 | LTC2600CGN#PBF Analog Devices Inc. | 集成电路（IC） | DigiKey                                        |
| MAX6662              | 符号温度传感器  | 1  | 38.26  | 38.26  | MAX6662MSA+ Analog Devices Inc./Maxim Integrated | Sensors, Transducers | DigiKey              |
| MCX-90               | MCX连接器   | 4  |        |        |                                                                                                |
| BAV99s               | 开关二极管    | 4  | 2.82   | 11.28  | BAV99S,115 Nexperia USA Inc. | 分立半导体产品 | DigiKey                                               |
| REG1117              | 线性稳压器    | 1  | 24.32  | 24.32  | REG1117 Texas Instruments | 集成电路（IC） | DigiKey                                                 |
| SN74LVC1G04          | 逆变器      | 1  | 1.91   | 1.91   | SN74LVC1G04DCKR UMW | 集成电路（IC） | DigiKey                                                       |
| SN74LVC1G17          | 缓存器      | 1  | 3.07   | 3.07   | SN74LVC1G17DBVR Texas Instruments | 集成电路（IC） | DigiKey                                         |
| SN74LVC1T45DB        | 总线收发器    | 1  | 4.65   | 4.65   | SN74LVC1T45DBVR Texas Instruments | 集成电路（IC） | DigiKey                                         |
| THS4508              | 放大器      | 1  | 70.3   | 70.3   | THS4508RGTT Texas Instruments | 集成电路（IC） | DigiKey                                             |
| TPS79625             | 低压差线性稳压器 | 1  | 26.89  | 26.89  | TPS79625DCQR Texas Instruments | 集成电路（IC） | DigiKey                                            |
| USB_CONN_B           | USB接口    | 1  |        |        |                                                                                                |
| XC3S400-TQ144        | FPGA     | 1  | 483.38 | 483.38 | XC3S400-4TQG144C AMD | 集成电路（IC） | DigiKey                                                      |
| XCF02S-V020          | EEPROM   | 1  | 116.29 | 116.29 | XCF02SVOG20C_（XILINX(赛灵思)）XCF02SVOG20C中文资料_价格_PDF手册-立创电子商城 (szlcsc.com)                        |
| XC7A100T             | FPGA     | 1  | 1251.6 | 1251.6 | XC7A100T-1FTG256I AMD | 集成电路（IC） | DigiKey                                                     |
| ADL5611              | 增益模块     | 2  | 21.93  | 43.86  | https://www.analog.com/cn/products/adl5611.html                                                |
| CAP_0402 10n         | 电容       | 4  |        |        |[得捷电子 中国 DigiKey官网 | 供应商直授权电子元器件分销商](https://www.digikey.cn/?utm_source=baidu&utm_medium=cpc&utm_campaign=Brand%20Keywords&utm_content=Digikey_Brand&utm_term=digi%20key)                                                                                                |
| CAP_0402 100n        | 电容       | 19 |        |        |                                                                                                |
| CAP_0402 100p        | 电容       | 5  |        |        |                                                                                                |
| CAP_0402 220n        | 电容       | 24 |        |        |                                                                                                |
| CAP_0603 1u          | 电容       | 7  |        |        |                                                                                                |
| CAP_0603 4.7n        | 电容       | 1  |        |        |                                                                                                |
| CAP_0603 5.6n        | 电容       | 1  |        |        |                                                                                                |
| CAP_0603 10n         | 电容       | 6  |        |        |                                                                                                |
| CAP_0603 15p         | 电容       | 2  |        |        |                                                                                                |
| CAP_0603 39p         | 电容       | 1  |        |        |                                                                                                |
| CAP_0603 56p         | 电容       | 2  |        |        |                                                                                                |
| CAP_0603 100n        | 电容       | 54 |        |        |                                                                                                |
| CAP_0603 100p        | 电容       | 1  |        |        |                                                                                                |
| CAP_0805 4.7u        | 电容       | 15 |        |        |                                                                                                |
| CAP_1206 10u         | 电容       | 16 |        |        |                                                                                                |
| CAP_1206 22u         | 电容       | 1  |        |        |                                                                                                |
| CAP_1206 100n        | 电容       | 1  |        |        |                                                                                                |
| CAP_1210 47u         | 电容       | 1  |        |        |                                                                                                |
| CAP_1210 100u        | 电容       | 2  |        |        |                                                                                                |
| CAPP 220u            | 电容       | 1  |        |        |                                                                                                |
| CONN_MOLEX_JTAG_FPGA | JTAG接口   | 1  |        |        |                                                                                                |
| IND_0603 82nH        | 电感       | 2  |        |        |                                                                                                |
| IND_0603 220nH       | 电感       | 6  |        |        |                                                                                                |
| IND_1008 10uH        | 电感       | 1  |        |        |                                                                                                |
| IND_1812 10uH        | 电感       | 2  |        |        |                                                                                                |
| JMP2MM               |          | 2  |        |        |                                                                                                |
| RES_0402 0E          | 电阻       | 20 |        |        |                                                                                                |
| RES_0402 15E         | 电阻       | 8  |        |        |                                                                                                |
| RES_0402 16E         | 电阻       | 4  |        |        |                                                                                                |
| RES_0402 22E         | 电阻       | 16 |        |        |                                                                                                |
| RES_0402 49.9E       | 电阻       | 4  |        |        |                                                                                                |
| RES_0402 61.9E       | 电阻       | 8  |        |        |                                                                                                |
| RES_0402 64.9E       | 电阻       | 8  |        |        |                                                                                                |
| RES_0402 100E        | 电阻       | 2  |        |        |                                                                                                |
| RES_0402 169E        | 电阻       | 8  |        |        |                                                                                                |
| RES_0402 348E        | 电阻       | 8  |        |        |                                                                                                |
| RES_0402 390k        | 电阻       | 3  |        |        |                                                                                                |
| RES_0603 0E          | 电阻       | 14 |        |        |                                                                                                |
| RES_0603 1k          | 电阻       | 5  |        |        |                                                                                                |
| RES_0603 1.5E        | 电阻       | 4  |        |        |                                                                                                |
| RES_0603 2k4         | 电阻       | 1  |        |        |                                                                                                |
| RES_0603 2.2k        | 电阻       | 2  |        |        |                                                                                                |
| RES_0603 3.6k        | 电阻       | 8  |        |        |                                                                                                |
| RES_0603 4k7         | 电阻       | 4  |        |        |                                                                                                |
| RES_0603 4.7E        | 电阻       | 4  |        |        |                                                                                                |
| RES_0603 10E         | 电阻       | 1  |        |        |                                                                                                |
| RES_0603 10k         | 电阻       | 3  |        |        |                                                                                                |
| RES_0603 22E         | 电阻       | 2  |        |        |                                                                                                |
| RES_0603 23.7k       | 电阻       | 1  |        |        |                                                                                                |
| RES_0603 49.9E       | 电阻       | 1  |        |        |                                                                                                |
| RES_0603 75k         | 电阻       | 1  |        |        |                                                                                                |
| RES_0603 100E        | 电阻       | 1  |        |        |                                                                                                |
| RES_0603 100k        | 电阻       | 2  |        |        |                                                                                                |
| RES_0603 130E        | 电阻       | 1  |        |        |                                                                                                |
| RES_0603 220E        | 电阻       | 2  |        |        |                                                                                                |
| RES_0603 390k        | 电阻       | 1  |        |        |                                                                                                |
| RES_0805 0E          | 电阻       | 4  |        |        |                                                                                                |
| RES_0805 1k          | 电阻       | 1  |        |        |                                                                                                |
| RES_0805 51E         | 电阻       | 8  |        |        |                                                                                                |
| RES_1206 120E        | 电阻       | 1  |        |        |                                                                                                |
| SMA_SMD_S            | SMA接口    | 1  |        |        |                                                                                                |
