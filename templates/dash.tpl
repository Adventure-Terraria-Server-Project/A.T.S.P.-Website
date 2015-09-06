{% extends 'layout.tpl' %}
            {% block content %}
            <div class="row content">
                <div class="col-md-12">
                    <h2 class="text-success text-center">{{ name }}</h2>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div class="panel panel-info">
                            <div class="panel-heading"><h3 class="panel-title"><span class="text-danger glyphicon glyphicon-stop"></span> Banned Items</h3></div>
                            <div class="panel-body">
                                <table class="table table-condensed"><tr>{{ b_items }}</tr></table>
                            </div>
                        </div>
                        {%- if nickban or ipban %}
                        <div class="panel panel-danger">
                            <div class="panel-heading"><h3 class="panel-title"><span class="glyphicon glyphicon-ban-circle"></span> You are banned</h3></div>
                            <div class="panel-body">
                                <table class="table table-hover table-bordered table-striped">
                                    <tr>
                                        <th>Nick/IP</th>
                                        <th>Banned By</th>
                                        <th>Reason</th>
                                        <th>ETA</th>
                                    </tr>
                                    {{ nickban }}
                                    {{ ipban }}
                                </table>
                            </div>
                        </div>
                        {%- endif %}
                        {%- if msgs %}
                        <div class="panel panel-primary">
                            <div class="panel-heading"><h3 class="panel-title"><span class="glyphicon glyphicon-envelope fa-spin"></span> Offline Messages <span class="badge alert-danger">{{ count }}</span></h3></div>
                            <div class="panel-body">{{ msgs }}</div>
                        </div>
                        {%- else %}
                        <h3 class="text-primary text-center">You don't have unread messages!</h3>
                        {%- endif %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {%- if user_data['staff'] %}
                        <h2 class="text-info text-center">User Reports</h2>
                        <table class="table table-bordered"><tr><th>ID</th><th>Reported by</th><th>Reported User</td><th>Reason</th></tr>{{ reports }}</table>
                        {%- endif %}
                        <div id="stats_server" style="width: 100%; height: 400px"></div>
                        <div id="stats_user" style="width: 100%; height: 400px"></div>
                        <div id="stats_browser" style="width: 100%; height: 400px"></div>
                        <div id="stats_pages" style="width: 100%; height: 400px"></div>
                        {%- if user_data['user'][1] == 'superadmin' %}
                        <div id="backups" style="width: 100%; height: 400px"></div>
                        {%- endif %}
                    </div>
                </div>
            </div>
            <br>
            {%- endblock %}