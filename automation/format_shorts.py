#!/usr/bin/env python3
import os
from moviepy.editor import VideoFileClip

def convert_to_vertical(input_file, output_file="short_clip.mp4", start=0, end=15):
    if not os.path.exists(input_file):
        print(f"[X] Missing file: {input_file}")
        return
    clip = VideoFileClip(input_file).subclip(start, end)
    w, h = clip.size
    crop_w = int(h * (9 / 16))
    if crop_w > w: crop_w, crop_h = w, int(w * (16 / 9))
    else: crop_h = h
    cropped = clip.crop(x1=int((w - crop_w) / 2), y1=int((h - crop_h) / 2), width=crop_w, height=crop_h)
    cropped.resize((1080, 1920)).write_videofile(output_file, codec="libx264", audio_codec="aac", fps=30, preset="fast")
    clip.close()
    print(f"[✓] Vertical short saved: {output_file}")

if __name__ == "__main__":
    print("Run inside script or import function.")
