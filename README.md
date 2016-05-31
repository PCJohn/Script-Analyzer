# Script-Analyzer
Python modules to analyze movie scripts

ScriptAnalyzer contains tools for analyzing character interactions in movie scripts. It contains methods for finding the centrality of characters and extracting the important characters using the mean centrality as cutoff. Along with this, the scene_extraction module scores scenes. A scene score is the mean TFIDF score of all the keywords in the scene.

A demo of the character graph centrality can be found here: http://prithvijc.pythonanywhere.com/movie_graph

Requirements:


    (1) Python 2.7
    (2) matplotlib
    (3) networkx
    (4) numpy

Format of the script:

All scripts have been scraped from www.imsdb.com/all%20scripts/ and have the following format:

    DESCRIPTION
        ... (description of the scene/character action)
        ...
    CHAR_1_NAME
        "we have to go there..."
        ... (dialogue)
    CHAR_2_NAME
        "yeah..."
        ...
        .
        .
    DESCRIPTION
        .
        .
        .

scripts_clean.tar.gz contains 961 such scripts. These scripts were then cleaned to retain only ASCII text. New scripts must follow this as the module parses character names and scenes assuming this format.

The scenes extracted by the module are actually basically lines of the script between two DESCRIPTION lines. These are more like frames that contain sprints of interaction between sets of characters. Consecutive frames that have the same characters involved are merge together to form a scene. It is worth noting that this may not the true length of the scene as the same scene may have multiple frames involving distinct sets of characters. However, this division of the scripts into scenes will serve our purpose as the module is mainly looking at character centrality.

Usage:
(1) Extract scripts_clean.tar.gz to scripts_clean in the Script-Analyzer directory. This should extract all preprocessed the movie scripts.
(2) Run python example.py to see the demo of the character and important scene extraction on the movie "All the President's Men".

The methods to be used can be found in example.py. Details of usage are written in individual modules.
script_reader.py handles character interaction and centrality measures while scene_extractor handles finding the most important (actually, the most unique) scenes in the script.
