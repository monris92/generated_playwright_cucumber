# Git Workflow Guide

Panduan lengkap untuk bekerja dengan Git di project ini.

---

## 📋 Table of Contents

- [Branch Strategy](#branch-strategy)
- [Daily Workflow](#daily-workflow)
- [Merge ke Main](#merge-ke-main)
- [Resolve Conflicts](#resolve-conflicts)
- [Common Commands](#common-commands)
- [Best Practices](#best-practices)

---

## 🌳 Branch Strategy

### Branch Types:
- **`main`** - Production-ready code, stable version
- **`endri`** (atau nama developer) - Development branch, tempat kerja sehari-hari
- **Feature branches** - Untuk fitur spesifik (optional)

### Branch Naming Convention:
```
feature/nama-fitur     # Untuk fitur baru
bugfix/nama-bug        # Untuk perbaikan bug
hotfix/nama-hotfix     # Untuk urgent fix di production
```

---

## 🚀 Daily Workflow

### 1. Mulai Kerja (Setiap Hari)

```bash
# Pastikan di branch kerja
git checkout endri

# Pull perubahan terbaru dari remote
git pull origin endri

# (Optional) Sync dengan main jika ada update
git fetch origin main
git merge origin/main
```

### 2. Selama Kerja

```bash
# Cek status perubahan
git status

# Lihat perubahan yang sudah dibuat
git diff

# Add file yang sudah diubah
git add .                          # Add semua file
git add file1.py file2.py         # Add file spesifik

# Commit dengan pesan yang jelas
git commit -m "feat: add category feature to recorder"
git commit -m "fix: resolve syntax error in test file"
git commit -m "docs: update README with new instructions"
```

### 3. Push ke Remote (Backup & Share)

```bash
# Push perubahan ke remote branch
git push origin endri

# Jika ada error "rejected", pull dulu
git pull origin endri --rebase
git push origin endri
```

---

## 🔀 Merge ke Main

### Method 1: Pull Request (Recommended ✅)

#### Step 1: Persiapan di Branch Kerja
```bash
# Pastikan di branch endri
git checkout endri

# Pull latest dari endri
git pull origin endri

# Commit semua perubahan
git add .
git commit -m "Your changes description"

# Push ke remote
git push origin endri
```

#### Step 2: Sync dengan Main (Hindari Conflict)
```bash
# Fetch latest main
git fetch origin main

# Merge main ke branch kerja
git merge origin/main

# Jika ada conflict, resolve dulu (lihat section Resolve Conflicts)
# Setelah resolve:
git add .
git commit -m "Merge main into endri"
git push origin endri
```

#### Step 3: Create Pull Request
1. Buka **GitHub** → Repository
2. Klik **"Pull requests"** tab
3. Klik **"New pull request"**
4. Set:
   - Base: `main`
   - Compare: `endri`
5. Review changes yang akan di-merge
6. Klik **"Create pull request"**
7. Tambahkan:
   - **Title**: Ringkasan perubahan
   - **Description**: Detail perubahan, testing yang sudah dilakukan
8. Klik **"Create pull request"**

#### Step 4: Review & Merge
1. Review code (atau minta tim review)
2. Jika ada feedback:
   ```bash
   # Fix di branch endri
   git add .
   git commit -m "Address review feedback"
   git push origin endri
   # PR akan auto-update
   ```
3. Setelah approved, di GitHub:
   - Klik **"Merge pull request"**
   - Pilih merge strategy:
     - **Create a merge commit** (keep full history)
     - **Squash and merge** (combine all commits)
     - **Rebase and merge** (linear history)
   - Klik **"Confirm merge"**

#### Step 5: Cleanup
```bash
# Update local main
git checkout main
git pull origin main

# Back to branch kerja
git checkout endri
git pull origin endri

# (Optional) Delete feature branch jika sudah tidak dipakai
# Soft delete - hanya jika sudah merged
git branch -d feature/old-feature
git push origin --delete feature/old-feature

# Force delete - jika branch tidak perlu di-merge
git branch -D feature/old-feature
git push origin --delete feature/old-feature
```

---

### Method 2: Direct Merge (Solo Project Only)

⚠️ **Hanya untuk solo project atau urgent hotfix**

```bash
# Update main lokal
git checkout main
git pull origin main

# Merge branch kerja ke main
git merge endri

# Jika ada conflict, resolve dulu
# Setelah clean:
git push origin main

# Back to branch kerja
git checkout endri
```

---

## 🔧 Resolve Conflicts

### Ketika Muncul Conflict:

```bash
# Git akan show conflict files
git status

# Output example:
# both modified:   simple_recorder.py
# both modified:   run_tests_interactive.py
```

### Cara Resolve:

1. **Buka file yang conflict** di editor
2. Cari marker conflict:
   ```python
   <<<<<<< HEAD
   # Your changes
   self.category = None
   =======
   # Changes from main
   self.folder = None
   >>>>>>> main
   ```

3. **Edit file** - pilih mana yang mau dipakai:
   ```python
   # Keep both
   self.category = None
   self.folder = None
   
   # Or keep one
   self.category = None
   ```

4. **Hapus marker** (`<<<<<<<`, `=======`, `>>>>>>>`)

5. **Stage resolved files**:
   ```bash
   git add simple_recorder.py
   git add run_tests_interactive.py
   ```

6. **Commit merge**:
   ```bash
   git commit -m "Resolve merge conflicts"
   git push origin endri
   ```

### Tools untuk Resolve Conflict:
```bash
# Using VS Code
code simple_recorder.py

# Using merge tool
git mergetool

# Abort merge jika mau cancel
git merge --abort
```

---

## 📝 Common Commands

### Status & Info
```bash
git status                    # Lihat status perubahan
git log --oneline -10        # Lihat 10 commit terakhir
git log --graph --all        # Lihat commit graph
git diff                     # Lihat perubahan yang belum di-stage
git diff --staged            # Lihat perubahan yang sudah di-stage
git branch                   # Lihat semua branch lokal
git branch -a                # Lihat semua branch (lokal + remote)
```

### Branch Management
```bash
git checkout endri           # Switch ke branch endri
git checkout -b new-feature  # Create dan switch ke branch baru
git branch -d old-feature    # Delete branch lokal (jika sudah merged)
git branch -D old-feature    # Force delete branch lokal (unmerged)
git push origin --delete old # Delete branch remote
```

### Undo Changes
```bash
git restore file.py          # Undo perubahan file (belum di-stage)
git restore --staged file.py # Unstage file
git reset HEAD~1             # Undo last commit (keep changes)
git reset --hard HEAD~1      # Undo last commit (discard changes)
git revert abc123            # Revert specific commit
```

### Stash (Simpan Temporary)
```bash
git stash                    # Simpan perubahan sementara
git stash list               # Lihat daftar stash
git stash pop                # Apply dan hapus stash terakhir
git stash apply              # Apply stash tanpa hapus
git stash drop               # Hapus stash terakhir
```

### Remote Management
```bash
git remote -v                # Lihat remote URLs
git fetch origin             # Download remote changes (no merge)
git pull origin endri        # Fetch + merge
git push origin endri        # Push ke remote
git push --force-with-lease  # Force push (aman)
```

---

## ✅ Best Practices

### 1. Commit Messages
**Format:**
```
<type>: <description>

[optional body]
[optional footer]
```

**Types:**
- `feat:` - Fitur baru
- `fix:` - Bug fix
- `docs:` - Dokumentasi
- `style:` - Format, tidak mengubah logic
- `refactor:` - Refactor code
- `test:` - Tambah/update tests
- `chore:` - Maintenance tasks

**Examples:**
```bash
git commit -m "feat: add category selection in recorder"
git commit -m "fix: resolve syntax error in advance_search test"
git commit -m "docs: update git workflow guide"
git commit -m "refactor: simplify test runner logic"
git commit -m "test: add unit tests for recorder"
```

### 2. Commit Frequency
- ✅ Commit small, logical changes
- ✅ Commit working code
- ❌ Jangan commit broken code
- ❌ Jangan commit terlalu banyak changes sekaligus

### 3. Before Push
```bash
# Selalu test dulu sebelum push
python3 -m pytest
python3 simple_recorder.py  # Test if runs

# Cek perubahan
git diff

# Pastikan commit message jelas
git log --oneline -5
```

### 4. Branch Hygiene
- Keep branch up-to-date dengan main
- Delete branch yang sudah di-merge
- Don't work directly on main
- Use descriptive branch names

### 5. Pull Request
- Write clear PR title & description
- Explain WHY, not just WHAT
- Reference issue numbers jika ada
- Request review dari tim
- Respond to feedback promptly

### 6. Conflict Prevention
```bash
# Regularly sync dengan main
git fetch origin main
git merge origin/main

# Communicate dengan tim
# Avoid working on same files simultaneously
```

---

## 🆘 Common Issues & Solutions

### Issue 1: "Rejected - Non-Fast-Forward"
```bash
# Solution: Pull first, then push
git pull origin endri --rebase
git push origin endri
```

### Issue 2: "Divergent Branches"
```bash
# Solution: Specify strategy
git pull --rebase origin endri
# or
git pull --no-rebase origin endri
```

### Issue 3: Accidentally Committed to Main
```bash
# Move commits to branch
git branch endri              # Create branch from current state
git reset --hard origin/main  # Reset main to remote
git checkout endri            # Switch to new branch
```

### Issue 4: Need to Undo Last Commit
```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes and commit
git reset --hard HEAD~1
```

### Issue 5: Lost Changes
```bash
# Check reflog
git reflog

# Restore from reflog
git checkout <commit-hash>
git checkout -b recovery-branch
```

### Issue 6: Cannot Delete Branch (Not Fully Merged)
```bash
# Error message:
# "error: the branch 'branch-name' is not fully merged"

# Check if branch is really needed
git log branch-name --oneline -5

# If sure to delete (changes not needed)
git branch -D branch-name              # Force delete local
git push origin --delete branch-name   # Delete remote

# Alternative: Merge first, then delete
git checkout main
git merge branch-name
git branch -d branch-name  # Now safe to delete
```

---

## 📚 Additional Resources

- [Git Official Documentation](https://git-scm.com/doc)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Oh Shit, Git!?!](https://ohshitgit.com/) - Common mistakes & fixes

---

## 🎯 Quick Reference Card

```bash
# Daily workflow
git checkout endri → git pull → work → git add . → git commit -m "msg" → git push

# Merge to main (PR method)
git checkout endri → git pull → git merge origin/main → resolve conflicts → 
git push → Create PR on GitHub → Review → Merge

# Emergency rollback
git revert <commit-hash> → git push

# See what changed
git diff                    # Uncommitted changes
git diff --staged          # Staged changes
git log -p                 # Committed changes with diff
```

---

**Last Updated:** December 8, 2025
