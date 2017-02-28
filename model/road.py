from graph import static_object


class Road(static_object.StaticObject):
    def __init__(self, width, height):
        static_object.StaticObject.__init__(self, (0, 0), width, height, "grey")
    #
    # def __init__(self, image):
    #     static_object.StaticObject.__init__(self, (0, 0), image)
