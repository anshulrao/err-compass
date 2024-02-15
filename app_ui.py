from IPython.display import display, HTML
from sklearn.metrics.pairwise import cosine_similarity
import ipywidgets as widgets
import pandas as pd
import numpy as np
import re

from utils import style_table

class AppUI(object):
    def __init__(self):
        """
        Constructor.
        
        """
        print("Rendering the UI...")
        self._create_ui()
        
        
    def _compute_similarity(self, sentence1, sentence2):
        """
        Compute cosine similarity of two sentences.
        
        """
        # remove punctuations
        sentence1 = re.sub(r'[^\w\s]', '', sentence1)
        sentence2 = re.sub(r'[^\w\s]', '', sentence2)
        
        # tokenize
        words1 = sentence1.lower().split()
        words2 = sentence2.lower().split()
        
        # create a set of unique words
        unique_words = set(words1 + words2)
        
        # create vectors for each sentence
        vector1 = [words1.count(word) for word in unique_words]
        vector2 = [words2.count(word) for word in unique_words]
        
        # compute cosine similarity
        similarity = cosine_similarity([vector1], [vector2])[0][0]
        return similarity
    
    def _rank_sentences(self, target_sentence):
        """
        Rank the sentences in descending order based on their 
        similarity to target sentence.
        
        """
        df = pd.read_csv("mappings.csv")
        similarities = []
        
        # compute similarity between each sentence and target sentence.
        for _, row in df.iterrows():
            similarity = self._compute_similarity(target_sentence, row['phrase'])
            similarities.append((row['phrase'], row['resolution'], similarity))
        
        # order the sentences in descending order of similarity and then return them
        ranked_sentences = sorted(similarities, key=lambda x: x[2], reverse=True)
        return ranked_sentences
    
    def _create_insert_ui(self):
        """
        Create INSERT panel.
        
        """
        # create phrase text input box
        phrase_input = widgets.Text(
            value='',
            placeholder='Enter phrase...',
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
                df.loc[len(df.index)] = [phrase_input.value, resolution_input.value]
                df.drop_duplicates().to_csv("mappings.csv", index=False)
                colored_text = f"<span style='color: green;'>Row inserted!</span>"
                display(HTML(colored_text))        
        
        submit_btn.on_click(on_submit_btn_click)
        
        # arrange everything together
        vbox = widgets.VBox([
            widgets.HTML('<h2 style="text-align:center;">INSERT</h2>'),
            widgets.HBox([phrase_input, resolution_input]),
            widgets.HBox([submit_btn]),
            submit_output
        ], layout=widgets.Layout(margin='0px'))
        
        display(vbox)
        
    def _create_search_ui(self):
        """
        Create SEARCH panel.
        
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
        submit_output = widgets.Output()
        
        def on_submit_btn_click(b):
            """
            Display top 5 ranked resolutions for the given error message.
            
            """
            with submit_output:
                submit_output.clear_output(wait=True)
                target_sentence = sentence_input.value
                similarities = self._rank_sentences(target_sentence)
                df = pd.DataFrame(similarities, columns=['Error', 'Resolution', 'Accuracy']).head()
                display(HTML(style_table(df)))
                
        submit_btn.on_click(on_submit_btn_click)
        
        # arrange everything together
        vbox = widgets.VBox([
            widgets.HTML('<h2 style="text-align:center;">SEARCH</h2>'),
            widgets.HBox([sentence_input]),
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
