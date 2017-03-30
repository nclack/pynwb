from .core import docval, getargs, popargs
from .base import TimeSeries, Interface, _default_conversion, _default_resolution

import numpy as np
from collections import Iterable

class AnnotationSeries(TimeSeries):
    """
    Stores text-based records about the experiment. To use the
    AnnotationSeries, add records individually through
    add_annotation() and then call finalize(). Alternatively, if
    all annotations are already stored in a list, use set_data()
    and set_timestamps()

    All time series are created by calls to  NWB.create_timeseries().
    They should not not be instantiated directly
    """

    _ancestry = "TimeSeries,AnnotationSeries"
    _help = "Time-stamped annotations about an experiment."

    @docval({'name': 'name', 'type': str, 'doc': 'The name of this TimeSeries dataset'},
            {'name': 'source', 'type': str, 'doc': ('Name of TimeSeries or Modules that serve as the source for the data '
                                                   'contained here. It can also be the name of a device, for stimulus or '
                                                   'acquisition data')},
            {'name': 'data', 'type': (list, np.ndarray, TimeSeries), 'doc': 'The data this TimeSeries dataset stores. Can also store binary data e.g. image frames', 'default': list()},
            {'name': 'timestamps', 'type': (list, np.ndarray, TimeSeries), 'doc': 'Timestamps for samples stored in data', 'default': None},

            {'name': 'comments', 'type': str, 'doc': 'Human-readable comments about this TimeSeries dataset', 'default':None},
            {'name': 'description', 'type': str, 'doc': 'Description of this TimeSeries dataset', 'default':None},
            {'name': 'parent', 'type': 'NWBContainer', 'doc': 'The parent NWBContainer for this NWBContainer', 'default': None},
    )
    def __init__(self, **kwargs):
        name, source, data, timestamps = popargs('name', 'source', 'data', 'timestamps', kwargs)
        super(AnnotationSeries, self).__init__(name, source, data, 'n/a', resolution=np.nan, conversion=np.nan, timestamps=timestamps, **kwargs)


    @docval({'name': 'time', 'type': float, 'doc': 'The time for the anotation'},
            {'name': 'annotation', 'type': str, 'doc': 'the annotation'})
    def add_annotation(self, **kwargs):
        '''
        Add an annotation
        '''
        time, annotation = getargs('time', 'annotation', kwargs)
        self.fields['timestamps'].append(time)
        self.fields['data'].append(annotation)

class AbstractFeatureSeries(TimeSeries):
    """
    Represents the salient features of a data stream. Typically this
    will be used for things like a visual grating stimulus, where
    the bulk of data (each frame sent to the graphics card) is bulky
    and not of high value, while the salient characteristics (eg,
    orientation, spatial frequency, contrast, etc) are what important
    and are what are used for analysis

    All time series are created by calls to  NWB.create_timeseries().
    They should not not be instantiated directly
    """
    __nwbfields__ = ('feature_units', 'features')

    _ancestry = "TimeSeries,AbstractFeatureSeries"
    _help = "Features of an applied stimulus. This is useful when storing the raw stimulus is impractical."

    @docval({'name': 'name', 'type': str, 'doc': 'The name of this TimeSeries dataset'},
            {'name': 'source', 'type': str, 'doc': ('Name of TimeSeries or Modules that serve as the source for the data '
                                                   'contained here. It can also be the name of a device, for stimulus or '
                                                   'acquisition data')},
            {'name': 'feature_units', 'type': str, 'doc': 'The unit of each feature'},
            {'name': 'features', 'type': str, 'doc': 'Description of each feature'},

            {'name': 'data', 'type': (list, np.ndarray), 'doc': 'The data this TimeSeries dataset stores. Can also store binary data e.g. image frames', 'default': list()},
            {'name': 'resolution', 'type': float, 'doc': 'The smallest meaningful difference (in specified unit) between values in data', 'default': _default_resolution},
            {'name': 'conversion', 'type': float, 'doc': 'Scalar to multiply each element in data to convert it to the specified unit', 'default': _default_conversion},

            {'name': 'timestamps', 'type': (list, np.ndarray), 'doc': 'Timestamps for samples stored in data', 'default': None},
            {'name': 'starting_time', 'type': float, 'doc': 'The timestamp of the first sample', 'default': None},
            {'name': 'rate', 'type': float, 'doc': 'Sampling rate in Hz', 'default': None},

            {'name': 'comments', 'type': str, 'doc': 'Human-readable comments about this TimeSeries dataset', 'default':None},
            {'name': 'description', 'type': str, 'doc': 'Description of this TimeSeries dataset', 'default':None},
            {'name': 'control', 'type': Iterable, 'doc': 'Numerical labels that apply to each element in data', 'default': None},
            {'name': 'control_description', 'type': Iterable, 'doc': 'Description of each control value', 'default': None},
            {'name': 'parent', 'type': 'NWBContainer', 'doc': 'The parent NWBContainer for this NWBContainer', 'default': None},
    )
    def __init__(self, **kwargs):
        name, source, data = popargs('name', 'source', 'data', kwargs)
        super(AbstractFeatureSeries, self).__init__(name, source, data, "see 'feature_units'", **kwargs)
        self.features = getargs('features', kwargs)
        self.feature_units = getargs('feature_units', kwargs)

    @docval({'name': 'time', 'type': float, 'doc': 'the time point of this feature'},
            {'name': 'features', 'type': (list, np.ndarray), 'doc': 'the feature values for this time point'})
    def add_features(self, **kwargs):
        time, features = getargs('time', 'features', kwargs)
        self.timestamps.append(time)
        self.data.append(features)

class IntervalSeries(TimeSeries):
    """
    Stores intervals of data. The timestamps field stores the beginning and end of intervals. The
    data field stores whether the interval just started (>0 value) or ended (<0 value). Different interval
    types can be represented in the same series by using multiple key values (eg, 1 for feature A, 2
    for feature B, 3 for feature C, etc). The field data stores an 8-bit integer. This is largely an alias
    of a standard TimeSeries but that is identifiable as representing time intervals in a machinereadable
    way.
    """
    __nwbfields__ = ()

    _ancestry = "TimeSeries,IntervalSeries"
    _help = "Stores the start and stop times for events."

    @docval({'name': 'name', 'type': str, 'doc': 'The name of this TimeSeries dataset'},
            {'name': 'source', 'type': str, 'doc': ('Name of TimeSeries or Modules that serve as the source for the data '
                                                   'contained here. It can also be the name of a device, for stimulus or '
                                                   'acquisition data')},
            {'name': 'comments', 'type': str, 'doc': 'Human-readable comments about this TimeSeries dataset', 'default':None},
            {'name': 'description', 'type': str, 'doc': 'Description of this TimeSeries dataset', 'default':None},
            {'name': 'control', 'type': Iterable, 'doc': 'Numerical labels that apply to each element in data', 'default': None},
            {'name': 'control_description', 'type': Iterable, 'doc': 'Description of each control value', 'default': None},
            {'name': 'parent', 'type': 'NWBContainer', 'doc': 'The parent NWBContainer for this NWBContainer', 'default': None},
    )
    def __init__(self, **kwargs):
        name, source = popargs('name', 'source', kwargs)
        self.__interval_data = list()
        self.__interval_timestamps = list()
        super(IntervalSeries, self).__init__(name, source, self.__interval_data, "n/a",
                                             timestamps=self.__interval_timestamps,
                                             conversion='nan',
                                             resolution='nan',
                                             **kwargs)

    @docval({'name': 'start', 'type': float, 'doc': 'The name of this TimeSeries dataset'},
            {'name': 'stop', 'type': float, 'doc': 'The name of this TimeSeries dataset'}
    )
    def add_interval(self, **kwargs):
        start, stop = getargs('start', 'stop', kwargs)
        self.__interval_timestamps.append(start)
        self.__interval_timestamps.append(stop)
        self.__interval_data.append(1)
        self.__interval_data.append(-1)

class UnitTimes(Interface):
    """
    Event times of observed units (e.g. cell, synapse, etc.). The UnitTimes group contains a group
    for each unit. The name of the group should match the value in the source module, if that is
    possible/relevant (e.g., name of ROIs from Segmentation module).
    """

    __nwbfields__ = ('unit_source',
                     'unit_times',
                     'unit_description')

    _help = "Estimated spike times from a single unit"

    @docval({'name': 'source', 'type': str, 'doc': 'the source of the data represented in this Module Interface'},
            {'name': 'unit_times', 'type': Iterable, 'doc': 'Spike time for the units (exact or estimated)'},
            {'name': 'unit_description', 'type': str, 'doc': 'Description of the unit (eg, cell type).'},
            {'name': 'unit_source', 'type': str, 'doc': 'Name, path or description of where unit times originated. This is necessary only if the info here differs from or is more fine-grained than the interfaces source field.', 'default': None})
    def __init__(self, **kwargs):
        source, unit_times, unit_description, unit_source = popargs('source', 'unit_times', 'unit_description', 'unit_source', kwargs)
        super(UnitTimes, self).__init__(source, **kwargs)
        self.unit_times = unit_times
        self.unit_description = unit_description
        self.unit_source = unit_source

