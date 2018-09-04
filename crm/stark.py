# by luffycity.com

from stark.service.stark import site, ModelStark
from django.http import JsonResponse
from .models import *

from django.utils.safestring import mark_safe
from django.conf.urls import url

from django.shortcuts import HttpResponse, redirect, render


site.register(School)


class UserConfig(ModelStark):
    list_display = ["name", "email", "depart"]


site.register(UserInfo, UserConfig)


class ClassConfig(ModelStark):
    def display_classname(self, obj=None, header=False):
        if header:
            return "班级名称"
        class_name = "%s(%s)" % (obj.course.name, str(obj.semester))
        return class_name

    list_display = [display_classname, "tutor", "teachers"]


site.register(ClassList, ClassConfig)


class CusotmerConfig(ModelStark):
    def display_gender(self, obj=None, header=False):
        if header:
            return "性别"
        return obj.get_gender_display()

    def display_course(self, obj=None, header=False):
        if header:
            return "咨询课程"
        temp = []
        for course in obj.course.all():
            s = "<a href='/stark/crm/customer/cancel_course/%s/%s' style='border:1px solid #369;padding:3px 6px'><span>%s</span></a>&nbsp;" % (
                obj.pk, course.pk, course.name,)
            temp.append(s)
        return mark_safe("".join(temp))

    # list_display = ["name",'gender','course',"consultant",]
    list_display = ["name", display_gender, display_course, "consultant", ]

    def cancel_course(self, request, customer_id, course_id):
        print(customer_id, course_id)

        obj = Customer.objects.filter(pk=customer_id).first()
        obj.course.remove(course_id)
        return redirect(self.get_list_url())


    def public_customer(self,request):
        """公共客户"""
        # 未报名 且3天未跟进或者15天未成单


        import datetime
        now =datetime.datetime.now()
        print(now)
        '''
        datetime.datetime
        datetime.time
        datetime.date
        datetime.timedelta(days=7)
        '''

        # 3天未跟进 now - last_consult_date > 3   ----> last_consult_date < now-3
        # 15天未成单 now - recv_date > 3   ----> recv_date < now-15
        delta_day3 = datetime.timedelta(days=3)
        delta_day15 = datetime.timedelta(days=15)

        from django.db.models import Q

        # Customer.objects.filter(status=2,last_consult_date__lt=now-3)
        # customer_list = Customer.objects.filter(Q(last_consult_date__lt=now-delta_day3)|Q(recv_date__lt=now-delta_day15),status=2)

        # 过滤掉 我的客户
        # user_id = 2
        user_id = request.session.get('user_id')
        customer_list = Customer.objects.filter(Q(last_consult_date__lt=now-delta_day3)|Q(recv_date__lt=now-delta_day15),status=2).exclude(consultant=user_id)
        print(customer_list.query)
        print('public_customer_list',customer_list)

        return render(request,'public.html',locals())

    def further(self,request,customer_id):
        # user_id = 2  # request.session.get("user_id")
        user_id = request.session.get('user_id')
        import datetime
        now =datetime.datetime.now()
        delta_day3 = datetime.timedelta(days=3)
        delta_day15 = datetime.timedelta(days=15)
        from django.db.models import Q


        # 更改客户的课程顾问，和相应的时间
        # Customer.objects.filter(pk=customer_id).update(consultant=user_id,last_consult_date=now,recv_date=now)
        ret = Customer.objects.filter(pk=customer_id).filter(Q(last_consult_date__lt=now-delta_day3)|Q(recv_date__lt=now-delta_day15),status=2).update(consultant=user_id,last_consult_date = now,recv_date=now)
        if not ret:
            return HttpResponse('已经被跟进了')

        # 客户跟进表的数据
        CustomerDistrbute.objects.create(customer_id=customer_id,consultant_id=user_id,date=now,status=1)

        return HttpResponse('跟进成功')



    def mycustomer(self,request):
        # user_id = 2
        user_id = request.session.get('user_id')
        customer_distrbute_list = CustomerDistrbute.objects.filter(consultant=user_id)
        print('customer_distrbute_list',customer_distrbute_list)
        return render(request,'mycustomer.html',locals())



    def extra_url(self):
        temp = []
        temp.append(url(r"cancel_course/(\d+)/(\d+)", self.cancel_course))
        temp.append(url(r"public/", self.public_customer))
        temp.append(url(r"further/(\d+)", self.further))
        temp.append(url(r"mycustomer/", self.mycustomer))
        return temp


site.register(Customer, CusotmerConfig)


site.register(Department)
site.register(Course)


class ConsultConfig(ModelStark):
    list_display = ['customer', 'consultant', 'date', 'note']


site.register(ConsultRecord, ConsultConfig)



class CourseRecordConfig(ModelStark):
    def score(self, request, course_record_id):
        """录入成绩view"""
        study_record_list = StudyRecord.objects.filter(course_record=course_record_id)
        print(study_record_list)
        score_choices = StudyRecord.score_choices
        if request.method == "POST":
            print(request.POST)  # <QueryDict:  'score_4': ['100'], 'homeword_note_4': ['33']}>

            data = {}  # dic = {1:{'homework_note':'good','score':'90'},2:{'homework_note':'nonono','score':'80'},}

            for key, value in request.POST.items():
                if key == "csrfmiddlewaretoken": continue
                field, pk = key.rsplit('_', 1)

                if pk in data:
                    data[pk][field] = value
                else:
                    data[pk] = {field: value}

                print('data', data)

                for pk, val in data.items():
                    StudyRecord.objects.filter(pk=pk).update(**val)

                '''
                # 方式1
                if field == 'score':
                    StudyRecord.objects.filter(pk=pk).update(score=value)
                else:
                    StudyRecord.objects.filter(pk=pk).update(homework_note=value.strip())
                '''

            return redirect(request.path)  # 跳转到当前url

        return render(request, 'score.html', locals())

    def extra_url(self):
        """录入成绩url"""
        temp = []
        temp.append(url('record_score/(\d+)', self.score))
        return temp

    def record_score(self, obj=None, header=False):
        """录入成绩a标签"""
        if header:
            return "录入成绩"
        return mark_safe("<a href='record_score/%s'>录入成绩</a>" % (obj.pk))


    def record(self, obj=None, header=False):
        if header:
            return '学习记录'
        return mark_safe("<a href='/stark/crm/studyrecord/?course_record=%s'>记录</a>" % (obj.pk))

    list_display = ['class_obj', 'day_num', 'teacher', record, record_score]

    def patch_studyrecord(self, request, queryset):
        print(queryset)  # <QuerySet [<CourseRecord: python基础班(9期) day11>]>
        temp = []
        for course_record in queryset:
            student_list = Student.objects.filter(class_list=course_record.class_obj.pk)
            for student in student_list:
                obj = StudyRecord(student=student, course_record=course_record)
                temp.append(obj)

        StudyRecord.objects.bulk_create(temp)  # 批量生成数据

    patch_studyrecord.short_description = '批量生成学习记录'
    actions = [patch_studyrecord, ]


site.register(CourseRecord, CourseRecordConfig)


class StudyRecordConfig(ModelStark):
    def display_record(self, obj=None, header=False):
        if header:
            return "记录"
        return obj.get_record_display()

    def display_score(self, obj=None, header=False):
        if header:
            return "成绩"
        return obj.get_score_display()

    list_display = ['student', 'course_record', display_record, display_score]

    def patch_late(self, request, queryset):
        queryset.update(record='late')

    patch_late.short_description = '迟到'
    actions = [patch_late]


site.register(StudyRecord, StudyRecordConfig)



class StudentConfig(ModelStark):
    def score_view(self, request, stu_id):
        """查看成绩 view"""
        if request.is_ajax():
            cid = request.GET.get('cid')
            sid = request.GET.get('sid')

            print(cid,sid)
            study_record_list = StudyRecord.objects.filter(student=sid,course_record__class_obj=cid)

            print('study_record_list',study_record_list)

            # 方案1：构造数据 # [['day11', 85], ['day12', 90]]
            data_list = []
            for study_record in study_record_list:
                day_num = study_record.course_record.day_num
                data_list.append(['day%s' % day_num, study_record.score])

            print('data_list',data_list)

            #方案2：构造数据 dic = {day:[day11,day12],score:[85,90]}
            dic = {'day':[],'score':[]}
            for study_record in study_record_list:
                day_num = study_record.course_record.day_num
                dic['day'].append('day%s'%day_num)
                dic['score'].append(study_record.score)
            print(dic)
            print(dic['day'])
            print(dic['score'])

            return JsonResponse(dic,safe=False)

        else:
            student = Student.objects.filter(pk=stu_id).first()
            class_list = student.class_list.all()
            return render(request, 'score_view.html', locals())

    def extra_url(self):
        """查看成绩url"""
        temp = []
        temp.append(url(r"score_view/(\d+)/", self.score_view))
        return temp

    def score_show(self, obj=None, header=False):
        """查看成绩 a标签"""
        if header:
            return "查看成绩"
        return mark_safe('<a href="score_view/%s">查看成绩</a>' % (obj.pk))

    list_display = ['customer', 'class_list', score_show]
    list_display_links = ['customer']


site.register(Student, StudentConfig)
