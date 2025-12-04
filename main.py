import sys
import pandas as pd
from tqdm import tqdm

from docx_extractor import get_tabular_data
from data_locator import find_docx_paths, find_xlsx_paths

taxonomy_features = ["Insured", "Date", "Case Manager", "Type", "Location", "Industry", "KPMG Retained"]

def flatten_tab_data(tabular_data: pd.DataFrame) -> pd.DataFrame:
    global taxonomy_features
    
    data_dict = {feat: "" for feat in taxonomy_features}

    for i in range(len(tabular_data)):
        data_name = tabular_data.loc[i, 0]
        data = tabular_data.loc[i, 1]
        
        if "name of insured" in data_name.lower():
            data_dict[taxonomy_features[0]] = data
        elif "date of incident" in data_name.lower():
            data_dict[taxonomy_features[1]] = data.replace(" ", "")
        elif "case manager" in data_name.lower():
            data_dict[taxonomy_features[2]] = data
        elif "type of incident" in data_name.lower():
            data_dict[taxonomy_features[3]] = data
        elif "location" in data_name.lower():
            data_dict[taxonomy_features[4]] = data
        elif "industry" in data_name.lower():
            data_dict[taxonomy_features[5]] = data
        elif "retain" in data_name.lower():
            data_dict[taxonomy_features[6]] = data

    if any([dat != "" for dat in data_dict.values()]):
        return pd.DataFrame.from_dict([data_dict])
    else:
        return None

if __name__ == "__main__":
    usage_message = "Usage: python main.py <'xlxs'|'docx'>"
    
    if len(sys.argv) != 2:
        print(usage_message)
        sys.exit(1)
    
    data_root_dir = r"D:\\Users\hkolb\Documents\PythonProjects\sharepoint_data_crawler\data\OneDrive"
    
    if sys.argv[1] == "docx":
        taxonomy_df = pd.DataFrame(columns=taxonomy_features)
        
        docx_dict = find_docx_paths(data_root_dir)

        allpaths = list(docx_dict.values())
        for folder in tqdm(allpaths):
            # folder = sorted(folder)

            for i in range(len(folder)):
                tab_data = get_tabular_data(folder[i])
                new_row = flatten_tab_data(tab_data)
                taxonomy_df = pd.concat([taxonomy_df, new_row], ignore_index=True)

        taxonomy_df = taxonomy_df.drop_duplicates()
        print(taxonomy_df)
        
        taxonomy_df.to_csv("combined_taxonomy_data.csv", index=False)
    elif sys.argv[1] == "xlsx":
        xlsx_dict = find_xlsx_paths(data_root_dir)
        print("\nALL WORKBOOKS")
        for key in xlsx_dict.keys():
            for path in xlsx_dict[key]:
                if "workbook" in path.lower():
                    if "Project X " not in path:
                        print(path[path.find("OneDrive"):])
                # if "[insured]" not in path:
                #     print(path[path.rfind("\\"):])
    else:
        print(usage_message)
        sys.exit(1)
