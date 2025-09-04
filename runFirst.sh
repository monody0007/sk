#!/usr/bin/env bash

# --- 0. 检查依赖 ---
# 检查 python3.12 命令是否存在
if ! command -v python3.12 &> /dev/null
then
    echo "错误：未找到 python3.12 命令。请确保 Python 3.12 已安装并在您的 PATH 中。"
    echo "如果您已安装 Python 3.12，请确保可以通过 python3.12 命令访问。"
    if [ "$is_sourced" -eq 1 ]; then
        return 1
    else
        exit 1
    fi
fi

# 验证 Python 版本
PYTHON_VERSION=$(python3.12 --version 2>&1 | awk '{print $2}')
echo "使用 Python 版本：$PYTHON_VERSION"

# --- 1. 退出 conda 环境（如果存在）---
# 检查是否在 conda 环境
if [ -n "${CONDA_DEFAULT_ENV:-}" ]; then
    echo "检测到 conda 环境 ($CONDA_DEFAULT_ENV)，正在退出..."
    # 尝试退出 conda 环境
    if command -v conda &> /dev/null; then
        conda deactivate 2>/dev/null || true
        echo "已退出 conda 环境。"
    fi
fi

# --- 2. 创建并激活虚拟环境 ---
# 检查 .venv 目录是否存在
if [ ! -d ".venv" ]; then
    echo "正在使用 Python 3.12 创建虚拟环境..."
    python3.12 -m venv .venv
else
    echo "虚拟环境已存在，检查是否使用正确的 Python 版本..."
    VENV_PYTHON_VERSION=$(.venv/bin/python --version 2>&1 | awk '{print $2}')
    if [[ "$VENV_PYTHON_VERSION" != "3.12"* ]]; then
        echo "当前虚拟环境使用 Python $VENV_PYTHON_VERSION，需要重新创建使用 Python 3.12..."
        rm -rf .venv
        python3.12 -m venv .venv
        echo "已重新创建虚拟环境。"
    else
        echo "虚拟环境已使用正确的 Python 版本。"
    fi
fi

# 激活虚拟环境（需要在当前 shell 执行才会生效）
if [ "$is_sourced" -eq 0 ]; then
    echo "提示：你正在以子进程运行脚本。激活只会在子进程生效。"
    echo "如果希望在当前 shell 中激活，请使用: source ./runFirst.sh"
fi

# shellcheck disable=SC1091
source .venv/bin/activate

# 校验是否激活成功
if [ -z "${VIRTUAL_ENV:-}" ]; then
    echo "错误：虚拟环境未成功激活。"
    echo "请尝试：source .venv/bin/activate"
    if [ "$is_sourced" -eq 1 ]; then
        return 1
    else
        exit 1
    fi
fi

echo "虚拟环境已激活：$VIRTUAL_ENV"

# 添加自动加载 .env 文件的功能到虚拟环境激活脚本
if ! grep -q "source .env" .venv/bin/activate; then
    echo "正在配置虚拟环境自动加载 .env 文件..."
    echo "" >> .venv/bin/activate
    echo "# Auto-load .env file" >> .venv/bin/activate
    echo "if [ -f \"\$VIRTUAL_ENV/../.env\" ]; then" >> .venv/bin/activate
    echo "    set -a" >> .venv/bin/activate
    echo "    source \"\$VIRTUAL_ENV/../.env\"" >> .venv/bin/activate
    echo "    set +a" >> .venv/bin/activate
    echo "fi" >> .venv/bin/activate
    echo "已配置自动加载功能。"
fi

# --- 3. 安装依赖 ---
echo "正在安装依赖 (memu-py, crewai, langgraph)..."
# 更新 pip 并安装指定的包
pip install --upgrade pip > /dev/null # 将输出重定向，保持界面干净
pip install memu-py crewai langgraph
echo "依赖安装完成。"

# --- 4. 加载 .env 文件 ---
# 检查 .env 文件是否存在于当前目录
if [ -f ".env" ]; then
    echo "正在从 .env 文件加载环境变量..."
    # 使用 set -a 和 source 命令安全地加载变量，这可以正确处理值中的空格
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
    echo "环境变量加载成功。"
else
    echo "警告：未找到 .env 文件。请确保您已创建该文件并填入了 API 密钥。"
fi

# --- 完成 ---
echo ""
echo "✅ 环境设置完成！"
echo "之后若需手动激活环境，请运行: source .venv/bin/activate"
