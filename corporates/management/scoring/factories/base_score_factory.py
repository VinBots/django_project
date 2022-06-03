from importlib import import_module
from inspect import getmembers, isabstract, isclass
from corporates.management.scoring.base_scores.abs_base_score import AbsBaseScore


class BaseScoreFactory(object):
    def create_instance(self, score_name):
        module_folder = "corporates.management.scoring.base_scores"

        try:
            score_module = import_module("." + score_name.lower(), module_folder)
        except ImportError:
            score_module = import_module(".null_score", module_folder)

        classes = getmembers(score_module, lambda m: isclass(m) and not isabstract(m))

        for _, _class in classes:
            if issubclass(_class, AbsBaseScore):
                return _class(score_name)
