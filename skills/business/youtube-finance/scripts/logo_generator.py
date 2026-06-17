from manim import *
import os

class GlobalSignalLogo(Scene):
    def construct(self):
        self.camera.background_color = "#0A0A1A"
        
        # Earth globe
        globe = Circle(radius=2, color=BLUE, stroke_width=2)
        globe.set_fill(BLUE, opacity=0.3)
        
        # Latitude lines
        lat_lines = VGroup()
        for i in range(-2, 3):
            if i != 0:
                line = Line(LEFT*2 + UP*i*0.7, RIGHT*2 + UP*i*0.7, color=WHITE, stroke_width=1)
                lat_lines.add(line)
        
        # Longitude lines
        long_lines = VGroup()
        for i in range(-2, 3):
            if i != 0:
                line = Line(UP*2 + RIGHT*i*0.7, DOWN*2 + RIGHT*i*0.7, color=WHITE, stroke_width=1)
                long_lines.add(line)
        
        # Signal waves
        waves = VGroup()
        for i in range(3):
            wave = Arc(radius=2.5 + i*0.5, angle=PI/3, color=BLUE, stroke_width=2)
            wave.rotate(PI/2)
            wave.move_to(UP * (2.5 + i*0.3))
            waves.add(wave)
        
        # Globe group
        globe_group = VGroup(globe, lat_lines, long_lines, waves)
        globe_group.move_to(UP * 0.5)
        
        # Glow
        glow = Circle(radius=2.2, color=BLUE, stroke_width=1)
        glow.set_fill(BLUE, opacity=0.1)
        glow.move_to(UP * 0.5)
        
        # Title
        title = Text("GLOBAL SIGNAL", font_size=48, color=WHITE, weight=BOLD)
        title.move_to(DOWN * 2)
        
        subtitle = Text("DAILY ANALYSIS", font_size=24, color=BLUE)
        subtitle.move_to(DOWN * 2.8)
        
        # Add all to scene
        self.add(globe_group, glow, title, subtitle)
        
        # Save frame
        output_dir = "/root/youtube_pipeline/assets"
        os.makedirs(output_dir, exist_ok=True)
        self.camera.capture_mobjects([globe_group, glow, title, subtitle])
        
        # Save as PNG
        from PIL import Image
        img_array = self.camera.pixel_array
        img = Image.fromarray(img_array)
        img.save(f"{output_dir}/global_signal_logo.png")
        print(f"Logo saved to: {output_dir}/global_signal_logo.png")

if __name__ == "__main__":
    print("Generating Global Signal Logo...")
    config.pixel_height = 1000
    config.pixel_width = 1000
    config.frame_height = 10
    config.frame_width = 10
    config.background_color = "#0A0A1A"
    
    scene = GlobalSignalLogo()
    scene.render()
