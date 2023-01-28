from django.db import models

# Create your models here.

class Company(models.Model):
    # For some reasons unknown yet, Dennis didn't map the relationship betweeen Advocate and Company
    # But I expect it to be, One-t00many relationship i.e
    name = models.CharField(max_length=200)
    # Below is expected but above is given.
    # comName = models.CharField(Advocate, max_length=200)
    bio = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Advocate(models.Model):
    # And yes he later did add the relationship
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True )
    # XPLANATION OF TERMS
    # FOREIGNKEY: This establishes a one to many relationship, meaning an advocate can work in one company
    # on_delete=models.SET_NULL: This talks about what should happen to a relationship i.e Company when an 
    # advocate is deleted, SET_NULL means do nothing while CASCADE means delete.

    # Now I get, the relationship is such a way that the person's workplace must be linked with the person's profile
    name = models.CharField(max_length=500, null=True, blank=True)
    profile_pic = models.CharField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=500, null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)
    joined = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=250, null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.username
