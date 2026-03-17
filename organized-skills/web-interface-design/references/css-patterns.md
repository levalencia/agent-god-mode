# CSS Implementation Patterns

## Typography System

```css
:root {
  /* Font sizes */
  --text-xs: 0.75rem;   /* 12px */
  --text-sm: 0.875rem;  /* 14px */
  --text-base: 1rem;    /* 16px */
  --text-lg: 1.125rem;  /* 18px */
  --text-xl: 1.25rem;   /* 20px */
  --text-2xl: 1.5rem;   /* 24px */
  --text-3xl: 2rem;     /* 32px */
  --text-4xl: 2.5rem;   /* 40px */

  /* Line heights */
  --leading-tight: 1.1;
  --leading-snug: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.7;

  /* Letter spacing */
  --tracking-tight: -0.02em;
  --tracking-normal: 0;
  --tracking-wide: 0.02em;
}

h1 {
  font-size: var(--text-4xl);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
  font-weight: 700;
}

h2 {
  font-size: var(--text-3xl);
  line-height: var(--leading-tight);
  font-weight: 600;
}

h3 {
  font-size: var(--text-2xl);
  line-height: var(--leading-snug);
  font-weight: 600;
}

body {
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  color: #333;
}
```

---

## Spacing System

```css
:root {
  /* 4px base unit */
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

/* Paragraph spacing */
p + p { margin-top: var(--space-4); }

/* Heading spacing */
h2 {
  margin-top: var(--space-8);
  margin-bottom: var(--space-3);
}

h3 {
  margin-top: var(--space-6);
  margin-bottom: var(--space-2);
}
```

---

## Color System

```css
:root {
  /* Primary */
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

[data-theme="dark"] {
  --bg-page: #121212;
  --bg-surface: #1e1e1e;
  --bg-hover: #2a2a2a;
  --border: #333333;
  --text-primary: #e0e0e0;
  --text-secondary: #a0a0a0;
  --text-tertiary: #707070;
  --primary: #60a5fa;
  --primary-light: rgba(96, 165, 250, 0.15);
}
```

---

## Button System

```css
:root {
  --btn-height: 44px;
  --btn-padding-x: 24px;
  --btn-padding-y: 12px;
  --btn-radius: 6px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: var(--btn-height);
  padding: var(--btn-padding-y) var(--btn-padding-x);
  border-radius: var(--btn-radius);
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-primary {
  background: var(--primary);
  color: white;
  border: none;
}

.btn-primary:hover { background: var(--primary-dark); }

.btn-secondary {
  background: transparent;
  color: var(--primary);
  border: 2px solid var(--primary);
}

.btn-secondary:hover { background: var(--primary-light); }

.btn-tertiary {
  background: transparent;
  color: var(--primary);
  border: none;
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

## Form Input System

```css
:root {
  --input-height: 44px;
  --input-padding-x: 16px;
  --input-radius: 6px;
  --input-border: 1px solid #d1d5db;
}

.form-group { margin-bottom: var(--space-5); }

.form-label {
  display: block;
  margin-bottom: var(--space-2);
  font-weight: 500;
  font-size: var(--text-sm);
}

.form-input {
  width: 100%;
  height: var(--input-height);
  padding: 0 var(--input-padding-x);
  border: var(--input-border);
  border-radius: var(--input-radius);
  font-size: var(--text-base);
  transition: border-color 0.15s;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.form-input.error { border-color: var(--error); }

.form-error {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-top: var(--space-2);
  color: var(--error);
  font-size: var(--text-sm);
}
```

---

## Elevation System

```css
:root {
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
  --shadow-xl: 0 20px 25px rgba(0,0,0,0.15);

  /* Two-shadow technique */
  --shadow-card:
    0 1px 3px rgba(0,0,0,0.12),
    0 1px 2px rgba(0,0,0,0.06);

  --shadow-dropdown:
    0 4px 6px rgba(0,0,0,0.1),
    0 2px 4px rgba(0,0,0,0.06);

  --shadow-modal:
    0 20px 50px rgba(0,0,0,0.2),
    0 10px 20px rgba(0,0,0,0.1);
}
```

---

## Animation Patterns

```css
:root {
  --ease-out: cubic-bezier(0.25, 0, 0.25, 1);
  --ease-in: cubic-bezier(0.5, 0, 0.75, 0.5);
  --ease-in-out: cubic-bezier(0.45, 0, 0.55, 1);
}

/* Button press */
.btn:active {
  transform: scale(0.98);
  transition: transform 0.1s var(--ease-out);
}

/* Modal entrance */
@keyframes modalIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal { animation: modalIn 0.2s var(--ease-out); }

/* Skeleton loading */
@keyframes shimmer {
  from { background-position: 200% 0; }
  to { background-position: -200% 0; }
}

.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Responsive Breakpoints

```css
:root {
  --bp-sm: 640px;
  --bp-md: 768px;
  --bp-lg: 1024px;
  --bp-xl: 1280px;
  --bp-2xl: 1536px;
}

/* Fluid typography */
:root {
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.75vw, 1.5rem);
  --text-xl: clamp(1.5rem, 1.25rem + 1.25vw, 2.5rem);
}
```

---

## Utility Classes

```css
/* Text colors */
.text-primary { color: var(--text-primary); }
.text-secondary { color: var(--text-secondary); }
.text-error { color: var(--error); }
.text-success { color: var(--success); }

/* Backgrounds */
.bg-surface { background: var(--bg-surface); }
.bg-page { background: var(--bg-page); }

/* Flexbox */
.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.gap-2 { gap: var(--space-2); }
.gap-4 { gap: var(--space-4); }

/* Spacing */
.p-4 { padding: var(--space-4); }
.mt-4 { margin-top: var(--space-4); }
.mb-4 { margin-bottom: var(--space-4); }
```

---

## Card Component

```css
.card {
  background: var(--bg-page);
  border-radius: 8px;
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

.card-body { padding: var(--space-4); }

.card-title {
  font-size: var(--text-lg);
  font-weight: 600;
  margin-bottom: var(--space-2);
}

.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
  transition: all 0.2s var(--ease-out);
}
```

---

## Modal Component

```css
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--bg-page);
  border-radius: 8px;
  max-width: 560px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-modal);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-4);
  border-bottom: 1px solid var(--border);
}

.modal-body { padding: var(--space-4); }

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  padding: var(--space-4);
  border-top: 1px solid var(--border);
}
```
