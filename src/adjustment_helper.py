import time
import sys
import numpy as np
import pynanovna

# --- 設定項目 ---
CALIBRATION_FILE = "default.cal"
CENTER_FREQ = 10.13e6
SPAN_FREQ = 0.2e6
SWEEP_POINTS = 401
Z0 = 50.0

# ANSIカラー・制御コード
RED = "\033[31m"
BLUE = "\033[34m"
GREEN = "\033[32m"
RESET = "\033[0m"
CLEAR_LINE = "\033[K"  # 行末まで消去
UP_CURSOR = "\033[F"   # カーソルを一つ上の行の先頭へ移動

def get_color_text(val, target, label_high, label_low, unit=""):
    """値の大小を判定して色付き文字列を返す"""
    diff = val - target
    if diff > 0:
        return f"{RED}{label_high} (差: +{diff:.4f}{unit}){RESET}"
    elif diff < 0:
        return f"{BLUE}{label_low} (差: {diff:.4f}{unit}){RESET}"
    else:
        return f"{GREEN}Target一致{RESET}"

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
        
        # 更新する行数を保持（ヘッダーを除いた表示部分）
        num_display_lines = 5
        first_run = True

        while True:
            # データの取得と計算
            s11, s21, freqs = vna.sweep()
            z_array = Z0 * (1 + s11) / (1 - s11)
            real_parts = np.real(z_array)

            max_idx = np.argmax(real_parts)
            target_f = freqs[max_idx]
            target_z = z_array[max_idx]

            # 2回目以降のループでは、カーソルを前に出力した行数分だけ上に戻す
            if not first_run:
                sys.stdout.write(UP_CURSOR * num_display_lines)

            # --- 出力内容の構築 ---
            # 各行の先頭に CLEAR_LINE を入れることで、文字数が減った際の残像を防ぐ
            lines = [
                f"{CLEAR_LINE}[リアルタイム解析 - Real(Z)最大点]",
                f"{CLEAR_LINE}周波数  : {target_f/1e6:9.6f} MHz -> {get_color_text(target_f, CENTER_FREQ, '10.13MHzより高い', '10.13MHzより低い', 'Hz')}",
                f"{CLEAR_LINE}虚部(X) : {target_z.imag:10.4f} Ω     -> {get_color_text(target_z.imag, 0, '0より大きい(誘導性)', '0より小さい(容量性)', 'Ω')}",
                f"{CLEAR_LINE}実部(R) : {target_z.real:10.4f} Ω     -> {get_color_text(target_z.real, 50.0, '50Ωより大きい', '50Ωより小さい', 'Ω')}",
                f"{CLEAR_LINE}" + "-" * 60
            ]

            # まとめて出力
            sys.stdout.write("\n".join(lines) + "\n")
            sys.stdout.flush()
            
            first_run = False
            time.sleep(0.1)  # 画面のちらつき防止とVNAの負荷調整

    except KeyboardInterrupt:
        print("\nプログラムを終了します。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    main()