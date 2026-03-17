# SPA Architecture Fundamentals

## What is an SPA?

A Single Page Application is delivered to the browser and doesn't reload during use. The entire application runs as one web page with the shell loaded once. Navigation occurs through view swapping, not page refreshes.

## Paradigm Shift from MPA

| Aspect | Multi-Page App | Single Page App |
|--------|----------------|-----------------|
| **Initial Load** | Complete HTML per request | Shell + assets once |
| **Navigation** | Full page refresh | View swap, no refresh |
| **Presentation Logic** | Server | Client |
| **HTML Generation** | Server-side | Client-side |
| **Data Transfer** | HTML documents | JSON payloads |
| **Server Role** | Everything | Auth, validation, data API |

## Core Components

### The Shell

The master controller providing structure:
- Loads initially with core styles and scripts
- Manages feature containers
- Handles application-wide state
- Coordinates module loading/unloading
- Controls routing decisions

```javascript
// Shell structure example
const Shell = {
  init() {
    this.initRouter();
    this.initEventBus();
    this.loadInitialModules();
  },

  loadModule(name) {
    import(`./modules/${name}.js`).then(module => {
      module.init(this.container);
    });
  },

  unloadModule(name) {
    this.modules[name]?.destroy();
  }
};
```

### Feature Modules

Independent, loosely-coupled units:
- Self-contained functionality (chat, navigation, etc.)
- Attached to Shell via defined APIs
- Own lifecycle management
- Communicate through events or shared services

```javascript
// Module structure
const ChatModule = {
  init(container) {
    this.container = container;
    this.bindEvents();
    this.render();
  },

  destroy() {
    this.unbindEvents();
    this.container.innerHTML = '';
  },

  bindEvents() {
    this.eventBus.on('user:login', this.onUserLogin);
  }
};
```

### Views

HTML fragments dynamically created:
- Not complete pages
- Swapped in/out by router
- May have associated controllers
- Rendered from templates + data

### Models

Data representation with business logic:
- Validation rules
- Computed properties
- Serialization/deserialization
- Server sync methods

---

## Routing

### Client-Side Routing

Router controls browser navigation without server round-trips:

**Hash-based Routing:**
```javascript
// Uses fragment identifier (#)
// URL: example.com/#/users/123
window.addEventListener('hashchange', () => {
  const route = window.location.hash.slice(1);
  router.navigate(route);
});
```

**History API Routing:**
```javascript
// Uses pushState/replaceState
// URL: example.com/users/123
history.pushState({ page: 'users' }, '', '/users/123');

window.addEventListener('popstate', (e) => {
  router.navigate(window.location.pathname);
});
```

### Route Configuration

```javascript
const routes = [
  { path: '/', component: Home },
  { path: '/users', component: UserList },
  { path: '/users/:id', component: UserDetail },
  { path: '/users/:id/edit', component: UserEdit },
  { path: '*', component: NotFound } // Default/catch-all
];
```

### The Anchor Interface Pattern

URI anchor drives bookmark-able state:

1. History event changes anchor
2. Anchor change triggers state change
3. Single code path for all bookmark-able states
4. Supports Forward/Back, bookmarks, sharing

```javascript
// State encoded in URL
// example.com/#/products?category=shoes&sort=price

function onAnchorChange() {
  const anchor = parseAnchor(location.hash);
  const proposedState = anchorToState(anchor);

  if (isValidTransition(currentState, proposedState)) {
    applyState(proposedState);
    currentState = proposedState;
  } else {
    restoreAnchor(currentState); // Reject invalid change
  }
}
```

---

## Module Organization

### Module Pattern Benefits

- **Namespace isolation**: Prevents collisions
- **Privacy**: Internal implementation hidden
- **Public API**: Clear contract for consumers
- **Encapsulation**: Change internals without breaking consumers

### IIFE Module Pattern (Legacy)

```javascript
const MyModule = (function() {
  // Private
  let privateVar = 0;

  function privateMethod() {
    return privateVar++;
  }

  // Public API
  return {
    increment() {
      return privateMethod();
    },
    getValue() {
      return privateVar;
    }
  };
})();
```

### ES Module Pattern (Modern)

```javascript
// myModule.js
let privateVar = 0;

function privateMethod() {
  return privateVar++;
}

export function increment() {
  return privateMethod();
}

export function getValue() {
  return privateVar;
}
```

### File Organization

**By Feature (Recommended for SPAs):**
```
/src
  /features
    /auth
      /components
      /hooks
      /services
      index.js
    /products
      /components
      /hooks
      /services
      index.js
  /shared
    /components
    /hooks
    /utils
```

**By Type (Traditional):**
```
/src
  /components
  /hooks
  /services
  /utils
  /pages
```

---

## State Management

### State Categories

**Bookmark-able State:**
- Stored in URI (hash or path)
- Survives refresh
- Shareable via URL
- Examples: current page, filters, search query

**Session State:**
- Stored in sessionStorage or memory
- Lost on tab close
- Examples: form drafts, UI preferences

**Persistent State:**
- Stored in localStorage or database
- Survives browser close
- Examples: user preferences, tokens

### State Flow

```
User Action
    ↓
Update Anchor/URL
    ↓
hashchange/popstate Event
    ↓
Parse New State
    ↓
Validate Transition
    ↓
Update Model → Notify View
    ↓
Re-render Affected Components
```

### State Management Requirements

1. **Browser history works**: Forward/Back functional
2. **Bookmarks restore state**: URL captures app state
3. **Partial updates**: Only changed parts re-render
4. **Predictable updates**: Single source of truth

---

## Client-Server Communication

### Data Layer Responsibilities

- Abstract HTTP communication
- Handle request/response serialization
- Manage authentication headers
- Provide error handling patterns
- Cache responses when appropriate

### RESTful API Consumption

```javascript
class ApiClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  async request(method, path, data) {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: data ? JSON.stringify(data) : undefined
    });

    if (!response.ok) {
      throw new ApiError(response.status, await response.json());
    }

    return response.json();
  }

  get(path) { return this.request('GET', path); }
  post(path, data) { return this.request('POST', path, data); }
  put(path, data) { return this.request('PUT', path, data); }
  delete(path) { return this.request('DELETE', path); }
}
```

### BFF Pattern (Backend for Frontend)

Dedicated backend per frontend type:

```
Mobile App  →  Mobile BFF  →
                              →  Microservices
Web App     →  Web BFF     →
```

Benefits:
- Optimized payloads per client
- Aggregation of multiple services
- Client-specific transformations
- Reduces client complexity

---

## Event-Driven Communication

### Pub/Sub for Module Communication

```javascript
class EventBus {
  constructor() {
    this.events = {};
  }

  on(event, callback) {
    (this.events[event] ||= []).push(callback);
    return () => this.off(event, callback);
  }

  off(event, callback) {
    this.events[event] = this.events[event]?.filter(cb => cb !== callback);
  }

  emit(event, data) {
    this.events[event]?.forEach(cb => cb(data));
  }
}

// Usage
eventBus.on('cart:updated', (cart) => {
  updateCartIcon(cart.itemCount);
});

eventBus.emit('cart:updated', { itemCount: 3, total: 99.99 });
```

### Benefits

- Modules don't know about each other
- Easy to add new subscribers
- Testable in isolation
- Loose coupling

### Considerations

- Can make data flow hard to trace
- No type safety without extra tooling
- Memory leaks if subscriptions not cleaned up

---

## SPA Trade-offs

### Advantages

| Benefit | Description |
|---------|-------------|
| **Responsiveness** | No page reloads, instant feedback |
| **Reduced Server Load** | Static assets cached, only data transferred |
| **Rich Interactions** | Desktop-app-like experience |
| **Offline Capable** | Service workers enable offline mode |
| **Separation of Concerns** | Clear frontend/backend boundary |

### Disadvantages

| Challenge | Mitigation |
|-----------|------------|
| **Initial Load** | Code splitting, lazy loading |
| **SEO** | SSR/SSG, prerendering |
| **JavaScript Dependency** | Progressive enhancement, SSR fallback |
| **Memory Leaks** | Proper cleanup, monitoring |
| **Browser History** | Proper router implementation |
| **Bundle Size** | Tree shaking, dynamic imports |

---

## When to Choose SPA

**Good Fit:**
- App-like experience required
- Heavy user interaction
- Real-time features (chat, collaboration)
- Behind authentication (SEO less critical)
- Complex client-side state

**Poor Fit:**
- Content-heavy sites (blogs, news)
- SEO-critical public pages
- Simple forms or informational pages
- Users on very slow connections
- Extremely constrained devices/networks *and* no budget to invest in performance + accessibility engineering

### Accessibility Considerations (SPA-Specific)

SPAs can be fully accessible, but you must handle a few things explicitly:

- **Focus management on navigation:** move focus to the new page’s main heading or main landmark after route changes.
- **Route change announcements:** announce page title/heading changes (e.g., `aria-live`) so screen reader users understand navigation occurred.
- **Skip links + landmarks:** keep a working “Skip to content” link and stable landmarks (`<header>`, `<nav>`, `<main>`, `<footer>`).
- **Dialog/menu patterns:** use established WAI-ARIA patterns for modals, menus, comboboxes, and avoid “div soup”.

**Hybrid Approach:**
Many modern frameworks (Next.js, Remix, Nuxt) allow mixing:
- SSR for public, SEO-critical pages
- SPA behavior for authenticated sections
- Best of both worlds
