import numpy as np

def linear(x,a,b):
    return a*x + b

def inverse_prop(x,a,b):
    return a/x + b

def inverse_prop_ideal(x,a):
    return a/x

def L_ideal(freq,L):
    omega = 2 * np.pi * freq

    return 1j * omega * L

def C_ideal(freq,C):
    omega = 2 * np.pi * freq

    return 1 / (1j * omega * C)

def C_ideal_imag(freq,C):
    return C_ideal(freq,C).imag

def L_stray(freq, L, C, R):
    Z_L = L_ideal(freq,L)
    Z_R = R
    Z_C = C_ideal(freq,C)

    Z_total = 1 / (1 / (Z_L + Z_R) + 1 / Z_C)

    return Z_total

def L_stray_real(freq, L, C, R):
    Z = L_stray(freq,L,C,R)

    return Z.real

def L_stray_imag(freq, L, C, R):
    Z = L_stray(freq,L,C,R)

    return Z.imag

def RLC_ser_stray(freq, L, C, R, C_stray, R_stray):
    Z_L = L_stray(freq,L,C_stray,R_stray)
    Z_R = R
    Z_C = C_ideal(freq,C)

    Z_total = Z_L + Z_R + Z_C

    return Z_total


def RLC_ser_stray_abs_log(freq, L, C, R, C_stray, R_stray):
    Z = RLC_ser_stray(freq, L, C, R, C_stray, R_stray)

    return np.log(np.abs(Z))

def CR_par(freq, C, R):
    Z_R = R
    Z_C = C_ideal(freq,C)

    Z_total = 1 / (1 / Z_R + 1 / Z_C)

    return Z_total


def CR_par_real(freq, C, R):
    Z = CR_par(freq, C, R)
    real_part = np.array(Z.real, dtype=np.float64)
    return real_part


def CR_par_imag(freq, C, R):
    Z = CR_par(freq, C, R)
    imag_part = np.array(Z.imag, dtype=np.float64)
    return imag_part

def JG_R(freq,C1,R1,C2,R2):
    Z_C1 = C_ideal(freq,C1)
    Z_R1 = R1
    Z_C2 = C_ideal(freq,C2)
    Z_R2 = R2

    Z = (1/Z_C1 + 1/(Z_R1 + (1/Z_C2 + 1/Z_R2) ** -1)) ** -1

    return Z

def JG_R_real(freq,C1,R1,C2,R2):
    Z = JG_R(freq,C1,R1,C2,R2)
    return Z.real

def JG_R_imag(freq,C1,R1,C2,R2):
    Z = JG_R(freq,C1,R1,C2,R2)
    return Z.imag