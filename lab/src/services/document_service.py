from enum import Enum
import os
from platformdirs import *
import pathlib
from yaml import dump, safe_load
from dataclasses import asdict
from screen.screen_identifier import ScreenIdentifier
from models.location import Rect
import pandas as pd

class DocType(Enum):
    Settings = 1
    Excel = 2
    Text =3

class DocumentService:
    def __init__(self) -> None:
        self._excel_file_row = {}

    def save(self,type:DocType, data):
        if type == DocType.Settings:
            path = user_config_dir("ImageProcessing")
            pathlib.Path(path).mkdir(parents=True,exist_ok=True)
            with open(f"{path}/settings.yml","w+") as file:
                dump(self.normlize_locations(data), file, default_flow_style=False)  
        elif type == DocType.Text:
            self.save_text(data)
        elif type == DocType.Excel:
            self.save_excel(data)

    def load(self,type:DocType):
        if type == DocType.Settings:
            path = user_config_dir("ImageProcessing")
            try:
                with open(f"{path}/settings.yml") as file:
                    data = safe_load(file)
                    return self.denormlize_locations(data)
            except FileNotFoundError:
                return {}

    @staticmethod
    def save_text(data):
        report = data.report
        carbin = data.carbin
        output = data.file
        with open(f"{output}.txt","a+") as file:
            left_mean,right_mean,binary_mean = carbin.worm.cells[0].mean_density
            file.write(f"{carbin.time:<10.6f}  {binary_mean:<10.6f}   {left_mean:<14.6f}  {right_mean:<14.6f} {report.speed:<14.6f}  {carbin.worm.track.x:<14.6f} {carbin.worm.track.y:<14.6f}\n")
   
    def save_excel(self,data):
        report = data.report
        carbin = data.carbin
        output = f"{data.file}.xlsx"
        if output not in self._excel_file_row:
            self._excel_file_row[output] = 1
        left_mean,right_mean,binary_mean = carbin.worm.cells[0].mean_density
        if os.path.exists(output):
            with pd.ExcelWriter(output, engine="openpyxl",mode="a", if_sheet_exists="overlay") as writer:
                df = pd.DataFrame([[carbin.time,binary_mean,left_mean,right_mean,report.speed,carbin.worm.track.x,carbin.worm.track.y]])
                self._excel_file_row[output] = self._excel_file_row[output]+1
                df.to_excel(writer,sheet_name="Sheet1", index=False, header=False,startrow=self._excel_file_row[output])
        else:
            with pd.ExcelWriter(output, engine="openpyxl",mode="w") as writer:
                df = pd.DataFrame([[carbin.time,binary_mean,left_mean,right_mean,report.speed,carbin.worm.track.x,carbin.worm.track.y]],
                                  columns=["Time", "B_ratio","L_ratio", "R_ratio", "Speed", "X", "Y"])
                df.to_excel(writer,sheet_name="Sheet1", index=False)

    @staticmethod
    def normlize_locations(data):
        norm_data ={}
        for loc in data:
            norm_data[loc.name] =asdict(data[loc])
        return norm_data
    
    @staticmethod
    def denormlize_locations(data):
        denorm_data ={}
        for loc in data:
            denorm_data[ScreenIdentifier[loc]] =Rect(**data[loc])
        return denorm_data


if __name__ == "__main__":
    ds = DocumentService()
    print(ds.load(DocType.Settings))

