define('app/controllers/logs', ['app/models/log', 'ember'],
    //
    //  Logs Controller
    //
    //  @returns Class
    //
    function (Log) {

        'use strict';

        return Ember.ArrayController.extend(Ember.Evented, {


            //
            //
            //  Properties
            //
            //


            loading: null,


            //
            //
            //  Pseudo-Private Methods
            //
            //


            _reload: function () {
                Ember.run.later(this, function () {
                    this.load();
                }, 2000);
            },


            _setContent: function (logs) {
                Ember.run(this, function () {
                    var newContent = [];
                    logs.forEach(function (log) {
                        newContent.push(Log.create(log));
                    });
                    this.clear();
                    this.pushObjects(newContent);
                    this.trigger('onLogListChange');
                });
            },


            _prependContent: function (logs) {
                Ember.run(this, function () {
                    var additionalContent = [];
                    logs.forEach(function (log) {
                        additionalContent.push(Log.create(log));
                    });
                    this.unshiftObjects(additionalContent);
                    this.trigger('onLogListChange');
                });
            },


            _appendContent: function (logs) {
                Ember.run(this, function () {
                    var additionalContent = [];
                    logs.forEach(function (log) {
                        additionalContent.push(Log.create(log));
                    });
                    this.pushObjects(additionalContent);
                    this.trigger('onLogListChange');
                });
            }
        });
    }
);
