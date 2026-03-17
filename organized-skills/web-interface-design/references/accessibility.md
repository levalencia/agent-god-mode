# Accessibility Reference

## Core Principle

**Build accessibility from project start.** Retrofitting is harder and produces worse results.

---

## Contrast Requirements (WCAG)

| Element | Minimum Ratio |
|---------|---------------|
| Normal text | 4.5:1 |
| Large text (18px+ or 14px+ bold) | 3:1 |
| UI components | 3:1 |
| Non-essential decorative | No requirement |

**Testing:** Don't rely on vision alone. Use accessibility checkers.

---

## Font Weight Rules

**Critical:** Never use thin or light fonts in interfaces. Almost always unreadable.

**On dark backgrounds:** Reduce bold weight to Regular or Semibold for balance.

---

## Color Guidelines

### Problem Colors
- **Gray text:** Almost always unreadable
- **Yellow text:** Very difficult to read
- **Pure white on black:** Too contrasting for extended reading

### Solutions
- White on black: Use light gray (#E0E0E0) instead
- Gray text: Ensure meets 4.5:1 ratio
- Use color checkers to verify

---

## Beyond Color

**Never rely on color alone to convey meaning:**
- Add icons to error states
- Include text labels with colored indicators
- Ensure patterns work in grayscale

### Examples

**❌ Color only**
```html
<input class="error">
```

**✓ Color + icon + text**
```html
<input class="error" aria-describedby="email-error">
<span id="email-error">
  ⚠️ Enter a valid email address
</span>
```

---

## Focus States

Every interactive element needs visible focus:

```css
.interactive:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}
```

**Never:** Remove focus outlines without providing alternative.

---

## Hidden vs Visible Hints

**Bad:** Hints hidden behind icons (tooltip on hover).
- Doesn't work for screen readers
- Doesn't work for vision issues
- Requires hover (no touch support)

**Good:** Visible hints displayed directly.
- "Well read by any user and screen readers"

---

## Form Accessibility

### Labels
- Every input needs a visible label
- Connect with `for`/`id` attributes
- Never use placeholder as only label

```html
<label for="email">Email Address</label>
<input type="email" id="email">
```

### Error Messages
- Use `aria-live="assertive"` for dynamic validation
- Connect with `aria-describedby`
- Don't rely on color alone

```html
<input id="password" aria-describedby="password-error">
<div id="password-error" role="alert" aria-live="assertive">
  Password must be at least 8 characters
</div>
```

### Fieldsets
- Group related inputs (radio buttons, checkboxes)
- Use `fieldset` and `legend`

```html
<fieldset>
  <legend>Notification preferences</legend>
  <label><input type="checkbox"> Email</label>
  <label><input type="checkbox"> SMS</label>
</fieldset>
```

---

## Keyboard Navigation

### Requirements
- All interactive elements keyboard accessible
- Logical tab order
- Focus trap in modals
- Escape key closes modals/dropdowns

### Tab Patterns
| Component | Keyboard Behavior |
|-----------|-------------------|
| Tabs | Tab to list, arrows between tabs, Enter activates |
| Accordions | Tab to headers, Enter/Space toggles |
| Modals | Focus trapped, Escape closes |
| Dropdowns | Arrows navigate, Enter selects, Escape closes |

---

## Touch Accessibility

**Touch targets:**
- Minimum: 44×44px
- Recommended: 48×48px

**Spacing between targets:** 8px minimum to prevent mis-taps.

---

## Testing Requirements

1. Contrast ratio checker (WebAIM, Stark)
2. Color blind vision simulators
3. Screen reader testing (VoiceOver, NVDA)
4. Keyboard-only navigation test
5. Zoom to 200% test

**Don't rely on:** "Looks fine to me"

---

## Quick Checklist

### Text
- [ ] All text meets contrast requirements
- [ ] No thin/light fonts
- [ ] No pure white on pure black for long text

### Color
- [ ] Color not sole indicator for errors/states
- [ ] Works in grayscale

### Forms
- [ ] Labels above fields (visible)
- [ ] Error messages specific and helpful
- [ ] Touch targets ≥ 44px

### Focus
- [ ] Focus states visible
- [ ] Logical tab order
- [ ] Focus trapped in modals

### Screen Readers
- [ ] Form labels connected
- [ ] Images have alt text
- [ ] Dynamic content announced (`aria-live`)
