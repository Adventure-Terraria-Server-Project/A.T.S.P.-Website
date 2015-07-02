            {% extends "layout.tpl" %}
            {% block content %}
            <div class="row content">
                <div class="col-md-12">
                    <h2 class="text-success text-center">{{name}}</h2>
                </div>
                <div class="row">
                    <div style="position: fixed">
                        <ul class="nav nav-pills nav-stacked">
                            <li class="active"><a href="#tshock" data-toggle="tab"><span class="glyphicon glyphicon-chevron-right"></span> tShock</a></li>
                            <li><a href="#utils" data-toggle="tab"><span class="glyphicon glyphicon-chevron-right"></span> Utils</a></li>
                            <li><a href="#imanager" data-toggle="tab"><span class="glyphicon glyphicon-chevron-right"></span> Item Manager</a></li>
                            <li><a href="#ptrace" data-toggle="tab"><span class="glyphicon glyphicon-chevron-right"></span> Plugin Trace</a></li>
                            <li><a href="#log" data-toggle="tab"><span class="glyphicon glyphicon-chevron-right"></span> Log</a></li>
                            <li><a href="#commands" data-toggle="tab"><span class="glyphicon glyphicon-chevron-right"></span> Commands</a></li>
                            <li><a href="#slog" data-toggle="tab"><span class="glyphicon glyphicon-chevron-right"></span> ServerLog</a></li>
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
                            <li><a href="#">Nick</a></li>
                            <li><a href="#">Nick</a></li>
                            <li><a href="#">Nick</a></li>
                            <li><a href="#">Nick</a></li>
                        </ul>
                    </div>
                    <div class="col-md-10">
                        <div class="tab-content">
                            <div class="tab-pane fade in active" id="tshock">{{logs['tshock']}}</div>
                            <div class="tab-pane fade" id="utils">{{logs['utils']}}</div>
                            <div class="tab-pane fade" id="imanager">{{logs['imanager']}}</div>
                            <div class="tab-pane fade" id="ptrace">{{logs['ptrace']}}</div>
                            <div class="tab-pane fade" id="log">{{logs['log']}}</div>
                            <div class="tab-pane fade" id="commands">{{logs['commands']}}</div>
                            <div class="tab-pane fade" id="slog">{{logs['slog']}}</div>
                        </div>
                    </div>
                </div>
            </div>
            <br>{% endblock %}