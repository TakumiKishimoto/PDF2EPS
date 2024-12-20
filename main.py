import os
import subprocess
import argparse

def convert_all_pdfs_to_eps(input_folder, output_folder, convert_all=False):
    # 入力フォルダ内のすべてのPDFを処理
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_pdf = os.path.join(input_folder, filename)
            output_eps = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.eps")

            # 変換対象がない場合はスキップ（convert_all=Falseのとき）
            if not convert_all and os.path.exists(output_eps):
                print(f"スキップ: {output_eps}（すでに存在）")
                continue
            
            try:
                # Ghostscriptコマンドを作成
                command = [
                    "gs", 
                    "-dNOPAUSE", "-dBATCH", "-dSAFER",
                    "-sDEVICE=eps2write",
                    f"-sOutputFile={output_eps}",
                    input_pdf
                ]
                # コマンドを実行
                subprocess.run(command, check=True)
                print(f"変換完了: {output_eps}")
            except subprocess.CalledProcessError as e:
                print(f"エラー: {e} - {filename}")

if __name__ == "__main__":
    # コマンドライン引数を解析
    parser = argparse.ArgumentParser(description="PDFをEPSに変換")
    parser.add_argument("input_folder", help="PDFが入ったフォルダ")
    parser.add_argument("output_folder", help="EPSを出力するフォルダ")
    parser.add_argument("--all", action="store_true", help="すべてのPDFを変換（既存のEPSも含む）")

    args = parser.parse_args()

    # 出力フォルダが存在しない場合は作成
    os.makedirs(args.output_folder, exist_ok=True)

    # 変換を実行
    convert_all_pdfs_to_eps(args.input_folder, args.output_folder, convert_all=args.all)
