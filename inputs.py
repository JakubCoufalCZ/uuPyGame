"""Inputs module"""
import pygame

from enums import KeyType

PLAYER_KEYMAPS = {
    "wasd": {
        pygame.K_w: KeyType.UP.name,
        pygame.K_s: KeyType.DOWN.name,
        pygame.K_a: KeyType.LEFT.name,
        pygame.K_d: KeyType.RIGHT.name,
        pygame.K_SPACE: KeyType.SHOOT.name
    },
    "arrows": {
        pygame.K_UP: KeyType.UP.name,
        pygame.K_DOWN: KeyType.DOWN.name,
        pygame.K_LEFT: KeyType.LEFT.name,
        pygame.K_RIGHT: KeyType.RIGHT.name,
        pygame.K_RETURN: KeyType.SHOOT.name
    }
}

class InputBuffer:
    """Buffer for one player's inputs"""
    def __init__(self, max_size=20):
        self.buffer = []
        self.max_size = max_size

    def add(self, action):
        """Single input insert"""
        self.buffer.append(action)

        # todo filter duplicates and / or block opposites, UP vs DOWN

        if len(self.buffer) > self.max_size:
            self.buffer.pop(0)

    def get_all(self):
        """Inputs getter"""
        return list(self.buffer)

    def clear(self):
        """Clear inputs, usually after retrieving"""
        self.buffer.clear()


class InputManager:
    """Component for managing multiple player inputs"""
    def __init__(self, keymaps=None):
        self.player_inputs = {}
        self.keymaps = keymaps if keymaps else {}


    def add_keymap(self, uid, keymap):
        """Key map setting"""
        self.keymaps[uid] = keymap

    def add_input(self, uid, pygame_key):
        """Single input inserting with key map transform"""
        keymap = self.keymaps.get(uid, {})
        action = keymap.get(pygame_key)
        if action:
            if uid not in self.player_inputs:
                self.player_inputs[uid] = InputBuffer()
            self.player_inputs[uid].add(action)

    def add_inputs(self, uid, inputs):
        """Raw multiple inputs inserting without key map, usually from socket input"""
        if uid not in self.player_inputs:
            self.player_inputs[uid] = InputBuffer()
        for inp in inputs:
            self.player_inputs[uid].add(inp)

    def get_inputs(self, uid):
        """Inputs getter"""
        return self.player_inputs.get(uid, InputBuffer()).get_all()

    def clear_inputs(self, uid):
        """Clear inputs, usually after retrieving"""
        if uid in self.player_inputs:
            self.player_inputs[uid].clear()
