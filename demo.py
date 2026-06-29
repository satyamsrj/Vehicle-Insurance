from src.pipline.training_pipeline import TrainPipeline
from src.data_access.proj1_data import Proj1data   # ✅ lowercase d

def main():
    # Quick test: fetch data directly from MongoDB
    proj_data = Proj1data()
    df = proj_data.export_collection_as_dataframe(collection_name="Vehicle_Ins_Data")
    print("Sample data from MongoDB:")
    print(df.head())

    # Run the full training pipeline (currently only ingestion active)
    pipeline = TrainPipeline()
    pipeline.run_pipeline()

if __name__ == "__main__":
    main()
