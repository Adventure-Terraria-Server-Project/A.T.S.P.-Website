{% extends 'layout.tpl' %}
            {% block content %}
            <div class="row content">
                <div class="col-md-12">
                    <h2 class="text-success text-center">{{ name }}</h2>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div class="text-center alert alert-warning">Use <strong>www.s.yamahi.eu</strong> to access short URLs</div>
                        <dl class="dl-horizontal">
                            {{ url_config }}
                        </dl>
                    </div>
                </div>
                {%- if staff %}
                <div class="row">
                    <div class="col-md-12">
                        <form role="form" method="POST" action="/shorturl">
                            <div class="form-group">
                                <div class="col-md-3">
                                    <label for="surl">Short URL</label>
                                    <input name="surl" type="text" class="form-control" id="surl" placeholder="Short URL">
                                </div>
                                <div class="col-md-9">
                                    <label for="url">Long URL</label>
                                    <input name="url" type="url" class="form-control" id="url" placeholder="Long URL">
                                </div>
                            </div>
                            <div class="row text-center">
                                <button style="margin-top: 10px" type="submit" class="btn btn-lg btn-primary"><span class="glyphicon glyphicon-floppy-disk"></span> Save</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            {%- endif %}
            <br>
            {%- endblock %}