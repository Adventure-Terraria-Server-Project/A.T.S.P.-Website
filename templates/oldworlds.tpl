{% extends 'layout.tpl' %}
            {% block content %}
            <div class="row content">
                <div class="col-md-12">
                    <h2 class="text-success text-center">{{ name }}</h2>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>File</th>
                                    <th>Download</th>
                                </tr>
                            </thead>
                            <tbody class="infinite-scroll">
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <br>
            {%- endblock %}
