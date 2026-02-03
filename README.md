<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0+-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/AI-Vision%20Model-purple.svg" alt="AI Vision">
</p>

<h1 align="center">AI Image Renamer</h1>

<p align="center">
  <strong>基于 AI 视觉模型的智能图片批量重命名工具</strong>
</p>

<p align="center">
  上传图片 → AI 识别内容 → 按自定义规则重命名 → 批量下载
</p>

---

## ✨ 特性

- 🤖 **AI 智能识别** - 支持任意 OpenAI 兼容的视觉模型（通义千问、GPT-4V、DeepSeek 等）
- 📝 **自定义命名规则** - 前端可视化编辑 AI 提示词，灵活定义文件命名格式
- 📁 **批量处理** - 支持同时上传和处理多个图片文件
- 🎨 **现代化界面** - 美观的响应式 Web 界面，支持拖拽上传
- 📦 **一键下载** - 处理完成后打包下载所有重命名文件
- 🔧 **开箱即用** - 简单配置即可使用，支持多种 AI 服务商

## 📸 截图

<p align="center">
  <em>上传图片并设置命名规则</em>
</p>

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/ai-image-renamer.git
cd ai-image-renamer
```

### 2. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置 API

复制环境变量示例文件并填入你的 API 配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# API 密钥（必填）
API_KEY=your-api-key-here

# API 基础地址（必填）
API_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# 使用的模型名称
MODEL_NAME=qwen-vl-plus
```

### 4. 启动应用

```bash
python app.py
```

打开浏览器访问：**http://localhost:5000**

## 🔧 支持的 AI 服务商

| 服务商 | API_BASE_URL | 推荐模型 |
|--------|-------------|----------|
| 阿里云通义 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-vl-plus`, `qwen-vl-max` |
| OpenAI | `https://api.openai.com/v1` | `gpt-4-vision-preview`, `gpt-4o` |
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-vision` |
| 其他兼容服务 | 对应的 API 地址 | 支持视觉的模型 |

## 📝 命名规则示例

在前端界面中，你可以自定义 AI 提示词来控制文件命名格式：

### 发票/收据
```
识别图片内容，将图片命名为日期，比如：2022年5月10日，中海上湾卖水泥陈培，金额0元。
```

### 身份证
```
识别身份证信息，提取姓名和身份证号码，命名格式：姓名_身份证号
```

### 产品图片
```
识别产品图片，提取产品名称、品牌、规格，命名格式：品牌_产品名_规格
```

### 合同文件
```
识别合同信息，提取合同编号、甲方名称、签订日期，命名格式：合同编号_甲方_日期
```

## 📂 项目结构

```
ai-image-renamer/
├── app.py              # Flask 主应用
├── requirements.txt    # Python 依赖
├── .env.example        # 环境变量示例
├── .env                # 环境变量配置（需自行创建）
├── .gitignore          # Git 忽略规则
├── README.md           # 项目说明
├── templates/          # HTML 模板
│   └── index.html      # 主页面
├── static/             # 静态文件
│   └── style.css       # 样式文件
├── uploads/            # 上传文件临时存储
└── renamed/            # 重命名后的文件
```

## 🖼️ 支持的图片格式

- JPG / JPEG
- PNG
- BMP
- TIFF

## ⚠️ 注意事项

1. **API 额度**：请确保你的 API 账户有足够的调用额度
2. **文件大小**：建议单个图片文件不超过 10MB
3. **识别准确性**：AI 识别结果可能因图片质量和内容复杂度而有所差异
4. **隐私安全**：图片数据会发送到 AI 服务商，请注意隐私保护

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## ⭐ Star History

如果这个项目对你有帮助，请给一个 ⭐ Star 支持一下！

---

<p align="center">
  Made with ❤️ by AI Image Renamer Contributors
</p>
