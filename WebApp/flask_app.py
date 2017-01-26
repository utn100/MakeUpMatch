##########################################################################################################
#Functions for viewing html templates
##########################################################################################################
from flask import Flask, render_template, request, redirect, url_for
from scripts.forms import InputForm
from scripts.recommender import Products as prod
from scripts.recommender import Ingredients as ingr
import pandas as pd


#create Flask app
app = Flask(__name__)

#pre-load distances
distances = pd.read_csv('static/data/dist_reviews_tfidf.csv', header=0)

#display output
@app.route('/output')
def output(imgs=None, pgs=None, ref_imgs=None, ref_pgs=None):

    #restrict access
    if request.referrer is None:
        return render_template("403.html")
    
    #initialize variables
    imgs = request.args.get('imgs')
    pgs = request.args.get('pgs')
    ref_imgs = request.args.get('ref_imgs')
    ref_pgs = request.args.get('ref_pgs')

    #return output page
    return render_template("output.html", imgs=imgs, pgs=pgs, ref_imgs=ref_imgs, ref_pgs=ref_pgs)

#process products and ingredients
@app.route('/process')
def process(product_id=None, ingred=None):
    
    #restrict access
    if request.referrer is None:
        return render_template("403.html")

    #initialize variables
    product_id = request.args.get('product_id')
    ingred = request.args.get('ingred')

    #drop ingredients
    dists = ingr.dropIngreds(ingred, distances)

    #find nearest products
    recommended = prod.getTop(product_id, dists)

    #find reference product
    reference = prod.getRef(product_id)

    return redirect(url_for("output", recs=recommended, refs=reference))

#display homepage
@app.route('/inputs', methods=('GET', 'POST'))
def inputs():
    form = InputForm()
    error = None
    
    if request.method == 'POST':
        
        #check brand name
        brand_name = request.form.get('brand_name')
        if brand_name =='':
            return render_template("homepage.html", form=form, error="ERROR: Brand name required.")
        
        #check product name
        product_name = request.form.get('product_name')
        if product_name =='':
            return render_template("homepage.html", form=form, error="ERROR: Product name required.")
        
        #check ingredient name
        ingred_name = request.form.get('ingred_name')
        if ingred_name =='':
            return render_template("homepage.html", form=form, error="ERROR: Ingredient name required.")
                
        #query for product
        product = prod.findProduct(brand_name, product_name)
        if product == False:
            return render_template("homepage.html", form=form, error="Sorry, we do not have that product.")
        
        #query for ingredient
        ingred = ingr.findIngred(ingred_name)
        if ingred == False:
            return render_template("homepage.html", form=form, error="Sorry, we do not have that ingredient.")
        
        #go to process page
        return redirect(url_for("process", product_id=product, ingred=ingred))
        
        
    else:
        return render_template("homepage.html", form=form, error=error)


#display about
@app.route('/about')
def about():
    return render_template("about.html")


#display contact
@app.route('/contact')
def contact():
    return render_template("contact.html")


#display 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


#display 403
@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

#display homepage
@app.route('/homepage', methods=('GET', 'POST'))
def homepage():
    form = InputForm()
    error = None
    return render_template("homepage.html", form=form, error=error)

#display index
@app.route('/', methods=('GET', 'POST'))
def index():
    form = InputForm()
    error = None
    return render_template("homepage.html", form=form, error=error)


if __name__ == "__main__":
    app.run()














