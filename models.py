from django.db import models

class Document(models.Model):
    CATEGORY_CHOICES = [
        ('SUM', 'สรุปบทเรียน'),
        ('EXAM', 'ข้อสอบเก่า'),
    ]
    
    # เพิ่มตัวเลือกหมวดหมู่วิชา
    SUBJECT_CHOICES = [
        ('MATH', 'คณิตศาสตร์'),
        ('SCI', 'วิทยาศาสตร์'),
        ('LANG', 'ภาษา'),
        ('COM', 'คอมพิวเตอร์'),
        ('SOC', 'สังคมศึกษา'),
    ]

    subject_code = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=4, choices=CATEGORY_CHOICES)
    
    # เพิ่มฟิลด์นี้เข้าไป
    subject_category = models.CharField(
        max_length=10, 
        choices=SUBJECT_CHOICES, 
        default='MATH'
    )
    
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/', null=True, blank=True) 
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_subject_category_display()}] {self.title}"