# AlphaFold Database Usage Guide

## Table of Contents

1. [Searching and Retrieving Predictions](#1-searching-and-retrieving-predictions)
2. [Downloading Structure Files](#2-downloading-structure-files)
3. [Working with Confidence Metrics](#3-working-with-confidence-metrics)
4. [Parsing Structures with BioPython](#4-parsing-structures-with-biopython)
5. [Batch Processing Multiple Proteins](#5-batch-processing-multiple-proteins)
6. [Bulk Data Access via Google Cloud](#6-bulk-data-access-via-google-cloud)
7. [3D-Beacons API Alternative](#7-3d-beacons-api-alternative)

---

## 1. Searching and Retrieving Predictions

### Using Biopython (Recommended)

```python
from Bio.PDB import alphafold_db

# Get all predictions for a UniProt accession
predictions = list(alphafold_db.get_predictions("P00520"))

# Download structure file (mmCIF format)
for prediction in predictions:
    cif_file = alphafold_db.download_cif_for(prediction, directory="./structures")
    print(f"Downloaded: {cif_file}")

# Get Structure objects directly
from Bio.PDB import MMCIFParser
structures = list(alphafold_db.get_structural_models_for("P00520"))
```

### Direct REST API

```python
import requests

uniprot_id = "P00520"
api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
response = requests.get(api_url)
prediction_data = response.json()

alphafold_id = prediction_data[0]['entryId']
print(f"AlphaFold ID: {alphafold_id}")
```

### Finding UniProt Accessions from Protein Name

```python
import urllib.parse, urllib.request

def get_uniprot_ids(query, query_type='PDB_ID'):
    url = 'https://www.uniprot.org/uploadlists/'
    params = {
        'from': query_type,
        'to': 'ACC',
        'format': 'txt',
        'query': query
    }
    data = urllib.parse.urlencode(params).encode('ascii')
    with urllib.request.urlopen(urllib.request.Request(url, data)) as response:
        return response.read().decode('utf-8').splitlines()

protein_ids = get_uniprot_ids("hemoglobin", query_type="GENE_NAME")
```

---

## 2. Downloading Structure Files

```python
import requests

alphafold_id = "AF-P00520-F1"
version = "v4"

# Model coordinates (mmCIF)
model_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-model_{version}.cif"
response = requests.get(model_url)
with open(f"{alphafold_id}.cif", "w") as f:
    f.write(response.text)

# Confidence scores (JSON)
confidence_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-confidence_{version}.json"
confidence_data = requests.get(confidence_url).json()

# Predicted Aligned Error (JSON)
pae_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-predicted_aligned_error_{version}.json"
pae_data = requests.get(pae_url).json()

# PDB format alternative
pdb_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-model_{version}.pdb"
response = requests.get(pdb_url)
with open(f"{alphafold_id}.pdb", "wb") as f:
    f.write(response.content)
```

---

## 3. Working with Confidence Metrics

### pLDDT Scores

```python
import requests

alphafold_id = "AF-P00520-F1"
confidence_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-confidence_v4.json"
confidence = requests.get(confidence_url).json()

plddt_scores = confidence['confidenceScore']
high_confidence_residues = [i for i, score in enumerate(plddt_scores) if score > 90]
print(f"High confidence residues: {len(high_confidence_residues)}/{len(plddt_scores)}")
```

### PAE Matrix Visualization

```python
import numpy as np
import matplotlib.pyplot as plt
import requests

pae_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-predicted_aligned_error_v4.json"
pae = requests.get(pae_url).json()

pae_matrix = np.array(pae['distance'])
plt.figure(figsize=(10, 8))
plt.imshow(pae_matrix, cmap='viridis_r', vmin=0, vmax=30)
plt.colorbar(label='PAE (Å)')
plt.title(f'Predicted Aligned Error: {alphafold_id}')
plt.xlabel('Residue')
plt.ylabel('Residue')
plt.savefig(f'{alphafold_id}_pae.png', dpi=300, bbox_inches='tight')
# Low PAE (<5 Å) = confident relative positioning
# High PAE (>15 Å) = uncertain domain arrangements
```

---

## 4. Parsing Structures with BioPython

### Extract Coordinates and Contacts

```python
from Bio.PDB import MMCIFParser
import numpy as np
from scipy.spatial.distance import pdist, squareform

parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("protein", "AF-P00520-F1-model_v4.cif")

coords = []
for model in structure:
    for chain in model:
        for residue in chain:
            if 'CA' in residue:
                coords.append(residue['CA'].get_coord())

coords = np.array(coords)
print(f"Structure has {len(coords)} residues")

distance_matrix = squareform(pdist(coords))
contacts = np.where((distance_matrix > 0) & (distance_matrix < 8))
print(f"Number of contacts: {len(contacts[0]) // 2}")
```

### Extract pLDDT from B-factors

AlphaFold stores pLDDT scores in the B-factor column of structure files:

```python
from Bio.PDB import MMCIFParser

parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("protein", "AF-P00520-F1-model_v4.cif")

plddt_scores = []
for model in structure:
    for chain in model:
        for residue in chain:
            if 'CA' in residue:
                plddt_scores.append(residue['CA'].get_bfactor())

high_conf_regions = [(i, score) for i, score in enumerate(plddt_scores, 1) if score > 90]
print(f"High confidence residues: {len(high_conf_regions)}")
```

---

## 5. Batch Processing Multiple Proteins

```python
from Bio.PDB import alphafold_db
import pandas as pd
import numpy as np
import requests

uniprot_ids = ["P00520", "P12931", "P04637"]
results = []

for uniprot_id in uniprot_ids:
    try:
        predictions = list(alphafold_db.get_predictions(uniprot_id))
        if predictions:
            pred = predictions[0]
            cif_file = alphafold_db.download_cif_for(pred, directory="./batch_structures")

            alphafold_id = pred['entryId']
            conf_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-confidence_v4.json"
            conf_data = requests.get(conf_url).json()

            plddt_scores = conf_data['confidenceScore']
            avg_plddt = np.mean(plddt_scores)
            high_conf_fraction = sum(1 for s in plddt_scores if s > 90) / len(plddt_scores)

            results.append({
                'uniprot_id': uniprot_id,
                'alphafold_id': alphafold_id,
                'avg_plddt': avg_plddt,
                'high_conf_fraction': high_conf_fraction,
                'length': len(plddt_scores)
            })
    except Exception as e:
        print(f"Error processing {uniprot_id}: {e}")

df = pd.DataFrame(results)
print(df)
```

---

## 6. Bulk Data Access via Google Cloud

### Google Cloud Storage (gsutil)

```bash
# List available data
gsutil ls gs://public-datasets-deepmind-alphafold-v4/

# Download entire proteomes (by taxonomy ID)
gsutil -m cp gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-9606-*.tar .

# Download specific files
gsutil cp gs://public-datasets-deepmind-alphafold-v4/accession_ids.csv .
```

### Download by Species (Python)

```python
import subprocess

def download_proteome(taxonomy_id, output_dir="./proteomes"):
    """Download all AlphaFold predictions for a species"""
    if not isinstance(taxonomy_id, int):
        raise ValueError("taxonomy_id must be an integer")
    pattern = f"gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-{taxonomy_id}-*_v4.tar"
    subprocess.run(["gsutil", "-m", "cp", pattern, f"{output_dir}/"], check=True)

download_proteome(83333)  # E. coli (tax ID: 83333)
download_proteome(9606)   # Human (tax ID: 9606)
```

### BigQuery Metadata Access

```python
from google.cloud import bigquery

client = bigquery.Client()

query = """
SELECT
  entryId,
  uniprotAccession,
  organismScientificName,
  globalMetricValue,
  fractionPlddtVeryHigh
FROM `bigquery-public-data.deepmind_alphafold.metadata`
WHERE organismScientificName = 'Homo sapiens'
  AND fractionPlddtVeryHigh > 0.8
LIMIT 100
"""

results = client.query(query).to_dataframe()
print(f"Found {len(results)} high-confidence human proteins")
```

BigQuery free tier: 1 TB processed data/month.

---

## 7. 3D-Beacons API Alternative

AlphaFold can also be accessed via the 3D-Beacons federated API, which aggregates multiple structure providers:

```python
import requests

uniprot_id = "P00520"
url = f"https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/{uniprot_id}.json"
response = requests.get(url)
data = response.json()

# Filter for AlphaFold structures
af_structures = [s for s in data['structures'] if s['provider'] == 'AlphaFold DB']
print(f"Found {len(af_structures)} AlphaFold structures")
```
