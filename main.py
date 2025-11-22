from zipfile import BadZipFile

from docx_extractor import get_tabular_data
from data_locator import find_docx_paths


if __name__ == "__main__":
    data_root_dir = r"D:\\Users\hkolb\Documents\PythonProjects\sharepoint_data_crawler\data\OneDrive"
    docx_dict = find_docx_paths(data_root_dir)
    
    allpaths = list(docx_dict.values())
    for folder in allpaths:
        for i in range(len(folder)-1, 0, -1):
            if "response" in folder[i].lower():
                print(folder[i])
                print(get_tabular_data(folder[i]))
                break
    # docx_path_1 = allpaths[0][0]
    # try:
    #     df_list = get_tabular_data(docx_path_1, False)
    #     print(df_list)
    # except BadZipFile as e:
    #     print(f"Error {e} ! {docx_path_1[docx_path_1.rfind('\\'):]} cannot be extracted.")
