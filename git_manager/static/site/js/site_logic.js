var app = angular.module('git_manager', ['ngRoute']);

app.config(function ($interpolateProvider) {
    //allow django templates and angular to co-exist
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

app.config(function ($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'static/partials/index.html',
            controller: 'RepsListController'
        })
        .when('/about', {
            templateUrl: 'static/partials/about.html'
        })
        .when('/rep/:userName/:repName', {
            templateUrl: 'static/partials/repository.html',
            controller: 'RepositoryController'
        })
        .otherwise({
            redirectTo: '/'
        });
});

app.controller('RepsListController', function ($scope, $http) {
    $http.get('http://localhost:8000/get_reps').success(function (data, status, headers, config) {
        $scope.reps = data;
        $scope.visibility_loading_indicator = "hide";
    }).error(function () {
        alert("CONNECTION ERROR!");
    });
});

app.controller('RepositoryController', function ($scope, $routeParams, $http) {
    $scope.repName = $routeParams.repName;
    $scope.userName = $routeParams.userName;

    $http({method: "GET", url: 'http://localhost:8000/get_rep_statistic', params: {"user_name": $routeParams.userName, "rep_name": $routeParams.repName}}).
        success(function (data, status) {
            $scope.visibility_loading_indicator = "hide";
            $scope.charsStatistic = data;
        }).
        error(function () {
            alert("CONNECTION ERROR!");
        });
});


// directive to display chart
app.directive('chart', function () {
    return {
        restrict: 'A',
        link: function ($scope, $elm, $attr) {
            // Create the data table.
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Chars');
            data.addColumn('number', 'Count');

            // wait until the data is loaded
            $scope.$watch('charsStatistic', function (newValue, oldValue) {
                if ($scope.charsStatistic) {
                    var data_rows = [];
                    for (var i = 0; i < $scope.charsStatistic.length; i++) {
                        data_rows.push([$scope.charsStatistic[i]["char"], $scope.charsStatistic[i]["count"]]);
                    }
                    data.addRows(data_rows);
                    // set chart options
                    var options = {'title': 'Statistic occurrence of symbols', height: data_rows.length * 30};

                    // instantiate and draw our chart, passing in some options.
                    var chart = new google.visualization.BarChart($elm[0]);
                    chart.draw(data, options);
                }
            });
        }
    }
});