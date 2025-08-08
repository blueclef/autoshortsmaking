import subprocess
import os
from typing import List, Tuple

def render_video(scene_images: List[Tuple[str, float]], audio_file: str, subtitle_file: str, out_file: str, transition_duration: float = 0.5) -> None:
    """
    Renders a video with cross-fade transitions, audio, and subtitles using FFmpeg.

    Args:
        scene_images: A list of tuples, each containing the path to an image and its display duration.
        audio_file: The path to the audio file.
        subtitle_file: The path to the subtitle file (.srt).
        out_file: The path to save the output video file.
        transition_duration: The duration of the cross-fade transition in seconds.
    """
    if not scene_images:
        print("Error: No images provided for rendering.")
        return

    # FFmpeg command construction
    input_args = []
    filter_complex_parts = []
    total_duration = 0
    last_stream_idx = len(scene_images) - 1

    for i, (img_path, duration) in enumerate(scene_images):
        safe_img_path = img_path.replace('\\', '/')
        input_args.extend(['-loop', '1', '-t', str(duration), '-i', safe_img_path])
        
        # Scale each input image to the desired resolution
        filter_complex_parts.append(f"[{i}:v]scale=1080:1920,setsar=1[v{i}]")

    stream_count = len(scene_images)
    if stream_count > 1:
        # Chain fade transitions
        # Start with the first stream
        prev_stream = f"[v0]"
        for i in range(stream_count - 1):
            # The stream that will be faded in
            curr_stream = f"[v{i+1}]"
            # The output stream name for this stage
            output_stream = f"[vt{i}]"
            
            # Calculate the start time of the fade
            fade_start_time = sum(d for _, d in scene_images[:i+1]) - transition_duration
            
            filter_complex_parts.append(
                f"{prev_stream}{curr_stream}xfade=transition=fade:duration={transition_duration}:offset={fade_start_time}{output_stream}")
            prev_stream = output_stream
        final_video_stream = prev_stream
    else:
        final_video_stream = "[v0]"

    # Add subtitles and format the final output
    filter_complex_parts.append(f"{final_video_stream}subtitles='{subtitle_file.replace('\\', '/')}',format=yuv420p[video_out]")

    filter_complex = ";".join(filter_complex_parts)

    cmd = [
        'ffmpeg', '-y',
        *input_args,
        '-i', audio_file,
        '-filter_complex', filter_complex,
        '-map', '[video_out]',
        f'-map', f'{stream_count}:a', # Map the audio stream
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        out_file
    ]

    try:
        print("Running FFmpeg command:", " ".join(cmd))
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        print(f"Video rendered successfully and saved to {out_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg execution:")
        print(f"Stderr: {e.stderr}")
        print(f"Stdout: {e.stdout}")
    except FileNotFoundError:
        print("Error: ffmpeg is not installed or not in the system's PATH.")
