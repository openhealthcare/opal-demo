
    module.exports =  function(config){
    config.set({
        frameworks: ['jasmine'],
        browsers: ['Chrome'],
        basePath:  '../../opal/opal/static/js',

        files: [
            //JASMINE,
            //JASMINE_ADAPTER,
            'angular-1.2.11/angular.js',
            'angular-1.2.11/angular-route.js',
            'angular-1.2.11/angular-resource.js',
            'angular-1.2.11/angular-cookies.js',
            'angular-1.2.11/angular-mocks.js',
            'angular-1.2.11/angular-mocks.js',
            'angular-ui-utils-0.1.0/ui-utils.js',
            'angular-ui-bootstrap-0.10.0/ui-bootstrap-tpls.js',
            'angular-strap-2.0.0-rc.2/modules/tooltip.js',
            'angular-strap-2.0.0-rc.2/modules/tooltip.tpl.js',
            'angular-strap-2.0.0-rc.2/modules/dimensions.js',
            'angular-strap-2.0.0-rc.2/modules/parse-options.js',
            'angular-strap-2.0.0-rc.2/modules/typeahead.js',
            'angular-strap-2.0.0-rc.2/modules/typeahead.tpl.js',
            'jquery-1.11.0/jquery.js',
            'utils/underscore.js',
            'utils/moment.js',
            'opal/utils.js',
            'opal/directives.js',
            'opal/filters.js',
            'opal/services.js',
            'opal/controllers.js',
            'opal/app.js',
            '../../../../elcid/elcid/assets/js/elcid/*.js',
            'opaltest/*.js',
            '../../../../elcid/elcid/assets/js/elcidtest/*.js',
        ],

        preprocessors: {
            '**/opal/*.js': 'coverage'
        },

        reporters: ['progress', 'coverage'],

        autoWatch: true,

        coverageReporter: {
            type : 'html',
            dir : '../../../coverage-js/',
        },

    })
}
