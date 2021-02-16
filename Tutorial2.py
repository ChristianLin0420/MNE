### Parsing events from raw data ###

import os
import numpy as np
import mne

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file)
raw.crop(tmax=60).load_data()


######## What is a STIM channel? ########

raw.copy().pick_types(meg=False, stim=True).plot(start=3, duration=6) 