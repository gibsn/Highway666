from graph import moving_object


class Car(moving_object.MovingObject):
    def __init__(self, topleft, speed, width=0, height=0, image=None):
        moving_object.MovingObject.__init__(self, topleft, speed, (0, 0), width, height, image=image)

        self.wanted_speed = speed
