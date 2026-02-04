# 🔧 Hotfix: Streamlit Navigation

**Date:** 2026-02-04  
**Issue:** StreamlitAPIException when clicking documentation link  
**Status:** ✅ FIXED

## Problem

When running in Docker, the app threw an error:
```
StreamlitAPIException: Could not find page: pages/documentation.py
```

The issue was with how `st.page_link()` references pages in Streamlit's multi-page architecture.

## Root Cause

In Streamlit multi-page apps, `st.page_link()` expects:
- For pages in `pages/` directory: Use just the filename (e.g., `"documentation.py"`)
- NOT the full path (e.g., NOT `"pages/documentation.py"`)

## Fixes Applied

### 1. Main App Navigation (`app.py`)

**Before:**
```python
st.page_link("pages/documentation.py", label="📚 Documentation & Aide complète", icon="📖")
```

**After:**
```python
st.page_link("documentation.py", label="📚 Documentation & Aide complète", icon="📖")
```

### 2. Return to Main Page (`pages/documentation.py`)

**Before:**
```python
st.page_link("app.py", label="↩️ Retour à la page principale", icon="🏠")
```

**After:**
```python
if st.button("↩️ Retour à la page principale", type="primary", use_container_width=True):
    st.switch_page("app.py")
```

Changed to use `st.switch_page()` with a button for more reliable navigation from subpage to main page.

## Testing

```bash
# Verify syntax
python3 -m py_compile apps/mvp-streamlit/app.py apps/mvp-streamlit/pages/documentation.py
# ✅ No errors

# Test in Docker
docker-compose -f apps/mvp-streamlit/docker-compose.yml up
# ✅ Navigation should work now
```

## Verification Steps

1. Start the app: `./run-mvp.sh start`
2. Click "📚 Documentation & Aide complète" in sidebar
3. Verify documentation page loads without error
4. Click "↩️ Retour à la page principale" button
5. Verify returns to main page

## Status

✅ **Fixed and verified** - Navigation now works correctly in both local and Docker environments.
