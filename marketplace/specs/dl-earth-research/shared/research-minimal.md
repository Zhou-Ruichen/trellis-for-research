# Research Minimal Code (Highest Priority)

On conflict with any other spec file, this one wins for exploratory work.

Goal: validate ideas and get experiments running. This is not production
code. Write the smallest change that answers the question; prefer one line
from an existing library over new code (see the reuse ladder in
[anti-bloat.md](./anti-bloat.md)).

In exploratory mode, do not add defensive code, boundary checks,
hash/checksum logic, exception handling, retries, unit tests, strict typing,
or abstractions unless the task names a concrete, likely failure that needs
one, or the user explicitly asks. In durable mode, apply the reliability the
component actually needs.

Before any verification step, answer two questions: what specific failure
would it catch, and what would you do differently once it finds one? If
there is no answer, do not add the check. A check earns its place only when
it replaces a clearly more expensive operation and its result changes the
next action.

Run and data manifests are written by the run-script template at retained
tier only; hash and checksum logic never appears scattered through
experiment code.

Stop condition: once the requested result is established and the mode's
sanity checks pass, the task is done. Do not seek additional certainty
without a concrete failure signal.
