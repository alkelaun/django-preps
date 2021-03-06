import datetime
from django.db import models
from django.template.defaultfilters import slugify
from preps.apps.models import ModelBase
from preps.apps.sports.models import Season, School, GameBase, Player, Sport, Conference
from preps.apps.utils import functions as preps_utils

class FootballFields(models.Model):
    '''
    Represents statistics fields for Football. Used like a mixin.
    '''
    football_games                  = models.IntegerField(default=0, blank=True)
    rushing_rushes                  = models.IntegerField(default=0, blank=True)
    rushing_yards                   = models.IntegerField(default=0, blank=True)
    rushing_touchdowns              = models.IntegerField(default=0, blank=True)
    passing_attempts                = models.IntegerField(default=0, blank=True)
    passing_completions             = models.IntegerField(default=0, blank=True)
    passing_yards                   = models.IntegerField(default=0, blank=True)
    passing_interceptions           = models.IntegerField(default=0, blank=True)
    passing_touchdowns              = models.IntegerField(default=0, blank=True)
    receiving_receptions            = models.IntegerField(default=0, blank=True)
    receiving_yards                 = models.IntegerField(default=0, blank=True)
    receiving_touchdowns            = models.IntegerField(default=0, blank=True)
    kicking_xp_attempts             = models.IntegerField(default=0, blank=True)
    kicking_xp_made                 = models.IntegerField(default=0, blank=True)
    kicking_fg_attempts             = models.IntegerField(default=0, blank=True)
    kicking_fg_made                 = models.IntegerField(default=0, blank=True)
    football_fumbles                = models.IntegerField(default=0, blank=True)
    defense_tackles                 = models.IntegerField(default=0, blank=True)
    defense_sacks                   = models.IntegerField(default=0, blank=True)
    defense_interceptions           = models.IntegerField(default=0, blank=True)
    defense_fumbles_recovered       = models.IntegerField(default=0, blank=True)
    defense_fumbles_forced          = models.IntegerField(default=0, blank=True)
    
    class Meta:
        abstract                    = True

class Position(ModelBase):
    '''
    Represents a single Football position.
    '''
    name                            = models.CharField(max_length=255)
    short_name                      = models.CharField(max_length=5, help_text="5 characters or fewer.")
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.__unicode__())
        super(Position, self).save(*args, **kwargs)
    

class Game(GameBase):
    '''
    Represents a single Football game.
    '''
    home_team                       = models.ForeignKey(School, related_name="football_home_team", null=True)
    away_team                       = models.ForeignKey(School, related_name="football_away_team", null=True)
    season                          = models.ForeignKey(Season, related_name="football_game_season")
    home_quarter_1_score            = models.IntegerField(default=0, blank=True)
    home_quarter_2_score            = models.IntegerField(default=0, blank=True)
    home_quarter_3_score            = models.IntegerField(default=0, blank=True)
    home_quarter_4_score            = models.IntegerField(default=0, blank=True)
    home_overtime_1_score           = models.IntegerField(default=0, blank=True)
    home_overtime_2_score           = models.IntegerField(default=0, blank=True)
    home_overtime_3_score           = models.IntegerField(default=0, blank=True)
    home_total_score                = models.IntegerField(default=0, blank=True)
    away_quarter_1_score            = models.IntegerField(default=0, blank=True)
    away_quarter_2_score            = models.IntegerField(default=0, blank=True)
    away_quarter_3_score            = models.IntegerField(default=0, blank=True)
    away_quarter_4_score            = models.IntegerField(default=0, blank=True)
    away_overtime_1_score           = models.IntegerField(default=0, blank=True)
    away_overtime_2_score           = models.IntegerField(default=0, blank=True)
    away_overtime_3_score           = models.IntegerField(default=0, blank=True)
    away_total_score                = models.IntegerField(default=0, blank=True)
    week                            = models.IntegerField(max_length=2, default=0)
    game_of_the_week                = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s, week %s: %s at %s' % (self.season, self.week, self.away_team, self.home_team)
        
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.__unicode__())
        self.home_total_score   =   self.home_quarter_1_score+\
                                    self.home_quarter_2_score+\
                                    self.home_quarter_3_score+\
                                    self.home_quarter_4_score+\
                                    self.home_overtime_1_score+\
                                    self.home_overtime_2_score+\
                                    self.home_overtime_3_score
        self.away_total_score   =   self.away_quarter_1_score+\
                                    self.away_quarter_2_score+\
                                    self.away_quarter_3_score+\
                                    self.away_quarter_4_score+\
                                    self.away_overtime_1_score+\
                                    self.away_overtime_2_score+\
                                    self.away_overtime_3_score
        super(Game, self).save(*args, **kwargs)
    

class TeamGame(GameBase, FootballFields):
    '''
    Represents a single Football team's performance in a single game.
    '''
    team                            = models.ForeignKey(School, related_name="football_teamgame_team",)
    game                            = models.ForeignKey(Game, related_name="football_teamgame_game",)
    
    def __unicode__(self):
        return u'Week %s: %s stats (%s)' % (self.game.week, self.team, self.id)
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.__unicode__())
        super(TeamGame, self).save(*args, **kwargs)
    

class TeamSeason(ModelBase, FootballFields):
    '''
    Represents a single Football team's performance in a single season.
    '''
    team                            = models.ForeignKey(School, related_name="football_teamseason_team")
    season                          = models.ForeignKey(Season, related_name="football_teamseason_season")
    wins                            = models.IntegerField(default=0, blank=True)
    losses                          = models.IntegerField(default=0, blank=True)
    points_for                      = models.IntegerField(default=0, blank=True)
    points_against                  = models.IntegerField(default=0, blank=True)
    place                           = models.IntegerField(default=0, blank=True)
    conference                      = models.ForeignKey(Conference, related_name="football_teamseason_conference")
    conference_wins                 = models.IntegerField(default=0, blank=True)
    conference_losses               = models.IntegerField(default=0, blank=True)
    
    def __unicode__(self):
        return u'Season %s: %s stats (%s)' % (self.season.name, self.team, self.id)
    
    def get_schedule(self):
        '''
        Defines a function which returns games where this team is either the home or away team,
        ordered by week.
        '''
        return Game.objects.filter(Q(away_team=self) | Q(home_team=self)).order_by('week')

    # Defines a field "schedule" as a dynamic property of the get_schedule() function.
    schedule = property(get_schedule)
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.__unicode__())
        super(TeamSeason, self).save(*args, **kwargs)
    

class PlayerGame(ModelBase, FootballFields):
    '''
    Represents a single Football player's performance in a single game.
    '''
    player                          = models.ForeignKey(Player, related_name="football_playergame_player")
    game                            = models.ForeignKey(Game, related_name="football_playergame_game")
    
    def __unicode__(self):
        return u'Week %s: %s stats (%s)' % (self.game.week, self.player, self.id)
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.__unicode__())
        self.rushing_yards_per_attempt      = float(floatformat(preps_utils.handle_percents(self.rushing_yards, self.rushing_attempts), 1))
        self.receiving_yards_per_reception  = float(floatformat(preps_utils.handle_percents(self.receiving_yards, self.receptions), 1))
        self.passing_completion_percentage  = float(floatformat(preps_utils.handle_percents(self.passing_completions, self.passing_attempts), 3))
        self.passing_yards_per_attempt      = float(floatformat(preps_utils.handle_percents(self.passing_yards, self.passing_attempts), 1))
        if self.passing_attempts == 0:
            self.passing_rating = 0.0
        else:
            self.passing_rating             = float(floatformat(handle_hss_passer_rating(
                self.passing_yards,
                self.passing_touchdowns,
                self.passing_completions,
                self.passing_interceptions,
                self.passing_attempts
            ), 1))
        super(PlayerGame, self).save(*args, **kwargs)
    

class PlayerSeason(ModelBase, FootballFields):
    '''
    Represents a single Football player's season performance.
    '''
    player                          = models.ForeignKey(Player, related_name="football_playerseason_player")
    season                          = models.ForeignKey(Season, related_name="football_playerseason_season")
    position                        = models.ManyToManyField(Position, related_name="football_playerseason_position")
    number                          = models.IntegerField(default=0, blank=True)
    games                           = models.IntegerField(default=0, blank=True)
    rushing_yards_per_attempt       = models.FloatField(default=0.0)
    receiving_yards_per_reception   = models.FloatField(default=0.0)
    passing_yards_per_attempt       = models.FloatField(default=0.0)
    passing_completion_percentage   = models.FloatField(default=0.0)
    passing_rating                  = models.FloatField(default=0.0)
    
    def __unicode__(self):
        return u'Week %s: %s stats (%s)' % (self.game.week, self.player, self.id)
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.__unicode__())
        self.rushing_yards_per_attempt      = float(floatformat(preps_utils.handle_percents(self.rushing_yards, self.rushing_attempts), 1))
        self.receiving_yards_per_reception  = float(floatformat(preps_utils.handle_percents(self.receiving_yards, self.receptions), 1))
        self.passing_completion_percentage  = float(floatformat(preps_utils.handle_percents(self.passing_completions, self.passing_attempts), 3))
        self.passing_yards_per_attempt      = float(floatformat(preps_utils.handle_percents(self.passing_yards, self.passing_attempts), 1))
        if self.passing_attempts == 0:
            self.passing_rating = 0.0
        else:
            self.passing_rating             = float(floatformat(handle_hss_passer_rating(
                self.passing_yards,
                self.passing_touchdowns,
                self.passing_completions,
                self.passing_interceptions,
                self.passing_attempts
            ), 1))
        super(PlayerSeason, self).save(*args, **kwargs)
    

def handle_hss_passer_rating(yds, tds, cmpls, ints, atts):
    '''
    Defines a function which computes NCAA passer rating.
    '''
    yards = 8.4 * yds
    touchdowns = 330 * tds
    completions = 100 * cmpls
    interceptions = 200 * ints
    rating = yards + touchdowns + completions - interceptions
    return floatformat(rating / atts)