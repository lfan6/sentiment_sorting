# Lucas Fan
# FE-595 Assignment 3
# Sentiment Sorting

import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob


def merge_files(path):
    """ Function that merges files located in the path variable. * Note, the files must be in the form that we had in
    the previous assignment: a csv file with 2 columns of name and purpose"""
    os.chdir(path)  # Assigns the working directory based on path input
    num_files = int(input("How many files do you want to merge? "))  # Asks users for # of files wanted to merge
    print("Please enter the full name of each file (including '.csv')")
    files = []
    for i in range(0, num_files):  # Asks user for the file names, and adds names to a list
        file_name = input("Name of file "+str(i+1)+": ")
        files.append(file_name)
    data = pd.read_csv(files[0], skiprows=1, header=None)  # Create base dataframe from first file
    for i in range(1, num_files):  # Adds all the other files to the dataframe
        data = data.append(pd.read_csv(files[i], skiprows=1, header=None), ignore_index=True)
    data.columns = ['Name', 'Purpose']  # Sets column names
    return data


def best_worst(data):
    """ Function to find the best and worst business ideas by looking at the polarity scores of their purposes """
    scores = []
    analyzer = SentimentIntensityAnalyzer()  # Initialize Sentiment Analyzer
    for i in range(0, len(data)):  # Looping through list of purposes
        score = analyzer.polarity_scores(data.Purpose[i])['compound']  # Find the compound score of each purpose
        scores.append(score)  # Add score to list
    data['Score'] = scores # Adding the scores to the dataframe so each company has a score
    data = data.sort_values('Score').reset_index(drop=True)  # Sorting the dataframe by the score and resetting index
    print("Best Business Idea\n Company: " + data.Name.iloc[-1] + "\n Purpose: " + data.Purpose.iloc[-1] +
          "\n Score: " + str(data.Score.iloc[-1]))  # Prints last company in dataframe (highest score)
    print("Worst Business Idea\n Company: "+data.Name[0]+"\n Purpose: "+data.Purpose[0] +
          "\n Score: "+str(data.Score[0]))  # Prints first company in the dataframe (lowest score)
    return


def most_common(data):
    """ Function that finds the most common words/tokens in the company purposes"""
    desc = data.Purpose.str.cat(sep='. ')  # Concatenating all purposes into 1 big string
    blob = TextBlob(desc)  # Initialize TextBlob
    count = blob.word_counts  # Counts frequency of all the words in the descriptions
    sorted_count = sorted(count.items(), key=lambda x: x[1], reverse=True)  # Sorts the dictionary by the value
    word = []
    freq = []
    for i in range(0, 10):  # Loop to find the 10 most common words
        word.append(sorted_count[i][0])  # Most common word
        freq.append(sorted_count[i][1])  # Frequency of the word
    final = pd.DataFrame({'Word/Token': word, 'Frequency': freq})  # Adding the top 10 words to a dataframe
    print(final)


if __name__ == "__main__":
    df = merge_files("/Users/lucasfan/Documents/FE-595/PycharmProjects/HW3/Results")
    best_worst(df)
    most_common(df)

