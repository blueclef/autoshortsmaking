from typing import List, Dict, Any

def generate_srt(scenes: List[Dict[str, Any]]) -> str:
    """
    Generates SRT subtitle content from a list of scenes.

    Args:
        scenes: A list of scene dictionaries, each with 'start', 'end', and 'text'.

    Returns:
        A string containing the subtitles in SRT format.
    """
    srt_lines = []
    for i, scene in enumerate(scenes, 1):
        start_time = seconds_to_srt_time(scene['start'])
        end_time = seconds_to_srt_time(scene['end'])
        text = scene['text']
        srt_lines.append(f"{i}")
        srt_lines.append(f"{start_time} --> {end_time}")
        srt_lines.append(text)
        srt_lines.append("")
    return "\n".join(srt_lines)

def seconds_to_srt_time(seconds: float) -> str:
    """
    Converts seconds to SRT time format (HH:MM:SS,ms).
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"
