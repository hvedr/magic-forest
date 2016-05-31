angular.module('magicForestApp', [])
    .controller('ConfigurationController', function($scope, $http){
        $scope.size = {
            'width': 1003,
            'hight': 1000
        }

        $scope.image_url = "/static/img/rendered/example.jpg";

        $scope.generate = function(item, event){
            var promise = $http.post("/generate/", $scope.size);

            promise.success(function(data, status, headers, config) {
                $('#res_image').attr('src', data.url);
                $scope.image_url = data.url;
            });
            promise.error(function(data, status, headers, config) {
                alert("Generation failed!");
            });
        }
    }
);
