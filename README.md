# Portifolio Template With Flask
#### Video Demo:  <https://www.youtube.com/watch?v=e5LPFMAWw6c>
#### Description:
This is a portifolio template using bootstrap and flask. it's supposed to allow users to upload image files, select which ones should be displayed on the main page and generate most html stuff without the need to manually select the images, it uses sqlite databases to store all data.

file sources:
favicon
https://www.favicon.cc/?action=icon&file_id=730577

navbar logo
https://logoipsum.com/

most images
placekitten.com

##### layout.html
Basic Layout across all other pages, navbar and footer. Also contains a hidden admin link available only if logged in

##### layout.js
Just a simple script used on pages with images to display them inside the modal body.

##### index.html
Here we have a jinja loop that iterates over all "selected" images on the database and a striped down modal component from bootstrap for showing the images.

##### secret.html
accessible only ny manually typing secret in the url, have a form  that requires a "secret" string that is optionally stored as a enviroment variable, if data match in admin table the user will have acess to the admin page.

##### admin.html
There's a form that allows user to upload new images to the server. Also displays all images registered. It's possible to edit the images' title, description and wheter they're visible on the main page

##### contact.html and services.html
contact is supposed to have a simple text with any kind of contact you'd like to provide.
services has a carousel component from bootstrap, that should contain slides showing the kind of service you provide and a paragraph for the same purpose, since you probably won't list many services, there's no jinja loop and  you'll have to manually update the src attribute

##### delete.html and update.html
blank pages only suppose to handle requests originated from admin.html

##### styles.css
just basic classes with gradient colors

##### app.py and helpers.py
helpers.py only has a single function login_required
app.py manages all routes, validations and file managment

###### index
renders the index template with only the selected images

###### projecs
renders the project template with all registered images

###### services
only renders a basic page with some text

###### layout
redirects to index since it`s not supposed to be seen

###### secret
validates the form and logs in, there`s a commented section that used to be used to register a new admin

###### admin
handles all file uploads

###### delete/update
handles all delete/update operations

