# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import tqdm

from .base import BaseOptimizer


class RandomSearchOptimizer(BaseOptimizer):
    def __init__(
        self,
        search_config,
        n_iter,
        metric="accuracy",
        n_jobs=1,
        cv=5,
        verbosity=1,
        random_state=None,
        warm_start=False,
        memory=True,
        hyperband_init=False,
    ):
        super().__init__(
            search_config,
            n_iter,
            metric,
            n_jobs,
            cv,
            verbosity,
            random_state,
            warm_start,
            memory,
            hyperband_init,
        )

    def _move(self, cand):
        cand.pos = cand._space_.get_random_position()

    def search(self, nth_process, X, y):
        _cand_ = self._init_search(nth_process, X, y)

        _cand_.eval(X, y)

        _cand_.score_best = _cand_.score
        _cand_.pos_best = _cand_.pos

        for i in tqdm.tqdm(**self._tqdm_dict(_cand_)):

            self._move(_cand_)
            _cand_.eval(X, y)

            if _cand_.score > _cand_.score_best:
                _cand_.score_best = _cand_.score
                _cand_.pos_best = _cand_.pos

        return _cand_
