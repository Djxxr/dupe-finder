<div align="center">

<h1 align="center">Dupe-Finder</h1>

<p align="center">
  <em>A powerful and fast command-line tool to find and remove duplicate files.</em>
</p>

<p align="center">
  <img src="https://github.com/djxxr/dupe-finder/raw/main/demo.gif" alt="Dupe-Finder Demo">
</p>

<p align="center">
    <a href="https://github.com/djxxr/dupe-finder/blob/main/LICENSE">
        <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
    </a>
    <a href="#">
        <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python Version">
    </a>
     <a href="#">
        <img src="https://img.shields.io/badge/platform-windows-blue.svg" alt="Platform: Windows">
    </a>
</p>

</div>

---

### **Table of Contents**

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
  - [For End-Users (Executable)](#for-end-users-executable)
  - [For Developers (From Source)](#for-developers-from-source)
- [Building from Source](#building-from-source)
- [Technology Stack](#technology-stack)
- [License](#license)

---

### **Introduction**

**Dupe-Finder** is an interactive command-line utility designed to efficiently scan directories for content-identical files. By using a two-phase detection algorithm (size pre-filter followed by SHA-256 hash comparison), it accurately identifies duplicates, helping users reclaim disk space and organize their file systems.

The application is built with a focus on user experience, featuring a menu-driven interface that makes it accessible even to users less familiar with command-line tools.

---

### **Key Features**

- **Accurate Duplicate Detection:** Employs a robust size and SHA-256 hashing algorithm to ensure files are true duplicates before reporting them.
- **Interactive TUI:** A clean, menu-driven Text-based User Interface allows for easy navigation and operation without complex commands.
- **System-Aware Browse:** Automatically detects mounted disk drives and allows for Browse top-level directories, simplifying path selection.
- **Safe Deletion Module:** An interactive deletion prompt with a "select all but oldest" quick-action prevents accidental removal of all file copies and requires user confirmation.
- **Polished Visuals:** Utilizes the Rich library for clear, color-coded tables, progress bars, and user prompts.
- **Standalone Executable:** Can be easily built into a single `.exe` file for distribution to non-technical users, with no external dependencies required.

---

### **Getting Started**

#### **For End-Users (Executable)**

The easiest way to use Dupe-Finder is by downloading the pre-built executable for Windows.

1.  Navigate to the **[Releases](https://github.com/djxxr/dupe-finder/releases)** page of this repository.
2.  Download the latest `dupe-finder.exe` from the "Assets" section.
3.  Run the file. No installation is needed.

#### **For Developers (From Source)**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/djxxr/dupe-finder.git](https://github.com/djxxr/dupe-finder.git)
    ```
2.  **Navigate to the project directory and set up the environment:**
    ```bash
    cd dupe-finder
    python -m venv venv
    venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    python src/main.py
    ```

---

### **Building from Source**

To build the standalone `.exe` yourself, run the included build script. It will handle dependency checks and the PyInstaller compilation process automatically.

```bash
build.bat