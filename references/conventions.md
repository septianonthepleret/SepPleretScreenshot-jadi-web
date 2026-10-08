# Output conventions

## File structure (single-file default)
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Descriptive title</title>
  <style>
    :root { /* tokens */ }
    /* 1. reset  2. base  3. layout  4. components  5. utilities  6. media queries */
  </style>
</head>
<body>
  <!-- semantic landmarks: header, nav, main, section, aside, footer -->
  <script>/* only if behavior is needed */</script>
</body>
</html>
```
Use `lang="id"` if the page content is Indonesian.

## Tokens
```css
:root {
  --color-bg: #0f1115;
  --color-surface: #181b22;
  --color-text: #e8eaf0;
  --color-muted: #9aa3b2;
  --color-primary: #4f7cff;
  --radius-md: 12px;
  --space-1: .25rem; --space-2: .5rem; --space-3: 1rem; --space-4: 1.5rem; --space-5: 2.5rem;
  --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --shadow-card: 0 4px 16px rgb(0 0 0 / .18);
}
```
Snap measured spacing to a small scale (4/8/16/24/40) unless the design clearly uses something else.

## Naming
- Short, descriptive, BEM-ish: `.card`, `.card__title`, `.btn--primary`.
- Name by role, not appearance (`.btn--primary`, not `.btn--blue`).

## Responsiveness
- Mobile-first breakpoints at ~640px, 900px, 1200px, adjusted to where the layout actually breaks.
- Grids: `grid-template-columns: repeat(auto-fit, minmax(240px, 1fr))`.
- Fluid type: `font-size: clamp(1.75rem, 1.2rem + 2vw, 3rem)`.
- Images/media: `max-width: 100%; height: auto`, and `aspect-ratio` for placeholders.
- Wide tables scroll inside an `overflow-x: auto` wrapper.

## Accessibility checklist
- One `<h1>`, logical heading order.
- Buttons are `<button>`, links are `<a href>`.
- Form inputs have `<label>`; icon-only buttons have `aria-label`.
- Visible `:focus-visible` outline.
- Text contrast >= 4.5:1 (flag if the source design fails this, but keep fidelity).
- Interactive widgets: tabs (`role="tablist"`, `aria-selected`), accordions (`aria-expanded`), modals (focus trap, Esc to close).
- `@media (prefers-reduced-motion: reduce)` disables non-essential animation.

## Animation guidelines (from video)
- Animate only `transform` and `opacity` where possible.
- Typical durations: hover 120-200ms, small UI 200-300ms, panels/modals 250-400ms; use `ease-out` for entrances and `ease-in` for exits.
- Express timings as CSS variables so the user can tune them.
