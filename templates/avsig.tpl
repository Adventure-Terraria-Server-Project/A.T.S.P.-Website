            {% extends "layout.tpl" %}
            {% block content %}
            <div class="row content">
                <div class="col-md-12">
                    <h2 class="text-success text-center">{{name}}</h2>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div class="text-center alert alert-warning">Embed your character in other forums and websites!</div>
                    </div>
                    <div class="col-md-2"></div>
                    <div class="col-md-8 text-center">
                        <img src="{{ava}}"> <img src="{{sig}}"><br><br>
                        <div class="panel panel-info">
                            <div class="panel-heading">BBCode for Forums</div>
                            <div class="panel-body">
                                <code>[IMG]{{ava}}[/IMG]</code><br>
                                <code>[IMG]{{sig}}[/IMG]</code>
                            </div>
                        </div>
                        <div class="panel panel-primary">
                            <div class="panel-heading">HTML for Websites, Blogs and our Forum</div>
                            <div class="panel-body">
                                <code>&#60;a href="http://yamahi.eu"&#62;&#60;img src="{{ava}}"&#62;&#60;/a&#62;</code><br>
                                <code>&#60;a href="http://yamahi.eu"&#62;&#60;img src="{{sig}}"&#62;&#60;/a&#62;</code>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-2"></div>
                    </div>
                </div><br>{% endblock %}