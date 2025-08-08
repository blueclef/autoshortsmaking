from celery import Celery
from celery.utils.log import get_task_logger
import os
import shutil

# Import the pipeline logic
from app.services.prompt_builder import split_script_to_scenes, build_image_prompt
from app.services.generator_image import generate_image
from app.services.generator_tts import synthesize_tts
from app.services.subtitle import generate_srt
from app.services.renderer import render_video

logger = get_task_logger(__name__)

# Configure Celery
# In a real app, you'd use a config file.
# Assumes Redis is running on localhost:6379
celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task(bind=True)
def create_video_task(self, script: str):
    """The main Celery task for video generation."""
    task_id = self.request.id
    base_dir = f"temp_project_{task_id}"
    os.makedirs(base_dir, exist_ok=True)

    def update_state(progress: int, message: str):
        self.update_state(state='PROGRESS', meta={'progress': progress, 'message': message})
        logger.info(f"Task {task_id}: {message}")

    try:
        update_state(5, "스크립트를 장면으로 분할 중...")
        scenes = split_script_to_scenes(script)
        if not scenes:
            raise ValueError("스크립트에서 장면을 찾을 수 없습니다.")

        update_state(10, f"{len(scenes)}개의 장면 이미지 생성 중...")
        image_paths = []
        total_duration = scenes[-1]['end']
        for i, scene in enumerate(scenes):
            progress = 10 + int(40 * (i / len(scenes)))
            update_state(progress, f"장면 {i+1}/{len(scenes)} 이미지 생성...")
            prompt = build_image_prompt(scene)
            img_path = os.path.join(base_dir, f"scene_{i}.png")
            generate_image(prompt, img_path)
            duration = scene["end"] - scene["start"]
            image_paths.append((img_path, duration))

        update_state(50, "나레이션 음성 생성 중...")
        full_script_text = " ".join([s['text'] for s in scenes])
        audio_file = os.path.join(base_dir, "narration.mp3")
        synthesize_tts(full_script_text, audio_file, duration=total_duration)

        update_state(60, "자막 파일 생성 중...")
        subtitle_content = generate_srt(scenes)
        subtitle_file = os.path.join(base_dir, "subtitles.srt")
        with open(subtitle_file, "w", encoding="utf-8") as f:
            f.write(subtitle_content)

        update_state(70, "최종 비디오 렌더링 중...")
        output_video_file = os.path.join(base_dir, "final_video.mp4")
        render_video(image_paths, audio_file, subtitle_file, output_video_file)

        # The final result of the task
        result = {
            'progress': 100,
            'message': '작업 완료!',
            'video_url': output_video_file
        }
        return result

    except Exception as e:
        logger.error(f"Task {task_id} failed: {e}", exc_info=True)
        # You can perform cleanup here if needed
        raise
    finally:
        # In a real app, you might want to keep the files for a while
        # or upload them to cloud storage before cleaning up.
        pass
