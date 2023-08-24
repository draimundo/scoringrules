import jax
import numpy as np
import pytest
from scoringrules._energy import energy_score
from scoringrules._wenergy import owenergy_score, twenergy_score, vrenergy_score

ENSEMBLE_SIZE = 51
N = 100
N_VARS = 3

BACKENDS = ["numpy", "numba", "jax"]


@pytest.mark.parametrize("backend", BACKENDS)
def test_owes_vs_es(backend):
    obs = np.random.randn(N, N_VARS)
    fcts = np.expand_dims(obs, axis=-2) + np.random.randn(N, ENSEMBLE_SIZE, N_VARS)

    res = energy_score(fcts, obs, backend=backend)
    resw = owenergy_score(fcts, obs, backend=backend)
    np.testing.assert_allclose(res, resw, rtol=1e-10)


@pytest.mark.parametrize("backend", BACKENDS)
def test_twes_vs_es(backend):
    obs = np.random.randn(N, N_VARS)
    fcts = np.expand_dims(obs, axis=-2) + np.random.randn(N, ENSEMBLE_SIZE, N_VARS)

    res = energy_score(fcts, obs, backend=backend)
    resw = twenergy_score(fcts, obs, backend=backend)
    np.testing.assert_allclose(res, resw, rtol=1e-10)


@pytest.mark.parametrize("backend", BACKENDS)
def test_vres_vs_es(backend):
    obs = np.random.randn(N, N_VARS)
    fcts = np.expand_dims(obs, axis=-2) + np.random.randn(N, ENSEMBLE_SIZE, N_VARS)

    res = energy_score(fcts, obs, backend=backend)
    resw = vrenergy_score(fcts, obs, backend=backend)
    np.testing.assert_allclose(res, resw, rtol=1e-10)


@pytest.mark.parametrize("backend", BACKENDS)
def test_owenergy_score_correctness(backend):
    fcts = np.array(
        [[0.79546742, 0.4777960, 0.2164079], [0.02461368, 0.7584595, 0.3181810]]
    ).T
    obs = np.array([0.2743836, 0.8146400])

    def w_func(x, t):
        return (x > t).all().astype(np.float32)

    t = 0.2
    res = owenergy_score(fcts, obs, w_func, (t,), backend=backend)
    np.testing.assert_allclose(res, 0.2274243, rtol=1e-6)

    def w_func(x, t):
        return (x < t).all().astype(np.float32)

    t = 1
    res = owenergy_score(fcts, obs, w_func, (t,), backend=backend)
    np.testing.assert_allclose(res, 0.3345418, rtol=1e-6)


@pytest.mark.parametrize("backend", BACKENDS)
def test_twenergy_score_correctness(backend):
    fcts = np.array(
        [[0.79546742, 0.4777960, 0.2164079], [0.02461368, 0.7584595, 0.3181810]]
    ).T
    obs = np.array([0.2743836, 0.8146400])

    def v_func(x, t):
        return np.maximum(x, t)

    t = 0.2
    res = twenergy_score(fcts, obs, v_func, (t,), backend=backend)
    np.testing.assert_allclose(res, 0.3116075, rtol=1e-6)

    def v_func(x, t):
        return np.minimum(x, t)

    t = 1
    res = twenergy_score(fcts, obs, v_func, (t,), backend=backend)
    np.testing.assert_allclose(res, 0.3345418, rtol=1e-6)
