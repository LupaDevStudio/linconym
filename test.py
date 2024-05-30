from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation, AnimationTransition
from kivy.properties import NumericProperty, ListProperty
import random as rd

Builder.load_string('''                               
<Loading>:
                     
    RelativeLayout:
        id: relative_layout
        canvas.before:
            PushMatrix
            Rotate:
                angle: root.angle
                axis: 0, 0, 1
                origin: root.center
        canvas.after:
            PopMatrix

        Image:
            id: my_image
            source: "resources/images/front_daily_wheel.png"
            size_hint: None, None
            size: 500, 500
            pos_hint: {'center_x': 0.5, "center_y": 0.5}
    
    Image:
        id: image
        source: "resources/images/back_daily_wheel.png"
        size_hint: None, None
        size: 500, 500
        pos_hint: {'center_x': 0.5, "center_y": 0.5}  
''')


class Loading(FloatLayout):
    angle = NumericProperty(0)

    def __init__(self, **kwargs):

        super(Loading, self).__init__(**kwargs)
        number_of_turns = rd.randint(4, 8)
        last_angle = rd.randint(0, 360) + 360 * number_of_turns
        anim = Animation(angle=last_angle, duration=number_of_turns+1,
                         t=AnimationTransition.out_quad)
        anim.start(self)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0


class TestApp(App):
    def build(self):
        return Loading()


TestApp().run()
