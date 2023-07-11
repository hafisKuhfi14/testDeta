from streamlit_authenticator.exceptions import RegisterError

def _register_credentials(self, username: str, name: str, password: str, email: str, preauthorization: bool):
    """
    Adds to credentials dictionary the new user's information.

    Parameters
    ----------
    username: str
        The username of the new user.
    name: str
        The name of the new user.
    password: str
        The password of the new user.
    email: str
        The email of the new user.
    preauthorization: bool
        The preauthorization requirement, True: user must be preauthorized to register, 
        False: any user can register.
    """
    if not self.validator.validate_username(username):
        raise RegisterError('Username is not valid')
    if not self.validator.validate_name(name):
        raise RegisterError('Name is not valid')
    if not self.validator.validate_email(email):
        raise RegisterError('Email is not valid')
    
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
