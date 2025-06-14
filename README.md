<div align="center">

<h1 align="center">Dupe-Finder</h1>

<p align="center">
  <em>A powerful and fast CLI tool to find and remove duplicate files.</em>
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
- [Getting Started for Developers](#getting-started-for-developers)
  - [Prerequisites](#prerequisites)
  - [Setup and Run](#setup-and-run)
- [For End-Users (The Easy Way)](#for-end-users-the-easy-way)
- [Technology Stack](#technology-stack)
- [License](#license)

---

### **Introduction**

**Dupe-Finder** is an interactive command-line utility designed to efficiently scan directories for content-identical files. By using a two-phase detection algorithm (size pre-filter followed by SHA-256 hash comparison), it accurately identifies duplicates, helping users reclaim disk space and organize their file systems.

The application is built with a focus on user experience, featuring a menu-driven interface that makes it accessible even to users less familiar with command-line tools.

---

### **Key Features**

- **Accurate Duplicate Detection:** Employs a robust size and SHA-256 hashing algorithm to ensure files are true duplicates before reporting them.
- **Interactive TUI:** A user-friendly, menu-driven Text-based User Interface allows for easy navigation and operation without complex commands.
- **System-Aware Browse:** Automatically detects mounted disk drives and allows for Browse top-level directories, simplifying path selection.
- **Safe Deletion Module:** An interactive deletion prompt with a "select all but oldest" quick-action prevents accidental removal of all file copies and requires user confirmation.
- **Polished Visuals:** Utilizes the Rich library for clear, color-coded tables, progress bars, and user prompts.
- **Standalone Executable:** Comes with a one-click build script to create a distributable `.exe` for end-users.

---

### **Getting Started for Developers**

This section describes how to set up the project to run from source code.

#### **Prerequisites**

- **Python**: Version 3.8 or higher
- **Pip**: Python package installer (usually comes with Python)
- **Git**: For cloning the repository.

#### **Setup and Run**

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

### **For End-Users (The Easy Way)**

To get started, you need to build the executable from the source code.

1.  Run the `build.bat` script located in the main project folder. This will automatically process the source code and create the executable file.
2.  Once the script is finished, you will find `dupe-finder.exe` inside the newly created `/dist` folder.
3.  Run `dupe-finder.exe` to start the application. No installation is needed.

---

### **Technology Stack**

- **Python**: Core programming language.
- **Rich**: For all styled terminal output (tables, colors, progress bars).
- **Questionary**: For building the interactive TUI menus and prompts.
- **psutil**: For cross-platform detection of system disk drives.
- **PyFiglet**: For the startup ASCII art banner.
- **PyInstaller**: For packaging the application into a single executable.

---

### **License**

This project is distributed under the MIT License. See the `LICENSE` file for more information.