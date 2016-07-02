import unittest

from hail import Storm, _ReadonlyDict, _ReadonlyList
from os import getenv
from waiting import wait


class Test(unittest.TestCase):
    @staticmethod
    def wait(predicate):
        return wait(
            predicate,
            timeout_seconds=180, expected_exceptions=Exception
        )

    @classmethod
    def setUpClass(cls):
        cls.storm = Storm(
            getenv('STORM_UI_HOST', 'localhost'),
            int(getenv('STORM_UI_PORT', '8080'))
        )

    def test_cluster(self):
        self.wait(lambda: self.storm.cluster is not None)

        cluster = self.storm.cluster
        self.assertIsInstance(cluster, _ReadonlyDict)
        self.assertGreater(len(cluster), 0)

        cluster_configuration = cluster.configuration
        self.assertIsInstance(cluster_configuration, _ReadonlyDict)
        self.assertGreater(len(cluster_configuration), 0)

    def test_supervisors(self):
        self.wait(lambda: self.storm.supervisors)

        supervisors = self.storm.supervisors
        self.assertIsInstance(supervisors, _ReadonlyDict)
        self.assertGreater(len(supervisors), 0)

        supervisor = supervisors.items()[0][1]
        self.assertIsInstance(supervisor, _ReadonlyDict)
        self.assertGreater(len(supervisor), 0)

    def test_nimbuses(self):
        self.wait(lambda: self.storm.nimbuses)

        nimbuses = self.storm.nimbuses
        self.assertIsInstance(nimbuses, _ReadonlyList)
        self.assertGreater(len(nimbuses), 0)

        nimbus = self.storm.nimbuses[0]
        self.assertIsInstance(nimbus, _ReadonlyDict)
        self.assertGreater(len(nimbus), 0)

    def test_history(self):
        self.wait(lambda: self.storm.history is not None)

        history = self.storm.history
        self.assertIsInstance(history, _ReadonlyList)
        self.assertEqual(len(history), 0)

    def test_topologies(self):
        self.wait(lambda: self.storm.topologies is not None)

        topologies = self.storm.topologies
        self.assertIsInstance(topologies, _ReadonlyDict)
        self.assertEqual(len(topologies), 0)


if __name__ == '__main__':
    unittest.main()

