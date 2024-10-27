import json


def merge_licenses(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    license_dict = {}

    for entry in data:
        url = entry['url']
        license_name = entry['license_name']
        license_url = entry.get('license_url', '')

        # 如果 URL 不在字典中，初始化
        if url not in license_dict:
            license_dict[url] = {}

        # 仅在许可证名称不在字典中时添加它
        if license_name not in license_dict[url]:
            # 如果之前的 URL 为空，则更新 URL
            if license_name in license_dict[url] and license_dict[url][license_name] == '':
                license_dict[url][license_name] = license_url
            else:
                license_dict[url][license_name] = license_url if license_url else ''

    # 将合并结果写入到输出文件
    with open(output_file, 'w') as f:
        json.dump(license_dict, f, indent=4)


if __name__ == '__main__':
    merge_licenses('licenses.json', 'merged-licenses.json')

# input: licenses.json
# output: merged-licenses.json
