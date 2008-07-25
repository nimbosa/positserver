from django import newforms as forms
from django.contrib.formtools.wizard import FormWizard
from django.http import HttpResponseRedirect

value = ''
INSTANCES = (
		('one', 'Single Instance'),
		('many', 'Multiple Instances'),)

class AppgenForm(forms.Form):
	application_name = forms.CharField(initial='POSIT')
	application_type = forms.CharField(initial='victims', help_text="What type of data will you collect?<br/><b>Example:</b>victims,hawks")
	instances = forms.ChoiceField(choices=INSTANCES, help_text="""Will your application deal with multiple instances of a type of an object?
			<br/> <b>For example:</b> If your application deals with findings only and you just need one type, select single instance
			but if your application has multiple instances of the same object, say sightings of birds, select multiple instance.""")

class AppgenFormForInstance(forms.Form):
	record_name = forms.CharField(initial='finds')
	instance_name = forms.CharField(initial='sightings')
	server_address = forms.CharField(initial='192.168.1.139')


class AppgenFormForRecord(forms.Form):
	record_name = forms.CharField(initial='finds')
	server_address = forms.CharField(initial='192.168.1.139')

class StringGenForm(forms.Form):
	pass
#def get_second_form( values ):
  # second form contains only labels for items selected in FirstForm
#  class SecondForm( forms.Form ):
#    def __init__( self, values):
#      super( SecondForm, self ).__init__( values )
#      self.fields['instance'] = forms.CharField( max_length=100 )

#  return SecondForm
	
#def get_second_form(value):
#	return AppgenForm2(value)
	


class AppWizard(FormWizard):
	def done(self, request, form_list):
		return HttpResponseRedirect('/app/thanks/')

	def process_step(self, request, form, step):
		if (step==0):
			form.full_clean()
			value = form.cleaned_data['instances']
			check = forms.CharField()
			if (value == 'many'):
				self.form_list.append(get_second_form(value))
			print value, self.form_list
		super(AppWizard, self ).process_step( request, form, step )
