# Guardian’s Quickstart Capsule

> Fast onboarding for engineers — just the commands, no ceremony.

---

## 1. Clone & Enter Repo

```sh
git clone https://github.com/JermaineMerritt-ai/codexdominion-schemas.git
cd codexdominion-schemas
```

## 2. Install Dependencies

```sh
pip install -r requirements-dev.txt
npm install
```

## 3. Run Hygiene Sweep

```sh
./scripts/green_sweep.sh
```

## 4. Test & Validate

```sh
pytest
# (Optional) Node.js lint/format
npm run lint
npm run format
```

## 5. Commit & Push

```sh
git add -A
git commit -m "feat: your change"
git push
```

---

## 🛡️ Pro Tips

- Always run `green_sweep.sh` before pushing.
- Keep secrets out of commits—use GitHub Actions secrets.
- For full hygiene, see README and CONTRIBUTING.md.

---

## Stay green. Ship supreme.
