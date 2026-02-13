import numpy as np

def L_pure(freq,L):
    omega = 2 * np.pi * freq

    return 1j * omega * L

def C_pure(freq,C):
    omega = 2 * np.pi * freq

    return 1 / (1j * omega * C)

def L_stray(freq, L, C, R):
    Z_L = L_pure(freq,L)
    Z_R = R
    Z_C = C_pure(freq,C)

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
    Z_C = C_pure(freq,C)

    Z_total = Z_L + Z_R + Z_C

    return Z_total


def RLC_ser_stray_abs_log(freq, L, C, R, C_stray, R_stray):
    Z = RLC_ser_stray(freq, L, C, R, C_stray, R_stray)

    return np.log(np.abs(Z))
