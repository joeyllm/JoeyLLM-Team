# 📋 Project Overview

The project is divided into **two main semesters**, each focusing on different stages of the workflow used to build and train language models.

Students will work with:

- large-scale datasets
- machine learning workflows
- GPU compute infrastructure
- model training and fine-tuning

The goal is to learn how modern LLM systems are built **from raw data through to trained models**.

---

# 📊 Semester 1 – Data and Infrastructure

The first semester focuses on **understanding the infrastructure and preparing datasets**.

Key activities include:

### Data Cleaning

Students will work with large web datasets such as **FineWeb**, which are already stored on the project’s remote system.

Tasks include:

- exploring the dataset
- filtering content
- cleaning and normalising text
- preparing data suitable for machine learning

The goal is to produce **high-quality filtered datasets** that can be used for model training.

---

### Dataset Classification

Near the end of the first semester the team will begin building **classification models**.

These classifiers will analyse text and determine characteristics such as:

- country of origin (Australia, US, Canada, UK, etc.)
- regional language patterns
- other useful metadata

These tools help organise large datasets and enable more targeted model training later.

---

# 🤖 Semester 2 – Model Training

The second semester focuses on **training specialised AI models** using the cleaned datasets produced earlier.

Students will experiment with **fine-tuning existing language models** to specialise in different domains.

Examples include:

- regional models (Australian English, Canadian English, etc.)
- domain-specific models (banking, defence, science, hobbies, etc.)

The aim is to understand how datasets shape model behaviour and how specialised models can be built.

---

# 🖥 Compute Infrastructure

The project uses a remote compute environment with:

- **GPU servers**
- **Jupyter Notebook environments**
- large datasets stored locally

The Jupyter environment is primarily intended for:

- building workflows
- testing code
- developing data pipelines

Large training jobs may later be executed on:

- dedicated GPU servers
- clusters with **A100 GPUs**
- external high-performance computing systems.

---

# 🎯 Project Goal

By the end of the project the team will have:

- built tools for **cleaning large web datasets**
- created **text classification models**
- developed **training workflows**
- produced **fine-tuned language models for specialised contexts**

The project is designed to give students **hands-on experience with real-world AI infrastructure and workflows** used in modern language model development.

---

# ⚠️ Important

All project work should be kept inside this repository so that:

- documentation remains organised
- workflows are reproducible
- the project can be easily reviewed.

Keep documentation **short, clear, and written in Markdown (`.md`)** so it can be easily read directly in GitHub.
```

If you want, the next step would be improving this README by adding three things that will make the repo much clearer for students:

1. **A simple architecture diagram** of the pipeline (data → classifiers → fine-tuning).
2. **A "What students will actually build" section** (very helpful for TechLauncher grading).
3. **A 1-paragraph explanation of JoeyLLM itself** so they understand the bigger vision.
