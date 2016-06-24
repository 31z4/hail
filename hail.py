import httplib
import json

from collections import Mapping, Sequence
from urllib import urlencode

__all__ = ['Storm']


class _StormClient(object):
    _BASE_URL = '/api/v1'

    def __init__(self, host, port):
        self._host = host
        self._port = port

    def _request(self, url, method='GET'):
        connection = httplib.HTTPConnection(self._host, self._port, strict=True)
        connection.request(method, self._BASE_URL + url)
        response = connection.getresponse()

        assert response.status == httplib.OK

        return json.loads(response.read())


class _ReadonlyDict(Mapping):
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)


class _ReadonlyList(Sequence):
    def __init__(self, data):
        self._data = data

    def __getitem__(self, index):
        return self._data[index]

    def __contains__(self, item):
        return item in self._data

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)


class _StormResponseLoader(_StormClient):
    _PATH = ''

    def _load(self, data):
        return data

    def __init__(self, host, port, *args, **kwargs):
        super(_StormResponseLoader, self).__init__(host, port)

        url = self._PATH.format(*args)
        if kwargs:
            url += '?' + urlencode(kwargs)

        self._data = self._load(self._request(url))


class _ClusterConfiguration(_StormResponseLoader, _ReadonlyDict):
    _PATH = '/cluster/configuration'


class _ClusterSummary(_StormResponseLoader, _ReadonlyDict):
    _PATH = '/cluster/summary'


class _Supervisors(_StormResponseLoader, _ReadonlyDict):
    _PATH = '/supervisor/summary'

    def _load(self, data):
        return {
            item['id']: _ReadonlyDict(item)
            for item in data['supervisors']
        }


class _Nimbuses(_StormResponseLoader, _ReadonlyList):
    _PATH = '/nimbus/summary'

    def _load(self, data):
        return [
            _ReadonlyDict(item)
            for item in data['nimbuses']
            ]


class _History(_StormResponseLoader, _ReadonlyList):
    _PATH = '/history/summary'

    def _load(self, data):
        return [
            item
            for item in data['topo-history']
        ]


class _Topologies(_StormResponseLoader, _ReadonlyDict):
    _PATH = '/topology/summary'

    def _load(self, data):
        return {
            item['id']: _Topology(item, self._host, self._port)
            for item in data['topologies']
        }


class _TopologyWorkers(_StormResponseLoader, _ReadonlyList):
    _PATH = '/topology-workers/{0}'

    def _load(self, data):
        return [
            _ReadonlyDict(item)
            for item in data['hostPortList']
            ]


class _TopologyStats(_StormResponseLoader, _ReadonlyList):
    _PATH = '/topology/{0}'

    def _load(self, data):
        return [
            _ReadonlyDict(item)
            for item in data['topologyStats']
            ]


class _TopologyConfiguration(_StormResponseLoader, _ReadonlyList):
    _PATH = '/topology/{0}'

    def _load(self, data):
        return data['configuration']


class _TopologyBolts(_StormResponseLoader, _ReadonlyDict):
    _PATH = '/topology/{0}'

    def _load(self, data):
        return {
            item['boltId']: _Component(item, self._host, self._port, data['id'], item['boltId'])
            for item in data['bolts']
        }


class _TopologySpouts(_StormResponseLoader, _ReadonlyDict):
    _PATH = '/topology/{0}'

    def _load(self, data):
        return {
            item['spoutId']: _Component(item, self._host, self._port, data['id'], item['spoutId'])
            for item in data['spouts']
        }


class _ComponentDetails(_StormResponseLoader, _ReadonlyDict):
    _PATH = '/topology/{0}/component/{1}'


class _Cluster(_ClusterSummary):
    @property
    def configuration(self):
        return _ClusterConfiguration(self._host, self._port)


class _Topology(_StormClient, _ReadonlyDict):
    def __init__(self, data, host, port):
        super(_Topology, self).__init__(host, port)
        self._data = data

    @property
    def workers(self):
        return _TopologyWorkers(self._host, self._port, self._data['id'])

    @property
    def stats(self):
        return _TopologyStats(self._host, self._port, self._data['id'])

    @property
    def configuration(self):
        return _TopologyConfiguration(self._host, self._port, self._data['id'])

    @property
    def bolts(self):
        return _TopologyBolts(self._host, self._port, self._data['id'])

    @property
    def spouts(self):
        return _TopologySpouts(self._host, self._port, self._data['id'])


class _Component(_StormClient, _ReadonlyDict):
    def __init__(self, data, host, port, topology_id, component_id):
        super(_Component, self).__init__(host, port)
        self._data = data
        self._topology_id = topology_id
        self._component_id = component_id

    @property
    def details(self):
        return _ComponentDetails(self._host, self._port, self._topology_id, self._component_id)


class Storm:
    def __init__(self, host='localhost', port=8080):
        self._host = host
        self._port = port

    @property
    def cluster(self):
        return _Cluster(self._host, self._port)

    @property
    def supervisors(self):
        return _Supervisors(self._host, self._port)

    @property
    def nimbuses(self):
        return _Nimbuses(self._host, self._port)

    @property
    def history(self):
        return _History(self._host, self._port)

    @property
    def topologies(self):
        return _Topologies(self._host, self._port)
