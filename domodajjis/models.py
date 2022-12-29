from django.db import models
from users.models import User

class Gathering(models.Model):
      name = models.CharField(max_length=30, unique=True)
      policy = models.CharField(max_length=255, null=True)
      member_count = models.SmallIntegerField(default=1)
      host = models.ForeignKey(User, related_name='gatherings', on_delete=models.SET_NULL, null=True)
      participant = models.ManyToManyField(User, through='domodajjis.UserGathering')
      created_at = models.DateTimeField(auto_now_add=True)

      class Meta:
            db_table = 'gatherings'

      def __str__(self):
          return self.name

class UserGathering(models.Model):
    role = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gathering = models.ForeignKey(Gathering, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_gatherings'
    
    def __str__(self): 
        return f'{self.gathering} - {self.user}: {self.role}'