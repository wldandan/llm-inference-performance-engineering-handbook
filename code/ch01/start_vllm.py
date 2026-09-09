"""Start a vLLM OpenAI-compatible server for chapter 01.

This script assumes the model already exists locally or can be resolved by
vLLM from the given model id/path. It does not download model files.
"""

from __future__ import annotations

import argparse
import os
import subprocess


DEFAULT_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000


def build_command(
    vllm_bin: str,
    model: str,
    served_model_name: str,
    host: str,
    port: int,
    gpu_memory_utilization: float | None,
) -> list[str]:
    cmd = [
        vllm_bin,
        "serve",
        model,
        "--served-model-name",
        served_model_name,
        "--host",
        host,
        "--port",
        str(port),
    ]
    if gpu_memory_utilization is not None:
        cmd.extend(["--gpu-memory-utilization", str(gpu_memory_utilization)])
    return cmd


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Start vLLM OpenAI-compatible server for chapter 01",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--vllm-bin", default=os.environ.get("VLLM_BIN", "vllm"))
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Hugging Face model id or local model path")
    parser.add_argument("--served-model-name", default=DEFAULT_MODEL)
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--gpu-memory-utilization", type=float, default=None)
    parser.add_argument("--dry-run", action="store_true", help="Print command without starting vLLM")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    cmd = build_command(
        vllm_bin=args.vllm_bin,
        model=args.model,
        served_model_name=args.served_model_name,
        host=args.host,
        port=args.port,
        gpu_memory_utilization=args.gpu_memory_utilization,
    )
    if args.dry_run:
        print(" ".join(cmd))
        return
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
