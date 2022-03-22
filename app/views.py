"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from threading import local
from app import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from app.forms import Add_Property
from app.models import Propertydb
from werkzeug.utils import secure_filename
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Rene Tim")

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route('/properties/create', methods=['GET', 'POST'])
def add_property():
    property_object = Add_Property()
    p_title = property_object.property_title.data
    p_description = property_object.description.data
    p_no_of_rooms = property_object.no_of_rooms.data
    p_no_of_bathrooms = property_object.no_of_bathrooms.data
    p_price = property_object.price.data
    p_type = property_object.property_type.data
    p_location = property_object.location.data
    p_photo = property_object.photo.data

    if request.method == 'GET':
        return render_template('add_property.html', prop_obj=property_object)

    if request.method == 'POST':
        if property_object.validate_on_submit():
            clean_p_photo = secure_filename(p_photo.filename)
            p_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], clean_p_photo))
            if (p_photo and clean_p_photo) != "":
                prop_addition = Propertydb(p_title, p_description, p_no_of_rooms, p_no_of_bathrooms, p_price, p_type, p_location, clean_p_photo)
                db.session.add(prop_addition)
                db.session.commit()
                flash('Success! Your property has been saved.', 'success')
                return redirect(url_for('show_properties'))
    flash_errors(property_object)
    return render_template('add_property.html', prop_obj=property_object)

@app.route('/properties')
def show_properties():
    if request.method == 'GET':
        get_properties = Propertydb.query.all()
        return render_template('properties.html', properties=get_properties, loc=locale)

@app.route('/properties/<id>')
def show_property(id):
    get_property = Propertydb.query.filter(Propertydb.id==id).all()[0]
    return render_template('property.html', property = get_property, loc = locale)

@app.route('/uploads/<filename>')
def get_upload(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
