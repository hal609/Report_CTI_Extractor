import os

def find_docx_paths(root_path: str) -> dict:
    """ Crawls through a given folder, locates all "Reporting" folders and 
        collects the subpaths to each.

    Args:
        root_path (str): Path to the root directory from which to begin search.

    Returns:
        dict: Dictionary mapping subfolder names to the subpaths to the .docx files they contain.
    """
    report_dict: dict = {}
    
    for path, dir, files in os.walk(root_path):
        # path = path.replace("\\", "/") # Use only forward slashes in path
        for file in files:
            if "docx" in file.lower():# and "response" in file.lower():
                subpath = path[len(root_path) + 1:]
                # Extract first level folder name for use as key
                name = subpath[:path.rfind("\\")]
                # Assign the list of docx subpaths to that key index
                report_dict[name] = [fr"{path}\{file}" for file in files if "docx" in file]
    
    return report_dict

def find_xlsx_paths(root_path: str) -> dict:
    """ Crawls through a given folder, locates all "Reporting" folders and 
        collects the subpaths to each.

    Args:
        root_path (str): Path to the root directory from which to begin search.

    Returns:
        dict: Dictionary mapping subfolder names to the subpaths to the .docx files they contain.
    """
    report_dict: dict = {}
    
    for path, dir, files in os.walk(root_path):
        # path = path.replace("\\", "/") # Use only forward slashes in path
        for file in files:
            if "xls" in file.lower():# and "response" in file.lower():
                subpath = path[len(root_path) + 1:]
                # Extract first level folder name for use as key
                name = subpath[:path.rfind("\\")]
                # Assign the list of docx subpaths to that key index
                report_dict[name] = [fr"{path}\{file}" for file in files if "xls" in file]
    
    return report_dict