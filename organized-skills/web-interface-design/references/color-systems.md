# Color Systems Reference

## Base Colors to Select

### Essential Palette
- **Primary/Brand:** Main accent for buttons, links, labels
- **Black and White:** Foundation for text and backgrounds
- **Night and Smoke:** Dark theme alternatives (night = dark bg, smoke = light text)
- **State colors:** Informative (blue), Negative (red), Positive (green), Notice (yellow/orange)

### Extended Palette
- Secondary/tertiary accents
- Product-specific category colors
- Gradient colors
- Chart colors (distinct warm and cool scales)
- Illustration colors

---

## Dark Mode Design

**Background:** Don't use pure black. Use "night" (#121212) for softer appearance.

**Text:** Pure white is too bright—creates glowing halo. Use "smoke" (#E0E0E0) for body text.

**Key insight:** High contrast white-on-black is harder to read than reduced contrast.

### Dark Mode Adjustments
- Reduce color saturation
- Increase shadow opacity
- Use surface color elevation instead of shadows alone

---

## Mirrored Tints and Shades

Create matching light and dark theme colors:

```
Light theme: a1, a2, a3, a4, a5, a6, a7, a8, a9
Dark theme:  b1, b2, b3, b4, b5, b6, b7, b8, b9
```

**Usage:** If `a4` for background in light theme, use `b4` for same background in dark theme.

This enables automatic theme switching.

---

## Creating Tints and Shades

### The Color Builder Method

**Tints:** Base color with transparency over white background
**Shades:** Base color with transparency over dark background

```
Base blue: #2563EB

Tint: rgba(37, 99, 235, 0.1) on white → light blue
Shade: rgba(37, 99, 235, 0.3) on dark → deep blue
```

### Fine-tuning
- Increase saturation for muted tints (especially greens)
- Shift hue toward red for yellow/orange shades (avoid muddiness)

---

## Transparency Layer

Create transparent scales for white, black, night, smoke:

```
black-a5:  5% opacity
black-a10: 10% opacity
black-a20: 20% opacity
...
black-a90: 90% opacity
```

Plus specialized: 2%, 7% for subtle effects.

---

## Quantity Guidelines

- **Recommended:** 17 values per color (comprehensive)
- **Minimum:** 3 values (base + one tint + one shade)

More values = flexibility for complex interfaces.

---

## Testing Colors

Validate all tints/shades on actual UI:
- Check contrast ratios
- Verify visual balance across backgrounds
- Test in both light and dark themes
- Use accessibility checkers

---

## CSS Implementation

```css
:root {
  /* Light theme */
  --primary: #2563eb;
  --primary-light: #eff6ff;
  --primary-dark: #1d4ed8;

  /* State colors */
  --success: #16a34a;
  --success-bg: #f0fdf4;
  --error: #dc2626;
  --error-bg: #fef2f2;
  --warning: #d97706;
  --warning-bg: #fffbeb;
  --info: #0284c7;
  --info-bg: #f0f9ff;

  /* Neutrals */
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --text-tertiary: #9ca3af;
  --border: #e5e7eb;
  --bg-page: #ffffff;
  --bg-surface: #f9fafb;
  --bg-hover: #f3f4f6;
}

/* Dark theme */
[data-theme="dark"] {
  --bg-page: #121212;      /* Night */
  --bg-surface: #1e1e1e;
  --bg-hover: #2a2a2a;
  --border: #333333;

  --text-primary: #e0e0e0;  /* Smoke */
  --text-secondary: #a0a0a0;
  --text-tertiary: #707070;

  --primary: #60a5fa;
  --primary-light: rgba(96, 165, 250, 0.15);
  --primary-dark: #3b82f6;
}
```

---

## Good vs Bad Examples

**❌ Pure white on pure black**
```css
.dark-theme {
  background: #000000;
  color: #FFFFFF;
}
```

**✓ Muted dark theme**
```css
.dark-theme {
  background: #121212;
  color: #E0E0E0;
}
```
