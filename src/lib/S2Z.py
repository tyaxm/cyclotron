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

