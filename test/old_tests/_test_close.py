# -*- coding: utf-8 -*-

import pytest
import sys
from .test_base_class import TestBaseClass

aerospike = pytest.importorskip("aerospike")
try:
    import aerospike
except:
    print("Please install aerospike python client.")
    sys.exit(1)


class TestClose(TestBaseClass):

    def setup_class(cls):
        TestBaseClass.get_hosts()

    def test_close_positive(self):
        """
            Invoke close() after positive connect
        """
        config = {'hosts': TestClose.hostlist}
        if TestClose.user is None and TestClose.password is None:
            self.client = aerospike.client(config).connect()
        else:
            self.client = aerospike.client(config).connect(TestClose.user,
                                                           TestClose.password)

        self.closeobject = self.client.close()
        assert self.closeobject is None

    def test_close_negative(self):
        """
            Invoke close() after negative connect
        """
        config = {'hosts': [('127.0.0.1', 2000)]}

        with pytest.raises(Exception):
            self.client = aerospike.client(config).connect()
        with pytest.raises(AttributeError) as attributeError:
            self.closeobject = self.client.close()
        assert "'TestClose' object has no attribute 'client'" in str(
            attributeError.value)

    def test_close_positive_without_connection(self):
        """
            Invoke close() without connection
        """
        config = {'hosts': [('127.0.0.1', 3000)]}
        self.client = aerospike.client(config)

        try:
            self.closeobject = self.client.close()

        except aerospike.exception.ClusterError as exception:
            assert exception.code == 11
            assert exception.msg == 'No connection to aerospike cluster'
