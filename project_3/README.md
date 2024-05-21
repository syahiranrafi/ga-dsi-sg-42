# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Project 3 - Web APIs & NLP
Group 3:
Chin Chung Yau,
Ryan Yong,
Syahiran Rafi

- [Background](#Background) 
- [Problem Statement](#Problem-Statement)
- [Data Collection](#Data-Collection)
- [Data Cleaning & EDA](#Data-Cleaning-and-EDA)
- [Model Evaluation](#Model-Evaluation)
- [Hyperparameter Tuning](#Hyperparameter-Tuning)
- [Implementation](#Implementation)
- [Conclusion](#Conclusions)



# Background

As Reddit unveiled its [IPO](https://www.businesstimes.com.sg/companies-markets/reddit-prices-ipo-top-indicated-range-raise-us-748-million) at the higher range of US$34 a share, public eye has begun to focus on Reddit. What was once considered a benefit to users, Reddit's loose content-moderation approach has turned into a [weakness by political hobbyists and social hackers](https://www.weforum.org/agenda/2017/06/fighting-the-rise-of-fake-news-means-taking-another-look-at-your-phone-this-is-why/), aimed to disseminate misinformation on America's 4th most visited website.

Regarding misinformation, for the context of this project, it will follow [American Psychological Association](https://www.apa.org/topics/journalism-facts/misinformation-disinformation) (APA)'s classifcation as "any information that is demonstrably false or otherwise misleading, regardless of its source or intention." This is because fake news and satire articles are considered misinformation, deferring only in intention.

---

# Problem Statement

As Reddit navigates its IPO lock-up in the year of 2024, it has been attempting to adopt a more serious approach towards content moderation.

By using a classification model, we aim to help Reddit reduce the spread of misinformation by determining whether news posts on the site may be classified as fact or misinformation based on user engagement and discussion.

Additionally, we aim to help the user moderators on Reddit streamline their content moderation process within their individual subreddits.

---

# Data Collection

Data was scraped from two specific subreddits, r/news and r/TheOnion. r/news was used as the benchmark of factual news sources while r/TheOnion was used as a representation of misinformation. This is because r/TheOnion posts satirical articles from The Onion Website, which is widely known as a satirical journalist webpage with articles made with the intent of humor. However, satire articles are still characteristically misinformation, and hence r/TheOnion serves as a good representation of users interacting with headlines that are deemed misinformation.

# Data Cleaning and EDA

### Data Cleaning

To facilitate better results for EDA and modelling, it necessary to clean the raw data to remove any noise (characters/words/phrases which are not meaningful).

Our data cleaning process includes:
1. remove URL, 
2. remove newline
3. replace [deleted] and [removed] with "pseudodeleted" and "pseudoremoved"
4. remove newline/carriage return 
5. remove stop words 
6. remove punctuation and special characters
7. convert to lower → lemmatization 
8. remove lines with null comment

### Exploratory Data Analysis
EDA for data scraped from subreddits involves gaining insights into the dataset's characteristics, identifying patterns, and understanding its underlying structure. 

Further analysis includes analysing the distribution of comment lengths, distribtion of sentiment scores and topic modelling to identify common themes between the subreddits.

In general, both subreddits shared a significant overlap in the top 20 common words, but bigrams (and higher n-grams) showed a clearer distinction between the comments (r/news tends to be more political while r/TheOnion tends to have more violent discussion themes). The distribution of sentiment scores also showed comments in r/news to be more polarized than those in r/TheOnion.

# Model Evaluation

### Cross Validation Score Summary

#### Table of Cross Validation Scores for Count Vectorizer


| Models | cvec_accuracy | cvec_precision | cvec_recall | cvec_f1_score |
| -------- | :-------------- | :--------------- | ------------- | --------------- |
| lr     | 0.768834      | 0.742258       | 0.780837    | 0.760433      |
| knn    | 0.529564      | 0.500468       | 0.928744    | 0.650389      |
| nb     | 0.769999      | 0.780215       | 0.708682    | 0.741381      |
| bag    | 0.715901      | 0.834866       | 0.727339    | 0.706666      |
| xgb    | 0.699139      | 0.834866       | 0.447373    | 0.579627      |

#### Table of Cross Validation Scores for Td-idf Vectorizer


| Models | tvec_accuracy | tvec_precision | tvec_recall | tvec_f1_score |
| -------- | --------------- | ---------------- | ------------- | --------------- |
| lr     | 0.776433      | 0.762822       | 0.761956    | 0.761644      |
| knn    | 0.774421      | 0.470107       | 0.937005    | 0.626059      |
| nb     | 0.774421      | 0.793643       | 0.702445    | 0.744181      |
| bag    | 0.736396      | 0.728202       | 0.702782    | 0.714966      |
| xgb    | 0.838557      | 0.838557       | 0.445013    | 0.578061      |



from the tables above, best combination for hyper parameter tuning was chosen to be Logistic Regression with CountVectorizer as the transformer.

# Hyperparameter Tuning

Using a combination of GridSearchCV and Pipeline, the chosen combination was tuned based on the following parameters:

### Parameters

1. CountVectorizer
   * max Features: [2000,7500]
   * stop_words: [None,'english']
   * min_df: [1,10]
   * max_df: [0.1,0.9]
   * ngram_range: [(1,1),(1,2)]
2. Logistic Regression
   - C: [0.01, 1.0, 10]
   - penalty: ['l1','l2']
   - class_weight: ['balanced']

### GridSearchCV results

Using the following parameter metrics listed above, the GridSearchCV results are as follows:

1. CountVectorizer
   * max Features: 7500
   * stop_words: 'english'
   * min_df: 1
   * max_df: 0.1
   * ngram_range: (1,2)
2. Logistic Regression
   - C: 1.0
   - penalty: 'l1'
   - class_weight: 'balanced'

Using these parameters, the model was able to perform with a score of 0.837, with an accuracy of 0.796, precision of 0.752, sensitivity of 0.845 and f1_score of 0.796. This final model was pickled and used in the implementation process moving forward

## Implementation

Using a combined version of all the previous sections, a webscrape was done on r/politics as an example. The cleaning process done in 02 & 03 was executed identically while analysis of keywords such as 'misleading headlines' in the user comments help highlight potential posts that serve as a litmus test on the model's performance.

The model aims to assess the potential misinformation of the post from individual user comments and then aggregating the results based on wisdom of the crowd. This allows a % misinformation calculator to be generated, whcih triggers an alert warning on the dashboard for any given post that exceeds the threshold.

This threshold is able to be adjusted, and for the current model is set at 55%. This thresold resulted in a 43% of the first 100 posts on the hot page of r/politics to be flagged with an alert warning, which cuts down the moderator's duty by 57%. Instead of having to individually assess every post, moderators are now able to focus their attention on the flagged posts, streamlining their workflow using the dashboard.

### Conclusions

In conclusion, this project has effectively built a model using data collected from r/news and r/TheOnion to determine if a news article is deemed as fact or misinformation from the user engagement and discussions. While the similarities between top words of r/news and r/TheOnion prove to be difficult for human assessment, the model was still able to distinguish between the two types of articles effectively, with a streamlit app serving as an online dashboard for moderators to access quickly and effectively. Further improvements on the dataset and the threshold will improve the model's performance on sensitivity and accuracy.

---

### Files

* code
  1. 01_Data_Collection.ipynb
  2. 02_Data_Cleaning.ipynb
  3. 03_EDA.ipynb
  4. 04_Model_Evaluation.ipynb
  5. 05_Grid_HyperparameterTuning.ipynb
  6. 05a_Model_Pickling.ipynb
  7. 06_Implementation.ipynb
  8. count_vectorizer.pkl
  9. model.pkl
* data
  1. 01_raw_news_data.csv
  2. 01_raw_onion_data.csv
  3. 02_cleaned_data.csv
  4. 03_data_post_EDA.csv
* slides
  1. SG-DSI-42_PROJECT_03_GRP_03.pdf
* streamlit
  1. reddit_moderator_dashboard.py
  2. count_vectorizer.pkl
  3. model.pkl
* README.md
