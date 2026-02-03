# 📚 SaaS Planz - Documentation

Welcome to the SaaS Planz documentation. This guide helps you get started, understand the architecture, and navigate all available resources.

---

## 🚀 Quick Start

### ⚡ Launch in 3 Commands

```bash
# 1. Start the MVP Streamlit app
./run-mvp.sh start

# 2. Open in browser
open http://localhost:8501

# 3. That's it! 🎉
```

### Available Commands

```bash
./run-mvp.sh start       # Start the app
./run-mvp.sh stop        # Stop the app
./run-mvp.sh restart     # Restart
./run-mvp.sh logs        # View live logs
./run-mvp.sh status      # Container status
./run-mvp.sh shell       # Shell in container
./run-mvp.sh clean       # Clean everything
```

---

## 📁 Documentation Structure

### 📦 [examples/](examples/)
CSV templates and usage guides for users
- `template-disponibilites.csv` - Student availability template
- `template-recurring-slots.csv` - Recurring slots template
- `README-template.md` - Availability template guide
- `README-recurring-slots.md` - Recurring slots guide
- **6 Test Cases:** `01-simple` to `05-extreme` + `demo-warnings`

### 🏗️ [architecture/](architecture/)
System architecture documentation
- `ARCHITECTURE.md` - System design and components

### 🐳 [DOCKER.md](DOCKER.md)
Complete Docker setup and development guide
- Installation instructions
- Quick start & commands
- Development workflow with hot-reload
- Troubleshooting

### 📖 [guides/](guides/)
General guides and how-tos
- `TESTING.md` - Complete testing guide

### 🔧 [implementation/](implementation/)
Implementation reports and technical documentation
- `IMPLEMENTATION_COMPLETE.md` - Full implementation report
- `SELF_CHECK_REPORT.md` - Technical audit

---

## 🎯 Get Started by Role

### Developer

1. **Setup:** Read [DOCKER.md](DOCKER.md)
2. **Testing:** Read [guides/TESTING.md](guides/TESTING.md)
3. **Architecture:** Read [architecture/ARCHITECTURE.md](architecture/ARCHITECTURE.md)
4. **Implementation:** Read [implementation/IMPLEMENTATION_COMPLETE.md](implementation/IMPLEMENTATION_COMPLETE.md)

**Development workflow:**
```bash
# Start the app
./run-mvp.sh start

# Modify code in core/ or apps/mvp-streamlit/app.py
# → Hot-reload automatically detects changes
# → Refresh browser

# Run tests
cd apps/mvp-streamlit
docker-compose --profile test run --rm test
```

### End User (Tony)

1. **CSV Templates:** Read [examples/README-template.md](examples/README-template.md)
2. **Recurring Slots:** Read [examples/README-recurring-slots.md](examples/README-recurring-slots.md)
3. **Launch App:** Run `./run-mvp.sh start`
4. **Upload CSV** via http://localhost:8501

### DevOps

1. **Docker Guide:** Read [DOCKER.md](DOCKER.md)
2. **Scripts:** Check `scripts/` folder
3. **CI/CD:** (to be implemented)

---

## 📂 Project Structure

```
saas-planz/
├── core/                      # Core business logic (reusable)
│   ├── models.py              # Dataclasses (Slot, Student, Schedule)
│   ├── parser.py              # CSV parsing
│   ├── scheduler.py           # OR-Tools algorithm
│   └── formatter.py           # Export JSON/Markdown
├── apps/
│   └── mvp-streamlit/         # Phase 1: Streamlit MVP
│       ├── app.py             # UI
│       ├── Dockerfile
│       └── docker-compose.yml
├── tests/                     # Test suite
│   ├── test_parser.py
│   ├── test_scheduler.py
│   ├── test_formatter.py
│   └── test_integration.py
├── docs/                      # Documentation (this folder)
├── scripts/                   # Utility scripts
└── run-mvp.sh                 # Main launcher
```

**Key principle:** The `core/` module is **reusable** across all apps (future web, mobile, API, etc.).

---

## 📍 Quick Navigation

| Need | File |
|------|------|
| **Start the project** | `../README.md` (root) |
| **Docker setup** | `DOCKER.md` |
| **Fill CSV** | `examples/README-template.md` |
| **Testing guide** | `guides/TESTING.md` |
| **Implementation details** | `implementation/IMPLEMENTATION_COMPLETE.md` |
| **Architecture** | `architecture/ARCHITECTURE.md` |

---

## 🧪 Testing

### Quick Validation

```bash
# Run all tests
cd apps/mvp-streamlit
docker-compose --profile test run --rm test

# Expected output:
# =================== 45 passed in X.XXs ===================
```

### Manual Testing in Streamlit

1. Start app: `./run-mvp.sh start`
2. Open http://localhost:8501
3. Upload test cases from `docs/examples/test-cases/`
4. Verify results

**Available test cases:**
- `01-simple` - 4 students, basic case
- `02-moyen` - 8 students, medium complexity
- `03-complexe` - 14 students, linked groups
- `04-tres-complexe` - 22 students, high density
- `05-extreme` - 30 students, maximum capacity
- `demo-warnings` - Single-student warnings demo

---

## 🐛 Troubleshooting

### Docker Daemon Not Running

- **Windows/Mac:** Start Docker Desktop
- **Linux:** `sudo systemctl start docker`

### Port 8501 Already in Use

Change port in `apps/mvp-streamlit/docker-compose.yml`:
```yaml
ports:
  - "8502:8501"  # Use 8502 on host
```

### Permission Denied

```bash
chmod +x run-mvp.sh
```

### More Help

See [DOCKER.md](DOCKER.md) section "Troubleshooting" for complete guide.

---

## 🔮 Adding New Apps (Future Phases)

When ready for Phase 2 (web app, mobile, etc.):

```bash
# Create new app folder
mkdir -p apps/web-nextjs-fastapi
cd apps/web-nextjs-fastapi

# Create files
touch README.md Dockerfile docker-compose.yml

# Reuse core
# → Import from ../../core/
```

**The `core/` stays unchanged** - just import it from the new app!

---

## ✅ Pre-Flight Checklist

Before starting development:

- [ ] Docker installed (`docker --version`)
- [ ] Docker Compose installed (`docker compose version`)
- [ ] Scripts executable (`chmod +x run-mvp.sh`)
- [ ] Container starts (`./run-mvp.sh start`)
- [ ] App accessible (http://localhost:8501)
- [ ] Tests pass (`docker-compose --profile test run --rm test`)

---

## 📝 Additional Resources

### Tech-Spec (root directory)
- `../_bmad-output/implementation-artifacts/tech-spec-wip.md` - Refactoring tech-spec
- `../_bmad-output/implementation-artifacts/tech-spec-algo-generation-planning.md` - Algorithm planning

### Brainstorming
- `../_bmad-output/brainstorming/brainstorming-session-2026-02-01.md`

---

## 📞 Support

**Questions or issues?**
- Check logs: `./run-mvp.sh logs`
- Open shell: `./run-mvp.sh shell`
- See troubleshooting: [DOCKER.md](DOCKER.md)
- Review implementation: [implementation/IMPLEMENTATION_COMPLETE.md](implementation/IMPLEMENTATION_COMPLETE.md)

---

**Ready to go! Run `./run-mvp.sh start` 🚀**
