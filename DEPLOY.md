# 🚀 Deploy to PythonAnywhere — Easy Steps

This guide walks you through deploying the True Love AI app to PythonAnywhere.

**Your account:** https://www.pythonanywhere.com/user/trueloveai/
**Your live URL (after setup):** https://trueloveai.pythonanywhere.com/

---

## ✅ Prerequisites

- A free or paid PythonAnywhere account (you have: `trueloveai`)
- The latest code pushed to GitHub: https://github.com/Richard-Johnson-Anglican-College/12SE_True_Love_AI

---

## 📋 First-Time Deployment (Do This Once)

### **Step 1: Open a Bash Console**

1. Go to https://www.pythonanywhere.com/user/trueloveai/
2. Click **"Consoles"** tab → click **"Bash"** under "New console"

### **Step 2: Clone the Repository**

In the Bash console, run:

```bash
cd ~
git clone https://github.com/Richard-Johnson-Anglican-College/12SE_True_Love_AI.git
cd 12SE_True_Love_AI
```

### **Step 3: Create a Virtual Environment** ⚡ Fast Method

```bash
mkvirtualenv --python=/usr/bin/python3.13 --system-site-packages trueloveai-venv
```

This activates automatically. Your prompt will now show `(trueloveai-venv)`.

> **💡 Why `--system-site-packages`?**
> PythonAnywhere already has the exact versions of `numpy`, `pandas`, `matplotlib`, and `scikit-learn` that we need (verified pre-installed in `/usr/lib/python3.13/site-packages`). This flag inherits them, so you skip ~10-20 minutes of slow source compilation on the free tier.

### **Step 4: Install Only Flask (Everything Else Inherited)**

```bash
cd ~/12SE_True_Love_AI
pip install Flask==3.0.3
```

Takes ~10 seconds. The other packages (`scikit-learn`, `pandas`, `numpy`, `matplotlib`) are inherited from the system — no compilation needed.

### **Step 4b: Verify All Packages Are Available**

```bash
python -c "import flask, pandas, numpy, matplotlib, sklearn; print('Flask:', flask.__version__); print('pandas:', pandas.__version__); print('numpy:', numpy.__version__); print('matplotlib:', matplotlib.__version__); print('sklearn:', sklearn.__version__)"
```

You should see:
```
Flask: 3.0.3
pandas: 2.2.2
numpy: 2.1.0
matplotlib: 3.9.2
sklearn: 1.6.0
```

✅ All versions match — perfect.

> **⚠️ Avoid this slow alternative:** Running `pip install -r requirements.txt` in a fresh venv (without `--system-site-packages`) will try to compile `pandas 2.2.2` from source because no Python 3.13 wheel exists. This can hang for 10-20 minutes on the free tier or fail entirely. Always use the `--system-site-packages` approach above.

### **Step 5: Create the Web App**

1. Go to the **"Web"** tab on the PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Click **"Next"** (the domain `trueloveai.pythonanywhere.com` is auto-selected)
4. Choose **"Manual configuration"** (NOT Flask — we'll configure it manually for control)
5. Choose **"Python 3.13"**
6. Click **"Next"** to confirm

### **Step 6: Configure the Web App**

You'll now be on the configuration page. Set these values:

#### **Source code:**
```
/home/trueloveai/12SE_True_Love_AI
```

#### **Working directory:**
```
/home/trueloveai/12SE_True_Love_AI
```

#### **Virtualenv:**
```
/home/trueloveai/.virtualenvs/trueloveai-venv
```

### **Step 7: Edit the WSGI File**

1. On the Web tab, find the **"Code"** section
2. Click the WSGI configuration file link (looks like `/var/www/trueloveai_pythonanywhere_com_wsgi.py`)
3. **Delete everything** in that file
4. Replace with this:

```python
import sys

# Add project directory to Python path
project_home = '/home/trueloveai/12SE_True_Love_AI'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import your Flask app
from app import app as application
```

5. Click **"Save"** (top right)

### **Step 7b: Set Up Gemini API Key (for AI Narrator)** 🤖

The AI Narrator feature uses Google's Gemini API. You need to add your API key to a `config.py` file (which is intentionally **gitignored** so it never reaches GitHub).

#### **Get a free Gemini API key**
1. Visit https://aistudio.google.com/app/apikey
2. Click **"Create API key"**
3. Copy the key (starts with `AI...`)

#### **Create `config.py` on PythonAnywhere**

In the Bash console:

```bash
cd ~/12SE_True_Love_AI
nano config.py
```

Paste this (replace with your actual key):

```python
GEMINI_API_KEY = "AI...your-real-key-here..."
```

Save and exit: `Ctrl+O`, `Enter`, `Ctrl+X`.

#### **Verify**

```bash
python -c "import ai_narrator; print('AI Narrator available:', ai_narrator.is_available())"
```

Should print: `AI Narrator available: True`

> **🛡️ Graceful degradation:** If you skip this step, the app still works perfectly — the sparkle icon just won't appear on predictions. You can add the key later anytime.

### **Step 8: Configure Static Files**

This makes CSS and other static files load fast.

On the Web tab, scroll to **"Static files"** section and add:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/trueloveai/12SE_True_Love_AI/static/` |

Click **"Add a new static file mapping"** if there's no row, then enter the values.

### **Step 9: Reload Your Web App**

Scroll to the top of the Web tab and click the big green **"Reload trueloveai.pythonanywhere.com"** button.

### **Step 10: Visit Your Site!** 🎉

Open: https://trueloveai.pythonanywhere.com/

You should see your True Love AI app running live!

---

## 🔄 Updating After Code Changes (Do This Each Update)

Once code is pushed to GitHub, PythonAnywhere needs to **pull** the changes and **reload** the web app. This is a 30-second process.

### ⚡ Quick Update Workflow (3 Steps)

#### **Step 1: On your local machine**

Make changes → commit → push (you already do this):

```powershell
git add .
git commit -m "Your changes"
git push
```

#### **Step 2: On PythonAnywhere Bash console**

```bash
cd ~/12SE_True_Love_AI
git pull
```

#### **Step 3: Reload the web app**

Two ways to reload:

**Option A: From the Web tab** (easier)
- Go to https://www.pythonanywhere.com/user/trueloveai/webapps/
- Click the green **"Reload trueloveai.pythonanywhere.com"** button

**Option B: From Bash** (faster)
```bash
touch /var/www/trueloveai_pythonanywhere_com_wsgi.py
```
This "touches" the WSGI file, triggering an auto-reload.

✅ That's it! Your changes are now live at https://trueloveai.pythonanywhere.com/

---

### 🎯 Special Cases

#### **If you changed `requirements.txt`** (added/upgraded packages)

Add a `pip install` step:

```bash
workon trueloveai-venv
cd ~/12SE_True_Love_AI
git pull
pip install -r requirements.txt
```

Then reload.

#### **If you retrained models locally** (`models.pkl` changed)

**Option 1: Pull the new pickle (easy)**
```bash
cd ~/12SE_True_Love_AI
git pull
```
Then reload. Done.

**Option 2: Retrain on PythonAnywhere** (cleaner)
- Visit https://trueloveai.pythonanywhere.com/admin
- Click **"🔄 Retrain Models"** button
- Done — no Bash needed

#### **If changes don't appear after reload**
- Clear your browser cache (Ctrl+Shift+R)
- Check the error logs (Web tab → "Log files")

---

### 🚀 One-Liner for Future Updates

You can do everything in one command on PythonAnywhere Bash:

```bash
cd ~/12SE_True_Love_AI && git pull && touch /var/www/trueloveai_pythonanywhere_com_wsgi.py
```

Save this as a reminder! 🎯

---

### 📝 Update Action Cheat Sheet

| What Changed | Action Needed |
|--------------|---------------|
| HTML/CSS/Python code | `git pull` + reload |
| `requirements.txt` | `git pull` + `pip install` + reload |
| `models.pkl` | `git pull` + reload, OR click retrain button |
| `data.csv` | `git pull` + retrain models |

---

## 🛠️ Troubleshooting

### **Site shows "Something went wrong" / 500 error**

1. Go to **Web** tab
2. Scroll to **"Log files"** section
3. Click the **error log** link
4. Read the error at the bottom (most recent entry)

Common fixes:
- **ModuleNotFoundError:** Run `pip install -r requirements.txt` in the virtualenv
- **TemplateNotFound:** Check that source code path is correct
- **InconsistentVersionWarning (sklearn):** Run `python -c "from ml_engine import TrueLovePredictor; p = TrueLovePredictor(); p.train(); p.save_models()"` to regenerate `models.pkl` on PythonAnywhere

### **CSS/styling not loading**

- Check Static Files mapping is set: `/static/` → `/home/trueloveai/12SE_True_Love_AI/static/`
- Reload web app

### **Changes not appearing**

- Did you click the **Reload** button on the Web tab? PythonAnywhere caches everything until you reload.

### **Charts not rendering on admin page**

- Charts use matplotlib — should work on PythonAnywhere by default
- If issue persists, retrain models: click "🔄 Retrain Models" button on the admin dashboard

### **`pip install` stuck on "Preparing metadata (pyproject.toml)..."**

This means pip is trying to **compile pandas/numpy from source** — very slow on free tier (10-20 mins) and may hang indefinitely.

**Fix:** Cancel with `Ctrl+C` and recreate the venv with `--system-site-packages`:

```bash
deactivate
rmvirtualenv trueloveai-venv   # or: rm -rf ~/.virtualenvs/trueloveai-venv (faster)
mkvirtualenv --python=/usr/bin/python3.13 --system-site-packages trueloveai-venv
cd ~/12SE_True_Love_AI
pip install Flask==3.0.3
```

This inherits PythonAnywhere's pre-built numpy/pandas/matplotlib/scikit-learn — instant setup.

### **Need to retrain models on PythonAnywhere**

Use the admin dashboard's **"🔄 Retrain Models"** button, or run in Bash:

```bash
workon trueloveai-venv
cd ~/12SE_True_Love_AI
python -c "from ml_engine import TrueLovePredictor; p = TrueLovePredictor(); p.train(); p.save_models()"
```

Then reload the web app.

---

## 📦 Environment Versions (Already Aligned)

Your local and PythonAnywhere environments match:

| Package | Version |
|---------|---------|
| Python | 3.13 |
| Flask | 3.0.3 |
| scikit-learn | 1.6.0 |
| pandas | 2.2.2 |
| numpy | 2.1.0 |
| matplotlib | 3.9.2 |

All pinned in `requirements.txt`.

---

## 🔒 Security Notes

- The admin dashboard at `/admin` is currently **publicly accessible** with no authentication
- For a production deployment, consider adding password protection
- The CSV training data (`data.csv`) is included in the repo — make sure no real student data is in it!

---

## 🎓 Free vs. Paid PythonAnywhere

**Free tier limits:**
- 1 web app
- 512 MB disk space (plenty for this project)
- Custom domain not supported (must use `trueloveai.pythonanywhere.com`)
- App goes to sleep after 3 months of inactivity (just log in to keep it active)

**Paid tier perks (if needed):**
- Always-on tasks
- Custom domains
- More CPU/storage

For this educational project, **free tier is perfect**.

---

## 📚 Useful PythonAnywhere Commands

```bash
# List your virtualenvs
lsvirtualenv

# Switch to a virtualenv
workon trueloveai-venv

# Deactivate virtualenv
deactivate

# Check Python version
python --version

# View installed packages
pip list

# Disk usage
du -sh ~/12SE_True_Love_AI
```

---

## 🎯 Quick Reference Card

**Your URLs:**
- Live site: https://trueloveai.pythonanywhere.com/
- Admin dashboard: https://trueloveai.pythonanywhere.com/admin
- Dashboard: https://www.pythonanywhere.com/user/trueloveai/

**Update workflow:**
1. Edit code locally → commit → push to GitHub
2. PythonAnywhere Bash: `cd ~/12SE_True_Love_AI && git pull`
3. Web tab → Reload button

That's the entire deployment loop. 🎉
