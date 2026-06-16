# Git Hub Command and Steps

## For creating, update and commit in repository

### 1. Open Terminal in VS Code

Open project folder in VS Code, then:

**Terminal → New Terminal**

### 2. Initialize Git (if not already)

```bash
git init
```

### 3. Add all files

```bash
git add .
```

### 4. Create first commit

```bash
git commit -m "Initial commit"
```

### 5. Create a repository on GitHub

Go to:

[GitHub](https://github.com/bughunter-sks/)

* Click **New Repository**
* Enter repository name
* Click **Create Repository**
* Do **not** initialize with README if your local project already exists

### 6. Connect local project to GitHub

Copy the repository URL and run:

```bash
git remote add origin https://github.com/bughunter-sks/my-tds-tools.git
```

Example:

```bash
git remote add origin https://github.com/bughunter-sks/my-tds-tools.git
```

### 7. Push code

For a new repository:

```bash
git branch -M main
git push -u origin main
```

GitHub may prompt to authenticate using browser or a Personal Access Token.

### Verify

Check the remote:

```bash
git remote -v
```
![alt text](/assets/image-01.png)

Check status:

```bash
git status
```

For future updates, use:

```bash
git add .
git commit -m "Describe changes"
git push
```

### One-shot command sequence

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/bughunter-sks/my-tds-tools.git
git push -u origin main
```
