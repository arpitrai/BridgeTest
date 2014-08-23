from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth

from django.shortcuts import render_to_response
from django.template import RequestContext
from bridgebill.models import UserProfile, UserFriend, Bill, BillDetails, Feedback
from bridgebill.models import UserProfileForm, UserFriendForm, PartialBillForm, PartialBillDetailsForm, FeedbackForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, PasswordChangeForm

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required

from django.utils import simplejson

from django.conf import settings
if 'mailer' in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

from datetime import date
import time, urllib, json, signal

# Start - Settings to get email templates
account_creation_txt = get_template('email_templates/account_creation.txt')
account_creation_html = get_template('email_templates/account_creation.html')
bill_creation_txt = get_template('email_templates/bill_creation.txt')
bill_creation_html = get_template('email_templates/bill_creation.html')
payment_creation_txt = get_template('email_templates/payment_creation.txt')
payment_creation_html = get_template('email_templates/payment_creation.html')
feedback_txt = get_template('email_templates/feedback.txt')
feedback_html = get_template('email_templates/feedback.html')
# End - Settings to get email templates

# Start - Common function for creating UUIDs
import uuid
def create_uuid():
    return str(uuid.uuid4())
# End - Common function for creating UUIDs

# Start - Creating unique UserProfile ID
def create_userprofile_id():
    check_counter = True
    while check_counter is True:
        userprofile_id = 'up_' + create_uuid()
        try: 
            user_profile = UserProfile.objects.get(userprofile_id=userprofile_id)
            check_counter = True
        except:
            check_counter = False
    return userprofile_id
# End - Creating unique UserProfile ID

# Start - Creating unique UserFriend ID
def create_userfriend_id():
    check_counter = True
    while check_counter is True:
        userfriend_id = 'uf_' + create_uuid()
        try: 
            user_friend = UserFriend.objects.get(userfriend_id=userfriend_id)
            check_counter = True
        except:
            check_counter = False
    return userfriend_id
# End - Creating unique UserFriend ID

def login(request):
    authentication_form = AuthenticationForm()    
    error = ''
    if request.method == 'POST':
        authentication_form = AuthenticationForm(data=request.POST)
        if authentication_form.is_valid():
            auth_login(request, authentication_form.get_user())
            try: 
                url = request.GET['next']
                return HttpResponseRedirect(url)
            except: 
                return HttpResponseRedirect('/home/')
        else:
            error = 'Invalid username or password'
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect('/home/')
    return render_to_response('index.html', { 'authentication_form': authentication_form, 'error': error, 'request': request }, context_instance=RequestContext(request))

def login_error(request):
    error = 'Invalid username or password'
    authentication_form = AuthenticationForm()
    return render_to_response('index.html', { 'authentication_form': authentication_form, 'error': error, 'request': request }, context_instance=RequestContext(request))

def user_signup(request):
    if request.method == 'POST': 
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            username = user_creation_form.cleaned_data['username']
            password = user_creation_form.cleaned_data['password1']
            new_user = user_creation_form.save()
            new_user.email = new_user.username
            new_user.first_name = request.POST['firstname']
            new_user.save()
        
            userprofile_id = create_userprofile_id()
            user_profile = UserProfile(userprofile_id=userprofile_id, user=new_user)
            user_profile.save()

            new_user = authenticate(username=username, password=password)
            auth_login(request, new_user)
            
            # Send Email Start
            context = Context( {} )
            subject, to = 'Welcome to BridgeBill', new_user.email
            account_creation_txt_content = account_creation_txt.render(context)
            account_creation_html_content = account_creation_html.render(context)
            send_mail(subject, account_creation_txt_content, settings.DEFAULT_FROM_EMAIL, [ to ])
            # Send Email End

            userfriend_id = create_userfriend_id()
            user_own_friend = UserFriend(userfriend_id=userfriend_id, user_profile=user_profile, friend_email=request.user.email, friend_name=request.user.first_name+' '+ request.user.last_name, friend_deleted='N')
            user_own_friend.save()
            return HttpResponseRedirect('/home/')
        else:
            # Put in clause here when the user creation form is not valid
            pass
    else:
        user_creation_form = UserCreationForm()
        return render_to_response('user-signup.html', { 'user_creation_form': user_creation_form, 'request': request }, context_instance=RequestContext(request))

def forgot_password(request):
    password_reset(request, template_name='forgot-password.html', email_template_name='password_reset.txt', post_reset_redirect='/user/forgot-password-confirmation')
    #if request.method == 'POST':
        #user_exists = False
        #forgot_password_form = PasswordResetForm(request.POST)
        #if forgot_password_form.is_valid():
        #else:
            #return render_to_response('forgot-password-confirmation.html', { 'user_exists': user_exists, 'request': request }, context_instance=RequestContext(request))
    #else:
        #forgot_password_form = PasswordResetForm()
        #return render_to_response('forgot-password.html', { 'forgot_password_form': forgot_password_form, 'request': request }, context_instance=RequestContext(request))

@login_required
def home(request):
    userprofile_object = UserProfile.objects.get(user=request.user)

    class Persons:
        def __init__(self, name, total_borrowed={}, total_lent={}, total={}, total_flag={}, overall={}, slug=''):
            self.name = name
            self.total_borrowed = total_borrowed
            self.total_lent = total_lent
            self.total = total
            self.total_flag = total_flag
            self.overall = overall
            self.slug = slug

    persons_list = []
    borrower_also_lender_list = []

    my_borrowers = UserFriend.objects.filter(user_profile=userprofile_object).exclude(friend_email__iexact=userprofile_object.user.email).extra(select={'lower_name': 'lower(friend_name)'}).order_by('lower_name') # lower() works only with Postgres
    for each_borrower in my_borrowers:
        each_borrower_bills = BillDetails.objects.filter(bill__lender=userprofile_object, borrower=each_borrower, bill_cleared='N')
        total_lent = {}
        total_borrowed = {}
        if each_borrower_bills:
            for each_bill in each_borrower_bills:
                try:
                    temp = total_borrowed[each_bill.bill.currency] 
                    total_borrowed[each_bill.bill.currency] += each_bill.individual_amount
                except:
                    total_borrowed[each_bill.bill.currency] = each_bill.individual_amount

            person = Persons(name=each_borrower.friend_name, total_borrowed=total_borrowed, slug=each_borrower.userfriend_id)
           
            try:
                borrower_as_user = UserProfile.objects.get(user__email__iexact=each_borrower.friend_email)
                try: 
                    me_as_borrower = UserFriend.objects.get(user_profile=borrower_as_user, friend_email__iexact=userprofile_object.user.email)
                    borrower_also_lender_list.append(each_borrower.friend_email)
                    each_borrower_as_lender_bills = BillDetails.objects.filter(bill__lender=borrower_as_user, borrower=me_as_borrower, bill_cleared='N')
                    if each_borrower_as_lender_bills:
                        for each_bill in each_borrower_as_lender_bills:
                            try:
                                temp = total_lent[each_bill.bill.currency] 
                                total_lent[each_bill.bill.currency] += each_bill.individual_amount
                            except:
                                total_lent[each_bill.bill.currency] = each_bill.individual_amount
                except:
                    pass
            except:
                pass
            person.total_lent = total_lent

            person.total = {}
            person.total_flag = {}
            person.overall = {}
            for i in person.total_borrowed:
                if i in person.total_lent:
                    person.total[i] = person.total_borrowed[i] - person.total_lent[i]
                else:
                    person.total[i] = person.total_borrowed[i]


            for j in person.total_lent:
                if j not in person.total_borrowed:
                    person.total[j] = 0 - person.total_lent[j]
            
            for i in person.total:
                if person.total[i] < 0:
                    person.total_flag[i] = '-ve'
                    person.total[i] *= -1
                elif person.total[i] > 0:
                    person.total_flag[i] = '+ve'
                elif person.total[i] == 0:
                    person.total_flag[i] = '0'
                person.overall[i] = [ person.total[i], person.total_flag[i] ]
            
            persons_list.append(person)


    borrower_also_lender_userprofiles = []
    if borrower_also_lender_list:
        for borrower_also_lender in borrower_also_lender_list:
            borrower_also_lender_userprofile = UserProfile.objects.get(user__email__iexact=borrower_also_lender)
            borrower_also_lender_userprofiles.append(borrower_also_lender_userprofile)
    my_lenders = UserFriend.objects.filter(friend_email__iexact=userprofile_object.user.email).exclude(user_profile=userprofile_object).exclude(user_profile__in=borrower_also_lender_userprofiles)
    
    for each_lender in my_lenders:
        userprofile_lender = UserProfile.objects.get(user__email__iexact=each_lender.user_profile.user.email)
        borrower = UserFriend.objects.get(user_profile=userprofile_lender, friend_email__iexact = userprofile_object.user.email)
        each_lender_bills = BillDetails.objects.filter(bill__lender=userprofile_lender, borrower=borrower, bill_cleared='N')
        if each_lender_bills: 
            total_lent = {}
            for each_bill in each_lender_bills:
                try:
                    temp = total_lent[each_bill.bill.currency] 
                    total_lent[each_bill.bill.currency] += each_bill.individual_amount
                except:
                    total_lent[each_bill.bill.currency] = each_bill.individual_amount
            name = each_lender.user_profile.user.first_name + ' ' + each_lender.user_profile.user.last_name
            slug = userprofile_lender.userprofile_id
            person = Persons(name=name, total_lent=total_lent, slug=slug) 

            person.total = {}
            person.total_flag = {}
            person.overall = {}
            for i in person.total_lent:
                person.total[i] = 0 - person.total_lent[i]
                if person.total[i] < 0:
                    person.total_flag[i] = '-ve'
                    person.total[i] *= -1
                elif person.total[i] > 0:
                    person.total_flag[i] = '+ve'
                elif person.total[i] == 0:
                    person.total_flag[i] = '0'
                person.overall[i] = [ person.total[i], person.total_flag[i] ]
            persons_list.append(person)
 
    return render_to_response('home.html', { 'persons_list': persons_list, 'request': request }, context_instance=RequestContext(request))

@login_required
def home_details(request, person_id):
    userprofile_object = UserProfile.objects.get(user=request.user)

    class Transactions:
        def __init__(self, date, description, currency, individual_amount, flag, slug, detail_id):
            self.date = date
            self.description = description
            self.currency = currency
            self.individual_amount = individual_amount
            self.flag = flag
            self.slug = slug
            self.detail_id = detail_id

    if request.method == 'GET':
        if person_id[:3] == 'uf_':
            person = 'borrower_and_lender'
        else:
            person = 'lender'

        if person == 'borrower_and_lender':
            bill_list = []
            net_amount = {}
            net_flag = {}
            total_lent_amount = {}
            total_borrowed_amount = {}
            overall = {}

            # Start - First as borrower
            userfriend_id = person_id
            person_borrower = UserFriend.objects.get(user_profile=userprofile_object, userfriend_id=userfriend_id)
            person_name = person_borrower.friend_name
            person_email = person_borrower.friend_email
            person_borrower_bills = BillDetails.objects.filter(bill__lender=userprofile_object, borrower=person_borrower, bill_cleared='N').order_by('-bill__date')
            for each_bill in person_borrower_bills:
                try:
                    temp = total_lent_amount[each_bill.bill.currency] 
                    total_lent_amount[each_bill.bill.currency] += each_bill.individual_amount
                except:
                    total_lent_amount[each_bill.bill.currency] = each_bill.individual_amount
                transaction = Transactions(date=each_bill.bill.date, description=each_bill.bill.description, currency=each_bill.bill.currency, individual_amount=each_bill.individual_amount, flag='+ve', slug=each_bill.bill.overall_bill_id, detail_id=each_bill.billdetail_id)
                bill_list.append(transaction)
            # End - First as borrower
            
            # Start - Second as lender
            try: 
                person_as_lender = UserProfile.objects.get(user__email__iexact=person_email)
                me_as_borrower = UserFriend.objects.get(user_profile=person_as_lender, friend_email__iexact=userprofile_object.user.email)
                person_lender_bills = BillDetails.objects.filter(bill__lender=person_as_lender, borrower=me_as_borrower, bill_cleared='N').order_by('-bill__date')
                for each_bill in person_lender_bills:
                    try:
                        temp = total_borrowed_amount[each_bill.bill.currency] 
                        total_borrowed_amount[each_bill.bill.currency] += each_bill.individual_amount
                    except:
                        total_borrowed_amount[each_bill.bill.currency] = each_bill.individual_amount
                    transaction = Transactions(date=each_bill.bill.date, description=each_bill.bill.description, currency=each_bill.bill.currency, individual_amount=each_bill.individual_amount, flag='-ve', slug=each_bill.bill.overall_bill_id, detail_id=each_bill.billdetail_id)
                    bill_list.append(transaction)
            except:
                pass
            # End - Second as lender

            for i in total_lent_amount:
                if i in total_borrowed_amount:
                    net_amount[i] = total_lent_amount[i] - total_borrowed_amount[i]
                else:
                    net_amount[i] = total_lent_amount[i]

            for j in total_borrowed_amount:
                if j not in total_lent_amount:
                    net_amount[j] = 0 - total_borrowed_amount[j]

            for i in net_amount:
                if net_amount[i] < 0:
                    net_flag[i] = '-ve'
                    net_amount[i] *= -1
                elif net_amount[i] > 0:
                    net_flag[i] = '+ve'
                elif net_amount[i] == 0:
                    net_flag[i] = 'zero'
                overall[i] = [ net_amount[i], net_flag[i] ]

            return render_to_response('home-details.html', { 'bill_list': bill_list, 'person_name': person_name, 'person_email': person_email, 'overall': overall, 'request': request }, context_instance=RequestContext(request))

        elif person == 'lender':
            bill_list = []
            net_amount = {}
            net_flag = {}
            overall = {}
            userprofile_id = person_id
            
            person_as_lender = UserProfile.objects.get(userprofile_id=userprofile_id)
            person_name = person_as_lender.user.first_name + ' ' + person_as_lender.user.last_name
            person_email = person_as_lender.user.email
            me_as_borrower = UserFriend.objects.get(user_profile=person_as_lender, friend_email__iexact=userprofile_object.user.email)
            person_lender_bills = BillDetails.objects.filter(bill__lender=person_as_lender, borrower=me_as_borrower, bill_cleared='N').order_by('-bill__date')
            for each_bill in person_lender_bills:
                try:
                    temp = net_amount[each_bill.bill.currency] 
                    net_amount[each_bill.bill.currency] += each_bill.individual_amount
                except:
                    net_amount[each_bill.bill.currency] = each_bill.individual_amount
                transaction = Transactions(date=each_bill.bill.date, description=each_bill.bill.description, currency=each_bill.bill.currency, individual_amount=each_bill.individual_amount, flag='-ve', slug=each_bill.bill.overall_bill_id, detail_id=each_bill.billdetail_id)
                bill_list.append(transaction)

            for i in net_amount:
                if net_amount[i] != 0:
                    net_flag[i] = '-ve'
                else:
                    net_flag[i] = 'zero'
                overall[i] = [ net_amount[i], net_flag[i] ]

            return render_to_response('home-details.html', { 'bill_list': bill_list, 'person_name': person_name, 'person_email': person_email, 'overall': overall, 'request': request }, context_instance=RequestContext(request))

    else:
        billdetails_list = request.POST.getlist('billdetails_list')
        person_name = request.POST['person_name']
        person_email = request.POST['person_email']
        list_of_bills_cleared = base_function_settle_payment(request, userprofile_object, billdetails_list, person_email)
        return render_to_response('settle-payment-success.html', { 'person_name': person_name, 'list_of_bills_cleared': list_of_bills_cleared, 'request': request }, context_instance=RequestContext(request))

@login_required
def my_friends(request):
    userprofile_object = UserProfile.objects.get(user=request.user)
    if request.method == 'GET':
        my_friends = UserFriend.objects.filter(user_profile=userprofile_object, friend_deleted='N').exclude(friend_email__iexact=userprofile_object.user.email).extra(select={'lower_name': 'lower(friend_name)'}).order_by('lower_name') # lower() works only with Postgres
        return render_to_response('my-friends.html', { 'my_friends': my_friends, 'request': request }, context_instance=RequestContext(request))

@login_required
def edit_friend(request, userfriend_id):
    userprofile_object = UserProfile.objects.get(user=request.user)
    if request.method == 'POST' and request.is_ajax():
        try:
            time.sleep(3)
            userfriend_object = UserFriend.objects.get(userfriend_id=userfriend_id)
            friend_name = request.POST['friend_name']
            friend_email = request.POST['friend_email']

            if friend_name == '' or friend_email == '':
                if not friend_name:
                    error = { 'error_message': 'Invalid name' }
                elif not friend_email: 
                    error = { 'error_message': 'Invalid email address' }
                json = simplejson.dumps(error)
                return HttpResponse(json, mimetype='application/json')

            if userprofile_object.user.email == friend_email:
                error = { 'error_message': 'Can\'t add your own email address' }
                json = simplejson.dumps(error)
                return HttpResponse(json, mimetype='application/json')

            if userfriend_object.friend_email != friend_email:
                try: 
                    duplicate_userfriend_object = UserFriend.objects.get(user_profile=userprofile_object, friend_email__iexact=friend_email)
                    if duplicate_userfriend_object.friend_deleted == 'Y':
                        userfriend_object.friend_name = friend_name
                        userfriend_object.friend_email = friend_email
                        userfriend_object.save()
                        result = { 'friend_name': userfriend_object.friend_name, 'friend_email': userfriend_object.friend_email, 'userfriend_id': userfriend_object.userfriend_id }
                        json = simplejson.dumps(result)
                        return HttpResponse(json, mimetype='application/json')
                    else:
                        error = { 'error_message': 'Email address already exists!' }
                        json = simplejson.dumps(error)
                        return HttpResponse(json, mimetype='application/json')
                except:
                    if validate_email(friend_email):
                        userfriend_object.friend_name = friend_name
                        userfriend_object.friend_email = friend_email
                        userfriend_object.save()
                        result = { 'friend_name': userfriend_object.friend_name, 'friend_email': userfriend_object.friend_email, 'userfriend_id': userfriend_object.userfriend_id }
                        json = simplejson.dumps(result)
                        return HttpResponse(json, mimetype='application/json')
                    else:
                        error = { 'error_message': 'Invalid email address' }
                        json = simplejson.dumps(error)
                        return HttpResponse(json, mimetype='application/json')
            else:
                if userfriend_object.friend_name != friend_name:
                    userfriend_object.friend_name = friend_name
                    userfriend_object.save()
                result = { 'friend_name': userfriend_object.friend_name, 'friend_email': userfriend_object.friend_email, 'userfriend_id': userfriend_object.userfriend_id }
                json = simplejson.dumps(result)
                return HttpResponse(json, mimetype='application/json')

        except:
            pass
    else:
        if request.method == 'GET' and request.is_ajax():
            try:
                time.sleep(3)
                userfriend_object = UserFriend.objects.get(userfriend_id=userfriend_id)
                result = { 'friend_name': userfriend_object.friend_name, 'friend_email': userfriend_object.friend_email, 'userfriend_id': userfriend_object.userfriend_id }
                json = simplejson.dumps(result)
                return HttpResponse(json, mimetype='application/json')
            except:
                pass

@login_required
def add_friend(request):
    userprofile_object = UserProfile.objects.get(user=request.user)
    if request.method == 'POST' and request.is_ajax():
        time.sleep(3)
        friend_name = request.POST['friend_name']
        friend_email = request.POST['friend_email']

        if friend_name == '' or friend_email == '':
            if not friend_name:
                error = { 'error_message': 'Invalid name' }
            elif not friend_email: 
                error = { 'error_message': 'Invalid email address' }
            json = simplejson.dumps(error)
            return HttpResponse(json, mimetype='application/json')

        if userprofile_object.user.email == friend_email:
            error = { 'error_message': 'Can\'t add your own email address' }
            json = simplejson.dumps(error)
            return HttpResponse(json, mimetype='application/json')

        try:
            duplicate_userfriend_object = UserFriend.objects.get(user_profile=userprofile_object, friend_email__iexact=friend_email)
            if duplicate_userfriend_object.friend_deleted == 'Y':
                duplicate_userfriend_object.friend_name = friend_name
                duplicate_userfriend_object.friend_deleted = 'N'
                duplicate_userfriend_object.save()
                result = { 'friend_name': duplicate_userfriend_object.friend_name, 'friend_email': duplicate_userfriend_object.friend_email, 'userfriend_id': duplicate_userfriend_object.userfriend_id }
                json = simplejson.dumps(result)
                return HttpResponse(json, mimetype='application/json')
            else:
                error = { 'error_message': 'Email address already exists!' }
                json = simplejson.dumps(error)
                return HttpResponse(json, mimetype='application/json')
        except:
            if validate_email(friend_email):
                userfriend_id = create_userfriend_id()
                userfriend_object = UserFriend(userfriend_id=userfriend_id, user_profile=userprofile_object, friend_name=friend_name, friend_email=friend_email, friend_deleted='N')
                userfriend_object.save()
                result = { 'friend_name': userfriend_object.friend_name, 'friend_email': userfriend_object.friend_email, 'userfriend_id': userfriend_object.userfriend_id }
                json = simplejson.dumps(result)
                return HttpResponse(json, mimetype='application/json')
            else:
                error = { 'error_message': 'Invalid email address' }
                json = simplejson.dumps(error)
                return HttpResponse(json, mimetype='application/json')
    else:
        pass

@login_required
def delete_friend(request, userfriend_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            time.sleep(3)
            userfriend_object = UserFriend.objects.get(userfriend_id=userfriend_id)
            userfriend_object.friend_deleted = 'Y'
            userfriend_object.save()
            result = { 'friend_email': userfriend_object.friend_email }
            json = simplejson.dumps(result)
            return HttpResponse(json, mimetype='application/json')
        except:
            pass
    else:
        if request.method == 'GET' and request.is_ajax():
            pass
 
def base_function_net_outstanding(request, userp_o, person):
    userprofile_object = UserProfile.objects.get(user__email__iexact=userp_o)

    lender_bill_details = []
    borrower_bill_details = []
    net_amount = {}
    net_flag = {}
    overall = {}

    # Start - Person as Lender
    person_as_lender = ''
    total_lender_amount = {}
    try: 
        person_as_lender = UserProfile.objects.get(user__email__iexact=person)
        person_name = person_as_lender.user.first_name + ' ' + person_as_lender.user.last_name
    except:
        pass
    if person_as_lender:
        try: 
            me_as_borrower = UserFriend.objects.get(user_profile=person_as_lender, friend_email__iexact=userprofile_object.user.email)
            lender_bill_details = BillDetails.objects.filter(bill__lender=person_as_lender, borrower=me_as_borrower, bill_cleared='N')
            for bill in lender_bill_details:
                try:
                    temp = total_lender_amount[bill.bill.currency] 
                    total_lender_amount[bill.bill.currency] += bill.individual_amount
                except:
                    total_lender_amount[bill.bill.currency] = bill.individual_amount
        except:
            pass
    # End - Person as Lender

    # Start - Person as Borrower
    person_as_borrower = ''
    total_borrower_amount = {}
    try:
        person_as_borrower = UserFriend.objects.get(user_profile=userprofile_object, friend_email=person)
    except:
        pass
    if person_as_borrower:
        person_name = person_as_borrower.friend_name
        borrower_bill_details = BillDetails.objects.filter(bill__lender=userprofile_object, borrower=person_as_borrower, bill_cleared='N')
        for bill in borrower_bill_details:
            try:
                temp = total_borrower_amount[bill.bill.currency] 
                total_borrower_amount[bill.bill.currency] += bill.individual_amount
            except:
                total_borrower_amount[bill.bill.currency] = bill.individual_amount
    # End - Person as Borrower

    for i in total_borrower_amount:
        if i in total_lender_amount:
            net_amount[i] = total_borrower_amount[i] - total_lender_amount[i]
        else:
            net_amount[i] = total_borrower_amount[i]

    for j in total_lender_amount:
        if j not in total_borrower_amount:
            net_amount[j] = 0 - total_lender_amount[j]

    for i in net_amount:
        if net_amount[i] < 0:
            net_flag[i] = '-ve'
            net_amount[i] *= -1
        elif net_amount[i] > 0:
            net_flag[i] = '+ve'
        elif net_amount[i] == 0:
            net_flag[i] = 'zero'
        overall[i] = [ net_amount[i], net_flag[i] ]

    base_function_results = { 'person_name': person_name, 'lender_bill_details': lender_bill_details, 'borrower_bill_details': borrower_bill_details, 'overall': overall }
    return base_function_results

# Start - Record Bill - One Page
@login_required
def record_bill(request):
    userprofile_object = UserProfile.objects.get(user=request.user)
    if request.method == 'GET':
        my_friends = UserFriend.objects.filter(user_profile=userprofile_object, friend_deleted='N').extra(select={'lower_name': 'lower(friend_name)'}).order_by('lower_name') # lower() works only with Postgres

        # Start - Doing this so that 'Me' always appears on top
        temp = []
        for friend in my_friends:
            if friend.friend_email == userprofile_object.user.email:
                temp.append(friend)
        for friend in my_friends:
            if friend.friend_email != userprofile_object.user.email:
                temp.append(friend)
        my_friends = list(temp) 
        # End - Doing this so that 'Me' always appears on top

        currency = userprofile_object.currency
        if currency:
            bill_form = PartialBillForm({ 'currency': currency })
        else: 
            bill_form = PartialBillForm()
        return render_to_response('record-bill.html', { 'my_friends': my_friends, 'bill_form': bill_form, 'userprofile_object': userprofile_object, 'request': request }, context_instance=RequestContext(request))
# End - Record Bill - One Page

# Start - Recording Bills - Initial Option
#@login_required
#def record_bill_option(request):
    #if request.method == 'POST':
        #if request.POST['record_bill_option'] == 'equal_split':
            #return HttpResponseRedirect('/record-bill/equal-split/')
        #else: 
            #return HttpResponseRedirect('/record-bill/unequal-split/')
    #else:
        #return render_to_response('record-bill-option.html', { 'request': request }, context_instance=RequestContext(request))
# End - Recording Bills - Initial Option

# Start - Creating unique overall bill ID
def create_overall_bill_id():
    check_counter = True
    while check_counter is True:
        overall_bill_id = 'ob_' + create_uuid()
        try: 
            bill = Bill.objects.get(overall_bill_id=overall_bill_id)
            check_counter = True
        except:
            check_counter = False
    return overall_bill_id
# End - Creating unique overall bill ID

# Start - Creating unique bill detail ID
def create_billdetail_id():
    check_counter = True
    while check_counter is True:
        billdetail_id = 'bd_' + create_uuid()
        try: 
            bill_detail = BillDetails.objects.get(billdetail_id=billdetail_id)
            check_counter = True
        except:
            check_counter = False
    return billdetail_id
# End - Creating unique bill detail ID

# Start - Record Bill - Equal Split
@login_required
def record_bill_equal_split(request):
    userprofile_object = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        bill_form = PartialBillForm(request.POST)
        if bill_form.is_valid():
            overall_bill_id = create_overall_bill_id()
            lender = userprofile_object
            bill = Bill(overall_bill_id=overall_bill_id, lender=lender, date=bill_form.cleaned_data['date'], description=bill_form.cleaned_data['description'], amount=bill_form.cleaned_data['amount'], currency=bill_form.cleaned_data['currency'])
            bill.save()
            number_of_borrowers = len(request.POST.getlist('people')) + len(request.POST.getlist('people_new'))
            individual_amount = float(bill_form.cleaned_data['amount']/number_of_borrowers)

            # Start - Change user's default currency on user profile if applicable
            if userprofile_object.currency != bill_form.cleaned_data['currency']:
                userprofile_object.currency = bill_form.cleaned_data['currency']
                userprofile_object.save()
            # End - Change user's default currency on user profile if applicable

            # Start - For existing friends
            if request.POST.getlist('people'):
                for borrower in request.POST.getlist('people'):
                    billdetail_id = create_billdetail_id()
                    if borrower != userprofile_object.user.email:
                        borrower_object = UserFriend.objects.get(user_profile=userprofile_object, friend_email__iexact=borrower)
                        bill_detail = BillDetails(billdetail_id=billdetail_id, bill=bill, borrower=borrower_object, individual_amount=individual_amount, bill_cleared='N', bill_cleared_date=bill_form.cleaned_data['date'], bill_deleted='N')
                        bill_detail.save()

                        # Start - Send Email 
                        base_results_net_outstanding = base_function_net_outstanding(request, request.user.email, borrower)
                        net_outstanding = base_results_net_outstanding['overall']
                        context = Context({ 'userprofile_object': userprofile_object, 'bill': bill, 'bill_detail': bill_detail, 'net_outstanding': net_outstanding })
                        subject = 'New Bill Recorded: ' + bill.description
                        bill_creation_txt_content = bill_creation_txt.render(context)
                        bill_creation_html_content = bill_creation_html.render(context)
                        send_mail(subject, bill_creation_txt_content, settings.DEFAULT_FROM_EMAIL, [ borrower ])
                        # End - Send Email 

                    else:
                        borrower_object = UserFriend.objects.get(user_profile=userprofile_object, friend_email__iexact=userprofile_object.user.email)
                        bill_detail = BillDetails(billdetail_id=billdetail_id, bill=bill, borrower=borrower_object, individual_amount=individual_amount, bill_cleared='Y', bill_cleared_date=bill_form.cleaned_data['date'], bill_deleted='N')
                        bill_detail.save()
            # End - For existing friends
            
            # Start - For new friends
            if request.POST.getlist('people_new'):
                for borrower in request.POST.getlist('people_new'):
                    i = borrower[11:]
                    friend_name = request.POST['name_'+str(i)]
                    friend_email = request.POST['email_'+str(i)]
                    bill_cleared = 'N'
                    try:
                        user_friend = UserFriend.objects.get(user_profile=userprofile_object, friend_email__iexact=friend_email)
                        if user_friend.friend_deleted == 'Y':
                            user_friend.friend_deleted = 'N'
                        if user_friend.friend_email == userprofile_object.user.email:
                            bill_cleared = 'Y'
                        else:
                            if user_friend.friend_name != friend_name:
                                user_friend.friend_name = friend_name
                        user_friend.save()
                    except:
                        userfriend_id = create_userfriend_id()
                        user_friend = UserFriend(userfriend_id=userfriend_id, user_profile=userprofile_object, friend_name=friend_name, friend_email=friend_email, friend_deleted='N')
                        user_friend.save()
                    borrower_object = user_friend
                    billdetail_id = create_billdetail_id()
                    bill_detail = BillDetails(billdetail_id=billdetail_id, bill=bill, borrower=borrower_object, individual_amount=individual_amount, bill_cleared=bill_cleared, bill_cleared_date=bill_form.cleaned_data['date'], bill_deleted='N')
                    bill_detail.save()

                    # Start - Send Email 
                    if friend_email != request.user.email:
                        base_results_net_outstanding = base_function_net_outstanding(request, request.user.email, friend_email)
                        net_outstanding = base_results_net_outstanding['overall']
                        context = Context({ 'userprofile_object': userprofile_object, 'bill': bill, 'bill_detail': bill_detail, 'net_outstanding': net_outstanding })
                        subject = 'New Bill Recorded: ' + bill.description
                        bill_creation_txt_content = bill_creation_txt.render(context)
                        bill_creation_html_content = bill_creation_html.render(context)
                        send_mail(subject, bill_creation_txt_content, settings.DEFAULT_FROM_EMAIL, [ friend_email ])
                    # End - Send Email 
            # End - For new friends

            redirect_url = '/bill/details/c/'+ str(bill.overall_bill_id) + '/'
            return HttpResponseRedirect(redirect_url)
    #else:
        #my_friends = UserFriend.objects.filter(user_profile=userprofile_object, friend_deleted='N').extra(select={'lower_name': 'lower(friend_name)'}).order_by('lower_name') # lower() works only with Postgres

        ## Start - Doing this so that 'Me' always appears on top
        #temp = []
        #for friend in my_friends:
            #if friend.friend_email == userprofile_object.user.email:
                #temp.append(friend)
        #for friend in my_friends:
            #if friend.friend_email != userprofile_object.user.email:
                #temp.append(friend)
        #my_friends = list(temp) 
        ## End - Doing this so that 'Me' always appears on top

        #currency = userprofile_object.currency
        #if currency:
            #bill_form = PartialBillForm({ 'currency': currency })
        #else: 
            #bill_form = PartialBillForm()
        #return render_to_response('record-bill-equal-split.html', { 'my_friends': my_friends, 'bill_form': bill_form, 'userprofile_object': userprofile_object, 'request': request }, context_instance=RequestContext(request))

@login_required
def record_bill_unequal_split(request):
    userprofile_object = UserProfile.objects.get(user=request.user)
    my_friends = UserFriend.objects.filter(user_profile=userprofile_object, friend_deleted='N').extra(select={'lower_name': 'lower(friend_name)'}).order_by('lower_name') # lower() works only with Postgres
    number_of_friends = my_friends.count()
    if request.method == 'POST':
        bill_form = PartialBillForm(request.POST)
        if bill_form.is_valid():
            overall_bill_id = create_overall_bill_id()
            lender = userprofile_object
            bill = Bill(overall_bill_id=overall_bill_id, lender=lender, date=bill_form.cleaned_data['date'], description=bill_form.cleaned_data['description'], amount=bill_form.cleaned_data['amount'], currency=bill_form.cleaned_data['currency'])
            bill.save()

            # Start - Change user's default currency on user profile if applicable
            if userprofile_object.currency != bill_form.cleaned_data['currency']:
                userprofile_object.currency = bill_form.cleaned_data['currency']
                userprofile_object.save()
            # End - Change user's default currency on user profile if applicable

            # Start - To count total people involved
            friends_total = 0
            for i in range(0, number_of_friends):
                if request.POST['borrower_'+str(i)] != '':
                    friends_total += 1
            new_friends_total = len(request.POST.getlist('people_new'))
            total_people = friends_total + new_friends_total
            # End - To count total people involved

            # Start - For existing friends
            for i in range(0, number_of_friends):
                borrower_counter = 'borrower_' + str(i)
                number_of_people_counter = 'number_of_people_' + str(i)
                borrower_amount_counter = 'borrower_amount_' + str(i)
                try:
                    if request.POST[borrower_counter] != '':
                        billdetail_id = create_billdetail_id()
                        if request.POST[borrower_counter] != userprofile_object.user.email:
                            borrower = UserFriend.objects.get(user_profile=userprofile_object, friend_email__iexact=request.POST[borrower_counter])
                            bill_detail = BillDetails(billdetail_id=billdetail_id, bill=bill, borrower=borrower, individual_amount=float(request.POST[borrower_amount_counter]), bill_cleared='N', bill_cleared_date=bill_form.cleaned_data['date'], bill_deleted='N') 
                            bill_detail.save()

                            # Start - Send Email Start
                            base_results_net_outstanding = base_function_net_outstanding(request, request.user.email, request.POST[borrower_counter])
                            net_outstanding = base_results_net_outstanding['overall']
                            context = Context({ 'userprofile_object': userprofile_object, 'bill': bill, 'bill_detail': bill_detail, 'net_outstanding': net_outstanding })
                            subject = 'New Bill Recorded: ' + bill.description
                            bill_creation_txt_content = bill_creation_txt.render(context)
                            bill_creation_html_content = bill_creation_html.render(context)
                            send_mail(subject, bill_creation_txt_content, settings.DEFAULT_FROM_EMAIL, [ request.POST[borrower_counter] ])
                            # Send Email End
                        else:
                            borrower = UserFriend.objects.get(user_profile=userprofile_object, friend_email__iexact=userprofile_object.user.email)
                            bill_detail = BillDetails(billdetail_id=billdetail_id, bill=bill, borrower=borrower, individual_amount=float(request.POST[borrower_amount_counter]), bill_cleared='Y', bill_cleared_date=bill_form.cleaned_data['date'], bill_deleted='N')
                            bill_detail.save()
                    else:
                        continue
                except:
                    continue
            # End - For existing friends

            # Start - For new friends
            if request.POST.getlist('people_new'):
                for borrower in request.POST.getlist('people_new'):
                    i = borrower[13:]
                    friend_name = request.POST['x_name_'+str(i)]
                    friend_email = request.POST['x_email_'+str(i)]
                    number_of_people = request.POST['x_number_of_people_'+str(i)]
                    borrower_amount = request.POST['x_borrower_amount_'+str(i)]
                    bill_cleared = 'N'
                    if friend_name and friend_email and number_of_people and borrower_amount:
                        try:
                            user_friend = UserFriend.objects.get(user_profile=userprofile_object, friend_email__iexact=friend_email)
                            if user_friend.friend_deleted == 'Y':
                                user_friend.friend_deleted = 'N'
                            if user_friend.friend_email == userprofile_object.user.email:
                                bill_cleared = 'Y'
                            else:
                                if user_friend.friend_name != friend_name:
                                    user_friend.friend_name = friend_name
                            user_friend.save()
                        except:
                            userfriend_id = create_userfriend_id()
                            user_friend = UserFriend(userfriend_id=userfriend_id, user_profile=userprofile_object, friend_name=friend_name, friend_email=friend_email, friend_deleted='N')
                            user_friend.save()
                        borrower_object = user_friend
                        billdetail_id = create_billdetail_id()
                        bill_detail = BillDetails(billdetail_id=billdetail_id, bill=bill, borrower=borrower_object, individual_amount=borrower_amount, bill_cleared=bill_cleared, bill_cleared_date=bill_form.cleaned_data['date'], bill_deleted='N')

                        bill_detail.save()
                        
                        # Start - Send Email 
                        if friend_email != request.user.email:
                            base_results_net_outstanding = base_function_net_outstanding(request, request.user.email, friend_email)
                            net_outstanding = base_results_net_outstanding['overall']
                            context = Context({ 'userprofile_object': userprofile_object, 'bill': bill, 'bill_detail': bill_detail, 'net_outstanding': net_outstanding })
                            subject = 'New Bill Recorded: ' + bill.description
                            bill_creation_txt_content = bill_creation_txt.render(context)
                            bill_creation_html_content = bill_creation_html.render(context)
                            send_mail(subject, bill_creation_txt_content, settings.DEFAULT_FROM_EMAIL, [ friend_email ])
                        # End - Send Email
            # End - For new friends

            redirect_url = '/bill/details/c/'+ str(bill.overall_bill_id) + '/'
            return HttpResponseRedirect(redirect_url)
    #else: 
        ## Start - Doing this so that 'Me' always appears on top
        #temp = []
        #for friend in my_friends:
            #if friend.friend_email == userprofile_object.user.email:
                #temp.append(friend)
        #for friend in my_friends:
            #if friend.friend_email != userprofile_object.user.email:
                #temp.append(friend)
        #my_friends = list(temp) 
        ## End - Doing this so that 'Me' always appears on top

        #currency = userprofile_object.currency
        #if currency:
            #bill_form = PartialBillForm({ 'currency': currency })
        #else: 
            #bill_form = PartialBillForm()
        #return render_to_response('record-bill-unequal-split.html', { 'my_friends': my_friends, 'bill_form': bill_form, 'userprofile_object': userprofile_object, 'request': request }, context_instance=RequestContext(request))

@login_required
def settle_payment(request):
    userprofile_object = UserProfile.objects.get(user=request.user)
    if request.method == 'GET':
        payment_person_list = []
        class Payment_Person:
            def __init__(self, name, email):
                self.name = name
                self.email = email

        my_borrowers_masterlist = UserFriend.objects.filter(user_profile=userprofile_object).exclude(friend_email__iexact=userprofile_object.user.email)
        for my_borrower in my_borrowers_masterlist:
            temp = 0
            bill_details = BillDetails.objects.filter(bill__lender=userprofile_object, borrower=my_borrower, bill_cleared='N')
            if bill_details:
                temp = 1
            if temp == 1:
                borrower_name = my_borrower.friend_name
                borrower_email = my_borrower.friend_email
                payment_person = Payment_Person(name=borrower_name, email=borrower_email)
                payment_person_list.append(payment_person)

        my_lenders_masterlist = UserFriend.objects.filter(friend_email__iexact=userprofile_object.user.email).exclude(user_profile=userprofile_object)
        for my_lender in my_lenders_masterlist:
            temp = 0
            my_lender_as_user = UserProfile.objects.get(user__email__iexact=my_lender.user_profile.user.email)
            me_as_userfriend = UserFriend.objects.get(user_profile=my_lender_as_user, friend_email__iexact=userprofile_object.user.email)
            bills = Bill.objects.filter(lender=my_lender_as_user)
            for bill in bills:
                bill_details = BillDetails.objects.filter(bill=bill,borrower=me_as_userfriend, bill_cleared='N')
                if bill_details:
                    temp = 1
            if temp == 1:
                lender_name = my_lender_as_user.user.first_name + ' ' + my_lender_as_user.user.last_name
                try:
                    lender_name = UserFriend.objects.get(user_profile=userprofile_object, friend_email__iexact=my_lender_as_user.user.email).friend_name
                except:
                    pass
                lender_email = my_lender_as_user.user.email
                temp_b = 1 
                for payment_person in payment_person_list:
                    if lender_email == payment_person.email:
                        temp_b = 0
                        break
                if temp_b  == 1:
                    payment_person = Payment_Person(name=lender_name, email=lender_email)
                    payment_person_list.append(payment_person)
        payment_person_list.sort(key=lambda x: x.name)
        blank_element = Payment_Person(name='', email='blank_element')
        payment_person_list.insert(0, blank_element)
        return render_to_response('settle-payment.html', { 'payment_person_list': payment_person_list, 'userprofile_object': userprofile_object, 'request': request }, context_instance=RequestContext(request))

@login_required
def settle_payment_ajax(request):
    time.sleep(2)
    userprofile_object = UserProfile.objects.get(user=request.user)
    if request.method == 'GET' and request.is_ajax():
        payment_form = PartialBillDetailsForm()
        person = request.GET['person']
        if person != 'blank_element':
            base_function_results = base_function_net_outstanding(request, request.user.email, person)
            overall_template_variables = { 'payment_form': payment_form, 'person_email': person, 'userprofile_object': userprofile_object, 'request': request }
            overall_template_variables.update(base_function_results)
        else:
            overall_template_variables = { 'blank_element': True, 'person_email': person, 'userprofile_object': userprofile_object, 'request': request }
        return render_to_response('settle-payment-ajax.html', overall_template_variables, context_instance=RequestContext(request)) 
    else:
        pass

def base_function_settle_payment(request, userprofile_object, billdetails_list, person_email, individual_bill_cleared_date=date.today().strftime('%Y-%m-%d'), individual_bill_remarks=''):
    class Transaction():
        pass
    list_of_bills_cleared = []
    total_amount_cleared = {}

    temp_bill_status = False 
    
    for bill in billdetails_list:
        bill_detail = BillDetails.objects.get(billdetail_id=bill)
        if temp_bill_status is False:
            if bill_detail.bill_cleared == 'N':
                temp_bill_status = True 
        bill_detail.bill_cleared = 'Y'
        bill_detail.bill_cleared_date = individual_bill_cleared_date
        bill_detail.remarks = individual_bill_remarks
        bill_detail.save()

        if bill_detail.bill.lender == userprofile_object:
            try:
                total_amount_cleared[bill_detail.bill.currency] -= bill_detail.individual_amount
            except: 
                total_amount_cleared[bill_detail.bill.currency] = -bill_detail.individual_amount
        else:
            try:
                total_amount_cleared[bill_detail.bill.currency] += bill_detail.individual_amount
            except: 
                total_amount_cleared[bill_detail.bill.currency] = bill_detail.individual_amount

        transaction = Transaction()
        transaction.overall_bill_id = bill_detail.bill.overall_bill_id
        transaction.date = bill_detail.bill.date
        transaction.description = bill_detail.bill.description
        transaction.currency = bill_detail.bill.currency
        transaction.total_amount = bill_detail.bill.amount
        transaction.amount = bill_detail.individual_amount
        if bill_detail.bill.lender == userprofile_object:
            transaction.status = '+ve'
        else:
            transaction.status = '-ve'

        list_of_bills_cleared.append(transaction)

    # Start - Send Email
    if temp_bill_status is True:
        base_results_net_outstanding = base_function_net_outstanding(request, request.user.email, person_email)
        net_outstanding = base_results_net_outstanding['overall']
        context = Context({ 'userprofile_object': userprofile_object, 'list_of_bills_cleared': list_of_bills_cleared, 'total_amount_cleared': total_amount_cleared, 'remarks': individual_bill_remarks, 'net_outstanding': net_outstanding })
        subject = 'New Payment by: ' + userprofile_object.user.first_name + ' ' + userprofile_object.user.last_name
        payment_creation_txt_content = payment_creation_txt.render(context)
        payment_creation_html_content = payment_creation_html.render(context)
        send_mail(subject, payment_creation_txt_content, settings.DEFAULT_FROM_EMAIL, [ person_email ])
    # End - Send Email

    return list_of_bills_cleared

@login_required
def settle_payment_complete(request):
    userprofile_object = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        payment_form = PartialBillDetailsForm(request.POST)
        billdetails_list = request.POST.getlist('billdetail_id')
        if not billdetails_list:
            return render_to_response('settle-payment-error.html', { 'request': request }, context_instance=RequestContext(request))
        else:
            if payment_form.is_valid():
                person_name = request.POST['person_name']
                person_email = request.POST['person']
                individual_bill_cleared_date = payment_form.cleaned_data['date']
                individual_bill_remarks = payment_form.cleaned_data['remarks']
                list_of_bills_cleared = base_function_settle_payment(request, userprofile_object, billdetails_list, person_email, individual_bill_cleared_date, individual_bill_remarks)
                return render_to_response('settle-payment-success.html', { 'person_name': person_name, 'list_of_bills_cleared': list_of_bills_cleared, 'request': request }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/settle-payment/')

@login_required
def who_i_owe(request):
    userprofile_object = UserProfile.objects.get(user=request.user)
    me_as_borrower = UserFriend.objects.filter(friend_email__iexact=userprofile_object.user.email)

    class My_Lender:
        def __init__(self, lender_name, bill_date, bill_description, bill_currency, bill_individual_amount, bill_overall_bill_id):
            self.lender_name = lender_name
            self.bill_date = bill_date
            self.bill_description = bill_description
            self.bill_currency = bill_currency
            self.bill_individual_amount = bill_individual_amount
            self.bill_overall_bill_id = bill_overall_bill_id
    my_lender_list = []
    bill_details_my_lenders = BillDetails.objects.filter(borrower__in=me_as_borrower, bill_cleared='N').exclude(bill__lender=userprofile_object).order_by('bill__lender')
    for bill_detail in bill_details_my_lenders:
        try:
            lender_name = UserFriend.objects.get(user_profile=userprofile_object, friend_email__iexact=bill_detail.bill.lender.user.email).friend_name
        except:
            lender_name = bill_detail.bill.lender.user.first_name + ' ' + bill_detail.bill.lender.user.last_name
        bill_date = bill_detail.bill.date
        bill_description = bill_detail.bill.description
        bill_currency = bill_detail.bill.currency
        bill_individual_amount = bill_detail.individual_amount
        bill_overall_bill_id = bill_detail.bill.overall_bill_id
        my_lender = My_Lender(lender_name=lender_name, bill_date=bill_date, bill_description=bill_description, bill_currency=bill_currency, bill_individual_amount=bill_individual_amount, bill_overall_bill_id=bill_overall_bill_id)
        my_lender_list.append(my_lender)
    return render_to_response('who-i-owe.html', { 'my_lenders': my_lender_list, 'userprofile_object': userprofile_object, 'request': request }, context_instance=RequestContext(request))

@login_required
def who_owes_me(request):
    userprofile_object = UserProfile.objects.get(user=request.user)
    me_borrow_me = UserFriend.objects.get(user_profile=userprofile_object, friend_email__iexact=userprofile_object.user.email)
    my_borrowers = BillDetails.objects.filter(bill__lender=userprofile_object, bill_cleared='N').exclude(borrower=me_borrow_me).order_by('borrower')
    return render_to_response('who-owes-me.html', { 'my_borrowers': my_borrowers, 'userprofile_object': userprofile_object, 'request': request }, context_instance=RequestContext(request))

@login_required
def transaction_history(request):
    userprofile_object = UserProfile.objects.get(user=request.user)

    class Persons:
        def __init__(self, name, total_pending=0, total_cleared=0, slug=''):
            self.name = name
            self.total_pending = total_pending
            self.total_cleared = total_cleared
            self.slug = slug

    persons_list = []
    borrower_also_lender_list = []

    my_borrowers = UserFriend.objects.filter(user_profile=userprofile_object).exclude(friend_email__iexact=userprofile_object.user.email).extra(select={'lower_name': 'lower(friend_name)'}).order_by('lower_name') # lower() works only with Postgres
    for each_borrower in my_borrowers:
        total_pending = 0
        total_cleared = 0
        each_borrower_bills = BillDetails.objects.filter(bill__lender=userprofile_object, borrower=each_borrower)
        if each_borrower_bills:
            for each_bill in each_borrower_bills:
                if each_bill.bill_cleared == 'N':
                    total_pending += 1
                elif each_bill.bill_cleared == 'Y':
                    total_cleared += 1
            try:
                borrower_as_user = UserProfile.objects.get(user__email__iexact=each_borrower.friend_email)
                try: 
                    me_as_borrower = UserFriend.objects.get(user_profile=borrower_as_user, friend_email__iexact=userprofile_object.user.email)
                    borrower_also_lender_list.append(each_borrower.friend_email)
                    each_borrower_as_lender_bills = BillDetails.objects.filter(bill__lender=borrower_as_user, borrower=me_as_borrower)
                    if each_borrower_as_lender_bills:
                        for each_bill in each_borrower_as_lender_bills:
                            if each_bill.bill_cleared == 'N':
                                total_pending += 1
                            elif each_bill.bill_cleared == 'Y':
                                total_cleared += 1
                except:
                    pass
            except:
                pass
            person = Persons(name=each_borrower.friend_name, total_pending=total_pending, total_cleared=total_cleared, slug=each_borrower.userfriend_id)
            persons_list.append(person)

    borrower_also_lender_userprofiles = []
    if borrower_also_lender_list:
        for borrower_also_lender in borrower_also_lender_list:
            borrower_also_lender_userprofile = UserProfile.objects.get(user__email__iexact=borrower_also_lender)
            borrower_also_lender_userprofiles.append(borrower_also_lender_userprofile)

    # To find out who the 'pure' lenders are. Basically exclude the borrower also lender list as that is done above already
    my_lenders = UserFriend.objects.filter(friend_email__iexact=userprofile_object.user.email).exclude(user_profile=userprofile_object).exclude(user_profile__in=borrower_also_lender_userprofiles)
    
    for each_lender in my_lenders:
        total_pending = 0
        total_cleared = 0
        userprofile_lender = UserProfile.objects.get(user__email__iexact=each_lender.user_profile.user.email)
        borrower = UserFriend.objects.get(user_profile=userprofile_lender, friend_email__iexact = userprofile_object.user.email)
        each_lender_bills = BillDetails.objects.filter(bill__lender=userprofile_lender, borrower=borrower)
        if each_lender_bills: 
            for each_bill in each_lender_bills:
                if each_bill.bill_cleared == 'N':
                    total_pending += 1
                elif each_bill.bill_cleared == 'Y':
                    total_cleared += 1
            name = each_lender.user_profile.user.first_name + ' ' + each_lender.user_profile.user.last_name
            slug = userprofile_lender.userprofile_id
            person = Persons(name=name, total_pending=total_pending, total_cleared=total_cleared, slug=slug) 
            persons_list.append(person)

    return render_to_response('transaction-history.html', { 'persons_list': persons_list, 'request': request }, context_instance=RequestContext(request))

@login_required
def transaction_history_details(request, person_id):
    userprofile_object = UserProfile.objects.get(user=request.user)

    class Transactions:
        def __init__(self, date, lender, borrower, description, currency, individual_amount, status, slug, detail_id):
            self.date = date
            self.lender = lender
            self.borrower = borrower
            self.description = description
            self.currency = currency 
            self.individual_amount = individual_amount
            self.status = status
            self.slug = slug
            self.detail_id = detail_id

    if request.method == 'GET':
        if person_id[:3] == 'uf_':
            person = 'borrower_and_lender'
        else:
            person = 'lender'

        if person == 'borrower_and_lender':
            bill_list = []

            # Start - First as borrower
            userfriend_id = person_id
            person_borrower = UserFriend.objects.get(user_profile=userprofile_object, userfriend_id=userfriend_id)
            person_name = person_borrower.friend_name
            person_borrower_bills = BillDetails.objects.filter(bill__lender=userprofile_object, borrower=person_borrower).order_by('-bill__date')
            for each_bill in person_borrower_bills:
                lender = 'Me'
                transaction = Transactions(date=each_bill.bill.date, lender=lender, borrower=person_name, description=each_bill.bill.description, currency=each_bill.bill.currency, individual_amount=each_bill.individual_amount, status=each_bill.bill_cleared, slug=each_bill.bill.overall_bill_id, detail_id=each_bill.billdetail_id)
                bill_list.append(transaction)
            # End - First as borrower
            
            # Start - Second as lender
            person_email = person_borrower.friend_email
            try: 
                person_as_lender = UserProfile.objects.get(user__email__iexact=person_email)
                me_as_borrower = UserFriend.objects.get(user_profile=person_as_lender, friend_email__iexact=userprofile_object.user.email)
                person_lender_bills = BillDetails.objects.filter(bill__lender=person_as_lender, borrower=me_as_borrower).order_by('-bill__date')
                for each_bill in person_lender_bills:
                    borrower = 'Me'
                    transaction = Transactions(date=each_bill.bill.date, lender=person_name, borrower=borrower, description=each_bill.bill.description, currency=each_bill.bill.currency, individual_amount=each_bill.individual_amount, status=each_bill.bill_cleared, slug=each_bill.bill.overall_bill_id, detail_id=each_bill.billdetail_id)
                    bill_list.append(transaction)
            except:
                pass
            # End - Second as lender

            return render_to_response('transaction-history-details.html', { 'bill_list': bill_list, 'person_name': person_name, 'request': request }, context_instance=RequestContext(request))

        elif person == 'lender':
            bill_list = []
            userprofile_id = person_id
            
            person_as_lender = UserProfile.objects.get(userprofile_id=userprofile_id)
            person_name = person_as_lender.user.first_name + ' ' + person_as_lender.user.last_name
            me_as_borrower = UserFriend.objects.get(user_profile=person_as_lender, friend_email__iexact=userprofile_object.user.email)
            person_lender_bills = BillDetails.objects.filter(bill__lender=person_as_lender, borrower=me_as_borrower).order_by('-bill__date')
            for each_bill in person_lender_bills:
                borrower = 'Me'
                transaction = Transactions(date=each_bill.bill.date, lender=person_name, borrower=borrower, description=each_bill.bill.description, currency=each_bill.bill.currency, individual_amount=each_bill.individual_amount, status=each_bill.bill_cleared, slug=each_bill.bill.overall_bill_id, detail_id=each_bill.billdetail_id)
                bill_list.append(transaction)

            return render_to_response('transaction-history-details.html', { 'bill_list': bill_list, 'person_name': person_name, 'request': request }, context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect('/transaction-history/')

def specific_bill_details(request, view_status, overall_bill_id):
    class Error:
        pass
    error = Error()
    if request.method == 'POST' and request.user.is_authenticated():
        userprofile_object = UserProfile.objects.get(user=request.user)
        if 'mark_bill_paid' in request.POST:
            bill = Bill.objects.get(overall_bill_id=overall_bill_id)
            if 'lender_as_user_yes' in request.POST: 
                bill_details = BillDetails.objects.filter(bill=bill)
                for bill_detail in bill_details:
                    bill_detail.bill_cleared = 'Y'
                    bill_detail.bill_cleared_date = date.today().strftime('%Y-%m-%d')
                    bill_detail.save()
                redirect_url = '/bill/details/s/'+ str(bill.overall_bill_id) + '/'
                return HttpResponseRedirect(redirect_url)
                #return HttpResponseRedirect('/home/')
            else:
                lender_as_user = UserProfile.objects.get(user__email__iexact=request.POST['lender'])
                user_friend = UserFriend.objects.get(user_profile=lender_as_user, friend_email__iexact=userprofile_object.user.email)
                person_name = lender_as_user.user.first_name + ' ' + lender_as_user.user.last_name
                person_email = lender_as_user.user.email
                #billdetail = BillDetails.objects.get(bill=bill, borrower=user_friend)
                #billdetails_list = [ billdetail.billdetail_id ]
                billdetails_list = []
                billdetails = BillDetails.objects.filter(bill=bill, borrower=user_friend)
                for billdetail in billdetails:
                    billdetails_list.append(billdetail.billdetail_id)
                list_of_bills_cleared = base_function_settle_payment(request, userprofile_object, billdetails_list, person_email)
                return render_to_response('settle-payment-success.html', { 'person_name': person_name, 'list_of_bills_cleared': list_of_bills_cleared, 'request': request }, context_instance=RequestContext(request))

        elif 'delete_bill' in request.POST:
            bill = Bill.objects.get(overall_bill_id=overall_bill_id)
            if bill.lender == userprofile_object:
                user_as_own_friend = UserFriend.objects.get(user_profile=userprofile_object, friend_email=userprofile_object.user.email)
                bill_details = BillDetails.objects.filter(bill=bill)
                delete_status = 'Y'
                for bill_detail in bill_details:
                    if bill_detail.borrower != user_as_own_friend:
                        if bill_detail.bill_cleared == 'Y':
                            delete_status = 'N'
                            break
                if delete_status == 'Y':
                    for bill_detail in bill_details:
                        bill_detail.delete()
                    bill.delete()
                    return HttpResponseRedirect('/home/')
            view_status = 'v'
            error.delete_error = 'Bill can\'t be deleted!'
    page_header = 'Bill Details'
    if view_status == 'c':
        page_header = 'Bill Created Successfully!'
    elif view_status == 'v':
        page_header = 'Bill Details'
    elif view_status == 's':
        page_header = 'Bill Settled Successfully!'

    try:
        bill = Bill.objects.get(overall_bill_id=overall_bill_id)
        borrowers = BillDetails.objects.filter(bill=bill)

        borrower_and_lender_one_only = False
        bill_paid_number_of_people = 0
        bill_paid_status = ''
        as_borrower_paid_already = True

        try:
            userprofile_object = UserProfile.objects.get(user=request.user)

            # Start - Doing this so that 'Me' always appears on top
            temp = []
            for borrower in borrowers:
                if borrower.borrower.friend_email == userprofile_object.user.email:
                    temp.append(borrower)
            for borrower in borrowers:
                if borrower.borrower.friend_email != userprofile_object.user.email:
                    temp.append(borrower)
            borrowers = list(temp) 
            # End - Doing this so that 'Me' always appears on top

            lender_as_own_friend = UserFriend.objects.get(user_profile=bill.lender, friend_email__iexact=bill.lender.user.email)
            bill_details = BillDetails.objects.filter(bill=bill)
            if bill.lender == userprofile_object:
                user_lender = True

                # Start - Only one bill detail where borrower and lender are the same
                if bill_details.count() == 1 and bill_details[0].borrower == lender_as_own_friend:
                    borrower_and_lender_one_only = True
                # End - Only one bill detail where borrower and lender are the same

                # Start - More than one bill detail or uniques. Nobody has paid yet, Some have paid, All have paid
                bill_details = bill_details.exclude(borrower=lender_as_own_friend)
                for bill_detail in bill_details:
                    if bill_detail.bill_cleared == 'Y':
                        bill_paid_number_of_people += 1
                if bill_paid_number_of_people == 0:
                    bill_paid_status = 'None'
                elif bill_paid_number_of_people == bill_details.count():
                    bill_paid_status = 'All'
                else:
                    bill_paid_status = 'Some'
                # End - Multiple borrowers. Nobody has paid yet, Some have paid, All have paid
            else:
                user_lender = False
                # Didn't do as per the next 2 lines because user might have mistakenly entered borrower email twice
                # bill_detail = BillDetails.objects.get(bill=bill, borrower__friend_email=userprofile_object.user.email)
                # bill_status = bill_detail.bill_cleared
                for bill_detail in bill_details:
                    if bill_detail.borrower.friend_email == userprofile_object.user.email:
                        if bill_detail.bill_cleared == 'N':
                            as_borrower_paid_already = False 
                            break
        except:
            userprofile_object = ''
            user_lender = False

        return render_to_response('specific-bill-details.html', { 'page_header': page_header, 'bill': bill, 'borrowers': borrowers, 'user_lender': user_lender, 'borrower_and_lender_one_only': borrower_and_lender_one_only, 'bill_paid_status': bill_paid_status, 'as_borrower_paid_already': as_borrower_paid_already, 'view_status': view_status, 'error': error, 'userprofile_object': userprofile_object, 'request': request }, context_instance=RequestContext(request))
    except:
        return render_to_response('404.html', { 'request': request }, context_instance=RequestContext(request))

@login_required
def my_profile(request):
    userprofile_object = UserProfile.objects.get(user=request.user)
    my_friends_count = UserFriend.objects.filter(user_profile=userprofile_object, friend_deleted='N').exclude(friend_email__iexact=userprofile_object.user.email).count()
    edit = False 
    email = ''
    class Error:
        pass
    error = Error()
    if request.method == 'POST':
        if request.POST['edit_or_save'] == 'save':
            userprofile_form = UserProfileForm(request.POST)
            if userprofile_form.is_valid():
                userprofile_object.currency = userprofile_form.cleaned_data['currency']
                userprofile_object.save()
                request.user.first_name = request.POST['first_name']
                try: 
                    request.user.last_name = request.POST['last_name']
                except:
                    pass
                request.user.save()
                user_as_own_friend = UserFriend.objects.get(user_profile=userprofile_object,friend_email=userprofile_object.user.email)
                user_as_own_friend.friend_name = request.user.first_name + ' ' + request.user.last_name 
                user_as_own_friend.save()
                email = request.POST['email']
                if validate_email(email):
                    if not User.objects.filter(email__iexact=email).exclude(email__iexact=userprofile_object.user.email).exists():
                        request.user.username = request.user.email = email
                        request.user.save()
                        user_as_own_friend.friend_email = email
                        user_as_own_friend.save()
                        userprofile_object = UserProfile.objects.get(user=request.user)
                        return render_to_response('my-profile.html', { 'userprofile_object': userprofile_object, 'my_friends_count': my_friends_count, 'request': request }, context_instance=RequestContext(request))
                    else:
                        error.email_exists='Email already exists!'
                else:
                    error.email_invalid = 'Invalid email address'
        userprofile_form = UserProfileForm({ 'currency': userprofile_object.currency })
        edit = True
        return render_to_response('my-profile.html', { 'edit': edit, 'error': error, 'email': email, 'userprofile_object': userprofile_object, 'userprofile_form': userprofile_form, 'my_friends_count': my_friends_count, 'request': request }, context_instance=RequestContext(request))
    return render_to_response('my-profile.html', { 'userprofile_object': userprofile_object, 'my_friends_count': my_friends_count, 'request': request }, context_instance=RequestContext(request))

def validate_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

@login_required
def change_password(request):
    class Error:
        pass
    error = Error()
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']
        if old_password and new_password1 and new_password2:
            if request.user.check_password(old_password):
                if new_password1 == new_password2:
                    request.user.set_password(new_password1)
                    request.user.save()
                    return HttpResponseRedirect('/change-password-success/')
                else:
                    error.new_password = 'New passwords don\'t match. Try again'
            else: 
                error.old_password = 'Incorrect password'
        else:
            error.old_password = 'Please enter all fields'
    return render_to_response('change-password.html', { 'error': error, 'request': request }, context_instance=RequestContext(request))

@login_required
def change_password_success(request):
    return render_to_response('change-password-success.html', { 'request': request }, context_instance=RequestContext(request))

@login_required
def logout_user(request):
	auth_logout(request)
	return HttpResponseRedirect('/') 

def feedback(request):
    feedback_form = FeedbackForm()
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback_form.save() 

            # Start - Send Email 
            name = feedback_form.cleaned_data['name']
            email = feedback_form.cleaned_data['email']
            message = feedback_form.cleaned_data['message']
            context = Context({ 'name': name, 'email': email, 'message': message })
            subject = 'New Feedback by: ' + name
            feedback_txt_content = feedback_txt.render(context)
            feedback_html_content = feedback_html.render(context)
            send_mail(subject, feedback_txt_content, settings.DEFAULT_FROM_EMAIL, [ 'arpitrai@bridgebill.com', 'arpitrai@gmail.com' ])
            # End - Send Email

            return HttpResponseRedirect('/feedback/confirmation')
    return render_to_response('feedback.html', { 'feedback_form': feedback_form, 'request': request }, context_instance=RequestContext(request))

# Start - To set user's currency based on the IP -- CURRENTLY DOES NOT WORK BECAUSE SIGNALS SHOULD BE IN MAIN THREAD
def add_default_currency(request, userprofile_object):
    if not userprofile_object.currency:
        def handler(signum, frame):
            raise Exception

        def get_ip_country():
            ip = request.META['REMOTE_ADDR']
            ip_url_for_hostipapi = 'http://api.hostip.info/get_json.php?ip=' + str(ip) + ')'
            ip_details = urllib.urlopen(ip_url_for_hostipapi).read()
            ip_details_json = json.loads(ip_details)
            return ip_details_json['country_code']

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(2) # Set the timeout in seconds here. If it is greater than t seconds, skip the function

        try:
            country_code = get_id_country()
            if country_code == 'IN':
                userprofile_object.currency = 'INR'
            elif country_code == 'SG':
                userprofile_object.currency = 'SGD'
            elif country_code == 'US':
                userprofile_object.currency = 'USD'
            else:
                userprofile_object.currency = 'SGD'
            userprofile_object.currency.save()
        except Exception:
            pass
    return True
# End - To set user's currency based on the IP -- CURRENTLY DOES NOT WORK BECAUSE SIGNALS SHOULD BE IN MAIN THREAD

# Start - For making changes to a table / deleting a table
from django.db import connection, transaction
def change_table_heroku(request):
    cursor = connection.cursor()
    cursor.execute("UPDATE bridgebill_bill set currency='SGD';")
    transaction.commit_unless_managed()
    return HttpResponse('<p>Success!</p>')
# End - For making changes to a table / deleting a table
