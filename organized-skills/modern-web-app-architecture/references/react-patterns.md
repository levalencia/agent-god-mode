# React Patterns & Architecture

## Component Patterns

### Container/Presentational Pattern

**Presentational Components:**
- Concerned with how things look
- Receive data via props
- No side effects or state management
- Easy to test and reuse

**Container Components:**
- Concerned with how things work
- Manage state and side effects
- Pass data to presentational components

```jsx
// Presentational
function UserList({ users, onDelete }) {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>
          {user.name}
          <button onClick={() => onDelete(user.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
}

// Container
function UserListContainer() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers().then(setUsers);
  }, []);

  const handleDelete = (id) => {
    setUsers(users.filter(u => u.id !== id));
  };

  return <UserList users={users} onDelete={handleDelete} />;
}
```

**Modern Take:** With hooks, this separation often happens within a single component using custom hooks to extract logic.

---

### Compound Components Pattern

**Purpose:** Create components that work together, sharing implicit state.

```jsx
function Select({ children, value, onChange }) {
  return (
    <SelectContext.Provider value={{ value, onChange }}>
      <div className="select">{children}</div>
    </SelectContext.Provider>
  );
}

Select.Option = function Option({ value, children }) {
  const { value: selected, onChange } = useContext(SelectContext);
  return (
    <div
      className={selected === value ? 'selected' : ''}
      onClick={() => onChange(value)}
    >
      {children}
    </div>
  );
};

// Usage - clean, flexible API
<Select value={country} onChange={setCountry}>
  <Select.Option value="us">United States</Select.Option>
  <Select.Option value="uk">United Kingdom</Select.Option>
  <Select.Option value="ca">Canada</Select.Option>
</Select>
```

**When to Use:**
- Complex components with related parts (Tabs, Accordion, Menu)
- Want flexible, declarative API
- Parent-child components share state

---

### Provider Pattern

**Purpose:** Share data across component tree without prop drilling.

```jsx
const ThemeContext = createContext(null);

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  const toggle = useCallback(() => {
    setTheme(t => t === 'light' ? 'dark' : 'light');
  }, []);

  const value = useMemo(() => ({ theme, toggle }), [theme, toggle]);

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

// Custom hook with safety check
function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be within ThemeProvider');
  return context;
}
```

**Best Practices:**
- Create custom hook for consuming context
- Memoize context value to prevent unnecessary re-renders
- Split contexts by update frequency (auth rarely changes, theme might)

---

### Hooks Pattern

**Purpose:** Extract reusable stateful logic.

```jsx
// Custom hook for form input
function useInput(initialValue) {
  const [value, setValue] = useState(initialValue);

  const onChange = useCallback((e) => {
    setValue(e.target.value);
  }, []);

  const reset = useCallback(() => {
    setValue(initialValue);
  }, [initialValue]);

  return { value, onChange, reset };
}

// Custom hook for async data
function useAsync(asyncFn, deps = []) {
  const [state, setState] = useState({
    data: null,
    loading: true,
    error: null
  });

  useEffect(() => {
    setState(s => ({ ...s, loading: true }));
    asyncFn()
      .then(data => setState({ data, loading: false, error: null }))
      .catch(error => setState({ data: null, loading: false, error }));
  }, deps);

  return state;
}
```

**Rules:**
- Name must start with `use`
- Only call at top level (not in conditions/loops)
- Only call from React functions

---

### Render Props Pattern

**Purpose:** Share code using prop whose value is a function.

```jsx
function Mouse({ render }) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMove = (e) => setPosition({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);

  return render(position);
}

// Usage
<Mouse render={({ x, y }) => (
  <div>Mouse at: {x}, {y}</div>
)} />
```

**Modern Alternative:** Custom hooks are usually cleaner:
```jsx
function useMousePosition() {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  // ... same effect logic
  return position;
}
```

---

### HOC Pattern (Higher-Order Components)

**Purpose:** Enhance components with additional functionality.

```jsx
function withAuth(Component) {
  return function AuthenticatedComponent(props) {
    const { user, loading } = useAuth();

    if (loading) return <Spinner />;
    if (!user) return <Redirect to="/login" />;

    return <Component {...props} user={user} />;
  };
}

// Usage
const ProtectedDashboard = withAuth(Dashboard);
```

**When to Prefer Hooks:**
- Logic needed in multiple components
- Want to avoid wrapper component overhead
- Need access to multiple data sources

**When to Use HOC:**
- Need to modify rendered output (wrapping)
- Cross-cutting concerns (auth, logging)
- Working with class components

---

## Performance Optimization

### Memoization Patterns

**React.memo - Component Memoization:**
```jsx
const ExpensiveList = memo(function ExpensiveList({ items }) {
  return items.map(item => <ExpensiveItem key={item.id} {...item} />);
});
```

**useMemo - Value Memoization:**
```jsx
// Expensive calculation
const sortedItems = useMemo(
  () => items.slice().sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// Referential equality for objects passed to memoized children
const filters = useMemo(
  () => ({ category, minPrice, maxPrice }),
  [category, minPrice, maxPrice]
);
```

**useCallback - Function Memoization:**
```jsx
// Stable function reference for memoized children
const handleDelete = useCallback((id) => {
  setItems(prev => prev.filter(item => item.id !== id));
}, []); // Empty deps - setItems is stable
```

**When to Memoize:**
- Component receives complex objects/arrays as props
- Child component is wrapped in React.memo
- Calculation is expensive (>1ms)
- Function is passed to memoized child
- Value is dependency of other hooks

**When NOT to Memoize:**
- Primitive props (strings, numbers)
- Component rarely re-renders anyway
- Memoization cost > computation cost

---

### Code Splitting Patterns

**Route-based Splitting:**
```jsx
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

**Component-based Splitting:**
```jsx
const HeavyChart = lazy(() => import('./components/HeavyChart'));

function Analytics() {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<Spinner />}>
          <HeavyChart />
        </Suspense>
      )}
    </div>
  );
}
```

---

## State Management Patterns

### State Lifting

```jsx
// Lift state to nearest common ancestor
function Parent() {
  const [shared, setShared] = useState(initialValue);

  return (
    <>
      <ChildA value={shared} onChange={setShared} />
      <ChildB value={shared} />
    </>
  );
}
```

### State Colocation

Keep state as close to where it's used as possible:

```jsx
// Bad - state in parent when only one child needs it
function Parent() {
  const [localThing, setLocalThing] = useState('');
  return <Child value={localThing} onChange={setLocalThing} />;
}

// Good - state in component that uses it
function Child() {
  const [localThing, setLocalThing] = useState('');
  return <input value={localThing} onChange={e => setLocalThing(e.target.value)} />;
}
```

### Reducer Pattern

```jsx
function reducer(state, action) {
  switch (action.type) {
    case 'ADD_ITEM':
      return { ...state, items: [...state.items, action.payload] };
    case 'REMOVE_ITEM':
      return { ...state, items: state.items.filter(i => i.id !== action.payload) };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    default:
      throw new Error(`Unknown action: ${action.type}`);
  }
}

function useShoppingCart() {
  const [state, dispatch] = useReducer(reducer, { items: [], loading: false });

  const addItem = useCallback((item) => {
    dispatch({ type: 'ADD_ITEM', payload: item });
  }, []);

  return { ...state, addItem };
}
```

---

## Testing Patterns

### Testing Library Philosophy

Test user behavior, not implementation:

```jsx
// Bad - testing implementation
expect(component.state.isOpen).toBe(true);

// Good - testing behavior
expect(screen.getByRole('dialog')).toBeVisible();
```

### Component Testing Pattern

```jsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('submits form with user data', async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();

  render(<ContactForm onSubmit={onSubmit} />);

  await user.type(screen.getByLabelText(/email/i), 'test@example.com');
  await user.type(screen.getByLabelText(/message/i), 'Hello!');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
    message: 'Hello!'
  });
});
```

### Hook Testing Pattern

```jsx
import { renderHook, act } from '@testing-library/react';

test('useCounter increments', () => {
  const { result } = renderHook(() => useCounter(0));

  expect(result.current.count).toBe(0);

  act(() => {
    result.current.increment();
  });

  expect(result.current.count).toBe(1);
});
```

---

## TypeScript Patterns

### Props Typing

```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
}

function Button({ variant = 'primary', size = 'md', loading, children, ...props }: ButtonProps) {
  return (
    <button className={`btn-${variant} btn-${size}`} disabled={loading} {...props}>
      {loading ? <Spinner /> : children}
    </button>
  );
}
```

### Generic Components

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}

// Usage with type inference
<List
  items={users}
  renderItem={user => user.name}
  keyExtractor={user => user.id}
/>
```

### Hook Typing

```typescript
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}
```

---

## Error Boundaries (Production Resilience)

React error boundaries catch render-time errors in their subtree and allow graceful fallback UI.

**Important:** Error boundaries must be class components (as of React 18+).

```tsx
import React from 'react';

export class ErrorBoundary extends React.Component<
  { fallback?: React.ReactNode; children: React.ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: unknown) {
    // Send to monitoring (Sentry, etc.)
    console.error(error);
  }

  render() {
    if (this.state.hasError) return this.props.fallback ?? <p>Something went wrong.</p>;
    return this.props.children;
  }
}
```

**Placement guidance:**
- Route/page-level boundaries: prevent a whole app white-screen.
- “Risky” widgets: charts, rich text renderers, third-party embeds.
- Pair with retry/reset logic (reset boundary state when navigation succeeds).

---

## Suspense (Code Splitting + Async Boundaries)

**Code splitting (stable, common):**

```tsx
import { lazy, Suspense } from 'react';

const SettingsPage = lazy(() => import('./pages/SettingsPage'));

function AppRoutes() {
  return (
    <Suspense fallback={<p>Loading…</p>}>
      <SettingsPage />
    </Suspense>
  );
}
```

**Boundary guidance:**
- Prefer multiple small boundaries over one giant boundary.
- Put fallbacks where users “expect” waiting (page region vs whole screen).
- Avoid nesting boundaries that constantly remount (it can lose state).

---

## Concurrency Patterns (Responsiveness)

Use transitions to keep input responsive while expensive updates happen.

```tsx
import { useTransition } from 'react';

function Search({ onQuery }) {
  const [isPending, startTransition] = useTransition();

  return (
    <div>
      <input
        onChange={(e) => {
          const q = e.target.value;
          startTransition(() => onQuery(q));
        }}
      />
      {isPending && <span>Searching…</span>}
    </div>
  );
}
```

**When to use:**
- Large lists/tables where filtering/sorting is expensive
- Navigations that trigger large renders
- Typing into inputs that updates multiple components
