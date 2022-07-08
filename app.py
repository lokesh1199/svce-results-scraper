from io import BytesIO

from flask import Flask, redirect, render_template, request, send_file, url_for
from openpyxl.writer.excel import save_virtual_workbook

from forms import ResultsForm
from scraper import generateRollNos, toExcel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab4d360b39c62652d5dceb5c8888abb87c2c9598c27f'


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ResultsForm()
    if form.validate_on_submit():
        start = form.startRollNo.data
        end = form.endRollNo.data
        link = form.link.data
        filename = form.filename.data + '.xlsx'

        print('start...')
        wb = toExcel(4, generateRollNos(start, end))
        print('done...')
        excel = BytesIO(save_virtual_workbook(wb))

        return send_file(excel, download_name=filename, as_attachment=True)

    return render_template('home.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
