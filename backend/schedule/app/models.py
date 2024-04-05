from django.db import models


class User(models.Model):
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Trainer(models.Model):
    GENDER = [
        ('man', 'мужчина'),
        ('women', 'Женщина')
    ]
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=GENDER, default='man')
    gyms = models.ManyToManyField('Gym')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Gym(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'

    def __str__(self):
        return self.name

class Schedule(models.Model):
    DAYS = [
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье')
    ]

    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    day = models.CharField(max_length=9, choices=DAYS, default='monday')
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'

    def __str__(self):
        return f"{self.trainer.first_name} {self.trainer.last_name} - {self.day} ({self.start_time}-{self.end_time})"

class Record(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        unique_together = ('trainer', 'schedule')

    def __str__(self):
        return f"{self.client} -> {self.trainer} -> {self.schedule}"
