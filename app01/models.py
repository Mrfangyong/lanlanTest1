from django.db import models

# Create your models here.
class User(models.Model):
    """ 用户表 """
    gender=(
        ("male","男"),
        ("famale","女"),
        )
    name=models.CharField(max_length=128,unique=True)
    password=models.CharField(max_length=256)
    email=models.EmailField(unique=True)
    sex=models.CharField(max_length=32,choices=gender,default="男")
    c_time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering=["c_time"]
        verbose_name="用户"
        verbose_name_plural="用户"
        
class content_table(models.Model):
    id=models.IntegerField(primary_key=True)
    content=models.TextField()
    action=models.CharField(max_length=225)
    translate=models.TextField()
    book_name=models.CharField(max_length=225)
    length=models.IntegerField()
    collection_nums=models.IntegerField()
    delete_flag=models.IntegerField()
    def __str__(self):
        return self.book_name   
    
    
class article_type_table(models.Model):
    id=models.IntegerField(primary_key=True)
    type_name=models.CharField(max_length=225)
    def __str__(self):
        return self.type_name
class crawler_data(models.Model):
    id=models.IntegerField(primary_key=True)
    contents=models.CharField(max_length=225)
    question=models.CharField(max_length=225)
    length=models.IntegerField()
    source=models.CharField(max_length=225)
    type_id=models.IntegerField()
    collection_nums=models.IntegerField()
    delete_flag=models.IntegerField()
    def __str__(self):
        return self.contents   
class history_table(models.Model):
    account=models.CharField(max_length=255)
    time=models.CharField(max_length=255)
    action=models.CharField(max_length=255)
    plate=models.CharField(max_length=255)
    def __str__(self):
        return self.account
    
    
# class relevant_word_search(models.Model):
#     words=models.CharField(max_length=225)
#     
class IMG(models.Model):
    img=models.ImageField(upload_to="img")
    name=models.CharField(max_length=20)
    first_name=models.CharField(max_length=20)
    def __str__(self):
        return self.name




