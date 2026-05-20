# Decision: Keep Project Outside OneDrive

## Context

Windows 11 defaults to storing user files in `C:\Users\juliu\Documents`, which is automatically synced to OneDrive. This project uses a `.env` file containing live Anthropic API keys and any other credentials added in future phases.

## Decision

**Project lives at `C:\Users\juliu\Projects\Ai-Agents-Fluency`** — outside the OneDrive sync boundary.

## Reasoning

1. **Credentials shouldn't traverse cloud sync.** A `.env` file containing API keys uploaded to Microsoft's cloud is a credential exposure risk, even if OneDrive is private. Keys belong in local storage only.

2. **OneDrive–Python interaction has known friction.** OneDrive's background sync process can lock files mid-write, cause unexpected permission errors, and interfere with file watchers — all of which create unpredictable behavior during active development.

3. **The `.gitignore` backstop isn't enough.** `.gitignore` prevents keys from entering Git history but does nothing about OneDrive sync, which operates independently of Git.

## Revisit Condition

Move the project back under `Documents` (or another OneDrive-synced path) only if **both** conditions are true:

- OneDrive sync stops causing file-locking and permission friction with Python tooling, **and**
- Storing credentials in Microsoft's cloud becomes acceptable (e.g., project moves to secrets management and `.env` is no longer used for live keys).

## Files Affected

None. Project path is already correct. This record documents why it is where it is.
