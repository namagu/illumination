'''
Define a generic sequence of images.
'''
from .Sequence import *

class Image_Sequence(Sequence):
    '''
    This isn't a standalone. Other image sequences inherit from it.
    '''
    spatial = {}

    @property
    def shape(self):
        '''
        Returns
        -------
        s : tuple
            The shape of the image stack (ntimes x nrows x ncols)
        '''
        d = self[0]
        return (self.N, d.shape[0], d.shape[1])

    def _gather_3d(self):
        '''
        Gather a 3D cube of images.

        This will generally work, but it
        may be faster if you already have
        access to the full 3D array stored
        in memory (as in a Stamp or TPF).

        Returns
        -------
        s : array
        The image stack, with shape (ntimes x nrows x ncols)
        '''

        s = np.zeros(self.shape)
        self.speak('gathering the sequence cube, with shape {}'.format(self.shape))
        for i in range(self.N):
            self.speak(' loaded frame {}/{}'.format(i+1, self.N), progress=True)
            s[i, :, :] = self[i]
        return s

    def median(self):
        '''
        Calculate the median image.

        Returns
        -------
        median : 2D image
            The median of the image sequence.
        '''

        try:
            self.spatial['median']
        except KeyError:
            self.speak('creating a median image for {}'.format(self))
            s = self._gather_3d()
            self.spatial['median'] = np.median(s, axis=0)
        return self.spatial['median']

    def sum(self):
        '''
        Calculate the sum of all the images.

        Returns
        -------
        sum : 2D image
            The median of the image sequence.
        '''

        s = self._gather_3d()
        return np.sum(s, axis=0)

    def mean(self):
        '''
        Calculate the sum of all the images.
        It works in an inline fashion, so you
        don't need to load the entire image
        cube into memory (that might get big!)

        Returns
        -------
        mean : 2D image
            The median of the image sequence.
        '''

        try:
            self.spatial['mean']
        except KeyError:
            self.speak('creating a mean image for {}'.format(self))

            # calculate the mean in a running fashion (less memory)
            total = np.zeros_like(self[0])
            for i in range(self.N):
                self.speak(' included frame {}/{} in mean'.format(i+1, self.N), progress=True)
                total += self[i]

            self.spatial['mean'] = total/self.N

        return self.spatial['mean']