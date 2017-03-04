from graph import moving_object


class Car(moving_object.MovingObject):
    def __init__(self, topleft, speed, width, height, image=None):
        moving_object.MovingObject.__init__(self, topleft, speed, (0, 0), width, height, image=image)

        self.wanted_speed = speed
