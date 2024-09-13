from django import forms

from adminpanel.models import Blog, Comment, User, Profile



class BlogForm(forms.ModelForm):
    status_choices = (
        ('PUBLISH', 'Publish'),        
        ('DRAFT', 'Draft'),
    )
    title = forms.CharField(
        max_length=200, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of your Blog'})
    )
    description = forms.CharField(
        required=True, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Scribble your content'})
    )
    blog_image = forms.ImageField(
        required=True, 
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=status_choices, 
        required=True, 
        initial='PUBLISH',
        widget=forms.RadioSelect(attrs={'class': 'form-radio-inline'})
    )

    class Meta:
        model = Blog
        exclude = ['user', 'created_at', 'updated_at']

class CommentForm(forms.ModelForm):
   
    comment = forms.CharField(
        max_length=200, 
        required=True, 
        label="",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Post your comments here'})
    )
    
    class Meta:
        model = Comment
        fields =['comment']

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'})
    )
    new_password1 = forms.CharField(
        required=True,
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        required=True,
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'})
    )

    class Meta:
        model = User
        fields = '__all__'
        
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("The old password is incorrect.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("The new passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        new_password = self.cleaned_data.get('new_password1')
        self.user.set_password(new_password)
        if commit:
            self.user.save()
        return self.user


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label='First Name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=True, label='Last Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(max_length=50, required=True, label='Email',
                             widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    username = forms.CharField(max_length=50, required=True, label='Username',
                               widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control','readonly':'readonly'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
   
class ProfileForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Phone"
    )
    profile_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe yourself'
        }),
        label="About"
    )
    profile_image = forms.ImageField(
        label="Profile Picture",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )
    id_proof = forms.ImageField(
        label="ID Proof",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Profile
        exclude = ['user']

