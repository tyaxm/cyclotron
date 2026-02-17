import numpy as np

Z0 = 50

# port1 ---- +
#            |
#            Z
#            |
# GND   ---- +
def direct(data):
    freq = data[:, 0]
    Z_tot = (1 + data[:, 1] + 1j * data[:, 2]) / (1 - data[:, 1] - 1j * data[:, 2]) * Z0
    return freq,Z_tot

# port1 ---- + ---- Zs ---- port2 
#            |
#            Zb
#            |
# GND   ---- + ------------ GND
def bridge_at_port1(data):
    freq = data[:, 0]
    s11 = data[:, 1] + 1j * data[:, 2]
    s21 = data[:, 3] + 1j * data[:, 4]
    Zs = ((1 + s11) / s21 - 1) * Z0
    Zb = (1 + s11) / (1 - s11 - s21) * Z0
    return freq, Zs, Zb

# port1 ---- Zs ---- + ---- port2 
#                    |
#                    Zb
#                    |
# GND   ------------ + ---- GND
def bridge_at_port2(data):
    freq = data[:, 0]
    s11 = data[:, 1] + 1j * data[:, 2]
    s21 = data[:, 3] + 1j * data[:, 4]
    Zs = (1 + s11 - s21) / (1 - s11) * Z0
    Zb = 1/(1 - s11 - s21) * ((1 + s11) * Z0 - (1 - s11) * Zs)
    return freq, Zs, Zb


# data1
# port1 ---- + -----+-- Zs ---- port2 
#            |      |
#            Zb2    Zb1
#            |      |
# GND   ---- + -----+---------- GND

# data2
# port1 --+-- Zs ---- + ---- port2 
#         |          |
#         Zb2        Zb1
#         |          |
# GND   --+--------- + ---- GND

def two_bridges_with_stray_in_port1(data1, data2):
    freq = data1[:, 0]
    s11_1 = data1[:, 1] + 1j * data1[:, 2]
    s21_1 = data1[:, 3] + 1j * data1[:, 4]
    s11_2 = data2[:, 1] + 1j * data2[:, 2]
    s21_2 = data2[:, 3] + 1j * data2[:, 4]
    Zb_para = (1 + s11_1) / (1 - s11_1 - s21_1) * Z0
    Zb1 = Z0 * (1 + s11_2 - s21_2) / (Z0 * (1 + s11_2) / Zb_para - 1 + s11_2 + s21_2)
    Zb2 = (-Z0 * (1 + s11_2) * Zb1) / (Zb1 * s21_2 + Z0 * s21_2 - Zb1 * (1-s11_2))
    Zs = (1 + s11_2 - s21_2) * Zb1 / (s21_2 * (Zb1 / Z0 +1))
    return freq, Zb1, Zb2, Zs

def db(x):
    return 20 * np.log10(x)

# data1
# port1 ---- + ---- Zs ---- + ---- port2 
#            |              |
#            Zb1            Zb2
#            |              |
# GND   ---- + ------------ + ---- GND

# data2
# port1 ---- + ---- Zs ---- + ---- port2 
#            |              |
#            Zb2            Zb1
#            |              |
# GND   ---- + ------------ + ---- GND

def bridges_at_ports_1_2(data1,data2):
    freq = data1[:, 0]
    s11_1 = data1[:, 1] + 1j * data1[:, 2]
    s21_1 = data1[:, 3] + 1j * data1[:, 4]
    s11_2 = data2[:, 1] + 1j * data2[:, 2]
    s21_2 = data2[:, 3] + 1j * data2[:, 4]


    q1 = (1 - s11_1) / (1 + s11_1)
    q2 = (1 - s11_2) / (1 + s11_2)
    r1 = s21_1/(1 + s11_1)
    r2 = s21_2/(1 + s11_2)
    
    Zb1 = (1/r1 - r2)/(q1/r1 + r2 - q2 -1) * Z0
    Zb2 = (1/r2 - r1)/(q2/r2 + r1 - q1 -1) * Z0

    Zs = (1/r1 - 1 ) / (1/Z0 + 1/Zb2)

    return freq,Zb1,Zs,Zb2

def bridges_at_ports_1_2_miss(data1,data2):
    freq = data1[:, 0]
    s11_1 = data1[:, 1] + 1j * data1[:, 2]
    s21_1 = data1[:, 3] + 1j * data1[:, 4]
    s11_2 = data2[:, 1] + 1j * data2[:, 2]
    s21_2 = data2[:, 3] + 1j * data2[:, 4]

    r1 = s21_1/(1 + s11_1)
    r2 = s21_2/(1 + s11_2)
    
    Zb1 = (1/r1 - r2)/(1/r1 + r2 -2) * Z0
    Zb2 = (1/r2 - r1)/(1/r2 + r1 -2) * Z0

    Zs = (1/r1 - 1 ) * (1 / (1/Z0 + 1/Zb2))

    return freq,Zb1,Zs,Zb2
    