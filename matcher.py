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

predefined_rules = {
    # predefined rule for overriding
    "json-20210307.jar": "Public Domain",
    "java-cup-runtime-11b-20160615.jar": "Historical Permission Notice and Disclaimer",
    "LatencyUtils-2.0.3.jar": "BSD-2-Clause",
    # for unknown rule in licenses.json
    "jakarta.activation-2.0.0.jar": "BSD-3-Clause",
    "netty-tcnative-boringssl-static-2.0.36.Final.jar": "Apache 2.0",
    "netty-tcnative-classes-2.0.46.Final.jar": "Apache 2.0",
    "sjk-jfr5-0.5.jar": "Apache 2.0",
    "sjk-jfr6-0.7.jar": "Apache 2.0",
    "sjk-nps-0.9.jar": "Apache 2.0",
    # for multiple license (greater than 2)
    "javassist-3.21.0-GA.jar": "Apache 2.0",
    "javassist-3.24.0-GA.jar": "Apache 2.0",
    "javassist-3.28.0-GA.jar": "Apache 2.0",
    "jersey-apache-connector-3.0.3.jar": "EPL 2.0",
    "jersey-client-3.0.3.jar": "EPL 2.0",
    "jersey-common-3.0.3.jar": "EPL 2.0",
    "jersey-container-grizzly2-http-3.0.3.jar": "EPL 2.0",
    "jersey-container-grizzly2-servlet-3.0.3.jar": "EPL 2.0",
    "jersey-container-servlet-3.0.3.jar": "EPL 2.0",
    "jersey-container-servlet-core-3.0.3.jar": "EPL 2.0",
    "jersey-entity-filtering-3.0.3.jar": "EPL 2.0",
    "jersey-hk2-3.0.3.jar": "EPL 2.0",
    "jersey-media-jaxb-3.0.3.jar": "EPL 2.0",
    "jersey-media-json-jackson-3.0.3.jar": "EPL 2.0",
    "jersey-server-3.0.3.jar": "EPL 2.0",
    "jersey-test-framework-core-3.0.3.jar": "EPL 2.0",
    "jersey-test-framework-provider-grizzly2-3.0.3.jar": "EPL 2.0"
}


def load_jars(file_path):
    with open(file_path, 'r') as file:
        return {item['jar']: item['url'] for item in json.load(file)}


def match_licenses(licenses_file, urls_file):
    jars = load_jars(urls_file)

    with open(licenses_file, 'r') as file:
        data = json.load(file)

    results = []  # 存储结果的列表

    for jar_file, url in jars.items():
        predefined_rule = predefined_rules.get(jar_file)
        if predefined_rule is not None:
            results.append({"jar": jar_file, "url": url, "rule": predefined_rule})
            continue

        licenses = data.get(url)
        if licenses is None:
            print(f"Error: No matching rule for {jar_file} {url}, no licenses")
            continue

        license_names = list(licenses.keys())
        matched_rule = None

        if len(license_names) == 2:
            # 匹配多个许可证的规则
            for rule_name, rule_logic in multiple_license_rules.items():
                if rule_logic(license_names):
                    matched_rule = rule_name
                    break

            if matched_rule:
                results.append({"jar": jar_file, "url": url, "rule": matched_rule})
            else:
                print(f"Error: No matching rule for {jar_file} {url}, multiple licenses found: {license_names}")
        elif len(license_names) == 1:
            license_name = license_names[0]

            # 匹配单个许可证的规则
            for rule_name, rule_logic in single_license_rules.items():
                if rule_logic(license_name):
                    matched_rule = rule_name
                    break

            if matched_rule:
                results.append({"jar": jar_file, "url": url, "rule": matched_rule, "license_url": licenses[license_name]})
            else:
                print(f"Error: No matching rule for {jar_file} {url}, no matching rule for {license_name}")
        elif len(license_names) > 2:
            print(f"Error: No matching rule for {jar_file} {url}, multiple licenses found: {license_names}")

    # 将结果写入 urls.json
    with open('matched-licenses.json', 'w') as output_file:
        json.dump(results, output_file, indent=4)

if __name__ == "__main__":
    match_licenses('merged-licenses.json', 'urls.json')

# input: merged-licenses.json and urls.json
# output: matched-licenses.json
