# Visual Hierarchy Reference

## The Core Principle

**Design exists to separate the primary from the secondary.**

Users should instantly recognize what matters. When everything competes for attention, nothing matters.

---

## Primary vs Secondary Elements

**Typical primary elements:**
- Headings
- Buttons
- Links
- Images
- Navigation
- Controls

**Secondary elements:**
- Body text
- Hints and help text
- Metadata
- Decorative elements

**Exception:** Content-oriented sites (news, docs) reverse this—body text becomes primary.

---

## Five Techniques for Creating Focus

| Technique | How It Works |
|-----------|--------------|
| **Shape** | Distinctive forms attract attention (icons draw eye) |
| **Color** | Bright/contrasting colors indicate importance |
| **Size** | Larger elements signal importance |
| **Weight** | Bolder weight creates attention chain |
| **Combination** | Multiple techniques reinforce focus |

**Warning:** Using all techniques on everything negates their power. Reserve strong emphasis for truly important elements.

---

## Three Levers of Hierarchy (Beyond Size)

### 1. Font Weight
Instead of making primary too large and secondary too small:
- Primary: 600-700 weight
- Secondary: 400-500 weight
- Avoid below 400 (accessibility)

```css
.primary-text { font-weight: 600; color: #111; }
.secondary-text { font-weight: 400; color: #555; }
.tertiary-text { font-weight: 400; color: #888; }
```

### 2. Color Proximity
De-emphasize by moving toward background color:
- Dark gray (#333) for primary
- Medium gray (#666) for secondary
- Light gray (#999) for tertiary

### 3. Contrast × Surface Area
Balance inversely:
- Large elements: lower contrast OK
- Small elements: need higher contrast
- Small + low contrast = invisible
- Large + high contrast = overwhelming

---

## Semantic Color Usage

**Limit accent colors to meaningful contexts:**
- Blue: links and interactive elements
- Red: errors and destructive actions
- Green: success states
- Yellow/Orange: warnings

**Don't use accent colors for decoration.** Every colored element should mean something.

---

## The Action Pyramid

Every page has:
1. **One primary action** — The main thing
2. **Few secondary actions** — Important but not critical
3. **Several tertiary actions** — Rarely needed

| Level | Treatment |
|-------|-----------|
| Primary | Solid fill, high contrast, largest |
| Secondary | Outline or subtle fill |
| Tertiary | Text-only or ghost |

**Common mistake:** Making destructive actions look primary. Unless destruction IS the purpose.

---

## The Consistency Principle

Same patterns should work the same way everywhere:
- Same button style = same type of action
- Same spacing rhythm throughout
- Same interaction patterns
- Same feedback mechanisms

**Inconsistency tax:** Every deviation forces relearning.

---

## The Forgiveness Principle

Interfaces must tolerate error:
- Every action reversible
- Destructive operations require confirmation
- Recovery always possible

---

## Design Process Tips

### Start with Features, Not Layouts
Don't design layout first. Start with:
- What does this feature need?
- What elements required?
- How do they relate?

Layout emerges from features.

### Work in Grayscale First
Design without color to establish hierarchy through:
- Size
- Weight
- Spacing
- Position

**Why:** If design doesn't work in grayscale, it relies too heavily on color. Color should enhance hierarchy, not create it.

### Start with Too Much Whitespace
Begin generous, reduce as needed:
- Easier to remove than add
- Cramped feels cheap
- Whitespace = quality and clarity

### Design Mobile-First
Mobile constraints force better decisions:
- Prioritize ruthlessly
- Simplify navigation
- Focus on essential
- Scale up is easier

---

## Troubleshooting

### "It looks cluttered"
- Too many elements competing?
- Not enough whitespace?
- Inconsistent spacing?
- Hierarchy unclear?

**Fix:** Remove non-essential, increase spacing, reduce secondary element weight.

### "Users don't know what to click"
- Links not styled distinctly?
- Buttons look like labels?
- Ghost buttons blending in?
- No hover states?

**Fix:** Underline + color for links, shadows on buttons, solid primary CTAs.

### "Everything competes for attention"
- Multiple primary actions?
- Too many accent colors?
- Same visual weight everywhere?

**Fix:** One primary action, semantic colors only, vary weight/color.
