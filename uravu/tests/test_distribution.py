"""
Tests for distribution module
"""

# Copyright (c) Andrew R. McCluskey
# Distributed under the terms of the MIT License
# author: Andrew R. McCluskey


import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from uravu.distribution import Distribution
from scipy.stats import norm, uniform

class TestDistribution(unittest.TestCase):
    """
    Testing the Distribution class.
    """
    def test_init_name(self):
        distro = Distribution(norm.rvs(loc=0, scale=1, size=1000), name='random')
        assert_equal(distro.name, 'random')

    def test_init_samples(self):
        samples = norm.rvs(loc=0, scale=1, size=1000)
        distro = Distribution(samples)
        assert_equal(distro.samples, samples)

    def test_init_random_state(self):
        distro = Distribution(norm.rvs(loc=0, scale=1, size=1000), name='random')
        assert isinstance(distro._random_state, np.random._generator.Generator)

    def test_normal(self):
        distro = Distribution(norm.rvs(loc=0, scale=1, size=100, random_state=np.random.RandomState(1)))
        assert_equal(distro.normal, True)

    def test_not_normal(self):
        distro = Distribution(uniform.rvs(loc=0, scale=1, size=100, random_state=np.random.RandomState(1)))
        assert_equal(distro.normal, False)

    def test_size(self):
        distro = Distribution(uniform.rvs(loc=0, scale=1, size=100))
        assert_equal(distro.size, 100)

    def test_pdf(self):
        distro = Distribution(uniform.rvs(loc=0, scale=1, size=100, random_state=np.random.RandomState(1)))
        assert_almost_equal(distro.pdf(0), [0.5805], decimal=4)

    def test_logpdf(self):
        distro = Distribution(uniform.rvs(loc=0, scale=1, size=100, random_state=np.random.RandomState(1)))
        assert_almost_equal(distro.logpdf(0), np.log([0.5805]), decimal=4)

    def test_negative_pdf(self):
        distro = Distribution(uniform.rvs(loc=0, scale=1, size=100, random_state=np.random.RandomState(1)))
        assert_almost_equal(distro.negative_pdf(0), [-0.5805], decimal=4)

    def test_dist_max(self):
        distro = Distribution(norm.rvs(loc=0, scale=1, size=100, random_state=np.random.RandomState(1)))
        assert_almost_equal(distro.dist_max, 0, decimal=1)

    def test_min(self):
        distro = Distribution(np.linspace(1, 10, 100))
        assert_equal(distro.min, 1)

    def test_max(self):
        distro = Distribution(np.linspace(1, 10, 100))
        assert_equal(distro.max, 10)

    def test_n(self):
        distro = Distribution(norm.rvs(loc=0, scale=1, size=100, random_state=np.random.RandomState(1)))
        assert_almost_equal(distro.n, 0, decimal=1)

    def test_s(self):
        distro = Distribution(norm.rvs(loc=0, scale=1, size=100, random_state=np.random.RandomState(2)))
        assert_almost_equal(distro.s, 1, decimal=1)

    def test_v(self):
        distro = Distribution(norm.rvs(loc=0, scale=2, size=100, random_state=np.random.RandomState(2)))
        assert_almost_equal(distro.v, 4, decimal=0)

    def test_s_uniform(self):
        distro = Distribution(uniform.rvs(loc=0, scale=1, size=100, random_state=np.random.RandomState(2)))
        assert_equal(distro.s, None)

    def test_v_uniform(self):
        distro = Distribution(uniform.rvs(loc=0, scale=2, size=100, random_state=np.random.RandomState(2)))
        assert_equal(distro.v, None)

    def test_con_int(self):
        distro = Distribution(norm.rvs(loc=0, scale=2, size=10000, random_state=np.random.RandomState(2)))
        assert_almost_equal(distro.con_int()[0], -2 * 1.96, decimal=1)
        assert_almost_equal(distro.con_int()[1], 2 * 1.96, decimal=1)

    def test_add_samples(self):
        samples = norm.rvs(loc=0, scale=2, size=100, random_state=np.random.RandomState(2))
        distro = Distribution(samples)
        distro.add_samples(samples)
        assert_equal(distro.size, 200)

    def test_repr(self):
        distro = Distribution(norm.rvs(loc=0, scale=1, size=100, random_state=np.random.RandomState(2)))
        assert_equal(distro.__repr__(), distro.samples.__repr__())

    def test_str(self):
        distro = Distribution(norm.rvs(loc=2, scale=0.0001, size=100, random_state=np.random.RandomState(2)))
        assert_equal(distro.__str__(), f'{distro.n:.3e} +/- {distro.s:.3e}')

    def test_dict_roundtrip(self):
        distro = Distribution(norm.rvs(loc=0, scale=1, size=1000), name='random')
        distro_new = Distribution.from_dict(distro.to_dict())
        assert_equal(distro.samples, distro_new.samples)
        assert distro.name == distro_new.name
