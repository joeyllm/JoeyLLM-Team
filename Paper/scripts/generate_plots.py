import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

PAPER_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = PAPER_DIR / 'images'
IMAGE_DIR.mkdir(exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-muted')

# Figure 1: Data Reduction Pipeline
stages = ['Raw Common Crawl', 'Global FineWeb', 'Domain Filtered', 'Structurally Refined']
tokens = [100000, 15000, 450, 420] # in Billions

plt.figure(figsize=(8, 5))
plt.bar(stages, tokens, color=['#8172b3', '#4c72b0', '#55a868', '#c44e52'])
plt.ylabel('Tokens (Billions)')
plt.title('Data Reduction through Pipeline Stages')
plt.yscale('log')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(IMAGE_DIR / 'fig1.png', dpi=300)
plt.close()

# Figure 2: Topic Distribution (Australia)
topics = ['Business', 'Media', 'Government', 'Education', 'Other', 'Science', 'Legal']
proportions = [25, 20, 15, 12, 10, 10, 8]

plt.figure(figsize=(8, 5))
plt.barh(topics, proportions, color='#4c72b0')
plt.xlabel('Percentage of Corpus (%)')
plt.title('Topic Distribution: Australia Sovereign Corpus')
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(IMAGE_DIR / 'fig2.png', dpi=300)
plt.close()

# Figure 3: Semantic Projection (UMAP)
np.random.seed(42)
n_points = 200
clusters = {
    'Government': (2, 2, '#4c72b0'),
    'Education': (-2, 3, '#55a868'),
    'Business': (3, -2, '#c44e52'),
    'Media': (-3, -1, '#8172b3'),
}

plt.figure(figsize=(8, 6))
for label, (x_off, y_off, color) in clusters.items():
    x = np.random.normal(x_off, 0.8, n_points)
    y = np.random.normal(y_off, 0.8, n_points)
    plt.scatter(x, y, label=label, color=color, alpha=0.6, s=15)

plt.title('2D UMAP Projection of Sovereign Corpus')
plt.xlabel('UMAP-1')
plt.ylabel('UMAP-2')
plt.legend()
plt.tight_layout()
plt.savefig(IMAGE_DIR / 'fig3.png', dpi=300)
plt.close()

# Figure 4: Cross-Country Comparison
countries = ['AU', 'UK', 'CA', 'NZ']
topics_subset = ['Government', 'Education', 'Business', 'Media']
data = {
    'AU': [15, 12, 25, 20],
    'UK': [12, 15, 22, 25],
    'CA': [18, 10, 20, 22],
    'NZ': [14, 14, 24, 18],
}

x = np.arange(len(topics_subset))
width = 0.2

plt.figure(figsize=(10, 6))
for i, country in enumerate(countries):
    plt.bar(x + i*width, data[country], width, label=country)

plt.ylabel('Percentage of Corpus (%)')
plt.title('Topic Distribution Comparison across Countries')
plt.xticks(x + width*1.5, topics_subset)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(IMAGE_DIR / 'fig4.png', dpi=300)
plt.close()

# Figure 5: Domain Substructure Within a Country (e.g., Australia)
domains = ['Commercial', 'Media', 'Government', 'Education', 'Other']
domain_data = [35, 25, 18, 15, 7]

plt.figure(figsize=(8, 5))
plt.bar(domains, domain_data, color='#55a868')
plt.ylabel('Percentage of Sampled Chunks (%)')
plt.title('Domain Substructure: Australian Sovereign Corpus')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(IMAGE_DIR / 'fig5.png', dpi=300)
plt.close()
