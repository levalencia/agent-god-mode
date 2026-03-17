# Buttons Reference

## Making Buttons Look Clickable

Users must instantly recognize something is a button.

**Universal cues:**
- Drop shadows (even in flat design)
- Rounded corners
- Distinct shape from surrounding content
- Depth/elevation appearance

---

## Button Hierarchy

**Three weight levels:**

| Level | Use For | Visual Treatment |
|-------|---------|------------------|
| Primary | Main action, CTA | Filled, high contrast, prominent |
| Secondary | Alternative actions | Outlined or lower contrast fill |
| Tertiary | Minor actions | Text-only or very subtle |

**Rule:** One primary button per view. Multiple primary buttons confuse priority.

---

## CTA Button Design

**Contrast is essential.** CTA must stand out from everything.

**Effective techniques:**
- Complementary color to background
- Larger size than secondary buttons
- Strategic placement in scan path
- White space around button

**Research finding:** Red buttons can outperform green—test what works.

---

## Button Sizing

**Touch targets:**
- Minimum: 44×44px
- Preferred: 48×48px

**Research:** Larger buttons boost engagement by ~20%, but don't make them unprofessionally large.

**Padding ratios:** Horizontal typically 1.5–2× vertical.

```css
.button {
  padding: 12px 24px;  /* 1:2 ratio */
  min-height: 44px;
}
```

---

## Ghost Buttons

**Definition:** Transparent background, border only.

**Finding:** Ghost buttons grab less attention than solid CTAs.

**Use for:**
- Secondary actions alongside solid primary
- When you need button but not visual weight
- Image overlays where solid would obscure content

**Avoid for:**
- Primary conversions
- Critical actions
- Anywhere visibility crucial

---

## Button States

| State | Purpose | Treatment |
|-------|---------|-----------|
| Default | Ready for interaction | Standard appearance |
| Hover | User considering action | Slight color shift, cursor pointer |
| Active/Pressed | Being clicked | Darker shade, slight depression |
| Focused | Keyboard navigation | Clear focus ring |
| Disabled | Not available | 50% opacity, cursor change |
| Loading | Processing | Spinner, disabled interaction |

---

## Common Button CSS

```css
:root {
  --btn-height: 44px;
  --btn-padding-x: 24px;
  --btn-padding-y: 12px;
  --btn-radius: 6px;
  --btn-font-weight: 600;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: var(--btn-height);
  padding: var(--btn-padding-y) var(--btn-padding-x);
  border-radius: var(--btn-radius);
  font-weight: var(--btn-font-weight);
  font-size: 1rem;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-primary {
  background: var(--primary);
  color: white;
  border: none;
}

.btn-primary:hover {
  background: var(--primary-dark);
}

.btn-secondary {
  background: transparent;
  color: var(--primary);
  border: 2px solid var(--primary);
}

.btn-secondary:hover {
  background: var(--primary-light);
}

.btn-tertiary {
  background: transparent;
  color: var(--primary);
  border: none;
  padding: var(--btn-padding-y) 0;
}

.btn:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

---

## Good vs Bad Examples

**❌ Multiple primary buttons**
```html
<div class="actions">
  <button class="btn-primary">Save Draft</button>
  <button class="btn-primary">Preview</button>
  <button class="btn-primary">Publish</button>
</div>
```

**✓ Clear hierarchy**
```html
<div class="actions">
  <button class="btn-tertiary">Save Draft</button>
  <button class="btn-secondary">Preview</button>
  <button class="btn-primary">Publish</button>
</div>
```

---

## Destructive Actions

Destructive buttons (Delete, Remove) should:
- Use warning/red color
- NOT be primary unless destruction is the page's purpose
- Require confirmation for irreversible actions
