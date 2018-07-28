from ...imports import *

class FrameBase:

	data = None
	plotted = None
	frametype = 'base'
	timeunit = 'day'

	def __init__(self, ax=None,
					   data=None,
					   name='',
					   illustration=None,
					   aspectratio=1,
					   **kwargs):
		'''
		Initialize this Frame.


		choosing the Axes in which it will display,
		and the setting data to be associated with it.

		Parameters
		----------

		ax : matplotlib.axes.Axes instance
			All plotting will happen inside this ax.
			If set to None, the `self.ax attribute` will
			need to be set manually before plotting.

		data : flexible
			It can be custom object (e.g. a Stamp),
			or simple arrays, or a list of HDULists,
			or something else, depending on
			what this actual Frame does with it
			in `plot` and `update`.

		name : str
			A name to give this Frame.
		'''

		# assign this frame an axes to sit in
		self.ax = ax

		# this is likely a Sequence of some kind
		self.data = data

		# is there another overarching frame this one should be aware of?
		self.illustration = illustration

		# what is the intrinsic aspect ratio of this frame?
		self.aspectratio = aspectratio

		# keep track of a list of frames included in this one
		self.includes = []

		# store a name for this frame, if there is one
		self.name = name
		self._currenttimestring = None

	@property
	def offset(self):
		'''
		Get a time offset, to use as a zero-point.

		Returns
		-------
		offset : float
			An appropriate time zero-point (in JD).
		'''

		# is an offset already defined?
		try:
			return self._offset
		except AttributeError:
			# is there a minimum of the illustration's times?
			try:
				self._offset = np.min(self.illustration._gettimes().jd)
			except (AttributeError, ValueError):
				# otherwise, use only this frame to estimate the offset
				try:
					self._offset = np.min(self._gettimes().jd)
				except ValueError:
					self._offset = 0.0

			return self._offset

	def _timestring(self, time):
		'''
		Return a string, given an input time.

		Parameters
		----------
		time : astropy Time
			A particular time.

		Returns
		-------
		timestring : str
			A string describing the times.
		'''

		days = time.jd-self.offset
		inunits = (days*u.day).to(self.timeunit)
		return 't={:.5f}{:+.5f}'.format(self.offset, inunits)

	def __repr__(self):
		'''
		Default string representation for this frame.
		'''
		return '<{} Frame | data={} | name={}>'.format(self.frametype,
													   self.data,
													   self.name)

	def plot(self):
		'''
		This should be redefined in a class that inherits from FrameBase.
		'''
		raise RuntimeError("Don't know how to `plot` {}".format(self.frametype))

	def update(self, *args, **kwargs):
		'''
		This should be redefined in a class that inherits from FrameBase.
		'''
		raise RuntimeError("Don't know how to `update` {}".format(self.frametype))

	def _find_timestep(self, time):
		'''
		Given a time, identify its index.

		Parameters
		----------

		time : float
			A single time (in JD?).

		Returns
		-------
		index : int
			The index of the *closest* time point.
		'''
		return self.data._find_timestep(time)

	def _gettimes(self):
		'''
		Get the available times associated with this frame.
		'''

		# does the data have a time axis defined?
		try:
			return self.data.time
		# if not, return an empty time
		except AttributeError:
			return Time([], format='gps')

	def _timesandcadence(self, round=None):
		'''
		Get all the unique times available across all the frames,
		along with a suggested cadence set by the minimum
		(rounded) differences between times.

		Parameters
		----------
		round : float
			All times will be rounded to this value.
			Times separated by less than this value
			will be considered identical.
		'''

		# store this calculation with the illustration, so it doesn't need repeating
		try:
			self._precaculatedtimesandcadence
		except AttributeError:
			self._precaculatedtimesandcadence = {}
		try:
			times, cadence = self._precaculatedtimesandcadence[round]
		except KeyError:
			gps = self._gettimes().gps

			if round is None:
				diffs = np.diff(np.sort(gps))
				round = np.min(diffs[diffs > 0])

			baseline = np.min(gps)
			rounded = round*np.round((gps-baseline)/round) + baseline
			uniquegpstimes = np.unique(rounded)
			cadence = np.min(np.diff(uniquegpstimes))*u.s
			times = Time(uniquegpstimes, format='gps')
			self._precaculatedtimesandcadence[round] = times, cadence

		return times, cadence

	def _transformimage(self, image):
		'''
		Some frames will want to flip or rotate an image before display.
		This handles that transformation. (This should probably be set
		up as an matplotlib.axes transform type of thing.)
		'''
		return image


	def _transformxy(self, x, y):
		'''
		This handles the same transformation as that which goes into
		transform image, but for x and y arrays.
		'''
		return x, y

	def _get_orientation(self):
		'''
		Figure out the orientation of the overarching illustration.
		'''
		try:
			return self.illustration.orientation
		except:
			return 'vertical'
