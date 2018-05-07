// URLs REST
angular.module(
    'taResource', ['ngResource']
).factory(
    'tonDataAccess', function ($resource) {
        var url = "/ton/url";

        return $resource(
            url, {}, { update: { method: 'PUT'} }
        );
    }
);

angular.module(
    'tonApp', ["taResource"]
);

function tonController($scope, taResource) {
    var params = {};
    taResource.save(params, function(data){ /* ton callback*/ });
    taResource.query({id:2});
    taResource.update(params);
    taResource.delete(params);
}
