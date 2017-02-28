from graph import moving_object


class Car(moving_object.MovingObject):
    def __init__(self, topleft, speed, width, height):
        moving_object.MovingObject.__init__(self, topleft, speed, (1, 0), width, height, "blue")

        self.wanted_speed = speed
