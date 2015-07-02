            {% extends "layout.tpl" %}
            {% block content %}
            <div class="row content">
                <div class="col-md-12">
                    <h2 class="text-success text-center">{{name}}</h2>
                </div>
                <div class="row">
                    <div class="col-md-12">{% if staff %}
                        <form class="text-center" role="form" method="POST" action="/motd_rules">
                            <div class="form-group">
                                <h3 class="text-danger">Rules</h2>
                                <textarea class="form-control" name="rules" type="text" rows="7">{{moru['rules']}}</textarea>
                            </div><br>
                            <div class="form-group">
                                <h3 class="text-danger">MOTD</h2>
                                <textarea class="form-control" name="motd" type="text" rows="7">{{moru['motd']}}</textarea>
                            </div><br>
                            <button type="submit" value="Send" class="btn btn-primary"><span class="glyphicon glyphicon-floppy-disk"></span> Save All</button>
                        </form>{% else %}
                        <div class="panel panel-primary">
                            <div class="panel-heading">
                                <h3 class="panel-title text-center">Rules</h3>
                            </div>
                            <div class="panel-body">{{moru['rules']}}</div>
                        </div><br>
                        <div class="panel panel-success">
                            <div class="panel-heading text-center">
                                <h3 class="panel-title">MOTD</h3>
                            </div>
                            <div class="panel-body">{{moru['motd']}}</div>
                        </div>{% endif %}
                    </div>
                </div>
            </div>
            <br>{% endblock %}