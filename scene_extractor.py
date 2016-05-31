'''
Module to extract unique scenes from the script. Uses the values of the mean TFIDF scores of words in a scene to evaluate its uniqueness and importance in the movie.

Usage:
    
    import scene_extractor as se
    scene_finder = se.Scene_Extractor()
    scene_finder.main_scenes(script,10)

This should print out the contents of the top 10 scenes with high scores in this format:
    ...
    <scene contents>
    ...
    ___________________
    ...
    <list of characters in the scene>
    ...
    ______<scene score>____


Author: Prithvijit Chakrabarty (prithvichakar@gmail.com)
'''

from __future__ import division
import nltk
from nltk import sent_tokenize,pos_tag,word_tokenize
import os
import numpy as np
from tfidf import TFIDF_Model,Tokenizer
from nltk.corpus import stopwords
import script_manager as sm

class Scene_Extractor():

    #Initialize the TFIDF model
    def __init__(self,tfidf_model_path='./tfidf_model1.pkl'):
        self.tf = TFIDF_Model(tfidf_model_path)

    #Returns a list of 3-tuples: (scene text, list of chars in scene,score)
    def get_char_scene(self,script,char_list,keys):
        scenes = []
        N = len(script)
        in_dialogue = False
        has_desc_tag = False
        i = 0
        scene_text = []
        scene_char = set
        while (i < N):
            line = script[i].strip()
            if line == sm.DESC_TAG:
                if in_dialogue:
                    #Find characters in the scene description
                    score = 0
                    key_count = 0
                    for line in scene_text:
                        line = line.strip()
                        for w in word_tokenize(line):
                            if w in keys:
                                score = score+keys[w]
                                key_count = key_count+1
                            w = w.lower()
                            if w in char_list:
                                scene_char = scene_char.union(set([w]))
                    if key_count > 0:
                        score = score/key_count
                    scenes.append((scene_text,list(scene_char),score))
                    #Clear text, char list buffers
                    scene_text = []
                    scene_char.clear()
                    in_dialogue = False
                    scene_text.append(line)
            elif line.isupper():
                scene_char = scene_char.union(set([line.strip().lower()]))
                in_dialogue = True
                scene_text.append(line)
            else:
                scene_text.append(line)
            i = i+1
        self.merge_scenes(scenes)
        return scenes

    #Refine the snippets -- combine consecutive snippets if they have the same characters
    def merge_scenes(self,scenes):
        i = 0
        while i < len(scenes)-1:
            while len(set(scenes[i+1][1])-set(scenes[i][1])) == 0:
                scenes[i][0].extend(scenes[i+1][0][1:])
                scenes[i] = (scenes[i][0],scenes[i][1],(scenes[i][2]+scenes[i+1][2]) )
                del scenes[i+1]
                if i >= len(scenes)-1:
                    break
            i = i+1
    
    #Method to print out the main scenes of the script. Prints out N scenes with the highest mean TFIDF scores
    def main_scenes(self,script,N):
        char_list,keywords = self.tf.get_keywords(script)
        if len(char_list) == 0:
            return None
        scenes = self.get_char_scene(script,char_list,keywords)
        scenes.sort(reverse=True, key=lambda x:x[-1])
        scenes = scenes[:N]
       
        for scene,char,score in scenes:
            print '\n'.join(scene)
            print '________________________________'
            print char
            print '____________',score,'___________'

