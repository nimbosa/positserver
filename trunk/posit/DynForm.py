from django import forms

class DynForm(forms.Form):    
    """
    Dynamic form that allows the user to change and then verify the data that was parsed
    """
    def setFields(self, kwds):
        """
        Set the fields in the form
        """
        keys = kwds.keys()
        keys.sort()
        for k in keys:
            self.fields[k] = kwds[k]
            
    def setData(self, kwds):
        """
        Set the data to include in the form
        """
	self.is_bound = True
        keys = kwds.keys()
        keys.sort()
        for k in keys:
            self.data[k] = kwds[k]
            
    def validate(self, post):
        """
        Validate the contents of the form
        """
        for name,field in self.fields.items():
            try:
                field.clean(post[name])
            except ValidationError, e:
                self.errors[name] = e.messages

#### In the view ########################################################
	
# Form definition
# kwargs is a dictionary. The key being the name of the field and the value 
# being the type (CharField(kwargs*))
#kwargs['a_name'] = forms.CharField(label="Name", max_length=25, help_text="name")
#kwargs['b_lname'] = forms.CharField(label="Last Name", help_text="lname")
#kwargs['c_bday'] = forms.DateField(label="Birthday", help_text="birthday")

# Creating the form object and manipulating/validating it
#form = DynForm() # Create the form
#form.setFields(kwargs) # Set the fields as defined in the kwargs dictionary
#form.setData(request.POST) # Set the form data
#form.validate(request.POST) # validate the from 

##########################################################################

