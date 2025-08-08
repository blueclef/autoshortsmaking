import re
from typing import List, Dict, Any

def split_script_to_scenes(script_text: str) -> List[Dict[str, Any]]:
    """
    Splits the script text into scenes based on a specific format.
    Expected format per line: (start_time-end_time) text [visual_hint]
    Example: (0-3.5) 안녕하세요! [오프닝 로고]
    """
    scenes = []
    # Regex to capture: (float-float) text [text]
    pattern = re.compile(r"\((\d*\.?\d+)-(\d*\.?\d+)\)\s*(.*?)\s*\[(.*?)\]")
    
    for line in script_text.strip().split('\n'):
        match = pattern.match(line.strip())
        if match:
            start_time, end_time, text, visual = match.groups()
            scenes.append({
                "start": float(start_time),
                "end": float(end_time),
                "text": text.strip(),
                "visual": visual.strip()
            })
    return scenes


def build_image_prompt(scene: Dict[str, Any]) -> str:
    """
    Builds an image generation prompt for a given scene.
    """
    base = f"A dramatic, cinematic thumbnail showing {scene['visual']}. Bold headline text overlay: '{scene['text']}'. 9:16 aspect ratio, high contrast, vibrant colors"
    return base
