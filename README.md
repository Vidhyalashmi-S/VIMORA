# VIMORA — Chemistry Learning Explorer

**Developed by:** Vidhyalashmi S  
**Program:** B.Tech CSE (AI&ML)  
**Institution:** SRM Institute of Science and Technology

VIMORA is a Streamlit learning app with a polished chemistry-themed interface, live PubChem compound data for a curated set of classroom examples, 2D structures, interactive 3D molecular views (when PubChem provides a 3D conformer), a compact 118-element periodic table, a quiz, and a record-aware study assistant.

## Important scope note
No single app can guarantee coverage of *every* chemical compound in existence. PubChem is a large, continually updated database, but its records vary in completeness. This starter intentionally limits the searchable compound examples to a small classroom-safe allowlist; it does **not** provide unrestricted search for drugs, intoxicants, or hazardous substances. The element reference lists all 118 named elements for general study.

## Run locally
1. Install Python 3.10 or newer.
2. Extract this ZIP.
3. Open a terminal in the `vimora` folder.
4. Run:
   ```bash
   pip install -r requirements.txt
   python -m streamlit run app.py
   ```

## Deploy with GitHub + Streamlit Community Cloud
1. Create a new GitHub repository named `vimora`.
2. Upload the contents of this folder (not the ZIP file itself).
3. Open Streamlit Community Cloud and connect your GitHub account.
4. Choose **Create app**, select your repository, branch, and `app.py` as the main file, then deploy.

## Data and credits
- Compound records, properties, synonyms, 2D images and available 3D records: **PubChem / U.S. National Library of Medicine**, accessed through PUG REST.
- Interactive molecular viewer: 3Dmol.js loaded from its public CDN.
- Element names, symbols, atomic numbers and approximate atomic masses are bundled as a compact reference dataset.

PubChem PUG REST documentation: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest

## Current features
- Compound search across the included educational allowlist.
- Formula, molecular mass, IUPAC name, SMILES, InChIKey, selected descriptors and hydrogen-bond counts when available.
- PubChem 2D depiction and interactive 3D model where a 3D conformer is available.
- 118-element periodic-table reference with filtering.
- Quick chemistry quiz.
- Rule-based study assistant that explains facts returned for the selected record.

## Notes
- An internet connection is required for live PubChem records and the 3D viewer.
- Some PubChem records do not contain every property or a 3D conformer.
- Applications and industrial contexts are not automatically inferred: consult authoritative sources for verified, source-specific uses.
- This project is an educational reference, not medical, safety, procurement or laboratory-procedure advice.
