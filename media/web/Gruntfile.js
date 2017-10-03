/*
 *  - v - Gruntfile.js
 * home: http://www.haoku.net/
 * Copyright (c) 2015 XiaoKu Inc. All Rights Reserved.
 */

'use strict';

module.exports = function (grunt) {

	grunt.initConfig({
		pkg: grunt.file.readJSON('web.json'),

		banner: '/*\n * <%= pkg.name %> - v<%= pkg.version %> - ' +
			'<%= grunt.template.today("yyyy-mm-dd") %>\n' +
			'<%= pkg.homepage ? " * home: " + pkg.homepage + "\\n" : "" %>' +
			' * Copyright (c) <%= grunt.template.today("yyyy") %> <%= pkg.author.name %>' +
			' All Rights Reserved.\n */\n',

		clean: {
			files: [
				'dist/js/*.js',
				'dist/css/*.css',
				'dist/img/**',
			],
		},

		concat: {
			options: {
				banner: '<%= banner %>',
			},
			editor: {
				src: [
					'src/js/editor.js',
				],
				dest: 'dist/js/editor.js',
			},
			dist: {
				src: [
					'src/js/cool.js',
					'src/js/check.js',
					'src/js/users.js',
					'src/js/web.js',
				],
				dest: 'dist/js/<%= pkg.name %>.js',
			},
		},

		uglify: {
			options: {
				banner: '<%= banner %>',
			},
			ie8: {
				src: [
					'bower_components/html5shiv/dist/html5shiv.min.js',
					'bower_components/respond/dest/respond.min.js',
					'bower_components/respond/dest/respond.matchmedia.addListener.min.js',
				],
				dest: 'dist/js/ie8.min.js',
			},
			editor: {
				src: [
					'bower_components/select2/dist/js/select2.full.min.js',
					'bower_components/select2/dist/js/i18n/zh-CN.js',
                    'libs/likedown/js/flowchart-1.4.0.js',
		            'libs/raphael.js',
		            'bower_components/underscore/underscore-min.js',
		            'bower_components/js-sequence-diagrams/build/sequence-diagram-min.js',
		            'bower_components/MathJax/MathJax.js',
		            'bower_components/MathJax/config/TeX-AMS_HTML.js',
		            'libs/likedown/js/likedown-ext.js',
		            'dist/js/editor.js',
				],
				dest: 'dist/js/editor.min.js',
			},
			dist: {
				src: [
					'bower_components/jquery/dist/jquery.min.js',
					'bower_components/jquery-form/jquery.form.js',
					'bower_components/jquery-tmpl/jquery.tmpl.js',
					'libs/bootstrap/js/bootstrap.min.js',
					'libs/highlight/highlight.pack.js',
					'libs/area.js',
					'<%= concat.dist.dest %>',
				],
				dest: 'dist/js/<%= pkg.name %>.min.js',
			},
		},

		jshint: {
			gruntfile: {
				options: {
					jshintrc: 'grunt/.jshintrc',
				},
				src: 'Gruntfile.js',
			},
			js: {
				options: {
					jshintrc: 'src/js/.jshintrc',
				},
				src: 'src/js/*.js',
			},
		},

		less: {
			options: {
				banner: '<%= banner %>',
			},
			dist: {
				files: {
					'dist/css/<%= pkg.name %>.css': 'src/less/web.less',
				},
			},
		},

		cssmin: {
			optioins: {
				banner: '<%= banner %>',
			},
			dist: {
				files: {
					'dist/css/<%= pkg.name %>.min.css': [
						'libs/bootstrap/css/bootstrap.min.css',
						'libs/highlight/styles/github.css',
        				'bower_components/select2/dist/css/select2.min.css',
						'libs/likedown/css/likedown.css',
						'dist/css/<%= pkg.name %>.css',
					],
				},
			},
		},

		watch: {
			gruntfile: {
				files: '<%= jshint.gruntfile.src %>',
				tasks: ['jshint:gruntfile'],
			},
			js: {
				files: '<%= jshint.js.src %>',
				tasks: ['concat', 'jshint:js'],
			},
			css: {
				files: 'src/less/*.less',
				tasks: ['less'],
			},
		},

		copy: {
			fonts: {
				expand: true,
				cwd: 'libs/bootstrap',
				src: 'fonts/*',
				dest: 'dist/',
			},
			likedown_img: {
				expand: true,
				src: 'libs/likedown/img/**',
				dist: 'dist/'
			},
			img: {
				expand: true,
				src:'img/**',
				dest: 'dist/',
			}
		},
	});

	require('load-grunt-tasks')(grunt);
	require('time-grunt')(grunt);

	grunt.registerTask('dist-css', ['less', 'cssmin']);
	grunt.registerTask('dist-js', ['concat', 'uglify']);
	grunt.registerTask('dist-copy', ['copy']);
	grunt.registerTask('build', ['clean', 'dist-css', 'dist-js', 'dist-copy']);
	grunt.registerTask('default', ['build']);

};