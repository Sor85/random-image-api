# 使用官方 Python 运行时作为父镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到容器中的 /app 目录
# 首先复制 requirements.txt 以便利用 Docker 的层缓存
COPY requirements.txt .

# 安装 requirements.txt 中指定的任何所需包
RUN pip install --no-cache-dir -r requirements.txt

# 将项目的其余部分复制到工作目录
COPY . .

# 确保 app.py 和 images 目录被正确复制
# 注意：images 目录在构建时如果不存在，则不会被复制。
# 我们会在运行时通过 volume挂载 images 目录，所以构建时不一定需要它。
# 但如果希望镜像中包含一个空的 images 目录（app.py 会在启动时创建），可以添加：
# RUN mkdir -p images

# 使端口 5000 可用于此容器外部的连接
EXPOSE 5000

# 定义环境变量（如果需要的话，比如 FLASK_ENV）
# ENV FLASK_APP app.py
# ENV FLASK_RUN_HOST 0.0.0.0
# 我们已经在 app.py 中将 host 设置为 '0.0.0.0' （如果需要外部访问的话），
# 并且 debug 模式通常在生产 Docker 镜像中关闭。
# 为了简单起见，app.py 已经配置为在 0.0.0.0:5000 上运行（如果按之前建议修改了的话）。
# 如果没有修改，它会默认在 127.0.0.1:5000 运行，这在 Docker 容器中可能需要调整。
# 我们会修改 app.py 让它默认监听 0.0.0.0。

# 运行 app.py 时，应用程序将在容器内的 0.0.0.0:5000 上可用
CMD ["python", "app.py"] 