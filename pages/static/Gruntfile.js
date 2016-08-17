lib = require('bower-files')({
    overrides: {
        modernizr: {
            main: 'modernizr.js',
            dependencies: {}
        }
    }
});

module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        coffee: {
            compileJoined: {
                options : {
                    join: true,
                    sourceMap: true
                },
                files: {
                    'build/javascript/pages-coffee.js': ['**/coffee/*.coffee']  // concat then compile into single file
                }
            }
        },
        sass: {
            dist: {
                options: {
                    compass: true,
                    require: 'susy'
                },
                files: [{
                    expand: true,
                    cwd: 'sass',
                    src: ['**/*.scss'],
                    dest: './build/css',
                    ext: '.css'
                }]
            }
        },
        watch: {
            reload: {
                files: ['**/*.css', '**/js/**/*.js'],
                options: {
                    livereload: true
                }
            },
            css: {
                files: '**/*.scss',
                tasks: ['sass']
            },
            coffee: {
                files: '**/coffee/*.coffee' ,
                tasks: ['coffee']
            },
            //ts: {
            //    files: ['**/typescript/**/*.ts', "!node_modules/**/*.ts", "!typings/main", "!typings/main.d.ts"],
            //    tasks: ['ts']
            //},
            pages: {
                files: ['**/js/**/*.js'],
                tasks: ['concat']
            }
        },
        concat: {
            pages: {
                src: ['**/js/**/*.js'],
                dest: 'build/javascript/pages.js'
            }
        },
        uglify: {
            options: {
                sourceMap: true,
                banner: '/*! <%= pkg.name %> */\n'
            },
            bower_components: {
                files: {
                    'build/lib.min.js': lib.ext('js').files
                }
            },
            pages: {
                files: {
                    'build/pages.min.js': 'build/javascript/pages.js'
                }
            }
        },
        ts: {
            default: {
                src: ['typescript/**/*.ts', "!node_modules/**/*", "!typings/main", "!typings/main.d.ts"],
                tsconfig: true,
                options: {

                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-coffee');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks("grunt-ts");

    //grunt.registerTask('concat-dashboard', ['concat:dashboard_js', 'uglify:dashboard_js']);
    grunt.registerTask('build', ['sass', 'concat', 'uglify']);
    grunt.registerTask('default', ['sass', 'watch'])
};
