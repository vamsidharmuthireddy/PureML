from pathlib import Path
from typing import Dict

from ..model_framework import ModelFramework, ModelFrameworkType
from ..packaging_utils import infer_requirements

class Tensorflow(ModelFramework):
    framework_name: str = 'tensorflow'
    additional_requirements: list = [
                                        "numpy",
                                        "scipy",
                                        "joblib"
                                    ]
    requirements: list = [framework_name]



    def typ(self) -> ModelFrameworkType:
        return ModelFrameworkType.TENSORFLOW

    def supports_model_class(self, model_class) -> bool:
        model_framework, _, _ = model_class.__module__.partition(".")
        return model_framework == ModelFrameworkType.TENSORFLOW.value


    def get_requirements(self):

        default_requirements = [infer_requirements(framework_name=self.framework_name)]

        self.requirements = default_requirements + self.additional_requirements

        return self.requirements
