from playground.tv import *
orbit = 9
directory = '/pdo/ramp/orbit-{}/ffi_fits'.format(orbit)

# make a movie of each camera
for c in [1, 2, 3, 4]:
    i = illustratefits(pattern='/pdo/ramp/orbit-9/ffi_fits/tess*-*-{}-crm-ffi_dehoc.fits'.format(c),
                       ext_image=0, get_camera=camera_from_filename)
    i.plot()
    filename = 'orbit-{}-camera-{}-illustrated.pdf'.format(orbit, c)
    plt.savefig(filename, dpi=1000)
    print("saved to {}".format(filename))
    animate(i, filename=filename.replace('.pdf', '.mp4'), dpi=400,
            cadence=1 * u.s)  # dehocs have no time, so use 1s
