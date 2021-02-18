### Interpolating bad channels ###

import os
from copy import deepcopy
import numpy as np
import mne

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file, verbose=False)


######## Marking bad channels ########
print(raw.info['bads'])

picks = mne.pick_channels_regexp(raw.ch_names, regexp='EEG 05.')
raw.plot(order=picks, n_channels=len(picks))

picks = mne.pick_channels_regexp(raw.ch_names, regexp='MEG 2..3')
raw.plot(order=picks, n_channels=len(picks))

original_bads = deepcopy(raw.info['bads'])
raw.info['bads'].append('EEG 050')               # add a single channel
raw.info['bads'].extend(['EEG 051', 'EEG 052'])  # add a list of channels
bad_chan = raw.info['bads'].pop(-1)  # remove the last entry in the list
raw.info['bads'] = original_bads     # change the whole list at once

# default is exclude='bads':
good_eeg = mne.pick_types(raw.info, meg=False, eeg=True)
all_eeg = mne.pick_types(raw.info, meg=False, eeg=True, exclude=[])
print(np.setdiff1d(all_eeg, good_eeg))
print(np.array(raw.ch_names)[np.setdiff1d(all_eeg, good_eeg)])


######## When to look for bad channels ########
raw2 = raw.copy()
raw2.info['bads'] = []
events = mne.find_events(raw2, stim_channel='STI 014')
epochs = mne.Epochs(raw2, events=events)['2'].average().plot()


######## Interpolating bad channels ########
raw.crop(tmin=0, tmax=3).load_data()

eeg_data = raw.copy().pick_types(meg=False, eeg=True, exclude=[])
eeg_data_interp = eeg_data.copy().interpolate_bads(reset_bads=False)

for title, data in zip(['orig.', 'interp.'], [eeg_data, eeg_data_interp]):
    fig = data.plot(butterfly=True, color='#00000022', bad_color='r')
    fig.subplots_adjust(top=0.9)
    fig.suptitle(title, size='xx-large', weight='bold')