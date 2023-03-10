from scengine.entity import Entity
from scengine.vector2 import Vector2
import pygame as pg
import math


class Player(Entity):
    def __init__(self, game, x: int | float = 50, y: int | float = 50) -> None:
        super().__init__(game, x, y)
        self.GAME = game

        self.keybinds = {
            key: ord(value) for key, value in self.GAME.SETTINGS["keybinds"].items()
        }

        self.keys_pressed = {key: False for key in self.keybinds.keys()}

        self.speed = 220

        self.current_chunk = None

    def set_key(self, key: str) -> None:
        """Set a key state to pressed

        Args:
            key (str): key name
        """
        self.keys_pressed[key] = True

    def reset_key(self, key: str) -> None:
        """Set a key state to unpressed

        Args:
            key (str): key name
        """
        self.keys_pressed[key] = False

    def get_key(self, key: str) -> None:
        """Returns the state of the key

        Args:
            key (str): key name

        Returns:
            bool: state of the key
        """
        return self.keys_pressed[key]

    def event_handler(self, events: list[pg.event.Event]) -> None:
        """Handle user input events

        Args:
            events (list[pg.event.Event]): list of events
        """
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == self.keybinds["left"]:
                    self.set_key("left")
                if event.key == self.keybinds["right"]:
                    self.set_key("right")
                if event.key == self.keybinds["up"]:
                    self.set_key("up")
                if event.key == self.keybinds["down"]:
                    self.set_key("down")

            if event.type == pg.KEYUP:
                if event.key == self.keybinds["left"]:
                    self.reset_key("left")
                if event.key == self.keybinds["right"]:
                    self.reset_key("right")
                if event.key == self.keybinds["up"]:
                    self.reset_key("up")
                if event.key == self.keybinds["down"]:
                    self.reset_key("down")

    def update(self) -> None:
        """Updates the player"""
        super().update()

        self.move()
        self.rect.x, self.rect.y = self.position

        self.current_chunk: tuple[int, int] = (
            math.floor(
                self.position.x / self.GAME.WORLD.TILE_SIZE / self.GAME.WORLD.CHUNK_SIZE
            ),
            math.floor(
                self.position.y / self.GAME.WORLD.TILE_SIZE / self.GAME.WORLD.CHUNK_SIZE
            ),
        )

        self.position.set(self.position.round(1))

        self.GAME.HUD.debug(f"Absolute | x: {self.position.x} y: {self.position.y}")
        self.GAME.HUD.debug(
            f"Chunk    | x: {self.current_chunk[0]} y: {self.current_chunk[1]}"
        )

    def move(self) -> None:
        """Moves the player according to recorded inputs"""

        speed = self.speed * self.ENGINE.DELTA_TIME
        velocity = Vector2(0, 0)

        if self.get_key("left"):
            velocity.add(Vector2(-speed, 0))
        if self.get_key("right"):
            velocity.add(Vector2(speed, 0))
        if self.get_key("up"):
            velocity.add(Vector2(0, -speed))
        if self.get_key("down"):
            velocity.add(Vector2(0, speed))

        self.position.add(velocity)
        self.position.round(1)

    def draw(self) -> None:
        super().draw(self.GAME.CAMERA.scroll)
