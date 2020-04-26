#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import logging
import os
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}

# TODO: connect to a local postgresql database (Completed)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# Venue has many Show
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy=True)
    genres = db.Column(db.String)
    city_state_id = db.Column(db.Integer, db.ForeignKey('CityState.id', ondelete='CASCADE'), nullable=False)


class CityState(db.Model):
    __tablename__ = 'CityState'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), nullable=False, unique=True)
    venues = db.relationship('Venue', backref='city_state', lazy=True, cascade='all, delete-orphan')
    state = db.Column(db.String(120), nullable=False, unique=True)
    artists = db.relationship('Artist', backref='city_state', lazy=True, cascade='all, delete-orphan')

# TODO: implement any missing fields, as a database migration using Flask-Migrate (Completed)
# Artist has many Shows
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True, cascade='all, delete-orphan')
    city_state_id = db.Column(db.Integer, db.ForeignKey('CityState.id', ondelete='CASCADE'), nullable=False)


# TODO: implement any missing fields, as a database migration using Flask-Migrate (Completed)

# TODO (Completed): Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data. (Completed)
  city_state = CityState.query.all()
  data = []
  for c in city_state:
      ven_list = [{
        "id": venue.id,
        "name": venue.name
      } for venue in c.venues]
      data.append({
        "city": c.city.title(),
        "state": c.state.upper(),
        "venues": ven_list
      })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: (Completed) implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.genres.ilike('%{}%'.format(search_term))).all()
  print(venues)
  response2 = {
    "count": len(venues),
    "data": [{
        "id": venue.id,
        "name": venue.name
    } for venue in venues]
  }
  return render_template('pages/search_venues.html', results=response2, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # TODO: replace with real venue data from the venues table, using venue_id (Completed)
  venue = Venue.query.get(venue_id)
  past_shows, upcoming_shows = get_past_upcom_shows(venue.shows, 0)
  genres = venue.genres.split(',')[:-1]
  city_state = CityState.query.get(venue.city_state_id)
  data = {
    "id": venue.id,
    "name": venue.name,
    "city": city_state.city,
    "state": city_state.state,
    "address": venue.address,
    "phone": venue.phone,
    "genres": genres,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "website": venue.website,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  return render_template('pages/show_venue.html', venue=data)

# Helper function to get Past_Shows and Upcoming_Shows | return Tuple(p_shows, u_shows)
def get_past_upcom_shows(shows, category): # Category:  0 => Venue | 1 => Artist
    past_shows = []
    upcoming_shows = []
    if category: # Get shows for Artist
        for show in shows:
            venue = Venue.query.get(show.venue_id)
            if show.start_time < datetime.today():
                past_shows.append({
                    "venue_id": show.venue_id,
                    "venue_name": venue.name,
                    "venue_image_link": venue.image_link,
                    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                })
            else:
                upcoming_shows.append({
                    "venue_id": show.venue_id,
                    "venue_name": venue.name,
                    "venue_image_link": venue.image_link,
                    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                })
    else: # Get shows for Venue
        for show in shows:
            artist = Artist.query.get(show.artist_id)
            if show.start_time < datetime.today():
                past_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": artist.name,
                    "artist_image_link": artist.image_link,
                    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                })
            else:
                upcoming_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": Artist.query.get(show.artist_id).name,
                    "artist_image_link": Artist.query.get(show.artist_id).image_link,
                    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                })
    return (past_shows, upcoming_shows)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead (Completed)
  # TODO: on unsuccessful db insert, flash an error instead. (Completed)
  # TODO: modify data to be the data object returned from db insertion (Completed)
  form = VenueForm()
  error = False
  genres_list = ''
  if form.validate():
      try:
          # Get image_link
          file = request.files['image_link']
          if file and allowed_file(file.filename):
              filename = secure_filename(file.filename)
              filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
              file.save(filepath)
              for g in form.genres.data:
                  genres_list += '{},'.format(g)
              # Check if City and State Already exists
              city = form.city.data.strip().title()
              state = form.state.data
              city_state = CityState.query.filter_by(state=state).first()
              if not city_state:
                  city_state = CityState(
                    city=city,
                    state=state
                  )
              venue = Venue(
                name=form.name.data.strip(),
                address=form.address.data.strip(),
                phone=form.phone.data.strip(),
                genres=genres_list,
                image_link=filepath,
                seeking_talent=form.seeking_talent.data,
                seeking_description=form.seeking_description.data.strip(),
                website=form.website.data.strip(),
                facebook_link=form.facebook_link.data.strip())
              city_state.venues.append(venue)
              db.session.add(venue)
              db.session.commit()
              print('File found: {}'.format(file.filename))
          else:
              error=True
              form.errors['image_link'] = ['Invalid image extension']
      except Exception as e:
          error = True
          print(e)
          db.session.rollback()
      finally:
          db.session.close()
      if not error:
          flash('Venue "' + form.name.data + '" was successfully listed!')
          return render_template('pages/home.html', errors=form.errors)
      else:
          print(form.errors)
          flash('Error: Venue "' + form.name.data + '" Cannot be created')
          return render_template('forms/new_venue.html', form=form, errors=form.errors)

  print(form.errors)
  return render_template('forms/new_venue.html', form=form, errors=form.errors)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using (Compeleted)
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error=False
  try:
      venue = Venue.query.get(venue_id)
      db.session.delete(venue)
      db.session.commit()
  except:
      error=True
      db.session.rollback()
  finally:
      db.session.close()
      if not error:
          print('Venue with ID: {} | Deleted successfully'.format(venue_id))
      else:
          print('ERROR: Venue with ID: {} | Colud not be deleted'.format(venue_id))

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database (Completed)
  artists = Artist.query.all()
  data = [{
    "id": artist.id,
    "name": artist.name,
  } for artist in artists]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: (Completed) implement search on artists with partial string search. Ensure it is case-insensitive.
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
  response={
    "count": len(artists),
    "data": [{
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": filter(lambda show: show.start_time >= datetime.today(), artist.shows)
    } for artist in artists]
  }
  print(response2['data'])
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # TODO: (Completed) replace with real artist data from the artists table, using artist_id
  artist = Artist.query.get(artist_id)
  genres = artist.genres.split(',')[:-1]
  city_state = CityState.query.get(artist.city_state_id)
  past_shows, upcoming_shows = get_past_upcom_shows(artist.shows, 1)
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": genres,
    "facebook_link": artist.facebook_link,
    "website": artist.website,
    "city": city_state.city,
    "state": city_state.state,
    "phone": artist.phone,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  city_state = CityState.query.get(artist.city_state_id)
  form = ArtistForm(seeking_venue = 1 if artist.seeking_venue else 0, genres=artist.genres.split(',')[:-1], state=city_state.state)
  artist={
    "id": artist.id,
    "name": artist.name,
    "city": city_state.city,
    "state": city_state.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id> (Completed)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing (Completed)
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  error=False
  is_new_city_state = False
  artist = {}
  genres_list = ''
  filepath = ''
  try:
      # Get image_link
      file = request.files['image_link']
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
          file.save(filepath)
          artist = Artist.query.get(artist_id)
          city_state_old = CityState.query.get(artist.city_state_id)
          city_state_new = CityState.query.filter_by(state=form.state.data).first()
          if not city_state_new:
              print('He didnt find it, it is new')
              city_state_new = CityState(city=form.city.data.strip(), state=form.data.state)
              db.session.add(city_state_new)
              city_state_new.artists.append(artist)
          else:
              if city_state_old.state != city_state_new.state:
                  print('I am here***********')
                  is_new_city_state=True

          for g in form.genres.data:
              genres_list += '{},'.format(g)
          artist.name = form.name.data.strip()
          artist.phone = form.phone.data.strip()
          artist.genres = genres_list
          artist.website = form.website.data.strip()
          artist.facebook_link = form.facebook_link.data.strip()
          artist.seeking_venue = form.seeking_venue.data
          artist.seeking_description = form.seeking_description.data.strip()
          artist.image_link = filepath
          if is_new_city_state:
              db.session.add(artist)
              print('gsdfsdfsdfsdfsdfsfsdf')
              city_state_new.artists.append(artist)
              # city_state_old.artists.remove(artist)

          db.session.commit()
      else:
          artist = {
            'name': form.name.data,
            'phone': form.phone.data,
            'genres': form.genres.data,
            'city': form.city.data,
            'state': form.state.data,
            'website': form.website.data,
            'facebook_link': form.facebook_link.data,
            'seeking_venue': form.seeking_venue.data,
            'seeking_description': form.seeking_description.data,
          }
          print(artist)
          error=True
          form.errors['image_link'] = ['Invalid image']
  except Exception as e:
      print(e)
      artist = {
        'name': form.name.data,
        'phone': form.phone.data,
        'genres': form.genres.data,
        'city': form.city.data,
        'state': form.state.data,
        'website': form.website.data,
        'facebook_link': form.facebook_link.data,
        'seeking_venue': form.seeking_venue.data,
        'seeking_description': form.seeking_description.data,
      }
      error=True
      db.session.rollback()
  finally:
      db.session.close()
      if not error:
          flash('Artist "' + form.name.data + '" Update Successfully')
          return redirect(url_for('show_artist', artist_id=artist_id))
      else:
          flash('ERROR: Artist "' + form.name.data + '" Cannot be updated')
          return render_template('forms/edit_artist.html', form=form, artist=artist, errors=form.errors)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  city_state = CityState.query.get(venue.city_state_id)
  form = VenueForm(seeking_talent = 1 if venue.seeking_talent else 0, genres=venue.genres.split(',')[:-1], state=city_state.state)
  venue={
    "id": venue.id,
    "name": venue.name,
    "city": city_state.city,
    "state": city_state.state,
    "phone": venue.phone,
    "address": venue.address,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id> (Completed)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing (Completed)
  form = VenueForm()
  print('asdkaskdaskdksakdkasdksadsasd')
  error=False
  is_new_city_state = False
  venue = {}
  genres_list = ''
  filepath = ''
  try:
      # Get image_link
      file = request.files['image_link']
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
          file.save(filepath)
          venue = Venue.query.get(venue_id)
          city_state_old = CityState.query.get(venue.city_state_id)
          city_state_new = CityState.query.filter_by(state=form.state.data).first()
          if not city_state_new:
              print('He didnt find it, it is new')
              city_state_new = CityState(city=form.city.data.strip(), state=form.state.data)
              db.session.add(city_state_new)
              city_state_new.venues.append(venue)
          else:
              if city_state_old.state != city_state_new.state:
                  print('I am here***********')
                  is_new_city_state=True

          for g in form.genres.data:
              genres_list += '{},'.format(g)
          venue.name = form.name.data.strip()
          venue.phone = form.phone.data.strip()
          venue.genres = genres_list
          venue.address = form.address.data.strip()
          venue.website = form.website.data.strip()
          venue.facebook_link = form.facebook_link.data.strip()
          venue.seeking_talent = form.seeking_talent.data
          venue.seeking_description = form.seeking_description.data.strip()
          venue.image_link = filepath
          if is_new_city_state:
              db.session.add(venue)
              print('gsdfsdfsdfsdfsdfsfsdf')
              city_state_new.venues.append(venue)

          db.session.commit()
      else:
          venue = {
            'name': form.name.data,
            'phone': form.phone.data,
            'genres': form.genres.data,
            'city': form.city.data,
            'address': form.address.data,
            'state': form.state.data,
            'website': form.website.data,
            'facebook_link': form.facebook_link.data,
            'seeking_talent': form.seeking_talent.data,
            'seeking_description': form.seeking_description.data,
          }
          print(venue)
          error=True
          form.errors['image_link'] = ['Invalid image']
  except Exception as e:
      print(e)
      venue = {
        'name': form.name.data,
        'phone': form.phone.data,
        'genres': form.genres.data,
        'city': form.city.data,
        'address': form.address.data,
        'state': form.state.data,
        'website': form.website.data,
        'facebook_link': form.facebook_link.data,
        'seeking_talent': form.seeking_talent.data,
        'seeking_description': form.seeking_description.data,
      }
      error=True
      db.session.rollback()
  finally:
      db.session.close()
      if not error:
          flash('Venue "' + form.name.data + '" Update Successfully')
          return redirect(url_for('show_venue', venue_id=venue_id))
      else:
          flash('ERROR: Venue "' + form.name.data + '" Cannot be updated')
          return render_template('forms/edit_venue.html', form=form, errors=form.errors, venue=venue)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # TODO: insert form data as a new Venue record in the db, instead (Completed)
  # TODO: on unsuccessful db insert, flash an error instead. (Completed)
  # TODO: modify data to be the data object returned from db insertion (Completed)
  error = False
  form = ArtistForm()
  genres_list = ''
  if form.validate():
      try:
          file = request.files['image_link']
          if file and allowed_file(file.filename):
              filename = secure_filename(file.filename)
              filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
              file.save(filepath)
              for g in form.genres.data:
                  genres_list += '{},'.format(g)
              city_state = CityState.query.filter_by(state=form.state.data).first()
              if not city_state:
                  city_state = CityState(
                    city=form.city.data.strip().title(),
                    state=form.state.data
                  )
              artist = Artist(
                name = form.name.data.strip(),
                phone = form.phone.data.strip(),
                genres = genres_list,
                image_link = filepath,
                seeking_venue = form.seeking_venue.data,
                seeking_description = form.seeking_description.data.strip(),
                website = form.website.data.strip(),
                facebook_link = form.facebook_link.data.strip())
              city_state.artists.append(artist)
              db.session.add(artist)
              db.session.commit()
          else:
              error=True
              form.errors['image_link'] = ['Invalid image extension']
      except Exception as e:
          print(e)
          error=True
          db.session.rollback()
      finally:
          db.session.close()
          if not error:
              flash('Artist "' + request.form['name'] + '" Added Successfully')
              return render_template('pages/home.html', errors=form.errors)
          else:
              flash('ERROR: Artist "' + request.form['name'] + '" cannot be added')
              return render_template('forms/new_artist.html', form=form, errors=form.errors)

  print(form.errors)
  return render_template('forms/new_artist.html', form=form, errors=form.errors)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # TODO: replace with real venues data. (Completed)
  shows = Show.query.all()
  data = []
  for show in shows:
      artist = Artist.query.get(show.artist_id)
      data.append({
          "venue_id": show.venue_id,
          "venue_name": Venue.query.get(show.venue_id).name,
          "artist_id": show.artist_id,
          "artist_name": artist.name,
          "artist_image_link": artist.image_link,
          "start_time": show.start_time.strftime('%m/%d/%Y, %H:%M:%S')
      })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # TODO: insert form data as a new Show record in the db, instead (Completed)
  error=False
  form = ShowForm(request.form)
  if form.validate():
      try:
          show = Show(
            venue_id = form.venue_id.data,
            artist_id = form.artist_id.data,
            start_time = form.start_time.data
          )
          db.session.add(show)
          db.session.commit()
      except:
          db.session.rollback()
          error=True
      finally:
          db.session.close()
          if not error:
              flash('Show was successfully created')
              return render_template('pages/home.html', errors=form.errors)
          else:
              flash('There is an Error creating show')
              return render_template('forms/new_show.html', form=form)

  return render_template('forms/new_show.html', errors=form.errors)
  # TODO: on unsuccessful db insert, flash an error instead. (Completed)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
