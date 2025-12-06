# Circle Taxi

A taxi booking application built with Python and Tkinter.

## Requirements

* Python **3.11 or higher**
* On **Windows**, CairoSVG requires a Cairo DLL (see instructions below)

---

## Installation

### 1. Unzip the archive

```bash
unzip tkinter.zip
cd tkinter
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

* **Linux/macOS:**

  ```bash
  source venv/bin/activate
  ```

* **Windows:**

  ```bash
  venv\Scripts\activate
  ```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ⚠️ Windows-Only: Install Cairo DLL (Needed for CairoSVG)

CairoSVG requires native Cairo libraries on Windows.
If Cairo is missing, you'll see an error like:

```
OSError: no library called "cairo" was found
```

### Fix

1. Download the prebuilt **self-contained `cairo.dll`** (64-bit) from:
   [https://github.com/preshing/cairo-windows/releases](https://github.com/preshing/cairo-windows/releases)

2. Copy **cairo.dll** into your virtual environment:

```
venv\Scripts\
```

3. Restart your terminal and activate the venv again.

After this, CairoSVG will work correctly on Windows.

---

## Running the Application

Run the main application:

```bash
python -m app.main
```
