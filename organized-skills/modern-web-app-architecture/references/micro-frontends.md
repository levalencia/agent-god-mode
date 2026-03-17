# Micro-frontends Architecture

## Overview

Micro-frontends extend microservices principles to the frontend, creating vertically-sliced applications from database to UI. Each micro-frontend represents a business subdomain with end-to-end team ownership.

**Core Principle:** Optimize for feature development speed and team autonomy over code reuse.

## When to Use Micro-frontends

### Good Fit

- **Team Scale:** 10+ developers, multiple teams
- **Longevity:** Long-term maintenance expected
- **Independence:** Teams need parallel development
- **Migration:** Incremental legacy replacement
- **Technology:** Need framework flexibility

### Poor Fit

- **Small Teams:** <5 developers
- **Simple Domains:** Single bounded context
- **Rapid Pivoting:** Frequently changing business model
- **Limited DevOps:** Infrastructure immaturity

---

## Composition Strategies

### Vertical Split (Page-based)

One micro-frontend per page/view:

```
example.com/products  → Products MFE
example.com/cart      → Cart MFE
example.com/checkout  → Checkout MFE
```

**Characteristics:**
- Application shell orchestrates loading
- Only one MFE active at a time
- Simpler developer experience
- No namespace conflicts
- Lower component reusability

**Best For:** Familiar to SPA developers, clear page boundaries

### Horizontal Split (Fragment-based)

Multiple micro-frontends compose single views:

```
┌─────────────────────────────────────┐
│           Header MFE                 │
├───────────────┬─────────────────────┤
│   Sidebar MFE │    Content MFE      │
│               │                     │
└───────────────┴─────────────────────┘
```

**Characteristics:**
- Higher modularity and reuse
- More complex coordination
- Requires namespace management
- Shared state challenges

**Best For:** Reusable fragments, multiple teams per page

---

## Composition Techniques

### Client-Side

**Links (Simplest):**
```html
<!-- Navigation links between MFEs -->
<a href="/products">Products</a>
<a href="/cart">Cart</a>
```
- High isolation
- Page transitions (not seamless)
- Different apps, same domain

**Iframes:**
```html
<iframe src="https://checkout.example.com/widget"></iframe>
```
- Strong isolation (separate browsing context)
- Layout/sizing challenges
- Performance overhead
- Limited parent-child communication

**Web Components:**
```javascript
// checkout-button.js (MFE)
class CheckoutButton extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `<button>Checkout (${this.getAttribute('count')})</button>`;
  }
}
customElements.define('checkout-button', CheckoutButton);

// Parent app
<checkout-button count="3"></checkout-button>
```
- Encapsulation via Shadow DOM
- Framework-agnostic
- Lifecycle management
- Native browser support

**Module Federation (Webpack 5):**
```javascript
// Remote (checkout MFE)
new ModuleFederationPlugin({
  name: 'checkout',
  filename: 'remoteEntry.js',
  exposes: {
    './Button': './src/CheckoutButton',
  },
  shared: ['react', 'react-dom'],
});

// Host (shell)
new ModuleFederationPlugin({
  name: 'shell',
  remotes: {
    checkout: 'checkout@https://checkout.example.com/remoteEntry.js',
  },
  shared: ['react', 'react-dom'],
});

// Usage in shell
const CheckoutButton = React.lazy(() => import('checkout/Button'));
```
- Runtime code sharing
- Automatic vendor deduplication
- No build-time coupling
- Version negotiation

### Server-Side

**SSI (Server-Side Includes):**
```html
<!--#include virtual="/fragments/header" -->
<main>Content</main>
<!--#include virtual="/fragments/footer" -->
```
- Simple, well-understood
- Fast first-page load
- No client-side JavaScript needed

**ESI (Edge-Side Includes):**
```html
<esi:include src="/fragments/header" />
<main>Content</main>
<esi:include src="/fragments/footer" />
```
- Composition at CDN level
- Caching per fragment
- Reduces origin load

**Podium (Node.js):**
```javascript
// Layout server
const layout = new Layout({ name: 'myLayout' });
const header = layout.client.register({ name: 'header', uri: 'http://header/manifest.json' });

app.get('/', async (req, res) => {
  const incoming = res.locals.podium;
  const [headerHtml] = await Promise.all([header.fetch(incoming)]);
  res.send(`<html><body>${headerHtml}<main>...</main></body></html>`);
});
```

---

## Communication Patterns

### Same-View Communication

**Custom Events:**
```javascript
// Publisher (Cart MFE)
window.dispatchEvent(new CustomEvent('cart:updated', {
  detail: { itemCount: 3, total: 99.99 }
}));

// Subscriber (Header MFE)
window.addEventListener('cart:updated', (e) => {
  updateCartBadge(e.detail.itemCount);
});
```

**Event Bus (injected by shell):**
```javascript
// Shell provides event bus
window.eventBus = new EventEmitter();

// MFEs use it
window.eventBus.emit('user:logout');
window.eventBus.on('user:logout', clearUserData);
```

### Cross-View Communication

**URL/Query Parameters:**
```
/products?category=shoes&sort=price
↓ navigate to
/cart?from=products
```

**Web Storage:**
```javascript
// Auth MFE sets token
sessionStorage.setItem('auth_token', token);

// Other MFEs read
const token = sessionStorage.getItem('auth_token');
```

**Cookies (same subdomain):**
```javascript
document.cookie = 'user_id=123; path=/; domain=.example.com';
```

### Backend Communication

**Service Dictionary:**
```json
{
  "services": {
    "products": "https://api.example.com/products",
    "users": "https://api.example.com/users",
    "orders": "https://api.example.com/orders"
  }
}
```

**BFF per MFE:**
```
Products MFE → Products BFF → Product Service
Cart MFE     → Cart BFF     → Cart Service, Inventory Service
```

---

## Team Organization

### Cross-Functional Teams

Each team includes:
- Frontend developers
- Backend developers
- Designer
- QA
- Product owner

### Team Boundaries

Align with business domains (DDD bounded contexts):

```
Team Discover: Help customers find products
  → Search MFE, Product Catalog MFE

Team Decide: Help customers make decisions
  → Product Detail MFE, Reviews MFE, Comparison MFE

Team Buy: Enable purchases
  → Cart MFE, Checkout MFE, Payment MFE
```

### Ownership Model

- **Full Stack Ownership:** Team owns DB → API → UI
- **Independent Deployments:** No cross-team coordination
- **Autonomous Decisions:** Teams choose tech within guardrails

---

## Deployment Strategies

### Independent Deployment

Each MFE deployable without others:

```yaml
# CI/CD per MFE
name: Deploy Products MFE
on:
  push:
    paths:
      - 'products-mfe/**'
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm ci && npm run build
      - run: aws s3 sync dist/ s3://bucket/products/
```

### Blue-Green Deployment

```
Production (Blue): v1.0
Staging (Green):   v1.1

1. Deploy v1.1 to Green
2. Test Green
3. Switch traffic Blue → Green
4. Blue becomes new staging
```

### Canary Releases

```javascript
// Edge function for gradual rollout
export function handler(event) {
  const userId = getUserId(event);
  const canaryPercentage = 10;

  if (hash(userId) % 100 < canaryPercentage) {
    return fetch('https://products-v2.example.com' + event.path);
  }
  return fetch('https://products-v1.example.com' + event.path);
}
```

### Strangler Pattern (Migration)

```
┌─────────────────────────────────┐
│           Router                │
└───────┬───────────────┬─────────┘
        │               │
   ┌────▼────┐    ┌─────▼─────┐
   │ Legacy  │    │ New MFE   │
   │  App    │    │           │
   └─────────┘    └───────────┘

Route by route, migrate legacy → MFE
```

---

## Namespacing

### CSS

```css
/* Team prefix all classes */
.decide_product-card { }
.decide_product-card__title { }
.inspire_recommendation { }
```

Or use CSS Modules/CSS-in-JS for automatic scoping.

### JavaScript

```javascript
// IIFE to avoid globals
(function() {
  // MFE code here
})();

// Or ES modules (naturally scoped)
```

### Events

```javascript
// Namespace custom events
dispatchEvent(new CustomEvent('checkout:item-added', { detail }));
dispatchEvent(new CustomEvent('checkout:payment-started', { detail }));
```

### Storage

```javascript
// Prefix storage keys
localStorage.setItem('decide:recent-views', JSON.stringify(items));
sessionStorage.setItem('checkout:cart-id', cartId);
```

---

## Error Handling

### Timeouts

```javascript
// Fragment fetch with timeout
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 3000);

try {
  const response = await fetch(fragmentUrl, { signal: controller.signal });
  clearTimeout(timeout);
  return response.text();
} catch (e) {
  return '<div class="fallback">Content unavailable</div>';
}
```

### Fallbacks

```html
<!-- Server-side with fallback -->
<esi:include src="/header" onerror="continue">
  <esi:fallback>
    <nav class="minimal-header">...</nav>
  </esi:fallback>
</esi:include>
```

### Circuit Breaker

```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 30000) {
    this.failures = 0;
    this.threshold = threshold;
    this.timeout = timeout;
    this.state = 'CLOSED';
  }

  async call(fn) {
    if (this.state === 'OPEN') {
      throw new Error('Circuit open');
    }

    try {
      const result = await fn();
      this.failures = 0;
      return result;
    } catch (e) {
      this.failures++;
      if (this.failures >= this.threshold) {
        this.state = 'OPEN';
        setTimeout(() => this.state = 'HALF-OPEN', this.timeout);
      }
      throw e;
    }
  }
}
```

---

## Performance Considerations

### Shared Dependencies

```javascript
// Module Federation shared config
shared: {
  react: { singleton: true, requiredVersion: '^18.0.0' },
  'react-dom': { singleton: true, requiredVersion: '^18.0.0' },
}
```

### Bundle Budgets

```javascript
// Fitness function in CI
const stats = require('./dist/stats.json');
const mainBundle = stats.assets.find(a => a.name.includes('main'));

if (mainBundle.size > 150000) {
  console.error('Bundle exceeds 150KB budget!');
  process.exit(1);
}
```

### Lazy Loading

```javascript
// Load MFE on scroll
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      loadMicroFrontend(entry.target.dataset.mfe);
      observer.unobserve(entry.target);
    }
  });
});

document.querySelectorAll('[data-mfe]').forEach(el => observer.observe(el));
```

---

## Architecture Comparison

| Aspect | Vertical Split | Horizontal Split |
|--------|----------------|------------------|
| **Complexity** | Lower | Higher |
| **Reusability** | Lower | Higher |
| **Coordination** | Minimal | More required |
| **Testing** | Simpler | More complex |
| **Performance** | Better (one MFE) | Overhead (multiple) |
| **Team Independence** | High | Medium |
