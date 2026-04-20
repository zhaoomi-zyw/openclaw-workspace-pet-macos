#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

OUTDIR = "/Users/omi/.openclaw/workspace-pet-macos"
FONT = "/System/Library/Fonts/PingFang.ttc"

def load_font(size):
    try:
        return ImageFont.truetype(FONT, size)
    except:
        try:
            return ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", size)
        except:
            return ImageFont.load_default()

def annotate(path, annotations, output_name):
    img = Image.open(path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    w, h = img.size

    for ann in annotations:
        x, y = ann["x"], ann["y"]
        label = ann["label"]
        color = ann.get("color", "#E53333")
        r = ann.get("r", 10)

        # Draw circle outline
        draw.ellipse([x-r, y-r, x+r, y+r], outline=color, width=3)

        # Draw label box
        font = load_font(16)
        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        bx = x + r + 5
        by = y - text_h // 2 - 4

        draw.rectangle([bx, by, bx + text_w + 10, by + text_h + 8], fill=color)
        draw.text((bx + 5, by + 3), label, font=font, fill="white")

    img_rgb = img.convert("RGB")
    out_path = os.path.join(OUTDIR, output_name)
    img_rgb.save(out_path, "PNG")
    print(f"Saved: {out_path}")

# Step 1: Login page - annotate login/register area
annotate(
    f"{OUTDIR}/qq_step1_login.png",
    [
        {"x": 880, "y": 300, "label": "① 扫码登录", "color": "#E53333", "r": 12},
        {"x": 880, "y": 410, "label": "② 账号登录", "color": "#E53333", "r": 12},
        {"x": 880, "y": 470, "label": "③ 立即注册", "color": "#12a0e3", "r": 12},
        {"x": 1100, "y": 797, "label": "④ QQ开放平台文档", "color": "#888888", "r": 10},
    ],
    "qq_anno1_login.png"
)

# Step 2: App create page - annotate create button
annotate(
    f"{OUTDIR}/qq_step2_app.png",
    [
        {"x": 360, "y": 282, "label": "① 立即使用/创建应用", "color": "#E53333", "r": 14},
        {"x": 294, "y": 797, "label": "② 联系客服/扫码", "color": "#888888", "r": 10},
    ],
    "qq_anno2_create.png"
)

# Step 3: App credentials page
annotate(
    f"{OUTDIR}/qq_step3_creds.png",
    [
        {"x": 880, "y": 300, "label": "① 扫码登录", "color": "#E53333", "r": 12},
        {"x": 1100, "y": 797, "label": "② 查看文档", "color": "#888888", "r": 10},
        {"x": 808, "y": 499, "label": "③ 机器人Tab", "color": "#12a0e3", "r": 10},
    ],
    "qq_anno3_guild.png"
)

print("All annotations done!")
