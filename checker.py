import json

def find_missing_urls(licenses_file: str, urls_file: str, output_file: str):
    # 读取 licenses.json
    with open(licenses_file, 'r', encoding='utf-8') as f:
        licenses_data = json.load(f)

    # 读取 urls.json
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls_data = json.load(f)

    # 提取 licenses.json 中的所有 URL
    license_urls = {entry['url'] for entry in licenses_data}

    # 找出 urls.json 中不在 licenses.json 中的 URL
    missing_urls = [entry for entry in urls_data if entry['url'] not in license_urls]

    # 将结果写入到 missing-urls.json 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(missing_urls, f, ensure_ascii=False, indent=4)

    return missing_urls

if __name__ == "__main__":
    licenses_path = 'licenses.json'
    urls_path = 'urls.json'
    output_path = 'missing-urls.json'

    # 找出缺失的 URLs 并写入输出文件
    missing_urls = find_missing_urls(licenses_path, urls_path, output_path)

    # 输出结果
    if missing_urls:
        print(f"未找到的 URLs 已保存到 {output_path}")
    else:
        print("所有 URLs 都在 licenses.json 中找到。")
