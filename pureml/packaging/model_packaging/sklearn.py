from pathlib import Path
import typing

from ..model_framework import ModelConfig, ModelFramework, ModelFrameworkType
from ..packaging_utils import infer_requirements



class SKLearn(ModelFramework):
    framework_name: str = 'scikit-learn'
    additional_requirements: list = [
                                        "numpy",
                                        "scipy",
                                        "joblib"
                                    ]
    requirements: list = [framework_name]



    def typ(self) -> ModelFrameworkType:
        return ModelFrameworkType.SKLEARN

    # def infer_requirements(self) -> typing.Dict[str, str]:
    #     pass
        # return infer_sklearn_packages()

    # def serialize_model_to_directory(self, model, target_directory: Path):
    #     import joblib

    #     model_filename = MODEL_FILENAME
    #     model_filepath = target_directory / model_filename
    #     joblib.dump(model, model_filepath, compress=True)

    # def model_metadata(self, model) -> Dict[str, str]:
    #     supports_predict_proba = model_supports_predict_proba(model)
    #     return {
    #         "model_binary_dir": "model",
    #         "supports_predict_proba": supports_predict_proba,
    #     }



    def supports_model_class(self, model_class) -> bool:
        model_framework, _, _ = model_class.__module__.partition(".")
        return model_framework == ModelFrameworkType.SKLEARN.value


    def get_requirements(self):

        default_requirements = [infer_requirements(framework_name=self.framework_name)]

        self.requirements = default_requirements + self.additional_requirements

        return self.requirements

    def load_model(self, model_config_path:str= None):

        model_config = ModelConfig().load_from_disk(model_path=self.model_path)

    def predict(self):
        pass