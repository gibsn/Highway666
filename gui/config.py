from tkinter import Frame, Button, Label, Spinbox, X, Tk


class ConfigGui():
    def __init__(self, title, width, height):
        self.root = Tk()
        self.root.wm_title(title)
        self.root.wm_minsize(width, height)

        self.init_model_params()
        self.init_buttons()

    def init_buttons(self):
        self.buttons_frame = Frame(self.root)

        self.start_button = Button(self.buttons_frame, text='Start', command=self.start)
        self.start_button.pack(side='left')

        self.exit_button = Button(self.buttons_frame, text='Exit', command=self.quit)
        self.exit_button.pack(side='left')

        self.buttons_frame.pack(side='bottom')

    def init_model_params(self):
        self.speed_inf_frame, self.speed_inf_label, self.speed_inf = init_speed_inf(self.root)
        self.speed_sup_frame, self.speed_sup_label, self.speed_sup = init_speed_sup(self.root)

        self.spawn_inf_frame, self.spawn_inf_label, self.spawn_inf = init_spawn_inf(self.root)
        self.spawn_sup_frame, self.spawn_sup_label, self.spawn_sup = init_spawn_sup(self.root)

        self.slow_factor_frame, self.slow_factor_label, self.slow_factor = init_slow_factor(self.root)
        self.slow_time_frame, self.slow_time_label, self.slow_time = init_slow_time(self.root)

    def start(self):
        print("Starting modeling")
        print("Initial speed: %s to %s" % (self.speed_inf.get(), self.speed_sup.get()))
        print("Spawn interval: %s to %s" % (self.spawn_inf.get(), self.spawn_sup.get()))
        print("Slowing factor: %s" % (self.slow_factor.get()))
        print("Slowing time: %s" % (self.slow_time.get()))

        # Call some func with model params

    def quit(self):
        print("Quitting on user's demand")
        self.root.destroy()

    def loop(self):
        self.root.mainloop()


def init_speed_inf(root):
    speed_inf_frame = Frame(root)
    speed_inf_frame.pack(fill=X)

    speed_inf_label = Label(speed_inf_frame, text='Min initial speed:')
    speed_inf_label.pack(side='left')

    speed_inf = Spinbox(speed_inf_frame, from_=0, to=200, width=4)
    speed_inf.delete(0, 1)
    speed_inf.insert(0, 30)
    speed_inf.pack(side='right')

    return speed_inf_frame, speed_inf_label, speed_inf


def init_speed_sup(root):
    speed_sup_frame = Frame(root)
    speed_sup_frame.pack(fill=X)

    speed_sup_label = Label(speed_sup_frame, text='Max initial speed:')
    speed_sup_label.pack(side='left')

    speed_sup = Spinbox(speed_sup_frame, from_=0, to=200, width=4)
    speed_sup.delete(0, 1)
    speed_sup.insert(0, 60)
    speed_sup.pack(side='right')

    return speed_sup_frame, speed_sup_label, speed_sup


def init_spawn_inf(root):
    spawn_inf_frame = Frame(root)
    spawn_inf_frame.pack(fill=X)

    spawn_inf_label = Label(spawn_inf_frame, text='Min spawn interval:')
    spawn_inf_label.pack(side='left')

    spawn_inf = Spinbox(spawn_inf_frame, from_=0, to=10, width=4)
    spawn_inf.delete(0, 1)
    spawn_inf.insert(0, 1)
    spawn_inf.pack(side='right')

    return spawn_inf_frame, spawn_inf_label, spawn_inf


def init_spawn_sup(root):
    spawn_sup_frame = Frame(root)
    spawn_sup_frame.pack(fill=X)

    spawn_sup_label = Label(spawn_sup_frame, text='Max spawn interval:')
    spawn_sup_label.pack(side='left')

    spawn_sup = Spinbox(spawn_sup_frame, from_=0, to=10, width=4)
    spawn_sup.delete(0, 1)
    spawn_sup.insert(0, 5)
    spawn_sup.pack(side='right')

    return spawn_sup_frame, spawn_sup_label, spawn_sup


def init_slow_factor(root):
    slow_factor_frame = Frame(root)
    slow_factor_frame.pack(fill=X)

    slow_factor_label = Label(slow_factor_frame, text='Slowing factor:')
    slow_factor_label.pack(side='left')

    slow_factor = Spinbox(slow_factor_frame, from_=0, to=1, width=4, increment=0.1)
    slow_factor.delete(0, 3)
    slow_factor.insert(0, 0.5)
    slow_factor.pack(side='right')

    return slow_factor_frame, slow_factor_label, slow_factor


def init_slow_time(root):
    slow_time_frame = Frame(root)
    slow_time_frame.pack(fill=X)

    slow_time_label = Label(slow_time_frame, text='Slowing time (s):')
    slow_time_label.pack(side='left')

    slow_time = Spinbox(slow_time_frame, from_=0, to=10, width=4)
    slow_time.delete(0, 1)
    slow_time.insert(0, 5)
    slow_time.pack(side='right')

    return slow_time_frame, slow_time_label, slow_time
