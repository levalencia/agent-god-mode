# Typography Reference

## The Three Typography Decisions

Every project requires three fundamental choices:

**1. Body Font Selection**
The main text font used everywhere—button labels, body copy, long reads. This determines the project's overall typographic style.

**2. Heading Font Choice**
Either match body typeface or select a contrasting font for visual distinction.

**3. Accent Font**
For captions, quotations, code snippets:
- Monospaced: good for short captions
- Serif: suits quotes and callouts
- Can match body if not needed

---

## Heading Design

### Sizing
**Optimal ratio:** Heading to body text max 1:3.
```
Body: 16px → Heading max: 48px (16 × 3)
```
Ratios exceeding 1:3 upset harmony and distract from content.

### Spacing Rules
```
Space BEFORE heading: 1.25× to 2× paragraph spacing
Space AFTER heading: 0.375× to 0.75× body line spacing
```

**Example:**
- Paragraph spacing: 20px
- Space before heading: 40px (20 × 2)
- Space after heading: 15px

**Why more space above:** Headings belong to content below, not above. More space above signals new section.

**Critical rule:** Always follow a heading with a paragraph—not a list, image, or table.

### Line Spacing for Headings

| Heading Size | Line Spacing |
|--------------|--------------|
| Large (h1-h2) | 1.1 to 1.2 |
| Medium (h3-h4) | 1.2 to 1.3 |
| Small (h5-h6) | 1.3 to 1.4 |

**Sweet spot: 1.2**

Bold headings need tighter line spacing—their weight already creates separation.

### Weight and Color

**Font weight creates hierarchy:**
- Bold/ExtraBold/Heavy for main headings
- Only ONE heading per screen at maximum weight
- Too many bold headings = oversaturation

**Color for lower-level headings:**
- h4–h6 may be same size as body text
- Different color creates enough contrast

### All Caps Headings

**Problems:**
- Large all-caps hard to read (especially multi-line)
- Appears as "single solid black line"

**Solutions:**
- Increase letter spacing significantly
- Reserve for small decorative headings only

### Dividers with Headings

**Correct:** Divider ABOVE heading
```
─────────────────────────
## New Section Heading

Content that belongs to this heading...
```

**Wrong:** Divider between heading and content (breaks semantic connection)

---

## Body Text and Line Spacing

### Recommended Values

| Text Type | Line Spacing |
|-----------|--------------|
| Body (long reads) | 1.5 to 1.7 |
| Body (interfaces) | 1.3 to 1.5 |
| Headings | 1.1 to 1.4 |
| Captions/small text | 1.4 to 1.6 |

**Starting point:** 1.5 for long texts.

### Adjustment Factors

**Font characteristics:**
- High x-height fonts → increase spacing
- Low x-height fonts → can reduce spacing

**Line length:**
- Shorter lines → less spacing needed

**Critical insight:** Line spacing is independent of font SIZE.

### Paragraph Spacing

**Formula:** Paragraph spacing = Line spacing ÷ 1.5

```
Line spacing: 24px
Paragraph spacing: 16px (24 ÷ 1.5)
```

---

## Vertical Rhythm

### What It Actually Is

**Misconception:** Baseline grids automatically create harmony.

**Reality:** True rhythm requires:
- Contrast and variety of elements
- Repetitive spacing patterns
- Harmonious relationships between values

### Three Spacing Scale Approaches

**1. Unit-Based Scale (Recommended for interfaces)**
```
Base: 4px or 8px
Scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64...
```
Best for dashboards, apps, mixed content.

**2. Line Spacing-Based Scale (Recommended for content)**
```
Body line spacing: 24px
Scale: 24, 48, 72, 96...
```
Best for articles, documentation, long reads.

**3. Body Font Size-Based Scale (Avoid)**
```
Body: 16px → Scale: 16, 32, 48, 64...
```
"Most controversial and highly questionable." Text height ≠ pixel value.

### Two-Scale Strategy

Complex projects may need two independent scales:
- **Content scale (line-spacing based):** For articles, documentation
- **Module scale (unit-based):** For cards, navigation, forms

---

## Readability Fundamentals

### The Core Principle
**"If the text is difficult to read, all other design is irrelevant."**

### Color and Contrast

**Serif fonts:** Use pure black on white—thinner letterforms handle high contrast.

**Sans-serif fonts:** Tone down black (use #333) to avoid excessive contrast.

**Dark backgrounds:**
- Reduce white text intensity (use light gray)
- Pure white creates "glowing halo" effect
- Good for short text, challenging for long reads

**Colored text:** Reserve for feedback (errors, success).

### Contrast Guidelines

| Situation | Recommendation |
|-----------|----------------|
| White on gray | Avoid—hard to read |
| White on dark/bright | Much better |
| Black on white (sans-serif) | Tone down the black |
| Black on white (serif) | Pure black works |
| White on black | Reduce white intensity |

**Testing:** Don't rely on vision alone. Use accessibility checkers.

### Alignment

**Center alignment:** Only for brief content—3-4 lines maximum.

```
❌ Long centered paragraphs are hard to read
   because the eye must find each new line start.

✓ Short centered text
   works fine.
```

**Left alignment:** Preferred for extended passages.

---

## Scanning vs Reading

### Two Different Design Modes

**Scanning interfaces:**
- Short texts, captions, headings, indicators
- Dashboards, control panels, marketing sites
- Users rapidly scan headings and images
- **Design:** Heavy emphasis on focal points, contrast, color

**Reading interfaces:**
- Long-form: articles, guides, documentation
- Users read beginning to end
- **Design:** Vertical layout, focus without distraction, careful body text parameters

### Different Typography for Each

Mixed interfaces (homepage with linked articles) may need **two separate typographic systems**:
- Scanning: More color, more contrast
- Reading: Careful line length, spacing, rhythm

---

## Links

### Color Selection

**Blue remains most familiar.** However:
- Red links work within red-accented interfaces
- Match link color to overall accent system

### Underlining Standards

**In body text:** Use underline + different color. Color alone "gets lost."

**Exceptions to underlining:**
- Navigation menus
- Dedicated CTA blocks
- All-caps links

**Best practice:** Users shouldn't expend cognitive effort determining clickability.

### Link Density

**"Principle of one link":** Limit to one link per paragraph.

Multiple links? Relocate to separate block:
```
Paragraph text without inline links.

**Related resources:**
- Link to first resource
- Link to second resource
```

### Link States

**Hover:** Clear contrast from normal appearance.

**Active menu state:** Explicit differentiation—underline removal or decorative elements.
