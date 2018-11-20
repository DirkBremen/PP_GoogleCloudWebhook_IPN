def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    def send_email(user, pwd, recipient, subject, body):
        import smtplib

        FROM = user
        TO = recipient if isinstance(recipient, list) else [recipient]
        SUBJECT = subject
        TEXT = body

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(user, pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print('successfully sent the mail')
        except:
            print("failed to send mail")
    import sys
    import urllib
    import requests

    VERIFY_URL_PROD = 'https://ipnpb.paypal.com/cgi-bin/webscr'
    VERIFY_URL_TEST = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'

    # Switch as appropriate
    VERIFY_URL = VERIFY_URL_TEST

    # CGI preamble
    print ('content-type: text/plain')
    print ()

    params = request.form.to_dict()

    # Add '_notify-validate' parameter
    params.update({'cmd':'_notify-validate'})

    # Post back to PayPal for validation

    headers = {'content-type': 'application/x-www-form-urlencoded',
               'user-agent': 'Python-IPN-Verification-Script'}
    r = requests.post(VERIFY_URL, params=params, headers=headers, verify=True)
    r.raise_for_status()
    
    # Check return message and take action as needed
    if r.text == 'VERIFIED':
        send_email("dirkpp74@gmail.com","ajCD@2018","bremendirk@gmail.com", "verified", params)
    elif r.text == 'INVALID':
        send_email("dirkpp74@gmail.com","ajCD@2018","bremendirk@gmail.com", "invalid", params)
    else:
        send_email("dirkpp74@gmail.com","ajCD@2018","bremendirk@gmail.com", "something else", params)