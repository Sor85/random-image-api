import os
import random
from flask import Flask, send_from_directory, abort

app = Flask(__name__)

# 图片存放的根目录
IMAGE_ROOT_DIR = 'images'
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}

@app.route('/<category_name>')
def random_image(category_name):
    # 构建分类文件夹的完整路径
    category_path = os.path.join(IMAGE_ROOT_DIR, category_name)

    # 检查路径是否存在且为文件夹
    if not os.path.exists(category_path) or not os.path.isdir(category_path):
        abort(404, description=f"Category '{category_name}' not found.")

    # 获取文件夹下所有文件
    try:
        files = os.listdir(category_path)
    except OSError:
        abort(500, description="Error reading image directory.")

    # 筛选图片文件
    image_files = [f for f in files if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS]

    if not image_files:
        abort(404, description=f"No images found in category '{category_name}'.")

    # 随机选择一张图片
    random_image_name = random.choice(image_files)

    # 返回图片
    # send_from_directory 需要目录路径和文件名
    # 目录路径应该是相对于 app.py 的，或者绝对路径。
    # Flask 建议不要直接用 app.root_path 来构建用户提供的内容的路径，
    # 但在这里我们是从配置的 IMAGE_ROOT_DIR 读取，所以是可控的。
    # 我们需要确保 IMAGE_ROOT_DIR 是一个安全的、预期的位置。
    # `os.path.join` 会正确处理路径。
    # `send_from_directory` 的第一个参数是目录，第二个是文件名。
    # 这里的目录应该是 IMAGE_ROOT_DIR，因为 category_name 已经是其子目录了。
    # 不对，send_from_directory 的第一个参数应该是包含文件的目录，这里是 category_path
    # 但是，为了安全和 Flask 的工作方式，通常我们会使用一个相对于应用根目录的路径，
    # 或者一个已知的、安全的绝对路径。

    # 最简单且推荐的方式是，如果 IMAGE_ROOT_DIR 是相对于 app.py 的，
    # 并且我们要发送的文件在 IMAGE_ROOT_DIR/category_name/random_image_name
    # 那么 send_from_directory 的第一个参数应该是包含 category_name 的目录，即 IMAGE_ROOT_DIR
    # 然后文件名参数应该是 category_name/random_image_name
    # return send_from_directory(IMAGE_ROOT_DIR, os.path.join(category_name, random_image_name))
    # 或者，可以直接使用 category_path 作为目录，random_image_name 作为文件名
    return send_from_directory(category_path, random_image_name)


@app.route('/')
def index():
    return "图床已启动。请访问 /文件夹名 来获取随机图片。"

if __name__ == '__main__':
    # 确保 images 目录存在
    if not os.path.exists(IMAGE_ROOT_DIR):
        os.makedirs(IMAGE_ROOT_DIR)
        print(f"'{IMAGE_ROOT_DIR}' 目录已创建。请在该目录下创建分类文件夹并放入图片。")
    
    # 监听所有可用IP，方便Docker容器访问
    app.run(host='0.0.0.0', port=5000, debug=True) 