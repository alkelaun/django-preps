import datetime
from django.db import models
from django.template.defaultfilters import slugify
from preps.apps.models import ModelBase

class Sport(ModelBase):
    '''
    Represents a single sport.
    '''
    GENDER_CHOICES = (
        (0, 'Boys'),
        (1, 'Girls'),
        (2, 'Coed'),
    )
    name                            = models.CharField(max_length=255)
    gender                          = models.IntegerField(max_length=1, choices=GENDER_CHOICES)
    
    def __unicode__(self):
        return u'%s %s' % (self.get_gender_display(), self.name)
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug               = slugify(self.__unicode__())
        super(Sport, self).save(*args, **kwargs)
    

class Conference(ModelBase):
    '''
    Represents a single conference.
    '''
    name                            = models.CharField(max_length=255)
    sport                           = models.ForeignKey(Sport)
    
    def __unicode__(self):
        return u'%s: %s' % (self.name, self.sport)
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug               = slugify(self.__unicode__())
        super(Conference, self).save(*args, **kwargs)
    

class Season(ModelBase):
    '''
    Represents a single sport season.
    '''
    name                            = models.IntegerField(max_length=4, help_text="Integer representing the year of the season, e.g., 2011.")
    start_date                      = models.DateField(blank=True, null=True, help_text="Start date for this season.")
    end_date                        = models.DateField(blank=True, null=True, help_text="End date for this season.")
    sport                           = models.ForeignKey(Sport)
    
    def __unicode__(self):
        return u'%s %s' % (self.sport, self.name)
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug               = slugify(self.__unicode__())
        super(Season, self).save(*args, **kwargs)
    

class School(ModelBase):
    '''
    Represents a single school.
    '''
    name                            = models.CharField(max_length=255)
    address                         = models.TextField(default='')
    local                           = models.BooleanField(default=False)
    url                             = models.URLField(blank=True, null=True)
    mascot                          = models.CharField(max_length=255, blank=True, null=True)
    logo_url                        = models.URLField(blank=True, null=True)
    use_custom_logo                 = models.BooleanField(default=False)
    active_sports                   = models.ManyToManyField(Sport, null=True)
    
    def __unicode__(self):
        if self.mascot:
            return u'%s %s' % (self.name, self.mascot)
        else:
            return self.name
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug               = slugify(self.__unicode__())
        super(School, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        return ('school_detail', None, { 'school_slug': self.slug, 'pk': self.id })
    

class Player(ModelBase):
    '''
    Represents a single player.
    '''
    school                          = models.ForeignKey(School)
    first_name                      = models.CharField(max_length=255)
    last_name                       = models.CharField(max_length=255)
    middle_name                     = models.CharField(max_length=255, blank=True, null=True)
    height_feet                     = models.IntegerField(max_length=1, default=0)
    height_inches                   = models.IntegerField(max_length=2, default=0)
    weight_pounds                   = models.IntegerField(max_length=3, default=0)
    
    def __unicode__(self):
        return u'%s %s (%s)' % (self.first_name, self.last_name, self.school)
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':        
            self.slug               = slugify(self.__unicode__())
        super(Player, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        return ('player_detail', None, { 'player_slug': self.slug, 'pk': self.id })

class GameBase(ModelBase):
    '''
    Abstract base class for games.
    '''
    GAME_STATUS_CHOICES = (
        (0, 'Pregame'),
        (1, 'In progress'),
        (2, 'Delayed'),
        (3, 'Postponed'),
        (9, 'Final'),
    )
    GAME_TYPE_CHOICES = (
        (0, 'Preseason'),
        (1, 'Regular season'),
        (9, 'Playoff'),
    )
    game_date_time                  = models.DateTimeField(blank=True, null=True)
    override_game_scores            = models.BooleanField(default=False)
    status                          = models.IntegerField(max_length=1, choices=GAME_STATUS_CHOICES, default=0)
    status_description              = models.TextField(blank=True, null=True)
    game_type                       = models.IntegerField(max_length=1, choices=GAME_TYPE_CHOICES, default=0)
    featured_game                   = models.BooleanField(default=False)
    game_location                   = models.CharField(max_length=255, blank=True, null=True)
    game_location_address           = models.TextField(blank=True, null=True)
    game_location_description       = models.TextField(blank=True, null=True)
    conference_game                 = models.BooleanField(default=False)
    game_result_headline            = models.CharField(max_length=255, blank=True, null=True)
    game_result_summary             = models.TextField(blank=True, null=True)
    game_live_audio                 = models.CharField(max_length=255, blank=True, null=True)
    game_live_video                 = models.TextField(blank=True, null=True)
    
    class Meta:
        abstract=True

class MeetBase(ModelBase):
    '''
    Abstract base class for meets.
    '''
    MEET_STATUS_CHOICES = (
        (0, 'Pregame'),
        (1, 'In progress'),
        (2, 'Delayed'),
        (3, 'Postponed'),
        (9, 'Final'),
    )
    MEET_TYPE_CHOICES = (
        (0, 'Preseason'),
        (1, 'Regular season'),
        (9, 'Playoff'),
    )
    meet_date_time                  = models.DateTimeField(blank=True, null=True)
    status                          = models.IntegerField(max_length=1, choices=MEET_STATUS_CHOICES, default=0)
    status_description              = models.TextField(blank=True, null=True)
    meet_type                       = models.IntegerField(max_length=1, choices=MEET_TYPE_CHOICES, default=0)
    featured_meet                   = models.BooleanField(default=False)
    meet_location                   = models.CharField(max_length=255, blank=True, null=True)
    meet_location_address           = models.TextField(blank=True, null=True)
    meet_location_description       = models.TextField(blank=True, null=True)
    conference_meet                 = models.BooleanField(default=False)
    meet_result_headline            = models.CharField(max_length=255, blank=True, null=True)
    meet_result_summary             = models.TextField(blank=True, null=True)
    
    class Meta:
        abstract=True