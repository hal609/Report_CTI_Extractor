import os
import tempfile
import pandas as pd
from zipfile import ZipFile, BadZipFile
import xml.etree.ElementTree as ET
from pretty_warnings import warn

namespaces = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml'
}

# Read document.xml
# =================
def get_xml_root(docx_path: str) -> ET.Element|None:
    """ Extracts and reads the document.xml file from a docx and returns
        The root of the XML tree as a xml ElementTree Element.

    Args:
        docx_path (str): _description_

    Returns:
        ET.Element: _description_
    """
    
    # Create temp directory for files
    tmpdir = tempfile.mkdtemp()

    # Manipulate strings to format paths
    xml_subpath = f"word/document.xml"
    doc_xml_path = f"{tmpdir}/{xml_subpath}"

    # Extract just the document.xml file
    try:
        with ZipFile(docx_path, 'r') as zObject:
            zObject.extractall(tmpdir, members=[xml_subpath])
    except Exception as e:
        warn(f"File: {docx_path[docx_path.rfind('\\'):]} cannot be extracted. {e}")
        # print(f"File: {tmpdir[tmpdir.rfind('\\'):]} cannot be extracted due to error:\n{e}")
        return None

    # Parse document.xml
    tree = ET.parse(doc_xml_path)

    # Return root Element of parsed xml ElementTree object
    return tree.getroot()


# Extract data from tables
# =======================
def get_tabular_data(docx_path: str, combine_frames: bool = True) -> pd.DataFrame:
    """ Locate all data from any tables in the document.
        This wll usually be: 
            Name of Insured «Text»
            Indident Date, «Date»
            Type of incident, «Categorical Text»
            Location, «ISO 3166 Alpha-2 Code»
            Industry, «SIC Alphabetic Industry Class» 
            
    Args:
        docx_path (str): Path to a .docx file
        combine_frames (bool): If True then all tables are concatenated into a single dataframe
    """
    root = get_xml_root(docx_path)
    
    if root is None:
        return pd.DataFrame(columns=[0, 1]) if combine_frames else []
    
    tables = []

    # Find all tables
    for tbl in root.findall('.//w:tbl', namespaces):
        rows = []
        for tr in tbl.findall('.//w:tr', namespaces):
            cells = []
            for tc in tr.findall('.//w:tc', namespaces):
                # Extract all text in this cell
                texts = [t.text for t in tc.findall('.//w:t', namespaces) if t.text]
                cell_text = ' '.join(texts).strip()
                cells.append(cell_text)

            rows.append(cells)
        
        # Convert to DataFrame
        df = pd.DataFrame(rows)
        
        # Ensure at least two columns
        if df.shape[1] < 2:
            df = df.reindex(columns=range(2), fill_value="")
        
        tables.append(df)

    if len(tables) == 0: return tables
    
    if combine_frames:
        # Combine tables and return
        return pd.concat(tables, ignore_index=True)
    else:
        return tables


# Extract text data
# =================
def get_text_data(docx_path: str, split_paragraphs: bool = False):
    """ Reads raw text and paragraph data from a .docx file.

    Args:
        docx_path (str): Path to a .docx file
        split_paragraphs (bool, optional): If True, text is split on newlines into a list of paragraphs otherwise, text is returned. Defaults to False.
    """    

    root = get_xml_root(docx_path)

    text = ""
    for paragraph in root.findall(".//w:p", namespaces):
        text += "\n"
        for elem in paragraph.findall(".//w:t", namespaces):
            text += elem.text

    if not split_paragraphs:
        return text
    else:
        paragraphs = text.split("\n")
        paragraphs = [para for para in paragraphs if para != ""] # Remove blank paragraphs
        return paragraphs
