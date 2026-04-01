import time
import sys
import numpy as np
import pynanovna

CALIBRATION_FILE = "default.cal"
CENTER_FREQ = 10.13e6
SPAN_FREQ = 0.2e6
SWEEP_POINTS = 401
Z0 = 50.0

RED = "\033[31m"
BLUE = "\033[34m"
GREEN = "\033[32m"
RESET = "\033[0m"
CLEAR_LINE = "\033[K"
UP_CURSOR = "\033[F"

def get_color_text(val, target, unit=""):
    diff = val - target
    if diff > 0:
        return f"{RED} +{diff:.4f}{unit}){RESET}"
    elif diff < 0:
        return f"{BLUE} -{diff:.4f}{unit}){RESET}"
    else:
        return f"{GREEN} perfect!! {RESET}"

def main():
    try:
        vna = pynanovna.VNA()
        print("Connecting to VNA...")
        vna.load_calibration(CALIBRATION_FILE)
        
        start_f = CENTER_FREQ - (SPAN_FREQ / 2)
        stop_f = CENTER_FREQ + (SPAN_FREQ / 2)
        vna.set_sweep(start_f, stop_f, SWEEP_POINTS)

        print(f"Calibration: {CALIBRATION_FILE}")
        print(f"Sweep Range: {start_f/1e6:.3f} - {stop_f/1e6:.3f} MHz")
        print("-" * 60)
        
        num_display_lines = 4
        first_run = True

        while True:
            s11, s21, freq = vna.sweep()
            s11 = np.array(s11)
            s21 = np.array(s21)
            z_array = Z0 * (1 + s11) / (1 - s11)
            real_parts = np.real(z_array)

            max_idx = np.argmax(real_parts)
            target_f = freq[max_idx]
            target_z = z_array[max_idx]

            if not first_run:
                sys.stdout.write(UP_CURSOR * num_display_lines)

            lines = [
                f"{CLEAR_LINE}frequency  : {target_f/1e6:9.6f} MHz -> {get_color_text(target_f, CENTER_FREQ, 'Hz')}",
                f"{CLEAR_LINE}reactance  : {target_z.imag:10.4f} Ω     -> {get_color_text(target_z.imag, 0, 'Ω')}",
                f"{CLEAR_LINE}resistance : {target_z.real:10.4f} Ω     -> {get_color_text(target_z.real, 50.0, 'Ω')}"
            ]

            sys.stdout.write("\n".join(lines) + "\n")
            sys.stdout.flush()
            
            first_run = False
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nterminated")
    except Exception as e:
        print(f"\nerror : {e}")

if __name__ == "__main__":
    main()