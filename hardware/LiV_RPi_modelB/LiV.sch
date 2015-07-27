EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:LiV_2-cache
EELAYER 24 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date "27 jun 2014"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L CONN_13X2 P1
U 1 1 5240880E
P 6400 1750
F 0 "P1" H 6400 2450 60  0000 C CNN
F 1 "CONN_13X2" V 6400 1750 50  0000 C CNN
F 2 "" H 6400 1750 60  0000 C CNN
F 3 "" H 6400 1750 60  0000 C CNN
	1    6400 1750
	1    0    0    -1  
$EndComp
$Comp
L CONN_10X2 P2
U 1 1 53A25E54
P 6350 3550
F 0 "P2" H 6350 4100 60  0000 C CNN
F 1 "CONN_10X2" V 6350 3450 50  0000 C CNN
F 2 "" H 6350 3550 60  0000 C CNN
F 3 "" H 6350 3550 60  0000 C CNN
	1    6350 3550
	1    0    0    -1  
$EndComp
$Comp
L CONN_4 P7
U 1 1 53A25EA9
P 3050 3900
F 0 "P7" V 3000 3900 50  0000 C CNN
F 1 "I2C2" V 3100 3900 50  0000 C CNN
F 2 "" H 3050 3900 60  0000 C CNN
F 3 "" H 3050 3900 60  0000 C CNN
	1    3050 3900
	1    0    0    -1  
$EndComp
$Comp
L CONN_4 P8
U 1 1 53A25EB8
P 8200 5350
F 0 "P8" V 8150 5350 50  0000 C CNN
F 1 "TSENSE2" V 8250 5350 50  0000 C CNN
F 2 "" H 8200 5350 60  0000 C CNN
F 3 "" H 8200 5350 60  0000 C CNN
	1    8200 5350
	1    0    0    -1  
$EndComp
$Comp
L CONN_4 P9
U 1 1 53A25EC7
P 8200 6050
F 0 "P9" V 8150 6050 50  0000 C CNN
F 1 "TSENSE1" V 8250 6050 50  0000 C CNN
F 2 "" H 8200 6050 60  0000 C CNN
F 3 "" H 8200 6050 60  0000 C CNN
	1    8200 6050
	1    0    0    -1  
$EndComp
$Comp
L CONN_4 P3
U 1 1 53A25ED6
P 2200 1300
F 0 "P3" V 2150 1300 50  0000 C CNN
F 1 "SCREEN" V 2250 1300 50  0000 C CNN
F 2 "" H 2200 1300 60  0000 C CNN
F 3 "" H 2200 1300 60  0000 C CNN
F 4 "5V I2C" V 2200 1300 60  0001 C CNN "Desc"
	1    2200 1300
	-1   0    0    1   
$EndComp
$Comp
L CONN_2 P4
U 1 1 53A25F01
P 2000 5300
F 0 "P4" V 1950 5300 40  0000 C CNN
F 1 "CO2_RESET" V 2050 5300 40  0000 C CNN
F 2 "" H 2000 5300 60  0000 C CNN
F 3 "" H 2000 5300 60  0000 C CNN
	1    2000 5300
	-1   0    0    1   
$EndComp
$Comp
L CONN_4 P5
U 1 1 53A25F10
P 2000 6300
F 0 "P5" V 1950 6300 50  0000 C CNN
F 1 "CO2_COMM" V 2050 6300 50  0000 C CNN
F 2 "" H 2000 6300 60  0000 C CNN
F 3 "" H 2000 6300 60  0000 C CNN
	1    2000 6300
	-1   0    0    1   
$EndComp
$Comp
L CONN_4 P6
U 1 1 53A25F1F
P 3050 2900
F 0 "P6" V 3000 2900 50  0000 C CNN
F 1 "I2C1" V 3100 2900 50  0000 C CNN
F 2 "" H 3050 2900 60  0000 C CNN
F 3 "" H 3050 2900 60  0000 C CNN
	1    3050 2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6800 1150 7450 1150
Wire Wire Line
	6800 1350 7450 1350
Wire Wire Line
	6800 1450 7450 1450
Wire Wire Line
	6800 1550 7450 1550
Wire Wire Line
	6800 1650 7450 1650
Wire Wire Line
	6800 1850 7450 1850
Wire Wire Line
	6800 1950 7450 1950
Wire Wire Line
	6800 2150 7450 2150
Wire Wire Line
	6800 2250 7450 2250
Wire Wire Line
	6800 2350 7450 2350
Wire Wire Line
	6000 1250 5350 1250
Wire Wire Line
	6000 1350 5350 1350
Wire Wire Line
	6000 1450 5350 1450
Wire Wire Line
	6000 1650 5350 1650
Wire Wire Line
	6000 1750 5350 1750
Wire Wire Line
	6000 1850 5350 1850
Wire Wire Line
	6000 2050 5350 2050
Wire Wire Line
	6000 2150 5350 2150
Wire Wire Line
	6000 2250 5350 2250
Wire Wire Line
	6000 1150 5350 1150
Text Label 5400 1150 0    60   ~ 0
3_3V_PWR
Text Label 2650 1250 0    60   ~ 0
GPIO_2
Text Label 5400 1250 0    60   ~ 0
GPIO_2
Text Label 5400 1350 0    60   ~ 0
GPIO_3
Text Label 5400 1450 0    60   ~ 0
GPIO_4
Text Label 5400 1650 0    60   ~ 0
GPIO_17
Text Label 5400 1750 0    60   ~ 0
GPIO_27
Text Label 5400 1850 0    60   ~ 0
GPIO_22
Text Label 5400 2050 0    60   ~ 0
GPIO_10
Text Label 5400 2150 0    60   ~ 0
GPIO_9
Text Label 5400 2250 0    60   ~ 0
GPIO_11
Text Label 6850 1150 0    60   ~ 0
5V_PWR
Text Label 6850 1350 0    60   ~ 0
GND
Text Label 6850 1450 0    60   ~ 0
GPIO_14
Text Label 6850 1550 0    60   ~ 0
GPIO_15
Text Label 6850 1650 0    60   ~ 0
GPIO_18
Text Label 6850 1850 0    60   ~ 0
GPIO_23
Text Label 6850 1950 0    60   ~ 0
GPIO_24
Text Label 6850 2150 0    60   ~ 0
GPIO_25
Text Label 6850 2250 0    60   ~ 0
GPIO_8
Text Label 6850 2350 0    60   ~ 0
GPIO_7
Text Notes 950  5850 0    197  ~ 0
CO2 Sensor
Text Notes 2050 1950 0    197  ~ 0
Screen
Text Notes 5350 2700 0    197  ~ 0
RPi Connector
Text Notes 5600 4300 0    197  ~ 0
Expansion
Text Notes 2050 3500 0    197  ~ 0
3.3V I2C
Text Notes 8400 5750 0    197  ~ 0
3.3V GPIO
Wire Wire Line
	2700 2750 2150 2750
Wire Wire Line
	2700 2850 2150 2850
Wire Wire Line
	2700 2950 2150 2950
Wire Wire Line
	2700 3050 2150 3050
Wire Wire Line
	2700 3750 2150 3750
Wire Wire Line
	2700 3850 2150 3850
Wire Wire Line
	2700 3950 2150 3950
Wire Wire Line
	2700 4050 2150 4050
Wire Wire Line
	7250 5200 7850 5200
Wire Wire Line
	6950 5300 7850 5300
Wire Wire Line
	7850 5400 7250 5400
Wire Wire Line
	7850 5500 7250 5500
Wire Wire Line
	7850 5900 7250 5900
Wire Wire Line
	6950 6000 7850 6000
Wire Wire Line
	7850 6100 7250 6100
Wire Wire Line
	7850 6200 7250 6200
Wire Wire Line
	6750 3100 7550 3100
Wire Wire Line
	6750 3200 7550 3200
Wire Wire Line
	6750 3300 7550 3300
Wire Wire Line
	6750 3400 7550 3400
Wire Wire Line
	6750 3500 7550 3500
Wire Wire Line
	6750 3600 7550 3600
Wire Wire Line
	6750 3700 7550 3700
Wire Wire Line
	6750 3800 7550 3800
Wire Wire Line
	6750 3900 7550 3900
Wire Wire Line
	6750 4000 7550 4000
Wire Wire Line
	5950 3100 5200 3100
Wire Wire Line
	5950 3200 5200 3200
Wire Wire Line
	5950 3300 5200 3300
Wire Wire Line
	5950 3400 5200 3400
Wire Wire Line
	5950 3500 5200 3500
Wire Wire Line
	5950 3600 5200 3600
Wire Wire Line
	5950 3700 5200 3700
Wire Wire Line
	5950 3800 5200 3800
Wire Wire Line
	5950 3900 5200 3900
Wire Wire Line
	5950 4000 5200 4000
Wire Wire Line
	2350 5200 3150 5200
Wire Wire Line
	2350 5400 3150 5400
Wire Wire Line
	2350 6150 3150 6150
Wire Wire Line
	2350 6250 3150 6250
Wire Wire Line
	2350 6350 3150 6350
Wire Wire Line
	2350 6450 3150 6450
Wire Wire Line
	2550 1250 3100 1250
Wire Wire Line
	2550 1350 3100 1350
Wire Wire Line
	2550 1450 3100 1450
Wire Wire Line
	2550 1150 3100 1150
Text Label 2650 1150 0    59   ~ 0
GPIO_3
Text Label 2650 1450 0    59   ~ 0
GND
Text Label 2650 1350 0    59   ~ 0
5V_PWR
Text Label 2550 6150 0    59   ~ 0
GND
Text Label 2550 6250 0    59   ~ 0
5V_PWR
Text Label 2550 6350 0    59   ~ 0
GPIO_14
Text Label 2550 6450 0    59   ~ 0
GPIO_15
Text Label 5350 3100 0    59   ~ 0
3_3V_PWR
Text Label 6900 3100 0    59   ~ 0
5V_PWR
Text Label 7300 5900 0    59   ~ 0
3_3V_PWR
Text Label 6950 5700 0    59   ~ 0
GPIO_17
NoConn ~ 7250 6100
Text Label 7300 6200 0    59   ~ 0
GND
Wire Wire Line
	6800 1250 7450 1250
Text Label 6850 1250 0    59   ~ 0
5V_PWR
Wire Wire Line
	6800 1750 7450 1750
Wire Wire Line
	6800 2050 7450 2050
Text Label 6850 1750 0    59   ~ 0
GND
Text Label 6850 2050 0    59   ~ 0
GND
Wire Wire Line
	6000 1550 5350 1550
Wire Wire Line
	6000 1950 5350 1950
Wire Wire Line
	6000 2350 5350 2350
Text Label 5400 1550 0    59   ~ 0
GND
Text Label 5400 1950 0    59   ~ 0
3_3V_PWR
Text Label 5400 2350 0    59   ~ 0
GND
Text Label 7300 5200 0    59   ~ 0
3_3V_PWR
Text Label 7300 5500 0    59   ~ 0
GND
Text Label 2200 2750 0    59   ~ 0
3_3V_PWR
Text Label 2200 2850 0    59   ~ 0
GND
Text Label 2200 2950 0    59   ~ 0
GPIO_3
Text Label 2200 3050 0    59   ~ 0
GPIO_2
Text Label 2200 3750 0    59   ~ 0
3_3V_PWR
Text Label 2200 3850 0    59   ~ 0
GND
Text Label 2200 3950 0    59   ~ 0
GPIO_3
Text Label 2200 4050 0    59   ~ 0
GPIO_2
Text Label 6950 4900 0    59   ~ 0
GPIO_27
Text Label 5350 3200 0    60   ~ 0
GPIO_4
Text Label 5350 3300 0    60   ~ 0
GND
Text Label 5350 3400 0    60   ~ 0
GND
Text Label 5350 3500 0    60   ~ 0
GPIO_22
Text Label 5350 3600 0    60   ~ 0
3_3V_PWR
Text Label 5350 3700 0    60   ~ 0
GPIO_10
Text Label 5350 3800 0    60   ~ 0
GPIO_9
Text Label 5350 3900 0    60   ~ 0
GPIO_11
Text Label 5350 4000 0    60   ~ 0
GND
Text Label 6900 3200 0    60   ~ 0
5V_PWR
Text Label 6900 3300 0    60   ~ 0
GPIO_18
Text Label 6900 3400 0    60   ~ 0
GND
Text Label 6900 3500 0    60   ~ 0
GPIO_23
Text Label 6900 3600 0    60   ~ 0
GPIO_24
Text Label 6900 3700 0    60   ~ 0
GND
Text Label 6900 3800 0    60   ~ 0
GPIO_25
Text Label 6900 3900 0    60   ~ 0
GPIO_8
Text Label 6900 4000 0    60   ~ 0
GPIO_7
$Comp
L SW_PUSH SW1
U 1 1 53A7985F
P 3400 5300
F 0 "SW1" H 3550 5410 50  0000 C CNN
F 1 "SW_PUSH" H 3400 5220 50  0000 C CNN
F 2 "~" H 3400 5300 60  0000 C CNN
F 3 "~" H 3400 5300 60  0000 C CNN
	1    3400 5300
	0    1    1    0   
$EndComp
Wire Wire Line
	3150 5200 3150 5000
Wire Wire Line
	3150 5000 3400 5000
Wire Wire Line
	3400 5600 3150 5600
Wire Wire Line
	3150 5600 3150 5400
$Comp
L R R1
U 1 1 53A79A7B
P 6200 5900
F 0 "R1" V 6280 5900 40  0000 C CNN
F 1 "4.7k" V 6207 5901 40  0000 C CNN
F 2 "~" V 6130 5900 30  0000 C CNN
F 3 "~" H 6200 5900 30  0000 C CNN
	1    6200 5900
	0    1    1    0   
$EndComp
$Comp
L R R2
U 1 1 53A79A8A
P 6200 6300
F 0 "R2" V 6280 6300 40  0000 C CNN
F 1 "10k" V 6207 6301 40  0000 C CNN
F 2 "~" V 6130 6300 30  0000 C CNN
F 3 "~" H 6200 6300 30  0000 C CNN
	1    6200 6300
	0    1    1    0   
$EndComp
$Comp
L R R3
U 1 1 53A79A99
P 6200 5200
F 0 "R3" V 6280 5200 40  0000 C CNN
F 1 "4.7k" V 6207 5201 40  0000 C CNN
F 2 "~" V 6130 5200 30  0000 C CNN
F 3 "~" H 6200 5200 30  0000 C CNN
	1    6200 5200
	0    1    1    0   
$EndComp
$Comp
L R R4
U 1 1 53A79AA8
P 6200 5550
F 0 "R4" V 6280 5550 40  0000 C CNN
F 1 "10k" V 6207 5551 40  0000 C CNN
F 2 "~" V 6130 5550 30  0000 C CNN
F 3 "~" H 6200 5550 30  0000 C CNN
	1    6200 5550
	0    1    1    0   
$EndComp
Wire Wire Line
	5950 5900 5550 5900
Wire Wire Line
	5950 6300 5550 6300
Wire Wire Line
	5950 5200 5550 5200
Wire Wire Line
	5950 5550 5550 5550
Text Label 5550 5900 0    60   ~ 0
3_3V_PWR
Text Label 5550 6300 0    60   ~ 0
3_3V_PWR
Text Label 5550 5200 0    60   ~ 0
3_3V_PWR
Text Label 5550 5550 0    60   ~ 0
3_3V_PWR
NoConn ~ 7250 5400
Wire Wire Line
	6950 4900 6950 5550
Connection ~ 6950 5300
Wire Wire Line
	6950 5700 6950 6300
Connection ~ 6950 6000
$Comp
L GND #PWR01
U 1 1 53B02C09
P 8950 2200
F 0 "#PWR01" H 8950 2200 30  0001 C CNN
F 1 "GND" H 8950 2130 30  0001 C CNN
F 2 "" H 8950 2200 60  0000 C CNN
F 3 "" H 8950 2200 60  0000 C CNN
	1    8950 2200
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR02
U 1 1 53B02D44
P 9000 1750
F 0 "#PWR02" H 9000 1710 30  0001 C CNN
F 1 "+3.3V" H 9000 1860 30  0000 C CNN
F 2 "" H 9000 1750 60  0000 C CNN
F 3 "" H 9000 1750 60  0000 C CNN
	1    9000 1750
	0    1    1    0   
$EndComp
Wire Wire Line
	8950 2200 8950 2050
Wire Wire Line
	8950 2050 8650 2050
Wire Wire Line
	9000 1750 8650 1750
$Comp
L +5V #PWR03
U 1 1 53B02F16
P 9000 1900
F 0 "#PWR03" H 9000 1990 20  0001 C CNN
F 1 "+5V" H 9000 1990 30  0000 C CNN
F 2 "" H 9000 1900 60  0000 C CNN
F 3 "" H 9000 1900 60  0000 C CNN
	1    9000 1900
	0    1    1    0   
$EndComp
Wire Wire Line
	9000 1900 8650 1900
Text Label 8650 1750 0    60   ~ 0
3_3V_PWR
Text Label 8650 1900 0    60   ~ 0
5V_PWR
Text Label 8650 2050 0    60   ~ 0
GND
Wire Wire Line
	6450 5200 6950 5200
Wire Wire Line
	6950 5550 6450 5550
Wire Wire Line
	6450 5900 6950 5900
Connection ~ 6950 5900
Wire Wire Line
	6950 6300 6450 6300
Connection ~ 6950 5200
$Comp
L CONN_4 P10
U 1 1 5418DE41
P 3050 4550
F 0 "P10" V 3000 4550 50  0000 C CNN
F 1 "I2C3" V 3100 4550 50  0000 C CNN
F 2 "" H 3050 4550 60  0000 C CNN
F 3 "" H 3050 4550 60  0000 C CNN
	1    3050 4550
	1    0    0    -1  
$EndComp
Wire Wire Line
	2700 4400 2150 4400
Wire Wire Line
	2700 4500 2150 4500
Wire Wire Line
	2700 4600 2150 4600
Wire Wire Line
	2700 4700 2150 4700
Text Label 2200 4400 0    59   ~ 0
3_3V_PWR
Text Label 2200 4500 0    59   ~ 0
GND
Text Label 2200 4600 0    59   ~ 0
GPIO_3
Text Label 2200 4700 0    59   ~ 0
GPIO_2
$EndSCHEMATC
