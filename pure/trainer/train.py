from distutils.command.config import config
from pydantic import BaseModel, create_model
from sklearn.ensemble import RandomForestClassifier
import typing
import pandas as pd
import gradio as gr


class Trainer(BaseModel):
    label_header : typing.Any = None
    label_type: typing.Any = None
    label: typing.Any = None

    data_path: typing.Any = None
    data: typing.Any = None


    model: typing.Any = None

    app: typing.Any = None
    prediction_model : typing.Any = None


    def load_data(self):
        self.data = pd.read_parquet(self.data_path)

        print(self.data.columns)
        self.label = self.data.pop(self.label_header)

        print(self.data.shape, self.label.shape)

        


    def fit(self):
        self.model = RandomForestClassifier(verbose=1)
        self.model.fit(self.data, self.label)


    def predict(self, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15):
        row = [[a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15]]
        prediction = self.model.predict(row)
        prediction = prediction[0]
        print(prediction)
        return prediction


    def generate_prediction_model(self):
        class PredictionConfig:
            extra = 'forbid'
            arbitrary_types_allowed = True
            validate_assignment = True

        self.prediction_model  = create_model('PredictionModel', **self.data.iloc[1].to_dict(), __config__ = PredictionConfig)


    def create_gradio(self):
        # self.app = gr.Interface(fn=self.predict, inputs="text", outputs="text")
        self.generate_prediction_model()

        data_minmax = self.data.describe().loc[['min', 'max']]

        inputs = []
        for col_name in data_minmax.columns:
            min_value = int(data_minmax[col_name].loc['min'])
            max_value = int(data_minmax[col_name].loc['max'])
            value = int(self.data[col_name].iloc[1])
            label = col_name

            print(min_value, max_value, value, label)

            inputs.append(gr.Slider(minimum=min_value, maximum=max_value,
                             value=value, label=label, step=1))

        print(inputs)


        # def start(**kwargs):
        def start(model: self.prediction_model):
            print(model)
            return "Hello " + '' + " ! "


        # self.app = gr.Interface(fn=start, inputs=inputs, outputs="text")
        self.app = gr.Interface(fn=self.predict, inputs=inputs, outputs="text")
        




from pure.config.parser import Config

config = Config(config_path='/media/vamsidhar/HDD/aztlan/engageml/repos/Pure/sample_config/config_0.yaml')
config.load_config()

print(config.label_header, config.data_path)

trainer = Trainer(label_header=config.label_header, data_path=config.data_path)

trainer.load_data()

trainer.fit()

trainer.create_gradio()

trainer.app.launch()

# trainer.app.launch(share=True)