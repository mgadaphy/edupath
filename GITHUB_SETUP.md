# GitHub Setup Guide for EduPath

This guide will walk you through setting up GitHub for the EduPath project, including repository initialization, branch management, and CI/CD pipeline configuration.

## Table of Contents

1. [Initial Setup](#initial-setup)
2. [GitHub Repository Creation](#github-repository-creation)
3. [Local Repository Setup](#local-repository-setup)
4. [Branch Strategy](#branch-strategy)
5. [GitHub Actions Setup](#github-actions-setup)
6. [GitHub Pages Deployment](#github-pages-deployment)
7. [Collaboration Guidelines](#collaboration-guidelines)

## Initial Setup

1. **Install Git**
   - Download and install Git from [git-scm.com](https://git-scm.com/)
   - Configure your Git username and email:
     ```bash
     git config --global user.name "Your Name"
     git config --global user.email "your.email@example.com"
     ```

2. **Set up SSH Key** (recommended)
   - Generate a new SSH key:
     ```bash
     ssh-keygen -t ed25519 -C "your.email@example.com"
     ```
   - Add the SSH key to your GitHub account:
     1. Copy the public key: `cat ~/.ssh/id_ed25519.pub`
     2. Go to GitHub → Settings → SSH and GPG keys → New SSH key
     3. Paste your public key and save

## GitHub Repository Creation

1. **Create a new repository**
   - Go to [GitHub](https://github.com/new)
   - Enter "edupath" as the repository name
   - Add a description: "AI-powered educational guidance system for Cameroonian students"
   - Choose "Public" or "Private" as needed
   - Initialize with a README (optional, as we already have one)
   - Add .gitignore: Node, Python
   - Choose MIT License
   - Click "Create repository"

## Local Repository Setup

1. **Initialize Git** (if not already done)
   ```bash
   cd /path/to/edupath
   git init
   ```

2. **Add remote repository**
   ```bash
   git remote add origin git@github.com:yourusername/edupath.git
   ```

3. **Create .gitignore file** (if not already created)
   Create a `.gitignore` file with these contents:
   ```
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   build/
   develop-eggs/
   dist/
   downloads/
   eggs/
   .eggs/
   lib/
   lib64/
   parts/
   sdist/
   var/
   wheels/
   *.egg-info/
   .installed.cfg
   *.egg
   .venv
   venv/
   env/
   .env
   .python-version

   # Node
   node_modules/
   npm-debug.log
   yarn-debug.log
   yarn-error.log
   .pnp
   .pnp.js
   .yarn-integrity
   .next/
   out/
   .nuxt/
   dist/
   .cache/
   .vuepress/dist
   .svelte-kit
   .DS_Store

   # IDE
   .idea/
   .vscode/
   *.swp
   *.swo
   *~
   
   # Docker
   .docker/
   *.tar.gz
   
   # Local development
   .env.local
   .env.development.local
   .env.test.local
   .env.production.local
   ```

4. **Initial commit**
   ```bash
   git add .
   git commit -m "Initial commit: Project setup with FastAPI backend and React frontend"
   git branch -M main
   git push -u origin main
   ```

## Branch Strategy

We follow the [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/) branching model:

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features being developed
- `bugfix/*` - Bug fixes
- `release/*` - Release preparation
- `hotfix/*` - Critical production fixes

**Example workflow:**
```bash
# Create a new feature branch
git checkout -b feature/user-authentication develop

# Make your changes and commit
git add .
git commit -m "Add user authentication with JWT"

# Push to remote
git push -u origin feature/user-authentication

# Create a pull request from GitHub UI to merge into develop
```

## GitHub Actions Setup

1. **Create workflow directory**
   ```bash
   mkdir -p .github/workflows
   ```

2. **Create Python CI workflow** (`.github/workflows/python-ci.yml`):
   ```yaml
   name: Python CI

   on:
     push:
       branches: [ main, develop ]
     pull_request:
       branches: [ main, develop ]

   jobs:
     test:
       runs-on: ubuntu-latest
       services:
         postgres:
           image: postgres:13
           env:
             POSTGRES_USER: postgres
             POSTGRES_PASSWORD: postgres
             POSTGRES_DB: test_db
           ports:
             - 5432:5432
           options: >-
             --health-cmd pg_isready
             --health-interval 10s
             --health-timeout 5s
             --health-retries 5
       
       steps:
       - uses: actions/checkout@v3
       - name: Set up Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.10'
       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           pip install -r requirements.txt
       - name: Run tests
         env:
           DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
         run: |
           pytest
   ```

3. **Create Node.js CI workflow** (`.github/workflows/node-ci.yml`):
   ```yaml
   name: Node.js CI

   on:
     push:
       branches: [ main, develop ]
     pull_request:
       branches: [ main, develop ]

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
       - uses: actions/checkout@v3
       - name: Use Node.js
         uses: actions/setup-node@v3
         with:
           node-version: '18'
           cache: 'pnpm'
       - name: Install pnpm
         run: npm install -g pnpm
       - run: pnpm install
       - run: pnpm run build
         env:
           CI: true
       - run: pnpm test
         env:
           CI: true
   ```

## GitHub Pages Deployment

To deploy the frontend to GitHub Pages:

1. **Create deployment workflow** (`.github/workflows/deploy.yml`):
   ```yaml
   name: Deploy to GitHub Pages

   on:
     push:
       branches: [ main ]
     workflow_dispatch:

   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Use Node.js
           uses: actions/setup-node@v3
           with:
             node-version: '18'
             cache: 'pnpm'
         - name: Install pnpm
           run: npm install -g pnpm
         - run: pnpm install
         - run: pnpm run build
         - name: Deploy to GitHub Pages
           uses: JamesIves/github-pages-deploy-action@v4
           with:
             folder: edupath-frontend/dist
             branch: gh-pages
   ```

2. **Update Vite Config**
   In `vite.config.ts`:
   ```typescript
   export default defineConfig({
     base: '/edupath/', // Your repository name
     // ... other config
   })
   ```

3. **Enable GitHub Pages**
   - Go to Settings → Pages
   - Select source: `gh-pages` branch
   - Select folder: `/ (root)`
   - Click Save

## Collaboration Guidelines

1. **Issues**
   - Use templates for bugs and feature requests
   - Assign labels appropriately
   - Link issues to projects/milestones

2. **Pull Requests**
   - Reference related issues
   - Include screenshots for UI changes
   - Request reviews from at least one team member
   - All tests must pass before merging

3. **Code Review**
   - Be constructive and specific
   - Suggest improvements with code examples
   - Acknowledge good patterns
   - Use GitHub's suggestion feature

4. **Documentation**
   - Update README for significant changes
   - Add comments for complex logic
   - Document new environment variables

## Security Best Practices

1. **Secrets Management**
   - Never commit secrets to version control
   - Use GitHub Secrets for sensitive data
   - Rotate API keys regularly

2. **Dependencies**
   - Use Dependabot for security updates
   - Regularly audit dependencies
   - Pin dependency versions

3. **Branch Protection**
   - Enable branch protection for main and develop
   - Require pull request reviews
   - Require status checks to pass
   - Require linear history

## Troubleshooting

- **Permission denied (publickey)**: Ensure your SSH key is added to your GitHub account
- **Authentication failed**: Use a personal access token if you have 2FA enabled
- **Merge conflicts**: Use `git status` to identify conflicts and resolve them before pushing

## Resources

- [GitHub Docs](https://docs.github.com)
- [Git Flow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://pages.github.com/)

---

This guide provides a comprehensive setup for managing the EduPath project on GitHub. For any questions or issues, please open an issue in the repository.
