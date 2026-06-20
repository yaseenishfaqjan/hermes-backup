---
name: music-production
description: "AI music production: generation tools, songwriting craft, audio analysis, and prompt engineering."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [music, audio, ai-music, generation, songwriting, audiocraft, suno, heartmula, spectrogram]
    related_skills: [p5js, ascii-video]
---

# Music Production with AI

Complete workflow for AI-assisted music production: generating music and sound effects, writing songs and lyrics, engineering prompts for AI music platforms, and analyzing audio.

## When to Use

- Generate music from text descriptions
- Create sound effects and environmental audio
- Write original songs, parodies, or adaptations
- Engineer prompts for Suno, Udio, or similar AI music platforms
- Analyze audio with spectrograms and feature extraction
- Build music generation applications or pipelines

## Decision Map

| Goal | Tool | Section |
|------|------|---------|
| Text-to-music (local, open-source) | AudioCraft / MusicGen | § Audio Generation |
| Suno-like song generation (local) | HeartMuLa | § Audio Generation |
| Songwriting, lyrics, parody | Manual craft + AI prompts | § Songwriting |
| Suno/Udio prompt engineering | Style tags + metatags | § Prompt Engineering |
| Audio analysis, spectrograms | songsee | § Audio Analysis |

---

## Audio Generation

### AudioCraft (Meta) — Text-to-Music & Sound Effects

Local Python-based generation using Meta's AudioCraft suite.

**Stack:** `audiocraft`, `torch>=2.0.0`, `transformers>=4.30.0`

**Quick start:**
```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained('facebook/musicgen-medium')
model.set_generation_params(duration=30, top_k=250, temperature=1.0, cfg_coef=3.0)
wav = model.generate(["epic orchestral soundtrack with strings and brass"])
torchaudio.save("output.wav", wav[0].cpu(), sample_rate=32000)
```

**Model variants:**
| Model | Size | Use Case |
|-------|------|----------|
| `musicgen-small` | 300M | Quick generation |
| `musicgen-medium` | 1.5B | Balanced quality/speed |
| `musicgen-large` | 3.3B | Best quality |
| `musicgen-melody` | 1.5B | Melody conditioning |
| `musicgen-stereo-*` | Varies | Stereo output |
| `audiogen-medium` | 1.5B | Sound effects |

**Key parameters:** `duration` (1-120s), `top_k` (250), `temperature` (1.0), `cfg_coef` (3.0)

**Also supports:** melody conditioning (`generate_with_chroma`), stereo generation, audio continuation, style transfer (MusicGen-Style), EnCodec compression.

**GPU requirements:** small ~4GB FP32 / ~2GB FP16, medium ~8GB / ~4GB, large ~16GB / ~8GB.

### HeartMuLa — Open-Source Suno Alternative

Apache-2.0 music generation from lyrics + tags. Full songs with multilingual support.

**Stack:** Python 3.10, `torch==2.4.1`, `torchtune`, `transformers`

**Hardware:** 8GB VRAM minimum (with `--lazy_load true`), 16GB+ recommended. CPU possible but extremely slow.

**Basic generation:**
```bash
python ./examples/run_music_generation.py \
  --model_path=./ckpt --version="3B" \
  --lyrics="./assets/lyrics.txt" --tags="./assets/tags.txt" \
  --save_path="./assets/output.mp3" --lazy_load true
```

**Tags:** comma-separated, no spaces: `piano,happy,wedding,synthesizer,romantic`
**Lyrics:** use bracketed structural tags: `[Intro]`, `[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]`

**Key parameters:** `max_audio_length_ms` (240000 = 4min), `topk` (50), `temperature` (1.0), `cfg_scale` (1.5)

**Pitfalls:**
- Do NOT use bf16 for HeartCodec — degrades quality. Use fp32.
- Tags may be ignored (known issue); lyrics dominate.
- Triton not available on macOS; Linux/CUDA only for GPU acceleration.
- Dependency pin conflicts require manual upgrades and source patches (RoPE cache fix, HeartCodec loading fix).

**Performance:** RTF ≈ 1.0 — 4-minute song takes ~4 minutes on GPU.

---

## Songwriting

### Song Structure

Common skeletons — mix, modify, or invent:

```
ABABCB  Verse/Chorus/Verse/Chorus/Bridge/Chorus    (most pop/rock)
AABA    Verse/Verse/Bridge/Verse (refrain-based)    (jazz, ballads)
ABAB    Verse/Chorus alternating                    (simple, direct)
AAA     Verse/Verse/Verse (strophic)                (folk, storytelling)
```

Building blocks: Intro, Verse, Pre-Chorus, Chorus, Bridge, Outro. Structure serves emotion.

### Rhyme and Meter

- **Perfect:** lean/mean | **Family:** crate/braid | **Assonance:** had/glass
- **Internal rhyme:** within lines, not just at ends
- **Meter:** stressed syllables matter more than total count. Say it aloud.

### Emotional Arc

Contrast is the most powerful dynamic trick: whisper before scream, sparse before dense, slow before fast. Map energy: Intro 2-3 → Verse 5-6 → Pre-Chorus 7 → Chorus 8-9 → Bridge varies → Final Chorus 9-10.

### Show, Don't Tell

- "I was sad" = flat
- "Your hoodie's still on the hook by the door" = alive
- The hook is the line people remember — place it where it lands hardest

### Parody and Adaptation

1. Map the original: count syllables per line, mark rhyme scheme, identify stressed syllables
2. Match stressed syllables to the same beats
3. On held notes, match the VOWEL SOUND of the original
4. Monosyllabic swaps in key spots keep rhythm intact (Crime → Code, Snake → Noose)
5. Keep some original lines intact for recognizability

---

## Prompt Engineering for AI Music Platforms

### Style/Genre Description (Suno, Udio, etc.)

**Formula:** Genre + Mood + Era + Instruments + Vocal Style + Production + Dynamics

**BAD:** `"sad rock song"`
**GOOD:** `"Cinematic orchestral spy thriller, 1960s Cold War era, smoky sultry female vocalist, big band jazz, brass section with trumpets and french horns, sweeping strings, minor key, vintage analog warmth"`

**Describe the journey, not just the genre:**
```
"Begins as a haunting whisper over sparse piano. Gradually layers in muted brass.
Builds through the chorus with full orchestra. Second verse erupts with raw belting
intensity. Outro strips back to a lone piano and a fragile whisper fading to silence."
```

**Tips:**
- V4.5+ supports up to 1,000 chars in Style field — use them
- NO artist names or trademarks. Describe the sound instead.
- Build a vocal PERSONA, not just a gender: "A weathered torch singer with a smoky alto, slight rasp, who starts vulnerable and builds to devastating power"
- Unexpected combos: "bossa nova trap", "Appalachian gothic", "chiptune jazz"

### Metatags (place in [brackets] inside lyrics field)

**Structure:** `[Intro] [Verse] [Chorus] [Bridge] [Outro] [Instrumental] [Guitar Solo] [Build-up] [Silence] [End]`

**Vocal:** `[Whispered] [Spoken Word] [Belted] [Falsetto] [Powerful] [Soulful] [Raspy] [Breathy] [Harmonies] [Choir]`

**Dynamics:** `[High Energy] [Low Energy] [Building Energy] [Explosive] [Emotional Climax] [Gradual swell] [Quiet arrangement]`

**Atmosphere:** `[Melancholic] [Euphoric] [Nostalgic] [Aggressive] [Dreamy] [Intimate] [Dark Atmosphere]`

**SFX:** `[Vinyl Crackle] [Rain] [Applause] [Static] [Thunder]`

**Rules:** 5-8 tags per section max. Don't contradict yourself. Put tags in BOTH style field AND lyrics for reinforcement. Always use Custom Mode for serious work.

### Phonetic Tricks for AI Singers

- Spell words as they sound: "through" → "thru", "Nous" → "Noose"
- ALL CAPS = louder, more intense
- Vowel extension: "lo-o-o-ove" = sustained/melisma
- Ellipses: "I... need... you" = dramatic pauses
- Hyphenate to guide syllables: "Re-search", "bio-engineering"
- Spell out numbers: "24/7" → "twenty four seven"
- Space acronyms: "AI" → "A I" or "A-I"

---

## Audio Analysis

### songsee — Spectrograms and Feature Visualization

Go-based CLI tool for multi-panel audio analysis. Requires Go + optional ffmpeg.

**Install:** `go install github.com/steipete/songsee/cmd/songsee@latest`

**Usage:**
```bash
songsee track.mp3                    # Basic spectrogram
songsee track.mp3 -o spectrogram.png # Save to file
songsee track.mp3 --viz spectrogram,mel,chroma,hpss,selfsim,loudness,tempogram,mfcc,flux
songsee track.mp3 --start 12.5 --duration 8 -o slice.jpg
```

**Visualization types:** `spectrogram`, `mel`, `chroma`, `hpss` (harmonic/percussive), `selfsim` (self-similarity), `loudness`, `tempogram`, `mfcc`, `flux` (onset detection)

**Flags:** `--style` (classic/magma/inferno/viridis/gray), `--width/--height`, `--min-freq/--max-freq`, `--start/--duration`

**Use cases:** Compare audio outputs, debug synthesis, document pipelines, inspect with `vision_analyze`.

---

## Workflow

1. **Define the goal** — original song, parody, sound effect, instrumental, analysis?
2. **Choose the tool** — local generation (AudioCraft/HeartMuLa) vs platform (Suno/Udio) vs analysis (songsee)
3. **Write or generate** — For songs: craft lyrics first, then build the style description. For instrumentals: focus on the style description.
4. **Engineer the prompt** — Use the full formula: genre + mood + era + instruments + vocal style + production + dynamics. Describe the journey.
5. **Generate 3-5 variations** — Treat them like recording takes. Pick the best.
6. **Extend/iterate** — Restate genre/mood when extending to prevent style drift.
7. **Analyze** — Use songsee to inspect outputs, compare versions, debug issues.

---

## Pitfalls

- **AudioCraft:** CUDA OOM → use smaller model or reduce duration. Poor quality → increase cfg_coef.
- **HeartMuLa:** Do NOT use bf16 for HeartCodec. Dependency conflicts require manual patches.
- **Suno prompts:** All perfect rhymes can sound like nursery rhymes. All slant rhymes can sound lazy. Blend them.
- **Platform generation:** Expect ~3-5 generations per 1 good result. Revision is normal.
- **Phonetics:** AI singers don't read — they pronounce. Test proper nouns in short clips first.
- **songsee:** WAV/MP3 decoded natively; other formats need ffmpeg.
