# Swarm Pepes — “1%”

Output: **[artifacts/video.mp4](artifacts/video.mp4)** (`video/mp4`).

A 20-second portrait pixel-art spot: three common pulls, a dramatic fourth pull with gold skin and crown, then a golden crowned Pepe and the collection URL. Original procedural artwork, bitmap typography, and original synthesized chiptune score. No stock media or external brand assets.

## Media

- 1080 × 1920, 9:16, 30 fps, 600 frames, 20.000 seconds.
- H.264 / AVC, yuv420p, MP4 with front-loaded moov atom for browser playback.
- AAC audio, 44.1 kHz, mono, 192 kb/s encoder target. Pulse-wave arpeggios, synthesized bass, noise percussion, reel effects, accelerating final spin, and a reveal impact. Short ending fade.
- 270 × 480 native pixel canvas enlarged 4× using nearest-neighbor scaling; CRT scanlines.
- Measured encoding metadata: `validation/probe.json`.

## Timeline

| Time | Action |
| --- | --- |
| 0–3 s | Flashing “CAN YOU HIT THE 1%?” and lever pull |
| 3–11 s | Three fast common spins; green Pepes with plain hats pop out with COMMON tags |
| 11–16 s | Fourth spin decelerates, machine shakes; GOLD lands at 14.15 s, CROWN at 14.85 s; gold flashes and confetti |
| 16–20 s | Large glowing golden crowned Pepe; “GOLD SKIN: 1%.” and “CROWN: 3%.”; SWARMPEPE.XYZ appears at 18 s |

## Reproduce offline

Run `python3 src/render.py` using CPython 3.12 on Linux x86-64. No package installation or network is required. The renderer extracts `vendor/render-runtime.tar.xz` into `test/scratch/`, generates audio there, and renders the delivered MP4. Scratch files are disposable. The compact archive contains a purpose-built FFmpeg/FFprobe with libx264 and the required Pillow core and shared libraries. The host supplies Python 3.12, glibc and zlib. Dependency versions, build options, upstream source URLs and licenses are described in `vendor/README.md`. All runtime dependencies beyond those host components are bundled as ordinary files, not submodules. The render source is `src/render.py`.

The original broad FFmpeg distribution and unused Pillow extensions were replaced with this compact offline runtime to meet the 8 MiB source upload limit. The artwork, timeline, typography and score remain unchanged.

## Checks and limitations

Final file size: 2,090,714 bytes (1.99 MiB). Decoded audio measures −19.1 dB mean and −1.2 dB peak. Full stream decoding completed without errors; MP4 atom inspection confirms moov precedes mdat. Detailed checks and SHA-256 are recorded in `validation/checks.txt`.

FFprobe verifies duration, dimensions, H.264/yuv420p video, AAC audio, and frame rate. Local inspection uses a nine-frame contact sheet plus frames decoded from the actual MP4; full decoding checks stream integrity. Checks establish technical properties, not independent artistic approval.

Artwork is an original pixel interpretation of Pepe, not a copy of a verified collection token. Trait rarity percentages, collection name, domain, and Ethereum contract `0x999ce0ce8c5f7661e0c74a568ffe27ceb9177bdb` are supplied by the brief; no live contract or rarity verification was performed. The slot machine is a promotional visual metaphor. No voiceover. The source reproduction bundle targets Linux x86-64 / CPython 3.12; the delivered MP4 is the portable final asset.
