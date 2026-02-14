import numpy as np

def db(x):
    return 20 * np.log10(x)

#もし各点の不確かさの評価がきちんとできたらreduceΧ２乗がほしい

def reduced_chi2(x, y, fit, popt, sigma=None):
    """
    x: 横軸データ (numpy array)
    y: 縦軸データ (numpy array)
    fit: フィット関数 (例: lambda x, a, b: a*x + b)
    popt: フィットパラメータ (array)
    sigma: yの誤差 (array, 任意). Noneなら全て1として扱う
    """
    if sigma is None:
        sigma = np.ones_like(y)

    residuals = y - fit(x, *popt)
    chi2 = np.sum((residuals / sigma)**2)
    dof = len(y) - len(popt)  # 自由度 = データ点数 - パラメータ数
    return chi2 / dof




def find_minus_3dB_points(x, y_db, drop_db=3.01):
    """
    x     : 横軸配列
    y_db  : dB表記の縦軸 (20*log10)
    drop_db : 何 dB 下を探すか（デフォルト 3.01 dB）

    return: (x_left, x_right)
    """
    y_max = np.max(y_db)
    target = y_max - drop_db
    i_peak = np.argmax(y_db)

    # 左側
    x_left = None
    for i in range(i_peak - 1, -1, -1):
        if y_db[i] <= target <= y_db[i + 1]:
            x_left = np.interp(
                target,
                [y_db[i], y_db[i + 1]],
                [x[i], x[i + 1]]
            )
            break

    # 右側
    x_right = None
    for i in range(i_peak, len(x) - 1):
        if y_db[i] >= target >= y_db[i + 1]:
            x_right = np.interp(
                target,
                [y_db[i], y_db[i + 1]],
                [x[i], x[i + 1]]
            )
            break

    return x_left, x_right

def q_value(x, y_db, drop_db=3.01):
    x_left, x_right = find_minus_3dB_points(x, y_db, drop_db)
    x_max = x[np.argmax(y_db)]
    Q = x_max / (x_right - x_left)
    return Q