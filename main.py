import pandas as pd
from Processing_Changes import Changes_Main as c_m
import Cy_Excel as cye
import json
from ProcessingAssinting_Modules import cy_processing as cyp

#todo rename folders with underscore to be faster

#TODO add the try except exection line with a user input, so they can start the programm again and see the error log

def main_loop():

    try:
        with open(f"Confg/config_aMAIN.json") as json_file:
            main_config = json.load(json_file)
    except FileNotFoundError:
        print("Could not find Main Config File. Please Make sure it exists in the proper Folder and Check the Docs")


    print("Current Operation: Process Individual Excel Files\n")
    for items in main_config["Files_To_Read"]:
        print(f"Now handling file: {items}")
        with open(f"Config/{items}.json") as json_file:
            data = json.load(json_file)
        c_m.auto_run_config(data,main_config=main_config)

    try:
        print("\nCurrent Operation: Combine Excels into 1 Output")
        combine_df_list = []
        for excel_file_names in main_config["Combine_Sheets"]["Excel_Names"]:
            print(f"--Loading Excel: {excel_file_names}")
            combine_df_list.append(
                cye.load_excel(excel_file_name=f"Result Excels/{excel_file_names}", loader_variant="Excel_Headers"))

        output_df = pd.concat(combine_df_list, axis=0)  # TODO checking for same lenght
        print("--Combined Excels")
        print("--Making Output Excel, this may take a while")
        output_df.to_excel(f"Result Excels/{main_config['Combine_Sheets']['Output_Name']}.xlsx", index=False)

    except KeyError:
        print("Skipped combining, KeyError")  # TODO debugging
    print("All Done")


def looper():
    try:
        main_loop()
    except Exception as e:
        print(f"\nUncaught Exception:\n {e}\n\n")
    finally:
        userinput = input("Did everything work?\n"
                          "If not, this console will remain open until manually closed or you type 'c' in the console\n"
                          "If you want to run the program again, type 'r' in the console\n"
                          "If everything worked, either close the console or type 'c'\n"
                          "Your Input: ")
        if userinput == "r":
            looper()


if __name__ == '__main__':
    looper()


