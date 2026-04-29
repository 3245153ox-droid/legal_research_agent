# 法学硕士论文多材料研究 Agent MVP

这是一个可完整运行的 MVP，用于展示“法学多材料研究 Agent”的真实落地成果。它可以读取论文、法规政策、案例、判词、研究笔记等材料，自动生成：

- 文献综述矩阵
- 制度问题分析表
- 案例 / 判词要素表
- 研究空白与选题建议
- 论文问题意识、研究假设、章节结构
- 论证风险校验报告
- Token / Credits 消耗估算报告

本项目默认开启 `MOCK_MODE=true`，因此**不配置 API Key 也能跑通完整流程**，适合先用于审核演示。需要真实调用模型时，把 `.env` 中的 `MOCK_MODE=false`，并填写对应模型平台的 API 配置即可。

---

## 一、项目目录

```text
legal_research_agent_mvp/
├─ app.py                         # Streamlit 可视化界面
├─ run_agent.py                   # 命令行入口
├─ requirements.txt               # 依赖清单
├─ .env.example                   # 环境变量模板
├─ README.md                      # 使用说明
├─ 00_install_windows.ps1         # Windows 一键安装脚本
├─ 01_run_demo_windows.ps1        # Windows 一键运行示例脚本
├─ 02_start_app_windows.ps1       # Windows 启动可视化界面脚本
├─ samples/                       # 示例输入材料
├─ outputs_demo/                  # 预生成示例输出
└─ src/
   ├─ __init__.py
   ├─ agents.py                   # Agent 工作流
   ├─ file_loader.py              # 文件读取
   ├─ llm_client.py               # 模型调用与 mock 模式
   ├─ report_writer.py            # 报告输出
   └─ schemas.py                  # 数据结构
```

---

## 二、最快运行方式：Windows PowerShell

进入项目目录后运行：

```powershell
.\00_install_windows.ps1
.\01_run_demo_windows.ps1
```

运行完成后查看：

```text
outputs/
├─ research_report.md
├─ research_data.json
├─ literature_matrix.csv
├─ institution_analysis.csv
├─ case_matrix.csv
└─ token_usage.json
```

启动可视化界面：

```powershell
.\02_start_app_windows.ps1
```

---

## 三、手动运行方式

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run_agent.py --topic "新就业形态劳动者权益保障研究" --input samples --out outputs
```

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run_agent.py --topic "新就业形态劳动者权益保障研究" --input samples --out outputs
```

---

## 四、真实模型调用配置

编辑 `.env`：

```env
LLM_API_KEY=你的API_KEY
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
MOCK_MODE=false
```

如果使用 OpenAI-compatible 平台，只要它支持 `/chat/completions`，通常替换 `LLM_BASE_URL` 和 `LLM_MODEL` 即可。

---

## 五、审核时如何展示

建议提交或截图以下材料：

1. `app.py` 可视化界面：上传多份材料并运行 Agent；
2. `research_report.md`：完整研究报告；
3. `literature_matrix.csv`：文献综述矩阵；
4. `case_matrix.csv`：案例 / 判词要素表；
5. `token_usage.json`：Token / Credits 消耗估算；
6. `src/agents.py`：证明项目不是普通问答，而是多阶段 Agent 工作流。

---

## 六、项目成果描述可直接填写

我构建了一个面向法学硕士论文写作的“法学多材料研究 Agent MVP”。它用于解决论文前期研究中材料量大、文献分类困难、制度逻辑难以提炼、案例或判词要素抽取效率低的问题。该 Agent 将论文写作前期流程拆解为“材料解析—文献矩阵生成—制度问题识别—案例/判词要素抽取—研究空白判断—论文结构生成—论证风险校验”七个环节，能够把论文、法规、政策、案例、判词和研究笔记转化为可直接服务论文写作的结构化成果。

该项目属于高频长文本、多材料、多轮推理场景。一次完整任务通常需要处理多份文献、政策、案例或判词材料，并反复进行解析、归类、比较、改写和校验，因此对 Token / Credits 的消耗较高。项目输出包括文献综述矩阵、制度分析表、案例要素表、研究空白表、论文大纲和风险校验报告，可作为论文选题、文献综述和课程论文写作的基础材料。

---

## 七、注意事项

本项目是学术研究辅助工具，不替代正式法律意见。所有输出均需回到原始文献、法条和案例原文核验。
