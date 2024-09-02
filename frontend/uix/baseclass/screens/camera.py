from datetime import datetime

from kivymd.uix.screen import MDScreen


class CameraScreen(MDScreen):
    def capture(self):
        capture_time = datetime.now()
        self.ids.camera.export_to_png(
            f"data/images/{capture_time.year}{capture_time.month}{capture_time.day}_{capture_time.hour}{capture_time.minute}{capture_time.second}.png"
        )
