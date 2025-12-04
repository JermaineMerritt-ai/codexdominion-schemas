# 🌟 Contributing to CodexDominion

Welcome, Sovereign Steward 👑
This guide ensures every contribution honors the CodexDominion rhythm.

---

## 🧭 Standards

- **Variables** → `camelCase`
- **Classes / Interfaces** → `PascalCase`
- **Directories / Files** → `kebab-case`
- **Indentation** → 2 spaces
- **Line endings** → LF (Unix style)
- **Commits** → Use Conventional Commits:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation
  - `refactor:` for code improvements
  - `test:` for testing additions

---

## 🛠️ Setup

```bash
git clone https://github.com/JermaineMerritt-ai/codexdominion-schemas.git
npm install

Thank you for your interest in contributing to Codex Dominion! This document provides guidelines and instructions for contributing to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Community](#community)

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## 🚀 Getting Started

### Prerequisites

- **Node.js** >= 16.0.0
- **Python** >= 3.9.0
- **npm** >= 8.0.0
- **Git** for version control
- **Docker** (optional, for containerization)

### Setting Up Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/codexdominion-schemas.git
   cd codexdominion-schemas
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/JermaineMerritt-ai/codexdominion-schemas.git
   ```

4. **Install dependencies**:
   ```bash
   npm install
   pip install -r requirements.txt
   ```

5. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your local configurations
   ```

6. **Build the project**:
   ```bash
   npm run build
   ```

7. **Run tests**:
   ```bash
   npm test
   ```

## 🔄 Development Workflow

### Branching Strategy

We use a simplified Git Flow:

- **`main`**: Production-ready code
- **`staging`**: Pre-production testing
- **`development`**: Integration branch for features
- **`feature/*`**: New features
- **`bugfix/*`**: Bug fixes
- **`hotfix/*`**: Critical production fixes

### Creating a Feature Branch

```bash
# Update your local main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes and commit
git add .
git commit -m "feat: Add amazing feature"

# Push to your fork
git push origin feature/your-feature-name
```

### Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

**Examples:**
```bash
feat(capsules): Add treasury-audit capsule with monthly scheduling
fix(frontend): Resolve TypeScript interface duplication in capsule pages
docs(readme): Update installation instructions for Python 3.11
ci(workflows): Add automated security scanning workflow
```

## 📝 Coding Standards

### TypeScript/JavaScript

- Use **TypeScript** for all new code
- Follow **ESLint** configuration
- Use **Prettier** for formatting
- Maintain **strict type safety**
- Write **JSDoc comments** for public APIs

```typescript
/**
 * Fetches the latest artifact for a specific capsule
 * @param slug - The capsule identifier
 * @returns Promise resolving to the artifact data
 * @throws Error if capsule not found
 */
export async function fetchCapsuleArtifact(slug: string): Promise<Artifact> {
  // Implementation
}
```

### Python

- Follow **PEP 8** style guide
- Use **type hints** for all functions
- Write **docstrings** for all modules, classes, and functions
- Use **Black** for formatting
- Use **isort** for import sorting

```python
def execute_capsule(capsule_id: str, config: dict) -> dict:
    """
    Execute a capsule with the given configuration.

    Args:
        capsule_id: Unique identifier for the capsule
        config: Configuration dictionary for execution

    Returns:
        Dictionary containing execution results and metadata

    Raises:
        CapsuleNotFoundError: If capsule_id is invalid
        ExecutionError: If execution fails
    """
    # Implementation
```

### Code Quality Checks

Before submitting a PR, run:

```bash
# Linting
npm run lint

# Type checking
npm run type-check

# Formatting
npm run format

# Tests
npm test

# Python linting
flake8 .
black --check .
isort --check-only .
```

## 🔍 Pull Request Process

### Before Submitting

1. **Update your branch** with latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all tests** and ensure they pass:
   ```bash
   npm test
   pytest
   ```

3. **Update documentation** if needed

4. **Add tests** for new features

5. **Ensure no linting errors**:
   ```bash
   npm run lint
   flake8 .
   ```

### Submitting the PR

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub:
   - Use a clear, descriptive title
   - Reference related issues (e.g., "Fixes #123")
   - Provide detailed description of changes
   - Add screenshots for UI changes
   - List breaking changes if any

3. **PR Template** (automatically loaded):
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] All tests pass
   - [ ] New tests added
   - [ ] Manual testing completed

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No breaking changes (or documented)
   ```

### Review Process

1. **Automated checks** must pass (CI/CD workflows)
2. **Code review** by at least one maintainer
3. **Address feedback** and push updates
4. **Approval** required before merge
5. **Squash and merge** into target branch

## 🐛 Issue Guidelines

### Reporting Bugs

Use the **Bug Report** template and include:

- **Clear title** describing the issue
- **Steps to reproduce** the bug
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Node version, Python version)
- **Screenshots** or error logs
- **Possible solution** (optional)

### Requesting Features

Use the **Feature Request** template and include:

- **Clear description** of the feature
- **Use case** and motivation
- **Proposed implementation** (optional)
- **Alternatives considered**
- **Additional context**

### Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead, email: security@codex-dominion.com or see [SECURITY.md](SECURITY.md)

## 🧪 Testing

### Unit Tests

```bash
# Run all unit tests
npm test

# Run specific test file
npm test -- capsule.test.ts

# Run with coverage
npm test -- --coverage
```

### Integration Tests

```bash
# Run integration tests
npm test -- --testPathPattern=integration

# Run E2E tests
npm run test:e2e
```

### Writing Tests

```typescript
describe('CapsuleService', () => {
  describe('fetchArtifact', () => {
    it('should return artifact for valid slug', async () => {
      const artifact = await fetchArtifact('signals-daily');
      expect(artifact).toBeDefined();
      expect(artifact.title).toBeTruthy();
    });

    it('should throw error for invalid slug', async () => {
      await expect(fetchArtifact('invalid')).rejects.toThrow();
    });
  });
});
```

## 📚 Documentation

### When to Update Documentation

- Adding new features
- Changing APIs or interfaces
- Modifying configuration options
- Adding new dependencies
- Changing deployment procedures

### Documentation Locations

- **README.md**: Project overview and quick start
- **docs/**: Detailed documentation
- **API comments**: Inline code documentation
- **CHANGELOG.md**: Version history and changes

## 🏗️ Architecture Guidelines

### Project Structure

```
codex-dominion/
├── frontend/           # Next.js frontend application
│   ├── pages/         # Next.js pages
│   ├── components/    # React components
│   └── styles/        # Global styles
├── src/
│   └── backend/       # Python backend services
├── .github/
│   ├── workflows/     # CI/CD workflows
│   └── actions/       # Custom GitHub Actions
├── infra/
│   └── terraform/     # Infrastructure as Code
└── system_capsules/   # Capsule definitions
```

### Design Principles

1. **Separation of Concerns**: Keep components focused and modular
2. **Type Safety**: Use TypeScript and Python type hints
3. **Error Handling**: Comprehensive error handling with meaningful messages
4. **Testing**: Aim for >80% code coverage
5. **Documentation**: Document public APIs and complex logic
6. **Performance**: Optimize for speed and efficiency
7. **Security**: Follow security best practices

## 🌐 Community

### Communication Channels

- **GitHub Discussions**: General questions and discussions
- **Discord**: Real-time chat and community support
- **Email**: support@codex-dominion.com

### Getting Help

1. Check existing documentation
2. Search closed issues
3. Ask in Discord community
4. Create a GitHub Discussion
5. Open an issue if needed

## 🎯 Good First Issues

Look for issues labeled `good-first-issue` or `help-wanted` to get started!

## 📄 License

By contributing, you agree that your contributions will be licensed under the CODEX-SOVEREIGN-LICENSE.

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- GitHub contributors page
- Release notes for significant contributions

---

**Thank you for contributing to Codex Dominion!** 🚀

Your contributions help build the future of digital sovereignty and autonomous infrastructure.

For questions, reach out to the maintainers or join our Discord community.

**Repository**: https://github.com/JermaineMerritt-ai/codexdominion-schemas

**Maintained by**: Jermaine Merritt & The Codex Council
