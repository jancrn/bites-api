# bites-api

## Prerequisites/ Setup

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create a virtual environment

```bash
uv venv
```

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 4. Run the development server

```bash
fastapi dev main.py
```

## When adding a new dependency

### 1. Add the dependency to `requirements.txt

```bash
uv pip freeze --all > requirements.txt
```

### 2. Tell your fellow developers to update their dependencies

```bash
pip install -r requirements.txt
```
