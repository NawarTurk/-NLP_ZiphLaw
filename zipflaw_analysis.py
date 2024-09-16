import nltk  # pip install nltk   ....   for more infor check https://www.nltk.org/
from collections import Counter
import matplotlib.pyplot as plt  # pip install matplot
import matplotlib
import io
import base64



def run_zipf_analysis(book_text):
    def get_custom_rank():
        return (list(range(1,10, 1)) + list(range(10,100, 10)) + list(range(100, 1000, 100)) + list(range(1000, 10000, 1000)) + list(range(10000, 100000, 1000)) )

    matplotlib.use('Agg')

    nltk.download('punkt')  # for more info: https://www.nltk.org/api/nltk.tokenize.punkt.html
    book_tokens = nltk.word_tokenize(book_text)


    print('\nStep 3: Token cleaning')
    cleaned_tokens = [token.lower() for token in book_tokens if token.isalpha()]
    print(len(cleaned_tokens))

    token_frequencies = Counter(cleaned_tokens)
  
    sorted_token_frequencies = token_frequencies.most_common()
    cum_freq = 0
    table_data = []
    num_of_cleaned_tokens = len(cleaned_tokens)
    custom_rank = get_custom_rank()
    for rank, (token, frequency) in enumerate(sorted_token_frequencies, start=1):
        cum_freq += frequency/num_of_cleaned_tokens
        if rank in custom_rank:
            table_data.append({
                "word": token,
                "frequency": frequency,
                "cumulative_frequency": f"{round(cum_freq * 100, 2)}%",
                "rank": rank,
                "k": frequency * rank
            })

    ranks = range(1, len(sorted_token_frequencies)+1)
    frequencies = [freq for (_, freq) in sorted_token_frequencies]

    freq_img = io.BytesIO()  # Create an in-memory byte buffer
    plt.figure(figsize=(10, 8))
    plt.plot(ranks, frequencies, marker='o', linestyle='-', color='b')
    plt.xlabel('rank')
    plt.ylabel('frequency')
    plt.title(f"Zipf's Law: Freq. v.s. Rank")
    plt.grid(True)
    plt.savefig(freq_img, format='png')  # Save the figure to the buffer
    plt.close()
    freq_img.seek(0)  # Rewind the buffer
    freq_img_data = base64.b64encode(freq_img.getvalue()).decode('utf-8')  # Convert to base64


    log_img = io.BytesIO()  # Create another in-memory byte buffer
    plt.figure(figsize=(10, 8))
    plt.loglog(ranks, frequencies, marker='o', linestyle='-', color='b')
    plt.xlabel('log(rank)')
    plt.ylabel('log(frequency)')
    plt.title(f"Zipf's Law: Log(Freq.) v.s. Log(Rank)")
    plt.grid(True)
    plt.savefig(log_img, format='png')  # Save the figure to the buffer
    plt.close()
    log_img.seek(0)  # Rewind the buffer
    log_img_data = base64.b64encode(log_img.getvalue()).decode('utf-8')  # Convert to base64

    return freq_img_data, log_img_data, table_data

