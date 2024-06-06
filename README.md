# pytest-yorick

`pytest-yorick` is a test framework that integrates `pytest` with YAML, aiming to manage test cases using YAML files. All test information and steps are stored in YAML files. Test case designers do not need to call any Python methods, but only focus on the test data itself.

You can deploy locally by running the following command in the root directory:

```bash
pip install pytest-yorick
```

Custom parameters adapted through plugins can quickly select the corresponding test cases. The framework introduces four parameters: `suite`, `chapter`, `subchapter`, and `case`, which can be selected by ID:

```
pytest --suite ts-01 --chapter ch-01 --case tc-01
```

You can also select and execute multiple cases at once:

```
pytest --case tc-01 tc-02
```

The basic structure for managing test cases is as follows:

```
test-suite
  └── test-chapter
      └── test-subchapter (optional)
          └── test-case
```

For the YAML files of test cases, there are main files and auxiliary files. Here are examples of both:

**Main File: `tc-01-demo.yml`**
```yaml
test-name: tc-01-demo
description: "http test demo"
file-list:
  node1: "<Test-Case-Name>.http.yml"
user-data:
  id: 0001
  email: user@id.com
  pswd: qwer1234
  token_type:
  access_token:
  cookie:
test-steps:
  - node-name: node1
    message-id: get-demo-tc-01
    description: "get resource from jsonplaceholder"
```

**Auxiliary File: `tc-01-demo.http.yml`**
```yaml
MessageList:
  get-demo-tc-01:
    MessageDescription: ""
    NodeName: "node1"
    HttpMessage:
      Request:
        Method: "GET"
        Url: https://jsonplaceholder.typicode.com/posts/1
      Response:
        ResponseBody:
          id: 1
          userId: 1
          title: "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
          body: "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
        StatusCode: 200
```

In the main file, test case information and steps are managed, along with some custom user information. The auxiliary file stores detailed message content; currently, only HTTP messages are supported, but future plans include adding MySQL queries.

Auxiliary files usually share the same name as the main file, with an additional `.http` suffix. In the `file-list` of the main file, you can use `<Test-Case-Name>.http.yml` as a placeholder, which the framework will automatically recognize. The framework currently supports custom `marks` and `parametrize`, inspired by the `tavern` project.

The framework is also compatible with Allure. Users can quickly generate reports by installing Allure. For detailed steps, please refer to [Allure](https://allurereport.org/docs/install/).

You can deploy locally by running the following command in the root directory:

```bash
pip install pytest-yorick
```

The `pyproject.toml` file provides default configurations for pytest logs and allure parameters. You can add print statements in various files to observe the framework's execution flow for learning purposes. If you have installed allure, you can open the report using the following command:

```bash
allure serve ./allure-results
```

#### Acknowledgements
`pytest-yorick` makes use of several excellent open-source projects:
- [pytest](https://docs.pytest.org/en/latest/)
- [requests](http://docs.python-requests.org/en/master/)
- [pyyaml](https://github.com/yaml/pyyaml)
- [fastjsonschema](https://github.com/horejsek/python-fastjsonschema)
- [tavern](https://github.com/taverntesting/tavern)


---

# pytest-yorick

本项目是一种 pytest + YAML 测试框架，意在使用 YAML 文件对测试用例进行管理。所有的测试信息及步骤都保存在 YAML 文件中。测试用例设计者无需调用任何一种 Python 方法，只需关注测试数据本身。

你可以通过在本地进行部署，在根目录运行以下命令：

```bash
pip install pytest-yorick
```


通过插件适配的自定义参数可以快速选择对应的测试用例。框架新增了 `suite`、`chapter`、`subchapter`、`case` 四种参数，通过 ID 对 case 进行选择：

```
pytest --suite ts-01 --chapter ch-01 --case tc-01
```

你也可以同时选择多个进行执行：

```
pytest --case tc-01 tc-02
```

测试用例管理的基本结构如下：

```
test-suite
  └── test-chapter
      └── test-subchapter (optional)
          └── test-case
```
对于测试用例的 YAML 文件，分为主文件和附属文件，以下是主副文件的例子：

**主文件：`tc-01-demo.yml`**
```yaml
test-name: tc-01-demo
description: "http test demo"
file-list:
  node1: "<Test-Case-Name>.http.yml"
user-data:
  id: 0001
  email: user@id.com
  pswd: qwer1234
  token_type:
  access_token:
  cookie:
test-steps:
  - node-name: node1
    message-id: get-demo-tc-01
    description: "get resource from jsonplaceholder"
```

**附属文件：`tc-01-demo.http.yml`**
```yaml
MessageList:
  get-demo-tc-01:
    MessageDescription: ""
    NodeName: "node1"
    HttpMessage:
      Request:
        Method: "GET"
        Url: https://jsonplaceholder.typicode.com/posts/1
      Response:
        ResponseBody:
          id: 1
          userId: 1
          title: "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
          body: "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
        StatusCode: 200
```

在主文件中主要管理了用例信息和步骤，以及一些自定义的用户信息。在附属文件中存储了详细的消息内容，目前仅支持 HTTP 消息，未来计划新增 MySQL 等查询语句。

附属文件通常与主文件同名，多增加 `.http` 的后缀。在主文件的 `file-list` 中可以使用 `<Test-Case-Name>.http.yml` 作为占位符，框架会自动识别。框架目前支持自定义的 `marks` 和 `parametrize`，这一点参考了 `tavern` 项目的设计。

框架同时适配了 Allure，使用者可以通过安装 Allure 快速生成报告。详细流程可见：[Allure](https://allurereport.org/docs/install/)。

你可以通过在本地进行部署，在根目录运行以下命令：

```bash
pip install pytest-yorick
```

`pyproject.toml` 文件默认提供了 pytest 相关的日志和 allure 参数。你可以在各个文件中添加打印语句来查看框架的运行流程供学习。如果你已安装了 allure，可以通过以下命令来打开报告：

```bash
allure serve ./allure-results
```

#### 鸣谢
`pytest-yorick` 使用了以下优秀的开源项目：
- [pytest](https://docs.pytest.org/en/latest/)
- [requests](http://docs.python-requests.org/en/master/)
- [pyyaml](https://github.com/yaml/pyyaml)
- [fastjsonschema](https://github.com/horejsek/python-fastjsonschema)
- [tavern](https://github.com/taverntesting/tavern)
