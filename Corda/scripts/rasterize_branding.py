"""
Rasterize SVGs to PNG and ICO using Edge headless and ffmpeg
"""

import os
import sys
import subprocess

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
BRANDING_DIR = os.path.join(FRONTEND_DIR, "assets", "branding")
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def render_edge(svg_path, png_path, width, height):
    url = f"file:///{os.path.abspath(svg_path).replace(os.sep, '/')}"
    cmd = [
        EDGE_EXE,
        "--headless",
        "--hide-scrollbars",
        f"--screenshot={png_path}",
        f"--window-size={width},{height}",
        url
    ]
    subprocess.run(cmd, capture_output=True)
    if os.path.exists(png_path):
        print(f"✓ Rendered {os.path.basename(png_path)} ({width}x{height}, {os.path.getsize(png_path)} bytes)")
    else:
        print(f"❌ Failed to render {png_path}")

def main():
    print("==================================================")
    print("   CORDA — Edge Headless & FFmpeg Rasterizer")
    print("==================================================")

    # 1. High-Res Logo PNG (512x512)
    render_edge(
        os.path.join(BRANDING_DIR, "logo.svg"),
        os.path.join(BRANDING_DIR, "logo-512.png"),
        512, 512
    )

    # 2. Horizontal Logo PNG (800x200)
    render_edge(
        os.path.join(BRANDING_DIR, "logo-horizontal.svg"),
        os.path.join(BRANDING_DIR, "logo-horizontal.png"),
        800, 200
    )

    # 3. Apple Touch Icon PNG (180x180)
    apple_png_branding = os.path.join(BRANDING_DIR, "apple-touch-icon.png")
    render_edge(
        os.path.join(BRANDING_DIR, "apple-touch-icon.svg"),
        apple_png_branding,
        180, 180
    )
    # Copy to frontend root
    import shutil
    apple_png_root = os.path.join(FRONTEND_DIR, "apple-touch-icon.png")
    shutil.copyfile(apple_png_branding, apple_png_root)
    print(f"✓ Copied apple-touch-icon.png to {apple_png_root}")

    # 4. Favicon 64x64
    fav64_png = os.path.join(BRANDING_DIR, "favicon-64x64.png")
    render_edge(
        os.path.join(BRANDING_DIR, "favicon.svg"),
        fav64_png,
        64, 64
    )

    # 5. Downscale to 32x32 and 16x16 via ffmpeg from 64x64
    fav32_png = os.path.join(BRANDING_DIR, "favicon-32x32.png")
    fav32_root = os.path.join(FRONTEND_DIR, "favicon-32x32.png")
    subprocess.run(["ffmpeg", "-y", "-i", fav64_png, "-vf", "scale=32:32", fav32_png], capture_output=True)
    shutil.copyfile(fav32_png, fav32_root)
    print(f"✓ Generated 32x32 Favicon: {fav32_root}")

    fav16_png = os.path.join(BRANDING_DIR, "favicon-16x16.png")
    fav16_root = os.path.join(FRONTEND_DIR, "favicon-16x16.png")
    subprocess.run(["ffmpeg", "-y", "-i", fav64_png, "-vf", "scale=16:16", fav16_png], capture_output=True)
    shutil.copyfile(fav16_png, fav16_root)
    print(f"✓ Generated 16x16 Favicon: {fav16_root}")

    # 6. Generate favicon.ico (multi-resolution ICO)
    fav_ico_branding = os.path.join(BRANDING_DIR, "favicon.ico")
    fav_ico_frontend = os.path.join(FRONTEND_DIR, "favicon.ico")
    fav_ico_root = os.path.join(BASE_DIR, "favicon.ico")
    subprocess.run(["ffmpeg", "-y", "-i", fav32_png, fav_ico_branding], capture_output=True)
    shutil.copyfile(fav_ico_branding, fav_ico_frontend)
    shutil.copyfile(fav_ico_branding, fav_ico_root)
    print(f"✓ Generated multi-size favicon.ico: {fav_ico_frontend}")

    print("\n✨ Rasterization Complete!")

if __name__ == "__main__":
    main()
