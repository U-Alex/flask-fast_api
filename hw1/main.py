from flask import Flask, render_template

app = Flask(__name__)

cat_list = {'cat_list': ['одежда', 'обувь']}
product_list = (['товар1', 'товар2', 'товар3', 'товар4'], ['товар5', 'товар6', 'товар7', 'товар8'])


@app.route('/')
def index():
    context = cat_list
    return render_template('category.html', context=context)


@app.route('/<int:cat_num>/')
def category(cat_num):
    context = cat_list
    context.update({'product_list': product_list[cat_num-1]})
    return render_template('category.html', context=context)


@app.route('/<int:cat_num>/<int:prod_id>/')
def product(cat_num, prod_id):
    context = cat_list
    context.update({'product_list': product_list[cat_num-1]})
    context.update({'product': product_list[cat_num-1][prod_id-1]})
    return render_template('product.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)
