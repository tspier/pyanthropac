#############################################################
#   PyAnthropac, v0.1
#   Troy E. Spier, Ph.D.
#   Released on 26 November 2022
#############################################################
#
#   This program serves as a Python-based substitute
#   for the 1990s-era program called Anthropac, which
#   allows the results of freelisted ethnographic data
#   to be analyzed by frequency of occurrence and the
#   cognitive salience of each item individually, which
#   is based also on its distribution within the lists
#   themselves. The formula used to solve this is called
#   Smith's S and is as follows:
#
#       S = ((Σ(L-R + 1))/L)/N
#
#   In this formula, L is the number of items in each list,
#   R is the rank of the individual item within the list,
#   and N is the total number of lists. The sum of the
#   list-specific salience of each item is divided by the
#   total number of lists.
#############################################################
#
# NOTE:
#
#   There is a small (large?) caveat here that I am neither
#   a trained programmer nor someone with formal training in
#   statistics. Instead, I was offering a lesson to students
#   in our MA TESOL program on mixed-methods approaches to
#   data collected through a variety of methods, including
#   e.g. freelisting. In order to illustrate how this worked,
#   I gave them each one minute to write down any vulgar
#   words that they could think of in English. Some of these
#   are, admittedly, more vulgar than others, but the set of
#   lists offered a valuable set of practice data to be used
#   and tested through the program.
#############################################################

from prettytable import PrettyTable
import sys


def calculate_salience(file):
    # This section initializes all major variables at once and
    # sets them, where necessary, to zero or empty.
    global all_words, words_salience, lines
    all_words, words_salience = {}, {}
    count = 0
    line_number = 0

    # This section opens the file in read-only mode and reads
    # each line one-by-one, stripping the newline at the end
    # of each, and treating each line as the freelist of a
    # different participant.
    input = open(file, "r")
    lines = input.readlines()
    for line in lines:
        line = line.strip()

        # This section provides the headers and padding for the
        # tables concerning the freelists individually.
        myTable = PrettyTable(["Position in List", "Word", "Ranked Points", "Salience"])
        myTable.padding_width = 5

        # This section splits each line (i.e. each freelist) at
        # spaces and checks to see if each word has already been
        # included in the list of all words. If so, then the total
        # frequency increases by one; if not, then it is added to
        # the list and assigned a frequency of one.
        for word in line.split(" "):
            if word in all_words:
                all_words[word] += 1
            else:
                all_words[word] = 1
            count += 1
            length_of_list = len(line.split(" "))
            word_rank = line.split(" ").index(word)
            ranked_position = length_of_list - word_rank
            salience_in_list = "{:.2f}".format(ranked_position / length_of_list)

            # This section checks to see if the word is already in
            # the dictionary containing the freelist-specific salience
            # of that word. If so, then the salience of the new occurrence
            # is added to the extant value of any previous sums of
            # freelist-specific salience. If not, then the word is added
            # to the list, and the freelist-specific salience is assigned
            # as the value.
            if word in words_salience:
                words_salience[word] += float(salience_in_list)
            else:
                words_salience[word] = float(salience_in_list)

            # This line adds a new row of data to the table, which
            # includes the position in the list, the word itself,
            # the reverse-position in the list, and its salience
            # within that list itself. The position in the list has
            # to be reversed; otherwise, lower-listed items would
            # receive a higher score and, thus, provide wildly
            # inaccurate results.
            myTable.add_row([count, word, str(ranked_position), str(salience_in_list)])

        # This line resets the counter to zero and prints the table
        # and the participant number, which corresponds to the line,
        # i.e. if the data come from the third line, then this would
        # refer to the third participant.
        count = 0
        print(myTable.get_string(title="PARTICIPANT #" + str(line_number + 1)))
        line_number += 1


def word_frequency(all_words):
    # This section provides the headers and padding for the
    # tables concerning the word frequency (N/%) and overall
    # composite salience. It also calculates the total number
    # of unique words.
    wordFreqTable = PrettyTable(["Word", "Frequency (N)", "Frequency (%)", "Composite Salience"])
    wordFreqTable.padding_width = 5
    total_word_count = 0

    for frequency in all_words.values():
        total_word_count += frequency

    # This section utilizes the previous list of all words
    # and calculates the composite salience to two decimals
    # by dividing the summed freelist salience of each item
    # by the total number of participants (i.e. lines).
    for word, frequency in all_words.items():
        cognitive_salience = "{:.2f}".format(words_salience[word] / len(lines))
        word_frequency_percentage = "{:.2f}".format((frequency/total_word_count)*100)
        wordFreqTable.add_row([word, frequency, str(word_frequency_percentage), str(cognitive_salience)])

    # This section prints two different tables. Both contain
    # the word, its frequency of occurrence, and its composite
    # salience. The difference, however, is that the first
    # table sorts it by frequency; the second, by salience.
    print(
        wordFreqTable.get_string(
            sortby="Frequency (N)",
            reversesort=True,
            title="FREQUENCY AND COMPOSITE SALIENCE (SORTED BY WORD FREQUENCY)",
        )
    )
    print(
        wordFreqTable.get_string(
            sortby="Composite Salience",
            reversesort=True,
            title="FREQUENCY AND COMPOSITE SALIENCE (SORTED BY COMPOSITE SALIENCE)",
        )
    )


def main():
    # This section will utilize the second command-line argument
    # as the name of the file containing the freelists. The first
    # argument is always the name of the file. Any other arguments
    # given will be ignored.
    try:
        calculate_salience(sys.argv[1])
        word_frequency(all_words)

    # This section will alert the user if no file has been provided
    # as the argument, i.e. no data supplied to the program.
    except:
        print("********* ERROR *********")
        print("An error has occurred. Make sure to use the following command: ")
        print("\tpython3 pyanthropac.py NAME_OF_FILE.txt")


# This section ensures that the program begins with the main()
# function when run from the command line.
if __name__ == "__main__":
    main()
