// Karma configuration
// Generated on Tue Feb 02 2016 22:09:42 GMT-0500 (EST)

module.exports = function(config) {
  config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',


    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],


    // list of files / patterns to load in the browser
    files: [
      //can't get karma to pull in cdn deps, storing a copy for the tests in lib
      'lib/js/jquery.2.2.0.min.js',
      'lib/js/angular.1.3.15.min.js',
      'lib/js/angular-cookies.1.3.15.min.js',
      'lib/js/angular-resource.1.3.15.min.js',
      
      'lib/js/angular-mocks.1.3.15.js',
      '../static/js/template_app/global/app_init.js',
      '../static/js/template_app/**/*.js',
      'tests/**/*.js'
    ],


    // list of files to exclude
    exclude: [
    ],

    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
        '../static/js/template_app/**/*.js': 'coverage',
    },


    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress', 'coverage'],


    coverageReporter: {
        type: 'html',
        dir: '../../reports/js_coverage',
        instrumenterOptions: {
            istanbul: { noCompact: true }
        },
        check: {
            global: {
                statements:53,
                branches: 0,
                functions: 41,
                lines: 53,
            },
        }
    },
    
    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: ['PhantomJS'],


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: true,

    // Concurrency level
    // how many browser should be started simultaneous
    concurrency: Infinity
  })
}
