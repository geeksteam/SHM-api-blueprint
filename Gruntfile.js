

module.exports = function(grunt){
  // Load grunt tasks automatically
  require('load-grunt-tasks')(grunt);

    var apibType = grunt.option('type') || '';
    if ( apibType === '' ) {
        apibType = 'all';
    }

    grunt.initConfig({
        exec: {
            // Remove tabs
            removetabs: [ 'perl', '-p', '-i', '-e', '"s/\t/  /g"', 'apiary.apib' ].join(' '),
            // exec Make
            makeapib: [ './_bin/MakeApib', apibType, './apiary.apib' ].join(' ')
        },
        watch: {
            scripts: {
                files: ['**/*.apib'],
                tasks: ['exec:makeapib','exec:removetabs'],
                options: {
                    spawn: false,
                },
            },
        }
    });
    grunt.loadNpmTasks('grunt-env');
    grunt.loadNpmTasks('grunt-exec');
    grunt.registerTask('default', [ 'watch' ]);
    grunt.registerTask('build', ['exec:makeapib','exec:removetabs']);
};
