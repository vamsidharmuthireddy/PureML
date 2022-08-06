from random import sample
import gradio as gr
# def start(name):
#     return "Hello " + name + " ! "

# face = gr.Interface(fn=start, inputs="text", outputs="text")
# face.launch()


# class sample_class():

#     def __init__(self):
#         self.app = None

#     def start(self, name):
#         return "Hello " + name + " ! "
        
# face = gr.Interface(fn=sample_class().start, inputs="text", outputs="text")
# face.launch()



# class sample_class():

#     def __init__(self):
#         self.app = None

#     def start(self, name):
#         return "Hello " + name + " ! "
        
#     def build_app(self):
#         face = gr.Interface(fn=sample_class().start, inputs="text", outputs="text")
#         face.launch()

# sample_class().build_app()



# class sample_class():

#     def __init__(self):
#         self.app = None

#     def start(self, name):
#         return "Hello " + name + " ! "
        
#     def build_app(self):
#         self.app = gr.Interface(fn=sample_class().start, inputs="text", outputs="text")
#         self.app.launch()

# sample_class().build_app()

class sample_class():

    def __init__(self):
        self.app = None

    def start(self, name):
        return "Hello " + name + " ! "
        
    def build_app(self):
        self.app = gr.Interface(fn=self.start, inputs="text", outputs="text")
        # face.launch()

s = sample_class()
s.build_app()

s.app.launch()
