{% extends 'layout.tpl' %}
            {% block content %}
            <div class="row content">
                <div class="col-md-12 text-center">
                    <h2 class="text-success">{{ name }}</h2>
                </div>
                <br>
                <div class="row text-center">
                    <form role="form" method="POST" action="/invpars">
                        <div class="form">
                            <div class="col-md-8">
                                <label for="nick">Search for a offline user</label>
                                <input name="nick" type="text" class="form-control" id="nick" placeholder="User">
                            </div>
                        </div>
                        <div class="col-md-4">
                            <button style="margin-top: 10px" type="submit" class="btn btn-lg btn-primary"><span class="glyphicon glyphicon-search"></span> Search</button>
                        </div>
                    </form>
                    {%- if inventory %}
                    <div class="col-md-12 text-center">
                        <h3 class="text-warning"><span class="text-danger glyphicon glyphicon-heart"></span> {{ inventory['health'] }} <span class="text-primary glyphicon glyphicon-star"></span> {{ inventory['mana'] }} <i class="text-info fa fa-users"></i> {{ inventory['group'] }}</h3>
                        <table class="table table-bordered"><tr>{{ inventory['inv'] }}</tr></table>
                    </div>
                    {%- endif %}
                    <div class="col-md-12">
                        <div class="panel-group" id="pinv">
                            {{ p_list }}
                        </div>
                    </div>
                </div>
            </div>
            <br>
            {%- endblock %}
