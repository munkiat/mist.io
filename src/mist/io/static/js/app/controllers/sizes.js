define('app/controllers/sizes', ['app/models/size'],
    //
    //  Sizes Controller
    //
    //  @returns Class
    //
    function (Size) {

        'use strict';

        return Ember.ArrayController.extend(Ember.Evented, {


            //
            //
            //  Properties
            //
            //


            loading: null,
            backend: null,


            //
            //
            //  Initialization
            //
            //


            init: function () {
                this._super();
                this.set('loading', true);
            },


            //
            //
            //  Methods
            //
            //


            load: function (sizes) {
                this._updateContent(sizes);
                this.set('loading', false);
            },


            getSize: function (sizeId) {
                return this.findBy('id', sizeId);
            },


            //
            //
            //  Pseudo-Private Methods
            //
            //


            _updateContent: function (sizes) {
                Ember.run(this, function () {

                    // Remove deleted sizes
                    this.forEach(function (size) {
                        if (!sizes.findBy('id', size.id))
                            this.removeObject(size);
                    }, this);

                    sizes.forEach(function (size) {

                        var oldSize = this.getSize(size.id);

                        if (oldSize)
                            // Update existing sizes
                            forIn(size, function (value, property) {
                                oldSize.set(property, value);
                            });
                        else
                            // Add new sizes
                            this._addSize(size);
                    }, this);

                    this.trigger('onSizeListChange');
                });
            },


            _addSize: function (size) {
                Ember.run(this, function () {
                    this.addObject(Size.create(size));
                    this.trigger('onSizeAdd');
                });
            },


            _deleteSize: function (sizeId) {
                Ember.run(this, function () {
                    this.removeObject(this.getSize(sizeId));
                    this.trigger('onSizeDelete');
                });
            }
        });
    }
);
