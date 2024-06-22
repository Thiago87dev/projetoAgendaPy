from django import forms
from contact.models import Contact
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category',
            'picture',
        )
        # config os campos e widgets 1 (utilizado para criar)
        # widgets = {
        #     'first_name': forms.TextInput(
        #         attrs={
        #             'class': 'class-a1 class-b1',
        #             'placeholder': 'Escreva aqui'
        #         }
        #     )
        # }
        
    # config os campos e widgets 2 (utilizado para criar)
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'class-a2 class-b2',
                'placeholder': 'Escreva aqui'
            }
        ),
        label='first name here',
        help_text='Help text for the user'  
    )
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        ),
        required=False
    )
    
    # config os campos e widgets 3 (utilizado para alterar/atualizar)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # self.fields['first_name'].widget.attrs.update({
        #     'class': 'class-a3 class-b3',
        #     'placeholder': 'Escreva aqui',
        # })
        
        # deixando os inputs com a borda vermelha em caso de erro
        # for field in self.fields:
        #     if self.errors.get(field):
        #         current_classes = self.fields[field].widget.attrs.get('class', '')
        #         self.fields[field].widget.attrs['class'] = f'{current_classes} input-error'
    
    # validando campos    
    # Quando for validar mais de um campo juntos (quando um campo depende do outro) (ex: senhas iguais)
    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        if first_name == last_name:
            msg = ValidationError(
                'First name and last name cannot be the same',
                code = 'invalid'
            )
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)
                
        return super().clean()
    
    # Quando for validar apenas um campo separado
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        if first_name == 'ABC':
            self.add_error(
                'first_name',
                ValidationError(
                    'It can`t be ABC',
                    code='invalid'
                )
            )
        return first_name
    
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )
    last_name = forms.CharField(
        required=True,
        min_length=3,
    )
    email = forms.EmailField(
        required=True,
        min_length=3,
    )
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2'
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('A user with that email already exists.', code='invalid')
            )
        
        return email

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=3,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length':'Please, add more than 2 letters'
        }
    )
    
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length':'Please, add more than 1 letters'
        }
    )
    
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    
    password2 = forms.CharField(
        label='Password 2',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Use the same password as before',
        required=False
    )
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username'
        )
        
    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        
        password = cleaned_data.get('password1')
        if password:
            user.set_password(password)
            
        if commit:
            user.save()
            
        return user
        
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Passwords must be the same')
                )
        
        return super().clean()
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email
        
        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('A user with that email already exists.', code='invalid')
                )
        
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )
        return password1