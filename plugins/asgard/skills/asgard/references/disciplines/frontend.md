# Frontend discipline

Load this packet for an activity that owns a user-visible web interface, interaction, responsive layout, or interface copy. It supplements Brokkr or Sindri; it does not replace the implementer's role packet or create shared ownership.

## Design capability

For a new interface or material visual redesign, require `$frontend-design` in the activity contract and confirm that it is available before dispatch. The implementer must use it before coding to ground the direction in the product, audience, and page objective; define deliberate color, type, layout, and one restrained signature element; critique generic choices; and build from the revised plan.

For a localized change that must preserve an established design system, use `$frontend-design` only when a new visual decision is necessary. Existing repository conventions and the user's explicit brief take precedence. Do not add fonts, packages, generated media, or other dependencies without authorization.

Include affected responsive states, keyboard focus, reduced motion, loading, empty, error, and action-copy behavior in the DoD. Require visual evidence at relevant desktop and mobile viewports when the environment can render the interface; record why when meaningful visual validation is unavailable.

## Independent interface gate

For a stable candidate that materially changes UI code or behavior, require an independent read-only reviewer using `$web-design-guidelines`. The reviewer must fetch the current guideline source required by that skill, inspect the exact owned files or candidate diff, and report findings in its terse `file:line` format. Return `APPROVED` only when no actionable finding remains; otherwise return `CHANGES_REQUIRED` and route findings through Odin to the original implementer.

The implementer must not perform or approve this gate. If the skill, current guideline source, affected files, or meaningful rendered evidence is unavailable, report the missing evidence; do not silently substitute a stale review. Odin may approve a proportional fallback only within the user-approved graph.
