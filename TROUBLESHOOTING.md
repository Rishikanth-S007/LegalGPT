# LegalGPT Troubleshooting Guide

## Issue: "Analyzing your legal query..." Never Finishes

### Root Cause Found
**Multiple uvicorn processes running on port 8000 causing conflicts**

---

## SOLUTION: Clean Restart Procedure

### Step 1: Kill All Old Processes

**Windows PowerShell:**
```powershell
# Kill all Python/Uvicorn processes on port 8000
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | 
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

**Or run the batch file:**
```cmd
C:\LegalGPT\kill_old_server.bat
```

### Step 2: Start Backend Clean

**Method A: Use the startup script**
```cmd
C:\LegalGPT\START_BACKEND.bat
```

**Method B: Manual start**
```cmd
cd C:\LegalGPT\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Verify Server is Running

**Test 1: Simple ping**
```bash
curl http://localhost:8000/api/test/ping
# Should return: {"status":"ok","message":"pong"}
```

**Test 2: Health check**
```bash
curl http://localhost:8000/health
# Should return health status in < 1 second
```

**Test 3: Prediction API**
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"Someone stole my phone\"}" \
  --max-time 15
```

### Step 4: Start Frontend

```cmd
cd C:\LegalGPT\frontend
npm start
```

---

## Expected Startup Logs

When backend starts correctly, you should see:

```
============================================================
[STARTUP] STARTING LEGALGPT ENGINE...
============================================================

------------------------------------------------------------
[INIT] Initializing Multi-Law Predictor Engine...
------------------------------------------------------------
[LOAD] Loading Sentence Transformer model...
[OK] Embedding model loaded
[LOAD] Loading Cross-Encoder reranker...
[OK] Cross-encoder loaded
[BUILD] Building FAISS index from legal dataset...
   Encoding 497 legal scenarios...
   [OK] Index built successfully!
------------------------------------------------------------
[SUCCESS] Indexed 497 legal scenarios
------------------------------------------------------------

============================================================
[INIT] Creating LawPredictor instance...
============================================================
============================================================
[SUCCESS] Engine Ready!
============================================================

============================================================
[SUCCESS] ENGINE READY - Models loaded and cached in memory
============================================================

INFO:     Application startup complete.
```

**IMPORTANT:** You should see **ONLY ONE** "Initializing" message.
If you see TWO, there's still a duplicate import issue.

---

## Common Issues & Fixes

### Issue 1: Port Already in Use

**Symptom:**
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000): 
only one usage of each socket address (protocol/network address/port) is normally permitted
```

**Fix:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /F /PID <PID>
```

### Issue 2: Timeout on Prediction

**Symptom:**
- API call times out after 10-30 seconds
- No response from `/api/predict`

**Possible Causes:**
1. **Blocking synchronous code** - FIXED by making `/api/predict` async
2. **FAISS index not loaded** - Check startup logs
3. **Deadlock in ThreadPoolExecutor** - Restart server

**Fix:**
Restart the backend server completely (kill all processes first)

### Issue 3: Frontend Shows Loading Forever

**Symptom:**
- "Analyzing your legal query..." animation runs forever
- No error in console
- No response displayed

**Debug Steps:**

1. **Open Browser DevTools (F12)**
2. **Go to Console tab**
3. **Look for logs:**
   - "Sending request to: http://localhost:8000/api/predict"
   - "Response status: 200" or error
   - "API Response data: {...}"

4. **Go to Network tab**
5. **Find `/api/predict` request**
6. **Check:**
   - Status: Should be 200
   - Time: Should be < 10 seconds
   - Response: Should show JSON data

**Common Causes:**
- Backend not running → Start backend
- CORS error → Check CORS settings in backend
- Wrong URL → Check `REACT_APP_BACKEND_URL` in `.env`
- Response parsing error → Check console for JavaScript errors

### Issue 4: "Out of Scope" for Valid Legal Queries

**Already Fixed!** See summary of keyword fixes in previous session.

If still happening:
1. Check query contains legal keywords
2. Verify FAISS index loaded correctly (497 scenarios)
3. Check backend logs for prediction confidence score

---

## Testing Checklist

Before reporting issues, verify:

- [ ] No other processes on port 8000
- [ ] Backend starts without errors
- [ ] Only ONE engine initialization message
- [ ] `/api/test/ping` returns "pong"
- [ ] `/health` returns status < 1 second
- [ ] `/api/predict` returns response < 10 seconds
- [ ] Frontend connects to correct backend URL
- [ ] Browser console shows no CORS errors
- [ ] Network tab shows 200 OK for API calls

---

## Quick Test Script

Save as `test_backend.py`:

```python
import requests
import time

print("Testing LegalGPT Backend...")

# Test 1: Ping
try:
    r = requests.get("http://localhost:8000/api/test/ping", timeout=3)
    print(f"✓ Ping: {r.json()}")
except Exception as e:
    print(f"✗ Ping failed: {e}")
    exit(1)

# Test 2: Health
try:
    r = requests.get("http://localhost:8000/health", timeout=3)
    print(f"✓ Health: {r.json()['status']}")
except Exception as e:
    print(f"✗ Health failed: {e}")
    exit(1)

# Test 3: Prediction
try:
    start = time.time()
    r = requests.post(
        "http://localhost:8000/api/predict",
        json={"query": "Someone stole my phone"},
        timeout=15
    )
    elapsed = time.time() - start
    data = r.json()
    print(f"✓ Predict: {elapsed:.2f}s")
    print(f"  Response keys: {list(data.keys())}")
    if 'response' in data:
        resp = data['response']
        if isinstance(resp, dict):
            print(f"  Applicable Law: {resp.get('applicable_law', 'N/A')}")
            print(f"  Confidence: {resp.get('confidence', 'N/A')}")
except Exception as e:
    print(f"✗ Predict failed: {e}")
    exit(1)

print("\n✓ All tests passed!")
```

Run with:
```bash
cd C:\LegalGPT
python test_backend.py
```

---

## Getting Help

If issues persist:

1. **Share startup logs** (first 50 lines)
2. **Share browser console errors** (F12 → Console)
3. **Share network tab** (F12 → Network → /api/predict)
4. **Run test script** and share output
5. **Check if port 8000 has multiple listeners:**
   ```
   netstat -ano | findstr :8000
   ```

---

## Files Modified (Latest Session)

1. `C:\LegalGPT\backend\app\main.py`
   - Made `/api/predict` async with ThreadPoolExecutor
   - Added `/api/test/ping` endpoint
   - Added detailed logging

2. `C:\LegalGPT\backend\app\services\ai_service.py`
   - Updated to use `law_predictor_service`
   - Fixed response format handling

3. `C:\LegalGPT\frontend\src\components\ChatInterface.js`
   - Enhanced error handling
   - Added console logging
   - Improved response parsing

---

Last Updated: 2026-03-23
