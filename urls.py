from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from bridgebill import views

# For serving static files on development environment
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.login),
    #url(r'^$', 'django.contrib.auth.views.login', { 'template_name': 'index.html' }),
    url(r'^login-error$', views.login_error),

    url(r'^home/$', views.home),
    url(r'^home/details/(?P<person_id>[a-zA-Z0-9_-]+)/$', views.home_details),
    url(r'^bill/details/(?P<view_status>[a-zA-Z0-9_-])/(?P<overall_bill_id>[a-zA-Z0-9_-]+)/$', views.specific_bill_details),
    url(r'^user/sign-up/$', views.user_signup),
    url(r'^user/forgot-password/$', 'django.contrib.auth.views.password_reset',{ 'template_name':'forgot-password.html', 'email_template_name':'email_templates/password_reset.txt', 'post_reset_redirect': '/user/forgot-password/password-reset-initiated/' } ),
    url(r'^user/forgot-password/password-reset-initiated/$', 'django.contrib.auth.views.password_reset_done',{ 'template_name':'forgot-password-confirmation.html' } ),
    url(r'^user/forgot-password/password-reset-form/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',{ 'template_name':'forgot-password-actual-form.html', 'post_reset_redirect': '/user/forgot-password/password-reset-complete/' } ),
    url(r'^user/forgot-password/password-reset-complete/$', 'django.contrib.auth.views.password_reset_complete',{ 'template_name':'forgot-password-success.html' } ),
    #url(r'^record-bill/$', views.record_bill_option),
    url(r'^record-bill/$', views.record_bill),
    url(r'^record-bill/equal-split/$', views.record_bill_equal_split),
    url(r'^record-bill/unequal-split/$', views.record_bill_unequal_split),
    url(r'^settle-payment/$', views.settle_payment),
    url(r'^settle-payment-ajax/$', views.settle_payment_ajax),
    url(r'^settle-payment/complete/$', views.settle_payment_complete),
    url(r'^who-i-owe/$', views.who_i_owe),
    url(r'^who-owes-me/$', views.who_owes_me),
    url(r'^transaction-history/$', views.transaction_history),
    url(r'^transaction-history/details/(?P<person_id>[a-zA-Z0-9_-]+)/$', views.transaction_history_details),
    url(r'^my-profile/$', views.my_profile),
    url(r'^my-profile/my-friends/$', views.my_friends),
    url(r'^my-profile/my-friends/edit-friend/(?P<userfriend_id>[a-zA-Z0-9_-]+)/$', views.edit_friend), # AJAX
    url(r'^my-profile/my-friends/delete-friend/(?P<userfriend_id>[a-zA-Z0-9_-]+)/$', views.delete_friend), # AJAX
    url(r'^my-profile/my-friends/add-friend/$', views.add_friend), # AJAX
    url(r'^my-profile/change-password/$', views.change_password),
    url(r'^my-profile/change-password-success/$', views.change_password_success),
    url(r'^logout/$', views.logout_user),
    url(r'^about-us/$', direct_to_template, { 'template': 'about-us.html' }),
    url(r'^feedback/$',  views.feedback),
    url(r'^feedback/confirmation$', direct_to_template, { 'template': 'feedback_success.html' }),
    url(r'^contact-us/$', direct_to_template, { 'template': 'contact-us.html' }),

    # For making changes to table
    #url(r'^change_table/$',  views.change_table_heroku),

    url(r'', include('social_auth.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# For serving static files on development environment
urlpatterns += staticfiles_urlpatterns()
