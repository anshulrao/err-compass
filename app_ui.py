from IPython.display import display, HTML
import ipywidgets as widgets
import pandas as pd

from utils import *
from similarity_calculator import SentenceSimilarityCalculator

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

class AppUI(object):
    def __init__(self):
        """
        Constructor.
        
        """
        print("Rendering the UI...")
        self._create_ui()
        self.model = None
        self.similarity_calculator = SentenceSimilarityCalculator(refresh_word2vec=True)

    def _rank_sentences(self, target_sentence, model):
        """
        Rank the sentences in descending order based on their 
        similarity to target sentence.
        
        """
        df = pd.read_csv("mappings.csv")
        similarities = []
        
        # compute similarity between each sentence and target sentence.
        for _, row in df.iterrows():
            similarity = self.similarity_calculator.compute_similarity(target_sentence, row['phrase'], model)
            similarities.append((row['phrase'], row['resolution'], similarity))
        
        # order the sentences in descending order of similarity and then return them
        ranked_sentences = sorted(similarities, key=lambda x: x[2], reverse=True)
        return ranked_sentences
    
    def _create_insert_ui(self):
        """
        Create INSERT ERROR & RESOLUTION panel.
        
        """
        # create error text input box
        error_input = widgets.Text(
            value='',
            placeholder='Enter error/failure message...',
            description='',
            disabled=False,
            layout=widgets.Layout(flex='1')
        )
        
        # create resolution text input box
        resolution_input = widgets.Text(
            value='',
            placeholder='Enter resolution...',
            description='',
            disabled=False,
            layout=widgets.Layout(flex='1')
        )
        
        # create the submit button
        submit_btn = widgets.Button(description="Submit", layout=widgets.Layout(flex='1'))
        submit_output = widgets.Output()
        
        def on_submit_btn_click(b):
            """
            Add values to mappings.csv when button is clicked.
            
            """
            with submit_output:
                submit_output.clear_output(wait=True)
                df = pd.read_csv("mappings.csv")
                df.loc[len(df.index)] = [error_input.value, resolution_input.value]
                df.drop_duplicates().to_csv("mappings.csv", index=False)
                colored_text = f"<span style='color: green;'>Row inserted!</span>"
                display(HTML(colored_text))        
        
        submit_btn.on_click(on_submit_btn_click)
        
        # arrange everything together
        vbox = widgets.VBox([
            widgets.HTML('<h2 style="text-align:center;">INSERT ERROR & RESOLUTION</h2>'),
            widgets.HBox([error_input, resolution_input]),
            widgets.HBox([submit_btn]),
            submit_output
        ], layout=widgets.Layout(margin='0px'))
        
        display(vbox)
        
    def _create_search_ui(self):
        """
        Create SEARCH ERROR panel.
        
        """
        # create error text input box
        sentence_input = widgets.Text(
            value='',
            placeholder='Enter error/failure message...',
            description='',
            disabled=False,
            layout=widgets.Layout(flex='1')
        )
        
        # create the submit button
        submit_btn = widgets.Button(description="Submit", layout=widgets.Layout(flex='1'))

        # create model dropdown
        model_dropdown = widgets.Dropdown(
            options=['BoW', 'Word2Vec', 'GloVe'],
            value="BoW",
            description="Model:",
            disabled=False
        )

        submit_output = widgets.Output()
        
        def on_submit_btn_click(b):
            """
            Display top 5 ranked resolutions for the given error message.
            
            """
            with submit_output:
                submit_output.clear_output(wait=True)
                target_sentence = sentence_input.value
                similarities = self._rank_sentences(target_sentence, model_dropdown.value)
                df = pd.DataFrame(similarities, columns=['Error', 'Resolution', 'Accuracy']).head()
                display(HTML(style_table(df)))
                
        submit_btn.on_click(on_submit_btn_click)
        
        # arrange everything together
        vbox = widgets.VBox([
            widgets.HTML('<h2 style="text-align:center;">SEARCH ERROR</h2>'),
            widgets.HBox([sentence_input, model_dropdown]),
            widgets.HBox([submit_btn]),
            submit_output
        ], layout=widgets.Layout(margin='0px'))

        display(vbox)

    def _create_filter_ui(self):
        """
        Create FILTER LOG FILE panel.

        """
        # create error text input box
        fn_input = widgets.Text(
            value='',
            placeholder='Enter log filename...',
            description='',
            disabled=False,
            layout=widgets.Layout(flex='1')
        )

        # create the submit button
        submit_btn = widgets.Button(description="Submit", layout=widgets.Layout(flex='1'))

        # create model dropdown
        model_dropdown = widgets.Dropdown(
            options=['BoW', 'Word2Vec', 'GloVe'],
            value="BoW",
            description="Model:",
            disabled=False
        )

        submit_output = widgets.Output()

        def on_submit_btn_click(b):
            """
            Read log file to filter out error/failure messages and then
            search for them in stored mappings file.

            """
            with submit_output:
                submit_output.clear_output(wait=True)
                error_msgs = read_error_messages_from_log_file(fn_input.value)
                for error_msg in error_msgs:
                    similarities = self._rank_sentences(error_msg, model_dropdown.value)
                    df = pd.DataFrame(similarities, columns=['Error', 'Resolution', 'Accuracy']).head()
                    display(HTML(f'<font color="darkred">{error_msg}</font>'))
                    display(HTML(style_table(df)))

        submit_btn.on_click(on_submit_btn_click)

        # arrange everything together
        vbox = widgets.VBox([
            widgets.HTML('<h2 style="text-align:center;">FILTER LOG FILE</h2>'),
            widgets.HBox([fn_input, model_dropdown]),
            widgets.HBox([submit_btn]),
            submit_output
        ], layout=widgets.Layout(margin='0px'))

        display(vbox)

    def _create_ui(self):
        """
        Create the UI.
        
        """
        self._create_insert_ui()
        self._create_search_ui()
        self._create_filter_ui()
