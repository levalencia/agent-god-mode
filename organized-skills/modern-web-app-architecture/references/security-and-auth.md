# Security & Authentication for Web Apps

## Security Posture (Defaults)

Assume:
- **XSS is your #1 frontend risk** (it turns into account takeover if tokens are stealable).
- Security is a **system property**: frontend + backend + infrastructure.
- **Client-side “route guards” are UX**, not authorization. Enforce authorization on the server/API.

## Auth Strategies (Choose Intentionally)

### 1) Cookie-Based Sessions (Often Best for Browsers)

**How it works:** server sets a session cookie; browser sends it automatically.

**Recommended cookie flags:**
- `HttpOnly` (prevents JS access)
- `Secure` (HTTPS only)
- `SameSite=Lax` (or `Strict` if feasible; `None` requires `Secure`)

**Pros:** resistant to token theft via XSS (session id not readable by JS), simple browser ergonomics.  
**Cons:** you must handle **CSRF** when cookies are ambient authority.

### 2) Token-Based (SPA + API)

If you must use bearer tokens:
- Prefer **access token in memory** (short-lived) + **refresh token in httpOnly cookie**.
- Avoid long-lived bearer tokens stored in `localStorage` by default.

**Pros:** simple API auth, works well across services.  
**Cons:** bearer tokens are high-value; storage choices matter.

### 3) OAuth/OIDC (Public Clients)

For SPAs using OAuth/OIDC:
- Prefer **Authorization Code + PKCE**.
- Avoid the legacy “implicit flow”.

## CSRF (If Using Cookies)

Mitigations (combine):
- `SameSite=Lax/Strict` cookies
- CSRF token pattern (synchronizer token or double-submit)
- Require `Origin`/`Referer` checks for state-changing requests
- Use **idempotent** semantics correctly (GET must not mutate)

## XSS (Prevent + Limit Blast Radius)

### Prevention
- Treat all user content as untrusted.
- Avoid injecting raw HTML (`dangerouslySetInnerHTML`) unless strictly necessary.
- Sanitize user-generated HTML on the server (and again on the client if needed).
- Never build HTML with string concatenation from untrusted values.

### Blast Radius Reduction
- Adopt a strong **Content Security Policy (CSP)** (ideally without `unsafe-inline`).
- Consider **Trusted Types** to prevent DOM XSS sinks in large apps.
- Minimize third-party scripts; prefer self-hosting.

## Common Web Security Headers (Baseline)

Server-side headers to consider:
- `Content-Security-Policy` (script/style/img/connect/frame directives; add `frame-ancestors` as needed)
- `Strict-Transport-Security` (HSTS)
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy`
- `Permissions-Policy`

## Frontend Data Handling Rules of Thumb

- Don’t put secrets in the browser (API keys, private tokens).
- Be careful with **PII in URLs** (URLs leak via logs, referrers, screenshots).
- Keep auth state changes observable and reversible (logout clears caches, tabs, and storage).
- Prefer a **BFF (Backend-for-Frontend)** when it reduces CORS complexity, hides secrets, or simplifies aggregation.

## Minimal Auth/Session Checklist

- [ ] Auth enforced on server/API (not just client routing)
- [ ] Tokens not stored in `localStorage` by default
- [ ] CSP in place (and tested)
- [ ] CSRF mitigations if using cookies
- [ ] Logout clears relevant caches/state
- [ ] Error monitoring configured without leaking secrets/PII

