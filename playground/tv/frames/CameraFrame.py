from .imshowFrame import *
from matplotlib.colors import SymLogNorm, LogNorm


class CameraFrame(imshowFrame):
    frametype = 'Camera'

    def __init__(self, *args, **kwargs):

        imshowFrame.__init__(self, *args, **kwargs)

        self.xmin, self.ymin = 0, 0
        try:
            # if there's an image, use it to set the size
            self.ymax, self.xmax = self.data[0].shape
        except (IndexError, AttributeError, TypeError):
            # allow us to create an empty image
            self.ymax = 4156
            self.xmax = 4272


# FIXME -- make sure I understand the geometry here (I don't think I do now)
class Camera1Frame(CameraFrame):
    frametype = 'Camera 1'

    def _transformimage(self, image):
        '''
        horizontal:
                (should be) +x is up, +y is left
                (looks like) +x is up, +y is right
        '''
        if self._get_orientation() == 'horizontal':
            return image.T[:, :]

    def _transformxy(self, x, y):
        '''
        This handles the same transformation as that which goes into
        transform image, but for x and y arrays.
        '''
        if self._get_orientation() == 'horizontal':
            displayy = x
            displayx = y  # self.ymax-y
        return displayx, displayy


class Camera2Frame(Camera1Frame):
    frametype = 'Camera 2'


class Camera3Frame(CameraFrame):
    frametype = 'Camera 3'

    def _transformimage(self, image):
        '''
        horizontal:
                (should be) +x is down, +y is right
                (looks like) +x is down, +y is left
        '''
        if self._get_orientation() == 'horizontal':
            return image.T[::-1, ::-1]

    def _transformxy(self, x, y):
        '''
        This handles the same transformation as that which goes into
        transform image, but for x and y arrays.
        '''
        if self._get_orientation() == 'horizontal':
            displayy = self.xmax - x
            displayx = self.ymax - y
        return displayx, displayy


class Camera4Frame(Camera3Frame):
    frametype = 'Camera 4'


cameras = {'cam1': Camera1Frame, 'cam2': Camera2Frame,
           'cam3': Camera3Frame, 'cam4': Camera4Frame}
