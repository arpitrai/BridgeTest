def fill_user_details(backend, details, response, user, is_new=False, *args,**kwargs):
    """Fills user details using data from provider, without overwriting
    existing values.

    backend: Current social authentication backend
    details: User details given by authentication provider
    response: ?
    user: User ID given by authentication provider
    is_new: flag

    source: social_auth.backends.pipeline.user.update_user_details
    """
    # Each pipeline entry must return a dict or None, any value in the dict
    # will be used in the kwargs argument for the next pipeline entry.
    #
    # If any function returns something else beside a dict or None, the
    # workflow will be cut and the value returned immediately, this is useful
    # to return HttpReponse instances like HttpResponseRedirect.

    changed = False  # flag to track changes

    for name, value in details.iteritems():
        # do not update username, it was already generated
        if name in (USERNAME, 'id', 'pk'):
            continue

        # set it only if the existing value is not set or is an empty string
        existing_value = getattr(user, name, None)
        if value is not None and (existing_value is None or
                                  not is_valid_string(existing_value)):
            setattr(user, name, value)
            changed = True

    # Fire a pre-update signal sending current backend instance,
    # user instance (created or retrieved from database), service
    # response and processed details.
    #
    # Also fire socialauth_registered signal for newly registered
    # users.
    #
    # Signal handlers must return True or False to signal instance
    # changes. Send method returns a list of tuples with receiver
    # and it's response.
    signal_response = lambda (receiver, response): response
    signal_kwargs = {'sender': backend.__class__, 'user': user,'response': response, 'details': details}

    changed |= any(filter(signal_response, pre_update.send(**signal_kwargs)))

    # Fire socialauth_registered signal on new user registration
    if is_new:
        changed |= any(filter(signal_response,
            socialauth_registered.send(**signal_kwargs)))

    if changed:
        user.save()
    print 'Here'
