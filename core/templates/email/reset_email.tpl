{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account Activation
{% endblock %}

{% block html %}
http://127.0.0.1:8000/accounts/api/v1/reset-password/confirm/{{ token }}
{% endblock %}