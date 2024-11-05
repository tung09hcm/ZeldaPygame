import pygame
import threading

class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        # Tải các âm thanh
        self.sounds = {
            "battle_champion": pygame.mixer.Sound("../resources/sound/BattleChampion.ogg"),
            "battle_elite": pygame.mixer.Sound("../resources/sound/BattleElite.ogg"),
            "cave": pygame.mixer.Sound("../resources/sound/Cave.ogg"),
            "cedolan_city": pygame.mixer.Sound("../resources/sound/CedolanCity.ogg"),
            "victory": pygame.mixer.Sound("../resources/sound/BattleVictory.ogg"),
        }

        # Đặt âm lượng mặc định nếu cần
        self.sounds["battle_champion"].set_volume(0.5)
        self.sounds["battle_elite"].set_volume(0.7)
        self.sounds["cave"].set_volume(0.8)
        self.sounds["cedolan_city"].set_volume(0.5)

    def play_sound(self, sound_name, loop=False):
        if sound_name in self.sounds:
            self.sounds[sound_name].play(-1 if loop else 0)

    def stop_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()

    def stop_all(self):
        for sound in self.sounds.values():
            sound.stop()

    def play_sound_with_duration(self, sound_name, duration=5):
        """Phát âm thanh trong khoảng thời gian xác định (mặc định là 5 giây)."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
            threading.Timer(duration, lambda: self.stop_sound(sound_name)).start()