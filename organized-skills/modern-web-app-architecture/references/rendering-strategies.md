# Rendering Strategies

## Overview

How and where HTML is generated significantly impacts performance, SEO, and user experience. Modern frameworks often combine multiple strategies.

## Strategy Comparison

| Strategy | Generation | SEO | TTI | Use Case |
|----------|------------|-----|-----|----------|
| **CSR** | Client | Poor | Slow | Apps behind auth |
| **SSR** | Server/request | Good | Medium | Dynamic, personalized |
| **SSG** | Build time | Good | Fast | Static content |
| **ISR** | Build + revalidate | Good | Fast | Semi-static |
| **RSC** | Server (component) | Good | Fast | Mixed static/dynamic |

---

## Client-Side Rendering (CSR)

### How It Works

1. Server sends minimal HTML shell
2. Browser downloads JavaScript bundle
3. JavaScript renders content
4. Data fetched after initial render

```html
<!-- Server response -->
<!DOCTYPE html>
<html>
<head>
  <script src="app.js" defer></script>
</head>
<body>
  <div id="root"></div>
</body>
</html>
```

```javascript
// app.js renders everything
ReactDOM.createRoot(document.getElementById('root')).render(<App />);
```

### Pros
- Rich interactivity
- Clear client/server separation
- Simple deployment (static files)
- Good for app-like experiences

### Cons
- Poor SEO (crawlers may not execute JS)
- Slow initial paint (wait for JS)
- Large JavaScript bundles
- Performance varies by device

### When to Use
- Authenticated applications (dashboards, admin)
- Highly interactive tools
- When SEO doesn't matter
- Internal applications

### Optimization
- Code splitting by route
- Lazy load non-critical components
- Service worker for caching
- Skeleton screens during load

---

## Server-Side Rendering (SSR)

### How It Works

1. Server renders full HTML on each request
2. HTML sent to browser (fast FCP)
3. JavaScript "hydrates" the page (makes it interactive)

```javascript
// Next.js pages router
export async function getServerSideProps(context) {
  const data = await fetchData(context.params.id);
  return { props: { data } };
}

export default function Page({ data }) {
  return <div>{data.title}</div>;
}
```

```javascript
// Next.js app router (default server component)
async function Page({ params }) {
  const data = await fetchData(params.id);
  return <div>{data.title}</div>;
}
```

### Pros
- Good SEO (full HTML for crawlers)
- Faster First Contentful Paint
- Works without JavaScript (progressive enhancement)
- Dynamic, personalized content

### Cons
- Higher server load
- Slower Time to First Byte
- Full page generated per request
- Hydration overhead

### When to Use
- SEO-critical dynamic pages
- Personalized content
- Frequently changing data
- E-commerce product pages

### Optimization
- Streaming SSR (send HTML in chunks)
- Selective hydration
- Cache where possible
- Edge rendering (closer to users)

---

## Static Site Generation (SSG)

### How It Works

1. Pages generated at build time
2. HTML files served from CDN
3. Optional client-side hydration

```javascript
// Next.js pages router
export async function getStaticProps() {
  const posts = await fetchPosts();
  return { props: { posts } };
}

export async function getStaticPaths() {
  const posts = await fetchPosts();
  return {
    paths: posts.map(post => ({ params: { id: post.id } })),
    fallback: false
  };
}
```

### Pros
- Fastest Time to First Byte
- Excellent SEO
- Cheap hosting (static files)
- Global CDN distribution
- High reliability

### Cons
- Build time increases with pages
- Stale content until rebuild
- Not suitable for dynamic content
- Long builds for large sites

### When to Use
- Marketing pages
- Documentation
- Blogs
- Product catalogs (stable inventory)

### Optimization
- Incremental builds (only changed pages)
- On-demand revalidation
- Hybrid with SSR for dynamic sections

---

## Incremental Static Regeneration (ISR)

### How It Works

Combines SSG with periodic background regeneration:

1. Page generated at build time
2. Served from cache
3. After revalidation period, regenerated in background
4. Next visitor gets fresh page

```javascript
// Next.js pages router
export async function getStaticProps() {
  const data = await fetchData();
  return {
    props: { data },
    revalidate: 60 // Regenerate every 60 seconds
  };
}
```

```javascript
// Next.js app router
async function Page() {
  const data = await fetchData();
  return <div>{data}</div>;
}

export const revalidate = 60; // Page-level revalidation
```

### On-Demand Revalidation

```javascript
// API route to trigger revalidation
export default async function handler(req, res) {
  await res.revalidate('/products');
  return res.json({ revalidated: true });
}
```

### Pros
- Static performance
- Content stays fresh
- Scales to millions of pages
- No full rebuild needed

### Cons
- Some staleness acceptable
- Complexity in revalidation logic
- First visitor after expiry waits

### When to Use
- Product pages (inventory updates)
- User profiles (infrequent changes)
- News sites
- Large catalogs

---

## React Server Components (RSC)

### How It Works

Components render on server, sending serialized output (not HTML) to client:

1. Server components run only on server
2. Can directly access databases, file system
3. Zero JavaScript sent for server components
4. Client components hydrate as needed

```javascript
// Server Component (default in app router)
async function ProductList() {
  const products = await db.query('SELECT * FROM products');
  return (
    <ul>
      {products.map(p => <ProductCard key={p.id} product={p} />)}
    </ul>
  );
}

// Client Component
'use client';
function AddToCartButton({ productId }) {
  const [loading, setLoading] = useState(false);

  async function handleClick() {
    setLoading(true);
    await addToCart(productId);
    setLoading(false);
  }

  return <button onClick={handleClick} disabled={loading}>Add to Cart</button>;
}
```

### Pros
- Zero-bundle server components
- Direct data access (no API layer)
- Automatic code splitting
- Better performance
- Simpler data fetching

### Cons
- New mental model
- Can't use hooks in server components
- Framework-specific (Next.js, etc.)
- Ecosystem still maturing

### When to Use
- Data-heavy pages
- Want minimal client JavaScript
- Using Next.js 13+ App Router
- Complex data fetching needs

### Patterns

**Container/Presentational with RSC:**
```javascript
// Server container
async function ProductPage({ id }) {
  const product = await fetchProduct(id);
  return <ProductDetails product={product} />;
}

// Client presentational
'use client';
function ProductDetails({ product }) {
  return (
    <div>
      <h1>{product.name}</h1>
      <AddToCartButton productId={product.id} />
    </div>
  );
}
```

---

## Islands Architecture

### How It Works

Static HTML with interactive "islands" that hydrate independently:

1. Most content is static HTML
2. Interactive components marked as islands
3. Each island hydrates independently
4. Minimal JavaScript shipped

```astro
---
// Astro example
import Header from './Header.astro'; // Static
import SearchBar from './SearchBar.tsx'; // Interactive island
---

<html>
  <body>
    <Header /> <!-- No JS -->
    <SearchBar client:visible /> <!-- Hydrates when visible -->
    <main>{staticContent}</main>
  </body>
</html>
```

### Pros
- Excellent performance
- Progressive enhancement
- Minimal JavaScript
- Independent hydration

### Cons
- Different development model
- Limited framework options
- Complexity for highly interactive apps

### When to Use
- Content-heavy sites with some interactivity
- Marketing sites
- Documentation
- Blogs with interactive widgets

---

## Streaming SSR

### How It Works

Send HTML in chunks as it's generated:

```javascript
// React 18 streaming
import { renderToPipeableStream } from 'react-dom/server';

app.get('/', (req, res) => {
  const { pipe } = renderToPipeableStream(<App />, {
    onShellReady() {
      res.setHeader('Content-Type', 'text/html');
      pipe(res);
    }
  });
});
```

```jsx
// With Suspense boundaries
function Page() {
  return (
    <Layout>
      <Header /> {/* Sent immediately */}
      <Suspense fallback={<Spinner />}>
        <SlowComponent /> {/* Streamed when ready */}
      </Suspense>
    </Layout>
  );
}
```

### Pros
- Faster Time to First Byte
- Progressive rendering
- Better perceived performance
- Prioritize critical content

### Cons
- More complex setup
- Not all hosting supports streaming
- Error handling complexity

---

## Decision Guide

```
Is content mostly static?
├─ Yes → Does it change frequently?
│        ├─ No → SSG
│        └─ Yes → ISR
│
└─ No → Is it personalized/user-specific?
        ├─ Yes → Is SEO critical?
        │        ├─ Yes → SSR
        │        └─ No → CSR (app behind auth)
        │
        └─ No → Is it highly interactive?
                ├─ Yes → CSR or Islands
                └─ No → SSR or RSC
```

## Hybrid Approaches

Modern frameworks support mixing strategies:

```javascript
// Next.js: Different strategies per route
// pages/index.js - SSG
export async function getStaticProps() { }

// pages/dashboard.js - CSR (no data fetching)
export default function Dashboard() {
  const { data } = useSWR('/api/user');
}

// pages/products/[id].js - ISR
export async function getStaticProps() {
  return { props: {}, revalidate: 60 };
}

// pages/cart.js - SSR
export async function getServerSideProps() { }
```

## Performance Comparison

| Metric | CSR | SSR | SSG | ISR | RSC |
|--------|-----|-----|-----|-----|-----|
| **TTFB** | Fast | Slow | Fastest | Fast | Medium |
| **FCP** | Slow | Fast | Fastest | Fast | Fast |
| **TTI** | Slow | Medium | Fast | Fast | Fast |
| **JS Size** | Large | Medium | Small | Small | Smallest |
| **Server Load** | None | High | None | Low | Medium |
