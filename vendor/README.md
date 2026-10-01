# Compact offline rendering runtime

`render-runtime.tar.xz` contains Linux x86-64 FFmpeg/FFprobe, a static
libx264 codec linked into those executables, and Pillow 12.3.0 for CPython 3.12.
It is extracted to disposable `test/scratch/runtime` by the renderer.
Pillow's core imaging extension and its transitive libraries are retained;
unused optional image extensions and their libraries are omitted. Pillow's
license metadata is inside the archive. No runtime downloads are performed.
The host supplies CPython 3.12, glibc, libm, pthread and zlib.

FFmpeg 7.0.2 source: https://ffmpeg.org/releases/ffmpeg-7.0.2.tar.xz
SHA-256: 8646515b638a3ad303e23af6a3587734447cb8fc0a0c064ecdb8e95c4fd8b389

x264 stable source: https://code.videolan.org/videolan/x264/-/archive/stable/x264-stable.tar.gz
Downloaded source SHA-256: 1108b94cd4c6943bc569afff1f8ec8c6034594a80d2baebc2b043bb438847485
Version: 0.165.x. The stable URL can change; the hash identifies this build.

x264 configure flags: `--enable-static --disable-cli --disable-asm`, with a
local install prefix. FFmpeg is configured with that prefix's pkg-config path:

```
--disable-everything --disable-autodetect --disable-doc --disable-debug
--disable-network --disable-x86asm --enable-gpl --enable-libx264
--enable-ffmpeg --enable-ffprobe --enable-protocol=file,pipe
--enable-demuxer=rawvideo,wav,mov --enable-muxer=mp4,null
--enable-decoder=rawvideo,pcm_s16le,h264,aac
--enable-encoder=libx264,aac,wrapped_avframe --enable-parser=h264,aac
--enable-filter=scale,format,aresample,anull,null
--enable-swscale --enable-swresample
```

Both are built with GCC and make. GPLv2 license texts accompany this archive.
This purpose-limited build supports rendering and decoding the delivered video;
it is not a general-purpose FFmpeg distribution.
