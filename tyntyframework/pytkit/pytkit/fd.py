import os
import pretty_errors
import pandas as pd

def get_file_paths_with_kws(pth, kw_lst, no_kw_lst = []):
    """
    Lists full paths of files having certian keywords in their names

    Parameters
    ----------
    pth: str Path to the root directory containing files.  kw_lst:
    list of str List of key words the files have

    Usage
    -----

    """
    # Check if directory is valid
    if not (os.path.exists(pth)):
        raise Exception(f"The path {pth} is not valid.")
    
    # create a list using comma separated values
    kw_lst_csv = []
    for idx, litem in enumerate(kw_lst):
        litem_split = litem.split(",")
        if len(litem_split) > 1:
            kw_lst_csv = kw_lst_csv + litem_split
        else:
            kw_lst_csv.append(litem_split[0])
            
    # create a list using comma separated values
    no_kw_lst_csv = []
    for idx, litem in enumerate(no_kw_lst):
        litem_split = litem.split(",")
        if len(litem_split) > 1:
            no_kw_lst_csv = no_kw_lst_csv + litem_split
        else:
            no_kw_lst_csv.append(litem_split[0])
    
    # Loop through each file
    files = []
    for r, d, f in os.walk(pth):
        for file in f:
            # Break comma separated values
            # Check if current file contains all of the key words
            kw_flag = all(kw in file for kw in kw_lst_csv)
            if len(no_kw_lst_csv) > 0:
                no_kw_flag = all(kw in file for kw in no_kw_lst_csv)
            else:
                no_kw_flag = False
            if kw_flag and not(no_kw_flag):
                files.append(os.path.join(r, file))

    # return
    files.sort()
    return files

def file_parts(fpth):
    """ Returns a list having
    1. Directory path where the file is located
    2. file name
    3. file extension.

    Usage
    -----
    ```python
    import pytkit as pk
    fpth= '/home/vj/.bashrc'
    dir_pth, fname, fext = file_parts(fpth)
    ```
    """
    dir_pth = os.path.dirname(fpth)
    fname_ext = os.path.basename(fpth)
    fname, fext   = os.path.splitext(fname_ext)
    return [dir_pth, fname, fext]

def check_file_existance(pth):
    """ Checks if a file exists

    Parameters
    ----------
    pth : Str
            Path to the file

    Returns
    -------
    Str
        Path to the file
    """
    if not os.path.isfile(pth):
        raise Exception(f"File not found\n    {pth}")
    else:
        return pth

def check_dir_existance(pth):
    """ Checks if a file exists

    Parameters
    ----------
    pth : Str
            Path to the directory

    Returns
    -------
    Str
        Returns directory path if it exists
    """
    if not os.path.isdir(pth):
        raise Exception(f"Directory does not exist\n    {pth}")        
    else:
        return pth


def load_as_df(pth, sheet_name=None):
    """ 
    Loads a CSV file or XLSX file to a dataframe if it exists.

    Parameters
    ----------
    pth : Str
        Path to the file

    sheet_name : Str, optional
        Sheet name if using an excel file

    Returns
    -------
    bool
        Returns `True` if the file exists else `False`.
    """
    if not os.path.exists(pth):
        raise Exception(f"USER_ERROR: file not found\n\t{pth}")
    else:
        if os.path.splitext(pth)[1] == ".csv":
            df = pd.read_csv(pth)
        elif os.path.splitext(pth)[1] == ".xlsx":
            df = pd.read_excel(pth, sheet_name=sheet_name)
        else:
            raise Exception(f"USER_ERROR: Unsupported file : {pth}")
    return df


def rename_dir_recursively(pth, oname, nname):
    """ 
    Loads a CSV file or XLSX file to a dataframe if it exists.

    Parameters
    ----------
    pth : Str
        Path to root directory
    oname : Str
        Old name of the directory
    nname : Str
        New name of directory
    """
    if not os.path.isdir(pth):
        raise Exception(f"USER_ERROR: path not found\n\t{pth}")

    # Get all directories
    all_dirs = []
    for root, subdirs, files in os.walk(pth):
        all_dirs += [f"{root}"]

    # Remove all directories without oname
    dirs = []
    for pth in all_dirs:
        
        if oname in pth:
            before, sep, after = pth.partition(oname)
            dirs += [f"{before}{sep}"]

    # Unique directory names
    dirs = list(set(dirs))

    # Rename the directories
    for d in dirs:
        output_path = f"{os.path.dirname(d)}/{nname}"
        cmd = f"mv {d} {output_path}"
        print(cmd)
        os.system(cmd)
