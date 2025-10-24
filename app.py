from flask import Flask, render_template, redirect, url_for, request

from DAL import add_project, delete_project, list_projects

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    errors = {}
    form_data = {
        'title': request.form.get('title', '').strip(),
        'description': request.form.get('description', '').strip(),
        'image_filename': request.form.get('image_filename', '').strip(),
    }

    if request.method == 'POST':
        if not form_data['title']:
            errors['title'] = 'Project title is required.'
        if not form_data['description']:
            errors['description'] = 'Please add a short project description.'
        if not form_data['image_filename']:
            errors['image_filename'] = 'Include the image file name stored in static/images.'

        if not errors:
            add_project(
                form_data['title'],
                form_data['description'],
                form_data['image_filename'],
            )
            return redirect(url_for('projects'))
    else:
        form_data = {'title': '', 'description': '', 'image_filename': ''}

    project_rows = list_projects()
    return render_template(
        'projects.html',
        projects=project_rows,
        form_data=form_data,
        errors=errors,
    )

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return redirect(url_for('thankyou'))
    return render_template('contact.html')

@app.route('/projects/<int:project_id>/delete', methods=['POST'])
def remove_project(project_id):
    delete_project(project_id)
    return redirect(url_for('projects'))

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)
