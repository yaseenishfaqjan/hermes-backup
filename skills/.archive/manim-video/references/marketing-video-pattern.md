# Marketing Video Pattern with Manim

Quick-start pattern for creating animated marketing/promotional videos using Manim. Produces 30-60 second explainer videos with problem/solution/CTA structure.

## When to Use

- User wants a "marketing video" for their product/service
- Need a short promo for social media (YouTube, Instagram, TikTok)
- Want animated text/graphics without complex math
- Need fast turnaround (no voiceover, no 3D)

## Structure

Standard 5-scene structure:

1. **Intro** - Brand name + tagline (3-5 seconds)
2. **Problem** - Pain points the customer faces (8-10 seconds)
3. **Solution** - How your product/service solves it (10-12 seconds)
4. **Proof/ROI** - Results, benefits, social proof (8-10 seconds)
5. **CTA** - Call to action with website/offer (5-8 seconds)

Total: ~40-55 seconds

## Color Palettes for Marketing

| Style | Background | Primary | Secondary | Accent | Use For |
|-------|-----------|---------|-----------|--------|---------|
| **Tech/SaaS** | `#0A0A0A` | `#00D4FF` | `#7B2D8E` | `#FFD700` | Software, automation |
| **Warm/Education** | `#1A1A2E` | `#E94560` | `#0F3460` | `#FFD700` | Courses, tutoring |
| **Professional** | `#1C1C1C` | `#58C4DD` | `#83C167` | `#FFFF00` | B2B services |
| **Healthcare** | `#0D1B2A` | `#1B9AAA` | `#EF476F` | `#FFC43D` | Medical, wellness |

## Scene Templates

### Intro Scene
```python
class IntroScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text("YOUR BRAND", font_size=72, color=PRIMARY, weight=BOLD)
        subtitle = Text("Your Tagline Here", font_size=32, color=WHITE)
        title.move_to(UP * 1.5)
        subtitle.move_to(DOWN * 0.5)
        self.play(Write(title), run_time=1.5)
        self.play(Write(subtitle), run_time=1)
        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1)
```

### Problem Scene
```python
class ProblemScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text("The Problem", font_size=48, color=ACCENT, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title, run_time=1))
        
        problems = VGroup(
            Text("❌ Pain point 1", font_size=30, color=WHITE),
            Text("❌ Pain point 2", font_size=30, color=WHITE),
            Text("❌ Pain point 3", font_size=30, color=WHITE),
        ).arrange(DOWN, buff=0.5)
        
        for problem in problems:
            self.play(Write(problem, run_time=0.8))
            self.wait(0.3)
        
        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1)
```

### Solution Scene
```python
class SolutionScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text("The Solution", font_size=48, color=PRIMARY, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title, run_time=1))
        
        features = VGroup(
            Text("✓ Feature 1", font_size=28, color=WHITE),
            Text("✓ Feature 2", font_size=28, color=WHITE),
            Text("✓ Feature 3", font_size=28, color=WHITE),
        ).arrange(DOWN, buff=0.4)
        
        for feature in features:
            self.play(Write(feature, run_time=0.7))
            self.wait(0.2)
        
        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1)
```

### ROI/Comparison Scene
```python
class ROIScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Before/After boxes side by side
        before_box = Rectangle(width=4, height=5, color=RED)
        after_box = Rectangle(width=4, height=5, color=GREEN)
        # ... add stats text inside each
        arrow = Arrow(before_box.get_right(), after_box.get_left(), color=PRIMARY)
        self.play(Create(before_box), Create(after_box), Create(arrow))
        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1)
```

### CTA Scene
```python
class CTAScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        cta_title = Text("Ready to Start?", font_size=48, color=PRIMARY, weight=BOLD)
        website = Text("yourwebsite.com", font_size=40, color=ACCENT)
        offer = Text("Special Offer!", font_size=36, color=GREEN, weight=BOLD)
        
        self.play(Write(cta_title, run_time=1.5))
        self.play(Write(website, run_time=1))
        self.play(Write(offer, run_time=1))
        
        # Pulse animation on key element
        self.play(offer.animate.scale(1.2), run_time=0.5)
        self.play(offer.animate.scale(1/1.2), run_time=0.5)
        
        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1)
```

## Rendering & Stitching

### Render all scenes (draft quality)
```bash
manim -ql script.py IntroScene ProblemScene SolutionScene ROIScene CTAScene
```

### Stitch into final video
```bash
cat > concat.txt << 'EOF'
file 'media/videos/script/480p15/IntroScene.mp4'
file 'media/videos/script/480p15/ProblemScene.mp4'
file 'media/videos/script/480p15/SolutionScene.mp4'
file 'media/videos/script/480p15/ROIScene.mp4'
file 'media/videos/script/480p15/CTAScene.mp4'
EOF
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy final.mp4
```

## Emoji Support

Manim supports emoji in Text() on most systems. If emoji don't render:
- Use Unicode characters instead (✓, ✗, →, ↑, ⚡, ⭐)
- Or replace with simple shapes (Circle, Star, Arrow)

## Tips for Marketing Videos

- **Keep text minimal** - One idea per scene, max 5 bullet points
- **Use brand colors** - Consistent palette across all scenes
- **Add wait() time** - Let viewers absorb each point (1-2 seconds)
- **End with pulse** - Animate the CTA element to draw attention
- **No math needed** - Marketing videos are text + shapes, no equations
- **Resolution**: 480p15 is fine for social media; use 1080p60 for professional
- **File size**: 480p15 videos are ~1MB per minute, perfect for WhatsApp/email

## System Dependencies for Ubuntu/VPS

If installing Manim on a headless server:
```bash
apt-get update && apt-get install -y libpango1.0-dev pkg-config libcairo2-dev
pip install manim
```

LaTeX is optional for marketing videos (no math equations needed).
