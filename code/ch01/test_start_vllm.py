import unittest

from start_vllm import DEFAULT_MODEL, build_command


class StartVllmTest(unittest.TestCase):
    def test_default_model_matches_chat_client(self):
        self.assertEqual(DEFAULT_MODEL, "Qwen/Qwen2.5-0.5B-Instruct")

    def test_build_command_uses_vllm_serve_cli(self):
        cmd = build_command(
            "vllm",
            model="/models/qwen",
            served_model_name="Qwen/Qwen2.5-0.5B-Instruct",
            host="127.0.0.1",
            port=8001,
            gpu_memory_utilization=0.2,
        )

        self.assertEqual(cmd[:3], ["vllm", "serve", "/models/qwen"])
        self.assertIn("--served-model-name", cmd)
        self.assertIn("Qwen/Qwen2.5-0.5B-Instruct", cmd)
        self.assertIn("--gpu-memory-utilization", cmd)
        self.assertIn("0.2", cmd)


if __name__ == "__main__":
    unittest.main()
