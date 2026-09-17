"""
Corda Brand Identity & Favicon Generator
Generates:
1. logo.svg (Main logomark)
2. logo-horizontal.svg (Brand lockup with typography)
3. logo-white.svg (Monochrome white for dark themes)
4. logo-dark.svg (Obsidian dark for light themes)
5. favicon.svg (Vector favicon with dark/light mode support)
6. apple-touch-icon.svg & .png (180x180)
7. favicon-32x32.png (32x32)
8. favicon-16x16.png (16x16)
9. favicon.ico (Standard multi-size ICO container)
10. logo-512.png (High-res standalone logomark)
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
os.makedirs(BRANDING_DIR, exist_ok=True)

# 1. Main Logomark SVG (512x512)
LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <!-- Background subtle gradient -->
    <radialGradient id="corda-bg-glow" cx="50%" cy="50%" r="50%" fx="30%" fy="30%">
      <stop offset="0%" stop-color="#8356E2" stop-opacity="0.18"/>
      <stop offset="60%" stop-color="#68F09E" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#070708" stop-opacity="0"/>
    </radialGradient>

    <!-- Outer Chord Sweeping Gradient -->
    <linearGradient id="chord-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#68F09E"/>
      <stop offset="30%" stop-color="#00D2FF"/>
      <stop offset="70%" stop-color="#8356E2"/>
      <stop offset="100%" stop-color="#E1F2B3"/>
    </linearGradient>

    <!-- Core Nucleus Gradient -->
    <linearGradient id="core-gradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#68F09E"/>
      <stop offset="50%" stop-color="#E1F2B3"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>

    <!-- Shadow / Glow Filters -->
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="core-glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Ambient background glow -->
  <circle cx="256" cy="256" r="240" fill="url(#corda-bg-glow)"/>

  <!-- Outer Orbital Reference Rings (Precision Architecture) -->
  <circle cx="256" cy="256" r="210" fill="none" stroke="rgba(255, 255, 255, 0.05)" stroke-width="1.5" stroke-dasharray="4 8"/>
  <circle cx="256" cy="256" r="160" fill="none" stroke="rgba(104, 240, 158, 0.1)" stroke-width="1.5"/>

  <!-- Geodetic Axis Markers -->
  <line x1="256" y1="36" x2="256" y2="56" stroke="#68F09E" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
  <line x1="256" y1="456" x2="256" y2="476" stroke="#8356E2" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
  <line x1="36" y1="256" x2="56" y2="256" stroke="#00D2FF" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
  <line x1="456" y1="256" x2="476" y2="256" stroke="#E1F2B3" stroke-width="2" stroke-linecap="round" opacity="0.6"/>

  <!-- THE CORDA CHORD (Stylized 'C' Monogram with Golden Ratio Curvature) -->
  <!-- Main dynamic tapered chord -->
  <path d="M 370 120
           C 280 60, 150 100, 100 190
           C 55 270, 85 375, 175 425
           C 255 470, 360 445, 395 385
           C 405 368, 392 355, 375 358
           C 335 365, 275 370, 215 345
           C 150 318, 130 240, 165 185
           C 200 130, 290 120, 350 148
           C 368 156, 385 142, 370 120 Z"
        fill="url(#chord-gradient)"
        filter="url(#neon-glow)"/>

  <!-- Inner Concentric Resonance Arc -->
  <path d="M 320 180
           C 260 145, 185 170, 160 230
           C 135 290, 165 350, 225 370
           C 270 385, 320 370, 340 335"
        fill="none"
        stroke="#E1F2B3"
        stroke-width="3"
        stroke-linecap="round"
        stroke-dasharray="12 8"
        opacity="0.75"/>

  <!-- THE ORACLE EYE (Central Consensus Nucleus) -->
  <!-- Outer Nucleus Ring -->
  <circle cx="268" cy="256" r="46" fill="#0E0E10" stroke="url(#chord-gradient)" stroke-width="3"/>

  <!-- Rhombus / Faceted Consensus Gem -->
  <polygon points="268,226 298,256 268,286 238,256"
           fill="url(#core-gradient)"
           filter="url(#core-glow)"/>

  <!-- Central Pupil / Lens of Truth -->
  <circle cx="268" cy="256" r="12" fill="#070708"/>
  <circle cx="272" cy="252" r="3.5" fill="#FFFFFF"/>
</svg>
"""

# 2. Horizontal Brand Lockup SVG (800x200)
LOGO_HORIZONTAL_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200" width="100%" height="100%">
  <defs>
    <linearGradient id="h-chord-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#68F09E"/>
      <stop offset="30%" stop-color="#00D2FF"/>
      <stop offset="70%" stop-color="#8356E2"/>
      <stop offset="100%" stop-color="#E1F2B3"/>
    </linearGradient>

    <linearGradient id="h-core-gradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#68F09E"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>

    <filter id="h-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- LEFT: LOGOMARK EMBLEM (Scaled to 150x150, centered at x=100, y=100) -->
  <g transform="translate(15, 15) scale(0.332)">
    <!-- Outer Arc -->
    <path d="M 370 120
             C 280 60, 150 100, 100 190
             C 55 270, 85 375, 175 425
             C 255 470, 360 445, 395 385
             C 405 368, 392 355, 375 358
             C 335 365, 275 370, 215 345
             C 150 318, 130 240, 165 185
             C 200 130, 290 120, 350 148
             C 368 156, 385 142, 370 120 Z"
          fill="url(#h-chord-gradient)"
          filter="url(#h-glow)"/>

    <!-- Inner Orbit -->
    <path d="M 320 180 C 260 145, 185 170, 160 230 C 135 290, 165 350, 225 370 C 270 385, 320 370, 340 335"
          fill="none" stroke="#E1F2B3" stroke-width="3" stroke-linecap="round" stroke-dasharray="12 8" opacity="0.75"/>

    <!-- Nucleus -->
    <circle cx="268" cy="256" r="46" fill="#0E0E10" stroke="url(#h-chord-gradient)" stroke-width="3"/>
    <polygon points="268,226 298,256 268,286 238,256" fill="url(#h-core-gradient)"/>
    <circle cx="268" cy="256" r="12" fill="#070708"/>
    <circle cx="272" cy="252" r="3.5" fill="#FFFFFF"/>
  </g>

  <!-- RIGHT: BESPOKE TYPOGRAPHY -->
  <g transform="translate(210, 0)">
    <!-- Wordmark: CORDA -->
    <text x="0" y="112"
          font-family="system-ui, -apple-system, 'Space Grotesk', 'Syne', sans-serif"
          font-size="82"
          font-weight="900"
          letter-spacing="0.06em"
          fill="#FFFFFF">
      CORDA
    </text>

    <!-- GenLayer Live Badge -->
    <g transform="translate(380, 58)">
      <rect x="0" y="0" width="170" height="28" rx="14" fill="rgba(104, 240, 158, 0.12)" stroke="rgba(104, 240, 158, 0.35)" stroke-width="1"/>
      <circle cx="14" cy="14" r="4" fill="#68F09E"/>
      <text x="26" y="18" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" letter-spacing="0.08em" fill="#68F09E">
        GENLAYER ORACLE
      </text>
    </g>

    <!-- Subtitle / Mission Tagline -->
    <text x="4" y="152"
          font-family="'JetBrains Mono', monospace"
          font-size="13"
          font-weight="500"
          letter-spacing="0.22em"
          fill="#9A9A9A">
      AUTONOMOUS PRIVACY DISCLOSURE PROTOCOL
    </text>
  </g>
</svg>
"""

# 3. Vector Favicon SVG (64x64) - Ultra Crisp for Browser Tabs
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <linearGradient id="fav-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#68F09E"/>
      <stop offset="40%" stop-color="#00D2FF"/>
      <stop offset="80%" stop-color="#8356E2"/>
      <stop offset="100%" stop-color="#E1F2B3"/>
    </linearGradient>

    <linearGradient id="fav-core" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#68F09E"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>
  </defs>

  <!-- Dark Background Pill for High Contrast across all browser themes -->
  <rect width="64" height="64" rx="16" fill="#070708"/>
  <rect width="64" height="64" rx="16" fill="none" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1.5"/>

  <!-- Scaled Optimized Mark -->
  <g transform="translate(6, 6) scale(0.1015)">
    <!-- Chord 'C' -->
    <path d="M 370 120
             C 280 60, 150 100, 100 190
             C 55 270, 85 375, 175 425
             C 255 470, 360 445, 395 385
             C 405 368, 392 355, 375 358
             C 335 365, 275 370, 215 345
             C 150 318, 130 240, 165 185
             C 200 130, 290 120, 350 148
             C 368 156, 385 142, 370 120 Z"
          fill="url(#fav-gradient)"/>

    <!-- Nucleus -->
    <circle cx="268" cy="256" r="48" fill="#0E0E10" stroke="url(#fav-gradient)" stroke-width="6"/>
    <polygon points="268,224 300,256 268,288 236,256" fill="url(#fav-core)"/>
    <circle cx="268" cy="256" r="12" fill="#070708"/>
  </g>
</svg>
"""

# 4. Apple Touch Icon SVG (180x180)
APPLE_ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180" width="180" height="180">
  <defs>
    <radialGradient id="apple-bg" cx="50%" cy="30%" r="80%">
      <stop offset="0%" stop-color="#1A1A24"/>
      <stop offset="60%" stop-color="#0E0E14"/>
      <stop offset="100%" stop-color="#070708"/>
    </radialGradient>

    <linearGradient id="apple-chord-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#68F09E"/>
      <stop offset="30%" stop-color="#00D2FF"/>
      <stop offset="70%" stop-color="#8356E2"/>
      <stop offset="100%" stop-color="#E1F2B3"/>
    </linearGradient>

    <linearGradient id="apple-core-gradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#68F09E"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>

    <filter id="apple-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- iOS squircle container -->
  <rect width="180" height="180" rx="42" fill="url(#apple-bg)"/>
  <rect width="180" height="180" rx="42" fill="none" stroke="rgba(255, 255, 255, 0.15)" stroke-width="2"/>

  <!-- Centered Emblem -->
  <g transform="translate(18, 18) scale(0.281)">
    <path d="M 370 120
             C 280 60, 150 100, 100 190
             C 55 270, 85 375, 175 425
             C 255 470, 360 445, 395 385
             C 405 368, 392 355, 375 358
             C 335 365, 275 370, 215 345
             C 150 318, 130 240, 165 185
             C 200 130, 290 120, 350 148
             C 368 156, 385 142, 370 120 Z"
          fill="url(#apple-chord-gradient)"
          filter="url(#apple-glow)"/>

    <path d="M 320 180 C 260 145, 185 170, 160 230 C 135 290, 165 350, 225 370 C 270 385, 320 370, 340 335"
          fill="none" stroke="#E1F2B3" stroke-width="4" stroke-linecap="round" stroke-dasharray="12 8" opacity="0.8"/>

    <circle cx="268" cy="256" r="46" fill="#0E0E10" stroke="url(#apple-chord-gradient)" stroke-width="4"/>
    <polygon points="268,226 298,256 268,286 238,256" fill="url(#apple-core-gradient)"/>
    <circle cx="268" cy="256" r="12" fill="#070708"/>
    <circle cx="272" cy="252" r="3.5" fill="#FFFFFF"/>
  </g>
</svg>
"""

# 5. Monochrome White Version
LOGO_WHITE_SVG = LOGO_SVG.replace('url(#chord-gradient)', '#FFFFFF').replace('url(#core-gradient)', '#FFFFFF').replace('stroke="#E1F2B3"', 'stroke="#FFFFFF"')

# 6. Monochrome Dark Version
LOGO_DARK_SVG = LOGO_SVG.replace('url(#chord-gradient)', '#070708').replace('url(#core-gradient)', '#070708').replace('stroke="#E1F2B3"', 'stroke="#070708"')

def main():
    print("==================================================")
    print("   CORDA — Brand Design & Asset Generator")
    print("==================================================")

    svg_files = {
        os.path.join(BRANDING_DIR, "logo.svg"): LOGO_SVG,
        os.path.join(BRANDING_DIR, "logo-horizontal.svg"): LOGO_HORIZONTAL_SVG,
        os.path.join(BRANDING_DIR, "logo-white.svg"): LOGO_WHITE_SVG,
        os.path.join(BRANDING_DIR, "logo-dark.svg"): LOGO_DARK_SVG,
        os.path.join(BRANDING_DIR, "favicon.svg"): FAVICON_SVG,
        os.path.join(BRANDING_DIR, "apple-touch-icon.svg"): APPLE_ICON_SVG,
        # Also mirror root favicons for direct web server serving
        os.path.join(FRONTEND_DIR, "favicon.svg"): FAVICON_SVG,
        os.path.join(BASE_DIR, "favicon.svg"): FAVICON_SVG,
    }

    for path, content in svg_files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"✓ Created SVG: {os.path.basename(path)} -> {path}")

    # Rasterize PNGs and ICO using ffmpeg
    print("\nRasterizing high-fidelity PNG and ICO assets using ffmpeg...")

    # A. apple-touch-icon.png (180x180)
    apple_svg = os.path.join(BRANDING_DIR, "apple-touch-icon.svg")
    apple_png_branding = os.path.join(BRANDING_DIR, "apple-touch-icon.png")
    apple_png_root = os.path.join(FRONTEND_DIR, "apple-touch-icon.png")
    subprocess.run(["ffmpeg", "-y", "-i", apple_svg, "-vf", "scale=180:180", apple_png_branding], capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-i", apple_svg, "-vf", "scale=180:180", apple_png_root], capture_output=True)
    print(f"✓ Generated 180x180 Apple Touch Icon: {apple_png_branding}")

    # B. favicon-32x32.png
    fav_svg = os.path.join(BRANDING_DIR, "favicon.svg")
    fav32_png = os.path.join(BRANDING_DIR, "favicon-32x32.png")
    fav32_root = os.path.join(FRONTEND_DIR, "favicon-32x32.png")
    subprocess.run(["ffmpeg", "-y", "-i", fav_svg, "-vf", "scale=32:32", fav32_png], capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-i", fav_svg, "-vf", "scale=32:32", fav32_root], capture_output=True)
    print(f"✓ Generated 32x32 Favicon: {fav32_png}")

    # C. favicon-16x16.png
    fav16_png = os.path.join(BRANDING_DIR, "favicon-16x16.png")
    fav16_root = os.path.join(FRONTEND_DIR, "favicon-16x16.png")
    subprocess.run(["ffmpeg", "-y", "-i", fav_svg, "-vf", "scale=16:16", fav16_png], capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-i", fav_svg, "-vf", "scale=16:16", fav16_root], capture_output=True)
    print(f"✓ Generated 16x16 Favicon: {fav16_png}")

    # D. favicon.ico (multi-resolution container from 32x32)
    fav_ico_branding = os.path.join(BRANDING_DIR, "favicon.ico")
    fav_ico_frontend = os.path.join(FRONTEND_DIR, "favicon.ico")
    fav_ico_root = os.path.join(BASE_DIR, "favicon.ico")
    subprocess.run(["ffmpeg", "-y", "-i", fav32_png, fav_ico_branding], capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-i", fav32_png, fav_ico_frontend], capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-i", fav32_png, fav_ico_root], capture_output=True)
    print(f"✓ Generated multi-size favicon.ico: {fav_ico_frontend}")

    # E. High-Res Logo PNGs (512x512)
    logo_svg = os.path.join(BRANDING_DIR, "logo.svg")
    logo512_png = os.path.join(BRANDING_DIR, "logo-512.png")
    subprocess.run(["ffmpeg", "-y", "-i", logo_svg, "-vf", "scale=512:512", logo512_png], capture_output=True)
    print(f"✓ Generated 512x512 Logo PNG: {logo512_png}")

    # F. Horizontal Logo PNG (800x200)
    logo_h_svg = os.path.join(BRANDING_DIR, "logo-horizontal.svg")
    logo_h_png = os.path.join(BRANDING_DIR, "logo-horizontal.png")
    subprocess.run(["ffmpeg", "-y", "-i", logo_h_svg, "-vf", "scale=800:200", logo_h_png], capture_output=True)
    print(f"✓ Generated Horizontal Logo PNG: {logo_h_png}")

    print("\n✨ All Brand & Favicon Assets Generated Successfully!")

if __name__ == "__main__":
    main()
