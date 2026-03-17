# Web Performance Optimization

## Core Principle

**Latency, not bandwidth, is the performance bottleneck.** Network round-trips and JavaScript execution time dominate perceived performance.

## Key Metrics

### Core Web Vitals

| Metric | Good | Needs Work | Poor | Measures |
|--------|------|------------|------|----------|
| **LCP** | <2.5s | 2.5-4s | >4s | Loading (largest content) |
| **INP** | <200ms | 200-500ms | >500ms | Interactivity (responsiveness to inputs) |
| **CLS** | <0.1 | 0.1-0.25 | >0.25 | Visual stability |

**Note:** FID was an older Core Web Vital and has been replaced by INP. Prefer INP for modern guidance.

### Additional Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| **FCP** | <1.8s | First Contentful Paint |
| **TTI** | <3.8s | Time to Interactive |
| **TBT** | <200ms | Total Blocking Time |
| **TTFB** | <600ms | Time to First Byte |

---

## Network Optimization

### TCP Fundamentals

**Three-way handshake:** Adds 1 RTT before data transfer
**Slow start:** Connection ramps up gradually

```
New connection cost:
  DNS lookup:     ~50ms
  TCP handshake:  1 RTT (~50ms)
  TLS handshake:  1-2 RTT (~100ms)
  First byte:     1 RTT
  ─────────────────────────
  Total:          ~200-300ms before first byte
```

**Optimization:**
- Keep connections alive (HTTP/2)
- Use `preconnect` for known origins
- Minimize cross-origin requests

### HTTP/2 Benefits

- **Multiplexing:** Multiple requests over single connection
- **Header compression:** HPACK reduces redundant headers
- **Stream prioritization:** Important resources first

**Caution:** HTTP/2 server push is effectively deprecated in modern browsers. Prefer `preload`, `modulepreload`, and server-side hints (e.g., 103 Early Hints) instead.

### HTTP/3 (QUIC) Note

HTTP/3 can reduce connection setup latency and mitigate head-of-line blocking at the transport layer. It’s not a silver bullet, but it’s often beneficial on lossy mobile networks.

### Resource Hints

```html
<!-- DNS prefetch for future navigations -->
<link rel="dns-prefetch" href="https://api.example.com">

<!-- Preconnect for critical third-parties -->
<link rel="preconnect" href="https://cdn.example.com" crossorigin>

<!-- Preload critical resources -->
<link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/critical.css" as="style">

<!-- Prefetch for likely next navigations -->
<link rel="prefetch" href="/dashboard.js">

<!-- Modulepreload for ES modules -->
<link rel="modulepreload" href="/app.js">
```

---

## JavaScript Optimization

### Loading Strategies

```html
<!-- Blocks rendering (avoid) -->
<script src="app.js"></script>

<!-- Downloads in parallel, executes when ready (may break order) -->
<script src="app.js" async></script>

<!-- Downloads in parallel, executes after HTML parsing (maintains order) -->
<script src="app.js" defer></script>

<!-- Best: place at end of body with defer -->
<script src="app.js" defer></script>
</body>
```

### Code Splitting

**Route-based:**
```javascript
// Only load code for current route
const routes = {
  '/': () => import('./pages/Home'),
  '/products': () => import('./pages/Products'),
  '/cart': () => import('./pages/Cart'),
};
```

**Component-based:**
```javascript
// Load heavy components on demand
const HeavyChart = lazy(() => import('./HeavyChart'));

function Dashboard() {
  const [showChart, setShowChart] = useState(false);
  return (
    <>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<Spinner />}>
          <HeavyChart />
        </Suspense>
      )}
    </>
  );
}
```

**Import on Interaction:**
```javascript
button.addEventListener('click', async () => {
  const { processData } = await import('./heavy-processor.js');
  processData(data);
});
```

**Import on Visibility:**
```javascript
const observer = new IntersectionObserver(async (entries) => {
  if (entries[0].isIntersecting) {
    const { renderWidget } = await import('./widget.js');
    renderWidget(container);
    observer.disconnect();
  }
});
observer.observe(container);
```

### Tree Shaking

**Requirements:**
- ES Modules (import/export)
- Webpack/Rollup configured correctly
- Side-effect-free code

```javascript
// package.json
{
  "sideEffects": false,
  // or specify files with side effects
  "sideEffects": ["*.css", "./src/polyfills.js"]
}
```

```javascript
// Good: named imports enable tree shaking
import { debounce } from 'lodash-es';

// Bad: imports entire library
import _ from 'lodash';
```

### Bundle Size Budgets

| Asset Type | Budget |
|------------|--------|
| **Critical JS** | <170KB gzipped |
| **Total JS** | <300KB gzipped |
| **Critical CSS** | <14KB |
| **Total page weight** | <1MB |

---

## Rendering Optimization

### Critical Rendering Path

1. **HTML parsing** → DOM construction
2. **CSS parsing** → CSSOM construction
3. **Render tree** → DOM + CSSOM
4. **Layout** → Calculate positions
5. **Paint** → Draw pixels

**Optimization:**
- Inline critical CSS
- Defer non-critical CSS
- Avoid render-blocking scripts
- Minimize DOM depth

### Critical CSS

```html
<head>
  <!-- Inline critical (above-the-fold) CSS -->
  <style>
    /* Critical styles for initial viewport */
    header { ... }
    .hero { ... }
  </style>

  <!-- Load full CSS asynchronously -->
  <link rel="preload" href="styles.css" as="style"
        onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="styles.css"></noscript>
</head>
```

### Layout Thrashing Prevention

```javascript
// Bad: forces layout recalculation each iteration
elements.forEach(el => {
  el.style.width = el.offsetWidth + 10 + 'px'; // Read then write
});

// Good: batch reads, then batch writes
const widths = elements.map(el => el.offsetWidth);
elements.forEach((el, i) => {
  el.style.width = widths[i] + 10 + 'px';
});
```

---

## Image Optimization

### Responsive Images

```html
<img
  srcset="
    image-320.jpg 320w,
    image-640.jpg 640w,
    image-1280.jpg 1280w
  "
  sizes="(max-width: 640px) 100vw, 640px"
  src="image-640.jpg"
  alt="Description"
  loading="lazy"
  decoding="async"
>
```

### Modern Formats

```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description">
</picture>
```

### Lazy Loading

```html
<!-- Native lazy loading -->
<img src="image.jpg" loading="lazy" alt="...">

<!-- With Intersection Observer for more control -->
<img data-src="image.jpg" class="lazy" alt="...">
```

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      observer.unobserve(img);
    }
  });
});

document.querySelectorAll('.lazy').forEach(img => observer.observe(img));
```

---

## Caching Strategies

### HTTP Caching

```
# Immutable assets (hashed filenames)
Cache-Control: public, max-age=31536000, immutable

# HTML (always revalidate)
Cache-Control: no-cache

# API responses
Cache-Control: private, max-age=0, must-revalidate
```

### Service Worker Caching

```javascript
// Cache-first for static assets
self.addEventListener('fetch', (event) => {
  if (event.request.destination === 'image' ||
      event.request.destination === 'script' ||
      event.request.destination === 'style') {

    event.respondWith(
      caches.match(event.request).then(cached => {
        return cached || fetch(event.request).then(response => {
          const clone = response.clone();
          caches.open('static-v1').then(cache => cache.put(event.request, clone));
          return response;
        });
      })
    );
  }
});

// Network-first for API
self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const clone = response.clone();
          caches.open('api-v1').then(cache => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
  }
});
```

---

## React-Specific Optimization

### Preventing Re-renders

```jsx
// Memoize expensive components
const ExpensiveList = memo(function ExpensiveList({ items }) {
  return items.map(item => <Item key={item.id} {...item} />);
});

// Stable references for callbacks
const handleClick = useCallback((id) => {
  setItems(prev => prev.filter(item => item.id !== id));
}, []);

// Memoize computed values
const sortedItems = useMemo(
  () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);
```

### Virtual Lists

```jsx
import { FixedSizeList } from 'react-window';

function VirtualList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>{items[index].name}</div>
  );

  return (
    <FixedSizeList
      height={400}
      itemCount={items.length}
      itemSize={35}
    >
      {Row}
    </FixedSizeList>
  );
}
```

---

## Measuring Performance

### Lab Tools

- **Lighthouse:** Chrome DevTools, comprehensive audit
- **WebPageTest:** Real browsers, multiple locations
- **Chrome DevTools Performance:** Detailed timeline

### Field Tools

- **Chrome UX Report (CrUX):** Real user data
- **web-vitals library:** Measure in production

```javascript
import { onLCP, onINP, onCLS } from 'web-vitals';

onLCP(console.log);
onINP(console.log);
onCLS(console.log);

// Send to analytics
function sendToAnalytics({ name, delta, id }) {
  gtag('event', name, {
    event_category: 'Web Vitals',
    // CLS is typically a small decimal; scale it for integer metrics.
    value: Math.round(name === 'CLS' ? delta * 1000 : delta),
    event_label: id,
    non_interaction: true,
  });
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

---

## Performance Checklist

### Critical Path
- [ ] Inline critical CSS (<14KB)
- [ ] Defer non-critical CSS
- [ ] Async/defer all JavaScript
- [ ] Preconnect to critical origins
- [ ] Preload critical resources

### JavaScript
- [ ] Code split by route
- [ ] Lazy load non-critical components
- [ ] Tree shake unused code
- [ ] Bundle size under budget
- [ ] Avoid large third-party libraries

### Images
- [ ] Modern formats (WebP, AVIF)
- [ ] Responsive images with srcset
- [ ] Lazy load below-fold images
- [ ] Properly sized (not scaled down)

### Caching
- [ ] Long cache for hashed assets
- [ ] Service worker for offline
- [ ] Proper cache headers

### React
- [ ] Memoize expensive components
- [ ] Virtual lists for large datasets
- [ ] Avoid unnecessary re-renders
- [ ] Use production builds
