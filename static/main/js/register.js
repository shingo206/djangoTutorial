const form_fields = document.getElementsByTagName('input');
form_fields[1].placeholder = 'Username..';
form_fields[2].placeholder = 'Email..';
form_fields[3].placeholder = 'Enter password...';
form_fields[4].placeholder = 'Re-enter Password...';

for (const field in form_fields) {
    if (form_fields.hasOwnProperty(field)) {
        form_fields[field].className += ' form-control'
    }
}