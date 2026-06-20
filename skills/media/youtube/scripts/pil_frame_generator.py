#!/usr/bin/env python3
"""
PIL + FFmpeg Frame Generator - Fallback when image generation APIs fail
Generates professional video frames with text overlays, screenshots, and avatars.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Config
WIDTH, HEIGHT = 1920, 1080
FPS = 30
DARK = (10, 10, 15)
NAVY = (15, 23, 42)
PURPLE = (124, 58, 237)
BLUE = (59, 130, 246)
CYAN = (6, 182, 212)
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)
RED = (239, 68, 68)


def get_font(size):
    """Load system fonts with fallback"""
    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf',
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                pass
    return ImageFont.load_default()


def create_bg():
    """Create gradient background"""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARK)
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(DARK[0] * (1 - ratio) + NAVY[0] * ratio)
        g = int(DARK[1] * (1 - ratio) + NAVY[1] * ratio)
        b = int(DARK[2] * (1 - ratio) + NAVY[2] * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img, draw


def add_text_centered(draw, text, y_offset, font, color, width, shadow=True):
    """Add centered text with optional shadow"""
    lines = text.split('\n')
    total_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)
    total_height += (len(lines) - 1) * 20
    current_y = y_offset - total_height // 2
    for line in lines:
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        if shadow:
            draw.text((x+3, current_y+3), line, font=font, fill=(0, 0, 0))
        draw.text((x, current_y), line, font=font, fill=color)
        current_y += text_height + 20


def add_screenshot(img, screenshot_path, x, y, w, h):
    """Add screenshot with rounded corners and shadow"""
    if not os.path.exists(screenshot_path):
        return
    try:
        ss = Image.open(screenshot_path).convert('RGB')
        ss = ss.resize((w, h), Image.Resampling.LANCZOS)
        
        mask = Image.new('L', (w, h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, w, h], radius=20, fill=255)
        
        shadow = Image.new('RGBA', (w+20, h+20), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle([10, 10, w+10, h+10], radius=20, fill=(0, 0, 0, 100))
        img.paste(shadow, (x-10, y-10), shadow)
        
        img.paste(ss, (x, y), mask)
        
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([x, y, x+w, y+h], radius=20, outline=PURPLE, width=3)
    except Exception as e:
        print(f"Screenshot error: {e}")


def add_avatar(img, avatar_path, x, y, size):
    """Add circular avatar with glow effect"""
    if not os.path.exists(avatar_path):
        return
    try:
        av = Image.open(avatar_path).convert('RGBA')
        av = av.resize((size, size), Image.Resampling.LANCZOS)
        
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, size, size], fill=255)
        
        glow = Image.new('RGBA', (size+40, size+40), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse([0, 0, size+40, size+40], fill=(124, 58, 237, 80))
        img.paste(glow, (x-20, y-20), glow)
        
        img.paste(av, (x, y), mask)
        
        draw = ImageDraw.Draw(img)
        draw.ellipse([x, y, x+size, y+size], outline=PURPLE, width=4)
    except Exception as e:
        print(f"Avatar error: {e}")


def generate_video(frames_dir, output_dir, scenes, images, avatar_path, voiceover_path):
    """Generate complete video from scenes"""
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    frame_count = 0
    for scene_name, duration in scenes:
        num_frames = duration * FPS
        print(f'Generating {scene_name}: {num_frames} frames...')
        
        for i in range(num_frames):
            frame_num = frame_count + i
            frame_file = f'{frames_dir}/frame_{frame_num:05d}.png'
            
            img, draw = create_bg()
            
            if scene_name == 'hook':
                font = get_font(80)
                add_text_centered(draw, 'A Hailstorm Just Hit\nYour Service Area', 400, font, WHITE, WIDTH)
                sub = get_font(32)
                add_text_centered(draw, 'Your competitors are already calling those homeowners.', 600, sub, GRAY, WIDTH)
                
            elif scene_name == 'problem':
                font = get_font(64)
                add_text_centered(draw, 'Most Roofers Miss 60%\nof Storm Leads', 400, font, WHITE, WIDTH)
                sub = get_font(24)
                add_text_centered(draw, 'Juggling weather sites, spreadsheets, and 3 different apps', 600, sub, GRAY, WIDTH)
                
            elif scene_name == 'solution':
                draw.rounded_rectangle([WIDTH//2-300, 200, WIDTH//2+300, 400], radius=30, fill=PURPLE)
                font = get_font(56)
                add_text_centered(draw, 'GlobalShield', 300, font, WHITE, WIDTH)
                sub = get_font(24)
                add_text_centered(draw, 'ROOFING OS', 370, sub, (200, 200, 255), WIDTH)
                tag = get_font(32)
                add_text_centered(draw, 'The first AI command center for storm restoration roofers', 550, tag, GRAY, WIDTH)
                
            elif scene_name.startswith('show_software') and images:
                idx = int(scene_name.replace('show_software', '')) - 1
                if idx < len(images):
                    add_screenshot(img, images[idx], 200, 150, 1520, 700)
                font = get_font(36)
                add_text_centered(draw, 'See How It Works', 900, font, WHITE, WIDTH)
                
            elif scene_name == 'features':
                font = get_font(48)
                add_text_centered(draw, 'All Connected in One Platform', 150, font, WHITE, WIDTH)
                feats = ['Storm Intel', 'AI Calling', 'Estimates', 'Dispatch', 'Payments', 'Dashboard']
                icons = ['🌩️','🤖','📐','🚐','💳','📊']
                start_x = WIDTH // 2 - (len(feats) * 250) // 2
                for idx, label in enumerate(feats):
                    x = start_x + idx * 250
                    y = 350
                    draw.ellipse([x+75, y, x+175, y+100], fill=(124, 58, 237, 50))
                    icon_font = get_font(40)
                    draw.text((x+100, y+20), icons[idx], font=icon_font, fill=WHITE)
                    label_font = get_font(20)
                    lb = label_font.getbbox(label)
                    lw = lb[2] - lb[0]
                    draw.text((x+125-lw//2, y+120), label, font=label_font, fill=GRAY)
                    
            elif scene_name == 'cta':
                add_avatar(img, avatar_path, 200, 300, 300)
                font = get_font(64)
                draw.text((600, 280), 'Stop Losing', font=font, fill=WHITE)
                draw.text((600, 370), 'Storm Jobs', font=font, fill=WHITE)
                sub = get_font(32)
                draw.text((600, 480), 'Book your free demo today', font=sub, fill=CYAN)
                url = get_font(28)
                draw.text((600, 550), 'scalaro.io', font=url, fill=PURPLE)
            
            img.save(frame_file, 'PNG')
        
        frame_count += num_frames
    
    print(f'\n✅ Generated {frame_count} frames')
    print(f'⏱️ Total duration: {frame_count / FPS:.1f} seconds')
    
    # Assemble with ffmpeg
    final_video = f'{output_dir}/final_video.mp4'
    cmd = f'ffmpeg -y -framerate {FPS} -i {frames_dir}/frame_%05d.png -i {voiceover_path} -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest {final_video}'
    print(f'\n🔧 Running: {cmd}')
    os.system(cmd)
    
    if os.path.exists(final_video):
        print(f'✅ Video created: {final_video}')
        return final_video
    else:
        print('❌ Video creation failed')
        return None


if __name__ == '__main__':
    # Example usage
    scenes = [
        ('hook', 8),
        ('problem', 10),
        ('solution', 8),
        ('show_software1', 12),
        ('show_software2', 12),
        ('features', 10),
        ('cta', 15),
    ]
    
    images = [
        '/path/to/screenshot1.png',
        '/path/to/screenshot2.png',
    ]
    
    generate_video(
        frames_dir='/tmp/video_frames',
        output_dir='/tmp/video_output',
        scenes=scenes,
        images=images,
        avatar_path='/path/to/avatar.png',
        voiceover_path='/path/to/voiceover.mp3'
    )
