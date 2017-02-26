#!/usr/local/bin/python3


from gui.config import ConfigGui

if __name__ == "__main__":
    print("Starting GUI")

    main_window = ConfigGui("Highway666 by Kirill Alekseev", 300, 200)
    main_window.loop()
