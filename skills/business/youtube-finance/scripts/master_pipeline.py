#!/usr/bin/env python3
"""
Global Signal Master Pipeline
Runs complete video production: Research → Script → Voiceover → Visuals → Assembly
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Pipeline stages
STAGES = {
    "research": "/root/.hermes/skills/business/youtube-finance/scripts/research_bot.py",
    "script": "/root/.hermes/skills/business/youtube-finance/scripts/script_generator.py",
    "voiceover": "/root/.hermes/skills/business/youtube-finance/scripts/voiceover_generator.py",
    "visuals": "/root/.hermes/skills/business/youtube-finance/scripts/visual_pipeline.py",
    "assembly": "/root/.hermes/skills/business/youtube-finance/scripts/video_assembler.py"
}

def run_stage(stage_name: str, args=None):
    """Run a pipeline stage"""
    script = STAGES.get(stage_name)
    if not script or not os.path.exists(script):
        print(f"❌ Stage '{stage_name}' not found: {script}")
        return False
    
    print(f"\n{'='*60}")
    print(f"🚀 Running Stage: {stage_name.upper()}")
    print(f"{'='*60}")
    
    cmd = ["python3", script]
    if args:
        cmd.extend(args)
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True, timeout=600)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Stage {stage_name} failed: {e}")
        return False

def run_full_pipeline():
    """Run complete pipeline for today's videos"""
    print("🎬 GLOBAL SIGNAL FULL PIPELINE")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    
    # Create pipeline directories
    dirs = [
        "/root/youtube_pipeline/content_calendar",
        "/root/youtube_pipeline/scripts",
        "/root/youtube_pipeline/voiceovers",
        "/root/youtube_pipeline/visuals",
        "/root/youtube_pipeline/final_videos"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # Stage 1: Research
    if not run_stage("research"):
        print("❌ Pipeline halted at research stage")
        return
    
    # Stage 2: Script Generation
    if not run_stage("script"):
        print("❌ Pipeline halted at script stage")
        return
    
    # Stage 3: Voiceover
    if not run_stage("voiceover"):
        print("⚠️ Voiceover stage failed, continuing with visuals...")
    
    # Stage 4: Visuals (if script exists)
    today = datetime.now().strftime("%Y-%m-%d")
    scripts = list(Path("/root/youtube_pipeline/scripts").glob(f"{today}_*.txt"))
    
    for script in scripts:
        if not run_stage("visuals", [str(script)]):
            print(f"⚠️ Visuals failed for {script.name}")
    
    # Stage 5: Assembly (if voiceover exists)
    voiceovers = list(Path("/root/youtube_pipeline/voiceovers").glob(f"{today}_*_full.mp3"))
    
    for vo in voiceovers:
        script_name = vo.stem.replace("_full", "")
        script_path = f"/root/youtube_pipeline/scripts/{script_name}.txt"
        visual_dir = f"/root/youtube_pipeline/visuals/{script_name}"
        output_path = f"/root/youtube_pipeline/final_videos/{script_name}.mp4"
        
        if os.path.exists(script_path):
            if not run_stage("assembly", [script_path, str(vo), visual_dir, output_path]):
                print(f"⚠️ Assembly failed for {script_name}")
    
    print("\n" + "="*60)
    print("✅ PIPELINE COMPLETE")
    print("="*60)
    
    # Show final videos
    final_videos = list(Path("/root/youtube_pipeline/final_videos").glob(f"{today}_*.mp4"))
    print(f"\n📹 Final Videos: {len(final_videos)}")
    for v in final_videos:
        size_mb = v.stat().st_size / (1024*1024)
        print(f"   • {v.name} ({size_mb:.1f} MB)")

def run_single_video(topic_title: str, source_url: str = ""):
    """Run pipeline for a single topic"""
    print(f"🎬 Producing single video: {topic_title}")
    
    # Create topic dict
    topic = {"title": topic_title, "url": source_url or "Manual topic"}
    
    # Generate script
    from script_generator import generate_script
    script_path = generate_script(topic)
    
    if not script_path:
        print("❌ Script generation failed")
        return
    
    # Generate voiceover
    from voiceover_generator import generate_voiceover
    vo_path = generate_voiceover(script_path)
    
    if not vo_path:
        print("⚠️ Voiceover failed, continuing...")
    
    # Generate visuals
    from visual_pipeline import generate_visuals_for_script
    visual_dir = f"/root/youtube_pipeline/visuals/{Path(script_path).stem}"
    generate_visuals_for_script(script_path, visual_dir)
    
    # Assemble
    from video_assembler import assemble_video
    output_path = f"/root/youtube_pipeline/final_videos/{Path(script_path).stem}.mp4"
    
    if vo_path and os.path.exists(visual_dir):
        assemble_video(script_path, vo_path, visual_dir, output_path)
    else:
        print("⚠️ Cannot assemble - missing voiceover or visuals")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Single video mode
        topic = sys.argv[1]
        source = sys.argv[2] if len(sys.argv) > 2 else ""
        run_single_video(topic, source)
    else:
        # Full pipeline mode
        run_full_pipeline()
