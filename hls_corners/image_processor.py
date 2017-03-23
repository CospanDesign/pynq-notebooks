#License Here


__author__      = "David McCoy"
__copyright__   = "Copyright 2017, Cospan Design"
__email__       = "dave.mccoy@cospandesign.com"


import os

from pynq import PL
from pynq import MMIO

CONTROL_ADDR                = 0x00
GIE_ADDR                    = 0x04
INT_CHANNEL_ENABLE_ADDR     = 0x08
INT_CHANNEL_STATUS_ADDR     = 0x0C
IMAGE_ROWS_ADDR             = 0x14
IMAGE_COLS_ADDR             = 0x1C

#Bits
CONTROL_START_BIT           = 0
CONTROL_DONE_BIT            = 1
CONTROL_IDLE_BIT            = 2
CONTROL_READY_BIT           = 3
CONTROL_AUTO_RESTART_BIT    = 7


class ImageProcessor (object):
    """Configure Image Processor

    Configure the behavior of the image processor

    Attributes
    ----------
    Nothing

    """

    def __init__(self, image_processor_name, debug = False):
        """Return a new AXI Stream Interconnect Object

        Parameters
        ----------
        ip : str
            The name of the IP required for the AXI Stream Interconnect
        """
        self.debug = debug
        if image_processor_name not in PL.ip_dict:
            raise LookupError("No such AXI Stream IP in the overlay.")
        self.image_proc = MMIO( PL.ip_dict[image_processor_name][0],
                                PL.ip_dict[image_processor_name][1])

    def get_control(self):
        return self.image_proc.read(0x00)

    def enable(self, enable, auto_restart = True):
        """Enables the image processor core

        parameters
        ----------
        enable : boolean
            True, enables the image processor core
        auto_restart : boolean
            True: The core will continue processing images until the user
            explicitly disables it

        Returns
        -------
        None
        """
        control = 0x00
        if enable:
            control |= (1 << CONTROL_START_BIT)

        if auto_restart:
            control |= (1 << CONTROL_AUTO_RESTART_BIT)
        if self.debug: print ("Message to control (0x%04X): 0x%08X", \
                                (CONTROL_ADDR, control))
        self.image_proc.write(CONTROL_ADDR, control)

    def is_enabled(self):
        """ Returns true if the image processor core is enabled

        parameters
        ----------
        None

        Returns
        -------
        Boolean
            True: Image Processor Core is enabled
            False: Image Processor Core is not enabled
        """
        return self.image_proc.is_register_bit_set(CONTROL_ADDR, \
                                                   CONTROL_START_BIT)

    def set_image_width(self, width):
        """Sets the image width

        Parameters
        ----------
        width : int
            Width of the image

        Returns
        -------
        None
        """
        self.image_proc.write(IMAGE_COLS_ADDR, width)

    def set_image_height(self, height):
        """Sets the image height

        Parameters
        ----------
        height : int
            Height of the image

        Returns
        -------
        None
        """
        self.image_proc.write(IMAGE_ROWS_ADDR, height)

    def get_image_width(self):
        """Gets the image width

        Paarameters
        -----------

        Returns
        -------
        int : width of the image
        """
        return self.image_proc.read(IMAGE_COLS_ADDR)

    def get_image_height(self):
        """Gets the image height

        Parameters
        ----------

        Returns
        -------
        int : height of the image
        """
        return self.image_proc.read(IMAGE_ROWS_ADDR)



