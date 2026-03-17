# Architecture Decision Making

## First Law of Software Architecture

> **Everything in software architecture is a trade-off.**

There are no "right" answers, only least-worst combinations of trade-offs for your specific context.

## Architecture Characteristics

### Identifying Characteristics

Extract from requirements and domain:
- **Explicit:** "Must handle 10,000 concurrent users" → Scalability
- **Implicit:** Payment processing → Security (often unstated)
- **Translated:** "User satisfaction" → Performance, Availability

### Common Characteristics

| Category | Characteristic | Description |
|----------|----------------|-------------|
| **Operational** | Performance | Response time, throughput |
| | Scalability | Handle growth |
| | Availability | Uptime percentage |
| | Reliability | Mean time between failures |
| | Elasticity | Handle burst traffic |
| **Structural** | Modularity | Logical separation |
| | Maintainability | Ease of change |
| | Testability | Ease of verification |
| | Deployability | Release frequency |
| **Cross-cutting** | Security | Authentication, authorization |
| | Accessibility | WCAG compliance |
| | Legal | Privacy, compliance |

### Prioritization

**Pick 3-7 characteristics.** Supporting all characteristics equally is impossible—they conflict.

Common trade-offs:
- Performance vs Maintainability
- Security vs Usability
- Scalability vs Simplicity
- Flexibility vs Performance

---

## Architecture Decision Records (ADRs)

### Purpose

Document significant decisions:
- Create historical record
- Explain reasoning (the "why")
- Prevent revisiting same decisions
- Onboard new team members

### Template

```markdown
# ADR-001: Use React with TypeScript

## Status
Accepted

## Context
We need to choose a frontend framework for our new e-commerce platform.
Team has experience with React and Angular. Project requires:
- Complex state management
- Strong type safety
- Long-term maintainability

## Decision
We will use React with TypeScript.

## Consequences
### Positive
- Team expertise reduces ramp-up time
- Large ecosystem for e-commerce features
- TypeScript catches errors at compile time

### Negative
- More boilerplate than plain JavaScript
- Need to maintain type definitions
- Some libraries lack good TypeScript support

### Risks
- React ecosystem churn (mitigate: abstract framework specifics)

## Alternatives Considered
1. **Angular**: Full framework but steeper learning curve
2. **Vue**: Simpler but less team experience
3. **React + JavaScript**: Faster initial development but more runtime errors
```

---

## Coupling and Cohesion

### Coupling Types

**Static (Compile-time):**

| Type | Description | Example |
|------|-------------|---------|
| **Name** | Shared naming | Function calls |
| **Type** | Type agreement | Interface parameters |
| **Meaning** | Hard-coded values | Magic strings/numbers |
| **Position** | Parameter order | Function arguments |
| **Algorithm** | Shared algorithm | Hash functions |

**Dynamic (Runtime):**

| Type | Description | Example |
|------|-------------|---------|
| **Execution** | Order dependency | A before B |
| **Timing** | Time dependency | Race conditions |
| **Values** | Transaction scope | Atomic updates |
| **Identity** | Shared references | Same object instance |

### Coupling Guidelines

1. **Minimize overall coupling** by encapsulating
2. **Minimize coupling across boundaries** (modules, services)
3. **Maximize coupling within boundaries** (it's fine internally)

### Cohesion Spectrum

From best to worst:

1. **Functional:** Everything related, all essentials present
2. **Sequential:** Output → Input chains
3. **Communicational:** Operate on same data
4. **Procedural:** Order-dependent execution
5. **Temporal:** Run at same time
6. **Logical:** Logically related, different functions
7. **Coincidental:** No meaningful relationship

---

## Architecture Quantum

> An independently deployable artifact with high functional cohesion and synchronous connascence.

### Components

- **Independently deployable:** Includes everything needed to function
- **High functional cohesion:** Does something purposeful
- **Synchronous connascence:** Synchronous calls create coupling

### Significance

Analyze architecture characteristics per quantum, not system-wide.

Example:
```
System has 3 quanta:
- User Service (high availability)
- Order Service (strong consistency)
- Reporting Service (high performance)

Each quantum may need different architecture characteristics.
```

---

## Fitness Functions

### Definition

Any mechanism providing objective integrity assessment of architecture characteristics.

### Examples

**Cyclomatic Complexity:**
```javascript
// CI check: fail if CC > 10
const cc = analyzeComplexity(file);
if (cc > 10) {
  throw new Error(`Complexity ${cc} exceeds threshold`);
}
```

**Bundle Size:**
```javascript
// Fail build if bundle exceeds budget
const stats = require('./dist/stats.json');
const mainBundle = stats.assets.find(a => a.name.includes('main'));
if (mainBundle.size > 170000) {
  process.exit(1);
}
```

**Layer Dependencies:**
```javascript
// ArchUnit-style: presentation cannot import data layer
rules.push({
  from: 'src/components/**',
  disallow: ['src/data/**'],
  message: 'Components cannot directly access data layer'
});
```

**Performance:**
```javascript
// Lighthouse CI
module.exports = {
  ci: {
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'first-contentful-paint': ['error', { maxNumericValue: 2000 }],
      }
    }
  }
};
```

### Benefits

- Automate important-but-not-urgent concerns
- Enable continuous governance
- Fast feedback to developers
- Document constraints as code

---

## Top-Level Partitioning

### Technical Partitioning (Layered)

```
┌─────────────────────┐
│    Presentation     │
├─────────────────────┤
│   Business Logic    │
├─────────────────────┤
│    Data Access      │
├─────────────────────┤
│      Database       │
└─────────────────────┘
```

**Pros:**
- Clear separation of technical concerns
- Familiar pattern
- Easy to locate code by type

**Cons:**
- Domains cut across all layers
- Changes often touch multiple layers
- Difficult to scale independently

**Best for:** Simple applications, CRUD-heavy systems

### Domain Partitioning

```
┌─────────┬─────────┬─────────┐
│ Users   │ Orders  │Products │
│ ─────── │ ─────── │ ─────── │
│ UI      │ UI      │ UI      │
│ Logic   │ Logic   │ Logic   │
│ Data    │ Data    │ Data    │
└─────────┴─────────┴─────────┘
```

**Pros:**
- Aligns with business capabilities
- Independent development and deployment
- Easier team organization (Conway's Law)

**Cons:**
- Potential code duplication
- Requires good domain understanding
- Cross-cutting concerns need addressing

**Best for:** Complex domains, multiple teams

---

## Conway's Law

> Organizations which design systems are constrained to produce designs which are copies of the communication structures of those organizations.

### Inverse Conway Maneuver

Structure teams to promote desired architecture:

**Want microservices?** Create small, cross-functional teams aligned to business domains.

**Want modular monolith?** Organize by feature teams with clear interfaces.

---

## Architecture Anti-patterns

| Anti-pattern | Description | Solution |
|--------------|-------------|----------|
| **Architecture Sinkhole** | Requests pass through layers without processing | Add value at each layer or simplify |
| **Vendor King** | Architecture dictated by vendor | Abstract vendor specifics |
| **Groundhog Day** | Revisiting same decisions | Document in ADRs |
| **Email-Driven** | Decisions scattered in emails | Centralize in ADRs |
| **Frozen Caveman** | Outdated expertise believed current | Continuous learning |
| **Golden Hammer** | One solution for all problems | Match tool to problem |

---

## Decision Framework

### Step 1: Identify Characteristics
- What does the business need?
- What are implicit requirements?
- Prioritize top 3-7

### Step 2: Determine Scope
- How many architecture quanta?
- What are their boundaries?
- Different characteristics per quantum?

### Step 3: Choose Partitioning
- Technical (simple, familiar)
- Domain (scalable, team-aligned)

### Step 4: Select Style
- Monolith vs distributed?
- Which pattern fits characteristics?
- What trade-offs are acceptable?

### Step 5: Document Decisions
- Write ADRs
- Implement fitness functions
- Review and update

---

## Architect Responsibilities

1. **Make architecture decisions** (guide, don't dictate)
2. **Analyze architecture continuously** (identify decay)
3. **Stay current with trends** (technical breadth)
4. **Ensure compliance** (fitness functions)
5. **Understand business domain** (speak stakeholder language)
6. **Navigate politics** (negotiate trade-offs)

---

## Practical Trade-off Analysis

### Framework

For each decision:

1. **List options** (usually 2-4 realistic choices)
2. **Identify criteria** (from architecture characteristics)
3. **Score each option** (1-5 per criterion)
4. **Weight criteria** (not all equal importance)
5. **Calculate weighted scores**
6. **Document reasoning** (ADR)

### Example: State Management Choice

| Criterion | Weight | Context | Redux | Zustand |
|-----------|--------|---------|-------|---------|
| Simplicity | 3 | 5 | 2 | 4 |
| Scalability | 4 | 3 | 5 | 3 |
| DevTools | 2 | 3 | 5 | 4 |
| Bundle Size | 3 | 5 | 2 | 5 |
| **Weighted** | | **47** | **42** | **48** |

Decision: Zustand for this project (but document why Redux might be better for larger teams or more complex state).
