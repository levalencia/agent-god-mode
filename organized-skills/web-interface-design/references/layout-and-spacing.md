# Layout and Spacing Reference

## Grid Fundamentals

**Modules:** Building blocks where rows and columns intersect.

**Spatial zones:** Clusters of modules grouping content with shared purpose.

**Gutters:** Spaces between columns/rows—give design breathing room.

**Margins:** Outer spacing around the grid.

---

## The Baseline Grid Misconception

**Myth:** Baseline grids automatically create harmony.

**Reality:** They only unify height dimensions. Harmony comes from:
- Contrast and variety
- Repetitive spacing patterns
- Harmonious relationships between values

### When to Use Baseline Grids

**Use for:**
- Fixed-height environments (apps)
- Print design
- Precise vertical alignment needs

**Don't force for:**
- Responsive websites
- Flexible content areas
- Variable content lengths

---

## Spacing Scales

### 4px Base Unit (Recommended)
```
4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96
```

Best for most web projects.

### 8px Base Unit
```
8, 16, 24, 32, 40, 48, 64, 80, 96
```

For larger, more spacious designs.

### CSS Implementation
```css
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
}
```

---

## Two-Scale Strategy

Complex projects mixing content and UI often need **two independent scales**:

- **Content scale (line-spacing based):** For articles, documentation
- **Module scale (unit-based):** For cards, navigation, forms

This prevents conflict between typography rhythm and component spacing.

---

## Spacing in Different Contexts

### Long-form Content
Vertical rhythm and typography spacing rules apply strictly.

### UI Modules (cards, navigation)
Contrast, grouping, composition matter more than strict rhythm.

---

## Responsive Considerations

### Pattern Adaptations

**Tabs → Accordions:** At narrow widths, horizontal tabs should become vertical accordions.

**Navigation:**
- Desktop: Horizontal with all items
- Tablet: Horizontal with overflow menu
- Mobile: Hamburger or bottom nav

**Tables:**
- Desktop: Full table
- Tablet: Priority columns, horizontal scroll
- Mobile: Card transformation

**Cards:**
- Desktop: 3-4 column grid
- Tablet: 2-column
- Mobile: Single column stack

**Forms:**
- Desktop: Multi-column for related fields
- Tablet: Two-column for short fields
- Mobile: Single column always

### Breakpoints

```css
--bp-sm: 640px;   /* Large phones */
--bp-md: 768px;   /* Tablets */
--bp-lg: 1024px;  /* Laptops */
--bp-xl: 1280px;  /* Desktops */
--bp-2xl: 1536px; /* Large desktops */
```

### Touch Considerations

**Touch targets:** 44×44px min, 48×48px recommended.

**Spacing between targets:** 8px minimum.

**Hover states:** Don't rely on hover—touch has none.

**Gestures:** Supplement with visible controls.

---

## Whitespace Principles

**Start with too much:** Easier to remove than add.

**Cramped = cheap:** Whitespace communicates quality.

**Group related elements:** Use spacing to show relationships.

---

## Good vs Bad Examples

**❌ Inconsistent spacing**
```css
.card { padding: 15px; }
.section { margin-bottom: 30px; }
.header { padding: 18px 25px; }
```

**✓ Consistent scale**
```css
.card { padding: 16px; }
.section { margin-bottom: 32px; }
.header { padding: 16px 24px; }
```
