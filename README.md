## 📚 README: HealthGPTDemo

### 📥 Installation and Setup Guide

---

#### 🔥 1. Installing `uv` on Different Systems

- **Linux (Ubuntu/Debian):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- **MacOS:**
```bash
brew install uv
```

- **Windows (via Scoop):**
```powershell
scoop install uv
```

- **Windows (via Chocolatey):**
```powershell
choco install uv
```

---

#### 📦 2. Project Initialization and Configuration

1. **Clone the Repository:**
```bash
git clone <REPOSITORY_URL>
cd HealthGPTDemo
```

2. **Create a Virtual Environment:**
```bash
uv venv
```

3. **Activate the Environment:**
- **Linux/MacOS:**
```bash
source .venv/bin/activate
```
- **Windows:**
```powershell
.venv\Scripts\activate
```

---

#### 🚀 3. Install Dependencies

```bash
uv sync
```
⚡️ **`uv sync`** installs all dependencies specified in `pyproject.toml` and generates the `uv.lock` file.

---

### 🏃‍♂️ 4. Run the Application

1. **Run the main application:**
```bash
uv run python app.py
```

2. **Or run with custom parameters:**
```bash
uv run python app.py --host 0.0.0.0 --port 8000
```