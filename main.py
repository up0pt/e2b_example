from e2b_code_interpreter import Sandbox

# コンテキストマネージャ（終了時に自動クリーンアップ）
with Sandbox.create() as sandbox:
    # --- 1回目の実行：変数定義 ---
    r1 = sandbox.run_code("x = 42; x")
    print("[run1]", r1.text)  # -> 42

    # --- 2回目の実行：状態が保持されている（xは残っている） ---
    r2 = sandbox.run_code("x = x + 1; x")
    print("[run2]", r2.text)  # -> 43

    # --- 3回目：ライブラリ読み込み & データを保持 ---
    code3 = """
import pandas as pd
df = pd.DataFrame({"a":[1,2,3], "b":[4,5,6]})
df.shape
"""
    r3 = sandbox.run_code(code3)
    print("[run3]", r3.text)  # -> (3, 2)

    # --- 4回目：前回の df を再利用して加工 ---
    code4 = """
df['c'] = df['a'] + df['b']
df.to_string(index=False)
"""
    r4 = sandbox.run_code(code4)
    print("[run4]\\n" + r4.text)

    # --- 5回目：ファイル出力（成果物を残す例） ---
    code5 = """
with open("summary.txt", "w", encoding="utf-8") as f:
    f.write("x=" + str(x) + "\\n")
    f.write(df.describe().to_string())
"written"
"""
    r5 = sandbox.run_code(code5)
    print("[run5]", r5.text)  # -> written