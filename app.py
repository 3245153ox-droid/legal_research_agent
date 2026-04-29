from pathlib import Path
import tempfile
import zipfile

import pandas as pd
import streamlit as st

from src.agents import LegalResearchAgent
from src.file_loader import load_file
from src.llm_client import LLMClient
from src.report_writer import build_markdown_report, write_outputs


st.set_page_config(page_title="法学多材料研究 Agent MVP", layout="wide")

st.title("法学多材料研究 Agent MVP")
st.caption("文献综述、制度分析、案例/判词抽取、论文结构生成、风险校验、Token/Credits 估算。")

with st.sidebar:
    st.header("运行参数")
    topic = st.text_input("研究主题", value="新就业形态劳动者权益保障研究")
    max_chars = st.slider("每份材料最大输入字符数", 3000, 30000, 12000, step=1000)
    st.info("默认 MOCK_MODE=true，无 API Key 也可演示。真实调用请修改 .env。")

uploaded_files = st.file_uploader(
    "上传论文、法规政策、案例、判词或研究笔记",
    type=["txt", "md", "pdf", "docx"],
    accept_multiple_files=True,
)

if st.button("运行法学研究 Agent", type="primary"):
    if not uploaded_files:
        st.error("请至少上传一份材料。")
        st.stop()

    materials = []
    with tempfile.TemporaryDirectory() as td:
        temp_dir = Path(td)
        for uf in uploaded_files:
            path = temp_dir / uf.name
            path.write_bytes(uf.read())
            materials.append(load_file(path))

    with st.spinner("Agent 正在处理材料。"):
        try:
            llm = LLMClient()
            agent = LegalResearchAgent(llm, max_chars_per_doc=max_chars)
            result = agent.run(topic=topic, materials=materials)
        except Exception as exc:
            st.exception(exc)
            st.stop()

    st.success("处理完成")

    st.subheader("输入材料")
    st.dataframe(pd.DataFrame([
        {"文件名": m.filename, "材料类型": m.source_type, "字符数": m.char_count}
        for m in result.materials
    ]), use_container_width=True)

    st.subheader("文献综述矩阵")
    st.dataframe(pd.DataFrame(result.literature_matrix), use_container_width=True)

    st.subheader("制度问题分析表")
    st.dataframe(pd.DataFrame(result.institution_analysis), use_container_width=True)

    st.subheader("案例 / 判词要素表")
    st.dataframe(pd.DataFrame(result.case_matrix), use_container_width=True)

    st.subheader("研究空白与选题比较")
    st.json(result.research_gap)

    st.subheader("论文写作方案")
    st.json(result.thesis_plan)

    st.subheader("反向校验报告")
    st.json(result.verification)

    st.subheader("Token / Credits 消耗估算")
    st.json(result.token_usage)

    report_md = build_markdown_report(result)
    st.download_button("下载 Markdown 报告", report_md, file_name="research_report.md", mime="text/markdown")

    with tempfile.TemporaryDirectory() as out_td:
        out_dir = Path(out_td)
        write_outputs(result, out_dir)
        zip_path = out_dir / "legal_research_agent_outputs.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in out_dir.iterdir():
                if p.name != zip_path.name:
                    zf.write(p, p.name)
        st.download_button(
            "下载全部输出 ZIP",
            zip_path.read_bytes(),
            file_name="legal_research_agent_outputs.zip",
            mime="application/zip",
        )
