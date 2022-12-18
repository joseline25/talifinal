from email.policy import default
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date, datetime, timedelta

# Create your models here.

# Instructor

class Instructor(models.Model):
    contract = (('Employee', 'Employee'), ('Freelancer', 'Freelancer'))
    devise = (('ILS', 'ILS'), ('EUR', 'EUR'), ('MUR', 'MUR'), ('CFA', 'CFA'), ('USD', 'USD'))

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    contract = models.CharField(choices=contract, max_length=200)
    devise = models.CharField(choices=devise, max_length=200)
    rate_course = models.IntegerField(default=0)
    rate_ta = models.IntegerField(default=0)
    rate_checker = models.IntegerField(default=0)
    rate_support = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name
    

# Course
  
class Course(models.Model):
    types = (('Course', 'Course'), ('TA', 'TA'), ('Checker', 'Checker'), ('Support', 'Support'))
    weeks = (('Week1', 'Week1'), ('Week2', 'Week2'), ('Week3', 'Week3'), ('Week4', 'Week4'), ('Week5', 'Week5'),
             ('Week6', 'Week6'), ('Week7', 'Week7'), ('Week8', 'Week8'), ('Week9', 'Week9'), ('Week10', 'Week10'),
             ('Week11', 'Week11'), ('Week12', 'Week12'), ('Week13', 'Week13'), ('Week14', 'Week14'),
             ('Week15', 'Week15'),
             ('Week16', 'Week16'), ('Week17', 'Week17'), ('Week18', 'Week18'), ('Week19', 'Week19'),
             ('Week20', 'Week20'),
             ('Week21', 'Week21'), ('Week22', 'Week22'), ('Week23', 'Week23'), ('Week24', 'Week24'),
             ('Week25', 'Week25'),
             ('Week26', 'Week26'), ('Week27', 'Week27'), ('Week28', 'Week28'), ('Week29', 'Week29'),
             ('Week30', 'Week30'))
    days = (('Day1', 'Day1'), ('Day2', 'Day2'), ('Day3', 'Day3'), ('Day4', 'Day4'), ('Day5', 'Day5'), ('Day6', 'Day6'),
            ('Day7', 'Day7'))
    moments = (('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'))

    week = models.CharField(choices=weeks, max_length=200)
    day = models.CharField(choices=days, max_length=200)
    moment = models.CharField(choices=moments, max_length=200)
    name_course = models.CharField(max_length=200)
    type_course = models.CharField(choices=types, max_length=200)
    hours = models.IntegerField()
    instructors = models.ManyToManyField(Instructor, related_name='courses', blank=True, null=True,
                                         through='InstructorProgram')

    def __str__(self):
        return self.name_course
    
    
    
# Structure

class Structure(models.Model):
    name_structure = models.CharField(max_length=200)
    courses = models.ManyToManyField(Course, related_name='structures', blank=True, null=True)

    def __str__(self):
        return self.name_structure



# Program 

class Program(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    confirmed = models.BooleanField(default=False)
    instructors = models.ManyToManyField(Instructor, through='InstructorProgram', related_name='programs', blank=True)

    # more fields for links and email
    google_meet_link = models.URLField(max_length = 200,blank=True)
    public_calendar = models.URLField(max_length = 200,blank=True)
    course_access = models.URLField(max_length = 200,blank=True)
    slack_room = models.URLField(max_length = 200,blank=True)
    link_attendance = models.URLField(max_length = 200,blank=True)
    email_program = models.URLField(max_length = 200,blank=True)
    
    
    def __str__(self):
        return self.name
    
    
    # return the list of weeks from Course model and from the calendar
    
    def program_date(self):
        
        if self.country == 'Israel':
            days_of_week = {'0': 'Sunday', '1': 'Monday', '2': 'Tuesday', '3': 'Wednesday', '4': 'Thursday',
                        '5': 'Friday', '6': 'Saturday'}
        else:
            
            days_of_week = {'0': 'Monday', '1': 'Tuesday', '2': 'Wednesday', '3': 'Thursday', '4': 'Friday',
                        '5': 'Saturday', '6': 'Sunday'}
        
        start_date = self.start_date
        end_date = self.end_date
        
        sd = datetime.strptime(str(start_date), '%Y-%m-%d')
        ed = datetime.strptime(str(end_date), '%Y-%m-%d')
        sd_day = str(start_date.weekday())
        ed_day = str(end_date.weekday())
        t = (sd.timetuple()[0], sd.timetuple()[1], sd.timetuple()[2])
        tab = [date(sd.timetuple()[0], sd.timetuple()[1], sd.timetuple()[2]).isocalendar().week,
               date(ed.timetuple()[0], ed.timetuple()[1], ed.timetuple()[2]).isocalendar().week, sd.timetuple()[0]]

        # calcul du nombre de semaines du programme
        # start_year_weeks = 52 ou 53!!!
        if start_date.year == end_date.year:
            total_nbr_weeks = tab[1] - tab[0] + 1
            
        else:
            start_year_weeks = date(start_date.year, 12, 31).isocalendar().week
            total_nbr_weeks = start_year_weeks - tab[0] + 1 + tab[1]
            

        tab_month = []
        if tab[1] > tab[0]:
            for i in range(tab[0], tab[1] + 1):
                tab_month.append(i)
        else:
            for i in range(tab[0], start_year_weeks + 1):
                tab_month.append(i)
            for i in range(1, tab[1] + 1):
                tab_month.append(i)

        weekss = []
        for val in Course.weeks:
            weekss.append(val[0])

        weeks = weekss[0:len(tab_month)]
        
        days_date = {}  # le dict de list pour chaque semaine de tab_month
        
        for i in tab_month:
            days_date[i] = []
            for j in range(1, 7):
                day = str(start_date.year) + "-W" + str(i) + "-" + str(j)
                r = datetime.strptime(day, "%Y-W%W-%w")
                days_date[i].append(days_of_week[str(r.date().weekday())] + ", " + str(r.date()))

        return (weeks, tab_month, days_date)
    
    
    def program_print(self):
        weeks, tab_month, days_date = self.program_date()
        #print(days_date)
        result = []
        
        week_courses_morning = []
        week_courses_afternoon = []
        week_courses_evening = []

        # print(week_courses)
        for i in weeks:
            index = weeks.index(i)
            val = tab_month[index]
            tab = days_date[val]
            tab1 = list(self.structure.courses.filter(week=str(i), moment='Morning'))  # .values('name_course')
            tab2 = list(self.structure.courses.filter(week=str(i), moment='Afternoon'))
            tab3 = list(self.structure.courses.filter(week=str(i), moment='Evening'))
            result.append(tab)
            week_courses_morning.append(tab1)
            week_courses_afternoon.append(tab2)
            week_courses_evening.append(tab3)
        # print(week_courses)
        return list(zip(weeks, result, week_courses_morning, week_courses_afternoon, week_courses_evening))

# Tasks for a program
class Task(models.Model):
    statuts = (('Waiting', 'Waiting'), ('Approved', 'Approved'), ('Pending', 'Pending'), ('Complete', 'Complete'))
    program = models.ForeignKey(Program, related_name='tasks', on_delete=models.CASCADE, null=True)
    name_task = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    added_date = models.DateField(auto_now_add=True)
    team = models.ManyToManyField(Instructor, related_name='tasks', blank=True)
    files = models.FileField(upload_to=None, max_length=254, blank=True)
    budget = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    statut = models.CharField(choices=statuts, max_length=50)
    
    def __str__(self):
        return self.name_task + ' ' + self.program.name
    


# ManytoMany class Instructor + Program


class InstructorProgram(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, blank=True, related_name='instructorfulltime')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    course_done = models.BooleanField(default=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)

    # Fo the date of a course

    #date = models.DateField(default=date.today)
    #week = models.CharField(max_length=200, blank=True)
    #week_number = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(53)])
    #day = models.CharField(max_length=200, blank=True)


    def __str__(self):
        return self.instructor.first_name + ' ' + self.course.name_course
    
    
    def set_moment(self):
        self.moment = self.course.moment
    
    # Compute salaries
    
    
    def salaires(self):
        if self.course.type_course == 'Course':
            val = self.instructor.rate_course * self.course.hours
        if self.course.type_course == 'TA':
            val = self.instructor.rate_ta * self.course.hours
        if self.course.type_course == 'Checker':
            val = self.instructor.rate_checker * self.course.hours
        if self.course.type_course == 'Support':
            val = self.instructor.rate_support * self.course.hours
        return val
    
# Courses's date for a Program


class ProgramDate(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    new_week = models.CharField( max_length=200, null=True)
    new_day = models.CharField( max_length=200, null=True)
    course_date = models.DateField(null=True)
    
    def __str__(self):
        return self.program.name + ' ' + self.program.structure.name_structure + ' ' + self.course.name_course
    
    
     
