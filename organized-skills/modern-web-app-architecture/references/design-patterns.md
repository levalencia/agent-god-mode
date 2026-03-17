# JavaScript Design Patterns

## Overview

Design patterns are proven solutions to common software problems. Modern JavaScript (ES2015+) has changed how many classic patterns are implemented.

## Pattern Categories

### Creational Patterns
Create objects in manner suitable to the situation.

### Structural Patterns
Compose objects into larger structures.

### Behavioral Patterns
Communication between objects.

---

## Module Pattern

**Purpose:** Encapsulate code with public/private access.

**Modern Implementation (ES Modules):**
```javascript
// basket.js
const basket = []; // private

export const addItem = (item) => basket.push(item);
export const getCount = () => basket.length;
export const getTotal = () => basket.reduce((sum, item) => sum + item.price, 0);
```

**When to Use:**
- Organizing code into logical units
- Hiding implementation details
- Creating clear public APIs

---

## Singleton Pattern

**Purpose:** Ensure only one instance exists globally.

**ES Module Implementation:**
```javascript
// config.js - modules are singletons by default
let instance;
const config = { theme: 'dark', locale: 'en' };

export const getConfig = () => config;
export const setConfig = (key, value) => { config[key] = value; };
```

**When to Use:**
- Application configuration
- Logger instances
- Database connections

**Caution:** In React, prefer Context or state management over singletons for better testability.

---

## Factory Pattern

**Purpose:** Create objects without specifying exact class.

```javascript
class VehicleFactory {
  create(type, options) {
    const vehicles = {
      car: Car,
      truck: Truck,
      motorcycle: Motorcycle
    };
    const Vehicle = vehicles[type];
    return Vehicle ? new Vehicle(options) : null;
  }
}

// Usage
const factory = new VehicleFactory();
const car = factory.create('car', { color: 'red' });
```

**When to Use:**
- Object creation logic is complex
- Type determined at runtime
- Decoupling code from specific classes

---

## Observer Pattern

**Purpose:** Object (subject) maintains list of dependents (observers) and notifies them of changes.

```javascript
class EventEmitter {
  constructor() {
    this.events = {};
  }

  on(event, listener) {
    (this.events[event] ||= []).push(listener);
    return () => this.off(event, listener);
  }

  off(event, listener) {
    this.events[event] = this.events[event]?.filter(l => l !== listener);
  }

  emit(event, data) {
    this.events[event]?.forEach(listener => listener(data));
  }
}
```

**When to Use:**
- Event-driven architectures
- Decoupling components
- Real-time updates

**React Equivalent:** Custom hooks with subscription patterns, or RxJS for complex streams.

---

## Publish/Subscribe Pattern

**Purpose:** Like Observer, but with intermediate event channel (more decoupled).

```javascript
class PubSub {
  constructor() {
    this.topics = {};
  }

  subscribe(topic, handler) {
    (this.topics[topic] ||= []).push(handler);
    return () => {
      this.topics[topic] = this.topics[topic].filter(h => h !== handler);
    };
  }

  publish(topic, data) {
    this.topics[topic]?.forEach(handler => handler(data));
  }
}
```

**Difference from Observer:** Publishers don't know subscribers exist. Complete decoupling.

---

## Mediator Pattern

**Purpose:** Centralize complex communications between objects.

```javascript
class ChatRoom {
  constructor() {
    this.users = {};
  }

  register(user) {
    this.users[user.name] = user;
    user.chatroom = this;
  }

  send(message, from, to) {
    if (to) {
      this.users[to]?.receive(message, from);
    } else {
      // Broadcast
      Object.keys(this.users)
        .filter(name => name !== from)
        .forEach(name => this.users[name].receive(message, from));
    }
  }
}
```

**When to Use:**
- Complex component interactions
- Reducing direct dependencies
- Centralizing business logic

**Modern Example:** Express.js middleware chain is a mediator pattern.

---

## Decorator Pattern

**Purpose:** Add behavior to objects dynamically without affecting other instances.

```javascript
// Functional approach
const withLogging = (fn) => (...args) => {
  console.log(`Calling with:`, args);
  const result = fn(...args);
  console.log(`Result:`, result);
  return result;
};

const add = (a, b) => a + b;
const loggedAdd = withLogging(add);
loggedAdd(2, 3); // Logs: Calling with: [2, 3], Result: 5
```

**Class Decorator (wrapping):**
```javascript
class Coffee {
  cost() { return 5; }
}

class WithMilk {
  constructor(coffee) { this.coffee = coffee; }
  cost() { return this.coffee.cost() + 1; }
}

const latte = new WithMilk(new Coffee());
latte.cost(); // 6
```

**React Equivalent:** Higher-Order Components (HOCs), though hooks are now preferred.

---

## Facade Pattern

**Purpose:** Provide simplified interface to complex subsystem.

```javascript
// Complex subsystems
class VideoDecoder { /* ... */ }
class AudioDecoder { /* ... */ }
class SubtitleLoader { /* ... */ }
class DisplayRenderer { /* ... */ }

// Facade
class VideoPlayer {
  constructor() {
    this.video = new VideoDecoder();
    this.audio = new AudioDecoder();
    this.subs = new SubtitleLoader();
    this.display = new DisplayRenderer();
  }

  play(file) {
    const video = this.video.decode(file);
    const audio = this.audio.decode(file);
    const subs = this.subs.load(file);
    this.display.render(video, audio, subs);
  }
}
```

**When to Use:**
- Simplifying complex APIs
- Creating library interfaces
- Hiding implementation complexity

---

## Proxy Pattern

**Purpose:** Placeholder object controlling access to another object.

```javascript
const handler = {
  get(target, prop) {
    console.log(`Accessing ${prop}`);
    return target[prop];
  },
  set(target, prop, value) {
    console.log(`Setting ${prop} to ${value}`);
    target[prop] = value;
    return true;
  }
};

const user = new Proxy({ name: 'John' }, handler);
user.name; // Logs: Accessing name
user.age = 30; // Logs: Setting age to 30
```

**Use Cases:**
- Validation
- Logging/profiling
- Lazy initialization
- Access control

---

## Flyweight Pattern

**Purpose:** Share common data between similar objects to minimize memory.

**DOM Example (Event Delegation):**
```javascript
// Instead of attaching listener to each button
document.querySelectorAll('button').forEach(btn => {
  btn.addEventListener('click', handleClick); // Bad: many handlers
});

// Use event delegation (flyweight)
document.body.addEventListener('click', (e) => {
  if (e.target.matches('button')) {
    handleClick(e); // Good: one handler
  }
});
```

**When to Use:**
- Many similar objects
- Shared immutable data
- DOM event handling

---

## Strategy Pattern

**Purpose:** Define family of algorithms, encapsulate each, make them interchangeable.

```javascript
const strategies = {
  credit: (amount) => amount * 1.02,    // 2% fee
  paypal: (amount) => amount * 1.03,    // 3% fee
  crypto: (amount) => amount * 1.01,    // 1% fee
};

const processPayment = (amount, method) => {
  const strategy = strategies[method];
  if (!strategy) throw new Error(`Unknown method: ${method}`);
  return strategy(amount);
};

processPayment(100, 'credit'); // 102
```

**When to Use:**
- Multiple algorithms for same task
- Runtime algorithm selection
- Avoiding large conditionals

---

## Command Pattern

**Purpose:** Encapsulate request as object, enabling parameterization and queuing.

```javascript
class Command {
  execute() { throw new Error('Override me'); }
  undo() { throw new Error('Override me'); }
}

class AddTextCommand extends Command {
  constructor(editor, text) {
    super();
    this.editor = editor;
    this.text = text;
  }

  execute() {
    this.editor.content += this.text;
  }

  undo() {
    this.editor.content = this.editor.content.slice(0, -this.text.length);
  }
}

// Command invoker with history
class Editor {
  constructor() {
    this.content = '';
    this.history = [];
  }

  execute(command) {
    command.execute();
    this.history.push(command);
  }

  undo() {
    this.history.pop()?.undo();
  }
}
```

**When to Use:**
- Undo/redo functionality
- Transaction logging
- Task queuing

---

## Loading Patterns

### Dynamic Import (Import on Interaction)
```javascript
button.addEventListener('click', async () => {
  const { sortBy } = await import('lodash-es');
  const sorted = sortBy(data, 'name');
});
```

### Import on Visibility
```javascript
const observer = new IntersectionObserver(async (entries) => {
  if (entries[0].isIntersecting) {
    const { Chart } = await import('chart.js');
    new Chart(canvas, config);
    observer.disconnect();
  }
});
observer.observe(chartContainer);
```

---

## Pattern Selection Guide

| Problem | Pattern |
|---------|---------|
| Need single global instance | Singleton (or ES Module) |
| Object creation is complex | Factory |
| Need to notify many objects of changes | Observer/Pub-Sub |
| Complex object interactions | Mediator |
| Add behavior without modifying class | Decorator |
| Simplify complex subsystem | Facade |
| Control access to object | Proxy |
| Many similar objects, memory concern | Flyweight |
| Multiple interchangeable algorithms | Strategy |
| Need undo/redo capability | Command |
