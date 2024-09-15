import PyPDF2  # pip install PyPDF2
import nltk  # pip install nltk   ....   for more infor check https://www.nltk.org/
from collections import Counter
import matplotlib.pyplot as plt  # pip install matplot
import os

books_folder = 'books'
book_title = 'book1.txt'
plot_folder = 'zipf_plots'
book_path = os.path.join(books_folder, book_title)



if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

def get_custom_rank():
    return (list(range(1,10, 1)) + list(range(10,100, 10)) + list(range(100, 1000, 100)) + list(range(1000, 10000, 1000)) + list(range(10000, 100000, 1000)) )

# Step 1: Extract Text
# for txt files
print('\nStep 1: Extract Text from text file')
try:
    with open(book_path, 'r', encoding='utf-8') as file:  # Opening the text file in read mode
        book_text = file.read()  # Reading the entire text file content as a string
except FileNotFoundError:
    print("File not found. Please check the path and the name of the file and try again.")
    exit()
# for pdf files
# with open(book_path, 'rb') as file:  # PDFs are not plain text files—they contain binary data. That's why we open them in binary mode ('rb') when reading the contents
#     reader = PyPDF2.PdfReader(file)
#     book_text = ''
#     for page in reader.pages:
#         book_text += page.extract_text()  # extract_text() turns the binary content of a PDF into usable text strings

# uncomment below for verification
# print("The first 1000 chars of the book are: " + book_text[:1000] + '"\n')
# print('- - - \n - - - \n  - - - \n')

# Step 2: Tokenize the Text
print('\nStep 2: Downloading punkt tokenizer and tokenizing the text\n')
nltk.download('punkt')  # for more info: https://www.nltk.org/api/nltk.tokenize.punkt.html
book_tokens = nltk.word_tokenize(book_text)
# uncomment for verification
# print("\nThe first 100 tokens of the book are: \n")
# print(book_tokens[:100])
# print('\n- - - \n - - - \n - - - \n')

#Step 3: Token cleaning (only alphabetic tokens i.e. words without numbers or punctuation)
print('\nStep 3: Token cleaning')
cleaned_tokens = [token.lower() for token in book_tokens if token.isalpha()]
# uncomment for verification
# print("\nThe first 100 cleaned tokens of the book are: \n")
# print(cleaned_tokens[:100])
# print('\n- - - \n - - - \n - - - \n')

#Step 4: Calculate token frequencies
print('\nStep 4: Calculate token frequencies')
token_frequencies = Counter(cleaned_tokens)
# Counter is an unordered collection where elements are stored as Dict keys and their count as dict value. 
# more info https://www.digitalocean.com/community/tutorials/python-counter-python-collections-counter
# uncomment for verification
# print("\nThe top 10 most frequent words are: \n")
# print(token_frequencies.most_common(10))  # https://note.nkmk.me/en/
# print('\n- - - \n - - - \n - - - \n')

# Step 5: Calculate k = f*r
print(f"{'Word':<20}{'frequency':<20}{'cumulative frequency':<30}{'rank':<12}{'k':<12}")
sorted_token_frequencies = token_frequencies.most_common()
cum_freq = 0
num_of_cleaned_tokens = len(cleaned_tokens)
custom_rank = get_custom_rank()
for rank, (token, frequency) in enumerate(sorted_token_frequencies, start=1):
    cum_freq += frequency/num_of_cleaned_tokens
    if rank in custom_rank:
        cum_freq_str = f"{round(cum_freq * 100, 2)}%"
        print(f"{token:<20}{frequency:<20}{cum_freq_str:<30}{rank:<12}{frequency*rank}\n")

ranks = range(1, len(sorted_token_frequencies)+1)
frequencies = [freq for (_, freq) in sorted_token_frequencies]

plt.figure(figsize=(10, 8))
plt.plot(ranks, frequencies, marker='o', linestyle='-', color='b')
plt.xlabel('rank')
plt.ylabel('frequency')
plt.title(f"Zipf's Law: Freq. v.s. Rank for {book_title}")
plt.grid(True)
plt.savefig(os.path.join(plot_folder, "zipfs_law_frequency_rank.png"))
plt.show()
print(f"zipfs_law_frequency_rank plot saved in {plot_folder} folder")
plt.close()

plt.figure(figsize=(10, 8))
plt.loglog(ranks, frequencies, marker='o', linestyle='-', color='b')
plt.xlabel('log(rank)')
plt.ylabel('log(frequency)')
plt.title(f"Zipf's Law: Log(Freq.) v.s. Log(Rank) for {book_title}")
plt.grid(True)
plt.savefig(os.path.join(plot_folder, "zipfs_law_log_frequency_rank.png"))
plt.show()
print(f"zipfs_law_log_frequency_rank plot saved in {plot_folder} folder")
plt.close()
