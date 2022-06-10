from wtforms import Form, StringField, validators


'''
INCOMPLETE
'''
class RegistrationForm(Form):
    username = StringField('username', [validators.length(min=1, max=30)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])


'''
INCOMPLETE
'''
class LoginForm(Form):
    email = StringField('email', [validators.length(min=7, max=50)])