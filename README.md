# MultipleChoiceOCR

This program was prototype created in the early versions of the popular app "HQ Trivia" to show
a possible way to play the game unfairly.

The program uses Google's Optical Character Recognition API to detect the question and answers that are being displayed on the screen.
Once the question and answerse are tokenized, the program uses Beautiful Soup to search the top 5 web-results, and ranks the answers choices using a
scoring system that grants points for how many times the answer choice appears and where they appear in the web results.
(An appearance in the first web result will grant more points than an appearance in the 5th web result).

The program then counts the totals and display which answer choice is the most likely winner.

The program also detects the word "NOT" in the question, in which case the answer choice with the least amount of points will be
displayed as winning. 
