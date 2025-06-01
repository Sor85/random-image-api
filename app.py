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

    return send_from_directory(category_path, random_image_name)


@app.route('/')
def index():
    return "图床已启动。请访问 /文件夹名 来获取随机图片。"

if __name__ == '__main__':
    # 确保 images 目录存在
    if not os.path.exists(IMAGE_ROOT_DIR):
        os.makedirs(IMAGE_ROOT_DIR)
        print(f"'{IMAGE_ROOT_DIR}' 目录已创建。请在该目录下创建分类文件夹并放入图片。")
    
    app.run(host='0.0.0.0', port=5000, debug=True) 