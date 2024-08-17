from enum import Enum
from platformdirs import *
import pathlib
from yaml import dump, safe_load
from dataclasses import asdict
from screen.screen_identifier import ScreenIdentifier
from models.location import Rect

class DocType(Enum):
    Settings = 1
    Excel = 2
    Text =3

class DocumentService:
    def __init__(self) -> None:
        pass

    def save(self,type:DocType, data):
        if type == DocType.Settings:
            path = user_config_dir("ImageProcessing")
            pathlib.Path(path).mkdir(parents=True,exist_ok=True)
            with open(f"{path}/settings.yml","w+") as file:
                dump(self.normlize_locations(data), file, default_flow_style=False)  

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

