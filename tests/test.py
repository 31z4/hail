from hail import Storm, _ReadonlyDict, _ReadonlyList
from unittest import TestCase


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._storm = Storm()

    def test_cluster(self):
        cluster = self._storm.cluster
        self.assertIsInstance(cluster, _ReadonlyDict)
        self.assertGreater(len(cluster), 0)

        cluster_configuration = cluster.configuration
        self.assertIsInstance(cluster_configuration, _ReadonlyDict)
        self.assertGreater(len(cluster_configuration), 0)

    def test_supervisors(self):
        supervisors = self._storm.supervisors
        self.assertIsInstance(supervisors, _ReadonlyDict)
        self.assertGreater(len(supervisors), 0)

        supervisor = supervisors.items()[0][1]
        self.assertIsInstance(supervisor, _ReadonlyDict)
        self.assertGreater(len(supervisor), 0)

    def test_nimbuses(self):
        nimbuses = self._storm.nimbuses
        self.assertIsInstance(nimbuses, _ReadonlyList)
        self.assertGreater(len(nimbuses), 0)

        nimbus = self._storm.nimbuses[0]
        self.assertIsInstance(nimbus, _ReadonlyDict)
        self.assertGreater(len(nimbus), 0)

    def test_history(self):
        history = self._storm.history
        self.assertIsInstance(history, _ReadonlyList)
        self.assertEqual(len(history), 0)

    def test_topologies(self):
        topologies = self._storm.topologies
        self.assertIsInstance(topologies, _ReadonlyDict)
        self.assertEqual(len(topologies), 0)


