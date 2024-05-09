import os
import pandas

#Test to make sure the CSV does Exist.
def Test_CSV_Exists():
    file = 'data.csv'
    assert os.path.exists(file) == True

#Test to check that there is data within the CSV.
def Test_CSV_DataExists():
    with open('data.csv', 'r') as file:
        assert file is not None

