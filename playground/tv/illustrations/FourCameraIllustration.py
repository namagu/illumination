from .IllustrationBase import *
from ..frames import CameraFrame, cameras

__all__ = ['FourCameraIllustration']

class FourCameraIllustration(IllustrationBase):
    '''
    For displaying a single Camera.
    '''
    illustrationtype = 'FourCamera'
    def __init__(self, cam1=[], cam2=[], cam3=[], cam4=[], orientation='horizontal', sizeofcamera = 4, **kwargs):

        # set up the basic geometry of the main axes
        sizeofcamera = 4
        N = 4
        self.orientation = orientation
        if self.orientation == 'horizontal':
            cols = N
            rows = 1
        IllustrationBase.__init__(self, rows, cols,
                                figkw=dict(figsize=(sizeofcamera*cols, sizeofcamera*rows*1.2)),
                                hspace=0.02, wspace=0.02,
                                left=0.05, right=0.95,
                                bottom=0.1, top=0.9)

        # initiate the axes for each camera
        for i in range(rows):
            for j in range(cols):

                # populate the axes on the main camera grid
                ax = plt.subplot(self.grid[i, j])

                # create a CameraFrame for this camera
                n = i*cols + j+1
                name = 'cam{}'.format(i*cols + j+1)
                self.frames[name] = cameras[name](ax=ax, data=locals()[name], illustration=self, **kwargs)