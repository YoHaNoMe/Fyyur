from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import RadioField, StringField, SelectField, SelectMultipleField, DateTimeField, IntegerField
from wtforms.validators import InputRequired, DataRequired, AnyOf, URL, Length, NumberRange

class ShowForm(FlaskForm):
    venue_id = IntegerField(
        'venue_id', validators=[
            InputRequired(message='This field is required'),
            NumberRange(min=1, message='ID cannot be zero or negative'),
            ]
    )
    artist_id = IntegerField(
        'venue_id', validators=[
            InputRequired(message='This field is required'),
            NumberRange(min=1, message='ID cannot be zero or negative'),
            ]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[InputRequired('This field is required')],
        default= datetime.today()
    )

class VenueForm(FlaskForm):
    name = StringField(
        'name',
        validators=[DataRequired(message='This field is required')]
    )
    city = StringField(
        'city',
        validators=[DataRequired(message='This field is required'), Length(max=120)]
    )
    state = SelectField(
        'state',
        validators=[DataRequired(message='This field is required')],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address',
        validators=[DataRequired(message='This field is required'), Length(min=2, max=120, message='The maximum length is 120')]
    )
    phone = StringField(
        'phone',
        validators=[DataRequired(message='This field is required'), Length(min=2, max=120, message='The maximum length is 120')]
    )
    seeking_talent = RadioField(
        'seeking_talent',
        choices = [(1, 'Yes'), (0, 'No')],
        coerce=int,
        default=0
    )
    seeking_description = StringField(
        'seeking_description',
        validators=[Length(max=120, message='The maximum is 120')]
    )
    image_link = FileField(
        'image_link',
        validators = [FileRequired(message='This field is required')]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres',
        validators=[DataRequired(message='This field is required')],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link',
        validators=[URL(message='Invalid Url')]
    )
    website = StringField(
        'website',
        validators=[URL(message='Invalid Url')]
    )

class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
    )
    seeking_venue = RadioField(
        'seeking_venue',
        choices = [(1, 'Yes'), (0, 'No')],
        coerce=int,
        default=0
    )
    seeking_description = StringField(
        'seeking_description',
        validators=[Length(max=120, message='The maximum is 120')]
    )
    image_link = FileField(
        'image_link',
        validators = [FileRequired(message='This field is required')]
    )

    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ],
        # default = ['Folk', 'Alternative']
    )

    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website',
        validators=[URL(message='Invalid Url')]
    )
    available_time = StringField(
        'available_time',
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM (completed)
