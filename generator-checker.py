import os
import subprocess
import re
import sys

# 定义正则表达式模式
CATEGORY_X = r"\bGPL|\bLGPL|Sleepycat License|BSD-4-Clause|\bBCL\b|JSR-275|Amazon Software License|\bRSAL\b|\bQPL\b|\bSSPL|\bCPOL|\bNPL1|Creative Commons Non-Commercial"
CATEGORY_B = r"\bCDDL1|\bCPL|\bEPL|\bIPL|\bMPL|\bSPL|OSL-3.0|UnRAR License|Erlang Public License|\bOFL\b|Ubuntu Font License Version 1.0|IPA Font License Agreement v1.0|EPL2.0|CC-BY"

def is_binary_file(file_path):
    result = subprocess.run(['perl', '-lne', 'print if -B', file_path], capture_output=True, text=True)
    return result.stdout.strip() != ''

def check_files_for_category_patterns(file_paths, category_pattern):
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if re.search(category_pattern, content):
                    print(f"The package shouldn't include invalid ASF category dependencies in {file_path}")
                    sys.exit(1)
        except UnicodeDecodeError:
            print(f"Binary file detected: {file_path}, skipping...")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

def main():
    # 获取 licenses 文件夹路径
    licenses_dir = os.path.join(os.getcwd(), 'licenses')

    if not os.path.exists(licenses_dir):
        print("The 'licenses' directory does not exist.")
        return

    # 获取 licenses 文件夹中的所有文件
    files = [os.path.join(licenses_dir, f) for f in os.listdir(licenses_dir) if os.path.isfile(os.path.join(licenses_dir, f))]
    text_files = [f for f in files if not is_binary_file(f)]

    # 检查 LICENSE 和 NOTICE 文件
    license_notice_files = [f for f in text_files if os.path.basename(f) in ['LICENSE', 'NOTICE']]

    # 检查 CATEGORY_X 和 CATEGORY_B 字符串
    check_files_for_category_patterns(license_notice_files, CATEGORY_X)
    check_files_for_category_patterns(license_notice_files, CATEGORY_B)

if __name__ == '__main__':
    main()
