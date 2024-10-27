# 前置准备

1. install-dist 模块下 known-dependencies.txt 和 all_dependencies 下面的 jar 包
2. mvn dependency:tree 的输出

# 步骤

- 通过 [url.py](url.py) 生成 [urls.json](urls.json)，其中包含 jar 包名和对应的 maven 仓库 url
 - jffi-1.2.16-native.jar 和 jffi-1.2.16.jar 对应的 url 一样
- 通过 [spider.py](spider.py) 在 url 中爬取 license 信息
  - 有些可能爬不到，在后续 match 阶段特判
- 通过 [merger.py](merger.py) 将爬取 license 信息整合，以 url 为 key
- 通过 [matcher.py](matcher.py) 匹配 license 规则
  - 保证每个 jar 都有对应的 license 规则
- 通过 [generator.py](generator.py) 生成 license 描述和文件
