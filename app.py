from src.data_access.proj1_data import Proj1data 
proj_data = Proj1data()
df = proj_data.export_collection_as_dataframe("Vehicle_Ins_Data")
print("Shape:", df.shape)
print(df.head())
