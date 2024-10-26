import json

# 规则定义
single_license_rules = {
    "Apache 2.0": lambda license_name: "Apache" in license_name,
    "MIT": lambda license_name: "MIT" in license_name,
    "BSD-2-Clause": lambda license_name: "BSD" in license_name and "2" in license_name,
    "BSD-3-Clause": lambda license_name: "BSD" in license_name and "3" in license_name,
    "BSD": lambda license_name: "BSD" in license_name,
    "EPL 1.0": lambda license_name: ("EPL" in license_name or "Eclipse Public License" in license_name) and "1" in license_name,
    "EPL 2.0": lambda license_name: ("EPL" in license_name or "Eclipse Public License" in license_name) and "2" in license_name,
    "ISC": lambda license_name: "ISC" in license_name,
    "EDL 1.0": lambda license_name: ("EDL" in license_name or "Eclipse Distribution License" in license_name) and "1" in license_name,
    "CDDL 1.1": lambda license_name: "CDDL" in license_name and "1.1" in license_name,
    "CDDL": lambda license_name: "CDDL" in license_name,
    "CC0 1.0": lambda license_name: "Creative Commons CC0" in license_name,
    "Public Domain": lambda license_name: "Public Domain" in license_name,
    "The JSON License": lambda license_name: "The JSON License" in license_name,
    "CUP Parser Generator Copyright Notice, License, and Disclaimer": lambda license_name: "CUP Parser Generator Copyright Notice, License, and Disclaimer" in license_name,
}

def any_match(str):
    return lambda license_names: any(single_license_rules[str](name) for name in license_names)


multiple_license_rules = {
    "Apache 2.0": any_match("Apache 2.0"),
    "EDL 1.0": any_match("EDL 1.0"),
    "EPL 2.0": any_match("EPL 2.0"),
    "CC0 1.0": any_match("CC0 1.0"),
    "MIT": any_match("MIT"),
    "CDDL": any_match("CDDL"),
    "Public Domain": any_match("Public Domain"),
}


def load_urls(file_path):
    with open(file_path, 'r') as file:
        return {item['url']: item['jar'] for item in json.load(file)}


def match_licenses(licenses_file, urls_file):
    urls = load_urls(urls_file)

    with open(licenses_file, 'r') as file:
        data = json.load(file)

    results = []  # 存储结果的列表

    for url, licenses in data.items():
        license_names = list(licenses.keys())
        matched_rule = None

        if len(license_names) > 1:
            # 匹配多个许可证的规则
            for rule_name, rule_logic in multiple_license_rules.items():
                if rule_logic(license_names):
                    matched_rule = rule_name
                    break

            jar_file = urls.get(url, "")  # 从 urls 中获取 jar 文件名
            if matched_rule:
                results.append({"jar": jar_file, "url": url, "rule": matched_rule})
            else:
                results.append({"jar": jar_file, "url": url, "rule": f"Error: Multiple licenses found: {license_names}"})
        elif len(license_names) == 1:
            license_name = license_names[0]

            # 匹配单个许可证的规则
            for rule_name, rule_logic in single_license_rules.items():
                if rule_logic(license_name):
                    matched_rule = rule_name
                    break

            jar_file = urls.get(url, "")  # 从 urls 中获取 jar 文件名
            if matched_rule:
                results.append({"jar": jar_file, "url": url, "rule": matched_rule, "license_url": licenses[license_name]})
            else:
                results.append({"jar": jar_file, "url": url, "rule": f"Error: No matching rule for {license_name}"})

    # 将结果写入 urls.json
    with open('matched-licenses.json', 'w') as output_file:
        json.dump(results, output_file, indent=4)

if __name__ == "__main__":
    match_licenses('merged-licenses.json', 'urls.json')
