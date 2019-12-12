import pyglet
import pyglet.gl as pygl

import subprocess as sp

FFMPEG_BIN = 'ffmpeg'
command = [ FFMPEG_BIN,
        '-y', # (optional) overwrite output file if it exists
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-s', '640x480', # size of one frame
        '-pix_fmt', 'rgb24',
        '-r', '24', # frames per second
        '-i', '-', # The imput comes from a pipe
        '-vf', 'transpose=cclock_flip,transpose=cclock', # flips openGl output the right way up
        '-an', # Tells FFMPEG not to expect any audio
        '-vcodec', 'mpeg4',
        'my_output_videofile.mp4' ]

pipe = sp.Popen( command, stdin=sp.PIPE, stderr=sp.PIPE)

window = pyglet.window.Window()

label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size =36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

@window.event
def on_key_press(symbol, modifiers):
    print('A key was pressed.')
    pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')

@window.event
def on_draw():
    window.clear()
    label.draw()

    square_vertices = pyglet.graphics.vertex_list_indexed(4,
        [0, 1, 2, 0, 2, 3],
        ('v2i', (100, 100,
                  150, 100,
                  150, 150,
                  100, 150))
    )
    square_vertices.draw(pyglet.gl.GL_TRIANGLES)

    line_vertices = pyglet.graphics.vertex_list(2,
        ('v2i', (10, 100,
                 15, 200)),
        ('c3B', (0, 0, 255,
                 0, 255, 0))
    )
    line_vertices.draw(pyglet.gl.GL_LINES)

window.push_handlers(pyglet.window.event.WindowEventLogger())

def write_to_video(dt):
    buffer = ( pygl.gl.GLubyte * (3*window.width*window.height) )(0)
    pygl.gl.glReadPixels(0, 0, 640, 480, pygl.gl.GL_RGB, 
                         pygl.gl.GL_UNSIGNED_BYTE, buffer)

    #frame = pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
    #pitch = -(frame.width * len('RGBA'))
    #print(frame.get_data('RGB', pitch))
    pipe.stdin.write(buffer) #frame.get_data('RGB', frame.pitch) )

pyglet.clock.schedule_interval(write_to_video, 0.01)
pyglet.app.run()