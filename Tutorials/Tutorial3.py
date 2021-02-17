### The Info data structure ###

import os
import mne

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_filt-0-40_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file)
print(raw.info)

info = mne.io.read_info(sample_data_raw_file)
print(info)


######## Querying the Info object ########
print(info.keys())
print()                     # insert a blank line
print(info['ch_names'])
print(info['chs'][0].keys())


######## Querying the Info object ########
print(mne.pick_channels(info['ch_names'], include=['MEG 0312', 'EEG 005']))
print(mne.pick_channels(info['ch_names'], include=[], exclude=['MEG 0312', 'EEG 005']))

print(mne.pick_types(info, meg=False, eeg=True, exclude=[]))


'''
    Here the ^ represents the beginning of the string and . character 
    matches any single character, so both EEG and EOG channels will be selected
'''
print(mne.pick_channels_regexp(info['ch_names'], '^E.G'))       


######## Obtaining channel type information ########
print(mne.channel_type(info, 25))

picks = (25, 76, 77, 319)
print([mne.channel_type(info, x) for x in picks])
print(raw.get_channel_types(picks=picks))

ch_idx_by_type = mne.channel_indices_by_type(info)
print(ch_idx_by_type.keys())
print(ch_idx_by_type['eog'])


######## Obtaining channel type information ########
print(info['nchan'])
eeg_indices = mne.pick_types(info, meg=False, eeg=True)
print(mne.pick_info(info, eeg_indices)['nchan'])
