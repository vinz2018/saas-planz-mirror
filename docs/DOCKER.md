# 🐳 Docker Setup & Guide

This guide explains how to run SaaS Planz using Docker **without installing Python, pandas, ortools, or streamlit** on your machine.

---

## 📋 Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Available Commands](#available-commands)
4. [Development Workflow](#development-workflow)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)
7. [Architecture](#architecture)

---

## Installation

### Prerequisites

Install Docker on your system:

**Windows/Mac:**
- Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Install and restart your machine
- Docker Desktop includes Docker Compose

**Linux (Ubuntu/Debian):**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose plugin
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Add your user to docker group (avoids sudo)
sudo usermod -aG docker $USER
# Log out and log back in to apply
```

**Verify installation:**
```bash
docker --version
docker compose version
```

---

## Quick Start

### 3 Steps to Launch

```bash
# 1. Start the application
./run-mvp.sh start

# 2. Wait ~30s for Docker to build (first time only)

# 3. Open in browser
open http://localhost:8501
```

✅ **That's it!** The app is running with all dependencies inside Docker.

---

## Available Commands

### Main Script: `./run-mvp.sh`

#### Application Management

| Command | Description |
|---------|-------------|
| `./run-mvp.sh start` | Start the application |
| `./run-mvp.sh stop` | Stop the application |
| `./run-mvp.sh restart` | Restart the application |
| `./run-mvp.sh logs` | View live logs (Ctrl+C to exit) |
| `./run-mvp.sh status` | Show container status |

#### Testing

| Command | Description |
|---------|-------------|
| `cd apps/mvp-streamlit && docker-compose --profile test run --rm test` | Run all pytest tests |

#### Development & Debugging

| Command | Description |
|---------|-------------|
| `docker exec -it saas-planz-mvp-streamlit bash` | Open shell in container |
| `./run-mvp.sh rebuild` | Rebuild from scratch (no cache) |
| `./run-mvp.sh clean` | Clean everything (containers + images) |

### Alternative (without script)

If the script doesn't work on your system:

```bash
# Start
cd apps/mvp-streamlit
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Tests
docker-compose --profile test run --rm test
```

---

## Development Workflow

### Hot-Reload Enabled ✅

The following directories are **mounted as volumes** → changes are **automatically detected**:

- `core/` → Core modules (parser, scheduler, formatter, models)
- `apps/mvp-streamlit/app.py` → Streamlit UI
- `docs/` → Documentation and templates

**Workflow:**
1. Modify a file in `core/` or `app.py`
2. Save
3. Refresh browser → Streamlit auto-detects changes
4. ✅ Changes applied!

**No need to restart the container** for most changes.

### When to Rebuild

Rebuild only if you modify:
- `requirements.txt` (new dependencies)
- `Dockerfile`
- `docker-compose.yml`

```bash
cd apps/mvp-streamlit
docker-compose down
docker-compose up -d --build
```

---

## Testing

### Run All Tests

```bash
cd apps/mvp-streamlit
docker-compose --profile test run --rm test
```

This runs the full pytest suite (test_parser.py, test_scheduler.py, test_formatter.py, test_integration.py).

### Manual Testing in Streamlit

1. Start the app: `./run-mvp.sh start`
2. Open http://localhost:8501
3. Upload test cases from `docs/examples/test-cases/`
4. Verify results

**Available test cases:**
- `01-simple` - Basic case (4 students)
- `02-moyen` - Medium case (8 students)
- `03-complexe` - Complex case (14 students)
- `04-tres-complexe` - Very complex (22 students)
- `05-extreme` - Extreme (30 students)
- `demo-warnings` - Single-student warnings demo

---

## Troubleshooting

### Port 8501 Already in Use

**Error:** `Bind for 0.0.0.0:8501 failed: port is already allocated`

**Solution:**
```bash
# Find what's using the port
lsof -i :8501  # Mac/Linux
netstat -ano | findstr :8501  # Windows

# Or change port in docker-compose.yml
ports:
  - "8502:8501"  # Use 8502 on host
```

### Docker Daemon Not Running

**Error:** `Cannot connect to the Docker daemon`

**Solution:**
- **Windows/Mac:** Start Docker Desktop
- **Linux:** `sudo systemctl start docker`

### Container Won't Start

**Debug steps:**
```bash
# View error logs
cd apps/mvp-streamlit
docker-compose logs app

# Check container status
docker-compose ps

# Rebuild from scratch
docker-compose down
docker-compose up -d --build --no-cache
```

### Changes Not Detected

**Solution:**
```bash
# Restart Streamlit
cd apps/mvp-streamlit
docker-compose restart

# Or rebuild if requirements.txt changed
docker-compose down
docker-compose up -d --build
```

### Access from Another Machine (Network)

1. Find your local IP:
   ```bash
   # Windows
   ipconfig | findstr IPv4
   
   # Mac/Linux
   ifconfig | grep "inet "
   ```

2. Access from another machine:
   ```
   http://<YOUR_IP>:8501
   ```
   Example: `http://192.168.1.100:8501`

---

## Architecture

### Docker Files Structure

```
saas-planz/
├── apps/mvp-streamlit/
│   ├── Dockerfile               # Python 3.11 + dependencies
│   ├── docker-compose.yml       # Service orchestration
│   ├── app.py                   # Streamlit UI (hot-reload)
│   └── requirements.txt         # Python packages
├── core/                        # Core modules (hot-reload)
│   ├── models.py
│   ├── parser.py
│   ├── scheduler.py
│   └── formatter.py
├── docs/                        # Documentation (hot-reload)
├── tests/                       # Test suite
└── run-mvp.sh                   # Main launcher script
```

### Docker Compose Services

**Service: `app` (main)**
- Image: Python 3.11 slim
- Port: 8501 (Streamlit)
- Volumes: Core, docs, app.py mounted for hot-reload
- Restart: unless-stopped

**Service: `test` (on-demand)**
- Same image as `app`
- Runs pytest
- Profile: `test` (doesn't start by default)

### Mounted Volumes

```yaml
volumes:
  - ../../core:/app/core           # Hot-reload core modules
  - ./app.py:/app/app.py           # Hot-reload Streamlit UI
  - ../../docs:/app/docs           # Hot-reload docs/templates
```

---

## Benefits of Docker Setup

| Aspect | Without Docker | With Docker |
|--------|---------------|-------------|
| **Installation** | pip install ... | Nothing on your PC ✅ |
| **Dependencies** | Python, pandas, ortools | All in container ✅ |
| **Isolation** | Pollutes system | Completely isolated ✅ |
| **Portability** | OS-dependent | Works everywhere ✅ |
| **Cleanup** | Difficult | `docker-compose down` ✅ |
| **Versions** | Potential conflicts | Fixed in Dockerfile ✅ |
| **Hot-reload** | ✅ Yes | ✅ Yes (volumes) |
| **Performance** | Native | ~5% overhead |

---

## Next Steps

### For Development

1. ✅ Start app: `./run-mvp.sh start`
2. ✅ Open http://localhost:8501
3. ✅ Modify code (automatic hot-reload)
4. ✅ Test: `docker-compose --profile test run --rm test`

### For Testing with Tony

1. ✅ Fill `template-disponibilites.csv`
2. ✅ Upload via Streamlit UI
3. ✅ Generate schedule
4. ✅ Download JSON + Markdown results

### For Production Deployment

See deployment options:
- **Railway** (recommended) - Simple git push
- **Render** - Deploy from Dockerfile
- **Heroku** - Container deployment
- **VPS** - Docker Compose on server

---

## Support

**Questions?**
- Check logs: `cd apps/mvp-streamlit && docker-compose logs app`
- Open shell: `docker exec -it saas-planz-mvp-streamlit bash`
- See `README.md` for full documentation

**Resources:**
- [Docker Docs](https://docs.docker.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [OR-Tools Guide](https://developers.google.com/optimization)

---

✅ **Ready to go! Run `./run-mvp.sh start` to begin.**
