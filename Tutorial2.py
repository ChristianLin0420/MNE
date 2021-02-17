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

events = mne.find_events(raw, stim_channel='STI 014')
print(events[:5])  # show the first 5


######## Reading embedded events as Annotations ########
testing_data_folder = mne.datasets.testing.data_path()
eeglab_raw_file = os.path.join(testing_data_folder, 'EEGLAB', 'test_raw.set')
eeglab_raw = mne.io.read_raw_eeglab(eeglab_raw_file)
print(eeglab_raw.annotations)

print(len(eeglab_raw.annotations))
print(set(eeglab_raw.annotations.duration))
print(set(eeglab_raw.annotations.description))
print(eeglab_raw.annotations.onset[0])


######## Converting between Events arrays and Annotations objects ########
events_from_annot, event_dict = mne.events_from_annotations(eeglab_raw)
print(event_dict)
print(events_from_annot[:5])

custom_mapping = {'rt': 77, 'square': 42}
(events_from_annot,
 event_dict) = mne.events_from_annotations(eeglab_raw, event_id=custom_mapping)
print(event_dict)
print(events_from_annot[:5])

# make the opposite conversion 
# (from an Events array to an Annotations object)
mapping = {1: 'auditory/left', 2: 'auditory/right', 3: 'visual/left',
           4: 'visual/right', 5: 'smiley', 32: 'buttonpress'}
annot_from_events = mne.annotations_from_events(
    events=events, event_desc=mapping, sfreq=raw.info['sfreq'],
    orig_time=raw.info['meas_date'])
raw.set_annotations(annot_from_events)

raw.plot(start = 5, duration = 5)


######## Making multiple events per annotation ########

# create the REM annotations
rem_annot = mne.Annotations(onset=[5, 41],
                            duration=[16, 11],
                            description=['REM'] * 2)
raw.set_annotations(rem_annot)
(rem_events, rem_event_dict) = mne.events_from_annotations(raw, chunk_duration=1.5)

print(np.round((rem_events[:, 0] - raw.first_samp) / raw.info['sfreq'], 3))

