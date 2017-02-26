from tkinter import *


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
        self.speed_inf_frame = Frame(self.root)
        self.speed_sup_frame = Frame(self.root)
        self.spawn_inf_frame = Frame(self.root)
        self.spawn_sup_frame = Frame(self.root)
        self.slow_factor_frame = Frame(self.root)
        self.slow_time_frame = Frame(self.root)

        self.speed_inf_frame.pack(fill=X)
        self.speed_sup_frame.pack(fill=X)
        self.spawn_inf_frame.pack(fill=X)
        self.spawn_sup_frame.pack(fill=X)
        self.slow_factor_frame.pack(fill=X)
        self.slow_time_frame.pack(fill=X)

        self.speed_inf_label = Label(self.speed_inf_frame, text='Min initial speed:')
        self.speed_inf = Spinbox(self.speed_inf_frame, from_=0, to=200, width=4)
        self.speed_inf_label.pack(side='left')
        self.speed_inf.pack(side='right')

        self.speed_sup_label = Label(self.speed_sup_frame, text='Max initial speed:')
        self.speed_sup = Spinbox(self.speed_sup_frame, from_=0, to=200, width=4)
        self.speed_sup_label.pack(side='left')
        self.speed_sup.pack(side='right')

        self.spawn_inf_label = Label(self.spawn_inf_frame, text='Min spawn interval:')
        self.spawn_inf = Spinbox(self.spawn_inf_frame, from_=0, to=10, width=4)
        self.spawn_inf_label.pack(side='left')
        self.spawn_inf.pack(side='right')

        self.spawn_sup_label = Label(self.spawn_sup_frame, text='Max spawn interval:')
        self.spawn_sup = Spinbox(self.spawn_sup_frame, from_=0, to=10, width=4)
        self.spawn_sup_label.pack(side='left')
        self.spawn_sup.pack(side='right')

        self.slow_factor_label = Label(self.slow_factor_frame, text='Slowing factor:')
        self.slow_factor = Spinbox(self.slow_factor_frame, from_=0, to=1, width=4, increment=0.1)
        self.slow_factor_label.pack(side='left')
        self.slow_factor.pack(side='right')

        self.slow_time_label = Label(self.slow_time_frame, text='Slowing time (s):')
        self.slow_time = Spinbox(self.slow_time_frame, from_=0, to=10, width=4)
        self.slow_time_label.pack(side='left')
        self.slow_time.pack(side='right')

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
