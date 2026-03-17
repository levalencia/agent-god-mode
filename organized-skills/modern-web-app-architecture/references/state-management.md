# State Management Patterns

## State Categories

| Type | Scope | Storage | Examples |
|------|-------|---------|----------|
| **Local** | Single component | useState/useReducer | Form inputs, toggles |
| **Shared** | Component subtree | Lifted state, Context | Filters, selections |
| **Global** | Entire app | Store (Redux, Zustand) | User, theme, cart |
| **Server** | Remote data | React Query, SWR | API responses |
| **URL** | Navigation | Router | Page, filters, search |

---

## Local State

### useState

```jsx
function Counter() {
  const [count, setCount] = useState(0);

  // Updater function for state based on previous
  const increment = () => setCount(prev => prev + 1);

  return <button onClick={increment}>{count}</button>;
}
```

### useReducer

For complex state with multiple sub-values:

```jsx
const initialState = { count: 0, step: 1 };

function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step };
    case 'setStep':
      return { ...state, step: action.payload };
    case 'reset':
      return initialState;
    default:
      throw new Error(`Unknown action: ${action.type}`);
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <input
        type="number"
        value={state.step}
        onChange={e => dispatch({ type: 'setStep', payload: +e.target.value })}
      />
    </>
  );
}
```

**When to use useReducer:**
- Next state depends on previous
- Multiple sub-values
- Complex update logic
- Want to test reducer separately

---

## Shared State

### Lifting State Up

Share state via nearest common ancestor:

```jsx
function Parent() {
  const [selected, setSelected] = useState(null);

  return (
    <>
      <List items={items} onSelect={setSelected} />
      <Detail item={selected} />
    </>
  );
}
```

### React Context

For state that many components need:

```jsx
// Create context
const AuthContext = createContext(null);

// Provider component
function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth().then(user => {
      setUser(user);
      setLoading(false);
    });
  }, []);

  const login = async (credentials) => {
    const user = await authService.login(credentials);
    setUser(user);
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  const value = useMemo(
    () => ({ user, loading, login, logout }),
    [user, loading]
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook
function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

**Context Best Practices:**
- Split contexts by update frequency
- Memoize context value
- Create custom hooks for consumption
- Don't overuse (prop drilling is fine for 2-3 levels)

---

## Global State Libraries

### Zustand (Minimal)

```javascript
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  reset: () => set({ count: 0 }),
}));

// Usage
function Counter() {
  const count = useStore((state) => state.count);
  const increment = useStore((state) => state.increment);

  return <button onClick={increment}>{count}</button>;
}
```

**With persistence:**
```javascript
import { persist } from 'zustand/middleware';

const useStore = create(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
    }),
    { name: 'app-storage' }
  )
);
```

**Pros:** Minimal boilerplate, no provider needed, good performance
**Cons:** Less structure for large apps, fewer dev tools

### Redux Toolkit

```javascript
import { createSlice, configureStore } from '@reduxjs/toolkit';

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => { state.value += 1; },
    decrement: (state) => { state.value -= 1; },
    incrementBy: (state, action) => { state.value += action.payload; },
  },
});

export const { increment, decrement, incrementBy } = counterSlice.actions;

const store = configureStore({
  reducer: {
    counter: counterSlice.reducer,
  },
});

// Usage
function Counter() {
  const count = useSelector((state) => state.counter.value);
  const dispatch = useDispatch();

  return (
    <button onClick={() => dispatch(increment())}>
      {count}
    </button>
  );
}
```

**Pros:** Time-travel debugging, middleware, large ecosystem
**Cons:** More boilerplate, learning curve

### Jotai (Atomic)

```javascript
import { atom, useAtom } from 'jotai';

// Primitive atom
const countAtom = atom(0);

// Derived atom
const doubledAtom = atom((get) => get(countAtom) * 2);

// Writable derived atom
const countryAtom = atom('us');
const currencyAtom = atom(
  (get) => currencies[get(countryAtom)],
  (get, set, newCurrency) => {
    set(countryAtom, Object.entries(currencies).find(([, c]) => c === newCurrency)?.[0]);
  }
);

// Usage
function Counter() {
  const [count, setCount] = useAtom(countAtom);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

**Pros:** Atomic model, minimal re-renders, React-like API
**Cons:** Different mental model, smaller ecosystem

### XState (State Machines)

```javascript
import { createMachine, assign } from 'xstate';
import { useMachine } from '@xstate/react';

const toggleMachine = createMachine({
  id: 'toggle',
  initial: 'inactive',
  context: { count: 0 },
  states: {
    inactive: {
      on: { TOGGLE: 'active' }
    },
    active: {
      entry: assign({ count: (ctx) => ctx.count + 1 }),
      on: { TOGGLE: 'inactive' }
    }
  }
});

function Toggle() {
  const [state, send] = useMachine(toggleMachine);

  return (
    <button onClick={() => send('TOGGLE')}>
      {state.value} (toggled {state.context.count} times)
    </button>
  );
}
```

**Pros:** Explicit states prevent impossible states, visual diagrams
**Cons:** Learning curve, overkill for simple state

---

## Server State

### React Query / TanStack Query

```javascript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Fetching
function Products() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;

  return <ProductList products={data} />;
}

// Mutations
function AddProduct() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: createProduct,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      mutation.mutate(new FormData(e.target));
    }}>
      {/* form fields */}
    </form>
  );
}
```

**Features:**
- Automatic caching
- Background refetching
- Optimistic updates
- Pagination support
- Offline support

### SWR

```javascript
import useSWR from 'swr';

const fetcher = (url) => fetch(url).then(res => res.json());

function Profile() {
  const { data, error, isLoading } = useSWR('/api/user', fetcher);

  if (isLoading) return <Spinner />;
  if (error) return <Error />;

  return <div>Hello, {data.name}</div>;
}
```

**Simpler than React Query, good for read-heavy apps.**

---

## URL State

### React Router

```jsx
import { useSearchParams } from 'react-router-dom';

function ProductList() {
  const [searchParams, setSearchParams] = useSearchParams();
  const category = searchParams.get('category') || 'all';
  const sort = searchParams.get('sort') || 'name';

  const updateFilters = (key, value) => {
    setSearchParams(prev => {
      prev.set(key, value);
      return prev;
    });
  };

  return (
    <>
      <select
        value={category}
        onChange={(e) => updateFilters('category', e.target.value)}
      >
        <option value="all">All</option>
        <option value="shoes">Shoes</option>
      </select>
      {/* Products filtered by URL params */}
    </>
  );
}
```

**Benefits of URL State:**
- Shareable links
- Browser history works
- Server can read initial state
- Bookmarkable

---

## State Management Selection Guide

```
What kind of state?
│
├─ Server data (API responses)
│  └─ React Query or SWR
│
├─ UI state (modals, dropdowns)
│  └─ Local useState
│
├─ Form state
│  └─ Local state or React Hook Form
│
├─ Shared between few components
│  └─ Lift state up
│
├─ Used by many components
│  ├─ Changes frequently → Zustand/Redux
│  └─ Changes rarely → Context
│
├─ Complex flows with explicit states
│  └─ XState
│
└─ Should persist in URL
   └─ URL/Search params
```

---

## Patterns Comparison

| Library | Boilerplate | Learning Curve | DevTools | Best For |
|---------|-------------|----------------|----------|----------|
| **Context** | Low | Low | React DevTools | Low-frequency global |
| **Zustand** | Minimal | Low | Yes | Simple global |
| **Redux TK** | Medium | Medium | Excellent | Complex, large apps |
| **Jotai** | Minimal | Medium | Yes | Atomic state |
| **XState** | High | High | Excellent | Complex flows |
| **React Query** | Low | Medium | Excellent | Server state |

---

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| **Global for local** | Unnecessary re-renders | Keep state local |
| **Prop drilling 10 levels** | Maintenance nightmare | Context or state lib |
| **Storing derived data** | Out of sync | Compute from source |
| **Mixing server/client state** | Complex sync | React Query for server |
| **Mutating state directly** | Bugs, no re-render | Immutable updates |
| **Giant store objects** | Performance issues | Split into slices |
