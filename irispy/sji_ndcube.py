
import numpy as np
from astropy.io import fits
import astropy.units as u
from ndcube import NDCube
from ndcube.wcs_util import WCS

from irispy import iris_tools

class IRISSJI(NDCube):
    """Class for reading, visualixing, and analyzing IRIS SJI data files.

    Parameters
    ----------
    filename: `str`
        IRIS SJI file name from which to read in data.
    """
    def __init__(self, filename):
        # Define data unit and readout noise.
        DN_unit = iris_tools.DN_UNIT["SJI"]
        readout_noise = iris_tools.READOUT_NOISE["SJI"]
        # Read file.
        hdulist = fits.open(filename)
        data = hdulist[0].data
        meta = hdulist[0].header
        wcs_ = WCS(hdulist[0].header)
        hdulist.close()
        # Derive uncertainty of data
        uncertainty = u.Quantity(np.sqrt(
            (data*DN_unit).to(u.ct).value + readout_noise.to(u.ct).value**2),
            unit=u.ct).to(DN_unit).value
        # Create NDCube with this info
        super(IRISSJI, self).__init__(
            data, wcs_, uncertainty=uncertainty, unit=DN_unit, meta=meta)