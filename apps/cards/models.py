from django.db import models
from django.utils.text import slugify
class Set(models.Model):
 name=models.CharField(max_length=160); slug=models.SlugField(unique=True,blank=True); description=models.TextField(blank=True); is_active=models.BooleanField(default=True); source_name=models.CharField(max_length=160,blank=True); source_url=models.URLField(blank=True); verified_at=models.DateTimeField(null=True,blank=True); verification_notes=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
 class Meta: ordering=("name",)
 def __str__(self): return self.name
 def save(self,*a,**k):
  if not self.slug:self.slug=slugify(self.name)
  super().save(*a,**k)
class CardQuerySet(models.QuerySet):
 def public(self): return self.filter(status=Card.Status.PUBLISHED,set__is_active=True)
class Card(models.Model):
 class CardType(models.TextChoices): LEGEND="LEGEND","Legend"; UNIT="UNIT","Unit"; PROGRAM="PROGRAM","Program"; GEAR="GEAR","Gear"
 class Status(models.TextChoices): DRAFT="DRAFT","Borrador"; REVIEWED="REVIEWED","Revisado"; PUBLISHED="PUBLISHED","Publicado"
 name=models.CharField(max_length=220); slug=models.SlugField(unique=True,blank=True); set=models.ForeignKey(Set,on_delete=models.PROTECT,related_name="cards"); card_type=models.CharField(max_length=10,choices=CardType.choices); status=models.CharField(max_length=10,choices=Status.choices,default=Status.DRAFT); collector_number=models.CharField(max_length=60,blank=True); cost=models.PositiveIntegerField(null=True,blank=True); rules_text=models.TextField(blank=True); ram=models.PositiveIntegerField(null=True,blank=True); power=models.PositiveIntegerField(null=True,blank=True); source_name=models.CharField(max_length=160,blank=True); source_url=models.URLField(blank=True); verified_at=models.DateTimeField(null=True,blank=True); verification_notes=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
 objects=CardQuerySet.as_manager()
 class Meta: ordering=("name",)
 def __str__(self): return self.name
 def save(self,*a,**k):
  if not self.slug:self.slug=slugify(self.name)
  super().save(*a,**k)
