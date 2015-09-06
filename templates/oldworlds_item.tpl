{%- for item in worlds %}
<tr><td>{{ item[0] }}</td><td>{{ item[1] }}</td><td><a class="btn btn-primary" href="static/files/world/{{ item[1] }}">Download <span class="glyphicon glyphicon-download-alt"></span></a></td></tr>
{%- endfor %}
