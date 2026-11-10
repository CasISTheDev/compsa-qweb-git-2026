# Exercises

Do them in order. Each one ends with something you can check.

## 1. Fork and clone

1. Top right of this page on GitHub: **Fork** → **Create fork**. You now have your own copy.
2. On your fork: green **Code** button → copy the HTTPS link.
3. In a terminal:
   ```sh
   git clone <the link you copied>
   cd compsa-qweb-git-2026
   git status
   ```
**Check:** `git status` says `On branch main` and `nothing to commit, working tree clean`.

## 2. Make a branch

Never work straight on `main`. A branch is a safe copy you can throw away.

```sh
git switch -c add-<your-github-username>
```

**Check:** `git status` says `On branch add-<your-github-username>`.

## 3. Add yourself

1. Copy the template to a file named after your GitHub username:
   ```sh
   cp members/_template.md members/<your-github-username>.md
   ```
2. Open it and fill in the three lines. Keep the `---` lines.
3. Save it, then:
   ```sh
   git add members/<your-github-username>.md
   git commit -m "Add <your name> to the wall"
   ```

**Check:** `git log --oneline -1` shows your message.

## 4. Push and open a pull request

```sh
git push -u origin add-<your-github-username>
```

GitHub prints a link. Open it (or go to your fork and click **Compare & pull request**) and press **Create pull request**.

A check runs on your PR (the **Checks** tab). Green means your file is in the right shape. Red tells you what to fix: edit the file, `git add`, `git commit`, `git push` again, and the PR updates by itself.

**Check:** your PR shows a green check. When a QWeb exec merges it, you're on the wall.

## 5. Make a merge conflict (on purpose)

Conflicts happen when two branches change the same line. Make one so it's not scary later.

```sh
git switch main
git switch -c left
```
Open `conflict.txt`, change the line under `Favourite language:` to something, then:
```sh
git commit -am "left's answer"
git switch main
git switch -c right
```
Change the **same line** to something different, then:
```sh
git commit -am "right's answer"
git merge left
```
Git stops and says `CONFLICT`. Open `conflict.txt`. You'll see:
```
<<<<<<< HEAD
right's version
=======
left's version
>>>>>>> left
```
Delete the markers, keep the version you want (or both), save, then:
```sh
git add conflict.txt
git commit -m "Resolve the conflict"
```
**Check:** `git log --oneline --graph` shows the two branches joining.

## 6. Undo things

| Oops | Fix |
|---|---|
| Changed a file and want it back the way it was | `git restore <file>` |
| Ran `git add` on the wrong file | `git restore --staged <file>` |
| Typo in your last commit message (not pushed yet) | `git commit --amend -m "Better message"` |
| A commit that's already pushed was wrong | `git revert <commit-id>`: makes a new commit that undoes it. Safe on shared branches. |

Try one: add a line to `conflict.txt`, commit it, then `git revert HEAD`.

**Check:** the line is gone and `git log` shows both commits.

## When it goes wrong

- **`Permission denied` / `403` on push:** you cloned this repo, not your fork. Fork it, then `git remote set-url origin <your fork's link>`.
- **`Please tell me who you are`:** run the two `git config --global` lines from the README.
- **Push asks for a password:** GitHub wants a token, not your password. Easiest fix: install GitHub Desktop or run `gh auth login`.
- **Your PR check is red:** open **Details** on the check; it says exactly which line is wrong.
