# Contributing Guidelines

Thank you for your interest in contributing to **Real-Time Kanji Tutor**!

This project adheres to professional software engineering standards to maintain high performance ($60\text{ FPS}$ real-time computer vision constraint) and code quality.

---

## 1. Branching Strategy

* `main`: The production-ready branch. All code must pass CI/CD checks before merging.
* `feature/<feature-name>`: For new computer vision modules, algorithms, or UI features.
* `fix/<bug-name>`: For bug fixes and algorithmic corrections.
* `docs/<topic>`: For documentation, theoretical explanations, or research notes.
* `test/<test-suite>`: For test additions and latency benchmarks.

---

## 2. Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

* `feat:` A new feature or algorithm (e.g., `feat: add Homography SVD calibration`)
* `fix:` A bug fix (e.g., `fix: resolve Laplacian variance division by zero`)
* `docs:` Documentation only changes (e.g., `docs: update Chapter 1 DIP fundamentals`)
* `style:` Code style/formatting changes without logic alteration (e.g., `style: format imports with ruff`)
* `refactor:` Code changes that neither fix a bug nor add a feature
* `perf:` Performance optimizations to respect the $16.66\text{ ms}$ budget
* `test:` Adding or updating tests (e.g., `test: add smoke test for package import`)
* `chore:` Build process, dependency, or tooling updates

---

## 3. Development Workflow

1. **Clone the repository and set up environment:**
   ```bash
   git clone https://github.com/hoangtranduchai/real-time-kanji-tutor.git
   cd real-time-kanji-tutor
   python -m venv .venv
   source .venv/bin/activate  # Or .\.venv\Scripts\Activate.ps1 on Windows
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   pip install -e .
   ```

2. **Lint and format code before committing:**
   ```bash
   ruff check .
   ruff format .
   ```

3. **Run automated tests:**
   ```bash
   pytest tests/ -v
   ```

---

## 4. Real-Time Latency Rule

All algorithms added to the primary video loop must respect the **Zero-Allocation** paradigm:
* Avoid dynamic memory allocations (`np.zeros`, `list.append` in loops) during active frame processing.
* Use pre-allocated buffers where possible to prevent garbage collection hiccups.
* Ensure execution latency for standard frame processing remains below $16.66\text{ ms}$ ($60\text{ FPS}$).

---

## 5. Submitting a Pull Request

1. Create a descriptive PR title using Conventional Commits.
2. Fill in the Pull Request template provided.
3. Ensure all GitHub Actions CI checks pass (green checkmark).
4. Request review from the maintainers.
