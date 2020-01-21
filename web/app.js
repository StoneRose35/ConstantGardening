
angular.module('gardener', [])
.controller('HumController', function($scope, $http) {
    $http.get('/humidities/10').
        then(function(response) {
            $scope.humidities = response.data;
        });
})
.controller('BrightnessController', function($scope, $http) {
    $http.get('/brightnesses/10').
        then(function(response) {
            $scope.brightnesses = response.data;
        });
})
.controller('AnotherController', function($scope) {
    $scope.magic_number = 42;
})
;
