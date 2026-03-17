# UI Components Reference

## Navigation

### Primary Navigation
**Position:** Top or left side—users expect it there.

**Visual weight:** Visible but not overwhelming. Infrastructure, not main event.

**Current state:** Always indicate location:
- Bold text
- Background color change
- Underline or border accent
- Icon change

```css
.nav-item.active {
  background: var(--primary-light);
  color: var(--primary);
  font-weight: 600;
}
```

### Mobile Navigation
- Hamburger menus reduce discoverability—consider bottom nav for critical actions
- Touch targets: 44px minimum height
- Thumb zone: Place frequent items within easy reach

### Breadcrumbs

**When to use:**
- Hierarchical sites (3+ levels)
- Users need location awareness
- Users may navigate up the tree

**Separator:** Use `>` or `/` consistently.

**Current page:** Not a link (redundant).

```
Home > Products > Electronics > Smartphones
       ↑ link    ↑ link       ↑ current (no link)
```

---

## Cards

### Anatomy
```
┌─────────────────────────────────────┐
│ [Image/Media]                       │
├─────────────────────────────────────┤
│ Category Label                      │  ← Optional eyebrow
│ Card Title                          │  ← Primary info
│ Supporting text...                  │  ← Secondary info
├─────────────────────────────────────┤
│ [Action Button]     [Secondary]     │  ← Actions at bottom
└─────────────────────────────────────┘
```

### Design Rules

**Consistent sizing:** Cards in grid should be same size.

**Image ratios:** Pick one (16:9, 4:3, 1:1) and use consistently.

**Padding:** Consistent internal spacing (16px, 20px, 24px).

**Clickable cards:**
```css
.card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transform: translateY(-2px);
  cursor: pointer;
}
```

### Content Hierarchy
1. Image (catches eye first)
2. Title (primary info)
3. Description (supporting)
4. Metadata (least important)
5. Actions (clear next steps)

**Never:** Put actions above title.

---

## Tabs

### When to Use

**Good for:**
- Switching related views
- Equally important content
- Quick access needed
- 2-5 options

**Bad for:**
- Sequential processes (use stepper)
- More than 5-6 sections
- Content needing comparison
- Long labels

### Design Rules

**Alignment:** Left-align. Centered only for 2-3 short labels.

**Active indicator:**
```css
.tab.active {
  font-weight: 600;
  color: var(--primary);
  border-bottom: 2px solid var(--primary);
}

.tab:not(.active) {
  color: var(--text-secondary);
  border-bottom: 2px solid transparent;
}
```

**Keyboard:** Tab to list, arrows to switch, Enter to activate.

### Responsive Behavior
- Scrollable tabs with indicators
- Dropdown collapse
- Convert to accordions

**Don't:** Let tabs wrap to multiple lines.

---

## Accordions

### When to Use

**Good for:**
- Long expandable content
- FAQs
- Mobile navigation
- Clear section boundaries

**Bad for:**
- Frequently compared content
- Very short content
- Desktop primary navigation

### Design Rules

**Expand indicator:** Chevron or +/- with animation.

**Open behavior:** Decide one-at-a-time or multiple.

**Clickability:** Entire header row, not just icon.

```css
.accordion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  cursor: pointer;
}

.accordion-icon {
  transition: transform 0.2s;
}

.accordion.open .accordion-icon {
  transform: rotate(180deg);
}
```

---

## Data Tables

### Alignment
- Text: Left-align
- Numbers: Right-align (decimal alignment)
- Dates: Left-align
- Status: Center

```css
.table td { text-align: left; }
.table td.numeric {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
.table td.status { text-align: center; }
```

### Row height
- Minimum: 48px (touch accessible)
- Dense: 40px acceptable

### Headers
- Sticky for long tables
- Sortable arrows
- Active sort: bold/colored

### Responsive Options
1. Horizontal scroll
2. Card transformation
3. Priority columns only

**Never:** Let tables break layout.

---

## Modals

### Anatomy
```
┌─────────────────────────────────────┐
│ [X]                          Title  │
├─────────────────────────────────────┤
│ Modal content                       │
├─────────────────────────────────────┤
│               [Cancel] [Confirm]    │
└─────────────────────────────────────┘
         ↓ Dimmed overlay behind
```

### Rules

**Size:** Don't fill screen—leave visible backdrop edge.

**Max width:** 480-640px for dialogs.

**Close options:** X button, Cancel, Escape, click outside (non-critical).

**Focus trap:** Tab cycles within modal.

```css
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  border-radius: 8px;
  max-width: 560px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}
```

### Destructive Actions

```
❌ Are you sure? [OK] [Cancel]

✓ Delete "Project Alpha"?
  This will permanently delete 47 files.
  This action cannot be undone.

  [Cancel]  [Delete Project] ← red
```

---

## Toast Notifications

**Position:** Top-right or bottom-center.

**Duration:**
- Success: 3-5 seconds
- Error: Stay until dismissed
- Info: 5-7 seconds

**Stacking:** Multiple toasts should stack, not replace.

```css
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 12px 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.toast.success {
  background: var(--success-bg);
  border-left: 4px solid var(--success);
}

.toast.error {
  background: var(--error-bg);
  border-left: 4px solid var(--error);
}
```
