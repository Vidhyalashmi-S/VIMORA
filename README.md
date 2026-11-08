# VIMORA — Chemistry Learning Explorer

**Developed by:** Vidhyalashmi S  
**Program:** B.Tech CSE (AI&ML)  
**Institution:** SRM Institute of Science and Technology

## Features
- Curated educational compound catalogue with live PubChem lookups.
- Formula, molecular mass, IUPAC name, Canonical/Isomeric SMILES, InChI and selected descriptors when available.
- PubChem 2D structure images and interactive 3D models through 3Dmol.js when a 3D conformer is available.
- Reference list of all 118 named elements.
- Chemistry quiz and record-aware study assistant.

## Scope
This student build intentionally uses a curated classroom-safe compound catalogue rather than unrestricted chemical searches. PubChem is extensive, but records vary and not every compound has every property or a 3D conformer.

## Run locally
```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## Deploy
Upload the contents of this folder to GitHub. In Streamlit Community Cloud, create an app, select the repository and branch, and set `app.py` as the main file.

## Data attribution
- Compound records, properties, synonyms and structure files: PubChem / U.S. National Library of Medicine, accessed through PUG REST.
- Molecular rendering: 3Dmol.js.
- Element reference: bundled list of 118 named elements.

Documentation: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest and https://3dmol.org/

VIMORA is an educational student project, not a medical, safety, procurement or laboratory-procedure tool.
