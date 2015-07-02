            {% extends "layout.tpl" %}
            {% block content %}
            <div class="row content">
                <div class="col-md-12">
                    <h2 class="text-success text-center">{{name}}</h2>
                </div>
                <div class="row">
                    <div class="col-md-3"></div>
                    <div class="col-md-6">
                        <dl class="dl-horizontal">
                            {{rank}}
                        </dl>
                    </div>
                </div>
            </div>
            <br>{% endblock %}