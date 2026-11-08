import streamlit as st
import requests, json, html
import streamlit.components.v1 as components
from urllib.parse import quote

st.set_page_config(page_title='VIMORA | Chemistry Explorer', page_icon='⚗️', layout='wide')
PUBCHEM='https://pubchem.ncbi.nlm.nih.gov/rest/pug'
HEADERS={'User-Agent':'VIMORA-Educational-App/2.0'}
# A deliberately curated set of common classroom examples, not an unrestricted chemical search.
COMPOUNDS={
 'water':'Water','glucose':'D-Glucose','sucrose':'Sucrose','citric acid':'Citric acid',
 'sodium chloride':'Sodium chloride','calcium carbonate':'Calcium carbonate','glycine':'Glycine',
 'alanine':'L-Alanine','starch':'Starch','cellulose':'Cellulose','ascorbic acid':'Ascorbic acid',
 'lactic acid':'Lactic acid','urea':'Urea','acetic acid':'Acetic acid','sodium bicarbonate':'Sodium bicarbonate',
 'carbon dioxide':'Carbon dioxide','oxygen':'Oxygen','nitrogen':'Nitrogen','ammonia':'Ammonia',
 'glycerol':'Glycerol','fructose':'D-Fructose','lactose':'Lactose','maltose':'Maltose',
 'serine':'L-Serine','glutamic acid':'L-Glutamic acid','lysine':'L-Lysine'
}
# Element name and symbol reference for all 118 named elements.
ELEMENTS='''H|Hydrogen;He|Helium;Li|Lithium;Be|Beryllium;B|Boron;C|Carbon;N|Nitrogen;O|Oxygen;F|Fluorine;Ne|Neon;Na|Sodium;Mg|Magnesium;Al|Aluminium;Si|Silicon;P|Phosphorus;S|Sulfur;Cl|Chlorine;Ar|Argon;K|Potassium;Ca|Calcium;Sc|Scandium;Ti|Titanium;V|Vanadium;Cr|Chromium;Mn|Manganese;Fe|Iron;Co|Cobalt;Ni|Nickel;Cu|Copper;Zn|Zinc;Ga|Gallium;Ge|Germanium;As|Arsenic;Se|Selenium;Br|Bromine;Kr|Krypton;Rb|Rubidium;Sr|Strontium;Y|Yttrium;Zr|Zirconium;Nb|Niobium;Mo|Molybdenum;Tc|Technetium;Ru|Ruthenium;Rh|Rhodium;Pd|Palladium;Ag|Silver;Cd|Cadmium;In|Indium;Sn|Tin;Sb|Antimony;Te|Tellurium;I|Iodine;Xe|Xenon;Cs|Caesium;Ba|Barium;La|Lanthanum;Ce|Cerium;Pr|Praseodymium;Nd|Neodymium;Pm|Promethium;Sm|Samarium;Eu|Europium;Gd|Gadolinium;Tb|Terbium;Dy|Dysprosium;Ho|Holmium;Er|Erbium;Tm|Thulium;Yb|Ytterbium;Lu|Lutetium;Hf|Hafnium;Ta|Tantalum;W|Tungsten;Re|Rhenium;Os|Osmium;Ir|Iridium;Pt|Platinum;Au|Gold;Hg|Mercury;Tl|Thallium;Pb|Lead;Bi|Bismuth;Po|Polonium;At|Astatine;Rn|Radon;Fr|Francium;Ra|Radium;Ac|Actinium;Th|Thorium;Pa|Protactinium;U|Uranium;Np|Neptunium;Pu|Plutonium;Am|Americium;Cm|Curium;Bk|Berkelium;Cf|Californium;Es|Einsteinium;Fm|Fermium;Md|Mendelevium;No|Nobelium;Lr|Lawrencium;Rf|Rutherfordium;Db|Dubnium;Sg|Seaborgium;Bh|Bohrium;Hs|Hassium;Mt|Meitnerium;Ds|Darmstadtium;Rg|Roentgenium;Cn|Copernicium;Nh|Nihonium;Fl|Flerovium;Mc|Moscovium;Lv|Livermorium;Ts|Tennessine;Og|Oganesson'''
ELEMENT_LIST=[x.split('|') for x in ELEMENTS.split(';')]

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
.stApp{background:radial-gradient(circle at 10% 0%,#173c49 0,#0a1c27 45%,#07141d 100%);color:#eaf3f5;font-family:'DM Sans',sans-serif}
h1,h2,h3{font-family:'Manrope',sans-serif;color:#f2fbfc}.block-container{max-width:1200px;padding-top:1.6rem}
.hero{padding:28px 30px;border:1px solid #285260;border-radius:22px;background:linear-gradient(120deg,#17434df2,#0d2433f2);margin-bottom:20px}
.eyebrow{color:#43d6c5;letter-spacing:2px;font-size:12px;font-weight:700}.hero h1{font-size:46px;margin:4px 0}.hero p,.muted{color:#b6cbd0}
.card{background:#102b36e8;border:1px solid #254957;border-radius:15px;padding:15px 17px;margin:7px 0}.label{font-size:11px;color:#9bb8c0;text-transform:uppercase;letter-spacing:1px}.metric{font-size:23px;font-weight:800;color:#f4ffff;overflow-wrap:anywhere}
div.stButton>button{border-radius:10px;border:1px solid #367a7b;background:#17454e;color:#efffff;font-weight:600}
[data-testid="stTextInput"] input{background:#102b36;color:white;border:1px solid #38606b;border-radius:10px}a{color:#65dfd1!important}footer{visibility:hidden}
</style>''',unsafe_allow_html=True)

def get_json(url):
    try:
        r=requests.get(url,headers=HEADERS,timeout=20)
        return r.json() if r.status_code==200 else None
    except requests.RequestException:return None

@st.cache_data(ttl=3600,show_spinner=False)
def get_record(name):
    url=f'{PUBCHEM}/compound/name/{quote(name,safe="")}/property/MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES,IUPACName,InChI,InChIKey,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount,RotatableBondCount/JSON'
    data=get_json(url)
    try:
        p=data['PropertyTable']['Properties'][0]; cid=p['CID']
        syn=get_json(f'{PUBCHEM}/compound/cid/{cid}/synonyms/JSON') or {}
        synonyms=syn.get('InformationList',{}).get('Information',[{}])[0].get('Synonym',[])[:8]
        return p,cid,synonyms
    except (TypeError,KeyError,IndexError):return None

def show_3d(cid):
    try:
        r=requests.get(f'{PUBCHEM}/compound/cid/{cid}/record/SDF?record_type=3d',headers=HEADERS,timeout=25)
        if r.status_code!=200 or ('V2000' not in r.text and 'V3000' not in r.text):
            st.info('A 3D conformer is not available for this record. The 2D structure is shown in the other panel.');return
        sdf=json.dumps(r.text)
        page=f'''<div id="vimora3d" style="height:420px;width:100%;background:#0b2029;border-radius:14px"></div>
        <script src="https://3Dmol.org/build/3Dmol-min.js"></script><script>
        (function(){{let el=document.getElementById('vimora3d');if(!window.$3Dmol){{el.innerHTML='3D viewer failed to load';return;}}
        let v=$3Dmol.createViewer(el,{{backgroundColor:'#0b2029',antialias:true}});v.addModel({sdf},'sdf');
        v.setStyle({{}},{{stick:{{radius:0.16}},sphere:{{scale:0.27}}}});v.zoomTo();v.render();v.resize();
        window.addEventListener('resize',()=>v.resize());}})();</script>'''
        components.html(page,height=435,scrolling=False)
        st.caption('Drag to rotate · Right-click and drag to pan · Scroll to zoom')
    except requests.RequestException:st.warning('Could not retrieve the 3D record. Try again later.')

def assistant_answer(q,p,name):
    q=q.lower(); formula=p.get('MolecularFormula','not reported'); mass=p.get('MolecularWeight','not reported')
    smi=p.get('ConnectivitySMILES') or p.get('CanonicalSMILES') or p.get('SMILES','not reported')
    if 'smiles' in q or 'notation' in q:return f'SMILES is a text representation of molecular connectivity. PubChem lists this notation for {name}: {smi}'
    if 'mass' in q or 'weight' in q:return f'The listed molecular weight of {name} is {mass} g/mol.'
    if 'formula' in q or 'atom' in q:return f'The molecular formula is {formula}. It tells you which elements are present and the number of atoms of each.'
    if 'bond' in q or 'structure' in q or 'shape' in q:return f'The structure shows how atoms are connected and arranged. The 2D image is a connectivity drawing; the 3D viewer helps explore spatial geometry. SMILES: {smi}'
    return f'{name}: molecular formula {formula}; molecular weight {mass} g/mol. Ask about its formula, mass, structure or SMILES.'

def compound_page(key):
    name=COMPOUNDS[key]
    with st.spinner('Retrieving the compound record from PubChem…'): result=get_record(name)
    if not result:st.error('PubChem could not return this record right now. Try again later.');return
    p,cid,synonyms=result
    st.markdown(f'## {html.escape(name)} <span style="color:#68ded0;font-size:13px">PubChem CID {cid}</span>',unsafe_allow_html=True)
    cols=st.columns(4)
    for c,(label,value) in zip(cols,[('Formula',p.get('MolecularFormula','—')),('Molecular mass',str(p.get('MolecularWeight','—'))+' g/mol'),('H-bond donors',p.get('HBondDonorCount','—')),('H-bond acceptors',p.get('HBondAcceptorCount','—'))]):
        with c:st.markdown(f'<div class="card"><div class="label">{label}</div><div class="metric">{html.escape(str(value))}</div></div>',unsafe_allow_html=True)
    a,b,c,d=st.tabs(['2D & 3D structures','Properties & SMILES','Learn','VIMORA assistant'])
    with a:
        x,y=st.columns(2)
        with x:st.markdown('### 2D structure');st.image(f'{PUBCHEM}/compound/cid/{cid}/PNG?image_size=large',use_container_width=True);st.caption('2D depiction from PubChem')
        with y:st.markdown('### Interactive 3D model');show_3d(cid)
    with b:
        props=[('IUPAC name',p.get('IUPACName','Not reported')),('Canonical SMILES',p.get('ConnectivitySMILES') or p.get('CanonicalSMILES','Not reported')),('Isomeric SMILES',p.get('SMILES') or p.get('IsomericSMILES','Not reported')),('InChI',p.get('InChI','Not reported')),('InChIKey',p.get('InChIKey','Not reported')),('XLogP',p.get('XLogP','Not reported')),('TPSA',p.get('TPSA','Not reported')),('Rotatable bonds',p.get('RotatableBondCount','Not reported'))]
        for label,val in props:
            st.markdown(f'<div class="card"><div class="label">{html.escape(label)}</div><div style="overflow-wrap:anywhere">{html.escape(str(val))}</div></div>',unsafe_allow_html=True)
            if 'SMILES' in label and val!='Not reported':st.code(str(val),language=None)
        st.write('**PubChem synonyms:** '+(', '.join(synonyms) if synonyms else 'Not reported'))
        st.markdown(f'[Open PubChem record](https://pubchem.ncbi.nlm.nih.gov/compound/{cid})')
    with c:
        st.write(f'The molecular formula is **{p.get("MolecularFormula","not reported")}**. A molecular formula indicates which elements are present and how many atoms of each are represented. Molecular weight is expressed in grams per mole.')
        st.info('Applications and properties depend on the exact substance and context. This student version focuses on chemistry learning, not chemical handling or use instructions.')
    with d:
        q=st.text_input('Ask a question about this compound',key=f'assist{cid}',placeholder='What does its SMILES notation mean?')
        if st.button('Explain',key=f'btn{cid}') and q.strip():st.info(assistant_answer(q,p,name))
        st.caption('This is a record-aware educational assistant, not a generative AI model.')

st.markdown('''<div class="hero"><div class="eyebrow">A MODERN CHEMISTRY LEARNING SPACE</div><h1>VIMORA ⚗</h1>
<p>Explore molecular structures, understand chemical properties and build confidence in chemistry — one discovery at a time.</p>
<div class="muted"><b>Developed by Vidhyalashmi S</b> · B.Tech CSE (AI&ML) · SRM Institute of Science and Technology</div></div>''',unsafe_allow_html=True)
page=st.sidebar.radio('EXPLORE VIMORA',['Compound explorer','Periodic table','Chemistry quiz','About VIMORA'])
st.sidebar.caption('Compound records and structure files: PubChem / U.S. National Library of Medicine.')
if page=='Compound explorer':
    st.markdown('## Compound explorer')
    st.write('Explore common classroom compounds using live PubChem records.')
    key=st.selectbox('Choose a compound',list(COMPOUNDS),format_func=lambda k:COMPOUNDS[k])
    if st.button('Explore compound',type='primary'):st.session_state['vimora_key']=key
    if st.session_state.get('vimora_key'):compound_page(st.session_state['vimora_key'])
    with st.expander('Search coverage note'):st.write('This educational build uses a curated classroom-safe catalogue, not unrestricted chemical search. Database coverage and available properties vary by record.')
elif page=='Periodic table':
    st.markdown('## Periodic table');term=st.text_input('Find an element by name or symbol')
    found=[(i+1,*e) for i,e in enumerate(ELEMENT_LIST) if not term or term.lower() in e[0].lower() or term.lower() in e[1].lower()]
    cols=st.columns(6)
    for i,(num,sym,name) in enumerate(found):
        with cols[i%6]:st.markdown(f'<div class="card" style="text-align:center"><div class="label">Atomic no. {num}</div><div class="metric" style="color:#55d9c9">{sym}</div>{name}</div>',unsafe_allow_html=True)
elif page=='Chemistry quiz':
    st.markdown('## Chemistry knowledge check')
    qs=[('What does a molecular formula show?',['Colour','Element types and atom counts','Smell'],1,'A formula lists the elements and atom counts.'),('What does SMILES represent?',['Molecular connectivity in text form','A smell','A lab method'],0,'SMILES is a text notation for molecular connectivity.'),('Common unit for molecular weight?',['metres','g/mol','litres'],1,'Molecular weight is commonly expressed in g/mol.'),('How many named elements are in the periodic table?',['92','108','118'],2,'There are 118 named elements.')]
    i=st.selectbox('Choose a question',range(len(qs)),format_func=lambda n:f'Question {n+1}');q,opts,ans,why=qs[i];st.markdown('### '+q);choice=st.radio('Choose your answer',opts,key=f'quiz{i}')
    if st.button('Check answer'):
        st.success('Correct! '+why) if opts.index(choice)==ans else st.warning('Not quite. '+why)
else:
    st.markdown('## About VIMORA')
    st.markdown('''<div class="card"><h3>Discover. Understand. Explore.</h3><p>VIMORA is a student-built chemistry learning platform featuring compound records, molecular properties, 2D depictions, interactive 3D models when available, a periodic table and quizzes.</p><p><b>Developed by</b><br>Vidhyalashmi S<br>B.Tech CSE (AI&ML)<br>SRM Institute of Science and Technology</p><p><b>Data attribution</b><br>Compound records and available structure files are retrieved from PubChem. Some records do not contain every property or a 3D conformer.</p></div>''',unsafe_allow_html=True)
    st.markdown('[PubChem PUG REST documentation](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest) · [3Dmol.js](https://3dmol.org/)')
    st.caption('Educational project only; not a medical, safety, procurement or laboratory-procedure tool.')
st.markdown('---');st.markdown('<p class="muted" style="text-align:center">VIMORA · Chemistry, made explorable · Built by Vidhyalashmi S</p>',unsafe_allow_html=True)
