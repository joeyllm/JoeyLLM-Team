## 🚀 The JoeyLLM New Paper Workflow

1. **Hugging Face**: Upload your paper to the JoeyLLM Org. 📦
2. **Zenodo**: Start a new upload at Zenodo. 📑
   - Upload your technical report/paper.
   - Add your ORCID iD: `0009-0007-4917-6727`.
   - Publish to get your new DOI. 🏷️
3. **ORCID**: Log in to your ORCID Dashboard. 🆔
   - Add the new DOI to your "Works" section.
   - This locks the credit to you before anyone else can claim it. 🔒
4. **GitHub**: Paste the new DOI and Hugging Face links into your README. 💻

---

# 📄 LaTeX Workflow (Quick Reminder)

* 📁 create a paper directory
* 🧠 work inside that directory

```bash
mkdir -p ~/Projects/Papers/<paper>
cd ~/Projects/Papers/<paper>
```

---

## 📁 Paper folder layout

```text
<paper>/
  main.tex
  main.pdf
  images/
  references/
  scripts/
  sections/
```

Keep `main.tex` and `main.pdf` at the top level so the same shortcut works everywhere. Put figures in `images/`, background papers and BibTeX files in `references/`, helper scripts in `scripts/`, and optional split-out TeX fragments in `sections/`.

---

## 🆕 New paper

```bash
name=$(basename "$PWD"); cat > main.tex <<EOF
\documentclass{article}
\begin{document}

\title{$name}
\maketitle

\end{document}
EOF
```

---

## 🚀 Run

Build the PDF, open the PDF viewer, and keep rebuilding automatically while you edit:

```bash
latexmk -pdf main.tex && { evince main.pdf >/dev/null 2>&1 & latexmk -pdf -pvc main.tex; }
```

---

## ✏️ Work

* 🧠 open in Vim (or any editor)
* 💾 edit + save → PDF updates automatically

---

## 📦 Setup (if needed)

```bash
sudo apt install texlive-full latexmk evince
```

Yes, that works cleanly.

### Add to `~/.bash_aliases`

```bash
cat >> ~/.bash_aliases <<'EOF'
paper() {
  latexmk -pdf main.tex && { evince main.pdf >/dev/null 2>&1 & latexmk -pdf -pvc main.tex; }
}
EOF
source ~/.bashrc
```

### Use

```bash
paper
```

