{% extends 'layout.tpl' %}
            {% block content %}
            <div class="row content">
                <div class="col-md-12">
                    <h2 class="text-success text-center">{{ name }}</h2>
                </div>
                <div class="row">
                    <div style="position: fixed">
                        <ul class="nav nav-pills nav-stacked">
                            <li class="active"><a href="#nick" data-toggle="tab"><span class="glyphicon glyphicon-user"></span> Nick</a></li>
                            <li><a href="#ip" data-toggle="tab"><span class="glyphicon glyphicon-globe"></span> IP</a></li>
                            <li><a href="#" id="toTop"><span class="glyphicon glyphicon-chevron-up"></span> To Top</a></li>
                            <li><a href="#" id="toBottom"><span class="glyphicon glyphicon-chevron-down"></span> To Bottom</a></li>
                        </ul>
                    </div>
                    <div class="col-md-2" style="visibility: hidden">
                        <ul class="nav nav-pills nav-stacked">
                            <li><a href="#">Nick</a></li>
                        </ul>
                    </div>
                    <div class="col-md-10">
                        <div class="tab-content">
                            <div class="tab-pane fade in active" id="nick"><table class="table table-bordered">{{ nickbans }}</table></div>
                            <div class="tab-pane fade" id="ip"><table class="table table-bordered">{{ ipbans }}</table></div>
                        </div>
                    </div>
                </div>
            </div>
            <br>
            {%- endblock %}