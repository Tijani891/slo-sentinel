# slo-sentinel

An uptime and SLO monitor that runs entirely on Cloudflare's free plan.

A Cron Trigger probes a list of HTTP endpoints every few minutes and records
status code, latency and errors in Cloudflare D1. A FastAPI app on a Python
Worker serves a public status page with uptime, p50/p95 latency, SLO targets
and remaining error budget, and incident history. Discord/Telegram webhooks
fire when an endpoint goes down and when it recovers.

> **Status:** early development. Built in public, one commit a day,
> Nov 15 – Dec 15, 2026.

## Stack

- Cloudflare Python Workers (Pyodide) + FastAPI
- Cloudflare D1 (SQLite) with versioned SQL migrations
- Cron Triggers for scheduled probing
- GitHub Actions: ruff, mypy, pytest, staging and production deploys, smoke
  tests, rollback

## Layout

```
src/entry.py          Worker entrypoint: the only file that imports Workers APIs
src/slo_sentinel/     Application code, importable under plain CPython
tests/                pytest suite (runs without the Workers runtime)
wrangler.jsonc        Worker configuration
```

## Local development

Requires [uv](https://docs.astral.sh/uv/) 0.13.4+ (pywrangler checks this) and Node.js 20+.

```bash
uv sync                      # install dependencies
uv run pytest --cov          # run tests with coverage
uv run ruff check .          # lint
uv run ruff format --check .
uv run mypy                  # type check
uv run pywrangler dev        # run the Worker locally on http://localhost:8787
```

## Roadmap

- [x] Scaffold, `/health`, lint/type/test tooling
- [ ] CI on every push and PR
- [ ] Dockerised dev and test environment
- [ ] Probing via Cron Trigger, stored in D1
- [ ] Uptime, latency percentiles, SLOs and error budgets
- [ ] Incident detection and webhook alerts
- [ ] Public status page
- [ ] Staging/production deploys, smoke tests, rollback
- [ ] SLO definitions, runbook, postmortem template

## License

MIT