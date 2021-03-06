from abc import ABCMeta, abstractmethod
from ..build import BuildManager
from ..build import GroupBuilder
from ..utils import docval, popargs, getargs
from ..container import Container

class FORMIO(object, metaclass=ABCMeta):
    @docval({'name': 'manager', 'type': BuildManager, 'doc': 'the BuildManager to use for I/O'},
            {"name": "source", "type": str, "doc": "the source of container being built i.e. file path", 'default': None})
    def __init__(self, **kwargs):
        self.__manager = getargs('manager', kwargs)
        self.__built = dict()
        self.__source = getargs('source', kwargs)

    @docval(returns='the Container object that was read in', rtype=Container)
    def read(self, **kwargs):
        f_builder = self.read_builder()
        container = self.__manager.construct(f_builder)
        return container

    @docval({'name': 'container', 'type': Container, 'doc': 'the Container object to write'})
    def write(self, **kwargs):
        container = getargs('container', kwargs)
        f_builder = self.__manager.build(container, source=self.__source)
        self.write_builder(f_builder)

    @abstractmethod
    @docval(returns='a GroupBuilder representing the read data', rtype='GroupBuilder')
    def read_builder(self):
        ''' Read data and return the GroupBuilder represention '''
        pass

    @abstractmethod
    @docval({'name': 'builder', 'type': GroupBuilder, 'doc': 'the GroupBuilder object representing the Container'})
    def write_builder(self, **kwargs):
        ''' Write a GroupBuilder representing an Container object '''
        pass

