import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.feature_extraction.text import CountVectorizer
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources (only the first time)
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

# 1. Load & clean data
posts_df = pd.read_csv('csv/offmychest_posts_comments_combined.csv')

def clean_and_tokenize(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize
    tokens = nltk.word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words]
    # Remove tokens that are purely numbers
    tokens = [w for w in tokens if not any(c.isdigit() for c in w)]
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(w) for w in tokens]
    return ' '.join(tokens)  # Join back into a cleaned string

posts_df['cleaned_post_text'] = posts_df['post_text'].apply(clean_and_tokenize)
print('Data cleaned... ' + posts_df.head().to_string());

# 2. Calculate supportive_percentage
# posts_df['supportive_percentage'] = posts_df['supportive_comments'] / posts_df['all_comments']

# 3. Tokenize posts into words (basic cleaning)
vectorizer = CountVectorizer(min_df=2)  # No need for stopwords='english' anymore because we cleaned
word_matrix = vectorizer.fit_transform(posts_df['cleaned_post_text'])
print('Tokenization complete... ' + str(word_matrix.shape[0]) + ' posts and ' + str(word_matrix.shape[1]) + ' words found.');

# 4. Build word/post matrix
word_df = pd.DataFrame(word_matrix.toarray(), columns=vectorizer.get_feature_names_out())
word_df['supportive_percentage'] = posts_df['supportive_percentage'].values
print('Word matrix created... ' + str(word_df.shape[0]) + ' posts and ' + str(word_df.shape[1]) + ' words found.');

# 5. Compare supportive % for each word
results = []
for word in vectorizer.get_feature_names_out():
    group_with_word = word_df[word_df[word] == 1]['supportive_percentage']
    group_without_word = word_df[word_df[word] == 0]['supportive_percentage']
    
    if len(group_with_word) < 2 or len(group_without_word) < 2:
        continue  # skip words appearing too rarely
    
    t_stat, p_val = stats.ttest_ind(group_with_word, group_without_word, equal_var=False)
    mean_with = group_with_word.mean()
    mean_without = group_without_word.mean()
    difference = mean_with - mean_without
    
    results.append({
        'word': word,
        'mean_supportive_with_word': mean_with,
        'mean_supportive_without_word': mean_without,
        'difference': difference,
        'p_value': p_val,
        'word_count': word_df[word].sum()
    })
print('Statistical analysis complete... ' + str(len(results)) + ' words analyzed.');

# 6. Output results
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by='difference', ascending=False)
results_df.to_csv('csv/word_supportive_analysis.csv', index=False)

# 7. Visualization
# Top 10 positive and top 10 negative words
word_count = 50;
top_positive = results_df.head(word_count)
# top_negative = results_df.tail(10)

# Barplot - Top Positive Words
plt.figure(figsize=(18, 8))
plt.bar(top_positive['word'], top_positive['difference'])
plt.xticks(rotation=90)
plt.title(f"Top {word_count} Words Correlated with Higher Supportive Comments")
plt.xlabel('Word')
plt.ylabel('Difference in Supportive %')
plt.tight_layout()
plt.savefig('csv/top_positive_words.png')
plt.show()

# # Barplot - Top Negative Words
# plt.figure(figsize=(14, 6))
# plt.bar(top_negative['word'], top_negative['difference'])
# plt.xticks(rotation=45)
# plt.title('Top 10 Words Correlated with Lower Supportive Comments')
# plt.xlabel('Word')
# plt.ylabel('Difference in Supportive %')
# plt.tight_layout()
# plt.savefig('top_negative_words.png')
# plt.show()

# # Scatter Plot - Frequency vs Effect Size
# plt.figure(figsize=(10, 6))
# plt.scatter(results_df['word_count'], results_df['difference'])
# plt.title('Word Frequency vs Impact on Supportive Comments')
# plt.xlabel('Word Count in Posts (log scale)')
# plt.ylabel('Difference in Supportive %')
# plt.xscale('log')
# plt.grid(True)
# plt.tight_layout()
# plt.savefig('word_frequency_vs_impact.png')
# plt.show()

print("✅ Analysis complete! Results saved to 'word_supportive_analysis.csv' and plots saved as PNG files.")
