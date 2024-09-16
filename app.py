from flask import Flask, render_template
from forms import FileUploadForm
from zipflaw_analysis import run_zipf_analysis  # Import the analysis function

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkeyhahaha'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FileUploadForm()
    freq_img_data = None
    log_img_data = None
    table_data = None


    if form.validate_on_submit():
        file = form.file.data
        book_text = file.read().decode('utf-8')
        freq_img_data, log_img_data, table_data = run_zipf_analysis(book_text)


    
    return render_template('index.html', form=form, freq_img_data=freq_img_data, log_img_data=log_img_data, table_data = table_data)

if __name__ == '__main__':
    app.run(debug=True)