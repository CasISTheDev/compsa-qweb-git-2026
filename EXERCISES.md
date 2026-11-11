# Exercises

These follow the slides. Each heading matches the title on screen, so if you fall behind,
find the slide's name here and pick up from there. Each one ends with something you can check.

The first half of the workshop happens in your own repo, `git-practice`. This repo starts at
**Pull Requests**.

Everywhere you see `<you>`, type your GitHub username. The slides fill it in for you.

## Pull Requests

Everyone in the room adds one file to this repo. Merged, and you're on the wall.

1. Top right of this page: **Fork** → **Create fork**. That's your own copy, on GitHub.
2. Paste **part 1** in your terminal. It downloads your copy, makes a branch, and copies the template:
   ```sh
   cd ~
   git clone https://github.com/<you>/compsa-qweb-git-2026.git
   cd compsa-qweb-git-2026
   git switch -c add-<you>
   cp members/_template.md members/<you>.md
   ```
3. Open `members/<you>.md` and fill in the three lines. Keep the `---` lines.
4. Save it, then paste **part 2**:
   ```sh
   git add .
   git commit -m "Add <you> to the wall"
   git push -u origin add-<you>
   ```
5. On your fork, click **Compare & pull request** → **Create pull request**.

A check runs on your pull request. Green means your file is right. Red tells you exactly what
to fix: fix it, then `git add`, `git commit`, `git push`, and the check runs again on its own.

**Check:** your pull request shows a green check. When a QWeb exec merges it, you're on
[the wall](https://queens-web-development-club.github.io/compsa-qweb-git-2026/).

## Conflicts

A conflict is Git asking you a question: two changes hit the same line, so which one do you
want? Make one on purpose, in your fork.

1. Go back to `main`, where your fork's `conflict.txt` lives:
   ```sh
   git switch main
   ```
2. **On GitHub:** open `conflict.txt` in your fork, click the pencil, change `(change this line)`
   to one language, and click **Commit changes**.
3. **In VS Code:** open `conflict.txt` and change the same line to a different language. Save, then:
   ```sh
   git add conflict.txt
   git commit -m "My favourite language"
   git pull
   ```
4. Git says `CONFLICT`. Open `conflict.txt`. You'll see:
   ```
   <<<<<<< HEAD
   your version
   =======
   GitHub's version
   >>>>>>> ...
   ```
   Pick one: yours, GitHub's, or both. Delete the three marker lines. Save.
5. Finish it:
   ```sh
   git add conflict.txt
   git commit -m "Pick a favourite language"
   git push
   ```

**Check:** `git log --oneline --graph` shows two lines joining into one.
Panic button, any time during a conflict: `git merge --abort`.

## Undo Anything

What went wrong? Find it, type the fix.

| What went wrong | Type this |
|---|---|
| I messed up a file and haven't committed | `git restore <file>` |
| I ran `git add` on the wrong file | `git restore --staged <file>` |
| My last commit note has a typo, and I haven't pushed | `git commit --amend -m "A better note"` |
| My last commit broke things, and I already pushed | `git revert --no-edit HEAD`, then `git push` |
| I just want to see an old version | `git log --oneline`, then `git show <code>` |

Amend only before you push. Once it's pushed, revert instead: it adds a new commit that does
the opposite, so nobody's history gets rewritten.

**Try it:** wipe everything in `conflict.txt` and save. Then `git restore conflict.txt`.
**Check:** it's back.

## Keep It Out

Not everything belongs in Git: secrets, people's data, huge files, generated files.
Do this one on `main`, not on your `add-` branch, so your pull request stays just your one file.

1. Make a fake secret:
   ```sh
   git switch main
   echo "API_KEY=not-a-real-key" > .env
   git status
   ```
   Git sees `.env` and wants to track it.
2. Open `.gitignore` (make it if it isn't there), add a line that says `.env`, and save.
3. Run `git status` again.

**Check:** `.env` is gone from the list, and only `.gitignore` shows up. Commit that.
Pushed a key by accident? Change the key. Git's history remembers it.

## When it goes wrong

- **`Permission denied` / `403` on push:** you cloned this repo, not your fork. Fork it, then `git remote set-url origin <your fork's link>`.
- **`Please tell me who you are`:** run the two `git config --global` lines from the README.
- **Push asks for a password:** GitHub wants a token, not your password. Easiest fix: install GitHub Desktop or run `gh auth login`.
- **Your check is red:** open **Details** on the check. It says exactly what to fix.
- **Your check says it's waiting for approval:** GitHub holds checks for brand new accounts. Put your hand up and an exec will approve it.
- **A screen full of `~` lines after `git commit`:** that's an editor called Vim. Press `Esc`, type `:q!`, press `Enter`, then commit again with `-m "your note"`.
