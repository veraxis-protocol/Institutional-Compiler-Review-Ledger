# Required GitHub Repository Settings Before Activation

Repository: `veraxis-protocol/Institutional-Compiler-Review-Ledger`
Visibility: public
Default branch: `main`

Required before `ACCEPT_REVIEW_LEDGER_BOOTSTRAP`:

- Require pull request before merging.
- Require at least one approving review.
- Require CODEOWNERS review for protected infrastructure changes.
- Dismiss stale approvals on new commits.
- Require conversation resolution.
- Require status check: `mechanical-verification / verify` (exact rendered name to be confirmed after first run).
- Require linear history.
- Block force pushes.
- Block branch deletion.
- Do not enable a setting that equates merge with owner acceptance.
- Keep Actions workflow permissions read-only unless a separately owner-authorized workflow needs more.
- Keep mechanical verification secrets-free.
- Public visibility is explicitly authorized by owner decision `PUBLIC_VISIBILITY_OWNER_OVERRIDE_001`; any later visibility change requires a separate owner event.

Note: settings must be measured after configuration and captured in a bootstrap review record; this checklist is not evidence that GitHub has applied them.

- Public-disclosure gate: reject secrets, credentials, confidential/clearance-blocked material, and artifacts not explicitly releasable to the public ledger.
