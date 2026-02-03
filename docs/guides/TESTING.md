# 🧪 Testing Guide

Complete guide for testing SaaS Planz.

---

## Quick Start

### Run All Tests with Docker

```bash
cd apps/mvp-streamlit
docker-compose --profile test run --rm test
```

**Expected output:**
```
=================== 45 passed in X.XXs ===================
```

---

## Unit Tests

### Test Structure

```
tests/
├── test_parser.py         # CSV parsing tests
├── test_scheduler.py      # Scheduling algorithm tests
├── test_formatter.py      # Output formatting tests
└── test_integration.py    # End-to-end tests
```

### Running Specific Tests

```bash
# Single test file
docker-compose --profile test run --rm test pytest tests/test_parser.py -v

# Single test class
docker-compose --profile test run --rm test pytest tests/test_parser.py::TestParseTime -v
```

### What's Tested

**test_parser.py:** Time parsing, CSV validation, linked groups  
**test_scheduler.py:** Skeleton validation, OR-Tools constraints, warnings  
**test_formatter.py:** JSON/Markdown export  
**test_integration.py:** End-to-end scenarios

---

## Manual Testing (Streamlit)

### Launch App

```bash
./run-mvp.sh start
# Open http://localhost:8501
```

### Test Cases

Located in `docs/examples/test-cases/`:

| Test Case | Students | Complexity |
|-----------|----------|------------|
| 01-simple | 4 | Basic |
| 02-moyen | 8 | Medium |
| 03-complexe | 14 | Complex |
| 04-tres-complexe | 22 | Very Complex |
| 05-extreme | 30 | Extreme |
| demo-warnings | 3 | Warnings Demo |

### Testing Workflow

1. Upload `disponibilites.csv` + `recurring-slots.csv`
2. Click "Générer Planning"
3. Verify results match expected output
4. Download JSON/Markdown

---

## CSV Validation

```bash
python scripts/validate_test_csv.py docs/examples/test-cases/*/disponibilites.csv
```

Checks: field count, time format, granularity, valid days.

---

## Adding New Tests

### Unit Test

Add function to appropriate file in `tests/`, then run:
```bash
docker-compose --profile test run --rm test pytest tests/test_parser.py::test_my_feature -v
```

### Manual Test Case

```bash
mkdir -p docs/examples/test-cases/06-my-case
# Add disponibilites.csv, recurring-slots.csv, README.md
python scripts/validate_test_csv.py docs/examples/test-cases/06-my-case/disponibilites.csv
```

---

## Troubleshooting

**Tests fail:** Check logs with `docker-compose logs test`  
**CSV errors:** Validate format, check for missing commas  
**Streamlit issues:** Review error message, check `./run-mvp.sh logs`

---

✅ **Ready to test!**
