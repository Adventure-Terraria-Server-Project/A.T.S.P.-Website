            {% extends "layout.tpl" %}
            {% block content %}
            <div class="row content">
                <div class="col-md-12">
                    <h2 class="text-success text-center">{{name}}</h2>
                </div>
                <div class="row">
                    <div style="position: fixed">
                        <ul class="nav nav-pills nav-stacked">
                            <li class="active"><a href="#t" data-toggle="tab"><span class="glyphicon glyphicon-chevron-right"></span> Today</a></li>
                            <li><a href="#yd" data-toggle="tab"><span class="glyphicon glyphicon-chevron-right"></span> Yesterday</a></li>
                            <li><a href="#tda" data-toggle="tab"><span class="glyphicon glyphicon-chevron-right"></span> Two Days Ago</a></li>
                            <li><a href="#query" data-toggle="tab"><span class="glyphicon glyphicon-chevron-right"></span> Query</a></li>
                            <li><a href="#" id="toTop"><span class="glyphicon glyphicon-chevron-up"></span> To Top</a></li>
                            <li><a href="#" id="toBottom"><span class="glyphicon glyphicon-chevron-down"></span> To Bottom</a></li>
                        </ul>
                    </div>
                    <div class="col-md-2" style="visibility: hidden">
                        <ul class="nav nav-pills nav-stacked">
                            <li><a href="#">Nick</a></li>
                            <li><a href="#">Nick</a></li>
                            <li><a href="#">Nick</a></li>
                            <li><a href="#">Nick</a></li>
                            <li><a href="#">Nick</a></li>
                        </ul>
                    </div>
                    <div class="col-md-9">
                        <div class="tab-content">
                            <div class="tab-pane fade in active" id="t">{{logs[3]}}</div>
                            <div class="tab-pane fade" id="yd">{{logs[2]}}</div>
                            <div class="tab-pane fade" id="tda">{{logs[1]}}</div>
                            <div class="tab-pane fade" id="query">{{logs[0]}}</div>
                        </div>
                    </div>
                </div>
            </div>
            <br>{% endblock %}