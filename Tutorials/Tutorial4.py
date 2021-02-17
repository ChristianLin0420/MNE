### Working with sensor locations ###

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa
import mne

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True, verbose=False)


######## Working with built-in montages ########
montage_dir = os.path.join(os.path.dirname(mne.__file__),
                           'channels', 'data', 'montages')
print('\nBUILT-IN MONTAGE FILES')
print('======================')
print(sorted(os.listdir(montage_dir)))

ten_twenty_montage = mne.channels.make_standard_montage('standard_1020')
print(ten_twenty_montage)

# these will be equivalent:
# raw_1020 = raw.copy().set_montage(ten_twenty_montage)
# raw_1020 = raw.copy().set_montage('standard_1020')

fig = ten_twenty_montage.plot(kind='3d')
fig.gca().view_init(azim=70, elev=15)
ten_twenty_montage.plot(kind='topomap', show_names=False)


######## Controlling channel projection (MNE vs EEGLAB) ########
biosemi_montage = mne.channels.make_standard_montage('biosemi64')
biosemi_montage.plot(show_names=False)
biosemi_montage.plot(show_names=False, sphere=0.07)
biosemi_montage.plot(show_names=False, sphere=(0.03, 0.02, 0.01, 0.075))
biosemi_montage.plot()
biosemi_montage.plot(sphere=(0, 0, 0.035, 0.094))


######## Reading sensor digitization files ########
fig = plt.figure()
ax2d = fig.add_subplot(121)
ax3d = fig.add_subplot(122, projection='3d')
raw.plot_sensors(ch_type='eeg', axes=ax2d)
raw.plot_sensors(ch_type='eeg', axes=ax3d, kind='3d')
ax3d.view_init(azim=70, elev=15)


######## Rendering sensor position with mayavi ########
fig = mne.viz.plot_alignment(raw.info, trans=None, dig=False, eeg=False,
                             surfaces=[], meg=['helmet', 'sensors'],
                             coord_frame='meg')
mne.viz.set_3d_view(fig, azimuth=50, elevation=90, distance=0.5)


######## Working with layout files ########
layout_dir = os.path.join(os.path.dirname(mne.__file__),
                          'channels', 'data', 'layouts')
print('\nBUILT-IN LAYOUT FILES')
print('=====================')
print(sorted(os.listdir(layout_dir)))

biosemi_layout = mne.channels.read_layout('biosemi')
biosemi_layout.plot()  # same result as: mne.viz.plot_layout(biosemi_layout)

midline = np.where([name.endswith('z') for name in biosemi_layout.names])[0]
biosemi_layout.plot(picks=midline)

layout_from_raw = mne.channels.make_eeg_layout(raw.info)
# same result as: mne.channels.find_layout(raw.info, ch_type='eeg')
layout_from_raw.plot()


