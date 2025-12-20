"""
Minimal test to see if FFmpeg can parse a simple filter with chunking.
"""

import tempfile
import subprocess
import os

# Create a simple test filter file
filter_content = """[0:v]drawtext=text="Test 1":fontsize=40:fontcolor=white:x=(w-text_w)/2:y=h/2:enable='between(t,0,1)'[v0];[v0]drawtext=text="Test 2":fontsize=40:fontcolor=white:x=(w-text_w)/2:y=h/2:enable='between(t,1,2)'[v]"""

filter_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8', newline='\n')
filter_file.write(filter_content)
filter_file.flush()
os.fsync(filter_file.fileno())
filter_file.close()

print(f"Created filter file: {filter_file.name}")
print(f"Content:\n{filter_content}\n")

# Test with FFmpeg
cmd = [
    "ffmpeg",
    "-f", "lavfi",
    "-i", "color=c=black:size=1280x720:duration=2:rate=24",
    "-filter_complex_script", filter_file.name,
    "-t", "1",
    "-f", "null",
    "-",
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        print("[PASS] FFmpeg parsed the filter successfully!")
    else:
        print(f"[FAIL] FFmpeg returned {result.returncode}")
        print(f"Error: {result.stderr[:500]}")
finally:
    os.unlink(filter_file.name)

