# Accessibility & Internationalization (i18n)

## Accessibility Baseline (Don’t Negotiate)

Start with the fundamentals:
- Prefer **semantic HTML** (`<button>`, `<a>`, `<label>`, `<main>`, headings) over div-based components.
- Ensure full **keyboard navigation** (Tab order, visible focus, Escape handling in dialogs).
- Provide **names** for controls (label text, `aria-label`, `aria-labelledby`).
- Validate **color contrast** and support **reduced motion**.
- Avoid announcing “fake” states (don’t use ARIA to patch broken semantics).

## SPA-Specific Accessibility Pitfalls

Single-page routing changes the DOM without a full navigation event, so you must implement:

- **Document title updates:** set meaningful titles per route.
- **Focus management on route change:** move focus to a page-level heading or main landmark.
- **Route change announcements:** announce navigations for screen readers (e.g., an `aria-live` region).
- **Skip-to-content link:** keep it functional even with client routing.

## Component Checklists

### Buttons and Links
- Buttons trigger actions; links navigate.
- Disabled buttons should be actual `disabled` buttons (not CSS only).
- Links must have an `href` (for accessibility and expected browser behavior).

### Forms
- Every input has a `<label>` (or `aria-labelledby`).
- Validation errors are associated with inputs (`aria-describedby`) and announced.
- Error messages are specific (“Email is required”, not “Invalid”).

### Dialogs/Modals
- Trap focus while open; restore focus to the trigger on close.
- Close on Escape.
- Use `role="dialog"` + `aria-modal="true"` and a labeled title.

### Menus/Comboboxes
- Follow established WAI-ARIA patterns; these are hard to “wing”.
- Prefer a vetted component library if you can’t invest in deep a11y work.

## Automated + Manual Testing

- Automated: axe-core (unit/component tests), Lighthouse accessibility checks.
- Manual: keyboard-only pass, screen reader spot checks on critical flows.
- Regression: add a11y checks to Storybook/Chromatic flows if you use Storybook.

---

## Internationalization (i18n) Basics

### Treat Locale as a First-Class Input

- Centralize locale selection (user preference, browser default, account setting).
- Don’t hardcode dates/numbers/currency formatting.

### Use `Intl` APIs

- `Intl.DateTimeFormat` for dates/times (time zones matter).
- `Intl.NumberFormat` for currency/percent/compact notation.
- `Intl.PluralRules` for pluralization logic.

### Design for Translation

- Avoid string concatenation (“Hello " + name) where grammar differs; use message templates.
- Expect text expansion (German/French) and contraction.
- Support **RTL** layouts if your product needs it (mirror spacing/icons, not just text direction).

## i18n Checklist

- [ ] All user-facing strings are externalized
- [ ] Dates/numbers/currency use `Intl`
- [ ] Layout tolerates longer strings
- [ ] RTL support decision is explicit
- [ ] Time zone strategy is defined (user vs account vs server)

