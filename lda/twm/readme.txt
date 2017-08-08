The source code(in resources folder)is from http://gibbslda.sourceforge.net/
Thanks 	Xuan-Hieu Phan and Cam-Tu Nguyen.


How to compile?
Untar and unzip the source code
$ gunzip GibbsLDA++.tar.gz
$ tar -xf GibbsLDA++.tar
Compile
Go to the home directory of GibbsLDA++ (i.e. GibbsLDA++ directory), and type:
$ make clean
$ make all
##############################################################################################################
NOTICE: if you cannot compile the file correctly, you may need to add #include <stdlib.h> and #include <stdio.h>
##############################################################################################################


Parameter estimation from scratch
Command line:

$ lda -est [-alpha <double>] [-beta <double>] [-ntopics <int>] [-niters <int>] [-savestep <int>] [-twords <int>] -dfile <string>

in which (parameters in [] are optional):

    -est: Estimate the LDA model from scratch
    -alpha <double>: The value of alpha, hyper-parameter of LDA. The default value of alpha is 50 / K (K is the the number of topics). See [Griffiths04] for a detailed discussion of choosing alpha and beta values.
    -beta <double>: The value of beta, also the hyper-parameter of LDA. Its default value is 0.1
    -ntopics <int>: The number of topics. Its default value is 100. This depends on the input dataset. See [Griffiths04] and [Blei03] for a more careful discussion of selecting the number of topics.
    -niters <int>: The number of Gibbs sampling iterations. The default value is 2000.
    -savestep <int>: The step (counted by the number of Gibbs sampling iterations) at which the LDA model is saved to hard disk. The default value is 200.
    -twords <int>: The number of most likely words for each topic. The default value is zero. If you set this parameter a value larger than zero, e.g., 20, GibbsLDA++ will print out the list of top 20 most likely words per each topic each time it save the model to hard disk according to the parameter savestep above.
    -dfile <string>: The input training data file. See section "Input data format" for a description of input data format.

Parameter estimation from a previously estimated model

Command line:

$ lda -estc -dir <string> -model <string> [-niters <int>] [-savestep <int>] [-twords <int>]

in which (parameters in [] are optional):

    -estc: Continue to estimate the model from a previously estimated model.
    -dir <string>: The directory contain the previously estimated model
    -model <string>: The name of the previously estimated model. See section "Outputs" to know how GibbsLDA++ saves outputs on hard disk.
    -niters <int>: The number of Gibbs sampling iterations to continue estimating. The default value is 2000.
    -savestep <int>: The step (counted by the number of Gibbs sampling iterations) at which the LDA model is saved to hard disk. The default value is 200.
    -twords <int>: The number of most likely words for each topic. The default value is zero. If you set this parameter a value larger than zero, e.g., 20, GibbsLDA++ will print out the list of top 20 most likely words per each topic each time it save the model to hard disk according to the parameter savestep above.

Inference for previously unseen (new) data

Command line:

$ lda -inf -dir <string> -model <string> [-niters <int>] [-twords <int>] -dfile <string>

in which (parameters in [] are optional):

    -inf: Do inference for previously unseen (new) data using a previously estimated LDA model.
    -dir <string>: The directory contain the previously estimated model
    -model <string>: The name of the previously estimated model. See section "Outputs" to know how GibbsLDA++ saves outputs on hard disk.
    -niters <int>: The number of Gibbs sampling iterations for inference. The default value is 20.
    -twords <int>: The number of most likely words for each topic of the new data. The default value is zero. If you set this parameter a value larger than zero, e.g., 20, GibbsLDA++ will print out the list of top 20 most likely words per each topic after inference.
    -dfile <string>:The file containing new data. See section "Input data format" for a description of input data format.

Input data format

Both data for training/estimating the model and new data (i.e., previously unseen data) have the same format as follows:

[M]

[document1]

[document2]

...

[documentM]

in which the first line is the total number for documents [M]. Each line after that is one document. [documenti] is the ith document of the dataset that consists of a list of Ni words/terms.

[documenti] = [wordi1] [wordi2] ... [wordiNi]

in which all [wordij] (i=1..M, j=1..Ni) are text strings and they are separated by the blank character.

Note that the terms document and word here are abstract and should not only be understood as normal text documents. This is because LDA can be used to discover the underlying topic structures of any kind of discrete data. Therefore, GibbsLDA++ is not limited to text and natural language processing but can also be applied to other kinds of data like images and biological sequences. Also, keep in mind that for text/Web data collections, we should first preprocess the data (e.g., removing stop words and rare words, stemming, etc.) before estimating with GibbsLDA++.
Outputs

Outputs of Gibbs sampling estimation of GibbsLDA++ include the following files:

<model_name>.others

<model_name>.phi

<model_name>.theta

<model_name>.tassign

<model_name>.twords

in which:

<model_name>: is the name of a LDA model corresponding to the time step it was saved on the hard disk. For example, the name of the model was saved at the Gibbs sampling iteration 400th will be model-00400. Similarly, the model was saved at the 1200th iteration is model-01200. The model name of the last Gibbs sampling iteration is model-final.

<model_name>.others: This file contains some parameters of LDA model, such as:

alpha=?

beta=?

ntopics=? # i.e., number of topics

ndocs=? # i.e., number of documents

nwords=? # i.e., the vocabulary size

liter=? # i.e., the Gibbs sampling iteration at which the model was saved

<model_name>.phi: This file contains the word-topic distributions, i.e., p(wordw|topict). Each line is a topic, each column is a word in the vocabulary.

<model_name>.theta: This file contains the topic-document distributions, i.e., p(topict|documentm). Each line is a document and each column is a topic.

<model_name>.tassign: This file contains the topic assignments for words in training data. Each line is a document that consists of a list of <wordij>:<topic of wordij>

<model_file>.twords: This file contains twords most likely words of each topic. twords is specified in the command line.

GibbsLDA++ also saves a file called wordmap.txt that contains the maps between words and word's IDs (integer). This is because GibbsLDA++ works directly with integer IDs of words/terms inside instead of text strings.
Outputs of Gibbs sampling inference for previously unseen data

The outputs of GibbsLDA++ inference are almost the same as those of the estimation process except that the contents of those files are of the new data. The <model_name> is exactly the same as the filename of the input (new) data.
