/* Because i didnt set placeholder values in forms.py they will be set here using vanilla Javascript
//We start indexing at one because CSRF_token is considered and input field
*/

//Query All input fields
var form_fields = document.getElementsByTagName('input')
form_fields[1].placeholder = 'Username..';
form_fields[2].placeholder = 'Email..';
form_fields[3].placeholder = 'Enter password...';
form_fields[4].placeholder = 'Re-enter Password...';


for (var field in form_fields) {
    form_fields[field].className += ' form-control'
}