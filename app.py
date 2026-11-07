
import streamlit as st
import requests, html, random, re
import streamlit.components.v1 as components

st.set_page_config(page_title="VIMORA | Chemistry Explorer", page_icon="⚗️", layout="wide")

# VIMORA — educational chemistry explorer. Search is intentionally limited to a
# curated set of classroom-safe substances; it is not a chemical procurement tool.
PUBCHEM = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
SAFE_COMPOUNDS = {
    "water": "Water", "glucose": "D-Glucose", "sucrose": "Sucrose",
    "citric acid": "Citric acid", "sodium chloride": "Sodium chloride",
    "calcium carbonate": "Calcium carbonate", "cellulose": "Cellulose",
    "glycine": "Glycine", "alanine": "L-Alanine", "starch": "Starch",
    "ascorbic acid": "Ascorbic acid", "lactic acid": "Lactic acid",
    "urea": "Urea", "ethanolamine": "Ethanolamine"
}
ELEMENTS = [
("H","Hydrogen",1,"1.008","Nonmetal"),("He","Helium",2,"4.0026","Noble gas"),
("Li","Lithium",3,"6.94","Alkali metal"),("Be","Beryllium",4,"9.0122","Alkaline earth metal"),
("B","Boron",5,"10.81","Metalloid"),("C","Carbon",6,"12.011","Nonmetal"),
("N","Nitrogen",7,"14.007","Nonmetal"),("O","Oxygen",8,"15.999","Nonmetal"),
("F","Fluorine",9,"18.998","Halogen"),("Ne","Neon",10,"20.180","Noble gas"),
("Na","Sodium",11,"22.990","Alkali metal"),("Mg","Magnesium",12,"24.305","Alkaline earth metal"),
("Al","Aluminium",13,"26.982","Post-transition metal"),("Si","Silicon",14,"28.085","Metalloid"),
("P","Phosphorus",15,"30.974","Nonmetal"),("S","Sulfur",16,"32.06","Nonmetal"),
("Cl","Chlorine",17,"35.45","Halogen"),("Ar","Argon",18,"39.948","Noble gas"),
("K","Potassium",19,"39.098","Alkali metal"),("Ca","Calcium",20,"40.078","Alkaline earth metal"),
("Sc","Scandium",21,"44.956","Transition metal"),("Ti","Titanium",22,"47.867","Transition metal"),
("V","Vanadium",23,"50.942","Transition metal"),("Cr","Chromium",24,"51.996","Transition metal"),
("Mn","Manganese",25,"54.938","Transition metal"),("Fe","Iron",26,"55.845","Transition metal"),
("Co","Cobalt",27,"58.933","Transition metal"),("Ni","Nickel",28,"58.693","Transition metal"),
("Cu","Copper",29,"63.546","Transition metal"),("Zn","Zinc",30,"65.38","Transition metal"),
("Ga","Gallium",31,"69.723","Post-transition metal"),("Ge","Germanium",32,"72.630","Metalloid"),
("As","Arsenic",33,"74.922","Metalloid"),("Se","Selenium",34,"78.971","Nonmetal"),
("Br","Bromine",35,"79.904","Halogen"),("Kr","Krypton",36,"83.798","Noble gas"),
("Rb","Rubidium",37,"85.468","Alkali metal"),("Sr","Strontium",38,"87.62","Alkaline earth metal"),
("Y","Yttrium",39,"88.906","Transition metal"),("Zr","Zirconium",40,"91.224","Transition metal"),
("Nb","Niobium",41,"92.906","Transition metal"),("Mo","Molybdenum",42,"95.95","Transition metal"),
("Tc","Technetium",43,"98","Transition metal"),("Ru","Ruthenium",44,"101.07","Transition metal"),
("Rh","Rhodium",45,"102.91","Transition metal"),("Pd","Palladium",46,"106.42","Transition metal"),
("Ag","Silver",47,"107.87","Transition metal"),("Cd","Cadmium",48,"112.41","Transition metal"),
("In","Indium",49,"114.82","Post-transition metal"),("Sn","Tin",50,"118.71","Post-transition metal"),
("Sb","Antimony",51,"121.76","Metalloid"),("Te","Tellurium",52,"127.60","Metalloid"),
("I","Iodine",53,"126.90","Halogen"),("Xe","Xenon",54,"131.29","Noble gas"),
("Cs","Caesium",55,"132.91","Alkali metal"),("Ba","Barium",56,"137.33","Alkaline earth metal"),
("La","Lanthanum",57,"138.91","Lanthanide"),("Ce","Cerium",58,"140.12","Lanthanide"),
("Pr","Praseodymium",59,"140.91","Lanthanide"),("Nd","Neodymium",60,"144.24","Lanthanide"),
("Pm","Promethium",61,"145","Lanthanide"),("Sm","Samarium",62,"150.36","Lanthanide"),
("Eu","Europium",63,"151.96","Lanthanide"),("Gd","Gadolinium",64,"157.25","Lanthanide"),
("Tb","Terbium",65,"158.93","Lanthanide"),("Dy","Dysprosium",66,"162.50","Lanthanide"),
("Ho","Holmium",67,"164.93","Lanthanide"),("Er","Erbium",68,"167.26","Lanthanide"),
("Tm","Thulium",69,"168.93","Lanthanide"),("Yb","Ytterbium",70,"173.05","Lanthanide"),
("Lu","Lutetium",71,"174.97","Lanthanide"),("Hf","Hafnium",72,"178.49","Transition metal"),
("Ta","Tantalum",73,"180.95","Transition metal"),("W","Tungsten",74,"183.84","Transition metal"),
("Re","Rhenium",75,"186.21","Transition metal"),("Os","Osmium",76,"190.23","Transition metal"),
("Ir","Iridium",77,"192.22","Transition metal"),("Pt","Platinum",78,"195.08","Transition metal"),
("Au","Gold",79,"196.97","Transition metal"),("Hg","Mercury",80,"200.59","Transition metal"),
("Tl","Thallium",81,"204.38","Post-transition metal"),("Pb","Lead",82,"207.2","Post-transition metal"),
("Bi","Bismuth",83,"208.98","Post-transition metal"),("Po","Polonium",84,"209","Metalloid"),
("At","Astatine",85,"210","Halogen"),("Rn","Radon",86,"222","Noble gas"),
("Fr","Francium",87,"223","Alkali metal"),("Ra","Radium",88,"226","Alkaline earth metal"),
("Ac","Actinium",89,"227","Actinide"),("Th","Thorium",90,"232.04","Actinide"),
("Pa","Protactinium",91,"231.04","Actinide"),("U","Uranium",92,"238.03","Actinide"),
("Np","Neptunium",93,"237","Actinide"),("Pu","Plutonium",94,"244","Actinide"),
("Am","Americium",95,"243","Actinide"),("Cm","Curium",96,"247","Actinide"),
("Bk","Berkelium",97,"247","Actinide"),("Cf","Californium",98,"251","Actinide"),
("Es","Einsteinium",99,"252","Actinide"),("Fm","Fermium",100,"257","Actinide"),
("Md","Mendelevium",101,"258","Actinide"),("No","Nobelium",102,"259","Actinide"),
("Lr","Lawrencium",103,"266","Actinide"),("Rf","Rutherfordium",104,"267","Transition metal"),
("Db","Dubnium",105,"268","Transition metal"),("Sg","Seaborgium",106,"269","Transition metal"),
("Bh","Bohrium",107,"270","Transition metal"),("Hs","Hassium",108,"277","Transition metal"),
("Mt","Meitnerium",109,"278","Unknown"),("Ds","Darmstadtium",110,"281","Unknown"),
("Rg","Roentgenium",111,"282","Unknown"),("Cn","Copernicium",112,"285","Unknown"),
("Nh","Nihonium",113,"286","Unknown"),("Fl","Flerovium",114,"289","Unknown"),
("Mc","Moscovium",115,"290","Unknown"),("Lv","Livermorium",116,"293","Unknown"),
("Ts","Tennessine",117,"294","Halogen"),("Og","Oganesson",118,"294","Noble gas")
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root{--ink:#eaf3f5;--muted:#9bb2ba;--teal:#43d6c5;--blue:#6ba8ff;--panel:#102b36}
.stApp{background:radial-gradient(circle at 12% 0%,#173c49 0,#0a1c27 42%,#07141d 100%);color:var(--ink);font-family:'DM Sans',sans-serif}
h1,h2,h3{font-family:'Manrope',sans-serif;color:#f2fbfc}
.block-container{padding-top:2rem;max-width:1200px}
.hero{padding:28px 30px;border:1px solid #285260;border-radius:22px;background:linear-gradient(120deg,rgba(23,67,77,.94),rgba(13,36,51,.92));margin-bottom:20px}
.eyebrow{color:var(--teal);letter-spacing:2px;font-size:12px;font-weight:700}
.hero h1{font-size:46px;letter-spacing:1px;margin:4px 0}
.hero p{color:#b6cbd0;font-size:16px;max-width:760px}
.card{background:rgba(16,43,54,.86);border:1px solid #254957;border-radius:16px;padding:18px 20px;margin:8px 0}
.metric{font-size:25px;font-weight:800;color:#f4ffff}
.label{font-size:12px;color:#9bb8c0;text-transform:uppercase;letter-spacing:1px}
.small{color:#9bb8c0;font-size:13px}
.pill{display:inline-block;border:1px solid #35706f;color:#75e5d7;background:#123a40;padding:4px 10px;border-radius:30px;font-size:12px;margin:3px}
div.stButton>button{border-radius:10px;border:1px solid #367a7b;background:#17454e;color:#efffff;font-weight:600}
div.stButton>button:hover{border-color:#55d9c9;color:#55d9c9}
[data-testid="stTextInput"] input{background:#102b36;color:#fff;border:1px solid #38606b;border-radius:10px}
[data-testid="stTabs"] button{color:#c6dadd}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

def api_json(url):
    try:
        r=requests.get(url,timeout=18,headers={"User-Agent":"VIMORA-Educational-App/1.0"})
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

@st.cache_data(ttl=3600, show_spinner=False)
def get_compound(name):
    # Only allow approved classroom examples; PubChem supplies the record.
    if name.lower().strip() not in SAFE_COMPOUNDS:
        return None
    encoded=requests.utils.quote(SAFE_COMPOUNDS[name.lower().strip()], safe="")
    p=api_json(f"{PUBCHEM}/compound/name/{encoded}/property/IUPACName,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES,InChIKey,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount,RotatableBondCount/JSON")
    if not p: return None
    try:
        prop=p["PropertyTable"]["Properties"][0]
        cid=prop["CID"]
        syn=api_json(f"{PUBCHEM}/compound/cid/{cid}/synonyms/JSON")
        synonyms=syn.get("InformationList",{}).get("Information",[{}])[0].get("Synonym",[])[:8] if syn else []
        desc=api_json(f"{PUBCHEM}/compound/cid/{cid}/description/JSON")
        descriptions=[]
        if desc:
            for item in desc.get("InformationList",{}).get("Information",[]):
                if item.get("Description"): descriptions.append(item["Description"])
        return {"prop":prop,"cid":cid,"synonyms":synonyms,"description":descriptions[:2]}
    except Exception: return None

def molecule_viewer(cid):
    sdf_url=f"{PUBCHEM}/compound/cid/{cid}/record/SDF?record_type=3d"
    try:
        r=requests.get(sdf_url,timeout=20)
        if r.status_code != 200 or len(r.text)<30: raise ValueError()
        sdf=r.text
        # Pass SDF safely as JSON text into the viewer.
        payload=json.dumps(sdf)
        page=f"""
        <div id="viewer" style="width:100%;height:440px;position:relative;border-radius:14px;overflow:hidden;background:#0b2029"></div>
        <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
        <script>
        const el=document.getElementById('viewer');
        const v=$3Dmol.createViewer(el,{{backgroundColor:'#0b2029'}});
        const sdf={payload};
        v.addModel(sdf,'sdf'); v.setStyle({{}},{{stick:{{radius:0.18}},sphere:{{scale:0.28}}}});
        v.zoomTo(); v.render(); v.zoom(0.9);
        </script>"""
        components.html(page,height=455)
    except Exception:
        st.info("A 3D conformer is not available for this record right now. The 2D PubChem structure is shown instead.")
        st.image(f"{PUBCHEM}/compound/cid/{cid}/PNG?image_size=large",use_container_width=True)

def render_compound(name):
    with st.spinner("Retrieving the compound record from PubChem…"):
        data=get_compound(name)
    if not data:
        st.error("The PubChem record could not be loaded. Check your connection and try again.")
        return
    p=data["prop"]; cid=data["cid"]
    st.markdown(f"## {html.escape(SAFE_COMPOUNDS[name.lower()])} <span class='pill'>PubChem CID {cid}</span>",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    for col,label,val in [(c1,"Molecular formula",p.get("MolecularFormula","—")),(c2,"Molecular mass",str(p.get("MolecularWeight","—"))+" g/mol"),(c3,"H-bond donors",p.get("HBondDonorCount","—")),(c4,"H-bond acceptors",p.get("HBondAcceptorCount","—"))]:
        with col: st.markdown(f"<div class='card'><div class='label'>{label}</div><div class='metric'>{val}</div></div>",unsafe_allow_html=True)
    tab1,tab2,tab3,tab4=st.tabs(["Molecule view","Properties & identifiers","Learn & applications","AI study assistant"])
    with tab1:
        left,right=st.columns([1,1.15])
        with left:
            st.markdown("### 2D structure")
            st.image(f"{PUBCHEM}/compound/cid/{cid}/PNG?image_size=large",use_container_width=True)
            st.caption("2D structure image provided by PubChem.")
        with right:
            st.markdown("### Interactive 3D model")
            molecule_viewer(cid)
            st.caption("Drag to rotate • Scroll to zoom • Use the model to explore spatial arrangement.")
    with tab2:
        rows=[
            ("IUPAC name",p.get("IUPACName","—")),("Canonical SMILES",p.get("ConnectivitySMILES",p.get("CanonicalSMILES","—"))),
            ("Isomeric SMILES",p.get("SMILES",p.get("IsomericSMILES","—"))),("InChIKey",p.get("InChIKey","—")),
            ("XLogP",p.get("XLogP","Not reported")),("Topological polar surface area",str(p.get("TPSA","Not reported"))+" Å²"),
            ("Rotatable bonds",p.get("RotatableBondCount","—")),("PubChem CID",cid)]
        for k,v in rows: st.markdown(f"<div class='card'><div class='label'>{html.escape(k)}</div><div>{html.escape(str(v))}</div></div>",unsafe_allow_html=True)
        st.markdown("**Known synonyms**")
        st.write(", ".join(data["synonyms"]) if data["synonyms"] else "No synonyms returned.")
        st.markdown(f"[Open this record on PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/{cid})")
    with tab3:
        st.markdown("### What is it?")
        st.write((data["description"][0] if data["description"] else "PubChem does not currently provide a concise description for this record.") )
        st.markdown("### Learning notes")
        st.write("Use the molecular formula to count each type of atom. The molecular weight is the average mass per mole. SMILES is a text representation of molecular connectivity; it is useful for cheminformatics tools.")
        st.markdown("### Applications")
        st.info("Applications vary by grade, purity and context. Use a trusted textbook or the linked PubChem record for verified, source-specific application information; this app does not provide handling or use instructions.")
    with tab4:
        st.markdown("### VIMORA learning assistant")
        st.write("Ask a classroom-style question about the displayed formula, mass, bonds or SMILES. The assistant explains the available record; it does not provide instructions for handling or using chemicals.")
        q=st.text_input("Your question",key=f"q_{cid}",placeholder="e.g. What does the molecular formula tell me?")
        if st.button("Ask VIMORA",key=f"ask_{cid}") and q.strip():
            st.info(ai_answer(q,p,SAFE_COMPOUNDS[name.lower()]))
        st.caption("Assistant responses are educational summaries, not laboratory or safety advice.")

def ai_answer(question,p,name):
    q=question.lower()
    formula=p.get("MolecularFormula","")
    mass=p.get("MolecularWeight","")
    smiles=p.get("ConnectivitySMILES",p.get("CanonicalSMILES",""))
    if any(x in q for x in ["smiles","notation"]):
        return f"SMILES is a compact text notation for molecular connectivity. For {name}, the PubChem record lists: {smiles}. It encodes how atoms are connected; it is not a 2D drawing."
    if any(x in q for x in ["mass","weight","molar"]):
        return f"The molecular weight listed for {name} is {mass} g/mol. This is the average mass of one mole of the compound."
    if any(x in q for x in ["formula","atom","element"]):
        return f"The molecular formula is {formula}. It tells you which elements are present and how many atoms of each are in one molecule or formula unit."
    if any(x in q for x in ["bond","connect","structure"]):
        return f"The structure describes how atoms are connected and arranged. The 2D diagram is a simplified connectivity view; the interactive 3D model helps you explore spatial shape. The SMILES record is {smiles}."
    return f"Here is a starting point for {name}: its formula is {formula} and its molecular weight is {mass} g/mol. Try asking about its formula, molecular mass, bonds, structure or SMILES notation."

def periodic_table():
    st.markdown("## Periodic table")
    st.write("Explore all 118 officially named elements. This section is a compact learning reference; it does not provide experimental handling guidance.")
    query=st.text_input("Find an element by name or symbol",key="element_search")
    filtered=[e for e in ELEMENTS if not query or query.lower() in e[0].lower() or query.lower() in e[1].lower()]
    cols=st.columns(6)
    for i,e in enumerate(filtered):
        with cols[i%6]:
            st.markdown(f"<div class='card' style='text-align:center;min-height:105px'><div class='label'>Atomic no. {e[2]}</div><div style='font-size:30px;font-weight:800;color:#55d9c9'>{e[0]}</div><div>{e[1]}</div><div class='small'>{e[3]} u</div></div>",unsafe_allow_html=True)
    if query and len(filtered)==1:
        e=filtered[0]
        st.success(f"{e[1]} ({e[0]}) · Atomic number {e[2]} · Atomic mass {e[3]} u · Classification: {e[4]}")

def quiz():
    st.markdown("## Quick chemistry check")
    questions=[
        ("What does a molecular formula show?",["The colour of a substance","The types and counts of atoms","The boiling point"],1,"A molecular formula lists the elements and atom counts."),
        ("What does SMILES represent?",["Molecular connectivity in text form","A substance's smell","Its laboratory storage"],0,"SMILES is a text notation for molecular structure."),
        ("What is the unit commonly used for molecular weight?",["metres","g/mol","litres"],1,"Molecular weight is commonly expressed in grams per mole."),
        ("How many elements are currently in the periodic table?",["92","108","118"],2,"The periodic table contains 118 named elements.")
    ]
    idx=st.selectbox("Choose a question",range(len(questions)),format_func=lambda x:f"Question {x+1}")
    q,opts,correct,why=questions[idx]
    st.markdown(f"### {q}")
    ans=st.radio("Select your answer",opts,key=f"quiz_{idx}")
    if st.button("Check answer"):
        if opts.index(ans)==correct: st.success("Correct! "+why)
        else: st.warning("Not quite. "+why)

st.markdown("""
<div class="hero">
<div class="eyebrow">A MODERN CHEMISTRY LEARNING SPACE</div>
<h1>VIMORA <span style="color:#43d6c5">⚗</span></h1>
<p>Explore molecular structures, understand chemical properties and build confidence in chemistry — one discovery at a time.</p>
<div class="small">Developed by <b>Vidhyalashmi S</b> · B.Tech CSE (AI&ML) · SRM Institute of Science and Technology</div>
</div>
""",unsafe_allow_html=True)

page=st.sidebar.radio("EXPLORE VIMORA",["Compound explorer","Periodic table","Chemistry quiz","About VIMORA"])
st.sidebar.markdown("---")
st.sidebar.caption("Data source: PubChem (NIH) for compound records. Element reference: curated periodic-table dataset.")
if page=="Compound explorer":
    st.markdown("## Compound explorer")
    st.write("Search the classroom-safe example library. Compound properties and structure records are retrieved live from PubChem.")
    search=st.text_input("Search a compound",placeholder="Try water, glucose, sucrose, citric acid…")
    if search:
        key=search.lower().strip()
        if key in SAFE_COMPOUNDS:
            render_compound(key)
        else:
            st.warning("This learning version searches a curated set of classroom examples rather than unrestricted chemical records. Try one of the examples below.")
    st.markdown("**Quick examples**")
    cols=st.columns(4)
    for i,n in enumerate(SAFE_COMPOUNDS.values()):
        with cols[i%4]:
            if st.button(n,key=f"compound_{i}",use_container_width=True):
                st.session_state["chosen_compound"]=n.lower()
    if st.session_state.get("chosen_compound"):
        render_compound(st.session_state["chosen_compound"])
elif page=="Periodic table":
    periodic_table()
elif page=="Chemistry quiz":
    quiz()
else:
    st.markdown("## About VIMORA")
    st.markdown("""
    <div class="card">
    <h3>Discover. Understand. Explore.</h3>
    <p>VIMORA is a student-built chemistry learning app designed to make chemical information easier to explore through clear property cards, molecular structure views, an interactive 3D viewer and short quizzes.</p>
    <p><b>Creator</b><br>Vidhyalashmi S<br>B.Tech CSE (AI&ML)<br>SRM Institute of Science and Technology</p>
    <p><b>Data attribution</b><br>Compound records are retrieved from PubChem, a resource of the U.S. National Library of Medicine. Data availability and completeness depend on the PubChem record.</p>
    </div>
    """,unsafe_allow_html=True)
    st.markdown("[PubChem database and API documentation](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)")
    st.caption("VIMORA is an educational project. It is not a chemical safety, medical, procurement or laboratory-procedure tool.")
st.markdown("---")
st.markdown("<div class='small' style='text-align:center'>VIMORA · Chemistry, made explorable · Built by Vidhyalashmi S</div>",unsafe_allow_html=True)
