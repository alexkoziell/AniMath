import pyglet

class Image():

    def __init__(self, filePath: str, x=0, y=0, start=0, end=-1):
        image = pyglet.image.load(filePath)
        self.sprite = pyglet.sprite.Sprite(image, x, y)
        if start < end:
            self.sprite.opacity = 0
            pyglet.clock.schedule_once(lambda dt: pyglet.clock.schedule_interval(self.fadeIn, 1/24.0),
                                       start)
            pyglet.clock.schedule_once(lambda dt: pyglet.clock.schedule_interval(self.fadeOut, 1/24.0),
                                       end)
    
    def fadeIn(self, dt):
        self.sprite.opacity += 10
        if self.sprite.opacity >= 255:
            self.sprite.opacity = 255
            pyglet.clock.unschedule(self.fadeIn)

    def fadeOut(self, dt):
        self.sprite.opacity -= 10
        if self.sprite.opacity <= 0:
            self.sprite.opacity = 0
            pyglet.clock.unschedule(self.fadeOut)