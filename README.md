# School Management System - Database Project 🎓

## 📌 Project Overview
This project is a comprehensive School Management System developed for the Introduction to Database course at National Economics University (NEU). It features a robust MySQL backend architecture and a Python-based interactive terminal frontend for database administration.

## 📁 Repository Contents
* **`database_setup.sql`**: The core SQL script containing the physical creation of tables (normalized to 3NF), Foreign Key constraints, advanced Views (e.g., `ViewTopStudents`), and Triggers.
* **`generate.py`**: A Python automation script that populates the database with exactly 510 mock records per entity, featuring simulated "Missing Data" to test system robustness.
* **`app.py`**: The main Python Command Line Interface (CLI) application allowing administrators to execute CRUD operations safely.
* **`Database_Report_Minh.pdf`**: The official, comprehensive project report compiled in LaTeX, detailing the system architecture, EER Diagram, practical scenarios, and evaluation.

## 🛠️ Technology Stack
* **Database:** MySQL (Server & Workbench)
* **Frontend/Automation:** Python (`mysql-connector-python`)
* **Documentation:** LaTeX (Overleaf)

## 🚀 Core Features
1. **Missing Data Handling:** A robust two-layered defense mechanism (SQL safeguards + Python frontend flexibility) to actively identify and patch incomplete records (e.g., missing grades or contact info).
2. **Advanced Database Objects:** Automated GPA calculation on a 4.0 scale via User-Defined Functions (UDFs) and comprehensive audit logging via Triggers.
3. **Interactive Terminal App:** A lightweight 10-option menu for easy, intuitive database management without the need to write direct SQL queries.

## ⚙️ How to Run
1. Import and execute the `database_setup.sql` script in MySQL Workbench to initialize the schemas, tables, views, and triggers.
2. Run `python generate.py` in your terminal to populate the database with mock data.
3. Run `python app.py` to launch the interactive management menu.

---
**Author:** Le Trieu Quang Minh - Class DS66A (NEU)