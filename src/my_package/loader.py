import os
from typing import Union
import h5py
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord


#Given the column names/dataset names, loads the datasets from hdf5 file
class StellarCatalogLoader:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        # This dictionary holds columns in memory once loaded
        self._cache = {}

    def get_columns(self, columns):
        # Identify which requested columns are NOT yet in our RAM cache
        for col in columns:
            if col not in ['ra', 'dec', 'xi', 'ext', 'parallax', 'parallax_err', 'quality_flags']:
                raise ValueError(f"Requested column {col} not in dataset.")
            
        missing_cols = [col for col in columns if col not in self._cache]
        
        if missing_cols:
            print(f"Loading {missing_cols} from disk into RAM (this happens only once)...")
            
            # Temporary storage to accumulate the list chunks before a single concatenate
            temp_storage = {col: [] for col in missing_cols}
            
            # Read through the 10 files
            for i in range(10):
                file_path = os.path.join(self.data_dir, f"xpparams_v2_zenodo_0{i}.h5")
                with h5py.File(file_path, 'r') as f:
                    if 'ra' in missing_cols:
                        temp_storage['ra'].append(f['ra'][:])
                    if 'dec' in missing_cols:
                        temp_storage['dec'].append(f['dec'][:])                    
                    if 'xi' in missing_cols:
                        temp_storage['xi'].append(f['stellar_params_est'][:, 3])
                    if 'ext' in missing_cols:
                        temp_storage['ext'].append(f['stellar_params_est'][:, 4])
                    if 'parallax' in missing_cols:
                        temp_storage['parallax'].append(f['stellar_params_est'][:, 5])
                    if 'parallax_err' in missing_cols:
                        temp_storage['parallax_err'].append(f['stellar_params_err'][:, 5])
                    if 'quality_flags' in missing_cols:
                        temp_storage['quality_flags'].append(f['quality_flags'][:])
            
            # Perform a SINGLE concatenate per column (drastically faster than looping concatenation)
            for col in missing_cols:
                self._cache[col] = np.concatenate(temp_storage[col])
                
        # Return the requested columns straight from memory
        if len(columns) == 1:
            return self._cache[columns[0]]
        return tuple(self._cache[col] for col in columns)
    
    def clear_cache(self, columns=None):
        """
        Clears the loaded data arrays from system RAM.
        
        Parameters:
        -----------
        columns : list of str, optional
            If specified, only clears the selected columns (e.g., ['parallax']).
            If None (default), empties the entire RAM cache.
        """
        if columns is None:
            self._cache.clear()
            print("System RAM completely cleared. All columns dropped.")
        else:
            for col in columns:
                if col in self._cache:
                    del self._cache[col]
                    print(f"Dropped '{col}' from RAM cache.")
                else:
                    print(f"'{col}' was not active in RAM.")


class HDF5Loader:
    def __init__(self, data_dir : Union[str, os.PathLike], fname : Union[str, os.PathLike]):
        self.data_dir = data_dir
        self.fname = fname
        self._cache = {}

# Given a tuple of HDF5 datasets, reads and returns those datasets
    def load_data(self, data_path : tuple):
        # Identify which requested columns are NOT yet in our RAM cache
        missing_data = [path for path in data_path if path not in self._cache]        
        if missing_data:
            print(f"Loading {missing_data} from disk into RAM (this happens only once)...")
            file_path = os.path.join(self.data_dir, self.fname)
            with h5py.File(file_path, 'r') as f:
                for path in missing_data:
                    self._cache[path] = f[path][:]
        if len(data_path) == 1:
            return self._cache[data_path[0]]
        return tuple(self._cache[path] for path in data_path)
                
    
#Load inverse noise maps to store field information
#field_name is one of 'CMB' or 'GAL'
class Field:
    def __init__(self, field_name : str, data_dir : Union[str, os.PathLike]):
        self.field_name = field_name
        with h5py.File(os.path.join(data_dir, 'BK24_radec_pvar.h5'), 'r') as f:
            self.xtic = f[f'{field_name}_B3_100/x_tic'][:,0]
            self.ytic = f[f'{field_name}_B3_100/y_tic'][:,0]
            self.Pw = f[f'{field_name}_B3_100/map'][:,:].T
            self.Pw *= 1. / self.Pw[~(self.Pw != self.Pw)].max()

    def get_mesh(self, galactic = False):
        """
        Gets the meshed longitude and latitude, in degrees, of the field footprint.
        Note: if galactic = True, the mesh is not rectangular, so lon and lat values depend on each other!
        """
        if not galactic:
            return np.meshgrid(self.xtic, self.ytic)
        else:
            xgrid, ygrid = np.meshgrid(self.xtic, self.ytic)
            coords = SkyCoord(ra = xgrid * u.degree, dec = ygrid * u.degree, frame = 'icrs')
            gal_coords = coords.transform_to('galactic')
            lgrid = gal_coords.l.degree
            bgrid = gal_coords.b.degree
            return lgrid, bgrid

    def get_bbox(self, galactic = False):
        """
        Gets rectangular bounding box of field. Use only when the shape of the footprint is not important.
        Wraps longitude to the range [-180, 180].
        """
        if not galactic:
            # Can use 1D edges, not mesh, since the field is rectangular in celestial frame.
            return np.min(self.xtic), np.max(self.xtic), np.min(self.ytic), np.max(self.ytic)
        else:            
            lgrid, bgrid = self.get_mesh(galactic=True)
            lw = np.mod(lgrid + 180, 360) - 180  # wrap to [-180,180]
            return (np.min(lw), np.max(lw), np.min(bgrid), np.max(bgrid))

