---
name: screenshot-to-html
description: Convert a screenshot, mockup, design export, or screen-recording video of a UI into clean, responsive HTML/CSS (optionally with vanilla JS or Tailwind) ready to implement as a web interface. Use this skill whenever the user uploads an image or video of a website, app screen, landing page, dashboard, or component and wants it recreated as code, says things like "turn this screenshot into HTML", "clone this UI", "implement this design", "ubah screenshot/video ini jadi kode", or wants a UI video's animations and interactions reproduced in a web page — even if they never say the word "skill".
---

# Screenshot / Video to HTML

Turn a visual reference (image or video) into production-quality HTML/CSS that matches the layout, spacing, colors, typography, and, for video, the motion and interactions.

## Workflow

### 1. Identify the input
- **Image** (png/jpg/webp): look at it directly. It is already in context if uploaded; otherwise `view` it from `/mnt/user-data/uploads`.
- **Video** (mp4/mov/webm/gif): run `scripts/extract_frames.py` first (see "Video input"). Never guess a video's content from the filename.

### 2. Decide output defaults (don't over-ask)
Ask at most one question, only if it changes the result a lot. Otherwise assume:
- Single self-contained `index.html` with inline `<style>` and (if needed) inline `<script>`.
- Plain CSS with custom properties. Use Tailwind only if the user asks for it or the screenshot is clearly a Tailwind-style site and they mention Tailwind.
- Responsive: desktop layout matching the screenshot, plus sensible tablet/mobile breakpoints.
- Semantic HTML, accessible by default.
If the user names a framework (React, Vue, Svelte), write it for that instead and say what you assumed.

### 3. Analyze before coding
Write a short internal inventory, then build from it:
1. **Layout skeleton**: header, sidebar, main, grid/flex structure, column counts, approximate widths in px or %.
2. **Design tokens**: colors (run `scripts/color_palette.py <image>` to get real hex values instead of eyeballing), font families/weights/sizes, spacing scale, border radius, shadows.
3. **Components**: buttons, cards, inputs, nav, tables, badges. Note repeated patterns and make them reusable classes.
4. **States** (video or multi-screenshot): hover, active, open/closed, tabs, modals, scroll effects.
5. **Assets**: icons, logos, photos. See "Assets".

### 4. Build
Follow `references/conventions.md` for CSS structure, naming, responsiveness, and accessibility. Key rules:
- Define tokens in `:root` first, then use them everywhere.
- Prefer flexbox/grid over absolute positioning. Use absolute positioning only for genuinely overlaid elements.
- Match proportions, not just pixels: use `rem`, `%`, `clamp()`, `minmax()`.
- Real text in real elements. Never put text inside an image.
- Don't invent features that aren't visible. Keep placeholder content faithful to the screenshot.

### 5. Verify visually
Render the page and compare it with the source:
```bash
python3 scripts/render_preview.py /mnt/user-data/outputs/index.html /home/claude/preview.png --width 1440
```
`view` the preview next to the original, list the differences (spacing, color, font size, alignment), fix them, and re-render. Do one or two correction rounds, not endless polishing.

### 6. Deliver
Save to `/mnt/user-data/outputs/` and share with `present_files`. In the reply, briefly state: assumptions made, what was approximated (fonts, icons, images), and how to swap in real assets. Keep it short.

## Video input

```bash
python3 scripts/extract_frames.py /mnt/user-data/uploads/demo.mp4 --out /home/claude/frames
```
This writes:
- `frames/frame_XXX.png`: key frames chosen by scene change, plus evenly spaced fallback frames (default max 12).
- `frames/contact_sheet.png`: all frames in one grid with timestamps, for a fast overview.
- `frames/frames.json`: timestamps and basic info (duration, resolution, fps).

Then:
1. `view` the contact sheet to understand the flow, then `view` individual frames that matter (the first frame is usually the base layout).
2. Build the **static layout from the clearest frame** first.
3. Translate what changes between frames into behavior:
   - Element appears/disappears -> toggle a class with JS, animate with CSS `transition`.
   - Fade/slide/scale on load or scroll -> CSS `@keyframes` or `IntersectionObserver`.
   - Tab, accordion, dropdown, modal, carousel -> small vanilla JS, with correct ARIA attributes.
   - Hover/press states -> `:hover`, `:active`, `:focus-visible`.
4. Estimate durations and easing from timestamps (frame gaps), and say they're estimates.
5. Respect `prefers-reduced-motion`.

Options: `--max-frames N`, `--every SECONDS` (force uniform sampling), `--start/--end` (limit range), `--scene-threshold 0.2` (lower = more sensitive). For long videos, extract a coarse pass first and then re-run on a narrow range.

## Assets
- **Icons**: reproduce as inline SVG (simple shapes) or use a well-known icon set via cdnjs only if the user is fine with an external dependency. Never leave broken `<img>` tags.
- **Photos/illustrations**: use a CSS gradient or neutral placeholder block with the same aspect ratio (`aspect-ratio`) and an informative `alt`. Tell the user which images need replacing.
- **Fonts**: identify the closest match. Use a system-font stack fallback; mention Google Fonts as an optional upgrade rather than assuming network access.
- **Logos / brand marks**: don't redraw trademarked logos. Use a text or neutral placeholder and flag it.

## Fidelity vs. quality
Fidelity to the screenshot is the goal, but the code must still be clean, responsive, and accessible. If the screenshot has something that cannot be reproduced exactly (custom font, proprietary icon, photo), approximate it and say so rather than hacking around it.

## Edge cases
- **Low-resolution or blurry image**: say which values (exact colors, small text) are guesses.
- **Screenshot contains sensitive data** (names, emails, tokens): replace with placeholder text in the code.
- **Multiple screenshots**: treat each as a page or state. Share the CSS, and use one file per page or a simple tab/route switch if the user wants a single file.
- **Mobile screenshot only**: build mobile-first, then add a reasonable desktop layout and say it was inferred.
- **Dark/light**: reproduce the theme shown; add the opposite theme only if asked.
