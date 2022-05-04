import pygame as pg


class Controller:
    """
    Abstract class for mapping control inputs to control outputs via a source function.
    """

    def __init__(self, scheme: list):
        """
        Take in a list that relates a control name to a control input to put into the source function.

        :param scheme: list of tuples with form: (name(str), input(any)).
        """
        self.controls = []  # list of name and control input pairs
        self.outs = {}  # map from name to control output

        self.update(None)
        for name, control, in scheme:
            self.controls.append((name, control))
            self.outs[name] = self.source(control)

    def __getitem__(self, item):
        """
        Gets a particular control output, which may be a boolean or a numerical value.

        :param item: the name string of the control
        :return: the current value of the control called "name." Must call tick() to update.
        """
        return self.outs[item]

    def __setitem__(self, key, value) -> bool:
        """
        Sets a particular control ouput to the desired value, but only if it exits.

        :param key: the control name
        :param value: the control value to force set
        :return: true if sucessful, false if control doesn't exist
        """
        if key in self.outs:
            self.outs[key] = value
            return True
        else:
            return False

    def tick(self, state=None):
        """
        Updates the Controller's ControlScheme's outputs on each call of tick.

        :param state: optional state parameter to condition the update function
        """
        self.update(state)
        for name, control in self.controls:
            self.outs[name] = self.source(control)

    def update(self, state=None):
        """
        Updates any of the internal functions of the Controller once each tick.

        :param state: optional state parameter to condition the update function
        :return: true when successful
        """
        return True

    def source(self, control):
        """
        Defines a source function when overloaded. By default, it just returns the control.

        :param control: an input for the source function
        :return: the output from the source function
        """
        return False


class KeyboardController(Controller):
    """
    A keyboard implementation of the Controller
    """
    keys = []

    def update(self, state=None):
        """
        Updates key list.

        :param state: does nothing.
        """
        self.keys = pg.key.get_pressed()

    def source(self, control):
        """
        Sorce function implemented with the keys list.

        :param control: the key code.
        :return: true if the key is pressed, false otherwise
        """
        return self.keys[control]
