import unittest
import unittest.mock
import os
import sys
import shutil
import uuid

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from main import run_generation_pipeline

# Check if ffmpeg is installed
ffmpeg_installed = shutil.which('ffmpeg') is not None

class TestIntegrationPipeline(unittest.TestCase):

    def setUp(self):
        """Set up a test environment."""
        self.test_task_id = f"test_{uuid.uuid4()}"
        self.test_dir = f"temp_project_{self.test_task_id}"
        self.tasks_patcher = unittest.mock.patch.dict('main.tasks', {{}}, clear=True)
        self.mock_tasks = self.tasks_patcher.start()
        self.mock_tasks[self.test_task_id] = {{'status': 'pending'}}

    def tearDown(self):
        """Clean up the test environment."""
        self.tasks_patcher.stop()
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @unittest.skipUnless(ffmpeg_installed, "FFmpeg is not installed or not in PATH, skipping integration test.")
    def test_full_pipeline_execution(self):
        """Tests the successful execution of the entire generation pipeline."""
        # Arrange: A sample script for the test
        sample_script = """
        (0-3) 이것은 통합 테스트입니다. [테스트 로고]
        (3-6) 모든 것이 잘 작동해야 합니다. [성공 아이콘]
        """

        # Act: Run the pipeline directly
        run_generation_pipeline(self.test_task_id, sample_script)

        # Assert
        final_status = self.mock_tasks[self.test_task_id]
        self.assertEqual(final_status['status'], 'completed')
        
        expected_video_path = os.path.join(self.test_dir, "final_video.mp4")
        self.assertTrue(os.path.exists(expected_video_path), "Final video file was not created.")
        self.assertGreater(os.path.getsize(expected_video_path), 0, "Final video file is empty.")

        print(f"Integration test successful! Final video created at: {expected_video_path}")
