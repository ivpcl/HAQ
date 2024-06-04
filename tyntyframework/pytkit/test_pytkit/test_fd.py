import pdb
import pathlib
import pytkit as pk

def test_check_file1():

    # Get location of file0.txt in data directory
    this_dir = pathlib.Path(__file__).parent.absolute()
    file0_pth = f"{this_dir}/data/file0.txt"

    # Assert that file0 exists
    assert pk.check_file(file0_pth) == True

def test_check_file2():

    # Get location of file0.txt in data directory
    this_dir = pathlib.Path(__file__).parent.absolute()
    file0_pth = f"{this_dir}/data/file100.txt"

    # Assert that file0 exists
    assert pk.check_file(file0_pth) == False

def test_load_as_df1():
    # Get location of file0.txt in data directory
    this_dir = pathlib.Path(__file__).parent.absolute()
    csv_pth = f"{this_dir}/data/test.csv"

    # Loading and checking number of entries
    df = pk.load_as_df(csv_pth)

    # Assert the csv file row entries
    assert len(df) == 6
    
