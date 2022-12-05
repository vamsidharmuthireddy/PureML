from pathlib import Path
from typing import Dict

from ..model_framework import ModelFramework, ModelFrameworkType
from ..packaging_utils import infer_requirements




class PytorchTabnet(ModelFramework):
    framework_name: str = 'pytorch_tabnet'
    additional_requirements: list = [
                                        'torch',
                                        'torchvision',
                                        'torchaudio',
                                        'numpy',
                                        'joblib'
                                    ]
    requirements: list = [framework_name]


    def typ(self) -> ModelFrameworkType:
        return ModelFrameworkType.PYTORCH


    def supports_model_class(self, model_class) -> bool:
        model_framework, _, _ = model_class.__module__.partition(".")
        return model_framework == ModelFrameworkType.PYTORCH_TABNET.value

    def get_requirements(self):

        default_requirements = [infer_requirements(framework_name=self.framework_name)]

        self.requirements = default_requirements + self.additional_requirements

        return self.requirements