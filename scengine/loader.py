import os
import yaml
import pygame as pg
from typing import TypeVar

TResourceLoader = TypeVar("TResourceLoader", bound="ResourceLoader")


class ResourceLoader:
    def __init__(self, resource_folder: str) -> None:
        self.resources = {}
        self.sprites = {}
        self.resource_folder = resource_folder

    def load_sprites(self) -> dict[str : pg.surface.Surface]:
        for file in os.listdir(f"{self.resource_folder}/textures"):
            self.sprites[str(file).replace(".png", "")] = pg.image.load(
                f"{self.resource_folder}/textures/{file}"
            ).convert()

        return self.sprites


class SettingsLoader:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.settings = None

    def load_settings(self) -> dict[str:any]:
        with open(self.file_path, "r") as file:
            self.settings = yaml.safe_load(file)

        return self.settings
