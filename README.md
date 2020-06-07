# Book.it!
> Discover old classics that Google has forgotten.

## Motivation
Sometimes, with a vague description, it is difficult to successfully find the title of an older book on Google. This is where Book.it! comes in. With a couple optimized algorithms and a database of over 15,000 titles that go way back into the 1800s, Book.it can find that one old classic you simply cannot find with your Google search.

## Method
First, we load in our dataset with [pandas](https://pandas.pydata.org/). We follow by precomputing the frequency of each word in the plot summaries of each title and store the information in a list of dictionaries. We serialize this variable with [pickle](https://docs.python.org/3/library/pickle.html) so that this precomputation (quadratic time complexity) is only run once. 

For each query,

1. The terms are split into individual words.
2. For each title, the [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) value of each term is calculated.
3. A score is assigned to each title, being the sum of tf-idf values for each search term.
4. Titles are sorted by tf-idf values.
5. The top 20 results are taken. We calculate the [longest common subsequence](https://en.wikipedia.org/wiki/Longest_common_subsequence_problem) (an element in the sequence is a word) between the search terms and each title's summary. Using that metric, we finally reorder the top 20 results.

The time complexity for a single query is O(NlogM) where N is the total number of book titles and M is the sum of the number of words in the summary of each title.

Our choice to use LCS to rank the top 20 tf-idf results is to add grammatical structure to our ranking process. Although tf-idf by itself is a spectacular ranking algorithm, it is only limited to individual terms. LCS enables us to gauge how relevant the entire search string is (though it is obligatory to mention that LCS on its own, without the help of tf-idf to narrow down the results, is not a good algorithm to use for our purposes).
