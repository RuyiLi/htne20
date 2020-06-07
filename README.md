# Book.it!
> Discover old classics that Google has forgotten.

## Motivation
Sometimes, with a vague description, it is difficult to successfully find the title of an older book on Google. This is where Book.it! comes in. With a couple optimized algorithms and a database of over 15,000 titles that go way back into the 1800s, Book.it can find that one old classic you simply cannot find with your Google search.

## Method
To search for relevant titles, the following steps are followed:
0. We precompute the frequency of each word in the plot summaries of each title and stor the information in a list of dictionaries. We serialize this variable with [pickle](https://docs.python.org/3/library/pickle.html).
1. The terms are split into individual words.
2. The [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) value of each term is calculated.
3.
