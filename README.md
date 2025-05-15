# Random-image

这是一个简单的 Flask 应用，用于提供一个 API，根据指定的分类随机返回图片。

## 功能

-   通过 URL 访问指定分类下的随机图片。
-   支持常见的图片格式: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`。

## 项目结构

```
.
├── app.py
├── images/
│   ├── category1/
│   │   ├── image1.jpg
│   │   └── image2.png
│   └── category2/
│       └── image3.gif
└── README.md
```

## 先决条件

-   Python 3.x
-   Flask

## 安装

1.  克隆本仓库:
    ```bash
    git clone [<repository-url>](https://github.com/Sor85/Random-image.git)
    cd Random-image
    ```
2.  安装依赖:
    ```bash
    pip install Flask
    ```

## 使用方法

1.  **准备图片:**
    在项目根目录下创建 `images` 文件夹。
    在 `images` 文件夹下，创建不同的子文件夹作为图片分类，例如 `images/cats`, `images/dogs`。
    将相应的图片放入对应的分类文件夹中。

2.  **运行应用:**
    ```bash
    python app.py
    ```
    应用默认会在 `http://0.0.0.0:5000/` 启动。
    启动时，如果 `images` 目录不存在，会自动创建。

3.  **获取随机图片:**
    打开浏览器或使用 API 测试工具访问以下 URL 格式:
    `http://localhost:5000/<category_name>`

    例如，如果您有一个名为 `cats` 的分类，并且其中有图片，您可以访问:
    `http://localhost:5000/cats`
    每次访问该 URL，都会随机返回 `images/cats/` 文件夹下的一张图片。

## 示例

假设你的 `images` 目录结构如下:

```
images/
├── nature/
│   ├── mountain.jpg
│   └── forest.png
└── animals/
    ├── cat.gif
    └── dog.jpeg
```

-   要获取 `nature` 分类下的随机图片，访问 `http://localhost:5000/nature`。
-   要获取 `animals` 分类下的随机图片，访问 `http://localhost:5000/animals`。

## Docker (可选)

如果您希望使用 Docker 运行此应用，可以创建一个类似如下的 `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# 创建 images 目录，如果应用启动时没有处理好权限问题，可以在这里创建
RUN mkdir -p images

EXPOSE 5000

CMD ["python", "app.py"]
```

您还需要一个 `requirements.txt` 文件，内容为:
```
Flask
```

然后构建并运行 Docker 镜像:
```bash
docker build -t random-image-api .
docker run -p 5000:5000 -v $(pwd)/images:/app/images random-image-api
```
请确保将 `$(pwd)/images` 替换为您本地 `images` 文件夹的实际绝对路径，以便将本地图片挂载到容器中。

## 注意事项

-   `IMAGE_ROOT_DIR` 在 `app.py` 中定义为 'images'。所有图片分类文件夹都应在此目录下。
-   应用在调试模式下运行 (`debug=True`)。对于生产环境，请将其设置为 `False`。

## 许可证

本项目采用 MIT 许可证。 
