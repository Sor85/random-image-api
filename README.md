# Pixiv 图片搜索 API

这是一个基于 FastAPI 和 pixivpy 构建的 API 服务，用于从 Pixiv 上搜索指定标签的图片，并支持多标签搜索和 R18 内容过滤。

## 特性

-   通过关键词搜索 Pixiv 图片。
-   支持多个标签同时搜索（使用逗号分隔）。
-   支持 R18 内容筛选。
-   随机返回一张符合条件的图片。
-   API 直接以图片流的形式返回图片，可直接在浏览器中显示或被客户端用作图片源。
-   **新增**: 搜索结果尝试按热门度排序（`popular_desc`），以期返回更高平均质量的图片。
-   **新增**: API会尝试获取多页搜索结果（当前最多3页）并从中随机选择，以显著降低连续请求返回重复图片的概率。
-   使用 Docker 容器化部署。

## API 端点

### `GET /pixiv/direct`

根据关键词搜索 Pixiv 图片，并随机返回一张符合条件的图片。

**请求参数:**

-   `keyword` (str, 必需): 搜索关键词（标签）。多个标签请用英文逗号 `,` 分隔。例如: `tag1,tag2`。
-   `r18` (int, 可选, 默认: `0`): 是否搜索 R18 内容。
    -   `0`: 非 R18 内容。
    -   `1`: R18 内容。
-   `min_bookmarks` (int, 可选, 默认: 不筛选): 最小收藏数。如果提供此参数且值大于0，则API会尝试筛选出收藏数大于或等于指定值的图片。如果未提供或值为0，则不按收藏数筛选。

示例：http://localhost:2494/pixiv/direct?r18=0&min_bookmarks=0&keyword=

**错误响应:**

-   `400 Bad Request`: 如果 `keyword` 参数为空。
-   `404 Not Found`: 如果没有找到符合搜索条件和R18设置的图片，或者选中的图片没有可用的图片URL。
-   `500 Internal ServerError`: 如果在与 Pixiv API 通信或处理过程中发生内部错误。
-   `502 Bad Gateway`: 如果API服务器在尝试从Pixiv获取图片时遇到问题。

## 前提条件

-   一个有效的 Pixiv `refresh_token`。

## 如何获取 `PIXIV_REFRESH_TOKEN`

`pixivpy` 库需要一个 `refresh_token` 来进行认证。获取此 token 的方法如下：

**使用`pixiv_auth.py`获取`refresh_token`**:
-   在项目根目录空白处按住 Shift 并右键鼠标，从“在此处打开终端/在此处打开 Powershell 窗口/在此处打开 Linux shell”中任选其一，在弹出的命令窗口中输入：`python pixiv_auth.py login`。这将会打开一个带有 Pixiv 登录界面的浏览器。
-   通过F12打开浏览器的开发控制台并跳转至“网络（Network）”选项。
-   记录网络日志。大多数情况下打开就是默认启动的，但是还是要检查一下。
-   在筛选器中输入：`callback?` 。
-   登录你的 Pixiv 账号
-   登录后会跳转到一个空白页面，但是在开发控制台里会出现你筛选的带有 `callback?` 的访问请求，点击这条请求，将“`https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback?state=...&code=...`”中的 `code` 复制到命令窗口中。
-   这样就会获取到 `Refresh Token`。

**重要提示: 如果最后按照这个步骤没有获取到 `Refresh Token`，那么重新操作一遍，并尽可能的提高速度，`code` 会很快过期。**

教程来源：https://mwm.pw/87/

## 本地运行

1.  **克隆仓库**:
    ```bash
    # git clone https://github.com/Sor85/pixiv_search_api.git
    # cd pixiv_search_api
    ```

2.  **创建并激活虚拟环境**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate    # Windows
    ```

3.  **安装依赖**: 
    ```bash
    pip install -r requirements.txt
    ```

4.  **设置环境变量**: 
    将你的 Pixiv `refresh_token` 设置为环境变量 `PIXIV_REFRESH_TOKEN`。
    ```bash
    export PIXIV_REFRESH_TOKEN="你的_refresh_token"
    ```
    在 Windows上，可以使用 `set PIXIV_REFRESH_TOKEN="你的_refresh_token"` (cmd) 或 `$env:PIXIV_REFRESH_TOKEN="你的_refresh_token"` (PowerShell)。

5.  **运行 FastAPI 应用**: 
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 2494 --reload
    ```

    API 将在 `http://localhost:2494` 上可用。

## 使用 Docker 运行

1.  **构建 Docker 镜像**: 
    在项目根目录下运行以下命令：
    ```bash
    docker build -t pixiv-search-api .
    ```

2.  **运行 Docker 容器**: 
    ```bash
    docker run -d -p 2494:2494 -e PIXIV_REFRESH_TOKEN="你的_refresh_token" --name pixiv_api pixiv-search-api
    ```

    API 将在 `http://localhost:2494` 上可用。

## 开发

-   **代码结构**:
    -   `main.py`: FastAPI 应用主文件，包含 API 端点逻辑和 Pixiv API 交互。
    -   `Dockerfile`: 用于构建 Docker 镜像的指令。
    -   `.dockerignore`: 指定在构建 Docker 镜像时要忽略的文件和目录。
    -   `requirements.txt`: Python 依赖列表。

-   **R18 内容处理**: 
    当前实现通过在 `r18=1` 时向搜索查询中添加 "R-18" 标签来初步过滤 R18 内容。更精确的过滤可以通过检查返回结果中每个 `illust` 对象的 `x_restrict` 字段来实现 (0: 全年龄, 1: R-18G, 2: R-18)。相关过滤逻辑已在 `main.py` 中实现。

-   **减少图片重复与热门排序**:
    -   API 默认会尝试获取多达3页的搜索结果，并在这些结果中进行去重和随机选择，这有助于减少短期内重复获取相同图片的几率。
    -   搜索时，API 会请求按热门度 (`popular_desc`) 排序。请注意，此排序方式的效果可能受 Pixiv会员策略影响。
-   **按收藏数筛选**:
    -   可以通过 `min_bookmarks` 查询参数指定最小收藏数。只有当提供此参数且其值大于0时，才会进行收藏数筛选。此筛选作用于API从Pixiv获取到的（当前最多约90张）热门图片结果集之上。

## 注意事项

-   频繁请求 Pixiv API（包括一次请求中获取多页数据）可能会导致你的 IP 被临时或永久限制。请合理使用。
-   Pixiv API 的行为可能会发生变化，这可能导致此服务无法正常工作。请关注 `pixivpy` 库的更新。
-   确保你的 Pixiv 账户设置允许你查看你尝试搜索的内容类型（例如 R18 内容）。
-   获取多页数据以减少重复会略微增加单次API请求的响应时间。