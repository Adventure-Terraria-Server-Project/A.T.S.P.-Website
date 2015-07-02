            {% extends "layout.tpl" %}
            {% block content %}
            <div class="row content">
                <div class="col-md-12">
                    <h2 class="text-success text-center">{{name}}</h2>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div class="alert alert-danger"><strong>Oh Snap!</strong> The page you are searching for is not here... Go back to the Dash or the Main-Site.</div>
                        {% if user_data['user'][0] == 'Login' %}<p class="text-warning">You are not logged in. Some pages are only accessible if you are logged in.<br>
                        Make sure, that you click on "<strong>Login</strong>" and enter your ingame login credentials and try to access the page again.</p>{% endif %}
                    </div>
                </div>
            </div><br>{% endblock %}