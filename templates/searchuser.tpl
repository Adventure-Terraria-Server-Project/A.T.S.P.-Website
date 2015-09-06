{% extends 'layout.tpl' %}
            {% block content %}
            <div class="row content">
                <div class="col-md-12">
                    <h2 class="text-success text-center">{{ name }}</h2>
                </div>
                <div class="row">
                    <div class="col-md-3"></div>
                    <div class="col-md-6">
                        <form role="form" method="POST" action="/searchuser">
                            <div class="form">
                                <div class="col-md-8">
                                    <label for="nick">Search for a user</label>
                                    <input name="nick" type="text" class="form-control" id="nick" placeholder="User">
                                </div>
                            </div>
                            <div class="col-md-4">
                                <button style="margin-top: 10px" type="submit" class="btn btn-lg btn-primary"><span class="glyphicon glyphicon-search"></span> Search</button>
                            </div>
                        </form>
                    </div>
                    {%- if result %}
                    <div class="col-md-12">{{ result }}</div>
                    {%- endif %}
                </div>
            </div>
            <br>
            {%- endblock %}