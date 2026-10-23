#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

def watermark_image(input_path, output_path, watermark_text="@TechGuideHQ1", opacity=128, position="bottom_right", font_size_ratio=0.05):
    try:
        with Image.open(input_path).convert("RGBA") as base_img:
            overlay = Image.new("RGBA", base_img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)
            img_w, img_h = base_img.size
            font_size = max(16, int(img_w * font_size_ratio))
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            margin = int(img_w * 0.03)
            x, y = img_w - text_w - margin, img_h - text_h - margin
            padding = 10
            box = [x - padding, y - padding, x + text_w + padding, y + text_h + padding]
            draw.rectangle(box, fill=(0, 0, 0, int(opacity * 0.6)))
            draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, opacity))
            watermarked = Image.alpha_composite(base_img, overlay)
            watermarked.convert("RGB").save(output_path, quality=95)
            print(f"[✓] Watermarked: {os.path.basename(input_path)}")
    except Exception as e:
        print(f"[X] Failed to process {input_path}: {e}")

def batch_watermark(input_folder="./input_images", output_folder="./watermarked_images", watermark_text="@TechGuideHQ1"):
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(input_folder, exist_ok=True)
    exts = (".png", ".jpg", ".jpeg", ".webp")
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(exts)]
    if not files:
        print(f"[{input_folder}] is empty. Place images there to run.")
        return
    for file in files:
        watermark_image(os.path.join(input_folder, file), os.path.join(output_folder, f"wm_{file}"), watermark_text)

if __name__ == "__main__":
    batch_watermark()
