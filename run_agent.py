import argparse
from pathlib import Path

from src.agents import LegalResearchAgent
from src.file_loader import load_materials
from src.llm_client import LLMClient
from src.report_writer import write_outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="法学多材料研究 Agent MVP")
    parser.add_argument("--topic", required=True, help="研究主题")
    parser.add_argument("--input", default="samples", help="输入文件夹或单个文件路径")
    parser.add_argument("--out", default="outputs", help="输出目录")
    parser.add_argument("--max-chars-per-doc", type=int, default=12000, help="每份材料最大输入字符数")
    args = parser.parse_args()

    materials = load_materials(args.input)
    if not materials:
        raise RuntimeError(f"没有读取到可处理材料：{args.input}")

    llm = LLMClient()
    agent = LegalResearchAgent(llm, max_chars_per_doc=args.max_chars_per_doc)
    result = agent.run(topic=args.topic, materials=materials)
    write_outputs(result, args.out)

    print(f"运行完成。输出目录：{Path(args.out).resolve()}")


if __name__ == "__main__":
    main()
