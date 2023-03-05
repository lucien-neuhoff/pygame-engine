import time
import pygame as pg
import pygame.freetype
from pathlib import Path

path = Path(__file__).parent

from .resource_loader import ResourceLoader
from .colors import Colors


class Engine:
    pg.init()

    def __init__(
        self,
        title: str = "SCEngine",
        size: tuple[int] = (1280, 720),
        background_color: pg.Color = Colors.background,
        resource_folder: str = path / "resources",
    ) -> None:
        self.TITLE = title
        self.SIZE = self.WIDTH, self.HEIGHT = size

        self.WINDOW = pg.display.set_mode(self.SIZE, True)
        self.DISPLAY = pg.surface.Surface(self.SIZE)

        self.CLOCK = pg.time.Clock()

        self.FONT = pygame.freetype.Font(
            rf"{resource_folder}/fonts/default.otf", 12, False, False
        )
        self.FONT.antialiased = False

        self.RESOURCE_LOADER = ResourceLoader(resource_folder)
        self.SPRITES = self.RESOURCE_LOADER.load_sprites()

        self.BACKGROUND_COLOR = background_color

        self.DELTA_TIME = None
        self.prev_time = time.time()
        self.now = 0

        self.RUNNING = False

    def event_handler(self) -> None:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.RUNNING = False
                exit(0)

        return events

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.WINDOW.fill(self.BACKGROUND_COLOR)
        self.DISPLAY.fill(self.BACKGROUND_COLOR)

    def run(self):
        self.RUNNING = True

        while self.RUNNING:
            self.now = time.time()
            self.DELTA_TIME = self.now - self.prev_time
            self.prev_time = self.now

            self.event_handler()
            self.update()
            self.draw()

    def font(
        self,
        content: str = "Placeholder",
        size: int = 20,
        color: tuple = Colors.white,
        bgcolor: tuple = None,
        padding: int = 4,
    ):
        """Renders text with given arguments

        Args:
            content (str, optional): Displayed text. Defaults to "Placeholder".
            size (int, optional): Text's size. Defaults to 24.
            color (tuple, optional): Text's color. Defaults to Colors.white.
            bgcolor (tuple, optional): Text's background color. Defaults to None.
            padding (int, optional): Text's padding. Defaults to 4.

        Returns:
            pygame.Surface: Rendered text surface
        """
        rendered_text = self.FONT.render(
            str(content), color, None, pygame.freetype.STYLE_DEFAULT, 0, size
        )[0]

        padded_rendered_text = pygame.Surface(
            (
                rendered_text.get_width() + padding * 2,
                rendered_text.get_height() + padding * 2,
            )
        )
        padded_rendered_text.convert_alpha()

        if bgcolor:
            padded_rendered_text.fill(bgcolor)

        padded_rendered_text.blit(rendered_text, (padding, padding))

        return padded_rendered_text
