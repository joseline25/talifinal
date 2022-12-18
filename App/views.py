from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import date, datetime, timedelta

# Create your views here.

def instructors_list(request):
    instructors = Instructor.objects.all()
    form = InstructorForm()
    context = {'instructors': instructors, 'form': form}  # , 'form': form

    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            country = form.cleaned_data['country']
            contract = form.cleaned_data['contract']
            devise = form.cleaned_data['devise']
            rate_course = form.cleaned_data['rate_course']
            rate_ta = form.cleaned_data['rate_ta']
            rate_checker = form.cleaned_data['rate_checker']
            rate_support = form.cleaned_data['rate_support']
            obj = Instructor(first_name=first_name, last_name=last_name, country=country, contract=contract,
                             devise=devise, rate_course=rate_course, rate_ta=rate_ta, rate_checker=rate_checker,
                             rate_support=rate_support)
            obj.save()
            return render(request, 'App/instructorslist.html', context)
        else:
            context['form'] = form
    return render(request, 'App/instructorslist.html', context)


def instructor_details(request, id):
    months = {'January':1,
              'February':2,
              'March':3,
              'April':4,
              'May':5,
              'June':6,
              'July':7,
              'August':8,
              'September':9,
              'October':10,
              'November':11,
              'December':12,}
    instructor = Instructor.objects.get(id=id)
    programs = InstructorProgram.objects.filter(instructor=instructor).values('program').distinct()
    courses = InstructorProgram.objects.filter(instructor=instructor)
    
    courses_program_date = []
    print(courses)
    for c in courses:
        print(c)
        object = ProgramDate.objects.get(program=c.program, course=c.course)
        
        print(object)
        courses_program_date.append(object)
    #instructor_calendar = 
    salaries = [x.salaires() for x in courses]
    total_salary = sum(salaries)
    context = {'instructor': instructor,
               'months': months,
               'courses': zip(courses_program_date, courses),
               'programs': programs,
               'total_salary': total_salary,
               'total': len(list(courses))}
    
    if request.method == "POST":
        month = request.POST.get("month")
        year = request.POST.get("year")
        context["month"] = month
        if not year:
            year = "2022"
        context["year"] = year
        val = InstructorProgram.objects.filter(instructor=instructor) # and date.month==months[month]
        object_val = []
        
        tab = []
        print(courses_program_date)
        for i in val:
            object = ProgramDate.objects.get(program=i.program, course=i.course)
            print(object.course_date.month)
            if object.course_date.month == months[month] and object.course_date.year == int(year):
                tab.append(i)
                object_val.append(object)
        context['tab'] = tab
        context['object_val'] = object_val
        context['search'] = zip(object_val, tab)
    

       
    return render(request, 'App/instructordetails.html', context)


def instructor_edit(request, id):
    instructor = Instructor.objects.get(id=id)
    form = InstructorForm(instance=instructor)

    if request.method == 'POST':
        form = InstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save()
            return redirect('App:instructorslist')

    context = {'form': form}
    return render(request, 'App/instructorslist.html', context)


def instructor_delete(request, id):
    instructor = Instructor.objects.get(id=id)
    context = {'instructor': instructor}
    if request.method == 'POST':
        instructor.delete()
        return redirect('App:instructors')
    return render(request, 'App/instructordelete.html', context)


# Structures

def structures_list(request):
    structures = Structure.objects.all()
    form = StructureForm()
    context = {'structures': structures, 'form': form}

    if request.method == 'POST':
        form = StructureForm(request.POST)
        if form.is_valid():
            name_structure = form.cleaned_data['name_structure']
            obj = Structure(name_structure=name_structure)
            obj.save()
            return render(request, 'App/structureslist.html', context)
        else:
            context['form'] = form
    return render(request, 'App/structureslist.html', context)


def structure_details(request, id):
    structure = Structure.objects.get(id=id)
    courses = structure.courses.all()
    form = CourseForm()
    context = {'structure': structure, 'courses': courses, 'form': form}

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            # form.save()
            week = form.cleaned_data['week']
            day = form.cleaned_data['day']
            moment = form.cleaned_data['moment']
            name_course = form.cleaned_data['name_course']
            type_course = form.cleaned_data['type_course']
            hours = form.cleaned_data['hours']
            context['formInfo'] = [week, day, moment, name_course, type_course, hours]
            obj = Course(week=week, day=day, moment=moment, name_course=name_course, type_course=type_course, hours=hours)
            obj.save()
            new_course = \
                Course.objects.filter(name_course=name_course, week=week, day=day, moment=moment, type_course=type_course,
                                              hours=hours)[0]
            structure.courses.add(new_course)
            return render(request, 'App/structuredetails.html', context)
        else:
            context['form'] = CourseForm()
    return render(request, 'App/structuredetails.html', context)


def structure_edit(request, id):
    structure = Structure.objects.get(id=id)
    form = StructureForm(instance=structure)

    if request.method == 'POST':
        form = StructureForm(request.POST, instance=structure)
        if form.is_valid():
            form.save()
            return redirect('App:structureslist')

    context = {'form': form}
    return render(request, 'App/structureslist.html', context)


def structure_delete(request, id):
    structure = Structure.objects.get(id=id)
    context = {'structure': structure}
    if request.method == 'POST':
        structure.delete()
        return redirect('App:structureslist')
    return render(request, 'App/structuredelete.html', context)


#  Courses

def courses_list(request):
    courses = Course.objects.all().distinct()
    context ={
        'courses': courses,
    }
    return render(request, 'App/courseslist.html', context)


def course_edit(request, id, pk):
    course = Course.objects.get(id=id)
    structure = Structure.objects.get(pk=pk)
    form = CourseForm(instance=course)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('App:structuredetails', id=pk)

    context = {
        'structure': structure,
        'form': form
        }
    return render(request, 'App/structuredetails.html', context)


def course_delete(request, id, pk):
    course = Course.objects.get(id=id)
    structure = Structure.objects.get(pk=pk)
    context = {'course': course,
               'structure': structure,
               }
    if request.method == 'POST':
        course.delete()
        return redirect('App:structuredetails', id=pk)
    return render(request, 'App/coursedelete.html', context)



# Programs

def programs_list(request):
    programs = Program.objects.all()
    form = ProgramForm()
    context = {'programs': programs,
               'form': form}
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            form.save()
            return render(request, 'App/programslist.html', context)
    else:
        context['form'] = ProgramForm()
    return render(request, 'App/programslist.html', context)


def program_details(request, id):
    
    day_week = { 'Day1' : 0, 'Day2' : 1, 'Day3' : 2, 'Day4' : 3, 'Day5' : 4,
                        'Day6' : 5, 'Day7' : 6}
    
    program = Program.objects.get(id=id)

    
    # je récupère tous les cours de ce programme et je les copie dans le model ProgramDate
    
    courses_to_copy = program.structure.courses.all()
    courses_actual = ProgramDate.objects.filter(program=program).distinct()
    courses_actuals = []
    for object in courses_actual:
        courses_actuals.append(object.course)
    
    for course in courses_to_copy:
        if course not in courses_actuals:
            index_week = program.program_date()[0].index(course.week)
            # get the week number in calendar
            index_calendar = program.program_date()[1][index_week]
           
            # get the weekday
            day = day_week[course.day]
            
            if day != 0:
                index_calendar += 1
            # get the year
            if index_calendar < program.program_date()[1][0]:
                year = program.end_date.year
            else:
                year = program.start_date.year
                
            my_date = str(year) + ' ' + str(index_calendar) + ' ' + str(day)
            
            print(program.start_date.weekday())
            
            if program.country == 'Israel' and program.start_date.weekday() == 0:
                
                my_date_calendar = datetime.strptime(my_date, "%Y %W %w") - timedelta(days=1)
                
            elif program.country == 'Israel' and program.start_date.weekday() == 6:
                my_date_calendar = datetime.strptime(my_date, "%Y %W %w") 
                
            else:
    
                my_date_calendar = datetime.strptime(my_date, "%Y %W %w") - timedelta(days=6)
                
            
            object = ProgramDate(program=program, course=course, new_week=course.week, new_day=course.day, course_date=my_date_calendar.date())
            object.save()
    
    # fin de la copie!
   
    
    printing = program.program_print()
    
    tab_weeks, tab_weeks_calendar, dates = program.program_date()
    start_date = program.start_date
    end_date = program.end_date
    weeks, tab_month, days_date = program.program_date()
    
    
    
    # recalcul de days_date
    
    courses_actual = ProgramDate.objects.filter(program=program, course__moment__contains = 'Morning').distinct()
    

    
    days_date = {}
    for val in program.program_date()[1]:
        tab = []
        index_val = program.program_date()[1].index(val)
        intermediary_val = program.program_date()[0][index_val]
        index_week = program.program_date()[0].index(intermediary_val)
        
        for d in ['Day1', 'Day2', 'Day3', 'Day4', 'Day5','Day6', 'Day7']:
            liste =  ProgramDate.objects.filter(program=program, new_week=program.program_date()[0][index_week], new_day=d, course__moment__contains='Morning')
            
            if len(liste)>0 :  
                object = liste[0] 
                
                """
                if program.country == 'Israel' and program.start_date.weekday() == 6:
                    
                    tab.append(object.course_date)
                else:
                    tab.append(object.course_date - timedelta(days=1))
                """
                tab.append(object.course_date)
            else:
                
                tab.append(' ')
        
        days_date[val] = tab
    
    
    days_date_tab = []
    for i in tab_month:
        days_date_tab.append(days_date[i])

    date_row1 = []
    date_row2 = []
    date_row3 = []
    date_row4 = []
    date_row5 = []
    for i in days_date_tab:
        date_row1.append(i[0])
        date_row2.append(i[1])
        date_row3.append(i[2])
        date_row4.append(i[3])
        date_row5.append(i[4])
    tab_d = [date_row1, date_row2, date_row3, date_row4, date_row5]
    

    # gestion des dates

    weekss = []
    for val in Course.weeks:
        weekss.append(val[0])

    weeks = weekss[0:len(tab_month)]
    # print(weeks)

    days = ['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7']
    moments = ['Morning', 'Afternoon', 'Evening']

    dayone_morning = program.structure.courses.filter(day='Day1', moment='Morning').order_by('week')
    tab1 = []
    for w in weeks:
        val = []
        for d in dayone_morning:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tab1.append(' ')
        else:
            tab1.append(val[0])
   
    daytwo_morning = program.structure.courses.filter(day='Day2', moment='Morning').order_by('week')
    tab2 = []
    for w in weeks:
        val = []
        for d in daytwo_morning:
            if d.week == w:
                #tab2.append(d)
                val.append(d)
        if len(val) == 0:
            tab2.append(' ')
        else:
            tab2.append(val[0])
    
    daythree_morning = program.structure.courses.filter(day='Day3', moment='Morning').order_by('week')
    tab3 = []
    for w in weeks:
        val = []
        for d in daythree_morning:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tab3.append(' ')
        else:
            tab3.append(val[0])

    dayfour_morning = program.structure.courses.filter(day='Day4', moment='Morning').order_by('week')
    tab4 = []
    for w in weeks:
        val = []
        for d in dayfour_morning:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tab4.append(' ')
        else:
            tab4.append(val[0])

    dayfive_morning = program.structure.courses.filter(day='Day5', moment='Morning').order_by('week')
    tab5 = []
    for w in weeks:
        val = []
        for d in dayfive_morning:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tab5.append(' ')
        else:
            tab5.append(val[0])

    daysix_morning = program.structure.courses.filter(day='Day6', moment='Morning').order_by('week')
    tab6 = []
    for w in weeks:
        val = []
        for d in daysix_morning:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tab6.append(' ')
        else:
            tab6.append(val[0])

    dayseven_morning = program.structure.courses.filter(day='Day7', moment='Morning').order_by('week')
    tab7 = []
    for w in weeks:
        val = []
        for d in dayseven_morning:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tab7.append(' ')
        else:
            tab7.append(val[0])
                
    
    dayone_afternoon = program.structure.courses.filter(day='Day1', moment='Afternoon').order_by('week')
    tabb1 = []
    for w in weeks:
        val = []
        for d in dayone_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb1.append(' ')
        else:
            tabb1.append(val[0])
    
            
    dayone_evening = program.structure.courses.filter(day='Day1', moment='Evening').order_by('week')
    tabbb1 = []
    for w in weeks:
        val = []
        for d in dayone_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb1.append(' ')
        else:
            tabbb1.append(val[0])
                
                
    daytwo_afternoon = program.structure.courses.filter(day='Day2', moment='Afternoon').order_by('week')
    tabb2 = []
    for w in weeks:
        val = []
        for d in daytwo_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb2.append(' ')
        else:
            tabb2.append(val[0])
                
    daytwo_evening = program.structure.courses.filter(day='Day2', moment='Evening').order_by('week')
    tabbb2 = []
    for w in weeks:
        val = []
        for d in daytwo_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb2.append(' ')
        else:
            tabbb2.append(val[0])
                
    daythree_afternoon = program.structure.courses.filter(day='Day3', moment='Afternoon').order_by('week')
    tabb3 = []
    for w in weeks:
        val = []
        for d in daythree_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb3.append(' ')
        else:
            tabb3.append(val[0])
                
    daythree_evening = program.structure.courses.filter(day='Day3', moment='Evening').order_by('week')
    tabbb3 = []
    for w in weeks:
        val = []
        for d in daythree_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb3.append(' ')
        else:
            tabbb3.append(val[0])
    
    
    dayfour_afternoon = program.structure.courses.filter(day='Day4', moment='Afternoon').order_by('week')
    tabb4 = []
    for w in weeks:
        val = []
        for d in dayfour_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb4.append(' ')
        else:
            tabb4.append(val[0])
                
    dayfour_evening = program.structure.courses.filter(day='Day4', moment='Evening').order_by('week')
    tabbb4 = []
    for w in weeks:
        val = []
        for d in dayfour_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb4.append(' ')
        else:
            tabbb4.append(val[0])
    
    
    dayfive_afternoon = program.structure.courses.filter(day='Day5', moment='Afternoon').order_by('week')
    tabb5 = []
    for w in weeks:
        val = []
        for d in dayfive_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb5.append(' ')
        else:
            tabb5.append(val[0])
                
    dayfive_evening = program.structure.courses.filter(day='Day5', moment='Evening').order_by('week')
    tabbb5 = []
    for w in weeks:
        val = []
        for d in dayfive_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb5.append(' ')
        else:
            tabbb5.append(val[0])
    
    
    daysix_afternoon = program.structure.courses.filter(day='Day6', moment='Afternoon').order_by('week')
    tabb6 = []
    for w in weeks:
        val = []
        for d in daysix_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb6.append(' ')
        else:
            tabb6.append(val[0])
                
    daysix_evening = program.structure.courses.filter(day='Day6', moment='Evening').order_by('week')
    tabbb6 = []
    for w in weeks:
        val = []
        for d in daysix_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb6.append(' ')
        else:
            tabbb6.append(val[0])
            
    
    dayseven_afternoon = program.structure.courses.filter(day='Day7', moment='Afternoon').order_by('week')
    tabb7 = []
    for w in weeks:
        val = []
        for d in dayseven_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb7.append(' ')
        else:
            tabb7.append(val[0])
                
    dayseven_evening = program.structure.courses.filter(day='Day7', moment='Evening').order_by('week')
    tabbb7 = []
    for w in weeks:
        val = []
        for d in dayseven_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb7.append(' ')
        else:
            tabbb7.append(val[0])
                
   
    
    
    tab_d = [zip(tab1, date_row1), zip(tab2, date_row2), zip(tab3, date_row3), zip(tab4, date_row4),
             zip(tab5, date_row5)]
    tab_d_afternoon = [tabb1, tabb2, tabb3, tabb4, tabb5, tabb6, tabb7]
    tab_d_evening = [tabbb1, tabbb2, tabbb3, tabbb4, tabbb5, tabbb6, tabbb7]
    
    instructors = Instructor.objects.all()

    context = {'program': program,
               'printing': printing,
               'start_year': start_date.year,
               'end_year': end_date.year,
               'weeks': weeks,
               'days': days,
               'moments': moments,
               'row1': tab1,
               'row2': tab2,
               'row3': tab3,
               'row4': tab4,
               'row5': tab5,
               'row6': tab6,
               'row7': tab7,
               'instructors': instructors,
               'tab_month': tab_month,
               'tab_d': tab_d,
               'tab_d_afternoon': tab_d_afternoon,
               'tab_d_evening': tab_d_evening,
               }
   
    
    """ récupération des valeurs du formulaire lors du choix des instructeurs par les tags 
    select et stockage dans un dictionnaire """

    program_instructors = InstructorProgram.objects.filter(program=program)#.values_list('instructor', flat=True).distinct()
    program_instructorss = InstructorProgram.objects.filter(program=program).values_list('instructor', flat=True).distinct()
    
    
    context['program_instructors'] = program_instructors
    context['program_instructorss'] = program_instructorss
    Instructorss = program.instructors.all().distinct()
    context['Instructorss'] = Instructorss 
    
    if request.method == "POST":
        a = {}
        salaires = {}
        for j in range(1, len(days) + 1):
            for i in range(1, len(weeks) + 1):
                key_morning = 'Week' + str(i) + 'Day' + str(j) + 'morning'
                key_afternoon = 'Week' + str(i) + 'Day' + str(j) + 'afternoon'
                key_evening = 'Week' + str(i) + 'Day' + str(j) + 'evening'
                
                
                if key_morning:
                    value = request.POST.get(key_morning)
                    a[key_morning] = value
                    key =key_morning
                elif key_afternoon:
                    value = request.POST.get(key_afternoon)
                    a[key_afternoon] = value
                    key = key_afternoon
                elif key_evening:
                    value = request.POST.get(key_evening)
                    a[key_evening] = value
                    key = key_evening
                
                search = Instructor.objects.filter(first_name__contains=a[key])
                
                if len(search) != 0:
                    
                    if key_morning:
                        course = program.structure.courses.filter(day='Day' + str(j), week='Week' + str(i), moment='Morning')
                    elif key_afternoon:
                        course = program.structure.courses.filter(day='Day' + str(j), week='Week' + str(i), moment='Afternoon')
                    elif key_evening:
                        course = program.structure.courses.filter(day='Day' + str(j), week='Week' + str(i), moment='Evening')
                        
                    index = tab_weeks.index(course[0].week)
                    
                    val = tab_weeks_calendar[index]
                    
                  
                    
                    day = course[0].day

                    object = InstructorProgram(instructor=search[0], course=course[0],
                                                date_added=datetime.now(), course_done=True, program=program)  # ,hours=course[0].hours+3
                    
                    object.set_moment() 
                    previous = InstructorProgram.objects.filter(instructor=search[0], course=course[0],
                                                                 program=program)
                    previous_instructor = InstructorProgram.objects.filter(course=course[0], program=program)
                    if len(previous_instructor) > 0:
                        previous_instructor[0].delete()
                    #if not (previous.exists() or previous_instructor.exists()):
                    object.save()

                    context['list_instructors'] = a
                    context['salaires'] = salaires
        program_courses_date = InstructorProgram.objects.filter(program=program).values('course').distinct()
        context['program_courses_date'] = program_courses_date
       
        program_instructors = InstructorProgram.objects.filter(program=program)#.values_list('instructor', flat=True).distinct()
        program_instructorss = InstructorProgram.objects.filter(program=program).values_list('instructor', flat=True).distinct()
        Instructorss = []
        for i in program_instructorss:
            val = Instructor.objects.get(id=i)
            Instructorss.append(val)
        context['program_instructors'] = program_instructors
        context['program_instructorss'] = program_instructorss
        context['Instructorss'] = Instructorss
        
        objts = InstructorProgram.objects.all()
        
        for val in objts:
            for i in program.program_print():
                for j in i[2]:
                    if val.course == j:
                        position = i[2].index(j)
                        val.week = i[0]
                        val.save()
                        datt = datetime.strptime(i[1][position].split(", ")[1], "%Y-%m-%d").date()
                        val.date = datt
                        val.save()
        #print("bonjour1", program.country)
        return render(request, 'App/programdetails.html', context)
    #print("bonjour2",program.country)

    return render(request, 'App/programdetails.html', context)


def program_edit(request, id):
    program = Program.objects.get(id=id)
    form = ProgramForm(instance=program)

    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('App:programslist')

    context = {'form': form}
    return render(request, 'App/programslist.html', context)



def program_delete(request, id):
    program = Program.objects.get(id=id)
    context = {'program': program}
    if request.method == 'POST':
        program.delete()
        return redirect('App:programslist')
    return render(request, 'App/programdelete.html', context)




def proginsdetails(request, id, pk):
    instructor = Instructor.objects.get(id=pk)
    program = Program.objects.get(pk=id) 
    courses = InstructorProgram.objects.filter(program=program, instructor=instructor)
    courses_id = InstructorProgram.objects.filter(program=program, instructor=instructor).values_list('course', flat=True).distinct()
    print(courses_id)
    courses_dates = []
    for i in courses_id:
        print(ProgramDate.objects.get(program=program, course__id=i).course_date)
        courses_dates.append(ProgramDate.objects.get(program=program, course__id=i))
    courses_combined = zip(courses, courses_dates)
    
    start_date = program.start_date
    end_date = program.end_date
    sd = datetime.strptime(str(start_date), '%Y-%m-%d')
    ed = datetime.strptime(str(end_date), '%Y-%m-%d')
    sd_day = str(start_date.weekday())
    ed_day = str(end_date.weekday())

    tab = [date(sd.timetuple()[0], sd.timetuple()[1], sd.timetuple()[2]).isocalendar().week,
           date(ed.timetuple()[0], ed.timetuple()[1], ed.timetuple()[2]).isocalendar().week, sd.timetuple()[0]]
    tab_month = []
    for i in range(tab[0], tab[1] + 1):
        tab_month.append(i)

    weekss = []
    for val in Course.weeks:
        weekss.append(val[0])

    weeks = weekss[0:len(tab_month)]
    days_of_week = {'0': 'Monday',
                    '1': 'Tuesday',
                    '2': 'Wednesday',
                    '3': 'Thursday',
                    '4': 'Friday',
                    '5': 'Saturday',
                    '6': 'Sunday'}

    val = 0
    tab_week = []
    #print("the courses are :")
    #print(courses)
    for c in courses:
        #print(c)
        val += c.salaires()
        #print(c['coursefulltime'])
        tab_week.append(c.course.week)

    dico = {}
    for i in weeks:
        key = i
        value = 'Week' + str(tab_month[weeks.index(i)])
        dico[key] = value

    weeks_year = []
    #for i in tab_week:
        #weeks_year.append(dico[i])
        # weeks_year.append(int(dico[i][4:]))

    context = {'instructor': instructor,
               'program': program,
               'start_month': datetime.strptime(str(program.start_date.month), "%m").strftime("%B"),
               'end_month': datetime.strptime(str(program.end_date.month), "%m").strftime("%B"),
               'courses': courses,
               'courses_combined': courses_combined,
               'total_salary': val,
               'tab_month': tab_month,
               'days_of_week': days_of_week,
               'sd_day': days_of_week[sd_day],
               'ed_day': days_of_week[ed_day],
               'weeks': weeks,
               'weekss': weekss,
               'tab_week': tab_week,
               'dico': dico,
               'weeks_year': weeks_year, }
    return render(request, 'App/programinstructordetails.html', context)



def modify_prog_calendar(request, id):
    program = Program.objects.get(id=id)
    program_elements = ProgramDate.objects.filter(program=program)
    
    form = ProgramDateForm()
    
    context = {'program': program,
               'program_elements': program_elements,
               'form' : form,
               }
        
    return render(request, 'App/programcalendarmodify.html', context)



def program_date_edit(request, id, pk):
    program_date = ProgramDate.objects.get(id=id)
    program = Program.objects.get(pk=pk)
    form = ProgramDateForm(instance=program_date)
    program_elements = [program_date]
    
    program_date_actual_date = program_date.course_date
    print(program_date_actual_date)
    
    if request.method == 'POST':
        form = ProgramDateForm(request.POST, instance=program_date)
        if form.is_valid():
            course_date = form.cleaned_data['course_date']
            print(course_date)
            date_difference = course_date - program_date_actual_date
            print(date_difference.days)
            
            courses_tab = list(ProgramDate.objects.filter(program=program).order_by('course_date'))
            print(courses_tab)
            index = courses_tab.index(program_date)
            print(index)
            if date_difference.days >= 0:
                for element in courses_tab[index + 1:]:
                    print(element.course_date)
                    element.course_date += timedelta(days=date_difference.days)
                    element.save()
            else:
                for element in courses_tab[index + 1:]:
                    print(element.course_date)
                    element.course_date += timedelta(days=date_difference.days) 
                    element.save()    
            form.save()
            return redirect('App:programdetails', id=pk)
    context = {
            'program_elements': program_elements,
            'program': program,
            'form': form,
        }
    return render(request, 'App/programcalendarmodify.html', context)


# Program details test for instructors printing

def programdetailstest(request, id):
    day_week = { 'Day1' : 0, 'Day2' : 1, 'Day3' : 2, 'Day4' : 3, 'Day5' : 4,
                        'Day6' : 5, 'Day7' : 6}
    
    program = Program.objects.get(id=id)

    
    # je récupère tous les cours de ce programme et je les copie dans le model ProgramDate
    
    courses_to_copy = program.structure.courses.all()
    courses_actual = ProgramDate.objects.filter(program=program).distinct()
    courses_actuals = []
    for object in courses_actual:
        courses_actuals.append(object.course)
    
    for course in courses_to_copy:
        if course not in courses_actuals:
            index_week = program.program_date()[0].index(course.week)
            # get the week number in calendar
            index_calendar = program.program_date()[1][index_week]
           
            # get the weekday
            day = day_week[course.day]
            
            if day != 0:
                index_calendar += 1
            # get the year
            if index_calendar < program.program_date()[1][0]:
                year = program.end_date.year
            else:
                year = program.start_date.year
                
            my_date = str(year) + ' ' + str(index_calendar) + ' ' + str(day)
            
            print(program.start_date.weekday())
            
            if program.country == 'Israel' and program.start_date.weekday() == 0:
                
                my_date_calendar = datetime.strptime(my_date, "%Y %W %w") - timedelta(days=1)
                
            elif program.country == 'Israel' and program.start_date.weekday() == 6:
                my_date_calendar = datetime.strptime(my_date, "%Y %W %w") 
                
            else:
    
                my_date_calendar = datetime.strptime(my_date, "%Y %W %w") - timedelta(days=6)
                
            
            object = ProgramDate(program=program, course=course, new_week=course.week, new_day=course.day, course_date=my_date_calendar.date())
            object.save()
    
    # fin de la copie!
   
    
    printing = program.program_print()
    
    tab_weeks, tab_weeks_calendar, dates = program.program_date()
    start_date = program.start_date
    end_date = program.end_date
    weeks, tab_month, days_date = program.program_date()
    
    
    
    # recalcul de days_date
    
    courses_actual = ProgramDate.objects.filter(program=program, course__moment__contains = 'Morning').distinct()
    

    
    days_date = {}
    for val in program.program_date()[1]:
        tab = []
        index_val = program.program_date()[1].index(val)
        intermediary_val = program.program_date()[0][index_val]
        index_week = program.program_date()[0].index(intermediary_val)
        
        for d in ['Day1', 'Day2', 'Day3', 'Day4', 'Day5','Day6', 'Day7']:
            liste =  ProgramDate.objects.filter(program=program, new_week=program.program_date()[0][index_week], new_day=d, course__moment__contains='Morning')
            
            if len(liste)>0 :  
                object = liste[0] 
                
                """
                if program.country == 'Israel' and program.start_date.weekday() == 6:
                    
                    tab.append(object.course_date)
                else:
                    tab.append(object.course_date - timedelta(days=1))
                """
                tab.append(object.course_date)
            else:
                
                tab.append(' ')
        
        days_date[val] = tab
    
    
    days_date_tab = []
    for i in tab_month:
        days_date_tab.append(days_date[i])

    date_row1 = []
    date_row2 = []
    date_row3 = []
    date_row4 = []
    date_row5 = []
    for i in days_date_tab:
        date_row1.append(i[0])
        date_row2.append(i[1])
        date_row3.append(i[2])
        date_row4.append(i[3])
        date_row5.append(i[4])
    tab_d = [date_row1, date_row2, date_row3, date_row4, date_row5]
    

    # gestion des dates

    weekss = []
    for val in Course.weeks:
        weekss.append(val[0])

    weeks = weekss[0:len(tab_month)]
    # print(weeks)

    days = ['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7']
    moments = ['Morning', 'Afternoon', 'Evening']

    dayone_morning = program.structure.courses.filter(day='Day1', moment='Morning').order_by('week')
    tab1 = []
    for w in weeks:
        val = []
        for d in dayone_morning:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tab1.append(' ')
        else:
            tab1.append(val[0])
   
    daytwo_morning = program.structure.courses.filter(day='Day2', moment='Morning').order_by('week')
    tab2 = []
    for w in weeks:
        val = []
        for d in daytwo_morning:
            if d.week == w:
                #tab2.append(d)
                val.append(d)
        if len(val) == 0:
            tab2.append(' ')
        else:
            tab2.append(val[0])
    
    daythree_morning = program.structure.courses.filter(day='Day3', moment='Morning').order_by('week')
    tab3 = []
    for w in weeks:
        val = []
        for d in daythree_morning:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tab3.append(' ')
        else:
            tab3.append(val[0])

    dayfour_morning = program.structure.courses.filter(day='Day4', moment='Morning').order_by('week')
    tab4 = []
    for w in weeks:
        val = []
        for d in dayfour_morning:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tab4.append(' ')
        else:
            tab4.append(val[0])

    dayfive_morning = program.structure.courses.filter(day='Day5', moment='Morning').order_by('week')
    tab5 = []
    for w in weeks:
        val = []
        for d in dayfive_morning:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tab5.append(' ')
        else:
            tab5.append(val[0])

    daysix_morning = program.structure.courses.filter(day='Day6', moment='Morning').order_by('week')
    tab6 = []
    for w in weeks:
        val = []
        for d in daysix_morning:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tab6.append(' ')
        else:
            tab6.append(val[0])

    dayseven_morning = program.structure.courses.filter(day='Day7', moment='Morning').order_by('week')
    tab7 = []
    for w in weeks:
        val = []
        for d in dayseven_morning:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tab7.append(' ')
        else:
            tab7.append(val[0])
                
    
    dayone_afternoon = program.structure.courses.filter(day='Day1', moment='Afternoon').order_by('week')
    tabb1 = []
    for w in weeks:
        val = []
        for d in dayone_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb1.append(' ')
        else:
            tabb1.append(val[0])
    
            
    dayone_evening = program.structure.courses.filter(day='Day1', moment='Evening').order_by('week')
    tabbb1 = []
    for w in weeks:
        val = []
        for d in dayone_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb1.append(' ')
        else:
            tabbb1.append(val[0])
                
                
    daytwo_afternoon = program.structure.courses.filter(day='Day2', moment='Afternoon').order_by('week')
    tabb2 = []
    for w in weeks:
        val = []
        for d in daytwo_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb2.append(' ')
        else:
            tabb2.append(val[0])
                
    daytwo_evening = program.structure.courses.filter(day='Day2', moment='Evening').order_by('week')
    tabbb2 = []
    for w in weeks:
        val = []
        for d in daytwo_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb2.append(' ')
        else:
            tabbb2.append(val[0])
                
    daythree_afternoon = program.structure.courses.filter(day='Day3', moment='Afternoon').order_by('week')
    tabb3 = []
    for w in weeks:
        val = []
        for d in daythree_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb3.append(' ')
        else:
            tabb3.append(val[0])
                
    daythree_evening = program.structure.courses.filter(day='Day3', moment='Evening').order_by('week')
    tabbb3 = []
    for w in weeks:
        val = []
        for d in daythree_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb3.append(' ')
        else:
            tabbb3.append(val[0])
    
    
    dayfour_afternoon = program.structure.courses.filter(day='Day4', moment='Afternoon').order_by('week')
    tabb4 = []
    for w in weeks:
        val = []
        for d in dayfour_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb4.append(' ')
        else:
            tabb4.append(val[0])
                
    dayfour_evening = program.structure.courses.filter(day='Day4', moment='Evening').order_by('week')
    tabbb4 = []
    for w in weeks:
        val = []
        for d in dayfour_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb4.append(' ')
        else:
            tabbb4.append(val[0])
    
    
    dayfive_afternoon = program.structure.courses.filter(day='Day5', moment='Afternoon').order_by('week')
    tabb5 = []
    for w in weeks:
        val = []
        for d in dayfive_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb5.append(' ')
        else:
            tabb5.append(val[0])
                
    dayfive_evening = program.structure.courses.filter(day='Day5', moment='Evening').order_by('week')
    tabbb5 = []
    for w in weeks:
        val = []
        for d in dayfive_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb5.append(' ')
        else:
            tabbb5.append(val[0])
    
    
    daysix_afternoon = program.structure.courses.filter(day='Day6', moment='Afternoon').order_by('week')
    tabb6 = []
    for w in weeks:
        val = []
        for d in daysix_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb6.append(' ')
        else:
            tabb6.append(val[0])
                
    daysix_evening = program.structure.courses.filter(day='Day6', moment='Evening').order_by('week')
    tabbb6 = []
    for w in weeks:
        val = []
        for d in daysix_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb6.append(' ')
        else:
            tabbb6.append(val[0])
            
    
    dayseven_afternoon = program.structure.courses.filter(day='Day7', moment='Afternoon').order_by('week')
    tabb7 = []
    for w in weeks:
        val = []
        for d in dayseven_afternoon:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabb7.append(' ')
        else:
            tabb7.append(val[0])
                
    dayseven_evening = program.structure.courses.filter(day='Day7', moment='Evening').order_by('week')
    tabbb7 = []
    for w in weeks:
        val = []
        for d in dayseven_evening:
            if d.week == w:
                val.append(d)
        if len(val) == 0:
            tabbb7.append(' ')
        else:
            tabbb7.append(val[0])
                
   
    
    
    tab_d = [zip(tab1, date_row1), zip(tab2, date_row2), zip(tab3, date_row3), zip(tab4, date_row4),
             zip(tab5, date_row5)]
    tab_d_afternoon = [tabb1, tabb2, tabb3, tabb4, tabb5, tabb6, tabb7]
    tab_d_evening = [tabbb1, tabbb2, tabbb3, tabbb4, tabbb5, tabbb6, tabbb7]
    
   
    instructors = Instructor.objects.all()
    status = ['Waiting', 'Approved', 'Pending', 'Complete']
    context = {'program': program,
               'printing': printing,
               'status': status,
               'start_year': start_date.year,
               'end_year': end_date.year,
               'weeks': weeks,
               'days': days,
               'moments': moments,
               'row1': tab1,
               'row2': tab2,
               'row3': tab3,
               'row4': tab4,
               'row5': tab5,
               'row6': tab6,
               'row7': tab7,
               'instructors': instructors,
               'tab_month': tab_month,
               'tab_d': tab_d,
               'tab_d_afternoon': tab_d_afternoon,
               'tab_d_evening': tab_d_evening,
               }
   
    
    """ récupération des valeurs du formulaire lors du choix des instructeurs par les tags 
    select et stockage dans un dictionnaire """

    program_instructors = InstructorProgram.objects.filter(program=program)#.values_list('instructor', flat=True).distinct()
    program_instructorss = InstructorProgram.objects.filter(program=program).values_list('instructor', flat=True).distinct()
    
    
    context['program_instructors'] = program_instructors
    context['program_instructorss'] = program_instructorss
    Instructorss = program.instructors.all().distinct()
    context['Instructorss'] = Instructorss 
    
    
    
    # Ajout des instructeurs pour zipper tab_d
        
    dayone_morning =  InstructorProgram.objects.filter(program=program, course__day='Day1', course__moment='Morning')
    tab1_i = []
    for w in weeks:
        val = []
        for d in dayone_morning:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tab1_i.append(' ')
        else:
            tab1_i.append(val[0])
    
    daytwo_morning =  InstructorProgram.objects.filter(program=program, course__day='Day2', course__moment='Morning')
    tab2_i = []
    for w in weeks:
        val = []
        for d in daytwo_morning:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tab2_i.append(' ')
        else:
            tab2_i.append(val[0])
    print(tab2_i)
    
    daythree_morning =  InstructorProgram.objects.filter(program=program, course__day='Day3', course__moment='Morning')
    tab3_i = []
    for w in weeks:
        val = []
        for d in daythree_morning:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tab3_i.append(' ')
        else:
            tab3_i.append(val[0])
    
    dayfour_morning =  InstructorProgram.objects.filter(program=program, course__day='Day4', course__moment='Morning')
    tab4_i = []
    for w in weeks:
        val = []
        for d in dayfour_morning:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tab4_i.append(' ')
        else:
            tab4_i.append(val[0])
    
    
    dayfive_morning =  InstructorProgram.objects.filter(program=program, course__day='Day5', course__moment='Morning')
    tab5_i = []
    for w in weeks:
        val = []
        for d in dayfive_morning:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tab5_i.append(' ')
        else:
            tab5_i.append(val[0])
    
    
    daysix_morning =  InstructorProgram.objects.filter(program=program, course__day='Day6', course__moment='Morning')
    tab6_i = []
    for w in weeks:
        val = []
        for d in daysix_morning:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tab6_i.append(' ')
        else:
            tab6_i.append(val[0])
    
    
    dayseven_morning =  InstructorProgram.objects.filter(program=program, course__day='Day7', course__moment='Morning')
    tab7_i = []
    for w in weeks:
        val = []
        for d in dayseven_morning:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tab7_i.append(' ')
        else:
            tab7_i.append(val[0])
    
    tab_dd = [zip(tab1, date_row1, tab1_i), zip(tab2, date_row2, tab2_i), zip(tab3, date_row3, tab3_i), zip(tab4, date_row4, tab4_i),
             zip(tab5, date_row5, tab5_i)]
    context['tab_dd']=tab_dd
    
    
    # for afternoon
    
    dayone_afternoon =  InstructorProgram.objects.filter(program=program, course__day='Day1', course__moment='Afternoon')
    tabb1_i = []
    for w in weeks:
        val = []
        for d in dayone_afternoon:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabb1_i.append(' ')
        else:
            tabb1_i.append(val[0])
    print("day on in the afternoon")
    print(tabb1_i)
            
    daytwo_afternoon =  InstructorProgram.objects.filter(program=program, course__day='Day2', course__moment='Afternoon')
    tabb2_i = []
    for w in weeks:
        val = []
        for d in daytwo_afternoon:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabb2_i.append(' ')
        else:
            tabb2_i.append(val[0])
            
    daythree_afternoon =  InstructorProgram.objects.filter(program=program, course__day='Day3', course__moment='Afternoon')
    tabb3_i = []
    for w in weeks:
        val = []
        for d in daythree_afternoon:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabb3_i.append(' ')
        else:
            tabb3_i.append(val[0])
    
    
    dayfour_afternoon =  InstructorProgram.objects.filter(program=program, course__day='Day4', course__moment='Afternoon')
    tabb4_i = []
    for w in weeks:
        val = []
        for d in dayfour_afternoon:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabb4_i.append(' ')
        else:
            tabb4_i.append(val[0])
            
    dayfive_afternoon =  InstructorProgram.objects.filter(program=program, course__day='Day5', course__moment='Afternoon')
    tabb5_i = []
    for w in weeks:
        val = []
        for d in daytwo_afternoon:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabb5_i.append(' ')
        else:
            tabb5_i.append(val[0])
    
    daysix_afternoon =  InstructorProgram.objects.filter(program=program, course__day='Day6', course__moment='Afternoon')
    tabb6_i = []
    for w in weeks:
        val = []
        for d in daysix_afternoon:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabb6_i.append(' ')
        else:
            tabb6_i.append(val[0])
    
    
    dayseven_afternoon =  InstructorProgram.objects.filter(program=program, course__day='Day7', course__moment='Afternoon')
    tabb7_i = []
    for w in weeks:
        val = []
        for d in dayseven_afternoon:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabb7_i.append(' ')
        else:
            tabb7_i.append(val[0])
            
            
    # for the evening
    
    dayone_evening =  InstructorProgram.objects.filter(program=program, course__day='Day1', course__moment='Evening')
    tabbb1_i = []
    for w in weeks:
        val = []
        for d in dayone_evening:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabbb1_i.append(' ')
        else:
            tabbb1_i.append(val[0])
    
    
    daytwo_evening =  InstructorProgram.objects.filter(program=program, course__day='Day2', course__moment='Evening')
    tabbb2_i = []
    for w in weeks:
        val = []
        for d in daytwo_evening:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabbb2_i.append(' ')
        else:
            tabbb2_i.append(val[0])
    
    
    daythree_evening =  InstructorProgram.objects.filter(program=program, course__day='Day3', course__moment='Evening')
    tabbb3_i = []
    for w in weeks:
        val = []
        for d in daythree_evening:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabbb3_i.append(' ')
        else:
            tabbb3_i.append(val[0])
    
    dayfour_evening =  InstructorProgram.objects.filter(program=program, course__day='Day4', course__moment='Evening')
    tabbb4_i = []
    for w in weeks:
        val = []
        for d in dayfour_evening:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabbb4_i.append(' ')
        else:
            tabbb4_i.append(val[0])
    
    
    dayfive_evening =  InstructorProgram.objects.filter(program=program, course__day='Day5', course__moment='Evening')
    tabbb5_i = []
    for w in weeks:
        val = []
        for d in dayfive_evening:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabbb5_i.append(' ')
        else:
            tabbb5_i.append(val[0])
    
    
    daysix_evening =  InstructorProgram.objects.filter(program=program, course__day='Day6', course__moment='Evening')
    tabbb6_i = []
    for w in weeks:
        val = []
        for d in daysix_evening:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabbb6_i.append(' ')
        else:
            tabbb6_i.append(val[0])
    
    dayseven_evening =  InstructorProgram.objects.filter(program=program, course__day='Day7', course__moment='Evening')
    tabbb7_i = []
    for w in weeks:
        val = []
        for d in dayseven_evening:
            if d.course.week == w:
                val.append(d.instructor)
        if len(val) == 0:
            tabbb7_i.append(' ')
        else:
            tabbb7_i.append(val[0])
    
    
    tab_dd_afternoon = [zip(tabb1, tabb1_i), zip(tabb2, tabb2_i), zip(tabb3, tabb3_i), zip(tabb4, tabb4_i), zip(tabb5, tabb5_i), zip(tabb6, tabb6_i), zip(tabb7,tabb7_i)]
    tab_dd_evening = [zip(tabbb1, tabbb1_i), zip(tabbb2, tabbb2_i), zip(tabbb3, tabbb3_i), zip(tabbb4, tabbb4_i), zip(tabbb5, tabbb5_i), zip(tabbb6, tabbb6_i), zip(tabbb7, tabbb7_i)]
    
    context['tab_dd_afternoon']=tab_dd_afternoon
    context['tab_dd_evening']=tab_dd_evening
    
    if request.method == "POST":
        a = {}
        salaires = {}
        weekform = request.POST.get("weekform")
        dayform = request.POST.get("dayform")
        momentform = request.POST.get("momentform")
        instructorform = request.POST.get("instructorform")
        
        # search instructor 
        search = Instructor.objects.get(id=instructorform)
        #search course
        course = program.structure.courses.filter(day=dayform, week=weekform, moment=momentform)
        
        # previous object
        previous_object = InstructorProgram.objects.filter(course=course[0],  program=program)
        if len(previous_object)> 0:
            previous_object[0].delete()
        # create object
        if len(course) > 0:
            object = InstructorProgram(instructor=search, course=course[0],
                                                date_added=datetime.now(), course_done=False, program=program)  
                    
            object.set_moment() 
            print(object)
            
            object.save()
        
        
        program_courses_date = InstructorProgram.objects.filter(program=program).values('course').distinct()
        context['program_courses_date'] = program_courses_date
       
        program_instructors = InstructorProgram.objects.filter(program=program)#.values_list('instructor', flat=True).distinct()
        program_instructorss = InstructorProgram.objects.filter(program=program).values_list('instructor', flat=True).distinct()
        Instructorss = []
        print(program_instructorss)
        for i in program_instructorss:
            val = Instructor.objects.get(id=i)
            Instructorss.append(val)
        context['program_instructors'] = program_instructors
        context['program_instructorss'] = program_instructorss
        context['Instructorss'] = Instructorss
        
        objts = InstructorProgram.objects.all()
        
        for val in objts:
            for i in program.program_print():
                for j in i[2]:
                    if val.course == j:
                        position = i[2].index(j)
                        val.week = i[0]
                        val.save()
                        datt = datetime.strptime(i[1][position].split(", ")[1], "%Y-%m-%d").date()
                        val.date = datt
                        val.save()
        
        
        return render(request, 'App/programdetailstest.html', context)
    
    
    
    return render(request, 'App/programdetailstest.html', context)


# Task Management

# create a task for a program 

def task_create(request, id):
    program = Program.objects.get(id=id)
    tasks = program.tasks.all()
    form = TaskForm()
    context = {'tasks': tasks, 'form': form}
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            taskname = request.POST.get('taskname')
            print(taskname)
            task = form.cleaned_data['taskname']
            print(task)
            instructor = request.POST.get('instructor')
            taskdesc = request.POST.get('taskdesc')
            TaskStatus = request.POST.get("TaskStatus") 
            taskbudget = request.POST.get('taskbudget')
    print("bonjour")
    
# edit a task

def task_edit(request, id, pk):
    pass

# delete task

def task_delete(request, id, pk):
    pass