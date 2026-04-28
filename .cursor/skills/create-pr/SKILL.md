---
name: create-pr
description: >-
  Stages current-branch changes, commits with a clear message, pushes to origin,
  and opens a GitHub pull request to bluemarlins/MagicSquare_09 with a review-ready
  body (background, change type, summary, review notes). Use when the user types
  create-pr, /create-pr, asks to open a PR, or to add/commit/push and create a PR
  in one flow.
---

# Create PR (add → commit → GitHub PR)

## Repository defaults

- **Remote:** `origin` → `https://github.com/bluemarlins/MagicSquare_09`
- **PR base branch:** `main` (if the repo uses another default, detect via `git remote show origin` and use `HEAD branch`)

## Preconditions (verify before mutating git)

1. **`gh` CLI:** Run `gh auth status`. If not logged in, stop and sign in (`gh auth login`); do not guess tokens.
2. **Branch:** If the current branch is `main` (or the default production branch), warn the user that PRs usually come from a feature branch; only proceed if they confirm or they explicitly want a PR from that branch.
3. **Empty changes:** If there is nothing to commit after staging, stop and report—do not create an empty commit for a PR.

## Workflow (execute in order; use the project shell)

### 1. Inspect changes

- `git status`
- `git diff` (and `git diff --stat` if useful) for **tracked** changes.
- For **untracked** files: include them only if they clearly belong to this change set; otherwise list them and ask whether to add.

### 2. Stage

- Prefer staging **modified tracked files:** `git add -u` (or explicit paths from `git status` if safer).
- Add new files with `git add <path>` when the user’s intent includes new code/docs for this PR.

### 3. Commit message

- Use **Conventional Commits** when it fits: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `chore:`, etc.
- Subject line ≤ ~72 characters; imperative mood; Korean or English is fine if it matches the team—default to **Korean** for this project when unsure.
- Body optional; include rationale if the subject alone is insufficient.

### 4. Commit and push

- `git commit -m "<subject>"` (and `-m "<body>"` if needed).
- `git push -u origin HEAD` (first push for the branch). Retry with user direction if push rejects (e.g. non-fast-forward).

### 5. Pull request body (reviewer-oriented)

Build a Markdown body (Korean preferred) that includes at least:

| Section | Content |
|--------|---------|
| **배경** | Why this change exists (problem, ticket, or goal). |
| **변경 유형** | One or more: 신규 구현, 테스트 추가/변경, 버그 수정, 리팩터링, 문서, 설정/CI, 기타 (짧게 태그 형태로 가능). |
| **수정 요약** | Bullet list of what files/areas changed and behavior impact. |
| **리뷰 시 포인트** | What reviewers should check (edge cases, API contract, tests, risks). |
| **테스트** | How you verified (commands run, manual steps)—or “해당 없음” with reason. |

Use the structure in [pr-body-template.md](pr-body-template.md) as a starting point; adapt sections to the actual diff (omit empty sections).

### 6. Create PR via GitHub CLI

- Write the body to a temp file in the repo or OS temp dir, e.g. `.git-pr-body.md` (add to `.gitignore` only if the team already uses that pattern; otherwise delete the file after `gh pr create`).
- Run:

```bash
gh pr create --repo bluemarlins/MagicSquare_09 --base main --head "$(git branch --show-current)" --title "<PR title>" --body-file "<path-to-body.md>"
```

- Title should match the commit/change theme; can differ slightly for clarity.
- Print the **PR URL** from the command output to the user.

### 7. If `gh pr create` fails

- Parse the error (already exists, auth, branch not pushed, etc.).
- If a PR already exists for the branch: `gh pr view --web` or `gh pr list --head <branch>` and report the link instead of opening a duplicate.

## Do not

- Force-push or rewrite history unless the user explicitly asks.
- Commit secrets, `.env`, or credentials.
- Skip `git status` / diff review before staging.

## Optional: draft PR

If the user wants a draft: add `--draft` to `gh pr create`.
