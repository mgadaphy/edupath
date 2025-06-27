# Contributing to EduPath

First off, thank you for considering contributing to EduPath! We're excited to have you on board. This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Bugs are tracked as [GitHub issues](https://github.com/yourusername/edupath/issues).

Before creating a bug report, please check if the bug has already been reported. If it has, add a comment to the existing issue instead of opening a new one.

When creating a bug report, please include:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Your environment (OS, browser, etc.)

### Suggesting Enhancements

Enhancement suggestions are also tracked as [GitHub issues](https://github.com/yourusername/edupath/issues).

Before creating an enhancement suggestion, please check if a similar enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.

When suggesting an enhancement, please include:
- A clear, descriptive title
- A description of the suggested enhancement
- Why this enhancement would be useful
- Any alternative solutions you've considered

### Your First Code Contribution

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests: `pnpm test` (frontend) / `pytest` (backend)
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to the branch: `git push origin feature/your-feature-name`
7. Open a pull request

## Development Workflow

1. **Fork** the repository on GitHub
2. **Clone** the project to your own machine
3. **Create a branch** for your feature or bugfix
4. **Commit** changes to your own branch
5. **Push** your work back up to your fork
6. Submit a **Pull Request** so that we can review your changes

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations, and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## Coding Standards

### Frontend
- Use TypeScript for all new code
- Follow the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use functional components with React Hooks
- Follow the existing code style and naming conventions
- Write unit tests for new components and features

### Backend
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Include unit tests for new features

## Commit Message Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/) for our commit messages. Format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc.)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries

### Examples
```
feat: add user authentication

docs: update README with installation instructions

fix(api): handle null values in user profile
```

## Getting Help

If you need help with anything, please don't hesitate to open an issue or reach out to the maintainers.
