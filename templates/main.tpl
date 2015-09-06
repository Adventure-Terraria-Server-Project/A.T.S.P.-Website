{% extends 'layout.tpl' %}
            {% block content %}
            <div class="row content">
                {%- if not user_data['mobile'] %}<div class="col-md-12 text-center">
                    <div class="jumbotron">
                        <h1 class="banner">Adventure Terraria Server Project</h1>
                        <div id="carousel" class="carousel slide" data-ride="carousel">
                            <!-- Indicators -->
                            <ol class="carousel-indicators">
                                {{ slider }}
                            </div>
                            <!-- Controls -->
                            <a class="left carousel-control" href="#carousel" role="button" data-slide="prev">
                                <span class="glyphicon glyphicon-chevron-left"></span>
                            </a>
                            <a class="right carousel-control" href="#carousel" role="button" data-slide="next">
                                <span class="glyphicon glyphicon-chevron-right"></span>
                            </a>
                        </div>
                        <br>
                        {%- if p_count %}
                        <div class="row render">
                            <p style="font-size: 14px">{{ p_list }}</p>
                        </div>
                        <div class="row">
                            <span class="label label-warning">Online Players {{ p_count['playercount'] }}</span>
                        </div>
                        {%- else %}
                        <div class="row">
                            <p>Server currently offline.</p>
                            <p>Please stay tuned!</p>
                        </div>
                        {%- endif %}
                        <br>
                        <div class="row">
                            <div class="btn-group">
                                <a href="#needhelp" data-toggle="modal" class="btn btn-danger">Need Help <span class="glyphicon glyphicon-question-sign"></span></a>
                                <a href="https://steamcommunity.com/groups/a_t_s_p/discussions" class="btn btn-primary"><span class="glyphicon glyphicon-tasks"></span> Forum</a>
                            </div>
                        </div><br>
                        <div class="row">
                            <div class="col-md-12">
                                <a href="steam://rungameid/105600//%20-j%20yamahi.eu%20-p%207878" class="btn btn-success btn-lg"><i class="fa fa-gamepad fa-lg"></i> Join A.T.S.P. Right Now! <i class="fa fa-gamepad fa-lg"></i></a>
                            </div>
                        </div><br>
                        <div class="row">
                            <div class="col-md-12 btn-group btn-group-justified">
                                <a target="_blank" class="btn btn-primary btn-sm" href="https://steamcommunity.com/groups/a_t_s_p"><i class="fa fa-steam-square fa-lg"></i> <strong>Join</strong> Steam Group</a>
                                <a target="_blank" class="btn btn-primary btn-sm" href="https://facebook.com/atsp.terraria"><i class="fa fa-facebook-square fa-lg"></i> <strong>Like</strong> on Facebook</a>
                                <a class="btn btn-success btn-sm" href="https://steamcommunity.com/groups/a_t_s_p/discussions/0/617335934135454248/"><span class="glyphicon glyphicon-gift"></span> <strong>Donate</strong> to support <strong>A.T.S.P.</strong></a>
                                <a target="_blank" class="btn btn-primary btn-sm" href="http://terraria-servers.com/server/7/vote/"><span class="glyphicon glyphicon-thumbs-up"></span> <strong>Vote</strong> on Terraria-Servers</a>
                                <a target="_blank" class="btn btn-primary btn-sm" href="http://www.tserverweb.com/terraria-server/285/like/"><span class="glyphicon glyphicon-star"></span> <strong>Vote</strong> on TServerWeb</a>
                            </div>
                        </div>
                    </div>
                </div>
                {%- else %}
                <div class="col-md-12 text-center">
                    <div>
                        <h4 class="text-primary">Adventure Terraria Server Project</h4>
                        <h6 class="label label-info">Online Players {{ p_count['playercount'] }}</h6>
                    </div><br>
                    <div class="row">
                        <div class="row">
                            <div class="btn-group">
                                <a href="#needhelp" data-toggle="modal" class="btn btn-danger btn-lg">Need Help <span class="glyphicon glyphicon-question-sign"></span></a>
                                <a href="https://steamcommunity.com/groups/a_t_s_p/discussions" class="btn btn-primary btn-lg"><span class="glyphicon glyphicon-tasks"></span> Forum</a>
                            </div>
                        </div><br>
                        <div class="row">
                            <div class="col-xs-12 btn-group btn-group-justified">
                                <a class="btn btn-success" href="https://steamcommunity.com/groups/a_t_s_p/discussions/0/617335934135454248/"><span class="glyphicon glyphicon-gift"></span> Donate</a>
                                <a class="btn btn-success" data-toggle="modal" href="#listModal"><i class="fa fa-eject fa-lg"></i> Vote</a>
                            </div>
                            <div class="col-xs-12 btn-group btn-group-justified">
                                <a target="_blank" class="btn btn-primary" href="http://terraria-servers.com/server/7/vote/"><span class="glyphicon glyphicon-thumbs-up"></span> TerrariaServers</a>
                                <a target="_blank" class="btn btn-primary" href="http://www.tserverweb.com/terraria-server/285/like/"><span class="glyphicon glyphicon-star"></span> TServerWeb</a>
                            </div>
                        </div>
                    </div>
                </div>
                {%- endif %}
                <div class="row">
                    <div class="col-md-6">
                        {%- if not user_data['mobile'] %}
                        <div class="panel-group" id="accordion">
                            <div class="panel panel-warning">
                                <div class="panel-heading" data-toggle="collapse" data-parent="#accordion" data-target="#collapseOne">
                                    <h4 class="panel-title"><span class="glyphicon glyphicon-question-sign fa-spin"></span> Need Help?</h4>
                                </div>
                                <div id="collapseOne" class="panel-collapse collapse">
                                    <div class="panel-body">
                                        <dl>
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
                                </div>
                            </div>
                            <div class="panel panel-success">
                                <div class="panel-heading" data-toggle="collapse" data-parent="#accordion" data-target="#collapseTwo">
                                    <h4 class="panel-title"><span class="glyphicon glyphicon-info-sign"></span> About this Server</h4>
                                </div>
                                <div id="collapseTwo" class="panel-collapse collapse in">
                                    <div class="panel-body">
                                        <ul>
                                            <li>ServerSideCharacter enabled.</li>
                                            <li>On Thursday hardmode will trigger when the <i>Wall of Flesh</i> is defeated on the server's current map, this continues until Sunday.</li>
                                            <li>The server World is reset every Sunday after 6 PM UTC, however the Ark and the Hotel will transfer.</li>
                                            <li><strong>Make sure you read <a href="https://steamcommunity.com/groups/a_t_s_p/discussions/0/617335934135479412/" target="_blank">the server rules here</a> to ensure you do not make any regrettable mistakes while enjoying your time on <i>A.T.S.P.</i></strong></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                        {%- endif %}
                        <br>
                        {%- if user_data['mobile'] %}
                        <div id="hardmodetime">
                            <h4>Time Left Until Hardmode is Available</h4>
                            <div class="hardmode hidden-xs progress">
                                <div id="hardmodeBar" class="progress-bar progress-bar-danger" role="progressbar"></div>
                            </div>
                            <span class="label label-danger" id="hardmodeText" title="Hardmode every Thursday 12 PM UTC"></span>
                            <h4>Time Left Until World Reset</h4>
                            <div class="worldreset hidden-xs progress">
                                <div id="worldResetBar" class="progress-bar progress-bar-info" role="progressbar"></div>
                            </div>
                            <span class="label label-info" id="worldResetText" title="Fresh world every Sunday after 6 PM UTC"></span>
                        </div>
                        <br>
                        {%- endif %}
                        <table class="table table-hover table-bordered table-striped jshide">
                            <tr>
                                <th style="color: red"><u>Server details</u></th>
                                <th style="color: green">Server</th>
                                <th style="color: green" class="hidden-xs" ><p class="irc" title="Click on 'Chat' to chat with us">IRC</p></th>
                                <th style="color: green" class="hidden-xs">Mumble</th>
                            </tr>
                            <tr>
                                <th style="color: blue">IP</th>
                                <td>yamahi.eu <a href="steam://rungameid/105600//%20-j%20yamahi.eu%20-p%207878" class="btn btn-info btn-xs pull-right hidden-xs"><span class="glyphicon glyphicon-globe"></span> Connect</a><br>[5.9.115.198]</td>
                                <td class="hidden-xs">yamahi.eu</td>
                                <td class="hidden-xs">neocomy.net</td>
                            </tr>
                            <tr>
                                <th style="color: blue">Port</th>
                                <td>7878</td>
                                <td class="hidden-xs">6667</td>
                                <td class="hidden-xs">64738</td>
                            </tr>
                            <tr>
                                <th style="color: blue">Channel</th>
                                <td><a target="_blank" href="https://youtube.com/user/theflame90">Youtube</a></td>
                                <td class="hidden-xs">#Yamaria</td>
                            </tr>
                        </table>
                        <div class="panel-group" id="accordiongroup">
                            <div class="panel panel-info">
                                <div class="panel-heading" data-parent="#accordiongroup" data-toggle="collapse" data-target="#collapseOnegroup">
                                    <h4 class="panel-title">
                                        <i class="fa fa-users fa-lg"></i> VIP
                                    </h4>
                                </div>
                                <div id="collapseOnegroup" class="panel-collapse collapse">
                                    <div class="panel-body">
                                        <table class="table-condensed">
                                            <tr>{{ groups['vips'] }}</tr>
                                        </table>
                                    </div>
                                </div>
                            </div>
                            <div class="panel panel-warning">
                                <div class="panel-heading" data-parent="#accordiongroup" data-toggle="collapse" data-target="#collapseTwogroup">
                                    <h4 class="panel-title">
                                        <i class="fa fa-users fa-lg"></i> Moderator
                                    </h4>
                                </div>
                                <div id="collapseTwogroup" class="panel-collapse collapse">
                                    <div class="panel-body">
                                        <table class="table-condensed">
                                            <tr>{{ groups['newadmins'] }}</tr>
                                        </table>
                                    </div>
                                </div>
                            </div>
                            <div class="panel panel-danger">
                                <div class="panel-heading" data-parent="#accordiongroup" data-toggle="collapse" data-target="#collapseThreegroup">
                                    <h4 class="panel-title">
                                        <i class="fa fa-users fa-lg"></i> Admin
                                    </h4>
                                </div>
                                <div id="collapseThreegroup" class="panel-collapse collapse">
                                    <div class="panel-body">
                                        <table class="table-condensed">
                                            <tr>{{ groups['admins'] }}</tr>
                                        </table>
                                    </div>
                                </div>
                            </div>
                            <div class="panel panel-default">
                                <div class="panel-heading" data-parent="#accordiongroup" data-toggle="collapse" data-target="#collapseFourgroup">
                                    <h4 class="panel-title">
                                        <i class="fa fa-users fa-lg"></i> Super Admin
                                    </h4>
                                </div>
                                <div id="collapseFourgroup" class="panel-collapse collapse">
                                    <div class="panel-body">
                                        <table class="table-condensed">
                                            <tr>{{ groups['superadmins'] }}</tr>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <br>
                    </div>
                    <div class="col-md-6">
                        {%- if not user_data['mobile'] %}
                        <div id="hardmodetime">
                            <h4>Time Left Until Hardmode is Available</h4>
                            <div class="hardmode progress progress-striped active">
                                <div id="hardmodeBar" class="progress-bar progress-bar-danger" role="progressbar"></div>
                            </div>
                            <span class="label label-danger" id="hardmodeText" title="Hardmode every Thursday 12 PM UTC"></span>
                            <h4>Time Left Until World Reset</h4>
                            <div class="worldreset progress progress-striped active">
                                <div id="worldResetBar" class="progress-bar progress-bar-info" role="progressbar"></div>
                            </div>
                            <span class="label label-info" id="worldResetText" title="Fresh world every Sunday after 6 PM UTC"></span>
                        </div>
                        <br>
                        {%- endif %}
                        <dl>
                            <dt>Adventure - Art - Community</dt>
                            <dd>A.T.S.P. is excited to present THE Terraria adventure server! Explore our worlds while stockpiling gear, make yourself a home to show off your hard work and finally, experience hardmode on the weekend to put your effort to the test. If this does not satisfy your adventuring desires, explore our mazes, beat our custom dungeons and make further use of our gameplay-extending features such as advanced wiring, custom statues and many more!</dd>
                            <dt>Be secure</dt>
                            <dd>Chests and other valuable objects are automatically protected upon placement, you can also protect whole buildings from change using our anti-grief plugins.</dd>
                            <dt>Professionally made server</dt>
                            <dd>The server is neither a home server nor a Hamachi server, we're a dedicated 24/7 root server hosted and manned by experienced adults. The server is even staffed with it's own developers!</dd>
                            <dt>Help us out</dt>
                            <dd>Although it's our hobby to host this server and let others have fun, this still comes at a price every month. While we force nobody to donate, we would be extremely grateful if you did. To encourage users to do so, everyone who donates 5 Euros or more recieves the special in-game rank "VIP". VIPs have access to more commands than regular players, can make use of more statues, own unlimited Bank Chests and more... Depending on the Donation-Type. <a href="https://steamcommunity.com/groups/a_t_s_p/discussions/0/617335934135454248/">Click Here</a>!</dd>
                        </dl>
                        <strong>Give it a try, join us and have some fun!</strong>
                    </div>
                </div>
            </div>
            <br>
            {%- endblock %}
