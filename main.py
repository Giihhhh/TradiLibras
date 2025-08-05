from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from reconhecer_letra import prever_letra

class CameraApp(App):
    def build(self):
        self.img = Image()
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return self.img

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            letra = prever_letra(frame)
            frame = cv2.putText(frame, f'Letra: {letra}', (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture

    def on_stop(self):
        self.capture.release()

if __name__ == '__main__':
    CameraApp().run()
