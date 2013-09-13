var api_call = function(query) {
    $.getJSON('/api?studio=' + query, function(data) {
        var name = data['studio_name'];
        var classes = data['class_list'];
        var link = data['link'];

        var class_table = $("#class_table").find('tbody');

        if (classes.length == 0) {
            class_table.append('<tr><th><a href="' + link +
                        '">No more classes at ' + name + ' today</th></tr>');
        } else {
            var header = '<tr><th><a href="' + link + '">' + name + '</th>' +
                         '<th>Start Time</th>' +
                         '<th>End Time</th></tr>';
            class_table.append(header);

            $.each(classes, function(index, val) {
                var row = '<tr><td>' + val['class_name'] + '</td>' +
                          '<td>' + val['start_time'] + '</td>' +
                          '<td>' + val['end_time'] + '</td></tr>';
                class_table.append(row);
            });
        }
    })
    .done(function(data) {
        $("#loading").hide();
    })
    .fail(function() {
        console.log("failed");
    });
}