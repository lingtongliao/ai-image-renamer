import os
import re
import base64
from flask import Flask, request, render_template, jsonify, send_file
from openai import OpenAI
from PIL import Image
import io
import zipfile
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 从环境变量读取API配置
API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen-vl-plus")

# 检查必要的配置
if not API_KEY or not API_BASE_URL:
    print("警告: 请在 .env 文件中配置 API_KEY 和 API_BASE_URL")
    print("可以复制 .env.example 为 .env 并填入您的配置")

# 配置API客户端
client = OpenAI(
    api_key=API_KEY or "placeholder",
    base_url=API_BASE_URL or "https://api.openai.com/v1",
)

# 默认命名规则提示词
DEFAULT_NAMING_PROMPT = "识别图片内容，将图片命名为日期，客户名称，金额，不要其他多余的文字（最后要加一个。号），比如：2022年5月10日，中海上湾卖水泥陈培，金额0元。"

# 创建必要的文件夹
os.makedirs("uploads", exist_ok=True)
os.makedirs("renamed", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)


def encode_image_to_base64(image_path):
    """将图片编码为base64格式"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_info_from_image(image_path, naming_prompt=None):
    """使用AI模型从图片中提取信息"""
    try:
        # 使用自定义或默认的命名规则
        prompt = naming_prompt if naming_prompt else DEFAULT_NAMING_PROMPT

        # 编码图片为base64
        base64_image = encode_image_to_base64(image_path)

        # 构建消息
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ]

        # 调用API
        response = client.chat.completions.create(
            model=MODEL_NAME, messages=messages, max_tokens=200
        )

        result = response.choices[0].message.content.strip()
        print(f"AI返回结果: {result}")

        # 直接返回AI生成的文件名
        return result

    except Exception as e:
        print(f"提取信息时发生错误: {e}")
        return "未知图片"


def clean_filename(text):
    """清理文件名中的非法字符"""
    # 移除或替换Windows文件名中的非法字符
    illegal_chars = '<>:"/\\|?*'
    for char in illegal_chars:
        text = text.replace(char, "")
    return text.strip()


def generate_new_filename(ai_generated_name, original_extension):
    """根据AI生成的名称生成新的文件名"""
    # 清理文件名中的非法字符
    cleaned_name = clean_filename(ai_generated_name)

    # 如果AI返回的是有效内容，使用它；否则使用时间戳
    if cleaned_name and cleaned_name != "未知图片" and len(cleaned_name.strip()) > 0:
        new_name = f"{cleaned_name}{original_extension}"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name = f"未识别_{timestamp}{original_extension}"

    return new_name


@app.route("/")
def index():
    return render_template("index.html", default_prompt=DEFAULT_NAMING_PROMPT)


@app.route("/upload", methods=["POST"])
def upload_files():
    """处理文件上传和重命名"""
    if "files" not in request.files:
        return jsonify({"error": "没有选择文件"}), 400

    files = request.files.getlist("files")
    if not files or files[0].filename == "":
        return jsonify({"error": "没有选择文件"}), 400

    # 获取前端传来的命名规则
    naming_prompt = request.form.get("naming_prompt", "").strip()
    if not naming_prompt:
        naming_prompt = DEFAULT_NAMING_PROMPT

    results = []
    renamed_files = []

    for file in files:
        if file and file.filename:
            try:
                # 保存原始文件
                original_filename = file.filename
                file_extension = os.path.splitext(original_filename)[1].lower()

                # 检查文件类型
                if file_extension not in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
                    results.append(
                        {
                            "original_name": original_filename,
                            "status": "error",
                            "message": "不支持的文件格式",
                        }
                    )
                    continue

                # 保存到uploads文件夹
                upload_path = os.path.join("uploads", original_filename)
                file.save(upload_path)

                # 使用AI生成文件名（传入命名规则）
                ai_generated_name = extract_info_from_image(upload_path, naming_prompt)

                # 生成新文件名
                new_filename = generate_new_filename(ai_generated_name, file_extension)

                # 复制文件到renamed文件夹
                renamed_path = os.path.join("renamed", new_filename)

                # 如果文件名已存在，添加序号
                counter = 1
                base_name, ext = os.path.splitext(new_filename)
                while os.path.exists(renamed_path):
                    new_filename = f"{base_name}_{counter}{ext}"
                    renamed_path = os.path.join("renamed", new_filename)
                    counter += 1

                # 复制文件
                import shutil

                shutil.copy2(upload_path, renamed_path)

                renamed_files.append(renamed_path)

                results.append(
                    {
                        "original_name": original_filename,
                        "new_name": new_filename,
                        "ai_generated_name": ai_generated_name,
                        "status": "success",
                    }
                )

            except Exception as e:
                results.append(
                    {
                        "original_name": original_filename,
                        "status": "error",
                        "message": f"处理失败: {str(e)}",
                    }
                )

    return jsonify(
        {
            "results": results,
            "total_processed": len(results),
            "success_count": len([r for r in results if r["status"] == "success"]),
        }
    )


@app.route("/download_all")
def download_all():
    """下载所有重命名后的文件（打包成zip）"""
    try:
        # 创建内存中的zip文件
        memory_file = io.BytesIO()

        with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
            renamed_dir = "renamed"
            if os.path.exists(renamed_dir):
                for filename in os.listdir(renamed_dir):
                    file_path = os.path.join(renamed_dir, filename)
                    if os.path.isfile(file_path):
                        zf.write(file_path, filename)

        memory_file.seek(0)

        return send_file(
            io.BytesIO(memory_file.read()),
            mimetype="application/zip",
            as_attachment=True,
            download_name="renamed_images.zip",
        )

    except Exception as e:
        return jsonify({"error": f"下载失败: {str(e)}"}), 500


@app.route("/clear")
def clear_files():
    """清空上传和重命名的文件"""
    try:
        import shutil

        # 清空uploads文件夹
        if os.path.exists("uploads"):
            shutil.rmtree("uploads")
            os.makedirs("uploads")

        # 清空renamed文件夹
        if os.path.exists("renamed"):
            shutil.rmtree("renamed")
            os.makedirs("renamed")

        return jsonify({"message": "文件已清空"})

    except Exception as e:
        return jsonify({"error": f"清空失败: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
