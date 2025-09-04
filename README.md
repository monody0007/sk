# Sekai Engine

<div align="center">

### 基于MemU的智能角色扮演引擎

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

</div>

**Sekai Engine** 是一个基于 [MemU](https://github.com/NevaMind-AI/memU) 记忆框架构建的智能角色扮演引擎，能够创建具有持久记忆能力的AI角色。通过结合CrewAI的多智能体框架和MemU的记忆系统，Sekai Engine为AI角色提供了深度记忆、情感连续性和角色一致性。

## ✨ 核心特性

### 🧠 持久记忆系统
- **基于MemU框架** - 利用MemU的92%准确率记忆检索系统
- **角色记忆持久化** - 每个角色都有独立的记忆空间
- **上下文感知** - 智能检索相关记忆以增强对话质量
- **记忆演化** - 角色记忆随时间自动优化和更新

### 🎭 智能角色扮演
- **CrewAI集成** - 使用CrewAI框架进行角色推理和对话生成
- **会话级持久化** - 维护完整的对话历史和角色状态
- **多角色支持** - 同时管理多个独立角色实例
- **角色一致性** - 确保角色在长时间对话中保持人设

### 🔄 自动化工作流
- **LangGraph编排** - 使用LangGraph构建记忆-对话-存储的完整流程
- **智能记忆检索** - 自动检索相关记忆作为对话上下文
- **对话记忆存储** - 自动将对话内容存储到MemU系统
- **错误处理** - 完善的异常处理和恢复机制

## 🔑 API密钥获取

**重要提醒：** 使用Sekai Engine前，您需要先在memU官网注册并获取API密钥。

### 获取memU API密钥

1. 访问 [memU官网](https://memu.ai/) 或 [memU GitHub仓库](https://github.com/NevaMind-AI/memU)
2. 注册账户并完成身份验证
3. 在控制台中生成您的API密钥
4. 将API密钥保存到安全位置

### 环境配置

1. 复制 `example.env` 为 `.env` 文件
2. 替换其中的占位符为你的真实API密钥
3. 运行 `./runFirst.sh` 完成环境配置

## 📁 项目结构

```
sekai_engine/
├── __init__.py                 # 包初始化
├── engine.py                   # 主引擎类
├── llm_service.py             # LLM服务封装
├── memu_adapter.py            # MemU适配器
├── crewai_runner.py           # CrewAI运行器
├── crews/
│   └── world_parser.py        # 世界解析器
├── prompts/
│   ├── templates.py           # 提示模板
│   └── helpers.py            # 提示构建助手
└── utils/
    └── env.py                 # 环境变量工具
```

## 🧪 测试指南

### 自测步骤

如果你想自己测试Sekai Engine，请按照以下步骤进行：

#### 1. 运行冒烟测试
首先运行冒烟测试来验证基础功能：

```bash
python smoke_test.py
```

这个测试会验证：
- MemU API连接
- 基础记忆存储和检索功能
- 环境配置是否正确

#### 2. 等待记忆聚类完成
运行冒烟测试后，需要：
1. 登录 [memU网站](https://memu.ai/)
2. 在控制台中等待记忆聚类（clustering）过程完成
3. 这个过程可能需要几分钟时间

#### 3. 获取Agent ID
记忆聚类完成后：
1. 在memU控制台中查看生成的agent列表
2. 记录几个agent的ID（通常是一串数字或UUID格式）

#### 4. 运行多智能体测试
使用获取到的agent ID运行多智能体测试：

```bash
python test_multi.py
```

在测试脚本中，你需要：
1. 将获取到的agent ID替换到相应的变量中
2. 运行测试来验证多智能体协作功能

### 测试文件说明

- `smoke_test.py` - 基础功能冒烟测试
- `test_single.py` - 单智能体测试
- `test_multi.py` - 多智能体协作测试

## 🔧 高级功能

```python
# 获取会话统计信息
info = engine.get_session_info()

# 清除特定会话
engine.clear_user_session("user001", "agent001")

# 获取结构化响应（包含完整上下文）
response = engine.engine_service_struct(user_id, agent_id, "你的问题")
```

## 🎮 世界设定示例

项目包含一个完整的世界设定示例（`memory_data.json`），描述了50个章节的复杂故事线。

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 📄 许可证

本项目采用 Apache License 2.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢 [MemU](https://github.com/NevaMind-AI/memU)、[CrewAI](https://github.com/joaomdmoura/crewAI)、[LangGraph](https://github.com/langchain-ai/langgraph) 和 [OpenAI](https://openai.com/) 提供的技术支持。

---

**Sekai Engine** - 让AI角色拥有真实的记忆和情感连续性 🧠✨
