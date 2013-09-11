var api_call = function(query) {

    $.getJSON('/api?studio=' + query)
    .done(function(data) {
        var name = data['studio_name'];
        var classes = data['class_list'];

        var class_table = $("#class_table").find('tbody');

        class_table.append('<tr><td><b>' + name + '</b></td></tr>');

        $.each(classes, function(index, val) {
            var row = '<tr><td>' + val['class_name'] + '</td>' +
                      '<td>' + val['start_time'] + '</td>' +
                      '<td>' + val['end_time'] + '</td></tr>';
            class_table.append(row);
        });
    })
    .fail(function() {
        console.log("failed")
    });
}