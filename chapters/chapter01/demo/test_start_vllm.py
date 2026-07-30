import unittest

from start_vllm import build_command


class StartVllmTest(unittest.TestCase):
    def test_build_command_uses_openai_api_server(self):
        cmd = build_command(
            python_bin="python3",
            model="/models/qwen",
            served_model_name="Qwen/Qwen2.5-0.5B",
            host="127.0.0.1",
            port=8001,
            gpu_memory_utilization=0.2,
        )

        self.assertEqual(cmd[:3], ["python3", "-m", "vllm.entrypoints.openai.api_server"])
        self.assertIn("--model", cmd)
        self.assertIn("/models/qwen", cmd)
        self.assertIn("--served-model-name", cmd)
        self.assertIn("Qwen/Qwen2.5-0.5B", cmd)
        self.assertIn("--gpu-memory-utilization", cmd)
        self.assertIn("0.2", cmd)


if __name__ == "__main__":
    unittest.main()
