<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{{ name }}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="description" content="This is our adventure Terraria Server with weekly world cycles, free build, free to explore and meaningful plugins!">
        <link rel="shortcut icon" href="favicon.ico">
        <!-- CSS -->
        <link rel="stylesheet" href="bootstrap.min.css">
        {%- if not user_data['mobile'] %}
        <link rel="stylesheet" href="bootstrap-theme.min.css">
        {%- endif %}
        <link rel="stylesheet" href="font-awesome.min.css">
        <link rel="stylesheet" href="custom.css">
    </head>
    <body>
        <div class="container">
            {%- if not user_data['mobile'] %}
            <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
            {%- else %}
            <nav class="navbar navbar-default navbar-static-top" role="navigation">
            {%- endif %}
                <div class="container">
                    <div class="navbar-header">
                        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                            <span class="sr-only">Toggle navigation</span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                        </button>
                        <a class="navbar-brand" href="/">A.T.S.P.</a>
                    </div>
                    <!-- Navbar -->
                    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                        <ul class="nav navbar-nav">
                            <li><a href="https://steamcommunity.com/groups/a_t_s_p/discussions"><span class="text-primary glyphicon glyphicon-tasks"></span> Message Board - Forums</a></li>
                            <li><a target="_blank" href="https://steamcommunity.com/groups/a_t_s_p"><i class="text-primary fa fa-steam fa-fw fa-lg"></i> Steam Group</a></li>
                            <li><a target="_blank" href="https://kiwiirc.com/client/irc.bakashimoe.me/#terraria-support,#Yamaria"><span class="text-primary glyphicon glyphicon-comment"></span> Chat</a></li>
                            <li><a href="irc://yamahi.eu:6667/Yamaria"><span class="text-primary glyphicon glyphicon-share-alt"></span> IRC Direct Link</a></li>
                            <li><a target="_blank" href="https://youtube.com/user/theflame90"><i class="text-primary fa fa-youtube fa-fw fa-lg"></i> Channel</a></li>
                        </ul>
                        <ul class="nav navbar-nav navbar-right">
                            {%- if user_data['user'][0] == 'Login' %}
                            <li class="active"><a data-toggle="modal" href="#loginModal"><span class="text-danger glyphicon glyphicon-user"></span> Login</a></li>
                            {%- else %}
                            <li class="dropdown">
                                <a data-toggle="dropdown" data-target="#" href="#"><span class="text-danger glyphicon glyphicon-user fa-lg"></span> {{ user_data['user'][0] }} <span class="caret"></span></a>
                                <ul class="dropdown-menu" role="menu">
                                    <li><a href="/dash"><i class="fa fa-list-alt"></i> Dash</a></li>
                                    {%- if user_data['staff'] %}
                                    <li><a href="/logs"><span class="glyphicon glyphicon-align-left"></span> Logs</a></li>
                                    <li><a href="/irclogs"><span class="glyphicon glyphicon-align-left"></span> IRC Logs</a></li>
                                    <li><a href="/bans"><span class="glyphicon glyphicon-list"></span> Ban List</a></li>
                                    <li><a href="/world-map"><span class="glyphicon glyphicon-picture"></span> World Map</a></li>
                                    <li><a href="/invpars"><span class="glyphicon glyphicon-th"></span> Inventory Parser</a></li>
                                    <li><a href="/searchuser"><span class="glyphicon glyphicon-search"></span> Search User</a></li>
                                    {%- elif user_data['user'][1] == 'vip++' %}
                                    <li><a href="/world-map-vip"><span class="glyphicon glyphicon-picture"></span> World Map</a></li>
                                    {%- elif user_data['user'][1] == 'supervip' %}
                                    <li><a href="/world-map"><span class="glyphicon glyphicon-picture"></span> World Map</a></li>
                                    {%- endif %}
                                    <li><a href="/motd-rules"><span class="glyphicon glyphicon-edit"></span> /motd &amp; /rules</a></li>
                                    <li><a href="/shorturl"><span class="glyphicon glyphicon-link"></span> URL Shortener</a></li>
                                    <li><a href="/embed"><span class="glyphicon glyphicon-picture"></span> Avatar &#38; Signature</a></li>
                                    <li><a href="/oldworlds"><span class="glyphicon glyphicon-download"></span> Old Worlds</a></li>
                                    <li><a href="#needhelp" data-toggle="modal"><span class="glyphicon glyphicon-question-sign fa-spin"></span> Need Help</a>
                                    <li><a href="/logout"><span class="glyphicon glyphicon-log-out"></span> Logout</a></li>
                                </ul>
                            </li>
                            {%- endif %}
                        </ul>
                    </div><!-- /.navbar-collapse -->
                </div>
            </nav>
            {%- if user_data['user'][0] == 'Login' %}
            <!-- Login Modal -->
            <div class="modal fade" id="loginModal">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                            <h4 class="modal-title"><span class="text-danger glyphicon glyphicon-log-in"></span> Login</h4>
                        </div>
                        <div class="modal-body">
                            <form class="form-horizontal" role="form" method="POST" action="/">
                                <div class="form-group">
                                    <label for="username" class="col-sm-2 control-label">Nickname</label>
                                    <div class="col-sm-10 input-group">
                                        <span class="input-group-addon"><span class="glyphicon glyphicon-user"></span></span>
                                        <input name="username" id="username" type="text" class="form-control" placeholder="Nickname">
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label for="password" class="col-sm-2 control-label">Password</label>
                                    <div class="col-sm-10 input-group">
                                        <span class="input-group-addon"><span class="glyphicon glyphicon-lock"></span></span>
                                        <input name="password" id="password" type="password" class="form-control" placeholder="Password">
                                    </div>
                                </div>
                                <button type="submit" class="btn btn-primary">Login</button>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <div class="progress progress-striped active">
                                <div class="progress-bar progress-bar-success"  role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>
                            </div>
                        </div>
                    </div><!-- /.modal-content -->
                </div><!-- /.modal-dialog -->
            </div><!-- /.modal -->
            {%- endif %}
            {#- {%- if not user_data['mobile'] %}
            <!-- News Modal - Cookie based -->
            <div class="modal fade" id="mainModal">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                            <h4 class="modal-title"><span class="text-danger glyphicon glyphicon-info-sign"></span> Did you know?</h4>
                        </div>
                        <div class="modal-body">
                            <p>You can login with your <strong>ingame Name and Password</strong> to get your personal Avatar and Signature with your own Character!<br>
                            VIP's have some more features.</p>
                            <p>If the Server asks for a Server Password, type in your own Password to login.</p>
                        </div>
                        <div class="modal-footer">
                            <div class="progress progress-striped active">
                                <div class="progress-bar"  role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>
                            </div>
                        </div>
                    </div><!-- /.modal-content -->
                </div><!-- /.modal-dialog -->
            </div><!-- /.modal -->
            {%- endif %} #}
            <!-- Need Help? Modal -->
            <div class="modal fade" id="needhelp">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                            <h4 class="modal-title"><span class="text-danger glyphicon glyphicon-question-sign"></span> Need Help</h4>
                        </div>
                        <div class="modal-body">
                            <dl class="dl-horizontal">
                                <dt><a target="_blank" href="https://steamcommunity.com/groups/a_t_s_p/discussions/0/617335934135479412/">Rules</a></dt>
                                <dd>Here are the rules</dd>
                                <dt><a target="_blank" href="https://steamcommunity.com/groups/a_t_s_p/discussions/0/617335934135388560/">How to contact Staff</a></dt>
                                <dd>How to efficiently contact Staff for help</dd>
                                <dt><a target="_blank" href="https://steamcommunity.com/groups/a_t_s_p/discussions/0/617335934135384358/">Guide</a></dt>
                                <dd>A detailed guide for new players - How to begin</dd>
                                <dt><a target="_blank" href="https://kiwiirc.com/client/irc.bakashimoe.me/#terraria-support,#Yamaria">IRC/Chat</a></dt>
                                <dd>If you directly want to chat (with staff), without being ingame</dd>
                                <dt><a target="_blank" href="https://steamcommunity.com/groups/a_t_s_p#announcements">News</a></dt>
                                <dd>All the News about A.T.S.P.</dd>
                                <dt><a target="_blank" href="https://steamcommunity.com/groups/a_t_s_p/discussions/0/">Information on A.T.S.P.</a></dt>
                                <dd>More details about Adventure Terraria Server Project</dd>
                            </dl>
                        </div>
                        <div class="modal-footer">
                            <div class="progress progress-striped active">
                                <div class="progress-bar"  role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>
                            </div>
                        </div>
                    </div><!-- /.modal-content -->
                </div><!-- /.modal-dialog -->
            </div><!-- /.modal -->
            {%- with msgs = get_flashed_messages() %}
                {%- if msgs %}
                    {%- for msg in msgs %}
            <div class="alert alert-success alert-dismissable">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                <span class="glyphicon glyphicon-info-sign"></span> {{ msg }}
            </div>
                    {%- endfor -%}
                {%- endif %}
            {%- endwith %}
            {%- block content %}
            {% endblock %}
            {%- if not user_data['mobile'] %}
            <div class="row well">
                <div class="col-md-12">
                    <footer>
                        <div class="col-md-4">
                            <ul>
                                <li><a target="_blank" href="https://twitter.com/ATSPTerraria">Twitter</a></li>
                                <li><a target="_blank" href="https://facebook.com/atsp.terraria">Facebook</a></li>
                                <li><a target="_blank" href="https://tserverweb.com/terraria-server/285/">TServerWeb</a></li>
                                <li><a target="_blank" href="http://terraria-server-list.com/server/316/">Terraria Server List</a></li>
                            </ul>
                        </div>
                        <div class="col-md-4">
                            <ul>
                                <li><a target="_blank" href="http://flask.pocoo.org">Flask</a></li>
                                <li><a target="_blank" href="https://python.org">Python</a></li>
                                <li><a target="_blank" href="https://jquery.com">JQuery</a></li>
                                <li><a target="_blank" href="http://getbootstrap.com">Bootstrap</a></li>
                            </ul>
                        </div>
                        <div class="col-md-4">
                            <ul>
                                <li>Kaimei</li>
                                <li><a target="_blank" href="http://tshock.co/xf/index.php?threads/dedicated-ssi-plugins-24-7-adventure-terraria-server-project-a-t-s-p.1687/">tShock</a></li>
                                <li><a target="_blank" href="https://terraria.org">Terraria</a></li>
                                <li><a target="_blank" href="https://github.com/Nama/A.T.S.P.-Website">Source on Github</a></li>
                            </ul>
                        </div>
                    </footer>
                </div>
            </div>
            <div id="bottombar">Recently Online: {{ user_data['recents'] }}</div>
            {%- endif %}
        </div>
        <!-- JavaScript -->
        <script src="jquery.min.js"></script>
        <script src="bootstrap.min.js"></script>
        <script src="custom.js"></script>
        {%- if request.path == '/oldworlds' %}
        <script type="text/javascript">
            var html_size = document.body.clientHeight;   // HTML content size
            var view = $(window).height();                // Window height
            var item = 0;
            function load() {
                next_url = "/get_worlds/" + item;
                $.ajax({
                    url: next_url,
                    cache: false,
                    async: false,
                    success: function( html ) {
                        $( "tbody.infinite-scroll" ).append( html );
                        item += 20;
                    }
                });
            };
            do {
                load();
                html_size = document.body.clientHeight;
            }
            while ( html_size <= view );
            $(window).scroll(function() {
                html_size = document.body.clientHeight;
                view = $( window ).height();
                if($(this).scrollTop() >= (html_size - view)*0.90 ) {
                    load();
                }
            });
        </script>
        {%- endif %}
        {%- if stats_server or backups %}
        <script src="highstock.js"></script>
        {%- endif %}
        {%- if stats_server %}
        <script type="text/javascript"><!--
            $(function () {
                $('#stats_server').highcharts({
                    chart: { type: 'areaspline' },
                    title: { text: 'Server User Statistics' },
                    rangeSelector: {
                        enabled: true,
                        selected: 0,
                        buttons: [{
                            text: '1d',
                            type: 'day',
                            count: 1,
                        },
                        {
                            text: '1w',
                            type: 'day',
                            count: 7,
                        },
                        {
                            text: '1m',
                            type: 'month',
                            count: 1,
                        },
                        {
                            text: '1y',
                            type: 'year',
                            count: 1,
                        },
                        {
                            text: 'All',
                            type: 'all',
                            count: 1,
                        }],
                        buttonTheme: { style: { width: '120px' }},
                    },
                    xAxis: { type: 'datetime', range: 1 * 24 * 3600 * 1000 },
                    yAxis: [{ // Regular Users Axis
                        title: { text: 'Peak Online Users' },
                        allowDecimals: false,
                        min: 0,
                    },
                    { // Staff Axis
                            title: { text: 'Staff Users' },
                            allowDecimals: false,
                            min: 0,
                            opposite: true,
                        }],
                    legend: {
                        enabled: false
                    },
                    series: [{
                        name: 'Total Users',
                        color: '#00ff18',
                        lineWidth: 1,
                        marker: { symbol: "circle", radius: 3 },
                        data: {{stats_server[0]}},
                        fillColor : {
                            linearGradient : {
                                x1: 0,
                                y1: 0,
                                x2: 0,
                                y2: 1
                            },
                            stops : [
                                [0, '#b3ffba'],
                                [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                            ]
                        }
                    },
                    {
                        name: 'Moderators',
                        color: '#dc6e28',
                        lineWidth: 1,
                        yAxis: 1,
                        marker: { symbol: "circle", radius: 3 },
                        data: {{stats_server[1]}},
                        fillColor : {
                            linearGradient : {
                                x1: 0,
                                y1: 0,
                                x2: 0,
                                y2: 1
                            },
                            stops : [
                                [0, '#ff8635'],
                                [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                            ]
                        }
                    },
                    {
                        name: 'Administrators',
                        color: '#c85050',
                        lineWidth: 1,
                        yAxis: 1,
                        marker: { symbol: "circle", radius: 3 },
                        data: {{stats_server[2]}},
                        fillColor : {
                            linearGradient : {
                                 x1: 0,
                                 y1: 0,
                                 x2: 0,
                                 y2: 1
                            },
                            stops : [
                                [0, '#ff6767'],
                                [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                            ]
                        }
                    }]
                });
            });
        --></script>
        {%- endif %}
        {%- if web_stats %}
        <script type="text/javascript"><!--
            $(function () {
                $('#stats_user').highcharts({
                    chart: { type: 'area'},
                    title: { text: 'User Visit Statistics'},
                    rangeSelector: {
                        enabled: true,
                        selected: 0,
                        buttons: [{
                            text: '1d',
                            type: 'day',
                            count: 1,
                        },
                        {
                            text: '1w',
                            type: 'day',
                            count: 7,
                        },
                        {
                            text: '1m',
                            type: 'month',
                            count: 1,
                        },
                        {
                            text: '1y',
                            type: 'year',
                            count: 1,
                        },
                        {
                            text: 'All',
                            type: 'all',
                            count: 1,
                        }],
                        buttonTheme: { style: { width: '120px' }},
                    },
                    navigator: {
                        enabled: true,
                        height: 20
                    },
                    legend: { enabled: false },
                    xAxis: { type: 'datetime', range: 5 * 24 * 3600 * 1000 },
                    yAxis: {
                        labels: {
                            formatter: function () {
                                return this.value / 1000;
                            }
                        }
                    },
                    tooltip: {
                        shared: true,
                    },
                    plotOptions: {
                        area: {
                            stacking: 'normal',
                            lineColor: '#666666',
                            lineWidth: 1,
                            marker: {
                                lineWidth: 1,
                                lineColor: '#666666'
                            }
                        }
                    },
                    series: [{
                        name: 'User',
                        data: {{web_stats['users']}},
                        stack: 'account'
                    }, {
                        name: 'Guest',
                        data: {{web_stats['guest']}},
                        stack: 'account'
                    }]
                });
            });
        --></script>
        <script type="text/javascript"><!--
            $(function () {
                $('#stats_browser').highcharts({
                    chart: { type: 'area'},
                    title: { text: 'Browser Visit Statistics'},
                    rangeSelector: {
                        enabled: true,
                        selected: 0,
                        buttons: [{
                            text: '1d',
                            type: 'day',
                            count: 1,
                        },
                        {
                            text: '1w',
                            type: 'day',
                            count: 7,
                        },
                        {
                            text: '1m',
                            type: 'month',
                            count: 1,
                        },
                        {
                            text: '1y',
                            type: 'year',
                            count: 1,
                        },
                        {
                            text: 'All',
                            type: 'all',
                            count: 1,
                        }],
                        buttonTheme: { style: { width: '120px' }},
                    },
                    navigator: {
                        enabled: true,
                        height: 20
                    },
                    legend: { enabled: false },
                    xAxis: { type: 'datetime', range: 5 * 24 * 3600 * 1000 },
                    yAxis: {
                        labels: {
                            formatter: function () {
                                return this.value / 1000;
                            }
                        }
                    },
                    tooltip: {
                        shared: true
                    },
                    plotOptions: {
                        area: {
                            stacking: 'normal',
                            lineColor: '#666666',
                            lineWidth: 1,
                            marker: {
                                lineWidth: 1,
                                lineColor: '#666666'
                            }
                        }
                    },
                    series: [{
                        name: 'Desktop',
                        data: {{web_stats['desktop']}},
                        stack: 'mobile'
                    }, {
                        name: 'Mobile',
                        data: {{web_stats['mobile']}},
                        stack: 'mobile'
                    }, {
                        name: 'Firefox',
                        data: {{web_stats['firefox']}},
                        stack: 'browser'
                    }, {
                        name: 'Chrome',
                        data: {{web_stats['chrome']}},
                        stack: 'browser'
                    }, {
                        name: 'Internet Explorer',
                        data: {{web_stats['ie']}},
                        stack: 'browser'
                    }, {
                        name: 'Opera',
                        data: {{web_stats['opera']}},
                        stack: 'browser'
                    }, {
                        name: 'Other',
                        data: {{web_stats['other']}},
                        stack: 'browser'
                    }]
                });
            });
        --></script>
        <script type="text/javascript"><!--
            $(function () {
                $('#stats_pages').highcharts({
                    chart: { type: 'area'},
                    title: { text: 'Pages Visit Statistics'},
                    rangeSelector: {
                        enabled: true,
                        selected: 0,
                        buttons: [{
                            text: '1d',
                            type: 'day',
                            count: 1,
                        },
                        {
                            text: '1w',
                            type: 'day',
                            count: 7,
                        },
                        {
                            text: '1m',
                            type: 'month',
                            count: 1,
                        },
                        {
                            text: '1y',
                            type: 'year',
                            count: 1,
                        },
                        {
                            text: 'All',
                            type: 'all',
                            count: 1,
                        }],
                        buttonTheme: { style: { width: '120px' }},
                    },
                    navigator: {
                        enabled: true,
                        height: 20
                    },
                    legend: { enabled: false },
                    xAxis: { type: 'datetime', range: 5 * 24 * 3600 * 1000 },
                    yAxis: {
                        labels: {
                            formatter: function () {
                                return this.value / 1000;
                            }
                        }
                    },
                    tooltip: {
                        shared: true
                    },
                    plotOptions: {
                        area: {
                            stacking: 'normal',
                            lineColor: '#666666',
                            lineWidth: 1,
                            marker: {
                                lineWidth: 1,
                                lineColor: '#666666'
                            }
                        }
                    },
                    series: [{
                        name: 'Main Page',
                        data: {{web_stats['index']}},
                        stack: 'page'
                    }, {
                        name: 'DashBoard',
                        data: {{web_stats['dash']}},
                        stack: 'page'
                    }, {
                        name: 'MOTD & Rules',
                        data: {{web_stats['motdrules']}},
                        stack: 'page'
                    }, {
                        name: 'Short URLs',
                        data: {{web_stats['shorturl']}},
                        stack: 'page'
                    }, {
                        name: 'Avatar & Signature',
                        data: {{web_stats['embed']}},
                        stack: 'page'
                    }, {
                        name: 'Vote TS',
                        data: {{web_stats['terrariaservers']}},
                        stack: 'page'
                    }, {
                        name: 'Vote TSW',
                        data: {{web_stats['tserverweb']}},
                        stack: 'page'
                    }, {
                        name: 'Vote List',
                        data: {{web_stats['votes']}},
                        stack: 'page'
                    }, {
                        name: '404',
                        data: {{web_stats['error']}},
                        stack: 'page'
                    }, {
                        name: 'World Map',
                        data: {{web_stats['world']}},
                        stack: 'page'
                    }, {
                        name: 'World Map VIP',
                        data: {{web_stats['worldvip']}},
                        stack: 'page'
                    },{% if user_data['staff'] %} {
                        name: 'Ban List',
                        data: {{web_stats['bans']}},
                        stack: 'page'
                    }, {
                        name: 'Logs',
                        data: {{web_stats['logs']}},
                        stack: 'page'
                    }, {
                        name: 'IRC Logs',
                        data: {{web_stats['irclogs']}},
                        stack: 'page'
                    }, {
                        name: 'Inventory Parser',
                        data: {{web_stats['invparser']}},
                        stack: 'page'
                    }, {
                        name: 'User Searcher',
                        data: {{web_stats['searchuser']}},
                        stack: 'page'
                    }{% endif %}]
                });
            });
        --></script>
        {%- endif %}
        {%- if backups %}
        <script type="text/javascript"><!--
            $(function () {
                $('#backups').highcharts({
                    chart: { type: 'areaspline' },
                    title: { text: 'Backup file size' },
                    rangeSelector: {
                        enabled: true,
                        selected: 2,
                        buttons: [{
                            text: '1d',
                            type: 'day',
                            count: 1,
                        },
                        {
                            text: '1w',
                            type: 'day',
                            count: 7,
                        },
                        {
                            text: '1m',
                            type: 'month',
                            count: 1,
                        },
                        {
                            text: '1y',
                            type: 'year',
                            count: 1,
                        },
                        {
                            text: 'All',
                            type: 'all',
                            count: 1,
                        }],
                        buttonTheme: { style: { width: '120px' }},
                    },
                    xAxis: { type: 'datetime', range: 7 * 24 * 3600 * 1000 },
                    yAxis: { // Regular Users Axis
                        title: { text: 'File Sizes in KiB' },
                        allowDecimals: false,
                        min: 0,
                    },
                    legend: {
                        enabled: true
                    },
                    series: [{
                        name: 'Server Files',
                        //color: '#00ff18',
                        lineWidth: 1,
                        marker: { symbol: "circle", radius: 3 },
                        data: {{backups[0]}},
                        fillColor : {
                            linearGradient : {
                                x1: 0,
                                y1: 0,
                                x2: 0,
                                y2: 1
                            },
                            stops : [
                                [0, Highcharts.getOptions().colors[0]],
                                [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                            ]
                        }
                    },
                    {
                        name: 'tShock DB',
                        color: '#00ff18',
                        lineWidth: 1,
                        marker: { symbol: "circle", radius: 3 },
                        data: {{backups[1]}},
                        fillColor : {
                            linearGradient : {
                                x1: 0,
                                y1: 0,
                                x2: 0,
                                y2: 1
                            },
                            stops : [
                                [0, '#84ff90'],
                                [1, Highcharts.Color('#84ff90').setOpacity(0).get('rgba')]
                            ]
                        }
                    },
                    {
                        name: 'tShock DB Weekly',
                        color: '#007711',
                        lineWidth: 1,
                        marker: { symbol: "circle", radius: 3 },
                        data: {{backups[2]}},
                        fillColor : {
                            linearGradient : {
                                x1: 0,
                                y1: 0,
                                x2: 0,
                                y2: 1
                            },
                            stops : [
                                [0, '#00d51e'],
                                [1, Highcharts.Color('#00d51e').setOpacity(0).get('rgba')]
                            ]
                        }
                    },
                    {
                        name: 'Website DB',
                        color: '#ff8a00',
                        lineWidth: 1,
                        marker: { symbol: "circle", radius: 3 },
                        data: {{backups[4]}},
                        fillColor : {
                            linearGradient : {
                                x1: 0,
                                y1: 0,
                                x2: 0,
                                y2: 1
                            },
                            stops : [
                                [0, '#ffc37d'],
                                [1, Highcharts.Color('#ffc37d').setOpacity(0).get('rgba')]
                            ]
                        }
                    },
                    {
                        name: 'htdocs',
                        color: '#ff0000',
                        lineWidth: 1,
                        marker: { symbol: "circle", radius: 3 },
                        data: {{backups[5]}},
                        fillColor : {
                            linearGradient : {
                                x1: 0,
                                y1: 0,
                                x2: 0,
                                y2: 1
                            },
                            stops : [
                                [0, '#ff7d7d'],
                                [1, Highcharts.Color('#ff7d7d').setOpacity(0).get('rgba')]
                            ]
                        },
                    },
                    ]
                });
            });
        --></script>
        {%- endif %}
    </body>
</html>
