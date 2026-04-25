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

### **Step 3: Create a Virtual Environment**

```bash
mkvirtualenv --python=/usr/bin/python3.13 trueloveai-venv
```

This activates automatically. Your prompt will now show `(trueloveai-venv)`.

### **Step 4: Install Dependencies**

```bash
pip install -r requirements.txt
```

Wait ~2 minutes for everything to install.

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

After you push changes to GitHub, run these on PythonAnywhere:

### **Quick Update (Bash Console)**

```bash
workon trueloveai-venv
cd ~/12SE_True_Love_AI
git pull
pip install -r requirements.txt   # only if requirements changed
```

### **Then Reload the Web App**

- Go to **Web** tab
- Click the green **"Reload"** button

That's it! Your changes are live.

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
