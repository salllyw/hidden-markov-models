# Hidden Markov Models
 Hidden Markov Models or hmms can be used for Part of Speech Tagging. 
 
 Here's an implementation.
 
 The algorithm uses hmm to learn a training dataset with the following specifications:-
 
 *word/tag* - represents the part of speech tag assigned to every word.
 
 each *word/tag* is separated by a space and each sentence in the corpus, is on a new line.
 
Credits to the the datasets can be found in CREDITS.md

## Implemenation

The training model calculates transition and emission probabilities for a training dataset.

My model uses Add-1-Smoothing aka [Additive/Laplace Smoothing](https://en.wikipedia.org/wiki/Additive_smoothing) 

(I have tested some other parametric smoothing techniques, please see the inferences section)

After parsing through the entire training dataset, my model performs transition smoothing.

All transitions between tag1->tag2 that have not been observed, are smoothened using Add-1-Smoothing.

The test model evaluates which tag most suits a word in the raw dataset.

For words never encountered before, emission smoothing is done by assigning equal probability all unique tags.

ie. for *word->tag* such that the training hmm has never seen 'word' before, for all tag in unique_tags , probability of *word/tag* is equal (can be set to -log(l) if using log probabilities, or 1/l where l=count(unique_tags))

## Code

**hmmlearn.py**

Training model for the HMM. 

Writes the model parameters like transition probabilities, emission probabilites and a list of unique words into an intermediate model file called hmmmodel.json (or hmmmodel_xx.json for language xx)

``` python3 hmmlearn.py /path/to/train/data```

**hmmdecode.py**

Testing of HMM. 

Tests raw (test) data using parameters from hmmmodel.json and traces the best tags using Viterbi Algorithm

``` python3 hmmdecode.py /path/to/test/data```

**hmmcompare.py**

Evaluates the accuracy of HMM against tagged (test) data

``` python3 hmmcompare.py```

## Results

This model was tested on three languages (trained on the train_dev dataset) and their accuracies observed are:-

English (en)  0.887830729996

Chinese (zh)  0.869547119547

Hindi (hi)    0.924188540785
           

The baseline accuracies and reference accuracies were:-
                  Baseline                  Reference
English:    0.842365317182              0.887910423972
Chinese:    0.838827838828              0.869547119547
Hindi:      0.85817104149               0.924188540785

Here the baseline model assigns the most common tags to words, and the reference model uses the viterbi algorithm and smoothing techniques to make more accurate part of speech tagging of sentences.

From the comparison, we can see that my model is at par with the reference model, and only falls short in English by 0.000079693976

## Inferences

The following enlist some observations and my inferences from implementing the Viterbi Algorithm and HMMs

Total number of words in development data tested using a model trained on the training dataset:-

en : 25148

zh : 12663

Reference correct tags count:- 

(Number of correctly tagged words according to reference accuracies for a model trained on the training dataset for the two languages)

en: 22135

zh: 10928


Number of correctly tagged words (development dataset) are:- 
----
     Parameter 1     |     Parameter 2     | English | Chinese. 
    :-----------:    |   :-------------:   |  :----: |  :----:  
0.70|3.0|22114|10940
0.80|3.0|22113|10938
0.30|3.0|22116|10941
0.50|3.0|22114|10941
0.55|3.0|22114|10940
|0.65|3.0|22116|10941|
|0.70|3.5|22116|10941|
|0.60|3.5|22116|10941|
|0.60|4.0|22117|10940|
|**1.00|1.0|22138|10928**|
|0.70|2.0|22114|10923|
|0.70|2.5|22112|10928|
|0.60|5.0|22118|10938|
|0.70|5.0|22120|10938|
|0.70|5.5|22116|10938|
|0.80|5.0|22119|10936|
|0.80|6.0|22109|10937|
|0.90|6.0|22109|10936|
|1.00|6.0|22109|10936|


**I see that on increasing Parameter2, number of correct tags for Chinese increases**

**Where as on increasing Parameter1, number of correct tags for English increases**

Laplace Smoothing is a standard smoothing technique. 

**By comparing my results for laplace smoothing(bold) to other paramter options, I observe that it produces results closest to reference results for English and Chinese.**
