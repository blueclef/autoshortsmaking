import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.prompt_builder import split_script_to_scenes, build_image_prompt

class TestPromptBuilder(unittest.TestCase):

    def test_split_script_to_scenes(self):
        """Tests if the script is split into a list of scene dictionaries."""
        script = """
        (0-3.5) 안녕하세요! [오프닝 로고]
        (4-8.1) 두 번째 장면입니다. [장면 2 비주얼]
        (10-15) 마지막 장면. [엔딩 크레딧] 
        """
        scenes = split_script_to_scenes(script)
        self.assertEqual(len(scenes), 3)
        self.assertEqual(scenes[0]['start'], 0)
        self.assertEqual(scenes[0]['end'], 3.5)
        self.assertEqual(scenes[0]['text'], "안녕하세요!")
        self.assertEqual(scenes[0]['visual'], "오프닝 로고")
        self.assertEqual(scenes[2]['text'], "마지막 장면.")

    def test_build_image_prompt(self):
        """Tests if a valid image prompt string is generated from a scene."""
        scene = {"start":0, "end":3, "text":"속보!", "visual":"뉴스 인트로"}
        prompt = build_image_prompt(scene)
        self.assertIsInstance(prompt, str)
        self.assertIn(scene['text'], prompt)
        self.assertIn(scene['visual'], prompt)
        self.assertIn("9:16 aspect ratio", prompt)

if __name__ == '__main__':
    unittest.main()
