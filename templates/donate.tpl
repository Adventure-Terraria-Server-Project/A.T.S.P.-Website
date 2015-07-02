            {% extends "layout.tpl" %}
            {% block content %}
            <div class="row content">
                <div class="col-md-12 text-center">
                    <h2 class="text-success">{{name}}</h2>
                </div>
                <br>
                <div class="row text-center">
                    <div class="col-md-12">
                        <div class="alert alert-danger"><strong>Attention!</strong> You need to be <strong>logged in</strong> to donate. Click on "Login" and type in your <strong>ingame nick and password</strong> and visit this site again.</div>
                        <div class="panel-group" id="accordion">
                            <div class="panel panel-success">
                                <div class="panel-heading" data-toggle="collapse" data-parent="#accordion" data-target="#collapseOne">
                                    <h4 class="panel-title"><span class="glyphicon glyphicon-gift"></span> Donate with a PayPal Account</h4>
                                </div>
                                <div id="collapseOne" class="panel-collapse collapse in">
                                    <div class="panel-body">
                                        <div class="alert alert-info" role="alert">Simply click on this button to support us with a donation on PayPal.</div>
                                        <a class="btn btn-lg btn-warning" href="/donate_paypal" target="_blank" rel="nofollow"><span class="glyphicon glyphicon-chevron-right"></span> Donate via PayPal <span class="glyphicon glyphicon-chevron-left"></span></a>
                                    </div>
                                </div>
                            </div>
                            <div class="panel panel-success">
                                <div class="panel-heading" data-toggle="collapse" data-parent="#accordion" data-target="#collapseTwo">
                                    <h4 class="panel-title"><span class="fa fa-external-link"></span> Donating without a PayPal Account</h4>
                                </div>
                                <div id="collapseTwo" class="panel-collapse collapse">
                                    <div class="panel-body">
                                        <div class="alert alert-danger" role="alert">Our preferred method of donation is PayPal, but if for some reason you can not or do not have access to a PayPal account, you can also donate via Fundrazr.</div>
                                        <ol>
                                            <li>Go to our <a href="/donate_fundrazr" target="_blank" rel="nofollow">Fundrazr</a> page</li>
                                            <li>Press the GIVE Button: <img src="fund_give.png" alt=""></li>
                                            <li>Select at least 5€ (<i>you can set a lower custom amount, but you wouldn't get VIP</i>) - press Continue</li>
                                            <li>Press continue to PayPal, a new window should open now.</li>
                                            <li>Click on "Buy as guest" <img src="fund_guest.png" alt=""> and fill out the form</li>
                                            <li>Thats it, we get notified about your donation. Now write your email-address or real name to <a href="http://terrariaforum.yamahi.eu/messages/add/Yama" target="_blank" rel="nofollow">Yama</a> with your Charactername</li>
                                        </ol>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                {% if user_data['staff'] %}{{donated}}{% endif %}
            </div>
            <br>{% endblock %}
