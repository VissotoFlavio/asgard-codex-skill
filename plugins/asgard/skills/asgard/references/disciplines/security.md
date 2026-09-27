# Security discipline

Load this packet when an activity or review explicitly needs deep vulnerability analysis beyond Heimdall's proportional default review. Deep analysis is appropriate for externally exposed surfaces, authentication or authorization changes, sensitive data handling, unsafe parsing, SSRF-capable inputs, file upload, webhooks, rate limiting, gateway or middleware configuration, session handling, CORS, or user-requested vulnerability discovery.

## Optional specialist skills

Before dispatching Heimdall for deep analysis, record whether the relevant skills are available:

- `$api-security-review` for REST, GraphQL, gRPC, OpenAPI/Swagger, API gateways, webhooks, API authentication, authorization, rate limiting, or service-to-service API consumption.
- `$web-security-review` for web applications, server-rendered or server-side web code, sessions, browser trust boundaries, XSS/CSRF risk, security headers, CORS, framework configuration, or classic OWASP web risks.

If a relevant skill is unavailable, ask the user whether to install it before the deep review. Installing a skill is optional and requires explicit user authorization. If the user declines or installation is unavailable, continue with Heimdall's native review, record the fallback in required skills and residual risk, and do not claim the missing skill was applied.

## Review scope

Use deep analysis only for the bounded candidate, paths, contracts, and threat surfaces in the activity contract. Prefer credible exploit paths, negative tests, and prioritized remediation over exhaustive checklist output. Never expose secrets, personal data, live exploit details, or unnecessary operational information.
