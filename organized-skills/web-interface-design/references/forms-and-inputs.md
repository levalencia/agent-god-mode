# Forms and Inputs Reference

## Form Design Philosophy

**Core insight:** "The easier the input, the faster the goal. Fewer refusals, higher conversion."

Every field creates friction. Every unclear label causes hesitation. Every validation error damages trust.

---

## Required vs Optional Fields

**Recommendation:** If a form has both required and optional fields, **remove optional fields entirely**.

Benefits:
- Removes asterisks and "required" indicators
- Simplifies visual design
- Reduces user decision-making

**If optional fields are necessary:**
- Mark with "(optional)" text
- Never rely solely on asterisks
- Place indicator after label, not inside field

---

## Input Field Design

### States

Every input needs these states:

| State | Visual Treatment |
|-------|-----------------|
| Default | Standard border, ready for input |
| Focused | Clear indicator (border color, glow) |
| Filled | May show checkmark for valid content |
| Error | Red border, error message visible |
| Disabled | Grayed out, cursor change |
| Read-only | Distinct from disabled, content copyable |

### Labels

**Placement:** Above the field, not inside.

```
✓ Email Address
  [                    ]

❌ [  Email Address    ]   ← disappears on focus
```

**Labels vs Placeholders:**
- **Labels:** Identify what field is for
- **Placeholders:** Hint on format/example (optional)

Never use placeholder as only label.

### Sizing

**Touch targets:** Minimum 44×44px.

**Field height:** Consistent across form (40px, 44px, or 48px).

**Field width:** Indicate expected content length:
- ZIP code: short
- Street address: long
- Phone: medium

---

## Validation and Errors

### Timing

**Inline validation:** Show errors as user leaves field, not while typing.

**Form-level validation:** On submit, scroll to first error and focus that field.

### Error Message Design

**Visual treatment:**
- Red border on problem field
- Error message directly below field
- Icon optional but helpful
- Semitransparent red background

**Message content:**
- Specific: "Password must be at least 8 characters" not "Invalid password"
- Constructive: Tell how to fix
- Polite: Never blame user

```
❌ Wrong format
❌ Error: Invalid input
✓ Enter a valid email (example: name@company.com)
✓ Password needs at least one number
```

### Accessibility

- Use `aria-live="assertive"` for dynamic validation
- Connect error messages with `aria-describedby`
- Don't rely on color alone—include text and/or icon

---

## Form Control Types

### Checkboxes

**When to use:** Multiple options can be selected. Binary yes/no.

**Label position:** Right of checkbox.

**Touch target:** Entire label clickable.

```html
<label class="checkbox-label">
  <input type="checkbox" name="subscribe">
  <span>Subscribe to newsletter</span>
</label>
```

**Indeterminate state:** For "select all" when some children selected.

**Grouping:** Use fieldset and legend for related checkboxes.

```html
<fieldset>
  <legend>Notification preferences</legend>
  <label><input type="checkbox"> Email</label>
  <label><input type="checkbox"> SMS</label>
</fieldset>
```

### Radio Buttons

**When to use:** Mutually exclusive options. User must choose exactly one.

**Minimum options:** Always 2+ (otherwise use checkbox).

**Pre-selection:** Consider pre-selecting most common, but never pre-select options with cost/commitment.

**Layout:**
- **Vertical:** Labels long, 3+ options, scanning important
- **Horizontal:** Only 2-3 options with short labels

```css
.radio-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
```

### Select Dropdowns

**When to use:**
- Many options (7+)
- Saving vertical space critical
- Options well-known

**When NOT to use:**
- Fewer than 5 options (use radios)
- User needs to see all options
- Options need explanation

**Native vs custom:** Native has better accessibility and mobile support.

**Searchable select:** Required when 15+ items.

**Placeholder:** Use "Select an option" not empty text.

```html
<select>
  <option value="" disabled selected>Select a country</option>
  <option value="us">United States</option>
</select>
```

### Text Areas

**Default size:** Match expected content length.

**Resize behavior:**
- Allow vertical resize
- Disable horizontal resize (breaks layout)
- Consider auto-resize

```css
textarea {
  resize: vertical;
  min-height: 120px;
}
```

**Character count:** Show when limits exist. Update real-time.

```
Message
[                                      ]
                                 247/500
```

### Toggle Switches

**When to use:**
- Immediate effect (no submit needed)
- Binary on/off states
- Settings that apply instantly

**When NOT to use:**
- Forms requiring submission
- Effect isn't immediate

**Visual states:**
- Off: Gray/neutral
- On: Colored (primary/success)
- Disabled: Reduced opacity

**Label position:** Left of toggle.

```css
.toggle {
  width: 48px;
  height: 28px;
  border-radius: 14px;
  background: var(--toggle-off);
  transition: background 0.2s;
}

.toggle.on { background: var(--primary); }

.toggle-handle {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  transition: transform 0.2s;
}

.toggle.on .toggle-handle {
  transform: translateX(20px);
}
```

### Date Pickers

**Input format:** Show expected format as placeholder/helper.

**Calendar popup:**
- Open on focus or icon click
- Allow manual text input
- Show current date
- Easy month/year navigation

**Date range:**
- Clear start/end fields
- Visual indication of range
- Prevent invalid ranges

**Accessibility:**
- Keyboard navigation (arrows for days)
- Screen reader announcements
- Clear focus indicators

### Search Fields

**Anatomy:**
```
┌────────────────────────────────────┐
│ 🔍  Search products...          [X]│
└────────────────────────────────────┘
  ↑                              ↑
  Icon                    Clear button
```

**Placeholder:** Describe what can be searched: "Search products..." not just "Search..."

**Clear button:** Show only when field has value.

**Submit behavior:** Instant search OR explicit submit—never require both.

**Empty state:** Helpful message with alternatives.

```
No results for "xyz"
Try searching for:
• Product category
• Brand name
```
